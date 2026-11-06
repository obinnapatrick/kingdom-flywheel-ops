"""Funnel, A/B, profile-version and goal-pacing analytics, plus rule-based insights."""
import calendar
import math
from datetime import date

from . import db, scoring

MIN_N = 10  # below this many sent proposals, rates are noise


def _rate(n, d):
    return round(n / d, 3) if d else None


def _stats(rows):
    sent = len(rows)
    viewed = sum(1 for r in rows if r["stage_reached"] >= 1)
    interview = sum(1 for r in rows if r["stage_reached"] >= 2)
    hired = sum(1 for r in rows if r["stage_reached"] >= 3)
    connects = sum(r["connects_spent"] or 0 for r in rows)
    return {"sent": sent, "viewed": viewed, "interview": interview, "hired": hired,
            "view_rate": _rate(viewed, sent), "interview_rate": _rate(interview, sent),
            "win_rate": _rate(hired, sent), "connects": connects,
            "connects_per_interview": round(connects / interview, 1) if interview else None,
            "connects_per_hire": round(connects / hired, 1) if hired else None}


def sent_rows(conn):
    return [dict(r) for r in conn.execute("SELECT * FROM proposals WHERE status != 'draft'").fetchall()]


def funnel(conn):
    return _stats(sent_rows(conn))


def by_variant(conn):
    rows = sent_rows(conn)
    return {v: _stats([r for r in rows if r["variant"] == v]) for v in sorted({r["variant"] for r in rows})}


def by_profile_version(conn):
    rows = sent_rows(conn)
    notes = {r["id"]: r["note"] for r in db.list_versions(conn)}
    out = []
    for v in sorted({r["profile_version"] for r in rows if r["profile_version"] is not None}):
        s = _stats([r for r in rows if r["profile_version"] == v])
        s.update(version=v, note=notes.get(v, ""))
        out.append(s)
    return out


def month_of(d=None):
    return (d or date.today()).strftime("%Y-%m")


def pacing(conn, today=None):
    """What activity this month's revenue goal implies, using a smoothed win rate."""
    today = today or date.today()
    month = month_of(today)
    goal = db.get_goal(conn, month)
    earned = conn.execute("SELECT COALESCE(SUM(amount),0) AS s FROM earnings WHERE substr(date,1,7)=?",
                          (month,)).fetchone()["s"]
    rows = sent_rows(conn)
    st = _stats(rows)
    # Bayesian-ish smoothing: prior of ~10% win rate worth 20 proposals, so early luck/bad luck doesn't swing the plan.
    win_rate = (st["hired"] + 2) / (st["sent"] + 20)
    remaining = max(goal["revenue_target"] - earned, 0)
    hires_needed = math.ceil(remaining / goal["avg_contract_value"]) if remaining else 0
    proposals_needed = math.ceil(hires_needed / win_rate) if hires_needed else 0
    days_in_month = calendar.monthrange(today.year, today.month)[1]
    days_left = days_in_month - today.day + 1
    per_week = round(proposals_needed / (days_left / 7), 1) if proposals_needed else 0
    sent_month = sum(1 for r in rows if (r["sent_at"] or "")[:7] == month)
    avg_connects = (st["connects"] / st["sent"]) if st["sent"] else 0
    return {"month": month, "revenue_target": goal["revenue_target"], "avg_contract_value": goal["avg_contract_value"],
            "earned": earned, "remaining": remaining, "win_rate_used": round(win_rate, 3),
            "hires_needed": hires_needed, "proposals_needed": proposals_needed, "per_week": per_week,
            "days_left": days_left, "sent_this_month": sent_month,
            "connects_needed": round(proposals_needed * avg_connects) if avg_connects else None,
            "note": "Proposals sent today mostly pay out in later weeks, so keep volume steady rather than cramming."}


def insights(conn):
    out = []
    add = lambda level, title, detail: out.append({"level": level, "title": title, "detail": detail})
    profile = db.get_profile(conn)
    jobs = db.list_jobs(conn)
    audit = scoring.audit_profile(profile, jobs)
    st = funnel(conn)

    if audit["score"] < 75:
        for p in audit["priorities"]:
            add("action", f"Profile: {p['label']}", f"+{p['gain']} pts available. {p['advice']}")
    if audit["missing_keywords"]:
        add("action", "Profile is missing in-demand skills",
            "Jobs you saved ask for: " + ", ".join(audit["missing_keywords"][:6]) + ". Add those you can truly deliver.")

    if st["sent"] < MIN_N:
        add("info", "Not enough data yet",
            f"{st['sent']} proposals sent. Send at least {MIN_N} before drawing conclusions; rates below that are noise.")
    else:
        if st["view_rate"] is not None and st["view_rate"] < 0.3:
            add("action", "Few clients are opening your proposals",
                f"View rate {st['view_rate']:.0%}. Work on the first two lines of your proposals and your profile title/hook, "
                "and be more selective about crowded, low-quality-client jobs.")
        elif st["view_rate"] is not None and st["interview_rate"] is not None and st["interview_rate"] < 0.1:
            add("action", "Views aren't turning into conversations",
                f"{st['view_rate']:.0%} view but {st['interview_rate']:.0%} interview. Tighten the pitch: one proof point, "
                "one specific question, and check price positioning.")
        if st["interview"] >= 3 and st["hired"] / st["interview"] < 0.25:
            add("action", "Interviews aren't closing",
                f"{st['hired']} hires from {st['interview']} interviews. Prepare a scoped plan before calls and "
                "propose a small paid first milestone.")
        if st["connects_per_hire"]:
            add("info", "Connects efficiency", f"~{st['connects_per_hire']} connects per hire so far.")

    var = by_variant(conn)
    if len(var) >= 2 and all(v["sent"] >= 8 for v in var.values()):
        ranked = sorted(var.items(), key=lambda kv: (kv[1]["interview_rate"] or 0), reverse=True)
        (a, sa), (b, sb) = ranked[0], ranked[1]
        if (sa["interview_rate"] or 0) > (sb["interview_rate"] or 0):
            add("info", f"Variant '{a}' is ahead",
                f"Interview rate {sa['interview_rate']:.0%} vs {sb['interview_rate']:.0%} for '{b}'. "
                "Small samples can mislead; keep testing before dropping one.")
    elif var:
        add("info", "A/B test running", "Each proposal variant needs 8+ sent before the comparison means anything.")

    p = pacing(conn)
    if p["remaining"] > 0:
        add("action" if p["per_week"] > 0 else "info", "Goal pacing",
            f"${p['remaining']:,.0f} left of ${p['revenue_target']:,.0f} this month. At a {p['win_rate_used']:.0%} win rate you need "
            f"~{p['proposals_needed']} more proposals (~{p['per_week']}/week) for {p['hires_needed']} hire(s).")
    else:
        add("info", "Monthly goal reached", f"${p['earned']:,.0f} earned. Keep the pipeline warm for next month.")
    return out


def dashboard(conn):
    profile = db.get_profile(conn)
    jobs = db.list_jobs(conn)
    return {"profile_audit": scoring.audit_profile(profile, jobs), "funnel": funnel(conn), "pacing": pacing(conn),
            "insights": insights(conn), "variants": by_variant(conn), "versions": by_profile_version(conn)}


def weekly_report(conn):
    d = dashboard(conn)
    f, p, a = d["funnel"], d["pacing"], d["profile_audit"]
    lines = [f"# Upwork weekly report ({date.today().isoformat()})", "",
             f"**Profile score:** {a['score']}/100  ·  **Earned this month:** ${p['earned']:,.0f} of ${p['revenue_target']:,.0f}",
             f"**Funnel:** {f['sent']} sent → {f['viewed']} viewed → {f['interview']} interviews → {f['hired']} hired", "",
             "## Do this week"]
    for i in d["insights"]:
        if i["level"] == "action":
            lines.append(f"- **{i['title']}**: {i['detail']}")
    lines += ["", "## FYI"] + [f"- **{i['title']}**: {i['detail']}" for i in d["insights"] if i["level"] != "action"]
    return "\n".join(lines)

"""Job-fit scoring, red-flag detection, job-text parsing and profile audit. Pure functions."""
import re
from collections import Counter
from datetime import datetime, timezone

STOP = set("""a an the and or for to of in on with we you your our is are be will this that it as at by from have has
i need looking want who can must should it's i'm about into their they them us not but if so do does""".split())

RED_FLAGS = [
    (r"\b(whatsapp|telegram|skype|signal app|discord dm)\b|outside (of )?upwork|off[- ]?platform|"
     r"(email|contact|message|text) me (at|on|outside)", "Asks to move off-platform (ToS risk, no payment protection)"),
    (r"\bfree (sample|trial|test|work|mockup)\b|unpaid (test|trial|sample)|for exposure|test project.{0,30}unpaid",
     "Unpaid test work requested"),
    (r"(share|lend|rent|sell|buy)\w* .{0,25}(upwork )?account|use my (upwork )?account|verified account|"
     r"(identity|id) verif\w+ .{0,20}(for me|on my behalf)",
     "Account sharing/renting requested (violates Upwork ToS, can get you banned)"),
    (r"\b(crypto (giveaway|investment)|guaranteed returns?|pay (you )?in gift ?cards?|send (me )?money first)\b",
     "Possible scam language"),
]


def tokens(text):
    out = []
    for t in re.findall(r"[a-z0-9+#.\-]{2,}", (text or "").lower()):
        t = t.strip(".-")
        if len(t) >= 2 and t not in STOP:
            out.append(t)
    return out


def norm_skill(s):
    return re.sub(r"\s+", " ", (s or "").strip().lower())


def _hours_since(iso, now=None):
    if not iso:
        return None
    try:
        dt = datetime.fromisoformat(str(iso).replace("Z", "+00:00"))
    except ValueError:
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    now = now or datetime.now(timezone.utc)
    return max((now - dt).total_seconds() / 3600, 0)


def detect_red_flags(job):
    text = f"{job.get('title', '')}\n{job.get('description', '')}"
    return [label for pat, label in RED_FLAGS if re.search(pat, text, re.I | re.S)]


def _skill_match(job, profile):
    prof_skills = {norm_skill(s) for s in profile.get("skills", [])}
    prof_text = f"{profile.get('title', '')} {profile.get('overview', '')} {profile.get('niche', '')}".lower()
    job_skills = [norm_skill(s) for s in job.get("skills", []) if s.strip()]
    desc = f"{job.get('title', '')} {job.get('description', '')}".lower()
    if job_skills:
        hit = [s for s in job_skills if s in prof_skills or re.search(r"(?<![a-z0-9])" + re.escape(s) + r"(?![a-z0-9])", prof_text)]
        ratio = len(hit) / len(job_skills)
        return ratio, hit, [s for s in job_skills if s not in hit]
    hit = [s for s in prof_skills if s and re.search(r"(?<![a-z0-9])" + re.escape(s) + r"(?![a-z0-9])", desc)]
    return min(len(hit) / 3, 1.0), hit, []


def score_job(job, profile, now=None):
    """Return {score 0-100, decision bid|maybe|skip, parts, flags, reasons}."""
    reasons, parts = [], {}

    ratio, hit, missing = _skill_match(job, profile)
    parts["skills"] = round(40 * ratio)
    if ratio >= 0.75:
        reasons.append(f"Strong skill match ({len(hit)} overlapping skills)")
    elif ratio < 0.4:
        reasons.append("Weak skill match; you would be competing outside your niche")
    if missing:
        reasons.append("Skills you don't list: " + ", ".join(missing[:5]))

    rate = float(profile.get("hourly_rate") or 0)
    bmax, bmin = job.get("budget_max"), job.get("budget_min")
    if job.get("budget_type") == "fixed":
        floor = float(profile.get("min_fixed_budget") or 300)
        amount = bmax if bmax is not None else bmin
        if amount is None:
            b = 8
        elif amount >= 3 * floor:
            b = 15
        elif amount >= floor:
            b = 11
        else:
            b = 3
            reasons.append(f"Budget ${amount:,.0f} is below your ${floor:,.0f} minimum")
    else:
        top = bmax if bmax is not None else bmin
        if top is None or rate <= 0:
            b = 8
        elif top >= rate:
            b = 15
        elif top >= 0.8 * rate:
            b = 9
        else:
            b = 3
            reasons.append(f"Top of range ${top:g}/hr is well under your ${rate:g}/hr")
    parts["budget"] = b

    q = 0
    v = job.get("client_verified")
    q += 8 if v == 1 else (4 if v is None else 0)
    if v == 0:
        reasons.append("Payment method not verified")
    sp = job.get("client_spend")
    q += 3 if sp is None else (6 if sp >= 50000 else 5 if sp >= 10000 else 3 if sp >= 1000 else 1 if sp > 0 else 0)
    hr = job.get("client_hire_rate")
    q += 2 if hr is None else (5 if hr >= 60 else 3 if hr >= 40 else 1)
    rt = job.get("client_rating")
    q += 3 if rt is None else (6 if rt >= 4.8 else 4 if rt >= 4.5 else 2 if rt >= 4.0 else 0)
    parts["client"] = q

    pc = job.get("proposals_count")
    if pc is None:
        c = 5
    else:
        c = 10 if pc < 5 else 8 if pc < 10 else 5 if pc < 20 else 2 if pc < 50 else 0
        if pc >= 50:
            reasons.append(f"{pc}+ proposals already; very crowded")
    parts["competition"] = c

    h = _hours_since(job.get("posted_at"), now)
    if h is None:
        f = 5
    else:
        f = 10 if h < 2 else 8 if h < 6 else 5 if h < 24 else 2 if h < 72 else 0
        if h < 2:
            reasons.append("Posted under 2 hours ago; early proposals get seen")
    parts["freshness"] = f

    flags = detect_red_flags(job)
    score = sum(parts.values())
    decision = "bid" if score >= 70 else "maybe" if score >= 50 else "skip"
    if flags:
        decision = "skip"
    return {"score": score, "decision": decision, "parts": parts, "flags": flags, "reasons": reasons,
            "matched_skills": hit, "missing_skills": missing}


# --------------------------------------------------------------- parsing
def _money(s):
    return float(s.replace(",", ""))


def parse_job_text(text):
    """Best-effort parse of text copied from an Upwork job page. The user reviews the result before saving."""
    raw = (text or "").strip()
    lines = [l.strip() for l in raw.splitlines() if l.strip()]
    out = {"title": lines[0][:200] if lines else "", "description": "\n".join(lines[1:]) if len(lines) > 1 else raw,
           "skills": [], "budget_type": "hourly"}

    m = re.search(r"\$\s?([\d,.]+)\s*(?:-|–|—|to)\s*\$\s?([\d,.]+)\s*(?:/\s*hr|per hour|hourly)", raw, re.I)
    if m:
        out.update(budget_type="hourly", budget_min=_money(m.group(1)), budget_max=_money(m.group(2)))
    else:
        m = re.search(r"\$\s?([\d,.]+)\s*(?:/\s*hr|per hour)", raw, re.I)
        if m:
            out.update(budget_type="hourly", budget_min=_money(m.group(1)), budget_max=_money(m.group(1)))
        else:
            m = re.search(r"fixed[- ]price[^$]{0,60}\$\s?([\d,]+(?:\.\d+)?)|budget[^$\n]{0,20}\$\s?([\d,]+(?:\.\d+)?)", raw, re.I)
            if m:
                amt = _money(m.group(1) or m.group(2))
                out.update(budget_type="fixed", budget_min=amt, budget_max=amt)

    m = re.search(r"\$\s?([\d.,]+)\s*([KkMm])?\+?\s*total spent", raw)
    if m:
        mult = {"k": 1e3, "m": 1e6}.get((m.group(2) or "").lower(), 1)
        out["client_spend"] = _money(m.group(1)) * mult
    m = re.search(r"(\d{1,3})%\s*hire rate", raw, re.I)
    if m:
        out["client_hire_rate"] = float(m.group(1))
    m = re.search(r"\b([0-5]\.\d{1,2})\s*(?:of\s*\d+\s*reviews?|stars?|/\s*5)", raw, re.I)
    if m:
        out["client_rating"] = float(m.group(1))
    if re.search(r"payment (method )?(is )?(not verified|unverified)", raw, re.I):
        out["client_verified"] = 0
    elif re.search(r"payment (method )?verified", raw, re.I):
        out["client_verified"] = 1
    m = re.search(r"proposals?:?\s*(?:less than\s*)?(\d+)(?:\s*(?:to|-|–)\s*(\d+))?", raw, re.I)
    if m:
        out["proposals_count"] = int(m.group(2) or m.group(1))
    m = re.search(r"(\d+)\s*connects", raw, re.I)
    if m:
        out["connects_cost"] = int(m.group(1))

    for i, l in enumerate(lines):
        if re.match(r"^skills( and expertise)?:?$", l, re.I):
            out["skills"] = [s for s in lines[i + 1:i + 16] if len(s) < 40 and not s.startswith("$")]
            break
        m = re.match(r"^skills( and expertise)?:\s*(.+)$", l, re.I)
        if m:
            out["skills"] = [s.strip() for s in m.group(2).split(",") if s.strip()]
            break
    return out


# ----------------------------------------------------------- profile audit
GENERIC_TITLES = {"freelancer", "expert", "professional", "developer", "designer", "writer", "specialist"}
HOOK_BAD = re.compile(r"^\s*(hi|hello|hey|greetings|dear|my name is|i am|i'm|i’m|welcome)\b", re.I)
CTA = re.compile(r"(message me|send me|let'?s|reach out|get in touch|book a|schedule a|invite me|\?\s*$)", re.I)
PROOF = re.compile(r"\b(increased|reduced|delivered|grew|saved|launched|shipped|built|scaled|improved|generated)\b", re.I)


def _check(cid, label, got, mx, advice, ok_at=None):
    ok_at = mx if ok_at is None else ok_at
    status = "pass" if got >= ok_at else ("warn" if got > 0 else "fail")
    return {"id": cid, "label": label, "points": got, "max": mx, "status": status,
            "advice": "" if status == "pass" else advice}


def demand_keywords(jobs, top=10):
    """Most common skills across saved jobs: the market's vocabulary for your niche."""
    c = Counter()
    for j in jobs:
        for s in {norm_skill(x) for x in j.get("skills", []) if x.strip()}:
            c[s] += 1
    return c.most_common(top)


def audit_profile(profile, jobs=()):
    title = profile.get("title", "")
    overview = profile.get("overview", "")
    skills = [norm_skill(s) for s in profile.get("skills", [])]
    first200 = overview[:200]
    checks = []

    pts = 0
    if 25 <= len(title) <= 70:
        pts += 8
    tl = title.lower()
    if title and any(s and s in tl for s in skills) and not set(tokens(title)) <= GENERIC_TITLES:
        pts += 7
    checks.append(_check("title", "Title: specific, 25-70 chars, names what you do", pts, 15,
                         "Aim for 25-70 characters and name a concrete skill or outcome (e.g. 'Shopify Speed Optimisation | "
                         "Core Web Vitals'), not just 'Developer'."))

    pts = 0
    if first200 and not HOOK_BAD.match(first200):
        pts += 5
    if re.search(r"\b(you|your)\b", first200, re.I):
        pts += 5
    if re.search(r"\d", first200) or PROOF.search(first200):
        pts += 5
    checks.append(_check("hook", "First 200 characters (shown in search) lead with the client's outcome", pts, 15,
                         "Open with the result clients get, not 'Hi, I'm...'. Use 'you/your', and include one number or "
                         "concrete outcome before the 200-character cut-off."))

    n = len(overview)
    pts = 10 if 600 <= n <= 1800 else 6 if (300 <= n < 600 or 1800 < n <= 3000) else 0
    checks.append(_check("length", "Overview length 600-1,800 characters", pts, 10,
                         f"Currently {n} characters. Short overviews lack proof; very long ones don't get read."))

    nums = len(re.findall(r"\d+", overview))
    pts = (5 if nums >= 2 else 0) + (5 if PROOF.search(overview) else 0)
    checks.append(_check("proof", "Concrete proof: numbers and delivered results", pts, 10,
                         "Add 2+ real, specific results (metrics, client types, timeframes). Only use ones that are true."))

    checks.append(_check("cta", "Ends with a clear call to action", 5 if CTA.search(overview.strip()[-160:]) else 0, 5,
                         "End with one invitation, e.g. 'Message me with your current setup and the result you need.'"))

    k = len(skills)
    pts = 15 if 10 <= k <= 15 else 9 if 5 <= k < 10 else 3 if k else 0
    checks.append(_check("skills", "10-15 relevant skills listed", pts, 15,
                         f"You list {k}. Fill the available slots with skills clients actually search for."))

    top = demand_keywords(jobs)
    missing = []
    if top:
        text = f"{title} {overview}".lower()
        have = 0
        for s, _ in top:
            if s in skills or re.search(r"(?<![a-z0-9])" + re.escape(s) + r"(?![a-z0-9])", text):
                have += 1
            else:
                missing.append(s)
        pts = round(15 * have / len(top))
        advice = "In demand in jobs you saved but missing from your profile: " + ", ".join(missing[:6]) + \
                 ". Add only the ones you can genuinely do."
    else:
        pts, advice = 8, "Save a few jobs in your niche so the audit can compare your profile with real demand."
    c = _check("demand", "Covers the skills your target jobs ask for", pts, 15, advice, ok_at=13)
    if not top:
        c["status"] = "warn"
    checks.append(c)

    rate = float(profile.get("hourly_rate") or 0)
    tops = sorted(j["budget_max"] for j in jobs if j.get("budget_type") == "hourly" and j.get("budget_max"))
    if tops and rate:
        med = tops[len(tops) // 2]
        pts = 5 if 0.8 * med <= rate <= 1.3 * med else 2
        advice = f"Median top-of-range in saved hourly jobs is ${med:g}/hr vs your ${rate:g}/hr. Test a change deliberately."
    else:
        pts, advice = 3, "Set your hourly rate and save hourly jobs to compare against the market."
    c = _check("rate", "Rate in line with the jobs you target", pts, 5, advice)
    if not (tops and rate):
        c["status"] = "warn"
    checks.append(c)

    pc = int(profile.get("portfolio_count") or 0)
    checks.append(_check("portfolio", "3+ portfolio items", 10 if pc >= 3 else 5 if pc else 0, 10,
                         f"You have {pc}. Add work samples that match the jobs you want."))

    score = sum(c["points"] for c in checks)
    checks_sorted = sorted((c for c in checks if c["status"] != "pass"), key=lambda c: c["max"] - c["points"], reverse=True)
    return {"score": score, "checks": checks, "missing_keywords": missing,
            "priorities": [{"id": c["id"], "label": c["label"], "advice": c["advice"],
                            "gain": c["max"] - c["points"]} for c in checks_sorted[:3]]}

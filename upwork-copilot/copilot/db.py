"""SQLite persistence. Zero third-party dependencies."""
import json
import os
import sqlite3
from datetime import datetime, timezone

SCHEMA = """
CREATE TABLE IF NOT EXISTS profile (
  id INTEGER PRIMARY KEY CHECK (id = 1),
  title TEXT NOT NULL DEFAULT '',
  overview TEXT NOT NULL DEFAULT '',
  niche TEXT NOT NULL DEFAULT '',
  skills TEXT NOT NULL DEFAULT '[]',
  proof_points TEXT NOT NULL DEFAULT '[]',
  hourly_rate REAL NOT NULL DEFAULT 0,
  min_fixed_budget REAL NOT NULL DEFAULT 300,
  portfolio_count INTEGER NOT NULL DEFAULT 0,
  updated_at TEXT
);
CREATE TABLE IF NOT EXISTS profile_versions (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  ts TEXT NOT NULL,
  note TEXT NOT NULL DEFAULT '',
  snapshot TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS jobs (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  title TEXT NOT NULL,
  description TEXT NOT NULL DEFAULT '',
  skills TEXT NOT NULL DEFAULT '[]',
  budget_type TEXT NOT NULL DEFAULT 'hourly',
  budget_min REAL,
  budget_max REAL,
  client_verified INTEGER,
  client_spend REAL,
  client_hire_rate REAL,
  client_rating REAL,
  proposals_count INTEGER,
  connects_cost INTEGER,
  posted_at TEXT,
  url TEXT NOT NULL DEFAULT '',
  fit_score INTEGER NOT NULL DEFAULT 0,
  fit_detail TEXT NOT NULL DEFAULT '{}',
  decision TEXT NOT NULL DEFAULT 'skip',
  created_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS proposals (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  job_id INTEGER NOT NULL REFERENCES jobs(id) ON DELETE CASCADE,
  body TEXT NOT NULL DEFAULT '',
  variant TEXT NOT NULL DEFAULT 'question',
  source TEXT NOT NULL DEFAULT 'template',
  status TEXT NOT NULL DEFAULT 'draft',
  stage_reached INTEGER NOT NULL DEFAULT -1,
  connects_spent INTEGER NOT NULL DEFAULT 0,
  bid_amount REAL,
  profile_version INTEGER,
  sent_at TEXT,
  updated_at TEXT NOT NULL,
  notes TEXT NOT NULL DEFAULT ''
);
CREATE TABLE IF NOT EXISTS earnings (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  proposal_id INTEGER REFERENCES proposals(id) ON DELETE SET NULL,
  amount REAL NOT NULL,
  date TEXT NOT NULL,
  note TEXT NOT NULL DEFAULT ''
);
CREATE TABLE IF NOT EXISTS goals (
  month TEXT PRIMARY KEY,
  revenue_target REAL NOT NULL,
  avg_contract_value REAL NOT NULL
);
"""

PROFILE_FIELDS = ["title", "overview", "niche", "skills", "proof_points",
                  "hourly_rate", "min_fixed_budget", "portfolio_count"]
JSON_PROFILE = {"skills", "proof_points"}
STAGES = {"sent": 0, "viewed": 1, "interview": 2, "hired": 3}
STATUSES = ["draft", "sent", "viewed", "interview", "hired", "lost"]
DEFAULT_GOAL = {"revenue_target": 5000.0, "avg_contract_value": 1000.0}


def now_iso():
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def connect(path=None):
    path = path or os.environ.get("UPWORK_COPILOT_DB") or os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "copilot.db")
    if path != ":memory:":
        os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys=ON")
    conn.executescript(SCHEMA)
    conn.execute("INSERT OR IGNORE INTO profile (id) VALUES (1)")
    conn.commit()
    return conn


# ---------------------------------------------------------------- profile
def get_profile(conn):
    row = conn.execute("SELECT * FROM profile WHERE id=1").fetchone()
    p = dict(row)
    for k in JSON_PROFILE:
        p[k] = json.loads(p[k] or "[]")
    v = conn.execute("SELECT MAX(id) AS v FROM profile_versions").fetchone()["v"]
    p["version_id"] = v
    return p


def _clean_profile(data):
    out = {}
    for k in PROFILE_FIELDS:
        if k not in data:
            continue
        v = data[k]
        if k in JSON_PROFILE:
            if isinstance(v, str):
                v = [s.strip() for s in v.replace("\n", ",").split(",") if s.strip()] if k == "skills" \
                    else [s.strip() for s in v.split("\n") if s.strip()]
            v = [str(s).strip() for s in v if str(s).strip()]
        elif k in ("hourly_rate", "min_fixed_budget"):
            v = float(v or 0)
        elif k == "portfolio_count":
            v = int(v or 0)
        else:
            v = str(v or "").strip()
        out[k] = v
    return out


def save_profile(conn, data, note=""):
    """Persist profile changes. Every real change creates a version so results can be compared per version."""
    from . import scoring  # local import avoids a cycle
    current = get_profile(conn)
    new = _clean_profile(data)
    changed = {k: v for k, v in new.items() if current.get(k) != v}
    if not changed:
        return current
    merged = {**{k: current[k] for k in PROFILE_FIELDS}, **new}
    sets = ", ".join(f"{k}=?" for k in PROFILE_FIELDS)
    vals = [json.dumps(merged[k]) if k in JSON_PROFILE else merged[k] for k in PROFILE_FIELDS]
    conn.execute(f"UPDATE profile SET {sets}, updated_at=? WHERE id=1", vals + [now_iso()])
    conn.execute("INSERT INTO profile_versions (ts, note, snapshot) VALUES (?,?,?)",
                 (now_iso(), note or "changed: " + ", ".join(sorted(changed)), json.dumps(merged)))
    conn.commit()
    profile = get_profile(conn)
    for j in conn.execute("SELECT id FROM jobs").fetchall():
        rescore_job(conn, j["id"], profile)
    conn.commit()
    return profile


def list_versions(conn):
    return [dict(r) for r in conn.execute(
        "SELECT id, ts, note FROM profile_versions ORDER BY id DESC").fetchall()]


# ------------------------------------------------------------------- jobs
JOB_FIELDS = ["title", "description", "skills", "budget_type", "budget_min", "budget_max",
              "client_verified", "client_spend", "client_hire_rate", "client_rating",
              "proposals_count", "connects_cost", "posted_at", "url"]


def _job_row_to_dict(r):
    d = dict(r)
    d["skills"] = json.loads(d["skills"] or "[]")
    d["fit_detail"] = json.loads(d["fit_detail"] or "{}")
    return d


def _num(v, cast=float):
    if v in (None, ""):
        return None
    return cast(v)


def add_job(conn, data):
    from . import scoring
    title = str(data.get("title", "")).strip()
    if not title:
        raise ValueError("title is required")
    skills = data.get("skills") or []
    if isinstance(skills, str):
        skills = [s.strip() for s in skills.replace("\n", ",").split(",") if s.strip()]
    cv = data.get("client_verified")
    job = {
        "title": title,
        "description": str(data.get("description", "")),
        "skills": json.dumps(skills),
        "budget_type": data.get("budget_type") if data.get("budget_type") in ("hourly", "fixed") else "hourly",
        "budget_min": _num(data.get("budget_min")),
        "budget_max": _num(data.get("budget_max")),
        "client_verified": None if cv in (None, "") else int(bool(cv)),
        "client_spend": _num(data.get("client_spend")),
        "client_hire_rate": _num(data.get("client_hire_rate")),
        "client_rating": _num(data.get("client_rating")),
        "proposals_count": _num(data.get("proposals_count"), int),
        "connects_cost": _num(data.get("connects_cost"), int),
        "posted_at": data.get("posted_at") or now_iso(),
        "url": str(data.get("url", "")),
        "created_at": now_iso(),
    }
    cols = ", ".join(job)
    cur = conn.execute(f"INSERT INTO jobs ({cols}) VALUES ({','.join('?' * len(job))})", list(job.values()))
    conn.commit()
    return rescore_job(conn, cur.lastrowid, get_profile(conn))


def rescore_job(conn, job_id, profile):
    from . import scoring
    row = conn.execute("SELECT * FROM jobs WHERE id=?", (job_id,)).fetchone()
    job = _job_row_to_dict(row)
    detail = scoring.score_job(job, profile)
    conn.execute("UPDATE jobs SET fit_score=?, fit_detail=?, decision=? WHERE id=?",
                 (detail["score"], json.dumps(detail), detail["decision"], job_id))
    conn.commit()
    return get_job(conn, job_id)


def get_job(conn, job_id):
    r = conn.execute("SELECT * FROM jobs WHERE id=?", (job_id,)).fetchone()
    return _job_row_to_dict(r) if r else None


def list_jobs(conn, limit=200):
    return [_job_row_to_dict(r) for r in conn.execute(
        "SELECT * FROM jobs ORDER BY fit_score DESC, id DESC LIMIT ?", (limit,)).fetchall()]


def delete_job(conn, job_id):
    conn.execute("DELETE FROM jobs WHERE id=?", (job_id,))
    conn.commit()


# -------------------------------------------------------------- proposals
def create_proposal(conn, job_id, body, variant, source):
    cur = conn.execute(
        "INSERT INTO proposals (job_id, body, variant, source, updated_at) VALUES (?,?,?,?,?)",
        (job_id, body, variant, source, now_iso()))
    conn.commit()
    return get_proposal(conn, cur.lastrowid)


def get_proposal(conn, pid):
    r = conn.execute(
        "SELECT p.*, j.title AS job_title, j.fit_score FROM proposals p JOIN jobs j ON j.id=p.job_id WHERE p.id=?",
        (pid,)).fetchone()
    return dict(r) if r else None


def list_proposals(conn):
    return [dict(r) for r in conn.execute(
        "SELECT p.*, j.title AS job_title, j.fit_score FROM proposals p JOIN jobs j ON j.id=p.job_id "
        "ORDER BY p.id DESC").fetchall()]


def update_proposal(conn, pid, data):
    p = get_proposal(conn, pid)
    if not p:
        raise KeyError(pid)
    fields = {}
    for k in ("body", "notes", "variant"):
        if k in data:
            fields[k] = str(data[k])
    if "connects_spent" in data:
        fields["connects_spent"] = int(data["connects_spent"] or 0)
    if "bid_amount" in data:
        fields["bid_amount"] = _num(data["bid_amount"])
    if "status" in data:
        st = data["status"]
        if st not in STATUSES:
            raise ValueError(f"status must be one of {STATUSES}")
        fields["status"] = st
        if st in STAGES:
            fields["stage_reached"] = max(p["stage_reached"], STAGES[st])
        if st == "sent" and not p["sent_at"]:
            fields["sent_at"] = now_iso()
            fields["profile_version"] = get_profile(conn)["version_id"]
        if st in ("viewed", "interview", "hired") and not p["sent_at"]:
            raise ValueError("mark the proposal as sent first")
    fields["updated_at"] = now_iso()
    sets = ", ".join(f"{k}=?" for k in fields)
    conn.execute(f"UPDATE proposals SET {sets} WHERE id=?", list(fields.values()) + [pid])
    conn.commit()
    return get_proposal(conn, pid)


# --------------------------------------------------------------- earnings
def add_earning(conn, amount, date=None, proposal_id=None, note=""):
    amount = float(amount)
    if amount <= 0:
        raise ValueError("amount must be positive")
    date = date or now_iso()[:10]
    datetime.strptime(date, "%Y-%m-%d")
    conn.execute("INSERT INTO earnings (proposal_id, amount, date, note) VALUES (?,?,?,?)",
                 (proposal_id, amount, date, note))
    conn.commit()


def list_earnings(conn):
    return [dict(r) for r in conn.execute("SELECT * FROM earnings ORDER BY date DESC, id DESC").fetchall()]


# ------------------------------------------------------------------ goals
def get_goal(conn, month):
    r = conn.execute("SELECT * FROM goals WHERE month=?", (month,)).fetchone()
    if r:
        return dict(r)
    last = conn.execute("SELECT * FROM goals ORDER BY month DESC LIMIT 1").fetchone()
    base = dict(last) if last else dict(DEFAULT_GOAL)
    return {"month": month, "revenue_target": base["revenue_target"],
            "avg_contract_value": base["avg_contract_value"]}


def set_goal(conn, month, revenue_target, avg_contract_value):
    revenue_target, avg_contract_value = float(revenue_target), float(avg_contract_value)
    if revenue_target <= 0 or avg_contract_value <= 0:
        raise ValueError("goal values must be positive")
    conn.execute("INSERT INTO goals (month, revenue_target, avg_contract_value) VALUES (?,?,?) "
                 "ON CONFLICT(month) DO UPDATE SET revenue_target=excluded.revenue_target, "
                 "avg_contract_value=excluded.avg_contract_value",
                 (month, revenue_target, avg_contract_value))
    conn.commit()
    return get_goal(conn, month)

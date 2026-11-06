"""Proposal drafting. Uses the Claude API when ANTHROPIC_API_KEY is set, else a grounded template.
Drafts are never sent anywhere: the user reviews, edits and submits on Upwork themselves."""
import json
import os
import re
import urllib.request

VARIANTS = ("question", "result")
MODEL = os.environ.get("UPWORK_COPILOT_MODEL", "claude-sonnet-5-5")

SYSTEM = """You write Upwork proposals for a freelancer. Rules:
- Use ONLY the facts in the freelancer profile and proof points provided. Never invent clients, results, numbers or tools.
- If no relevant proof point exists, write '[ADD: one relevant result]' where it belongs.
- Under 170 words. No greeting fluff ("I hope this finds you well"), no "I am writing to apply".
- First sentence must reference something specific from the job post.
- Finish with exactly one specific question about the job.
- Never suggest moving communication or payment off Upwork. Do not mention being an AI.
- Plain text only."""


def _first_sentence(text, limit=150):
    text = re.sub(r"\s+", " ", text or "").strip()
    m = re.match(r"(.{20,}?[.!?])(\s|$)", text)
    s = m.group(1) if m else text
    return s[:limit].rstrip(" ,;:") + ("..." if len(s) > limit else "")


def pick_variant(counts):
    """Balance A/B variants by choosing the one used least so far."""
    return min(VARIANTS, key=lambda v: (counts.get(v, 0), VARIANTS.index(v)))


def template_draft(profile, job, variant):
    need = _first_sentence(job.get("description")) or job.get("title", "your project")
    matched = (job.get("fit_detail") or {}).get("matched_skills") or profile.get("skills", [])[:3]
    skills = ", ".join(matched[:3]) or "this kind of work"
    proof = (profile.get("proof_points") or ["[ADD: one relevant result]"])[0]
    niche = profile.get("niche") or profile.get("title") or "this area"
    missing = (job.get("fit_detail") or {}).get("missing_skills") or []
    q = (f"Which of these matters most to you right now: speed to launch, or getting {missing[0]} right the first time?"
         if missing else "What would a successful first week look like for you?")
    if variant == "result":
        body = (f"{proof}\n\nYour post says: \"{need}\" That is the kind of problem I work on in {niche}, using {skills}.\n\n"
                f"My approach: confirm scope in a short message, deliver a first working version quickly, then refine with your feedback.\n\n{q}")
    else:
        body = (f"You wrote: \"{need}\" I'd start by pinning down exactly what done looks like for this.\n\n"
                f"I focus on {niche} and work with {skills}. {proof}\n\n"
                f"{q}")
    return body


def llm_draft(profile, job, variant, timeout=45):
    key = os.environ.get("ANTHROPIC_API_KEY")
    if not key:
        return None
    style = ("Lead with the most relevant proof point, then connect it to the job." if variant == "result"
             else "Lead with a sharp observation or question about the job, then briefly establish credibility.")
    user = json.dumps({
        "style": style,
        "freelancer": {k: profile.get(k) for k in ("title", "niche", "skills", "proof_points", "hourly_rate")},
        "job": {k: job.get(k) for k in ("title", "description", "skills", "budget_type", "budget_min", "budget_max")},
    })[:12000]
    req = urllib.request.Request(
        "https://api.anthropic.com/v1/messages",
        data=json.dumps({"model": MODEL, "max_tokens": 600, "system": SYSTEM,
                         "messages": [{"role": "user", "content": user}]}).encode(),
        headers={"x-api-key": key, "anthropic-version": "2023-06-01", "content-type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            data = json.load(r)
        text = "".join(b.get("text", "") for b in data.get("content", []) if b.get("type") == "text").strip()
        return text or None
    except Exception:
        return None


def draft(profile, job, variant):
    """Return (body, source). Falls back to the template on any LLM failure."""
    text = llm_draft(profile, job, variant)
    if text:
        return text, "claude"
    return template_draft(profile, job, variant), "template"

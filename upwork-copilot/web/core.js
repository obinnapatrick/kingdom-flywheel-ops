/* Upwork Copilot core: pure logic shared by the browser page and the Node tests.
   Port of copilot/scoring.py, drafting.py and analytics.py. No DOM, no network. */
(function (root) {
  "use strict";
  const STOP = new Set("a an the and or for to of in on with we you your our is are be will this that it as at by from have has i need looking want who can must should it's i'm about into their they them us not but if so do does".split(" "));
  const STAGES = { sent: 0, viewed: 1, interview: 2, hired: 3 };
  const STATUSES = ["draft", "sent", "viewed", "interview", "hired", "lost"];
  const VARIANTS = ["question", "result"];
  const MIN_N = 10;

  const RED_FLAGS = [
    [/\b(whatsapp|telegram|skype|signal app|discord dm)\b|outside (of )?upwork|off[- ]?platform|(email|contact|message|text) me (at|on|outside)/is,
      "Asks to move off-platform (ToS risk, no payment protection)"],
    [/\bfree (sample|trial|test|work|mockup)\b|unpaid (test|trial|sample)|for exposure|test project.{0,30}unpaid/is, "Unpaid test work requested"],
    [/(share|lend|rent|sell|buy)\w* .{0,25}(upwork )?account|use my (upwork )?account|verified account|(identity|id) verif\w+ .{0,20}(for me|on my behalf)/is,
      "Account sharing/renting requested (violates Upwork ToS, can get you banned)"],
    [/\b(crypto (giveaway|investment)|guaranteed returns?|pay (you )?in gift ?cards?|send (me )?money first)\b/is, "Possible scam language"],
  ];

  const esc = (s) => String(s).replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
  const normSkill = (s) => String(s || "").trim().toLowerCase().replace(/\s+/g, " ");
  const hasWord = (text, w) => !!w && new RegExp("(^|[^a-z0-9])" + esc(w) + "($|[^a-z0-9])").test(text);
  const tokens = (t) => (String(t || "").toLowerCase().match(/[a-z0-9+#.\-]{2,}/g) || []).map((x) => x.replace(/^[.-]+|[.-]+$/g, "")).filter((x) => x.length >= 2 && !STOP.has(x));
  const num = (v) => (v === null || v === undefined || v === "" || isNaN(Number(v)) ? null : Number(v));
  const ymd = (d) => d.getFullYear() + "-" + String(d.getMonth() + 1).padStart(2, "0") + "-" + String(d.getDate()).padStart(2, "0");
  const monthOf = (d) => ymd(d || new Date()).slice(0, 7);
  const nowIso = () => new Date().toISOString();
  const list = (v, sep) => (Array.isArray(v) ? v : String(v || "").split(sep)).map((s) => String(s).trim()).filter(Boolean);

  // ------------------------------------------------------------- job scoring
  function hoursSince(iso, now) {
    if (!iso) return null;
    const t = Date.parse(iso);
    if (isNaN(t)) return null;
    return Math.max(((now || new Date()).getTime() - t) / 3.6e6, 0);
  }
  function detectRedFlags(job) {
    const text = (job.title || "") + "\n" + (job.description || "");
    return RED_FLAGS.filter(([re]) => re.test(text)).map(([, label]) => label);
  }
  function skillMatch(job, profile) {
    const prof = new Set((profile.skills || []).map(normSkill));
    const profText = [profile.title, profile.overview, profile.niche].join(" ").toLowerCase();
    const jobSkills = (job.skills || []).map(normSkill).filter(Boolean);
    const desc = ((job.title || "") + " " + (job.description || "")).toLowerCase();
    if (jobSkills.length) {
      const hit = jobSkills.filter((s) => prof.has(s) || hasWord(profText, s));
      return { ratio: hit.length / jobSkills.length, hit, missing: jobSkills.filter((s) => !hit.includes(s)) };
    }
    const hit = [...prof].filter((s) => hasWord(desc, s));
    return { ratio: Math.min(hit.length / 3, 1), hit, missing: [] };
  }
  function scoreJob(job, profile, now) {
    const reasons = [], parts = {};
    const m = skillMatch(job, profile);
    parts.skills = Math.round(40 * m.ratio);
    if (m.ratio >= 0.75) reasons.push("Strong skill match (" + m.hit.length + " overlapping skills)");
    else if (m.ratio < 0.4) reasons.push("Weak skill match; you would be competing outside your niche");
    if (m.missing.length) reasons.push("Skills you don't list: " + m.missing.slice(0, 5).join(", "));

    const rate = Number(profile.hourly_rate) || 0;
    const bmax = num(job.budget_max), bmin = num(job.budget_min);
    let b;
    if (job.budget_type === "fixed") {
      const floor = Number(profile.min_fixed_budget) || 300, amt = bmax !== null ? bmax : bmin;
      if (amt === null) b = 8;
      else if (amt >= 3 * floor) b = 15;
      else if (amt >= floor) b = 11;
      else { b = 3; reasons.push("Budget $" + Math.round(amt).toLocaleString() + " is below your $" + Math.round(floor).toLocaleString() + " minimum"); }
    } else {
      const top = bmax !== null ? bmax : bmin;
      if (top === null || rate <= 0) b = 8;
      else if (top >= rate) b = 15;
      else if (top >= 0.8 * rate) b = 9;
      else { b = 3; reasons.push("Top of range $" + top + "/hr is well under your $" + rate + "/hr"); }
    }
    parts.budget = b;

    let q = 0;
    const v = job.client_verified;
    q += v === 1 ? 8 : v === null || v === undefined ? 4 : 0;
    if (v === 0) reasons.push("Payment method not verified");
    const sp = num(job.client_spend);
    q += sp === null ? 3 : sp >= 50000 ? 6 : sp >= 10000 ? 5 : sp >= 1000 ? 3 : sp > 0 ? 1 : 0;
    const hr = num(job.client_hire_rate);
    q += hr === null ? 2 : hr >= 60 ? 5 : hr >= 40 ? 3 : 1;
    const rt = num(job.client_rating);
    q += rt === null ? 3 : rt >= 4.8 ? 6 : rt >= 4.5 ? 4 : rt >= 4.0 ? 2 : 0;
    parts.client = q;

    const pc = num(job.proposals_count);
    if (pc === null) parts.competition = 5;
    else {
      parts.competition = pc < 5 ? 10 : pc < 10 ? 8 : pc < 20 ? 5 : pc < 50 ? 2 : 0;
      if (pc >= 50) reasons.push(pc + "+ proposals already; very crowded");
    }
    const h = hoursSince(job.posted_at, now);
    if (h === null) parts.freshness = 5;
    else {
      parts.freshness = h < 2 ? 10 : h < 6 ? 8 : h < 24 ? 5 : h < 72 ? 2 : 0;
      if (h < 2) reasons.push("Posted under 2 hours ago; early proposals get seen");
    }
    const flags = detectRedFlags(job);
    const score = Object.values(parts).reduce((a, c) => a + c, 0);
    let decision = score >= 70 ? "bid" : score >= 50 ? "maybe" : "skip";
    if (flags.length) decision = "skip";
    return { score, decision, parts, flags, reasons, matched_skills: m.hit, missing_skills: m.missing };
  }

  // ----------------------------------------------------------------- parsing
  const money = (s) => parseFloat(String(s).replace(/,/g, ""));
  function parseJobText(text) {
    const raw = String(text || "").trim();
    const lines = raw.split(/\r?\n/).map((l) => l.trim()).filter(Boolean);
    const out = { title: (lines[0] || "").slice(0, 200), description: lines.length > 1 ? lines.slice(1).join("\n") : raw, skills: [], budget_type: "hourly" };
    let m = raw.match(/\$\s?([\d,.]+)\s*(?:-|–|—|to)\s*\$\s?([\d,.]+)\s*(?:\/\s*hr|per hour|hourly)/i);
    if (m) { out.budget_type = "hourly"; out.budget_min = money(m[1]); out.budget_max = money(m[2]); }
    else if ((m = raw.match(/\$\s?([\d,.]+)\s*(?:\/\s*hr|per hour)/i))) { out.budget_type = "hourly"; out.budget_min = out.budget_max = money(m[1]); }
    else if ((m = raw.match(/fixed[- ]price[^$]{0,60}\$\s?([\d,]+(?:\.\d+)?)|budget[^$\n]{0,20}\$\s?([\d,]+(?:\.\d+)?)/i))) {
      out.budget_type = "fixed"; out.budget_min = out.budget_max = money(m[1] || m[2]);
    }
    if ((m = raw.match(/\$\s?([\d.,]+)\s*([KkMm])?\+?\s*total spent/))) out.client_spend = money(m[1]) * ({ k: 1e3, m: 1e6 }[(m[2] || "").toLowerCase()] || 1);
    if ((m = raw.match(/(\d{1,3})%\s*hire rate/i))) out.client_hire_rate = Number(m[1]);
    if ((m = raw.match(/\b([0-5]\.\d{1,2})\s*(?:of\s*\d+\s*reviews?|stars?|\/\s*5)/i))) out.client_rating = Number(m[1]);
    if (/payment (method )?(is )?(not verified|unverified)/i.test(raw)) out.client_verified = 0;
    else if (/payment (method )?verified/i.test(raw)) out.client_verified = 1;
    if ((m = raw.match(/proposals?:?\s*(?:less than\s*)?(\d+)(?:\s*(?:to|-|–)\s*(\d+))?/i))) out.proposals_count = Number(m[2] || m[1]);
    if ((m = raw.match(/(\d+)\s*connects/i))) out.connects_cost = Number(m[1]);
    for (let i = 0; i < lines.length; i++) {
      if (/^skills( and expertise)?:?$/i.test(lines[i])) { out.skills = lines.slice(i + 1, i + 16).filter((s) => s.length < 40 && !s.startsWith("$")); break; }
      const mm = lines[i].match(/^skills( and expertise)?:\s*(.+)$/i);
      if (mm) { out.skills = mm[2].split(",").map((s) => s.trim()).filter(Boolean); break; }
    }
    return out;
  }

  // ----------------------------------------------------------- profile audit
  const GENERIC = new Set(["freelancer", "expert", "professional", "developer", "designer", "writer", "specialist"]);
  const HOOK_BAD = /^\s*(hi|hello|hey|greetings|dear|my name is|i am|i'm|i’m|welcome)\b/i;
  const CTA = /(message me|send me|let'?s|reach out|get in touch|book a|schedule a|invite me|\?\s*$)/i;
  const PROOF = /\b(increased|reduced|delivered|grew|saved|launched|shipped|built|scaled|improved|generated)\b/i;
  function check(id, label, got, mx, advice, okAt) {
    okAt = okAt === undefined ? mx : okAt;
    const status = got >= okAt ? "pass" : got > 0 ? "warn" : "fail";
    return { id, label, points: got, max: mx, status, advice: status === "pass" ? "" : advice };
  }
  function demandKeywords(jobs, top) {
    const c = new Map();
    for (const j of jobs) for (const s of new Set((j.skills || []).map(normSkill).filter(Boolean))) c.set(s, (c.get(s) || 0) + 1);
    return [...c.entries()].sort((a, b) => b[1] - a[1]).slice(0, top || 10);
  }
  function auditProfile(p, jobs) {
    jobs = jobs || [];
    const title = p.title || "", ov = p.overview || "", skills = (p.skills || []).map(normSkill), first = ov.slice(0, 200), checks = [];
    let pts = 0;
    if (title.length >= 25 && title.length <= 70) pts += 8;
    if (title && skills.some((s) => s && title.toLowerCase().includes(s)) && !tokens(title).every((t) => GENERIC.has(t))) pts += 7;
    checks.push(check("title", "Title: specific, 25-70 chars, names what you do", pts, 15, "Aim for 25-70 characters and name a concrete skill or outcome (e.g. 'Shopify Speed Optimisation | Core Web Vitals'), not just 'Developer'."));
    pts = 0;
    if (first && !HOOK_BAD.test(first)) pts += 5;
    if (/\b(you|your)\b/i.test(first)) pts += 5;
    if (/\d/.test(first) || PROOF.test(first)) pts += 5;
    checks.push(check("hook", "First 200 characters (shown in search) lead with the client's outcome", pts, 15, "Open with the result clients get, not 'Hi, I'm...'. Use 'you/your', and include one number or concrete outcome before the 200-character cut-off."));
    const n = ov.length;
    pts = n >= 600 && n <= 1800 ? 10 : (n >= 300 && n < 600) || (n > 1800 && n <= 3000) ? 6 : 0;
    checks.push(check("length", "Overview length 600-1,800 characters", pts, 10, "Currently " + n + " characters. Short overviews lack proof; very long ones don't get read."));
    const nums = (ov.match(/\d+/g) || []).length;
    pts = (nums >= 2 ? 5 : 0) + (PROOF.test(ov) ? 5 : 0);
    checks.push(check("proof", "Concrete proof: numbers and delivered results", pts, 10, "Add 2+ real, specific results (metrics, client types, timeframes). Only use ones that are true."));
    checks.push(check("cta", "Ends with a clear call to action", CTA.test(ov.trim().slice(-160)) ? 5 : 0, 5, "End with one invitation, e.g. 'Message me with your current setup and the result you need.'"));
    const k = skills.length;
    pts = k >= 10 && k <= 15 ? 15 : k >= 5 && k < 10 ? 9 : k ? 3 : 0;
    checks.push(check("skills", "10-15 relevant skills listed", pts, 15, "You list " + k + ". Fill the available slots with skills clients actually search for."));
    const top = demandKeywords(jobs), missing = [];
    let advice;
    if (top.length) {
      const text = (title + " " + ov).toLowerCase();
      let have = 0;
      for (const [s] of top) { if (skills.includes(s) || hasWord(text, s)) have++; else missing.push(s); }
      pts = Math.round((15 * have) / top.length);
      advice = "In demand in jobs you saved but missing from your profile: " + missing.slice(0, 6).join(", ") + ". Add only the ones you can genuinely do.";
    } else { pts = 8; advice = "Save a few jobs in your niche so the audit can compare your profile with real demand."; }
    const dc = check("demand", "Covers the skills your target jobs ask for", pts, 15, advice, 13);
    if (!top.length) dc.status = "warn";
    checks.push(dc);
    const rate = Number(p.hourly_rate) || 0;
    const tops = jobs.filter((j) => j.budget_type === "hourly" && j.budget_max).map((j) => Number(j.budget_max)).sort((a, b) => a - b);
    let rc;
    if (tops.length && rate) {
      const med = tops[Math.floor(tops.length / 2)];
      rc = check("rate", "Rate in line with the jobs you target", rate >= 0.8 * med && rate <= 1.3 * med ? 5 : 2, 5, "Median top-of-range in saved hourly jobs is $" + med + "/hr vs your $" + rate + "/hr. Test a change deliberately.");
    } else { rc = check("rate", "Rate in line with the jobs you target", 3, 5, "Set your hourly rate and save hourly jobs to compare against the market."); rc.status = "warn"; }
    checks.push(rc);
    const pc = Number(p.portfolio_count) || 0;
    checks.push(check("portfolio", "3+ portfolio items", pc >= 3 ? 10 : pc ? 5 : 0, 10, "You have " + pc + ". Add work samples that match the jobs you want."));
    const score = checks.reduce((a, c) => a + c.points, 0);
    const priorities = checks.filter((c) => c.status !== "pass").sort((a, b) => b.max - b.points - (a.max - a.points)).slice(0, 3)
      .map((c) => ({ id: c.id, label: c.label, advice: c.advice, gain: c.max - c.points }));
    return { score, checks, missing_keywords: missing, priorities };
  }

  // ---------------------------------------------------------------- drafting
  const DRAFT_RULES = "You write Upwork proposals for a freelancer. Rules:\n- Use ONLY the facts in the freelancer profile and proof points provided. Never invent clients, results, numbers or tools.\n- If no relevant proof point exists, write '[ADD: one relevant result]' where it belongs.\n- Under 170 words. No greeting fluff, no 'I am writing to apply'.\n- First sentence must reference something specific from the job post.\n- Finish with exactly one specific question about the job.\n- Never suggest moving communication or payment off Upwork. Do not mention being an AI.\n- Output the proposal text only, plain text.";
  function firstSentence(text, limit) {
    limit = limit || 150;
    const t = String(text || "").replace(/\s+/g, " ").trim();
    const m = t.match(/^(.{20,}?[.!?])(\s|$)/);
    const s = m ? m[1] : t;
    return s.slice(0, limit).replace(/[ ,;:]+$/, "") + (s.length > limit ? "..." : "");
  }
  function pickVariant(counts) {
    return VARIANTS.slice().sort((a, b) => (counts[a] || 0) - (counts[b] || 0) || VARIANTS.indexOf(a) - VARIANTS.indexOf(b))[0];
  }
  function templateDraft(profile, job, variant) {
    const need = firstSentence(job.description) || job.title || "your project";
    const fit = job.fit || {};
    const matched = (fit.matched_skills && fit.matched_skills.length ? fit.matched_skills : (profile.skills || []).slice(0, 3)).slice(0, 3);
    const skills = matched.join(", ") || "this kind of work";
    const proof = (profile.proof_points || [])[0] || "[ADD: one relevant result]";
    const niche = profile.niche || profile.title || "this area";
    const miss = (fit.missing_skills || [])[0];
    const q = miss ? "Which of these matters most to you right now: speed to launch, or getting " + miss + " right the first time?" : "What would a successful first week look like for you?";
    if (variant === "result") return proof + "\n\nYour post says: \"" + need + "\" That is the kind of problem I work on in " + niche + ", using " + skills + ".\n\nMy approach: confirm scope in a short message, deliver a first working version quickly, then refine with your feedback.\n\n" + q;
    return "You wrote: \"" + need + "\" I'd start by pinning down exactly what done looks like for this.\n\nI focus on " + niche + " and work with " + skills + ". " + proof + "\n\n" + q;
  }
  function buildDraftPrompt(profile, job, variant) {
    const style = variant === "result" ? "Lead with the most relevant proof point, then connect it to the job." : "Lead with a sharp observation or question about the job, then briefly establish credibility.";
    const pick = (o, ks) => Object.fromEntries(ks.map((k) => [k, o[k]]));
    return DRAFT_RULES + "\n\nStyle: " + style + "\n\nFREELANCER:\n" + JSON.stringify(pick(profile, ["title", "niche", "skills", "proof_points", "hourly_rate"])) +
      "\n\nJOB:\n" + JSON.stringify(pick(job, ["title", "description", "skills", "budget_type", "budget_min", "budget_max"])).slice(0, 9000);
  }

  // --------------------------------------------------------------- analytics
  const rate = (n, d) => (d ? Math.round((n / d) * 1000) / 1000 : null);
  function stats(rows) {
    const sent = rows.length, c = (k) => rows.filter((r) => r.stage >= k).length;
    const viewed = c(1), interview = c(2), hired = c(3), connects = rows.reduce((a, r) => a + (r.connects || 0), 0);
    return { sent, viewed, interview, hired, view_rate: rate(viewed, sent), interview_rate: rate(interview, sent), win_rate: rate(hired, sent), connects,
      connects_per_hire: hired ? Math.round((connects / hired) * 10) / 10 : null };
  }
  const sentRows = (s) => s.proposals.filter((p) => p.status !== "draft");
  const funnel = (s) => stats(sentRows(s));
  function byVariant(s) {
    const rows = sentRows(s);
    const out = {};
    for (const v of [...new Set(rows.map((r) => r.variant))].sort()) out[v] = stats(rows.filter((r) => r.variant === v));
    return out;
  }
  function byVersion(s) {
    const rows = sentRows(s);
    return [...new Set(rows.map((r) => r.version).filter((v) => v !== null && v !== undefined))].sort((a, b) => a - b).map((v) => {
      const ver = s.versions.find((x) => x.id === v);
      return Object.assign(stats(rows.filter((r) => r.version === v)), { version: v, note: ver ? ver.note : "" });
    });
  }
  function getGoal(s, month) {
    if (s.goals[month]) return s.goals[month];
    const keys = Object.keys(s.goals).sort();
    return keys.length ? s.goals[keys[keys.length - 1]] : { target: 5000, acv: 1000 };
  }
  function pacing(s, today) {
    today = today || new Date();
    const month = monthOf(today), goal = getGoal(s, month);
    const earned = s.earnings.filter((e) => e.date.slice(0, 7) === month).reduce((a, e) => a + e.amount, 0);
    const st = funnel(s);
    const winRate = (st.hired + 2) / (st.sent + 20); // prior ~10% worth 20 proposals, so early luck doesn't swing the plan
    const remaining = Math.max(goal.target - earned, 0);
    const hires = remaining ? Math.ceil(remaining / goal.acv) : 0;
    const needed = hires ? Math.ceil(hires / winRate) : 0;
    const dim = new Date(today.getFullYear(), today.getMonth() + 1, 0).getDate();
    const daysLeft = dim - today.getDate() + 1;
    const sentMonth = sentRows(s).filter((r) => (r.sent_at || "").slice(0, 7) === month).length;
    return { month, revenue_target: goal.target, avg_contract_value: goal.acv, earned, remaining, win_rate_used: Math.round(winRate * 1000) / 1000, hires_needed: hires,
      proposals_needed: needed, per_week: needed ? Math.round((needed / (daysLeft / 7)) * 10) / 10 : 0, days_left: daysLeft, sent_this_month: sentMonth };
  }
  function insights(s, today) {
    const out = [], add = (level, title, detail) => out.push({ level, title, detail });
    const pct = (x) => Math.round(x * 100) + "%";
    const audit = auditProfile(s.profile, s.jobs), st = funnel(s);
    if (audit.score < 75) for (const p of audit.priorities) add("action", "Profile: " + p.label, "+" + p.gain + " pts available. " + p.advice);
    if (audit.missing_keywords.length) add("action", "Profile is missing in-demand skills", "Jobs you saved ask for: " + audit.missing_keywords.slice(0, 6).join(", ") + ". Add those you can truly deliver.");
    if (st.sent < MIN_N) add("info", "Not enough data yet", st.sent + " proposals sent. Send at least " + MIN_N + " before drawing conclusions; rates below that are noise.");
    else {
      if (st.view_rate < 0.3) add("action", "Few clients are opening your proposals", "View rate " + pct(st.view_rate) + ". Work on the first two lines of your proposals and your profile title/hook, and be more selective about crowded, low-quality-client jobs.");
      else if (st.interview_rate < 0.1) add("action", "Views aren't turning into conversations", pct(st.view_rate) + " view but " + pct(st.interview_rate) + " interview. Tighten the pitch: one proof point, one specific question, and check price positioning.");
      if (st.interview >= 3 && st.hired / st.interview < 0.25) add("action", "Interviews aren't closing", st.hired + " hires from " + st.interview + " interviews. Prepare a scoped plan before calls and propose a small paid first milestone.");
      if (st.connects_per_hire) add("info", "Connects efficiency", "~" + st.connects_per_hire + " connects per hire so far.");
    }
    const vr = byVariant(s), keys = Object.keys(vr);
    if (keys.length >= 2 && keys.every((k) => vr[k].sent >= 8)) {
      const r = keys.sort((a, b) => (vr[b].interview_rate || 0) - (vr[a].interview_rate || 0));
      if ((vr[r[0]].interview_rate || 0) > (vr[r[1]].interview_rate || 0)) add("info", "Variant '" + r[0] + "' is ahead", "Interview rate " + pct(vr[r[0]].interview_rate) + " vs " + pct(vr[r[1]].interview_rate || 0) + " for '" + r[1] + "'. Small samples can mislead; keep testing before dropping one.");
    } else if (keys.length) add("info", "A/B test running", "Each proposal variant needs 8+ sent before the comparison means anything.");
    const p = pacing(s, today);
    if (p.remaining > 0) add("action", "Goal pacing", "$" + Math.round(p.remaining).toLocaleString() + " left of $" + Math.round(p.revenue_target).toLocaleString() + " this month. At a " + pct(p.win_rate_used) + " win rate you need ~" + p.proposals_needed + " more proposals (~" + p.per_week + "/week) for " + p.hires_needed + " hire(s).");
    else add("info", "Monthly goal reached", "$" + Math.round(p.earned).toLocaleString() + " earned. Keep the pipeline warm for next month.");
    return out;
  }

  // -------------------------------------------------------- state operations
  function emptyState() {
    return { v: 1, seq: 0, profile: { title: "", overview: "", niche: "", skills: [], proof_points: [], hourly_rate: 0, min_fixed_budget: 300, portfolio_count: 0 },
      versions: [], jobs: [], proposals: [], earnings: [], goals: {} };
  }
  const nextId = (s) => ++s.seq;
  function rescoreAll(s, now) { for (const j of s.jobs) j.fit = scoreJob(j, s.profile, now); }
  function saveProfile(s, data, note) {
    const cur = s.profile, next = Object.assign({}, cur), changed = [];
    for (const k of Object.keys(cur)) {
      if (!(k in data)) continue;
      let v = data[k];
      if (k === "skills") v = list(v, /[\n,]/).map((x) => x.trim()).filter(Boolean);
      else if (k === "proof_points") v = list(v, "\n");
      else if (k === "hourly_rate" || k === "min_fixed_budget") v = Number(v) || 0;
      else if (k === "portfolio_count") v = parseInt(v, 10) || 0;
      else v = String(v || "").trim();
      if (JSON.stringify(v) !== JSON.stringify(cur[k])) { next[k] = v; changed.push(k); }
    }
    if (!changed.length) return false;
    s.profile = next;
    s.versions.push({ id: nextId(s), ts: nowIso(), note: note || "changed: " + changed.sort().join(", ") });
    rescoreAll(s);
    return true;
  }
  const currentVersion = (s) => (s.versions.length ? s.versions[s.versions.length - 1].id : null);
  function addJob(s, d) {
    const title = String(d.title || "").trim();
    if (!title) throw new Error("title is required");
    const cv = d.client_verified;
    const job = { id: nextId(s), title, description: String(d.description || "").slice(0, 8000), skills: list(d.skills, /[\n,]/),
      budget_type: d.budget_type === "fixed" ? "fixed" : "hourly", budget_min: num(d.budget_min), budget_max: num(d.budget_max),
      client_verified: cv === null || cv === undefined || cv === "" ? null : Number(!!Number(cv)), client_spend: num(d.client_spend), client_hire_rate: num(d.client_hire_rate),
      client_rating: num(d.client_rating), proposals_count: num(d.proposals_count), connects_cost: num(d.connects_cost), posted_at: d.posted_at || nowIso(), url: String(d.url || ""), created_at: nowIso() };
    job.fit = scoreJob(job, s.profile);
    s.jobs.push(job);
    return job;
  }
  function deleteJob(s, id) { s.jobs = s.jobs.filter((j) => j.id !== id); s.proposals = s.proposals.filter((p) => p.job_id !== id); }
  function createProposal(s, jobId, body, variant, source) {
    const p = { id: nextId(s), job_id: jobId, body, variant, source, status: "draft", stage: -1, connects: 0, bid: null, version: null, sent_at: null, updated_at: nowIso() };
    s.proposals.push(p);
    return p;
  }
  function updateProposal(s, id, d) {
    const p = s.proposals.find((x) => x.id === id);
    if (!p) throw new Error("proposal not found");
    if ("status" in d) {
      if (!STATUSES.includes(d.status)) throw new Error("status must be one of " + STATUSES.join(", "));
      if (["viewed", "interview", "hired"].includes(d.status) && !p.sent_at && d.status !== "sent") throw new Error("mark the proposal as sent first");
      p.status = d.status;
      if (d.status in STAGES) p.stage = Math.max(p.stage, STAGES[d.status]);
      if (d.status === "sent" && !p.sent_at) { p.sent_at = nowIso(); p.version = currentVersion(s); }
    }
    if ("body" in d) p.body = String(d.body);
    if ("connects" in d) p.connects = parseInt(d.connects, 10) || 0;
    if ("bid" in d) p.bid = num(d.bid);
    p.updated_at = nowIso();
    return p;
  }
  function addEarning(s, amount, date, note) {
    amount = Number(amount);
    if (!(amount > 0)) throw new Error("amount must be positive");
    date = date || ymd(new Date());
    if (!/^\d{4}-\d{2}-\d{2}$/.test(date) || isNaN(Date.parse(date))) throw new Error("date must be YYYY-MM-DD");
    s.earnings.push({ id: nextId(s), amount, date, note: String(note || "") });
  }
  function setGoal(s, month, target, acv) {
    target = Number(target); acv = Number(acv);
    if (!(target > 0) || !(acv > 0)) throw new Error("goal values must be positive");
    s.goals[month] = { target, acv };
  }
  function demoState() {
    const s = emptyState(), now = Date.now(), ago = (m) => new Date(now - m * 60000).toISOString();
    saveProfile(s, { title: "Shopify Developer", niche: "Shopify store speed and conversion work", overview: "Hi, I'm a developer with 6 years of experience building web apps.",
      skills: ["shopify", "liquid", "javascript", "web performance"], proof_points: ["[EXAMPLE] Cut a 40-product store's load time from 6.1s to 2.3s."], hourly_rate: 55, min_fixed_budget: 400, portfolio_count: 1 }, "example profile");
    addJob(s, { title: "Speed up my Shopify store (Core Web Vitals)", description: "Our store loads slowly on mobile. Need someone to audit and fix Liquid and JS bloat.", skills: ["shopify", "liquid", "web performance", "core web vitals"],
      budget_type: "hourly", budget_min: 40, budget_max: 70, client_verified: 1, client_spend: 24000, client_hire_rate: 72, client_rating: 4.9, proposals_count: 4, connects_cost: 16, posted_at: ago(50) });
    addJob(s, { title: "WordPress blog fix", description: "Contact me on WhatsApp for details. Free test task first.", skills: ["wordpress"], budget_type: "fixed", budget_min: 60, budget_max: 60, client_verified: 0, proposals_count: 48, posted_at: ago(1800) });
    addJob(s, { title: "Custom Shopify checkout upload app", description: "Build a small app to let customers upload files at checkout.", skills: ["shopify", "javascript", "node.js", "shopify functions"],
      budget_type: "fixed", budget_min: 1500, budget_max: 1500, client_verified: 1, client_spend: 3000, client_hire_rate: 50, client_rating: 4.6, proposals_count: 12, posted_at: ago(300) });
    return s;
  }

  const api = { STATUSES, VARIANTS, MIN_N, normSkill, tokens, scoreJob, detectRedFlags, parseJobText, auditProfile, demandKeywords, templateDraft, buildDraftPrompt, pickVariant,
    stats, funnel, byVariant, byVersion, pacing, insights, getGoal, monthOf, ymd, emptyState, saveProfile, addJob, deleteJob, createProposal, updateProposal, addEarning, setGoal, rescoreAll, demoState };
  root.CopilotCore = api;
  if (typeof module !== "undefined" && module.exports) module.exports = api;
})(typeof window !== "undefined" ? window : globalThis);

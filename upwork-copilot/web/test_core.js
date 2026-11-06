// Run: node --test web/   (mirrors tests/test_copilot.py for the browser port)
const test = require("node:test"), assert = require("node:assert/strict"), C = require("./core.js");
const NOW = new Date("2026-11-06T12:00:00Z");
const PROFILE = { title: "Shopify Speed Optimisation | Core Web Vitals", niche: "Shopify performance",
  overview: "You lose sales when your store is slow. I cut load time by 60% for 12 stores, delivered measurable Core Web Vitals gains, and reduced bounce rates. " + "I work in Liquid and JavaScript. ".repeat(20) + "Message me with your store URL and the result you need.",
  skills: ["shopify", "liquid", "javascript", "web performance", "core web vitals", "css", "html", "seo", "git", "figma"],
  proof_points: ["Cut load time from 6.1s to 2.3s."], hourly_rate: 55, min_fixed_budget: 400, portfolio_count: 4 };
const job = (o) => Object.assign({ title: "Speed up Shopify store", description: "Slow on mobile. Need Core Web Vitals fixed.", skills: ["shopify", "liquid", "core web vitals"], budget_type: "hourly",
  budget_min: 50, budget_max: 70, client_verified: 1, client_spend: 30000, client_hire_rate: 75, client_rating: 4.9, proposals_count: 3, posted_at: new Date(NOW - 30 * 60000).toISOString() }, o);
const fresh = () => { const s = C.emptyState(); C.saveProfile(s, PROFILE); return s; };

test("great job is bid", () => { const r = C.scoreJob(job(), PROFILE, NOW); assert.ok(r.score >= 85); assert.equal(r.decision, "bid"); });
test("poor job is skip", () => {
  const r = C.scoreJob(job({ skills: ["cobol"], client_verified: 0, client_spend: 0, client_hire_rate: 10, client_rating: 3, proposals_count: 80, budget_max: 20, posted_at: new Date(NOW - 5 * 864e5).toISOString() }), PROFILE, NOW);
  assert.equal(r.decision, "skip"); assert.ok(r.score < 40);
});
test("red flags force skip", () => {
  for (const t of ["Contact me on WhatsApp", "Please do a free sample first", "You will use my Upwork account", "we need to talk outside of Upwork"]) {
    const r = C.scoreJob(job({ description: t }), PROFILE, NOW); assert.equal(r.decision, "skip", t); assert.ok(r.flags.length, t);
  }
});
test("no false-positive flag", () => assert.deepEqual(C.detectRedFlags(job({ description: "We want a free shipping banner on our store" })), []));
test("fixed budget floor", () => {
  const lo = C.scoreJob(job({ budget_type: "fixed", budget_min: 100, budget_max: 100 }), PROFILE, NOW), hi = C.scoreJob(job({ budget_type: "fixed", budget_min: 2000, budget_max: 2000 }), PROFILE, NOW);
  assert.ok(lo.parts.budget < hi.parts.budget);
});
test("parse job text", () => {
  const p = C.parseJobText("Speed up my Shopify store\nWe are slow on mobile. Please help.\n$40.00 - $70.00 /hr\nProposals: 5 to 10\nPayment method verified\n4.92 of 31 reviews\n$24K total spent\n72% hire rate\nConnects: 16 connects\nSkills and expertise\nShopify\nLiquid\n");
  assert.equal(p.title, "Speed up my Shopify store"); assert.deepEqual([p.budget_min, p.budget_max, p.budget_type], [40, 70, "hourly"]);
  assert.equal(p.client_spend, 24000); assert.equal(p.client_hire_rate, 72); assert.equal(p.client_verified, 1); assert.equal(p.proposals_count, 10);
  assert.deepEqual(p.skills.slice(0, 2), ["Shopify", "Liquid"]); assert.ok(Math.abs(p.client_rating - 4.92) < 1e-9);
});
test("parse unverified and fixed", () => { const p = C.parseJobText("Logo\nPayment method not verified\nFixed-price\n$250.00"); assert.equal(p.client_verified, 0); assert.deepEqual([p.budget_type, p.budget_max], ["fixed", 250]); });

test("strong profile audits high", () => { const a = C.auditProfile(PROFILE, [job()]); assert.ok(a.score >= 85, JSON.stringify(a.checks.filter((c) => c.status !== "pass"))); assert.ok(a.score <= 100); });
test("weak profile audits low", () => { const a = C.auditProfile({ title: "Freelancer", overview: "Hi, I'm John.", skills: ["a"] }, []); assert.ok(a.score < 25); assert.equal(a.priorities.length, 3); });
test("missing demand keywords", () => assert.ok(C.auditProfile(PROFILE, [1, 2, 3].map(() => job({ skills: ["shopify", "klaviyo"] }))).missing_keywords.includes("klaviyo")));

test("template never invents proof", () => {
  for (const v of C.VARIANTS) { const b = C.templateDraft(Object.assign({}, PROFILE, { proof_points: [] }), job(), v); assert.ok(b.includes("[ADD:")); assert.ok(b.trim().endsWith("?")); }
});
test("template uses real proof; variants balance", () => {
  assert.ok(C.templateDraft(PROFILE, job(), "result").includes("6.1s to 2.3s"));
  assert.equal(C.pickVariant({}), "question"); assert.equal(C.pickVariant({ question: 3, result: 1 }), "result");
});
test("draft prompt carries rules and only profile facts", () => { const p = C.buildDraftPrompt(PROFILE, job(), "result"); assert.ok(p.includes("Never invent")); assert.ok(p.includes("6.1s to 2.3s")); });

test("profile versioning and rescoring", () => {
  const s = fresh(), v1 = s.versions.length, j = C.addJob(s, job()), before = j.fit.score;
  assert.equal(C.saveProfile(s, PROFILE), false); assert.equal(s.versions.length, v1);
  assert.equal(C.saveProfile(s, { hourly_rate: 70 }), true); assert.equal(s.versions.length, v1 + 1);
  C.saveProfile(s, { skills: ["cobol"], overview: "", title: "x" }); assert.ok(s.jobs[0].fit.score < before);
});
test("proposal lifecycle and funnel", () => {
  const s = fresh(), j = C.addJob(s, job()), p = C.createProposal(s, j.id, "b", "question", "template");
  assert.throws(() => C.updateProposal(s, p.id, { status: "interview" }));
  C.updateProposal(s, p.id, { status: "sent", connects: 16 }); C.updateProposal(s, p.id, { status: "interview" }); C.updateProposal(s, p.id, { status: "lost" });
  assert.equal(p.stage, 2);
  const f = C.funnel(s); assert.deepEqual([f.sent, f.viewed, f.interview, f.hired, f.connects], [1, 1, 1, 0, 16]);
  assert.throws(() => C.updateProposal(s, p.id, { status: "bogus" }));
});
test("pacing matches the Python implementation", () => {
  const s = fresh(); C.setGoal(s, "2026-11", 5000, 1000); C.addEarning(s, 1000, "2026-11-02");
  const pc = C.pacing(s, new Date(2026, 10, 6));
  assert.deepEqual([pc.remaining, pc.hires_needed, pc.win_rate_used, pc.proposals_needed, pc.days_left], [4000, 4, 0.1, 40, 25]);
});
test("goal met and earning validation", () => {
  const s = fresh(); C.setGoal(s, C.monthOf(new Date()), 500, 500); C.addEarning(s, 600); assert.equal(C.pacing(s).proposals_needed, 0);
  for (const bad of [0, -5]) assert.throws(() => C.addEarning(s, bad)); assert.throws(() => C.addEarning(s, 10, "not-a-date"));
});
test("insights: low data, then view-rate alert", () => {
  const s = fresh(); assert.ok(C.insights(s).some((i) => i.title === "Not enough data yet"));
  const j = C.addJob(s, job());
  for (let i = 0; i < 12; i++) { const p = C.createProposal(s, j.id, "b", "question", "template"); C.updateProposal(s, p.id, { status: "sent", connects: 10 }); }
  assert.ok(C.insights(s).some((i) => i.title === "Few clients are opening your proposals"));
});
test("deleting a job removes its proposals; state round-trips through JSON", () => {
  const s = fresh(), j = C.addJob(s, job()); C.createProposal(s, j.id, "b", "question", "template"); C.deleteJob(s, j.id);
  assert.equal(s.proposals.length, 0); const d = C.demoState(); assert.deepEqual(JSON.parse(JSON.stringify(d)), d);
});
test("demo data scores like the Python demo (89 bid / 66 maybe / skip with flags)", () => {
  const d = C.demoState(), by = Object.fromEntries(d.jobs.map((j) => [j.title, j.fit]));
  assert.equal(by["Speed up my Shopify store (Core Web Vitals)"].decision, "bid"); assert.equal(by["Custom Shopify checkout upload app"].decision, "maybe");
  assert.equal(by["WordPress blog fix"].decision, "skip"); assert.equal(by["WordPress blog fix"].flags.length, 2);
});

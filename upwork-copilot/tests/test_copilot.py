import json
import os
import sys
import unittest
from datetime import date, datetime, timedelta, timezone

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from copilot import analytics, db, drafting, scoring, server  # noqa: E402

PROFILE = {"title": "Shopify Speed Optimisation | Core Web Vitals", "niche": "Shopify performance",
           "overview": "You lose sales when your store is slow. I cut load time by 60% for 12 stores, delivered measurable "
                       "Core Web Vitals gains, and reduced bounce rates. " + "I work in Liquid and JavaScript. " * 20 +
                       "Message me with your store URL and the result you need.",
           "skills": ["shopify", "liquid", "javascript", "web performance", "core web vitals", "css", "html", "seo", "git", "figma"],
           "proof_points": ["Cut load time from 6.1s to 2.3s."], "hourly_rate": 55, "min_fixed_budget": 400, "portfolio_count": 4}
NOW = datetime(2026, 11, 6, 12, 0, tzinfo=timezone.utc)


def good_job(**kw):
    j = {"title": "Speed up Shopify store", "description": "Slow on mobile. Need Core Web Vitals fixed.",
         "skills": ["shopify", "liquid", "core web vitals"], "budget_type": "hourly", "budget_min": 50, "budget_max": 70,
         "client_verified": 1, "client_spend": 30000, "client_hire_rate": 75, "client_rating": 4.9,
         "proposals_count": 3, "posted_at": (NOW - timedelta(minutes=30)).isoformat()}
    j.update(kw)
    return j


class Scoring(unittest.TestCase):
    def test_great_job_is_bid(self):
        r = scoring.score_job(good_job(), PROFILE, now=NOW)
        self.assertGreaterEqual(r["score"], 85)
        self.assertEqual(r["decision"], "bid")

    def test_poor_job_is_skip(self):
        j = good_job(skills=["cobol"], client_verified=0, client_spend=0, client_hire_rate=10, client_rating=3.0,
                     proposals_count=80, budget_max=20, posted_at=(NOW - timedelta(days=5)).isoformat())
        r = scoring.score_job(j, PROFILE, now=NOW)
        self.assertEqual(r["decision"], "skip")
        self.assertLess(r["score"], 40)

    def test_red_flags_force_skip(self):
        for txt in ("Contact me on WhatsApp", "Please do a free sample first", "You will use my Upwork account",
                    "we need to talk outside of Upwork"):
            r = scoring.score_job(good_job(description=txt), PROFILE, now=NOW)
            self.assertEqual(r["decision"], "skip", txt)
            self.assertTrue(r["flags"], txt)

    def test_no_false_positive_flag(self):
        self.assertEqual(scoring.detect_red_flags(good_job(description="We want a free shipping banner on our store")), [])

    def test_fixed_budget_floor(self):
        low = scoring.score_job(good_job(budget_type="fixed", budget_min=100, budget_max=100), PROFILE, now=NOW)
        high = scoring.score_job(good_job(budget_type="fixed", budget_min=2000, budget_max=2000), PROFILE, now=NOW)
        self.assertLess(low["parts"]["budget"], high["parts"]["budget"])

    def test_parse(self):
        text = """Speed up my Shopify store
We are slow on mobile. Please help.
$40.00 - $70.00 /hr
Proposals: 5 to 10
Payment method verified
4.92 of 31 reviews
$24K total spent
72% hire rate
Connects: 16 connects
Skills and expertise
Shopify
Liquid
"""
        p = scoring.parse_job_text(text)
        self.assertEqual(p["title"], "Speed up my Shopify store")
        self.assertEqual((p["budget_min"], p["budget_max"], p["budget_type"]), (40.0, 70.0, "hourly"))
        self.assertEqual(p["client_spend"], 24000)
        self.assertEqual(p["client_hire_rate"], 72)
        self.assertEqual(p["client_verified"], 1)
        self.assertEqual(p["proposals_count"], 10)
        self.assertEqual(p["skills"][:2], ["Shopify", "Liquid"])
        self.assertAlmostEqual(p["client_rating"], 4.92)

    def test_parse_unverified_and_fixed(self):
        p = scoring.parse_job_text("Logo\nPayment method not verified\nFixed-price\n$250.00")
        self.assertEqual(p["client_verified"], 0)
        self.assertEqual((p["budget_type"], p["budget_max"]), ("fixed", 250.0))


class Audit(unittest.TestCase):
    def test_strong_profile_scores_high(self):
        a = scoring.audit_profile(PROFILE, [good_job()])
        self.assertGreaterEqual(a["score"], 85, [c for c in a["checks"] if c["status"] != "pass"])

    def test_weak_profile_scores_low_with_priorities(self):
        a = scoring.audit_profile({"title": "Freelancer", "overview": "Hi, I'm John.", "skills": ["a"]}, [])
        self.assertLess(a["score"], 25)
        self.assertEqual(len(a["priorities"]), 3)

    def test_missing_demand_keywords(self):
        jobs = [good_job(skills=["shopify", "klaviyo"]) for _ in range(3)]
        a = scoring.audit_profile(PROFILE, jobs)
        self.assertIn("klaviyo", a["missing_keywords"])

    def test_score_never_exceeds_100(self):
        self.assertLessEqual(scoring.audit_profile(PROFILE, [good_job()])["score"], 100)


class Drafting(unittest.TestCase):
    def setUp(self):
        os.environ.pop("ANTHROPIC_API_KEY", None)

    def test_template_has_no_invented_proof_when_none(self):
        p = {**PROFILE, "proof_points": []}
        for v in drafting.VARIANTS:
            body, src = drafting.draft(p, good_job(), v)
            self.assertEqual(src, "template")
            self.assertIn("[ADD:", body)
            self.assertTrue(body.strip().endswith("?"))

    def test_template_uses_real_proof(self):
        body, _ = drafting.draft(PROFILE, good_job(), "result")
        self.assertIn("6.1s to 2.3s", body)

    def test_variant_balancing(self):
        self.assertEqual(drafting.pick_variant({}), "question")
        self.assertEqual(drafting.pick_variant({"question": 3, "result": 1}), "result")


class Flow(unittest.TestCase):
    def setUp(self):
        self.c = db.connect(":memory:")
        self.addCleanup(self.c.close)
        db.save_profile(self.c, PROFILE)

    def test_profile_versioning(self):
        v1 = db.get_profile(self.c)["version_id"]
        db.save_profile(self.c, PROFILE)  # no change
        self.assertEqual(db.get_profile(self.c)["version_id"], v1)
        db.save_profile(self.c, {"hourly_rate": 70})
        self.assertGreater(db.get_profile(self.c)["version_id"], v1)

    def test_profile_change_rescores_jobs(self):
        j = db.add_job(self.c, good_job())
        before = j["fit_score"]
        db.save_profile(self.c, {"skills": ["cobol"], "overview": "", "title": "x"})
        self.assertLess(db.get_job(self.c, j["id"])["fit_score"], before)

    def test_proposal_lifecycle_and_funnel(self):
        j = db.add_job(self.c, good_job())
        p = db.create_proposal(self.c, j["id"], "body", "question", "template")
        with self.assertRaises(ValueError):
            db.update_proposal(self.c, p["id"], {"status": "interview"})  # can't skip 'sent'
        db.update_proposal(self.c, p["id"], {"status": "sent", "connects_spent": 16})
        db.update_proposal(self.c, p["id"], {"status": "interview"})
        p = db.update_proposal(self.c, p["id"], {"status": "lost"})
        self.assertEqual(p["stage_reached"], 2)  # losing doesn't erase that you got an interview
        f = analytics.funnel(self.c)
        self.assertEqual((f["sent"], f["viewed"], f["interview"], f["hired"]), (1, 1, 1, 0))
        self.assertEqual(f["connects"], 16)

    def test_bad_status_rejected(self):
        j = db.add_job(self.c, good_job())
        p = db.create_proposal(self.c, j["id"], "b", "question", "template")
        with self.assertRaises(ValueError):
            db.update_proposal(self.c, p["id"], {"status": "bogus"})

    def test_pacing(self):
        today = date(2026, 11, 6)
        db.set_goal(self.c, "2026-11", 5000, 1000)
        db.add_earning(self.c, 1000, "2026-11-02")
        pc = analytics.pacing(self.c, today)
        self.assertEqual(pc["remaining"], 4000)
        self.assertEqual(pc["hires_needed"], 4)
        self.assertAlmostEqual(pc["win_rate_used"], 0.1)  # prior only
        self.assertEqual(pc["proposals_needed"], 40)
        self.assertEqual(pc["days_left"], 25)

    def test_pacing_goal_met(self):
        db.set_goal(self.c, analytics.month_of(), 500, 500)
        db.add_earning(self.c, 600)
        self.assertEqual(analytics.pacing(self.c)["proposals_needed"], 0)

    def test_earning_validation(self):
        for bad in (0, -5):
            with self.assertRaises(ValueError):
                db.add_earning(self.c, bad)
        with self.assertRaises(ValueError):
            db.add_earning(self.c, 10, "not-a-date")

    def test_insights_low_data_and_report(self):
        ins = analytics.insights(self.c)
        self.assertTrue(any(i["title"] == "Not enough data yet" for i in ins))
        self.assertIn("# Upwork weekly report", analytics.weekly_report(self.c))

    def test_insights_view_rate_alert(self):
        j = db.add_job(self.c, good_job())
        for _ in range(12):
            p = db.create_proposal(self.c, j["id"], "b", "question", "template")
            db.update_proposal(self.c, p["id"], {"status": "sent", "connects_spent": 10})
        titles = [i["title"] for i in analytics.insights(self.c)]
        self.assertIn("Few clients are opening your proposals", titles)

    def test_api_routes(self):
        r = server.route(self.c, "POST", "/api/jobs", good_job())
        self.assertEqual(r["decision"], "bid")
        d = server.route(self.c, "POST", f"/api/jobs/{r['id']}/draft", {})
        self.assertEqual(d["status"], "draft")
        s = server.route(self.c, "PATCH", f"/api/proposals/{d['id']}", {"status": "sent", "connects_spent": 16})
        self.assertEqual(s["status"], "sent")
        self.assertIsNotNone(s["profile_version"])
        self.assertIn("funnel", server.route(self.c, "GET", "/api/dashboard", {}))
        self.assertIsNone(server.route(self.c, "GET", "/api/nope", {}))
        with self.assertRaises(ValueError):
            server.route(self.c, "POST", "/api/jobs", {"title": ""})


if __name__ == "__main__":
    unittest.main()

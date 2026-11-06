"""Example data so you can explore the UI. Fictional; run only on an empty database."""
from datetime import datetime, timedelta, timezone

from . import db


def load_demo(conn):
    if conn.execute("SELECT COUNT(*) c FROM jobs").fetchone()["c"] or db.get_profile(conn)["title"]:
        return {"loaded": False, "reason": "database is not empty"}
    db.save_profile(conn, {
        "title": "Shopify Developer", "niche": "Shopify store speed and conversion work",
        "overview": "Hi, I'm a developer with 6 years of experience building web apps.",
        "skills": ["shopify", "liquid", "javascript", "web performance"],
        "proof_points": ["[DEMO] Cut a 40-product store's load time from 6.1s to 2.3s."],
        "hourly_rate": 55, "min_fixed_budget": 400, "portfolio_count": 1}, note="demo profile")
    now = datetime.now(timezone.utc)
    jobs = [
        dict(title="Speed up my Shopify store (Core Web Vitals)", description="Our store loads slowly on mobile. "
             "Need someone to audit and fix Liquid and JS bloat.", skills=["shopify", "liquid", "web performance", "core web vitals"],
             budget_type="hourly", budget_min=40, budget_max=70, client_verified=1, client_spend=24000, client_hire_rate=72,
             client_rating=4.9, proposals_count=4, connects_cost=16, posted_at=(now - timedelta(minutes=50)).isoformat()),
        dict(title="WordPress blog fix", description="Contact me on WhatsApp for details. Free test task first.",
             skills=["wordpress"], budget_type="fixed", budget_min=60, budget_max=60, client_verified=0, proposals_count=48,
             posted_at=(now - timedelta(hours=30)).isoformat()),
        dict(title="Custom Shopify checkout upload app", description="Build a small app to let customers upload files at checkout.",
             skills=["shopify", "javascript", "node.js", "shopify functions"], budget_type="fixed", budget_min=1500, budget_max=1500,
             client_verified=1, client_spend=3000, client_hire_rate=50, client_rating=4.6, proposals_count=12,
             posted_at=(now - timedelta(hours=5)).isoformat()),
    ]
    for j in jobs:
        db.add_job(conn, j)
    return {"loaded": True, "jobs": len(jobs)}

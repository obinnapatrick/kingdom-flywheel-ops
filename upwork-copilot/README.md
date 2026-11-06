# Upwork Copilot

A local, human-in-the-loop app that helps you win more Upwork work each month: it scores jobs, drafts
proposals, audits your profile, and learns from your results. Zero dependencies (Python 3.9+ stdlib + SQLite).

## Why it doesn't auto-bid or log in to Upwork

Upwork's Terms of Use prohibit bots, scraping, and automated bidding or account actions, and enforce this with
account suspensions. Losing the account would cost you more than any automation could earn, so this app never
touches Upwork. You paste a job in, review a draft, and submit it yourself. The leverage comes from picking
better jobs, sending better proposals, and tracking what works. It can't guarantee income; it improves your odds
and shows you the numbers.

## Run it

```bash
cd upwork-copilot
python3 -m copilot serve            # http://127.0.0.1:8765
python3 -m copilot demo             # optional: load fictional example data into an empty DB
python3 -m copilot report           # weekly optimisation report as markdown (cron-friendly)
python3 -m unittest discover -s tests
```

Data lives in `upwork-copilot/data/copilot.db` (override with `UPWORK_COPILOT_DB`). It's git-ignored.
The server binds to 127.0.0.1 only and rejects non-local `Host` headers.

Optional: set `ANTHROPIC_API_KEY` to have Claude write proposal drafts (model via `UPWORK_COPILOT_MODEL`, default
`claude-sonnet-5-5`). Without it, a grounded template is used. Either way drafts only use facts you entered
under "Proof points" and leave `[ADD: …]` placeholders rather than inventing results.

## Browser-only version (iPad / phone): `web/`

`web/core.js` is a JavaScript port of the scoring, audit, drafting and analytics logic, and `web/app.template.html`
is the UI. `node web/build.js` inlines the core into one self-contained page at `web/dist/index.html`. It needs no
server: data is kept in the browser (or, when published as a claude.ai Artifact, in the viewer's private account
store), and drafts can use Claude through the host page instead of an API key.

```bash
node --test web/test_core.js        # 20 tests mirroring tests/test_copilot.py
node web/build.js                   # -> web/dist/index.html
```

The Python app and the browser page share the same scoring rules; if you change one, change the other.

## The weekly loop

1. **Profile**: paste your profile and your true proof points. Fix the top audit items. Every real change is saved as a
   version and each sent proposal is tagged with the version live at the time.
2. **Jobs**: paste job posts from Upwork. Each gets a 0-100 fit score (skills 40, budget 15, client quality 25,
   competition 10, freshness 10) with `bid / maybe / skip`. Off-platform requests, unpaid tests and account-sharing
   requests are flagged and forced to `skip`.
3. **Draft → edit → send yourself → "I sent it"**. Variants (`question`, `result`) are balanced automatically for A/B testing.
4. **Pipeline**: update status as clients respond (viewed → interview → hired / lost). Log earnings.
5. **Insights**: funnel rates, connects per hire, variant and profile-version comparison, and goal pacing
   (how many proposals/week your revenue goal needs at a smoothed win rate). Conclusions are withheld until you
   have ~10 sent proposals.

## Layout

| File | Purpose |
|---|---|
| `copilot/scoring.py` | job scoring, red flags, job-text parser, profile audit |
| `copilot/drafting.py` | Claude / template proposal drafts |
| `copilot/analytics.py` | funnel, A/B, pacing, insights, weekly report |
| `copilot/db.py` | SQLite schema + CRUD, profile versioning |
| `copilot/server.py`, `static/index.html` | local API and UI |

The scoring weights and audit thresholds are heuristics, not Upwork's ranking algorithm. Tune them in `scoring.py`
as your own data comes in.

# Economic Value Lab — Constitution

This file governs all work inside `economic-value-lab/`. It overrides enthusiasm, momentum and
the preferences of whoever is asking. If a request conflicts with this constitution, say so and
follow the constitution.

## Purpose

Systematically develop the ability to create very large amounts of **verified** economic value.
Software and AI (including Claude Code) are tools for that purpose. They are never the purpose.

## Order of operations (non-negotiable)

1. **Problem first.** A recurring, costly, specific problem experienced by an identifiable party.
2. **Evidence second.** Proof that the problem exists at the claimed size, from sources that
   could have shown otherwise.
3. **Economics third.** Who loses money, who can pay, how much is realistically capturable.
4. **Solution last.** Interventions are discussed only after 1–3 survive. Nothing is built until a
   problem has passed the full selection process in `kill_criteria.md` and `opportunity_rubric.md`.

## Permanent rules

### Evidence
1. **Evidence over enthusiasm.** Excitement is not a data point.
2. **No fabricated numbers.** Every number carries a source or is explicitly marked as an
   estimate with its derivation shown. "Industry estimates" with no traceable origin are
   recorded as *claims*, not evidence.
3. **Primary sources preferred.** Order of preference: official statistics / regulator data /
   statutory filings → peer-reviewed or independent research → trade-body surveys →
   consultancy reports → vendor marketing. Vendor marketing can never be the sole support for a
   magnitude used in a decision.
4. **Label every claim** as one of:
   - `FACT` — directly supported by a cited source that was read;
   - `REPORTED` — a source's claim seen second-hand (e.g. via a search excerpt) and not yet
     verified against the original document;
   - `ESTIMATE` — our calculation from stated inputs (show the arithmetic);
   - `ASSUMPTION` — accepted without evidence to allow progress (must be listed for testing);
   - `HYPOTHESIS` — a testable claim we intend to confirm or kill.
5. **Actively seek disconfirmation.** For every thesis, record the strongest evidence *against* it
   in `evidence/`. A file with only supporting evidence is incomplete.
6. **Retain failed hypotheses.** Nothing is deleted. Rejected candidates stay in
   `candidate_ledger.csv` and `decision_record.md` with the reason, so they are not rediscovered.

### Economics
7. **Economic value over technological novelty.** Never confuse impressive technology with
   valuable technology.
8. **Distinguish theoretical from capturable value.** Headline "cost to the economy" figures are
   upper bounds. Record, separately: total problem size → portion that is recoverable at all →
   portion a small operator could realistically capture → portion a buyer would pay for.
9. **Do not favour enormous markets if entry is unrealistic.** An accessible £5m problem beats an
   inaccessible £50bn one for a first laboratory.
10. **Measure outcomes wherever possible.** Prefer problems where value is observable as cash,
    time or output with a before/after or counterfactual design. Demonstrate causation, not
    correlation.

### Bias control
11. **Do not favour AI** when ordinary software, a spreadsheet, a checklist or a process change
    would work better. AI leverage is one scored dimension among many, deliberately low-weighted.
12. **Do not favour familiar industries.** Familiarity is a source of bias, not evidence. Any
    candidate that overlaps a prior venture of the operator must be disclosed as such and receives
    no scoring bonus.
13. **Avoid sunk-cost reasoning.** Past effort on a candidate is never a reason to continue it.
14. **Avoid hype.** Claims that depend on "AI will soon be able to…" are assumptions, not evidence.
15. **Do not declare winners from numerical scores alone.** Scores are judgement made explicit;
    they rank, they do not decide. Report sensitivity to weights and evidence confidence.

### Decisions
16. **Every major recommendation requires a red-team case against it**, written with the intent
    to kill it, answering at minimum the questions in `opportunity_rubric.md` §Red team.
17. **The system must be willing to conclude that no candidate is currently strong enough.**
    "Not yet — more evidence required" is a legitimate and often correct outcome.
18. **Accuracy over momentum.** Never select a market because progress is wanted.

## Operating assumptions (must be re-tested, not silently inherited)

- `ASSUMPTION` The operator is a single independent person with limited capital (order of
  £25k or less available before first evidence of value), no professional licences (legal,
  medical, financial-services, customs-authorised status) and no privileged industry access.
- `ASSUMPTION` The operator is UK-based (inferred from repository context, not stated). This
  affects accessibility scores. If wrong, re-score the ACC dimension for all candidates.

## Phase rules (Phase Zero)

- Do not build products, write production automation, contact companies, choose names, create
  branding or buy infrastructure.
- Research, evidence, scoring and red-teaming only.

## File map

| File | Role |
|---|---|
| `opportunity_rubric.md` | Scoring framework, weights and their justification, red-team protocol |
| `kill_criteria.md` | Conditions that eliminate a candidate before scoring |
| `sector_map.md` | First-principles map of economic functions and where waste concentrates |
| `candidate_ledger.csv` | Every candidate ever considered, with status — never delete rows |
| `evidence/` | Source register and per-candidate evidence for and against |
| `scoring/` | Scores, sensitivity script and generated results |
| `shortlist.md` | Surviving candidates in plain English |
| `decision_record.md` | What was examined, killed, why, and what remains unknown |

# Economic Value Lab — Phase Zero

Mission: find the first real economic problem worth attacking, using evidence rather than
enthusiasm. No products are built in this phase.

Start with `CLAUDE.md` (the constitution), then `decision_record_v2.md` (current state).

Current status (2026-09-29, step 1B): **no arena selected.** The v1 selector was found to be
biased and was replaced by rubric v2. See `decision_record_v2.md` (DR-002). DR-001 is preserved.

Regenerate scores after editing `scoring/scores.csv`:

```
python3 scoring/score.py              # v1 (historical)
python3 scoring/audit_v1/audit.py     # v1 bias audit
python3 scoring/v2/score_v2.py        # v2 scoring, robustness, bias re-audit
python3 scoring/v2/coverage.py        # archetype coverage
python3 scoring/v2/build_ledgers.py   # rebuild second_scan_v1.csv and candidate_ledger_v2.csv
```

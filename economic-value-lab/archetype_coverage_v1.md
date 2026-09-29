# Archetype Coverage Test v1

Question: did the first scan's 29 candidates cover the space of economic problem types, or did it
look mostly where it expected to find answers?

Each candidate gets one **primary** archetype (the mechanism that destroys value) and at most one
**secondary**. Mapping: `scoring/v2/archetypes.csv`; counts: `scoring/v2/coverage.py`.

## Scan 1 coverage (29 candidates)

| Archetype | Primary | Secondary | Status |
|---|---|---|---|
| Leakage / recovery | **13** | 1 | **Over-represented (45%)** |
| Coordination | 0 | 1 | Thin (secondary only) |
| Throughput | 0 | 0 | **Absent** |
| Waiting / delay | 1 | 1 | Thin |
| Quality / errors | 2 | 2 | Covered (weakly) |
| Forecasting | 0 | 1 | Thin (secondary only) |
| Scheduling | 0 | 1 | Thin (secondary only) |
| Asset utilisation | 0 | 1 | Thin (secondary only) |
| Maintenance | 3 | 0 | Covered |
| Procurement | 1 | 3 | Thin |
| Inventory / working capital | 1 | 3 | Thin |
| Decision latency (incl. decision quality) | 0 | 2 | Thin (secondary only) |
| Information flow | 1 | 3 | Thin |
| Knowledge work | 1 | 2 | Thin |
| Customer flow | 2 | 0 | Covered (weakly) |
| Workforce productivity | 0 | 0 | **Absent** |
| Compliance administration | 3 | 2 | Covered |
| Resource allocation | 1 | 0 | Thin |

**Result: the first scan was materially incomplete.** Two archetypes were absent (throughput,
workforce productivity). Seven had no primary candidate. Nine more had only one. The seven
archetypes with no primary candidate are the ones most associated with *productivity creation*
rather than recovery: throughput, coordination, scheduling, forecasting, asset utilisation,
decision latency and workforce.

## Why the gap arose (causes, not excuses)

1. The sector map's own hypothesis (M1/M4 are best suited) steered search queries.
2. Search queries were phrased as "cost of X / money lost to X". That wording surfaces problems
   whose loss is already denominated in cash, which are mostly leakage.
3. Productivity problems tend to be documented in official statistics (ONS, NHS, DfT, WRAP) rather
   than in vendor "£X lost" claims, and the first scan leaned on the latter.

## After the second scan (56 candidates: 29 + 2 derived arenas + 25 new)

| Archetype | Primary | Secondary |
|---|---|---|
| Leakage / recovery | 13 | 1 |
| Coordination | 1 | 3 |
| Throughput | 1 | 0 |
| Waiting / delay | 3 | 1 |
| Quality / errors | 3 | 4 |
| Forecasting | 2 | 2 |
| Scheduling | 2 | 1 |
| Asset utilisation | 1 | 4 |
| Maintenance | 4 | 2 |
| Procurement | 2 | 4 |
| Inventory / working capital | 3 | 4 |
| Decision latency | 3 | 5 |
| Information flow | 2 | 7 |
| Knowledge work | 3 | 3 |
| Customer flow | 3 | 0 |
| Workforce productivity | 2 | 2 |
| Compliance administration | 4 | 4 |
| Resource allocation | 4 | 0 |

Every archetype now has at least one primary candidate with evidence. **Residual thin spots:**
throughput, coordination and asset utilisation still have only one primary candidate each. They
count as "meaningfully considered", not "thoroughly explored". Recorded as an open gap in
`decision_record_v2.md`.

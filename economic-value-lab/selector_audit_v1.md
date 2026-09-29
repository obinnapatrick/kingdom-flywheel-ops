# Selector Audit v1 — did rubric v1 bias the first scan?

Date: 2026-09-29 (Phase Zero, step 1B). Audited artefacts: `opportunity_rubric.md`,
`kill_criteria.md`, `candidate_ledger.csv`, `scoring/score.py`, `scoring/scores.csv`,
`sector_map.md`. None of those files has been modified. Reproduce with
`python3 scoring/audit_v1/audit.py` (output: `scoring/audit_v1/audit_results.md`).

## Verdict

**Yes, the v1 selector was materially biased towards leakage/recovery problems**, through four
separate channels. In order of size:

1. **Candidate generation.** Before any scoring, the sector map stated a hypothesis that
   leakage (M1) and unclaimed entitlements (M4) suit a first laboratory, and the search effort
   followed it. 13 of 29 candidates (45%) were leakage/recovery. Seven of the 18 problem
   archetypes had no primary candidate at all (`archetype_coverage_v1.md`).
2. **Scoring anchors, not just weights.** The MEAS anchor defined a 5 as "value appears as
   discrete verifiable cash with a natural counterfactual". Leakage problems score 5 on MEAS by
   construction. This bias survives any reweighting (see test 4).
3. **Weights.** The proof-mechanics cluster (MEAS, TTP, ACC, IMPL) carried 33 of 100 weight
   points and produced 72% of the score gap between leakage and other problems.
4. **Kill criteria.** The measurability and proof-speed kills (K2, K5, K9) only ever hit
   non-leakage problems. Kills based on invented operator constraints (K1, K7, K8, K15) removed
   the high-ceiling operational problems before scoring could see them.

There was also a **missing dimension**. v1 had no measure of how consequential the capability
could become, and none separating productivity creation from redistribution. A recovery business
whose value is capped at the amount leaked scored the same as a problem whose solution raises
output.

**What the audit does *not* show:** that leakage problems are bad. They really are easier to
measure and faster to prove. That is a real advantage for a *first wedge*, and v2 keeps it on the
wedge axis.

## Method

- Group LEAK = the 13 candidates whose primary archetype is leakage/recovery. OTHER = the
  remaining 16. C26 (energy waste) is physical-resource waste, so it is OTHER, even though its
  wedge had a leakage shape.
- The 10 v1 survivors keep their original scores. I scored the 19 killed candidates
  retrospectively against the same v1 anchors, as if they had not been killed. **Limitation:**
  the same analyst did both, and the analyst knew the audit hypothesis. The permutation test
  below partly guards against a chance result, not against analyst bias.

## Results

### Test 1 — Is there a gap?

| | Mean v1 score |
|---|---|
| LEAK (n=13) | 67.6 |
| OTHER (n=16) | 60.9 |
| Gap | **+6.7 points** |
| One-sided permutation test (20,000 shuffles) | **p = 0.008** |

A gap this large would arise by random labelling fewer than 1 time in 100.

### Test 2 — Where does the gap come from?

Weighted contribution of each dimension to the +6.72-point gap:

| Dimension | Weight | LEAK mean | OTHER mean | Contribution |
|---|---|---|---|---|
| MEAS | 10 | 4.54 | 3.19 | **+2.70** |
| TTP | 9 | 3.54 | 2.69 | **+1.53** |
| URG | 9 | 3.54 | 2.75 | +1.42 |
| SOLV | 7 | 3.31 | 2.75 | +0.78 |
| IMPL | 5 | 3.77 | 3.12 | +0.64 |
| SEV | 9 | 3.38 | 3.12 | +0.47 |
| (10 other dimensions) | 51 | — | — | −0.82 net |

- The proof-mechanics cluster (MEAS+TTP+ACC+IMPL) contributes **+4.83 of +6.72 (72%)**.
- MEAS alone contributes 40%.
- The dimensions that favour OTHER problems (AIL, MOAT, FREQ, COMP, LEARN) carry little weight:
  3, 4, 6, 5 and 4 points.

### Test 3 — What happens with other weights?

| Weight set | Gap | Top 4 | Leakage in top 4 |
|---|---|---|---|
| v1 | +6.7 | C25, C02, C27, C26 | 3 |
| MEAS = 0 | +4.5 | C25, C02, C27, C26 | 3 |
| Proof cluster = 0 | +2.8 | C03, C25, C06, C02 | 3 |
| Proof cluster halved | +5.1 | C25, C02, C06, C27 | 4 |
| Equal weights | +4.6 | C25, C02, C26, C27 | 3 |

Removing the proof cluster entirely brings a maintenance problem (C03, downtime) to #1, but
leakage still takes 3 of the 4 places. The weights alone do not explain the result.

### Test 4 — Random weights (20,000 Dirichlet draws over all 16 dimensions)

- A neutral selector would put ~1.8 leakage candidates in a top 4 (45% base rate).
- Observed: 3 or 4 leakage candidates in the top 4 in **80.5%** of weightings; 0 in 0.0%.
- The gap is positive in **97.6%** of weightings.

**Interpretation.** No reasonable reweighting of v1 removes the bias, so it lives in the
**scores and anchors** (MEAS, TTP and URG are structurally higher for leakage problems). Weight
sensitivity analysis alone, which v1 relied on, could not have caught this. It only varies weights
over a fixed, already-biased score matrix.

### Test 5 — Anchor check

MEAS = 5 was given to 9 of 13 leakage candidates and to 1 of 16 others.

### Test 6 — Kill-criteria incidence

| Kill family | Leakage killed by it | Other killed by it |
|---|---|---|
| Measurability / proof speed (K2, K5, K9) | 0 of 13 | **4** of 16 (C08, C09, C15, C23) |
| Invented-constraint access kills (K1, K7, K8, K15) | 3 (C06, C18, C21) | **5** (C03, C04, C05, C09, C19) |
| Competition / regulation (K6, K11, K14, K18) | 6 | 5 |
| Kill rate overall | 7/13 = 54% | 12/16 = 75% |

Leakage candidates died of *competition*. Other candidates died of *being hard to measure quickly*
or *needing more than one person*. Those are two different filters, and only the first is about
the problem itself.

## Invented constraints

`CLAUDE.md` recorded three operating assumptions that the user never authorised: solo operator,
no licences, ≤ £25k capital. Through K1, K7, K8 and K15 they killed or down-scored the
operationally deepest candidates (downtime, healthcare operations, insurance claims). v2 removes
them and replaces them with access tiers (A = bootstrap can start, B = reachable with partners,
specialists, customers or capital, C = fundamentally inaccessible). Only tier C kills.

## Consequences for the v1 shortlist

The v1 shortlist is **not invalidated as a set of true statements**; the recorded evidence still
stands. But its *ranking* is an artefact of the selector and must not be used for selection. See
`decision_record_v2.md` for what happened to each finalist.

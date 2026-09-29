# Rubric v2 (supersedes `opportunity_rubric.md` for scoring; v1 is preserved unchanged)

Adopted 2026-09-29 after `selector_audit_v1.md`. Implementation: `scoring/v2/score_v2.py`.

## Why the methodology changed

| v1 defect (evidence) | v2 change |
|---|---|
| One blended score let proof-speed dimensions dominate; the proof cluster caused 72% of the leakage advantage (audit test 2) | **Two separate axes.** WEDGE (can a first experiment prove value?) and CEILING (how consequential could mastery become?). Neither can compensate for failure on the other |
| No dimension for long-term consequence; recovery and productivity were scored the same | **New ECONOMIC CAPABILITY CEILING** composite with 10 sub-factors, including productivity vs redistribution |
| MEAS anchor defined 5 as "discrete verifiable cash" (audit test 5) | MEAS re-anchored to **causal measurability by any credible design** within the experiment window (see below) |
| Invented constraints (solo, unlicensed, ≤ £25k) killed deep operational problems (audit test 6) | **Access tiers A/B/C** replace K1, K7, K8 and K15 as kills. Only tier C (fundamentally inaccessible) kills |
| Weight sensitivity could not detect bias located in the anchors (audit test 4) | Mandatory **archetype bias re-audit** on every scoring run, plus random-weight robustness *within* each axis |
| Candidate generation followed a prior hypothesis (coverage test) | Mandatory **archetype coverage test** before any shortlist: every archetype needs at least one evidenced primary candidate |

## Unit of analysis: arena + wedge

- An **arena** is a class of economic problem where world-class capability could compound
  (e.g. "construction contract administration reliability").
- A **wedge** is the first experiment inside an arena that a tier-A operator can start (e.g.
  "notice-deadline and change-record audit on closed subcontract packages").
- CEILING is scored on the arena. WEDGE is scored on the best *evidenced* wedge. An arena with no
  identifiable wedge scores WEDGE on its most practical known entry point, and that is usually
  low.

## Access tiers (replace invented constraints)

| Tier | Meaning | Effect |
|---|---|---|
| **A** | One bootstrap operator can begin a real test now, using public data or data a buyer routinely exports | Eligible for a first wedge |
| **B** | Reachable with partners, specialists, a design customer, a licence-holder or capital; no insider status needed | Eligible as an arena. Its wedge must still have a tier-A entry point, or the arena waits |
| **C** | Fundamentally inaccessible: statutory powers, judicial/sovereign functions, or a single gatekeeper that will not engage | Killed |

## Kill criteria v2 (changes to `kill_criteria.md`; the original is preserved)

- **Retained as hard kills (about the problem itself):** K2 unmeasurable *even in principle*,
  K3 tiny value, K4 no economic buyer, K6 solved cheaply already, K9 causation not attributable
  *by any design*, K10 misaligned incentives, K11 vanishing problem, K12 hype dependency,
  K14 extractive/toxic, K16 structural bottleneck, K17 no transferable learning, K18 single
  gatekeeper.
- **Kept as a hard kill for the first wedge only:** K13 safety-critical failure at the proof
  stage.
- **Converted from kills to wedge-axis scores:** K1 access → ACC_A / ACC_B; K5 proof cycle → TTP;
  K7 licence → access tier B; K8 capital → access tier B; K15 enterprise sales → URG and TTP.
- **New kill:** tier C access.
- **New rule:** when K6 (already solved) is invoked, the invoker must name the incumbents *and*
  state which segments were checked for an unserved wedge.

## WEDGE axis (first-experiment practicality), weights sum to 100

| Code | Weight | Anchor for 5 |
|---|---|---|
| WSEV | 14 | First wedge worth > £50k/yr to a typical buyer, counting **cash or monetisable productivity** (hours, throughput, capacity) |
| MEAS | 14 | A credible counterfactual exists within 12 weeks by *any* design: cash look-back, A/B or stepped rollout, interrupted time series on a stable baseline, matched sites. Cash is not required |
| URG | 14 | Budget holder acts without being chased |
| ACC_A | 14 | Tier-A operator can start with public or routinely exported data |
| SOLV | 12 | Bottleneck is mostly process/information, not power or physics |
| TTP | 10 | Credible evidence in < 4 weeks |
| SAT (inverse) | 10 | No credible provider serves the wedge segment |
| RISK (inverse) | 7 | Minimal legal/safety/reputational risk at proof stage |
| IMPL (inverse) | 5 | Analysis of existing data; no integration |

## CEILING axis (capability trajectory), weights sum to 100

| Code | Weight | Content |
|---|---|---|
| **CEIL** | **50** | **Economic Capability Ceiling**: mean of the ten sub-factors below |
| COMP | 12 | Each implementation improves the next (shared rule base, benchmarks, data) |
| REP | 10 | Same mechanics across many organisations and sectors |
| MOAT | 10 | Accumulated evidence, integrations, benchmarks or distribution become hard to copy |
| ACC_B | 10 | The mature form is reachable with partners/capital (5 = clearly) |
| LEARN | 8 | Teaches the operator to understand and redesign economic systems |

### ECONOMIC CAPABILITY CEILING sub-factors (each 0–5, equal weight)

The question: *"If we became world-class at solving this class of problem, how consequential
could that capability become?"* It deliberately does **not** score market size (TAM).

| Code | Sub-factor | 5 means |
|---|---|---|
| T | Transferability | Same capability applies across many industries |
| K | Depth of operational knowledge | Mastery requires and builds deep understanding of how operations actually run |
| S | Strategic importance | Problem sits on a critical path (safety, housing, energy, health, trade) |
| P | Productivity vs redistribution | Solving it raises output or frees capacity. Recovering money from a counterparty scores 1 |
| I | Diagnosis → intervention | Capability can move from finding the problem to changing the operation |
| E | Proprietary operational evidence | Every engagement yields outcome data others cannot see |
| Z | Productisation | Knowledge can become software, benchmarks or standard methods |
| V | Enterprise-value participation | Could eventually take part in value creation (shared savings, equity, outcome contracts), not just fees |
| A | Usefulness as AI becomes more capable | Better models make the capability *more* valuable rather than commoditising it |
| J | Adjacency | Leads naturally into larger economic problems |

## Combining the axes (ceiling cannot overpower practicality)

1. Kills v2 first.
2. **Gates:** WEDGE ≥ 60 **and** CEILING ≥ 60. Failing either gate leaves the candidate
   "parked". It is not killed.
3. **Rank** passing candidates by the **geometric mean √(WEDGE × CEILING)**. The geometric mean
   punishes imbalance: 90/40 scores 60, 65/65 scores 65.
4. **Confidence gate for selection:** evidence confidence ≥ M on WSEV, MEAS, ACC_A, URG *and*
   on at least 5 of the 10 CEIL sub-factors. CEIL sub-factors are the most speculative numbers in
   the lab, so they need their own evidence.
5. **Robustness:** a candidate must stay in the top 5 in ≥ 75% of random weightings
   (Dirichlet(1) within each axis) to be called robust.

## Mandatory checks on every run

- **Archetype bias re-audit:** report WEDGE, CEILING and combined means for leakage vs other
  archetypes. A combined gap of more than ±5 points in either direction triggers a written
  explanation. v2 was built to remove a pro-leakage bias, so it must be watched for the reverse:
  over-rewarding high-ceiling narratives.
- **Archetype coverage test** (`scoring/v2/coverage.py`).
- **Red-team protocol** from `opportunity_rubric.md` §6, plus the meta questions in
  `decision_record_v2.md`.

<!-- section 'First run of v2' removed for blind review: contains prior results -->

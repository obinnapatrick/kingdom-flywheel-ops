# Opportunity Rubric

The rubric ranks candidates that have **already survived `kill_criteria.md`**. It makes judgement
explicit and comparable. It does not make the decision: the red team, evidence confidence and
weight-sensitivity do.

## 1. Scoring scale

Each dimension is scored 0–5, where **5 is always the favourable end**. Dimensions where "more is
worse" (implementation cost, risk, competitive saturation) are scored inversely so that 5 means
low cost / low risk / low saturation.

Every score is accompanied by the evidence behind it (see `evidence/candidates/`). Each candidate
also carries an overall **evidence confidence** (H / M / L):

- **H** — key magnitudes supported by primary sources that were read.
- **M** — key magnitudes supported by named independent sources seen second-hand (`REPORTED`).
- **L** — key magnitudes rest mainly on vendor claims or our own assumptions.

A candidate with confidence L **cannot be selected**, whatever its score. It can only be
promoted to further evidence gathering.

## 2. Dimensions and anchors

| Code | Dimension | Question | 0 | 3 | 5 |
|---|---|---|---|---|---|
| SEV | Economic severity | How much money/time/output is genuinely lost — *capturable* per buyer and in aggregate? | Trivial or unknown | £10k–£100k/yr per buyer, £100m+ aggregate | >£100k/yr per buyer, £1bn+ aggregate, evidenced |
| FREQ | Frequency | How often does the loss event recur? | Once / rarely | Monthly | Daily or per transaction |
| MEAS | Measurability | Can before/after value be measured with a credible counterfactual? | No metric | Metric exists, confounded | Value appears as discrete verifiable cash or time with a natural counterfactual |
| ACC | Accessibility | Can a new solo operator reach the workflow *and* the data? | Requires insider status | Reachable with trust-building; data shareable | Public data or data the buyer routinely exports |
| TTP | Time to proof | How soon can meaningful evidence of value exist? | >12 months | 2–4 months | <4 weeks |
| SOLV | Solvability | Can the bottleneck actually be changed by an intervention? | Structural / power-driven | Partly process, partly power | Mostly process, information or error |
| REP | Repeatability | Does the same problem recur across many organisations? | Bespoke | Hundreds of similar orgs | Tens of thousands, same mechanics |
| URG | Buyer urgency | Does someone with authority have financial reason to act now? | No budget holder cares | Cares, low priority | Budget holder acts on it without being chased |
| IMPL | Implementation cost (inverse) | What does a real intervention require before value is shown? | Hardware/integration >£25k | Moderate integration, weeks of build | Spreadsheet/analysis on exported data |
| RISK | Risk (inverse) | Legal, regulatory, security, safety, reputational, operational | Severe/likely | Manageable with care | Minimal |
| SAT | Competitive saturation (inverse) | Are strong solutions already widespread? | Commoditised, dominant incumbents | Several credible providers, gaps exist | Few or no credible providers |
| COMP | Compounding potential | Does each engagement produce reusable knowledge, benchmarks, data or tooling? | Nothing carries over | Some templates carry over | Every case enriches a shared dataset / rule base |
| AIL | AI leverage | Can increasingly capable AI materially improve the economics? | None | Useful assist | Core cost driver falls sharply with better models |
| PIND | Provider independence | Could the core survive if a model provider vanished? | Single-provider dependency | Swappable with effort | Works without LLMs; AI is additive |
| LEARN | Operator learning | Does it teach transferable economic/system skills? | Narrow trick | Some transferable skills | Broad: B2B trust, measurement, regulation, data |
| MOAT | Moat trajectory | Could accumulated evidence, integrations, benchmarks, distribution or workflow knowledge become hard to copy? | Copyable in a weekend | Copyable in months | Requires years of accumulated cases/data |

## 3. Weights and why

Weights were set **after** defining the dimensions, from the lab's objective: create *verified*
value, learn fast, as a solo operator, without being fooled.

| Code | Weight | Rationale |
|---|---|---|
| MEAS | **10** | Highest. The lab's objective is *verified* value. If we cannot measure it we cannot learn, sell on evidence, or know whether we were wrong. |
| SEV | **9** | Value must be large enough to matter and to pay for acquisition. Not higher than MEAS because headline severity figures are the most frequently inflated numbers in this domain. |
| ACC | **9** | A large problem we cannot reach produces zero learning. For a solo operator, access is the binding constraint more often than value. |
| TTP | **9** | Learning rate compounds. A lab running 6 cycles a year beats one running 1. |
| URG | **9** | Without a motivated budget holder, even proven value does not convert. |
| SOLV | **7** | Some problems are structural (power, law). Important, but partly captured by kill K16. |
| FREQ | **6** | Frequent events give more data points and faster statistics; partly overlaps TTP. |
| REP | **6** | Needed for scale and compounding, but the first laboratory matters more than the tenth. |
| RISK | **6** | Hard risks are already handled by kills (K7, K13, K14); this weight covers residual risk. |
| SAT | **6** | Saturation compresses capturable value; but some saturation also proves a market exists. |
| IMPL | **5** | Low cost matters, but high cost is mostly filtered by K8. |
| COMP | **5** | The long-term objective ("very large value") depends on compounding, but only after a first win. |
| LEARN | **4** | Objective 10 requires learning value even in failure; partly a tiebreaker. |
| MOAT | **4** | Early-stage moat predictions are unreliable; weighted modestly to avoid storytelling. |
| AIL | **3** | Deliberately low. The constitution forbids favouring AI; AI leverage is upside, not a reason. |
| PIND | **2** | A hygiene factor; most candidates can be built provider-agnostic. |
| **Total** | **100** | |

**Score** = Σ(score × weight) / (5 × Σweights) × 100.

## 4. Sensitivity (mandatory)

Weights are judgement. Every scoring run must also rank candidates under alternative weight sets
(`scoring/score.py`): **equal**, **value-heavy**, **speed-heavy** and **defensibility-heavy**.
A candidate is **robust** only if it stays in the top half under all of them. Non-robust
candidates can survive but must be flagged. Differences of less than ~5 points are treated as
ties: that is roughly two single-point judgement changes on heavily weighted dimensions.

## 5. Tests applied after scoring

1. **Competitor test** — list who solves it today, at what price, and why the problem persists
   anyway. If persistence cannot be explained, assume we are missing a competitor.
2. **Access test** — name the concrete route to the first workflow and dataset, and what the
   buyer must hand over. Rate trust required.
3. **Economic test** — total problem → recoverable → capturable by a small operator → payable
   (willingness to pay). Show the arithmetic and label each input.

## 6. Red-team protocol

For each surviving candidate, a written attack answering:

1. Why has nobody already solved this?
2. Who is already solving it extremely well?
3. Why would a company trust us?
4. Why wouldn't the company build it internally?
5. Why wouldn't Microsoft, Google, Anthropic, OpenAI, Palantir, ServiceNow, UiPath or an industry
   incumbent make this irrelevant?
6. What happens as AI becomes dramatically cheaper and more capable?
7. Could a competitor copy the software in one weekend?
8. What could become genuinely difficult to copy?
9. Is the claimed economic loss actually recoverable?
10. Are we confusing a large market with an accessible market?
11. Are customers sufficiently motivated to change behaviour?
12. Can we get real data?
13. Can we demonstrate causation rather than correlation?
14. Can a one-person operator realistically begin here?
15. If the first experiment fails, will we still learn something valuable?

A candidate proceeds to selection only if the red team fails to produce a kill **and** its
evidence confidence is at least M on the dimensions SEV, MEAS, ACC and URG.

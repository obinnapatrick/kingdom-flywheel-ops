# Decision Record v2

`decision_record.md` (DR-001) is preserved unchanged. This file records DR-002.

## DR-002 — Red team of the selector (Phase Zero, step 1B), 2026-09-29

### Decision

**No arena selected.** The v1 selector was materially biased (`selector_audit_v1.md`). The
methodology has been replaced by `rubric_v2.md`. Under v2, four arenas are robust, but none meets
the evidence-confidence gate for selection.

### Why the methodology changed (summary)

1. The v1 selector favoured leakage/recovery problems: +6.7 points, p = 0.008. The cause was the
   measurability anchor and proof-speed weights, not chance.
2. Reweighting could not remove the bias (it persisted in 97.6% of random weightings), because it
   lived in the anchors and in candidate generation.
3. The first scan left 7 of 18 problem archetypes without a primary candidate
   (`archetype_coverage_v1.md`).
4. Three operator constraints (solo, unlicensed, ≤ £25k) were invented, not authorised. They
   killed operationally deep candidates.
5. There was no dimension for long-term capability ceiling, and none separating productivity
   from redistribution.

### Work done

- Bias audit with permutation, decomposition, counterfactual-weight and random-weight tests
  (`scoring/audit_v1/`).
- Archetype coverage test (`scoring/v2/coverage.py`).
- Second scan from scratch across under-represented archetypes: **25 new problems**, each with at
  least one evidence search, favouring official statistics (ONS, NHS England, DfT, DfE, Ofwat,
  NESO, CMA, WRAP, KCL). `second_scan_v1.csv`; sources S43–S77 in
  `evidence/source_register_v2.csv`.
- Competitive reality update on the four v1 finalists (below).
- Re-scored all 56 candidates on rubric v2 (`scoring/v2/`).

**Evidence limitation (unchanged):** the network policy still blocks gov.uk, ons.gov.uk,
england.nhs.uk, nao.org.uk, ofgem.gov.uk and neso.energy. Every new figure is `REPORTED` from
search excerpts. Vendor claims were not used as proof of magnitude; where only vendor evidence
exists, the candidate is marked S1-suspended.

---

## Task 6 — Competitive reality update on the v1 finalists

### Import duty (C25) — **materially weakened**

- Hypothesis given: the generic opportunity is smaller than implied. **Confirmed as far as
  evidence allows.** 47% of UK tariff lines are zero (S33), EU preference use is 90% (S25), and
  there are already AI and consultancy recovery offers (S42).
- Concentrated exceptions were searched: high-duty categories, special procedures such as
  inward processing and customs warehousing, and origin. **No quantified evidence was found for
  any of them.** They remain hypotheses.
- The large, real signal is **American, not British**. After the US Supreme Court struck down the
  IEEPA tariffs (20 Feb 2026), ~$165bn in refunds was ordered; CBP had authorised $104bn and paid
  $71bn by 29 June 2026 (S73). But it is a one-off event, processed through CBP's own importer
  refund system, and filing is dominated by licensed brokers.
- **Outcome:** the broad UK recovery thesis (C25) fails the CEILING gate and is parked. A broader
  arena, **C25b "trade-compliance decision quality under tariff volatility"**, is recorded
  separately. It passes both gates but has confidence L, and it was framed by this analyst in
  this session (halo risk).

### CPG deductions (C02) — **killed**

- Problem confirmed by the first independent source: the Credit Research Foundation found a median
  6–10% of deduction dollars invalid, and 15–20% in apparel (S75).
- Wedge search: every segment checked is now served. HighRadius (acquired Cforia) covers
  enterprise; SPS Commerce bought SupplyPike for $206m; Carbon6 covers Walmart 1P; Glimpse and
  iNymbus cover US natural-channel distributors (UNFI, KeHE) on success fees; Vividly covers trade
  promotion (S76). The UK version is constrained by the Groceries Code (S31).
- **Outcome: K6.** The problem is genuine, but no meaningful unsolved wedge remains for a new
  entrant. Kept as a reference for well-measured leakage mechanics.

### Construction (C27) — **split into layers; collection layer weakened; pre-dispute layer promoted as a new arena**

| Layer | Evidence | Verdict |
|---|---|---|
| Retentions | Ban confirmed; not before 2027, then 12–24 month transition (S37) | K11. No thesis built on it |
| Ordinary late payment | Structural/power-driven; reforms tightening terms (S37); ~£6bn/yr claimed cost of late and non-payment (S70, untraced) | K16 |
| Applications for payment | 73% of subcontractors report routine disputes over applications (S27, vendor) | Part of the pre-dispute layer |
| Variations | "Changes by clients" is a leading dispute cause; variations appear in 21% of adjudication experience (S69) | Part of the pre-dispute layer |
| Final accounts | "True value" final-account claims experienced by 35–38% (S69) | Recovery. Weakened with C27 |
| Evidence / documentation failure | **Inadequate contract administration is cited as a cause by 50%; lack of competence by 42% (S69)** | **Core of the pre-dispute layer** |
| Formal disputes | Record 2,264 adjudication referrals per year; most common claim £125k–£500k; smash-and-grab / technical notice claims experienced by 63% (S69) | Downstream symptom |

**Finding.** The pre-dispute layer is a more attractive *systems* problem than debt recovery.
1. Both sides lose. Main contractors lose smash-and-grab claims for missed notices; subcontractors
   lose true value.
2. Preventing disputes creates value rather than moving it between parties.
3. The mechanics (notices, time bars, change records) recur across every standard form of
   contract.

It is recorded as a new candidate, **C27b "construction contract administration reliability"**,
with its own evidence, per the anti-gaming rule in `kill_criteria.md`.

Competitive reality: on NEC projects this is served by Thinkproject CEMAR, which is used by
larger organisations and has added AI in 2026 (S71). The JCT and subcontract SME segment appears
less served. That is `HYPOTHESIS`, not verified.

### Energy (C26) — **killed**

- As instructed, basic half-hourly out-of-hours analysis was assumed to be commoditised, and I
  looked for evidence against that. Instead the evidence confirmed it: British Gas (Energy360,
  with explicit out-of-hours reporting), EDF, Yu, SSE and TotalEnergies all give business
  customers free half-hourly analytics (S74).
- A replacement energy wedge (business demand flexibility, N24) was tested and killed on value.
  The Demand Flexibility Service saved an estimated £483k nationally in winter 2024–25 (S67).
- **Outcome: K6.** Energy waste exists, but this wedge is not retained.

---

## Results under rubric v2

56 candidates scored: 29 original, 2 derived arenas, 25 new. 32 killed; 24 survive the kills; 9
pass both gates. Full table: `scoring/v2/results_v2.md`.

| Rank | Arena | Archetype | Tier | WEDGE | CEILING | √(W×C) | Robust (top-5 share) | Confidence |
|---|---|---|---|---|---|---|---|---|
| 1 | C27b Construction contract administration reliability | Information flow / coordination | A | 69.8 | 92.0 | 80.1 | 100% | M |
| 2 | N19 Inventory & working-capital decisions (mid-market) | Inventory / forecasting | A | 68.4 | 87.0 | 77.1 | 97% | M |
| 3 | N08 SME manufacturing throughput (OEE) | Throughput / asset utilisation | B | 62.6 | 93.0 | 76.3 | 82% | M |
| 4 | C25b Trade-compliance decision quality | Decision latency / compliance | B | 63.6 | 90.0 | 75.7 | 84% | **L** |
| 5 | N05 High-risk building Gateway 2 submission quality | Compliance / information flow | B | 69.8 | 79.4 | 74.4 | 51% (not robust) | M |
| — | Pass gates, not robust | C12, N18 (S1), N21 (S1), C30 | | | | | | |
| — | Parked: high ceiling, fails WEDGE gate | C03 downtime, N06 management practices, N01 delayed discharge, N02 theatres, N09 food forecasting, N22 RFQ latency | | | | | | |

**No arena passes the selection-confidence gate**: none has evidence confidence ≥ M on WSEV,
MEAS, ACC_A and URG *and* on 5 of the 10 ceiling sub-factors. The ceiling sub-factors are
analyst judgement with no evidence yet.

---

## Red team of the top arenas (hardest on the two this analyst reframed)

### C27b Construction contract administration reliability
- **Is it just C27 rebranded to survive?** Partly. Its evidence (S69) is new and independent, the
  buyer set is different (both contract sides), and the value is avoided disputes, not collected
  debt. But the analyst who proposed it also scored it, and it came out 100% robust. **Treat the
  rank as inflated until an independent re-score confirms it.**
- **Who solves it well?** CEMAR on NEC; experienced QSs; construction lawyers. Why it persists:
  the cost of poor administration is paid later, by a different budget (disputes), and small
  firms lack commercial staff. `HYPOTHESIS`.
- **Weekend copy?** A notice-deadline tracker, yes. A clause-level rule base across JCT/NEC/bespoke
  amendments, linked to outcome data (which failures became disputes, and what they cost), no.
- **AI much better?** Makes contract reading cheap, so a document-reading product commoditises.
  Outcome data and embedded workflow do not.
- **AI consultancy risk: HIGH.** The obvious wedge (review a firm's contracts and notices) is a
  consulting deliverable. It only compounds if each engagement adds to a shared rule base and
  outcome benchmark.
- **Magnitude:** 2,264 adjudications a year is a *symptom count*. The avoidable cost of poor
  administration per firm is unmeasured. The £6bn late-payment figure (S70) is untraced.
- **Causation:** disputes are rare per contract, so proving *prevention* needs many contracts or a
  long time. A look-back design (how many past disputes trace to administration failures) is
  feasible but shows correlation, not prevention.

### N19 Inventory & working-capital decisions (mid-market)
- **Who solves it well?** A crowded planning-software market (Netstock, Slimstock, Inventory
  Planner, ERP modules; not individually verified). Why it persists: adoption and
  planning-discipline gaps, not missing algorithms. `HYPOTHESIS`.
- **Evidence:** PwC data covers listed companies only (S62); no independent mid-market magnitude.
  Stock-out evidence is academic but retail-grocery-centric (S66).
- **Strength:** cash released and service levels are measurable with a stable baseline, and each
  engagement builds demand-pattern benchmarks by sector. This is productivity (capital
  efficiency), not recovery.
- **Risk:** it becomes "inventory consulting" unless the method is productised.

### N08 SME manufacturing throughput
- **Strength:** highest ceiling of the survivors. It is pure productivity, transfers across
  manufacturing, and moves naturally from diagnosis to intervention.
- **Weaknesses:** needs shop-floor access (tier B); OEE benchmarks are practitioner lore, not
  evidence (S51); Made Smarter and OEE-monitoring vendors are active; a bootstrap operator's
  first wedge is unclear.

### C25b Trade-compliance decision quality
- **Weakest evidence (L).** The scale signal is US and one-off (S73). The UK pool is unquantified.
  Also reframed in-session (halo risk).
- **Strength:** tariff volatility makes classification, origin and sourcing decisions more
  consequential. AI makes the rule base more valuable. Proprietary outcome data (rulings, accepted
  claims) compounds.

### N05 Gateway 2 submission quality
- **Weaknesses:** low volume (~1,500 decisions a year; S47), regulator performance improving fast
  (12–15 weeks now), specialist consultancies exist (S72), life-safety domain.
- Its value is as a **member of a family** with C12 (planning invalidation, 324k applications a
  year): "regulatory submission quality", which is information-quality work before a regulator
  decision. That family has not been scored as one arena. Open question.

---

## Meta red team (Task 7)

| Question | Honest answer |
|---|---|
| Are we selecting problems that are easy for AI to demonstrate? | **v1: yes.** Document-matching recovery demos well. **v2: partly still.** The #1 arena (contract administration) is text-heavy, exactly where LLM demos look impressive. The guard is that its value must be proved as disputes avoided, not documents read. |
| Are we confusing recoverable cash with productivity creation? | **v1: yes.** Nothing in v1 distinguished them. v2 scores it (sub-factor P). The risk of relapse is real: C27b's easiest wedge (spotting missed notices) turns back into claims recovery. |
| Are we overweighting fast case studies? | v1: yes (72% of the bias came from the proof cluster). v2 keeps speed on the WEDGE axis only, behind a gate. |
| Are we underweighting difficult but transformational workflow problems? | **Still somewhat.** Downtime (C03), management practices (N06) and delayed discharge (N01) have the highest ceilings but fail the WEDGE gate. The gate is deliberate: we need a first experiment. But these must stay on a **tier-B watchlist**, to be re-opened when a partner or design customer appears, not quietly forgotten. |
| Are we selecting service businesses instead of compounding capabilities? | **The main live risk.** Every top arena's obvious wedge is analyst-delivered. The test to apply: does engagement #21 ship with a rule base, benchmark or dataset materially better because of #1–#20? C27b, N19, N08 and C25b plausibly can; N05 (low volume) is doubtful. |
| Are we accidentally designing an AI consultancy? | **Yes, if nothing changes.** Countermeasure adopted in rubric v2: a wedge counts only if its deliverable is a *measured operational change plus a reusable artefact*, never a report. |
| Would mastering this make the operator better at redesigning economic systems? | N08 and N19: yes (operations and supply-chain mechanics). C27b: yes (inter-firm incentives, contracts, coordination). C25b: yes (regulation and trade). The v1 recovery wedges: mostly no. |
| Would implementation #20 make #21 better? | Plausible for C27b (clause and outcome base), N19 (demand-pattern benchmarks), N08 (loss taxonomy by process), C25b (rulings and outcomes). Not yet evidenced for any. |
| Could the capability affect businesses much larger than the first customer? | C27b: main contractors and clients set contract-administration standards down supply chains. N19/N08: supplier performance feeds large OEM and retailer supply chains. C25b: sourcing decisions. |

**Meta verdict:** the mission framing holds, but the lab has two failure modes to guard against:
(1) drifting back to recovery because it is easy to prove; (2) drifting into an AI-flavoured
consultancy because every first wedge is analyst work. v2 guards against the first. The second
needs a hard rule at wedge-design time, and has one now.

---

## Status of the original four finalists

| Finalist | Outcome |
|---|---|
| UK import-duty overpayment (C25) | **Materially weakened**, parked; replaced by C25b arena (confidence L) |
| US CPG deductions (C02) | **Killed** (K6) |
| UK construction subcontractor recovery (C27) | **Materially weakened**, parked; pre-dispute layer re-entered as C27b |
| UK out-of-hours electricity (C26) | **Killed** (K6) |

## Unresolved questions

1. Do the CEILING sub-factor scores hold up under an independent re-score? They now decide the
   ranking.
2. What is the avoidable (not recoverable) cost per typical buyer in C27b, N19 and N08?
3. Is there a tier-A wedge in N08, or does it need a design partner?
4. Is "regulatory submission quality" (C12 + N05 + customs declarations C24) one arena with a
   larger ceiling than its parts?
5. Throughput, coordination and asset utilisation still have only one primary candidate each.

## Evidence Sprint 2 (the next action)

Desk research only. No company contact, no building. Precondition: network access to gov.uk,
ons.gov.uk, nhs.uk, nao.org.uk, kcl.ac.uk, wrap.ngo and neso.energy.

| Step | What | Kill / promote rule |
|---|---|---|
| E1 | **Blind re-score.** A separate reviewer re-scores the 9 gate-passing arenas from `second_scan_v1.csv` / ledger evidence only, without seeing our scores | Any arena whose combined rank moves > 3 places is marked unstable and cannot be selected |
| E2 | C27b: read KCL 2024 report and Arcadis UK data in full; find any quantification of avoidable dispute/administration cost; map JCT/subcontract tooling | Kill if avoidable cost per mid-sized contractor cannot be bounded above £50k/yr, or if the JCT/SME segment is served |
| E3 | N19: independent (ONS/BoE/academic) evidence on mid-market inventory levels and planning maturity; tool-adoption rates | Kill if no independent magnitude or if adoption of planning tools is already high in the segment |
| E4 | N08: ONS/BEIS productivity dispersion within manufacturing; independent OEE/loss evidence; identify a tier-A entry | Park as tier-B watchlist if no tier-A entry exists |
| E5 | C25b: gov.uk preference utilisation tables, HMRC repayment statistics, UK trade-remedy data | Kill C25b if the UK decision pool cannot be bounded |
| E6 | Upgrade every `REPORTED` figure used by these arenas to `FACT` or strike it; re-run `scoring/v2/score_v2.py` and the bias re-audit | Selection may be considered only if an arena passes the confidence gate afterwards |

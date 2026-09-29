## PART 1 — BLIND SCORE (locked; see audit log for sha256)

Written before any web research and before opening any forbidden file. Inputs used: CLAUDE.md,
redacted rubric v2, kill_criteria.md, evidence/README.md, the two source registers (treated as
unverified leads), and the reviewer's own background knowledge. Every score below is `ESTIMATE`
(judgement made explicit). No evidence claim in Part 1 is `FACT`.

### Scoring conventions (the rubric does not spell these out, so they are stated here)

- Each code is scored 0–5. **Inverse codes (SAT, RISK, IMPL) are scored so that 5 = the favourable
  anchor** stated in the rubric (5 = no credible provider / minimal risk / analysis of existing data).
- `WEDGE = Σ(weight × score) / 5` over WSEV 14, MEAS 14, URG 14, ACC_A 14, SOLV 12, TTP 10, SAT 10,
  RISK 7, IMPL 5 (weights sum to 100, so max = 100).
- `CEIL mean` = arithmetic mean of the ten sub-factors T K S P I E Z V A J (0–5).
- `CEILING = 50 × CEILmean / 5 + Σ(weight × score)/5` over COMP 12, REP 10, MOAT 10, ACC_B 10, LEARN 8.
- `Combined = √(WEDGE × CEILING)`. Gates: WEDGE ≥ 60 and CEILING ≥ 60.
- Calculation script: `scratchpad/ir/score.py` (reproduced in the Appendix). Robustness: 5,000
  Dirichlet(1) weight draws within each axis (CEIL block weight also drawn).

### Score table (inputs)

| Arena | WSEV | MEAS | URG | ACC_A | SOLV | TTP | SAT | RISK | IMPL | T | K | S | P | I | E | Z | V | A | J | COMP | REP | MOAT | ACC_B | LEARN |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 Accountancy capacity | 3 | 3 | 3 | 3 | 4 | 3 | 1 | 3 | 2 | 3 | 2 | 2 | 4 | 3 | 2 | 4 | 2 | 1 | 3 | 2 | 4 | 1 | 4 | 2 |
| 2 B2B order entry | 3 | 5 | 3 | 3 | 5 | 4 | 1 | 4 | 2 | 3 | 2 | 2 | 3 | 3 | 2 | 5 | 2 | 1 | 3 | 2 | 4 | 1 | 4 | 2 |
| 3 Construction contract admin | 4 | 2 | 3 | 3 | 3 | 2 | 3 | 3 | 4 | 2 | 4 | 4 | 3 | 3 | 4 | 4 | 2 | 3 | 4 | 3 | 3 | 3 | 4 | 4 |
| 4 Customs / trade compliance | 3 | 5 | 4 | 4 | 4 | 3 | 2 | 3 | 5 | 3 | 3 | 4 | 2 | 3 | 4 | 4 | 3 | 2 | 3 | 4 | 4 | 2 | 4 | 3 |
| 5 HRB Gateway 2 | 5 | 1 | 4 | 2 | 3 | 1 | 3 | 2 | 3 | 1 | 4 | 5 | 4 | 3 | 3 | 3 | 2 | 3 | 3 | 3 | 1 | 3 | 3 | 3 |
| 6 Inventory & working capital | 4 | 3 | 3 | 4 | 4 | 2 | 2 | 4 | 4 | 4 | 4 | 3 | 4 | 4 | 4 | 4 | 4 | 3 | 4 | 4 | 5 | 2 | 4 | 4 |
| 7 MRO spares | 4 | 2 | 2 | 3 | 4 | 2 | 3 | 3 | 3 | 3 | 4 | 3 | 3 | 3 | 3 | 4 | 3 | 3 | 3 | 4 | 3 | 3 | 3 | 3 |
| 8 Planning validation | 2 | 4 | 2 | 5 | 4 | 3 | 2 | 4 | 4 | 1 | 2 | 4 | 3 | 2 | 2 | 4 | 1 | 1 | 3 | 3 | 2 | 1 | 3 | 2 |
| 9 SME manufacturing throughput | 4 | 3 | 2 | 2 | 3 | 2 | 3 | 3 | 2 | 5 | 5 | 4 | 5 | 5 | 5 | 3 | 4 | 3 | 5 | 4 | 5 | 3 | 4 | 5 |

### Results (computed)

| Arena | WEDGE | CEIL mean | CEILING | √(W×C) | Gates | Top-5 share (robustness) | Both gates pass share |
|---|---|---|---|---|---|---|---|
| 1 Accountancy capacity | 57.4 | 2.6 | 52.0 | 54.6 | PARK | 3% | 3% |
| 2 B2B order entry | 68.8 | 2.6 | 52.0 | 59.8 | PARK (ceiling) | 38% | 14% |
| 3 Construction contract admin | 59.0 | 3.3 | 66.6 | 62.7 | PARK (wedge, marginal) | 91% | 50% |
| 4 Customs / trade compliance | 73.6 | 3.1 | 65.4 | 69.4 | PASS | 99% | 88% |
| 5 HRB Gateway 2 | 54.6 | 3.1 | 57.0 | 55.8 | PARK | 5% | 1% |
| 6 Inventory & working capital | 66.4 | 3.8 | 76.0 | 71.0 | PASS | 100% | 87% |
| 7 MRO spares | 57.6 | 3.2 | 64.4 | 60.9 | PARK (wedge) | 61% | 31% |
| 8 Planning validation | 65.6 | 2.3 | 45.4 | 54.6 | PARK (ceiling) | 3% | 0% |
| 9 SME manufacturing throughput | 54.2 | 4.4 | 85.6 | 68.1 | PARK (wedge) | 99% | 7% |

Worked example (arena 6): WEDGE = (14·4+14·3+14·3+14·4+12·4+10·2+10·2+7·4+5·4)/5 = 332/5 = 66.4.
CEILING = 50·3.8/5 + (12·4+10·5+10·2+10·4+8·4)/5 = 38.0 + 190/5 = 38.0 + 38.0 = 76.0. √(66.4×76.0) = 71.0.

**Confidence gate (rubric step 4):** no arena has evidence confidence ≥ M on all of WSEV, MEAS,
ACC_A and URG at blind stage, because every magnitude in the registers is a search excerpt
(`REPORTED`). Therefore **no arena is selectable from Part 1**, whatever its number. The two gate
passes (6 and 4) are ranking signals only. Numbers are close: 6 vs 4 vs 9 differ by < 3 points on
the combined score, well inside judgement error.

**Self-audit of bias risk:** arena 9 gets the highest CEILING (85.6) almost entirely from
sub-factors that are narrative-heavy (T, K, I, E, J all 5). This is exactly the "over-rewarding
high-ceiling narratives" failure the rubric warns about. Its WEDGE (54.2) is the lowest but one.
Arena 4's WEDGE is driven by MEAS 5 and IMPL 5 — a cash look-back is causally clean, but that is
the proof-speed cluster that the v1 audit found biased towards *recovery*; P = 2 records that
most of its near-term value is redistribution from HMRC.

### Per-arena assessments

#### 1. ACCOUNTANCY CAPACITY
- **First-experiment viability:** Moderate. One small practice, one workflow (e.g. year-end accounts prep or bookkeeping review), measure hours per job from timesheets before/after. Feasible but confidential client data and professional-liability sensitivity.
- **Long-term ceiling:** Low–moderate (CEILING 52). Capability is "professional workflow automation", which frontier AI labs and incumbent platforms are attacking directly.
- **Evidence confidence:** LOW. Only lead is S64, a survey sponsored by an outsourcer (vendor, kill S1 applies).
- **Accessibility:** Tier A (a small practice could agree), tier B for scale.
- **Competitive pressure:** Very high — Xero/Sage/Intuit ecosystems, Dext, Karbon, Silverfin, CCH/IRIS, AI-native start-ups, offshore outsourcers.
- **Hard to copy:** Little. Possibly a benchmarked library of per-task time standards across practices.
- **Strongest case for:** Real, recurring capacity constraint in a regulated profession; capacity freed is genuine productivity (P = 4).
- **Strongest case against:** The value is being competed away by AI and outsourcing; nothing compounds for a small operator; evidence is vendor-only.
- **Fatal unknown:** Whether "turning away work" is a staffing-pipeline problem (not solvable by workflow change) or a throughput problem.

#### 2. B2B ORDER ENTRY (disclosed prior-venture overlap; no bonus applied)
- **First-experiment viability:** High. Historic order emails/PDFs + ERP order lines give a ground-truth set; accuracy and touch time measurable in weeks.
- **Long-term ceiling:** Low–moderate (CEILING 52). Document-to-ERP extraction is a commodity capability.
- **Evidence confidence:** LOW for magnitude (S30 vendor-only). HIGH that the activity exists.
- **Accessibility:** Tier A.
- **Competitive pressure:** Very high — Conexiom, Esker, Rossum, Nanonets, many AI start-ups, ERP vendors adding native capture.
- **Hard to copy:** Customer-specific mapping libraries (weak); ERP integrations (moderate).
- **Strongest case for:** Cleanest measurement of any arena; clear economic buyer.
- **Strongest case against:** The capability is precisely what 10× better AI makes free; SAT = 1; ceiling fails the gate.
- **Fatal unknown:** Whether any residual value survives once generic LLM extraction is bundled in ERPs.

#### 3. CONSTRUCTION CONTRACT ADMINISTRATION
- **First-experiment viability:** Moderate–low. A look-back on closed subcontract packages can find missed notices and unrecorded variations quickly, but that is *diagnosis*; causal proof that better administration *prevents disputes* needs long horizons because disputes are rare, lagged events (MEAS 2).
- **Long-term ceiling:** Moderate–high (CEILING 66.6): deep operational knowledge, strategic sector, proprietary project-outcome data, adjacency to commercial management.
- **Evidence confidence:** LOW–MEDIUM. The KCL/Adjudication Society report (S69) is independent and academic, but only seen via excerpt. Respondent-experience percentages are not shares of cases.
- **Accessibility:** Tier A for look-back (documents a subcontractor holds); tier B for the mature form (needs QS/legal partners).
- **Competitive pressure:** Medium. CEMAR serves NEC tier-1; payment platforms (Payapps, TrakPro) serve application workflows; QS and claims consultants provide judgement. JCT subcontract administration by SMEs may be under-served (HYPOTHESIS).
- **Hard to copy:** Outcome-linked dataset of administration failures → dispute outcomes; a validated rule base of notice/timing failure patterns per contract form.
- **Strongest case for:** Independent academic evidence of a record dispute volume, with contract-administration failure named as a leading cause; disputes are deadweight loss (legal costs, management time) not just transfer.
- **Strongest case against:** Much of the payment conflict is *strategic* (power asymmetry, deliberate pay-less tactics) not error; software for the mechanical layer exists; the non-mechanical layer is legal/QS judgement where liability sits; proof horizon is long.
- **Fatal unknown:** What fraction of disputes/value loss is caused by administrative *error* (fixable) rather than deliberate commercial behaviour (K16 structural bottleneck).

#### 4. CUSTOMS / TRADE-COMPLIANCE DECISIONS
- **First-experiment viability:** High. An importer's own declaration data (CDS export) can be audited retrospectively; overpaid duty found and repaid is a causally clean cash outcome.
- **Long-term ceiling:** Moderate (CEILING 65.4). Near-term value is mostly *redistribution* (repayment from HMRC; P = 2); productive value (fewer errors, better origin/sourcing decisions, lower admin burden) is real but harder to prove.
- **Evidence confidence:** LOW–MEDIUM. HMRC admin-burden and preference-utilisation statistics exist (S24, S25) but only seen via excerpt; the error-rate evidence (S39) is vendor-only.
- **Accessibility:** Tier A (importer's own data), tier B for mature form (customs broker / authorised status partners).
- **Competitive pressure:** Medium–high — duty-recovery specialists, brokers, Big-4 indirect-tax teams, classification software (Descartes, Thomson Reuters, TariffTel) and new AI entrants (S42).
- **Hard to copy:** Error-pattern rule base linked to repayment outcomes; HMRC ruling/acceptance patterns.
- **Strongest case for:** The only arena whose first wedge produces verifiable cash with a clean counterfactual in one cycle; data routinely available.
- **Strongest case against:** Largely recovery/redistribution; ~70% of MFN imports duty-free and 90% preference utilisation (both REPORTED) shrink the dutiable error pool; classification is a canonical target for AI commoditisation; crowded recovery market.
- **Fatal unknown:** The size of the recoverable overpayment pool for a *typical* mid-size importer, net of underpayments the audit would also surface.

#### 5. HIGH-RISK BUILDING APPROVAL SUBMISSIONS (Gateway 2)
- **First-experiment viability:** Low. One HRB project, decision times of months, BSR performance itself changing → almost no counterfactual (MEAS 1, TTP 1).
- **Long-term ceiling:** Moderate (CEILING 57). Highly strategic (housing, safety) but England-only and a few hundred applications a year (REP 1).
- **Evidence confidence:** LOW–MEDIUM; S47 figures are REPORTED and describe a rapidly improving system.
- **Accessibility:** Tier B (developer + principal designer engagement needed).
- **Competitive pressure:** Medium — fire engineers, principal designers, specialist Gateway 2 consultancies (S72).
- **Hard to copy:** Record of which submission defects cause rejection.
- **Strongest case for:** Enormous per-project delay cost; strategic importance.
- **Strongest case against:** Problem is partly regulator capacity (structural, K16) and may be shrinking (K11 risk); safety-critical domain raises RISK; tiny N.
- **Fatal unknown:** Whether 2026 rejection causes are applicant quality (fixable) or regulator process (not).

#### 6. INVENTORY & WORKING-CAPITAL DECISIONS
- **First-experiment viability:** Moderate. ERP exports (sales history, stock, purchase orders) are routine; diagnosis in weeks; but economic outcome (lower stock at equal/better service) needs at least one to two replenishment cycles, so TTP 2 and MEAS 3 (stepped rollout across SKU groups or branches).
- **Long-term ceiling:** High (CEILING 76). Transfers across distribution and manufacturing; allocative productivity (capital and lost sales); decision rules productise.
- **Evidence confidence:** LOW. Only lead is PwC (S62), a consultancy study of listed firms. No independent mid-market evidence in the registers.
- **Accessibility:** Tier A.
- **Competitive pressure:** High and mature — ERP MRP, Slimstock, Netstock, EazyStock, GMDH, Lokad, RELEX, Inventory Planner, consultancies. SAT = 2 is generous; K6 is the key risk.
- **Hard to copy:** Cross-client evidence on which parameter/policy changes actually release cash without service loss, by demand pattern.
- **Strongest case for:** Large, recurring, cash-denominated problem with routinely exported data; strong transfer.
- **Strongest case against:** Arguably solved by mature tools; the residual may be behavioural/organisational (people override tools), and experiments are slow and noisy.
- **Fatal unknown:** Whether mid-market firms that *already own* forecasting/replenishment tools still hold materially excess stock (i.e. whether the problem survives the tools).

#### 7. MRO SPARE-PARTS INVENTORY
- **First-experiment viability:** Low–moderate. Master-data diagnosis is quick; stock reduction and avoided downtime are slow and rare events.
- **Long-term ceiling:** Moderate (CEILING 64.4).
- **Evidence confidence:** LOW; all magnitude claims vendor-only (S61, kill S1 applies).
- **Accessibility:** Tier A–B (needs an asset-intensive site to share CMMS/ERP data).
- **Competitive pressure:** Medium — Sparetech, Verusen, SAP/Maximo modules, consultancies.
- **Hard to copy:** Normalised cross-site parts catalogue and criticality/failure data.
- **Strongest case for:** Obsolete spares are plausibly large and ignored budget lines.
- **Strongest case against:** Low urgency (URG 2), vendor-only magnitude, slow proof, safety/downtime risk of under-stocking critical spares.
- **Fatal unknown:** Independent magnitude of excess/obsolete MRO stock.

#### 8. PLANNING APPLICATION VALIDATION
- **First-experiment viability:** Moderate: public portals show validation dates; an agent's invalidation rate is measurable.
- **Long-term ceiling:** Low (CEILING 45.4). England-only, per-application value small, government digital-planning programmes and AI checkers commoditise it.
- **Evidence confidence:** LOW: 45% is one council (S12); national invalidation rate unknown.
- **Accessibility:** Tier A.
- **Competitive pressure:** Medium–high and state-backed (Planning Portal, digital planning programmes).
- **Hard to copy:** Very little.
- **Strongest case for:** Public data; housing relevance.
- **Strongest case against:** Small value per event; K11 (policy/digital reform) risk; low ceiling.
- **Fatal unknown:** National invalidation rate and the delay cost it causes.

#### 9. SME MANUFACTURING THROUGHPUT
- **First-experiment viability:** Low–moderate (WEDGE 54.2). Needs on-site data collection because SMEs often lack clean production data; an interrupted time series on daily bottleneck output within 12 weeks is possible but confounded by order mix and demand; value only real if the firm is capacity-constrained rather than demand-constrained.
- **Long-term ceiling:** Very high (CEILING 85.6) — **flagged as the most narrative-dependent score in this table**.
- **Evidence confidence:** LOW–MEDIUM. ONS management-practice evidence (S48) is official but associational and seen via excerpt; OEE norms (S51) are practitioner lore.
- **Accessibility:** Tier A for one willing firm (manual data), tier B at scale.
- **Competitive pressure:** Medium — lean consultancies, Made Smarter advisers, MAS-type services, OEE/MES tools (FourJaw, Evocon, Guidance, MachineMetrics). Crowded at the tool layer; the "diagnose the real constraint + prove the gain" layer is served mainly by consultants.
- **Hard to copy:** Outcome-linked benchmark of constraints and intervention effects across plants — *if* measurement discipline is maintained.
- **Strongest case for:** Productivity (not redistribution), deepest operational knowledge, strongest transfer and adjacency, strategically important.
- **Strongest case against:** It is the classic "consultancy" trap (rule 22); SMEs are low-urgency buyers with poor data; proof is slow and confounded; the knowledge may be too plant-specific to compound.
- **Fatal unknown:** Whether constraint-diagnosis knowledge actually transfers between plants (i.e. whether deployment 50 is materially better than deployment 1) — and whether the typical SME is capacity- or demand-constrained.

**No winner is chosen in Part 1.**

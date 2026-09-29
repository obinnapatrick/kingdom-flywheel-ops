# Independent Review v1 — Economic Value Lab, Phase Zero step 1C

Reviewer: independent evidence reviewer (Claude, Opus-family). **Residual independence limitation:**
the previous analyst is the same underlying model family, so shared priors, shared search behaviour and
shared blind spots are likely even with strict file blinding. See Part 7.

Date: 2026-09-29. Audit log: `independent_review_audit_log.md`. Part 1 sha256 is recorded there.
Evidence labels follow CLAUDE.md rule 4 (FACT/VERIFIED, REPORTED, ESTIMATE, ASSUMPTION, HYPOTHESIS).
**Headline caveat:** the egress proxy blocked almost every primary document. Only two documents were
opened and read. Almost everything here is REPORTED.

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

---

### Post-lock revisions (Part 1 itself is unchanged; these are recorded separately, with reasons)

Made after Part 2 research and **before** opening any forbidden file.

| Arena | Code | Locked → revised | Reason (evidence label) |
|---|---|---|---|
| 4 Customs | ACC_A | 4 → 5 | HMRC's free "Get Customs Data" service (launched 13 Nov 2025) lets importers download ImportItem / ImportHeader / ImportTax-line CSV reports for up to four years back (REPORTED, several secondary sources agree) |
| 4 Customs | SAT | 2 → 1 | Many AI classification and declaration-audit products now openly target duty recovery (Freehand, iCustoms, Digicust, MIC, mycustomsinfo, ONESOURCE, Zonos) (REPORTED, vendor pages: evidence of competition only) |
| 4 Customs | A (AI usefulness) | 2 → 1 | Vendors already claim 95–97% classification accuracy. The claims are unverified, but they show the core analytic is being commoditised now |
| 9 SME mfg | SAT | 3 → 2 | Made Smarter already gives SMEs free "digital transformation roadmaps" (expert diagnosis) plus grants. That is a free, state-funded competitor for diagnosis (REPORTED) |
| 5 HRB Gateway 2 | URG | 4 → 3 | Gateway 2 approvals rose to 84% (12 weeks to 31 Aug 2026), and new-build determination times are falling (REPORTED, trade press citing BSR). The problem is shrinking (K11 risk) |
| 8 Planning validation | SAT | 2 → 1 | A government-funded Local Digital project, "Reducing Invalid Planning Applications", targets exactly this wedge (REPORTED) |

Recomputed: Customs WEDGE 74.4 / CEILING 64.4 / √ 69.2 (still PASS). SME mfg 52.2 / 85.6 / 66.8 (PARK). HRB 51.8 / 57.0 / 54.3 (PARK). Planning 63.6 / 45.4 / 53.7 (PARK). The ranking does not change. The Customs **CEILING** falls to within 4.4 points of its gate.

---

## PART 2 — PRIMARY EVIDENCE SPRINT

### 2.0 Access reality (read this first)

The egress proxy blocked **every** primary source I tried: gov.uk, assets.publishing.service.gov.uk,
kcl.ac.uk, adjudication.org, ukri.org, ciip/ifm.cam.ac.uk, productivity.ac.uk, oecd.org, nber.org,
arxiv.org, ncbi/europepmc, researchgate, lexology, law-firm sites, cato.org, uktradeinfo.com and others.
The audit log lists 34 attempts. Only two documents were actually opened and read:

1. **Innovation & Research Caucus Report 044**, *Impacts on Regional Growth and Policy Effectiveness: Addressing Barriers to Digital and Sustainable Adoption in West Midlands Manufacturing SMEs* (Mahmood, Asghar, Kousha, University of Wolverhampton, March 2026). It was served from an S3 bucket.
2. A **third-party archive (TheGovernmentSays, S3) of the gov.uk C285 guidance**. The archived version is "last updated 20 December 2021", so the current text may differ.

I also checked the public TheGovernmentSays mirror for the Made Smarter evaluation page. I downloaded the 158 mirrored gov.uk pages first seen between 30 Jul and 3 Aug 2026. The evaluation page is **not** among them.

**Consequence:** apart from the two items above, every external claim below is `REPORTED` (search-engine
excerpt). Some excerpts are AI-generated summaries of search results, and at least once I saw such a summary distort
a finding: a secondary source turned KCL's "63% of respondents experienced" into "63% of adjudications". So an excerpt is weak evidence even about what a document says.

Column key: **V/R** = VERIFIED (opened and read) or REPORTED (excerpt only).

### 2A. SME MANUFACTURING THROUGHPUT

**Thesis under test:** "The valuable capability is not technology adoption. It is discovering the true constraint, choosing the minimum effective intervention and proving the gain."

| # | Source | Date | Exact claim supported | Quality | Limitations | V/R |
|---|---|---|---|---|---|---|
| M1 | DBT/DSIT, *Made Smarter Adoption: impact and process evaluation* (gov.uk publication page; report + technical annex) | Published 30 Jul 2026; covers Apr 2022–Mar 2025 | **The publication exists**, and it is an independent evaluation of design, delivery and impact using counterfactual analysis | Official, independent evaluator (a Cambridge CIIP/IfM study is linked to it) | Page and PDF blocked | REPORTED |
| M1a | Same, as summarised by excerpts | 2026 | "97% of firms that adopted digital technologies reported benefits such as improved production and planning efficiency, and reduced costs" | Self-report by beneficiaries | Self-report; no counterfactual | REPORTED |
| M1b | **The claim to test:** "adoption increased substantially, but robust analysis did not yet identify statistically significant impacts on turnover, employment or productivity" | — | **NOT FOUND in any excerpt retrieved (5 queries).** I could not confirm or refute it | — | Cannot be treated as evidence either way | **UNVERIFIED** |
| M2 | Made Smarter North West **pilot** interim evaluation (via Made Smarter / CIIP excerpts) | c.2021–22 | Participation "statistically significantly correlated with turnover increase (6.5%) and employment increase (3.9%) against a counterfactual"; 84% self-reported productivity increase | Programme-commissioned | Different (earlier) evaluation; "correlated" wording; search summaries conflated it with M1 | REPORTED |
| M3 | UKRI/Innovate UK, *Evaluation of Made Smarter Innovation Challenge* (final) | May 2025 | Turnover impact "statistically insignificant" against matched unsupported firms (but c.23% above unsuccessful applicants' path); employment +14–15%, statistically significant, n=243 SMEs; main outcomes "not anticipated until 2026/27 and beyond" | Official, independent, econometric | R&D innovation challenge, **not** the adoption programme | REPORTED |
| M4 | Bloom, Eifert, Mahajan, McKenzie & Roberts, "Does Management Matter? Evidence from India", QJE 128(1) | 2013 | RCT, 28 plants in 17 textile firms: consulting-led adoption of 38 operational management practices raised productivity about 17–18% through quality, efficiency and inventory; informational barriers explained non-adoption | Peer-reviewed RCT (the gold standard here) | Large firms in India with very intensive consulting; external validity to UK SMEs unproven | REPORTED |
| M5 | Bloom et al., "Do Management Interventions Last?" AEJ: Applied | 2018/2020 | About 9 years on, treated plants had dropped about 40% of their practice gains, but a significant 19.7 pp practice gap remained and productivity was higher | Peer-reviewed follow-up | Same sample limits | REPORTED |
| M6 | ONS, *Management practices in the UK: 2016 to 2023* (MES) | 13 May 2024 | Mean management score 0.55 (2023) vs 0.49; production 0.52 vs services 0.56; management quality "significantly related" to productivity | Official statistics | Associational; firms with 10+ employees | REPORTED |
| M7 | ONS business dynamism/productivity bulletin (via excerpt); Centre for Cities "long tail" blog | 2024; n.d. | 67.7% of firms have labour productivity below the mean (2022). **Disconfirming:** the least productive 40% of firms (employment-weighted) produce about 12% of value added | Official + think tank | Aggregate, not per-firm opportunity | REPORTED |
| M8 | IRC Report 044 (Wolverhampton), West Midlands manufacturing SMEs | Mar 2026 | Verbatim: "firms face financial limitations, skills deficits and time and managerial capacity constraints that restrict strategic investment"; "regional policy should focus less on promoting individual technologies and more on addressing the conditions that shape manufacturing SME behaviour" | Academic, UKRI-funded, qualitative | Interviews and focus groups; LSBS regional cells tiny (West Midlands n=20/22); about adoption barriers, **not** throughput losses | **VERIFIED** |
| M9 | OEE "typical 60% vs world-class 85%" (Made Smarter blog, OEE literature) | various | Typical OEE figures | Practitioner lore | No sampled study found | REPORTED (treat as ASSUMPTION) |
| M10 | OECD D4SME 2025 survey | 2025 | Maintenance costs (40%), lack of training time and hardware cost are the top barriers to SME digitalisation | Intergovernmental survey | Not manufacturing-specific; not UK-specific | REPORTED |

**Findings on the sub-questions**

- **Prevalence of operational constraints:** Plausible, but not established for UK SMEs specifically. The only causal evidence (M4, M5) is from large Indian plants. The UK evidence (M6, M7, M8) is associational or qualitative. No source measures throughput, downtime, lead time, scheduling or visibility losses in UK SMEs from a sample. Every OEE figure is lore (M9).
- **Can SMEs provide the data?** Partly. M8 (verified) names *time and managerial capacity* as the binding constraints, so asking a small firm to collect data is itself a cost. Paper job tracking is common (vendor claim). An experiment must therefore bring its own low-burden measurement, such as manual tally or a clamp-on cycle counter at a single bottleneck. That is hardware, which pushes IMPL and TTP down.
- **Time for a credible before/after:** At the process level, about 12–16 weeks: 4–6 weeks of baseline, 1–2 weeks of intervention, 6–8 weeks after. At firm level (turnover or GVA), M1/M3 suggest 2–3+ years, and even well-funded evaluations may not detect effects.
- **Competition:** OEE and machine-monitoring tools (FourJaw, Evocon, Guidance, MachineMetrics, Amper; all vendor claims), MES/ERP, lean consultancies, Growth Hubs, and **Made Smarter itself, which provides free expert diagnosis ("roadmaps") and grants**. The layer *above* the tools (diagnose the true constraint, then prove the gain) is served by consultants and by Made Smarter advisers. What neither appears to do is publish outcome-linked, causally measured results. That gap is the only candidate wedge. HYPOTHESIS.
- **Does the knowledge transfer?** M4 is the best evidence. The practices were generic (38 standard practices) and informational barriers dominated, which suggests knowledge transfers at the practice level. The specific constraint in each plant is local. Transfer is moderate, not strong.
- **Fastest low-risk subsectors (ESTIMATE, reasoning only):** repeat-part discrete production with countable output per shift and short cycle times. Examples: plastics injection moulding, packaging and converting, sheet-metal or CNC job shops with repeat work, and non-food contract packing. Avoid food safety, pharma and anything that touches machine guarding.

**Does the Made Smarter evaluation strengthen or weaken the capability?** First, **the specific finding could not be verified** (M1b). Treated conditionally:
- *If true, it is consistent with* the thesis that adoption ≠ productivity, and so appears to strengthen "the value is in diagnosis and proof".
- *But it weakens the arena as a first experiment* for three reasons. (i) Made Smarter already includes expert diagnosis (roadmaps) and specialist advisers, so "diagnosis plus technology" was tried at scale, and on this reading it could not show firm-level economic effects within 1–3 years. (ii) It implies that firm-level outcomes are too noisy or lagged to measure causally at small N, which directly threatens gate condition (3). (iii) It shows a well-funded state competitor already occupies the diagnosis layer for free.
- **Net judgement: weakens.** It pushes any credible wedge down to *process-level* measurement (bottleneck output per shift). The link from process gain to firm economics then remains an unproven ASSUMPTION: a throughput gain is worth money only if the firm is capacity-constrained, not demand-constrained. M3 (verified-as-reported, a different programme) shows the same pattern of an insignificant turnover effect.

**Verdict 2A:** The problem exists in the general sense (REPORTED, including strong RCT evidence abroad). Its UK SME magnitude is unestablished. The thesis is a reasonable HYPOTHESIS but not supported by UK evidence, and its most relevant UK test is unverified and, if true, cuts both ways.

### 2B. CONSTRUCTION CONTRACT ADMINISTRATION

| # | Source | Date | Exact claim supported | Quality | Limitations | V/R |
|---|---|---|---|---|---|---|
| K1 | KCL Centre of Construction Law & Adjudication Society, *2024 Construction Adjudication in the United Kingdom: Tracing trends and guiding reform* (third and final report) | Nov 2024 | Record **2,264** referrals to adjudicator nominating bodies (ANBs), May 2023–Apr 2024, +9% year on year. Consistent across many independent law-firm summaries | Academic plus ANB returns (count data) | PDF blocked (both kcl.ac.uk and adjudication.org) | REPORTED (high consistency) |
| K1a | Same | Nov 2024 | ANB split: RICS 1,340; UK Adjudicators 461; TECSA 148; claims under £125k about 20% of referrals | As above | — | REPORTED |
| K1b | Same | Nov 2024 | "Inadequate contract administration" named as a principal cause of disputes by **50%** (of survey respondents) | Perception survey of adjudication users | Share of respondents, not of disputes; self-selected sample. **I did not find the 42% "lack of competence" figure in any excerpt I retrieved**; it rests only on the prior register | REPORTED (50%); 42% UNCONFIRMED |
| K1c | Same | Nov 2024 | "Smash-and-grab"/technical payment claims **experienced by 63% of respondents**; true value 35–38%; loss and expense/delay 35%; EOT 26%; variations 21%; defects 14% | As above | Respondent experience, not case shares. One secondary misreported it as "63% of adjudications" | REPORTED |
| K1d | Same | Nov 2024 | "Most common claim value £125k–£500k" | — | **Not surfaced in any excerpt I retrieved** | UNCONFIRMED |
| K2 | Law-firm cost guides (Helix Law, MJD, HK Legal, expert-evidence.com) | various | Each party usually bears its own costs (Total M&E v ABB, 2002; s.108A HGCRA); adjudicator fees about £7–15k; straightforward legal fees £5–13k | Practitioner marketing | Low-end, small-claim framing | REPORTED |
| K3 | CIC blog "The £6 billion question" | n.d. | Late and non-payment cost construction about £6bn/yr | Trade-body blog | Origin untraced; mostly a transfer, not deadweight | REPORTED (weak) |
| K4 | Competitor pages: Thinkproject CEMAR, Built Intelligence FastDraft (NEC EW/CE), Sypro (NEC/JCT/FIDIC), Archdesk, Payapps/TrakPro, Lexilio/other AI contract review | 2026 | Tools exist for notices, EW/CE logs, applications, deadline tracking and AI contract review; Sypro claims ">4 in 5 UK projects still rely on manual or inconsistent contract management" | Vendor | Vendor claims (S1); competitor evidence only | REPORTED |
| K5 | JCT guidance (JCT Ltd, law firms) | 2016/2024 | Pay-less notice no later than 5 days before the final date for payment; payment notice within 5 days of the due date; JCT 2024 spells out notice content | Contract-publisher guidance | Mechanical rules, so easily encoded | REPORTED |

**Separated answers**

1. **Problem existence:** *Strongly reported.* The adjudication count is administrative data aggregated from ANBs, and it is consistent across more than 8 secondary sources. Contract-administration failure is *perceived* by half of users as a principal cause. Status: REPORTED, not VERIFIED.
2. **Economic magnitude (deadweight only; payments themselves are transfers, rule 21):** ESTIMATE. 2,264 referrals × (adjudicator £7–15k + two parties' legal/expert costs of £10–60k each for mid-value claims) ≈ **£60m–£300m a year** in direct dispute cost. Management time is excluded. It is an upper-bound-ish range with roughly 5× uncertainty, and the share caused by *administrative error* rather than deliberate commercial tactics is **unknown**. The portion a small operator could capture is a small fraction of that.
3. **Software opportunity:** The *mechanical* layer (notice calendars, EW/CE registers, application portals, AI clause review) is served and increasingly commoditised (K4, K5).
4. **Professional/legal judgement:** Valuation, entitlement and whether a notice is valid are QS and legal judgements. They are not reserved legal activities, but liability attaches. This layer is where the value is and where the operator is least qualified (tier B: needs a QS or construction-lawyer partner).
5. **An unsolved layer above existing software?** Possibly one: an *outcome-linked evidence layer* that answers which administration failures, by contract form, party type and value band, actually turn into disputes and losses, and which record-keeping interventions prevent them. Nobody appears to hold that data, because adjudication decisions are private. That is both the moat and the obstacle: the operator cannot get outcome data without many engagements, and cannot prove value without outcome data. HYPOTHESIS.
6. **Structural bottleneck (K16) risk:** Smash-and-grab claims exploit *missed* notices, which are errors the payer made. So for the **paying party** (typically main contractors paying subcontractors, or employers), notice discipline is an error problem that can be fixed. For the **payee**, most losses come from power asymmetry, which is not fixable by administration. The wedge should therefore target payers' notice discipline, which also avoids being extractive (K14).

### 2C. INVENTORY & WORKING CAPITAL

| # | Source | Date | Exact claim supported | Quality | Limitations | V/R |
|---|---|---|---|---|---|---|
| I1 | PwC UK Working Capital Study 25/26 | 2025/26 | UK NWC days +48.0% since 2015; mid-size firms NWC +19.8%; **mid-size DIO +24.2% (15.0 days) vs +5.5% (2.9 days) for large** | Consultancy (sells working-capital services); large filed-accounts sample | Sampling frame for "mid-size" unclear; associational; seller of the solution | REPORTED |
| I2 | Drakeley & Perera, "Inventory optimisation adoption amongst SMEs", *Advances in Manufacturing Technology XXXV* (IOS Press ATDE), Sheffield Hallam | 2022 | "Most SMEs use some form of IT platforms to manage inventory, [but] inventory optimisation does not appear to be a prime goal"; barriers are lack of in-house expertise and investment | Academic conference paper | Small, qualitative; conference proceedings | REPORTED |
| I3 | Search summary: "£1.6bn annual cost of overstocking to UK SMEs; 32% reduction with AI forecasting" | ? | — | Untraceable; looks vendor-originated | **Rejected** (S1/S2) | — |
| I4 | Netstock *Inventory Management Benchmark Report 2024* | 2024 | Vendor benchmark | Vendor | S1 | REPORTED (competitor evidence only) |

**Findings.** (a) There is no independent, non-vendor, sampled evidence on UK mid-market inventory performance or on how widely planning tools are adopted. That is a gap, not a finding. (b) I1 is the only quantitative signal. It is directionally supportive: mid-size firms' inventory days have deteriorated much more than large firms'. But it comes from a solution seller. (c) I2 suggests the problem is **not** missing software: SMEs have IT platforms but do not prioritise optimisation. That points to a *behavioural and organisational* residual (expertise, attention, governance), not an algorithmic one. (d) **K6 check.** Incumbents named: ERP MRP modules, Slimstock, Netstock, EazyStock, GMDH Streamline, Inventory Planner, Lokad, RELEX and working-capital consultancies. Segment checked for an unserved wedge: UK distributors with £10–100m turnover that run an ERP but no specialist planning tool. Its size is **unknown**. Nothing found eliminates the arena, and nothing independently establishes it.

**Verdict 2C:** Decision-problem existence is plausible but independently *unestablished* for the mid-market. The accessible value probably lies in getting planning policy adopted and governed, a place where mature tools already compete and generic AI will soon compete too.

### 2D. CUSTOMS / TRADE-COMPLIANCE DECISIONS

| # | Source | Date | Exact claim supported | Quality | Limitations | V/R |
|---|---|---|---|---|---|---|
| T1 | HMRC (Ipsos), *Estimating the customs administrative burden of 2022 declarations* | Research Sep 2023; published c.2025 | Burden of completing GB–EU import/export declarations in 2022 ≈ **£1.8bn**, 38.6m declarations, about **£48 per declaration** | Official | Admin *burden*, largely borne by intermediaries; says nothing about duty *errors* | REPORTED |
| T2 | DBT/HMRC, *Preference utilisation of UK trade in goods, 2024* | 2025 | **87.8%** of UK imports used a preference where one was available; **82.0%** for non-EU partners; **86.7%** of imports entered tariff-free (59.9% MFN zero, 25.5% FTA, 1.2% DCTS) | Official statistics | The register's "90.0% for EU27" may be a sub-figure; value of unused preference **not extracted** | REPORTED |
| T3 | gov.uk, *How to apply for a repayment of import duty and VAT if you've overpaid (C285)* — archived copy | Archived version dated 20 Dec 2021 | Verbatim: time limit "3 years for overpayments; 1 year for rejected imports; 3 months for invalidation of a customs entry"; "You must include commercial evidence with your claim, such as: the invoice; packing list; transport documents"; "If valid, your claim will be processed by the National Duty Repayment Centre within 30 days of receipt" | Official guidance (third-party archive) | 2021 version; the Aug 2025 update adds an EORI requirement (REPORTED) | **VERIFIED** (archive copy) |
| T4 | HMRC "Get Customs Data" service (via BWA, Price Bailey, customs-declarations.uk) | Launched 13 Nov 2025 | Free CSV reports (ImportItem, ImportHeader, ImportTax line, ExportItem) covering the last **4 years** in 31-day chunks, typically within 72h; replaces the paid MSS | Secondary summaries of an official service | Not seen first-hand | REPORTED |
| T5 | HMRC *Measuring tax gaps* 2025 edition | Jun 2025 | Tax gap 2023-24 5.3% (£46.8bn); "failure to take reasonable care" 31% and "error" 15% of the gap. **Customs duty is not headlined separately** | Official | Customs error rate unknown | REPORTED |
| T6 | Vendor sources (TariffTel "2 in 5 codes wrong"; iCustoms; mycustomsinfo) | various | Misclassification is common; post-clearance checks can reach back 4 years; penalties 30–100% of lost revenue | Vendor | S1; direction of error (over- vs under-payment) unknown | REPORTED (vendor) |
| T7 | Vendor AI classification claims (MIC 97%, ONESOURCE 95%, Freehand "autonomous classification tied to duty recovery") | 2026 | AI classification and recovery products are on sale | Vendor | Accuracy claims unverified | REPORTED (competitor evidence only) |
| T8 | IEEPA refunds (NRF, GHY, Holland & Knight, Conference Board excerpts) | Feb–Sep 2026 | *Learning Resources v. United States* (Feb 2026) held IEEPA tariffs unlawful. CBP's CAPE portal had accepted ~$132.5bn in potential refunds, with ~$106.6bn certified to Treasury by about September 2026 | Legal/trade-association secondary | US-only; one-off; figures vary by date | REPORTED |

**Findings**

- **Recurring errors that actually occur:** Only vendors report specific error types and rates (classification, missed preference, valuation, unused reliefs). HMRC publishes no customs-specific error rate that I could find. **Not established.**
- **Is the magnitude material?** It is bounded downward. 86.7% of import value is already duty-free, and 87.8% of preference-eligible imports already claim (T2). The overpaid-duty pool is a slice of about 13% of import value that is dutiable, minus correct payments. ESTIMATE: UK customs duty receipts are of the order of £5–6bn a year (my background knowledge, `ASSUMPTION`, not verified). If 1–3% of that were recoverable overpayment, the pool would be about £50–180m a year nationally, spread across ~251k importers (S32, REPORTED). That is **material for some importers, trivial for most**.
- **What data can businesses get?** Good: the free four-year CDS export (T4), and C285 repayment is a defined route (T3, verified). This is the arena's strongest point, but it lowers the barrier for **everyone**, including AI competitors.
- **Regulatory/professional barriers:** No licence is needed to advise or to prepare C285 claims for the importer. Agent authorisation is needed to act as a declarant. The main risk is surfacing *underpayments*, which bring disclosure duties, interest and penalties. Some importers may prefer not to look (a K10-type incentive tension).
- **Does AI commoditise or strengthen?** It commoditises the core analytic (classification, look-back matching); the evidence is visible now (T7). What stays scarce is audit-defensible origin evidence and supplier documentation. That is document and relationship work, not intelligence.
- **IEEPA relevance (critical):** Low. The refunds are US-only, a one-off event, and pure redistribution (P = 1). Brokers, law firms and CBP's own CAPE process already handle them, and the deadlines are driven by liquidation. They show that tariff volatility creates recovery windows. They do **not** show a recurring UK problem that a UK tier-A operator could enter now, and chasing them would be sunk into a closing window.

**Verdict 2D:** The mechanism is verified (C285) and data access is strongly reported. The *magnitude of recurring error* is unestablished and bounded down by official preference and zero-tariff shares. The value is mostly redistribution, and the analytic is commoditising.

### 2E. Other arenas (brief; no deep sprint because the blind scores and new evidence both point down)

| Arena | New evidence | Effect |
|---|---|---|
| 1 Accountancy | 73% turning away work: Advancetrack (outsourcer, vendor) again; ICAEW mid-tier research: 67% say recruiting qualified staff is a top issue (REPORTED, professional body) | Problem plausibly real (staffing), but the fix is labour supply. Wedge commoditised. No change |
| 2 B2B order entry | No independent source found; vendor-only | S1 soft kill stands for magnitude |
| 5 HRB Gateway 2 | Approvals 84% (12 weeks to 31 Aug 2026); Innovation Unit approvals 39% → 91% and median 43 → 22 weeks (REPORTED, trade press citing BSR) | Problem shrinking quickly: K11 (vanishing problem) risk rising |
| 7 MRO | Search results themselves note that the widely quoted 50–60% figure "has no locatable primary study behind it" (vendor site, REPORTED) | S1 soft kill stands |
| 8 Planning validation | About 50% invalid, from a Local Digital (government-funded) discovery project that exists to reduce invalid applications (REPORTED) | Problem likely real; state-funded competitor; low ceiling |

---

## PART 3 — ANTI-TECHNOLOGY TEST

"If Claude Code, AI agents and software disappeared tomorrow, would this still be an economically important problem?"

| Arena | Answer | Reasoning | Penalty |
|---|---|---|---|
| 9 SME manufacturing throughput | **YES** | Physical output lost at bottlenecks predates software (Bloom RCT: management practices, not IT) | None |
| 3 Construction contract admin | **YES** | Notices, valuations and disputes are statutory and contractual (HGCRA 1996), and adjudications are real deadweight cost | None |
| 6 Inventory & working capital | **YES** | Wrong stock ties up cash and loses sales in any era | None |
| 4 Customs / trade compliance | **YES, but smaller than it looks** | Duty errors and admin burden exist without software, but much of the near-term value is refunds (redistribution) | Mild: P already scored 2 |
| 7 MRO spares | YES | Obsolete and critical spares are physical | None, but magnitude unverified |
| 5 HRB Gateway 2 | YES (shrinking) | Regulatory approval quality | K11 risk |
| 8 Planning validation | YES (small per event) | Paper applications were invalidated too | Low value |
| 1 Accountancy capacity | YES (labour supply) | But the lever is staffing, not workflow | Arena mis-specified for software |
| 2 B2B order entry | **Weak / partly NO** | "Keying into ERP" presupposes the ERP; without software it is ordinary clerical order-taking, which is not a distinctive economic problem | **Heavy penalty** |

## PART 4 — AI IMPROVEMENT TEST (10× more capable, 10× cheaper)

| Arena | Verdict | Explanation |
|---|---|---|
| 9 SME mfg | **B leaning A** | Better AI makes diagnosis analytics nearly free. That *commoditises generic diagnosis* (an SME owner can ask a model), but it raises the relative value of what AI cannot do from a chat window: getting onto the shop floor, measuring the real constraint, running the intervention, and holding a causally measured outcome database. Valuable only if the operator owns that evidence |
| 3 Construction | **Wedge C, ceiling B** | Notice calendars, clause review and variation logging become free. Judgement on entitlement and valuation, plus any dispute-outcome dataset, stays scarce but needs professional partners |
| 6 Inventory | **B** | Forecasting algorithms are already commodities. Value sits in adoption and governance of policies and in cross-firm outcome evidence. AI could also let buyers self-serve that |
| 4 Customs | **C** | Classification and look-back matching are exactly what frontier models do well, and vendors already sell them. The residual is origin documentation and audit defence |
| 7 MRO | B | Master-data cleansing is commoditised; criticality judgement and failure data remain |
| 5 HRB | B | Document completeness checks commoditised; engineering judgement is not |
| 1, 2, 8 | **C** | Pure information-processing tasks |

## PART 5 — OPERATOR-COMPOUNDING TEST

"If we solve this 50 times, what will the operator know on deployment 50 that they could not know on deployment 1?"

| Arena | Concrete knowledge at deployment 50 | Strength |
|---|---|---|
| 9 SME mfg | (1) Empirical distribution of *where* the binding constraint sits, by process type (changeover vs unplanned stops vs scheduling vs quality vs material starvation). (2) Measured effect-size distribution per intervention class (e.g. SMED on moulding changeovers: median gain, variance, failure rate). (3) Base rate of "capacity-constrained vs demand-constrained" SMEs, the key economic filter. (4) A minimum-data diagnostic protocol validated against outcomes (which 2-week signals predict the true constraint). (5) Failure modes: interventions that decay (cf. the ~40% practice decay in M5). (6) A benchmark dataset of bottleneck output per shift. | **Strong**, *if* measurement discipline holds |
| 3 Construction | (1) Rule base of notice/timing failure patterns per contract form (JCT DB-Sub, NEC4 ECS…). (2) Rate at which a missed or defective notice converts into a smash-and-grab claim, and the typical amounts. (3) Which record-keeping interventions reduce variation disputes. (4) A labelled set of valid and invalid notices for evaluation. | Moderate–strong, but outcome observation is slow (disputes lag by months) |
| 6 Inventory | (1) Distribution of excess and obsolete % by demand pattern and sector. (2) Which policy changes release cash without service loss, with measured effect sizes. (3) Override behaviour: how often planners ignore recommendations, and why. (4) Adoption decay curves. | Moderate–strong |
| 4 Customs | (1) Error-type frequencies by sector and origin. (2) HMRC acceptance/rejection patterns on C285 claims. (3) Preference-documentation failure modes. | Moderate. Much becomes public or vendor knowledge quickly, and AI replicates it |
| 7 MRO | Parts-catalogue normalisation library; criticality versus stockout-downtime links | Moderate |
| 1, 2, 5, 8 | Mostly mapping/template libraries; weak outcome learning (2, 8); low N (5) | Weak |

## PART 6 — REALITY TEST: smallest credible experiment (none is to be built in Phase Zero)

### 6.9 SME manufacturing throughput
- **Organisation:** one UK SME (20–150 staff) in repeat discrete production (e.g. injection moulding or contract packing) that says it is **capacity-constrained**, with a visible order backlog or turned-away orders.
- **Process:** the single suspected bottleneck work centre (one press or one line).
- **Baseline:** good units per scheduled hour at that work centre, logged per shift for 4–6 weeks. Stop reasons are logged by the operator on a tally sheet or with a clamp-on cycle counter (~£200–£500).
- **Intervention:** one minimum intervention chosen from the diagnosis, e.g. a changeover-time reduction (SMED) on that press, or re-sequencing the schedule to cut changeovers. No capex beyond about £1k.
- **Comparison:** interrupted time series on the bottleneck, with a non-treated comparable work centre as a control series (difference-in-differences). Output is adjusted for product mix.
- **Economic outcome:** extra good units per week × contribution margin per unit. It counts **only** if the extra units were sold or cleared backlog, checked against the order book.
- **Data required:** shift output counts, stop logs, product mix, order backlog, unit contribution margin.
- **Access:** 1–2 days on site per week during baseline and intervention, plus the production manager's time (about 2 h/week).
- **Duration:** 12–16 weeks.
- **Cost (ESTIMATE):** £3–8k direct (travel, counters, the operator's own time excluded).
- **Expertise:** industrial engineering / lean (SMED, TOC), basic statistics.
- **Major risk:** the firm is demand-constrained, so throughput gains have no economic value, or the product-mix noise swamps the effect.
- **Success criterion:** ≥10% increase in good units per scheduled hour at the bottleneck, sustained for 6 weeks after the intervention, with the DiD estimate's 90% CI excluding zero. The extra units must convert into ≥£X per month of contribution, where X is pre-registered from the baseline.

### 6.3 Construction contract administration
- **Organisation:** one UK main contractor or large subcontractor that *pays* sub-subcontractors under JCT subcontracts.
- **Process:** issuing payment notices and pay-less notices on live subcontract packages.
- **Baseline:** look-back over the last 12–24 months: the % of payment cycles where a valid payment notice or pay-less notice was issued on time and with the required content, plus the number and value of payment adjudications and threatened claims.
- **Intervention:** a notice-discipline protocol (a checklist plus a calendar that starts 5 days before each due date, with a content template) run on half the live packages.
- **Comparison:** stepped rollout. Treated vs untreated packages, and each package against its own history.
- **Economic outcome:** avoided exposure = sum of the gaps between applied amounts and valued amounts in cycles where a *missed* notice would have made the applied sum payable (ESTIMATE of exposure), plus the number of claims avoided. The primary outcome (notice compliance) is measurable in weeks. The dispute outcome is **not** measurable in 12 weeks.
- **Data required:** subcontracts, applications, notices and dates, valuations.
- **Access:** the commercial manager or QS team, with confidentiality.
- **Duration:** look-back 3–4 weeks; prospective phase 12 weeks.
- **Cost:** £2–5k plus a QS or construction-law adviser for about 2 days (£2–4k).
- **Expertise:** construction QS/contract-administration expertise (tier B partner).
- **Major risk:** the measurable outcome (compliance) is a *process* metric. The economic outcome is counterfactual exposure, not observed saving, so it fails rule 10's causation standard unless disputes are frequent at that firm.
- **Success criterion:** notice compliance rises from baseline to ≥98% on treated packages, and the value of "exposed" cycles falls by ≥80% compared with untreated packages. Economic value is labelled ESTIMATE, not measured.

### 6.6 Inventory & working capital
- **Organisation:** one UK wholesale distributor (£10–50m turnover) that has an ERP but no specialist planning tool.
- **Process:** replenishment of one product family (about 500–2,000 SKUs) at one branch or warehouse.
- **Baseline:** 12 months of sales, stock, purchase orders and lead times from ERP exports. Baseline stock value, fill rate and lines lost to stock-out.
- **Intervention:** recalculate reorder points and order quantities with a segmented (ABC/XYZ) policy on a random half of the SKUs; the other half is left unchanged.
- **Comparison:** randomised SKU-level split within the family (A/B), stratified by velocity.
- **Economic outcome:** change in average stock value (cash released × cost of capital + carrying cost) at equal or better fill rate, and lost sales avoided.
- **Data required:** routine ERP exports (tier A).
- **Access:** the purchasing manager must actually place orders to the new parameters. **This compliance is the key dependency.**
- **Duration:** 12–20 weeks, i.e. at least two replenishment cycles.
- **Cost:** £2–6k.
- **Expertise:** inventory theory, supply planning.
- **Major risk:** buyers override the parameters; lead-time variability or seasonality confounds a short window; spillover between SKUs (shared suppliers or minimum order quantities).
- **Success criterion:** treated SKUs show ≥10% lower average stock value than control SKUs, with fill rate not lower by more than 0.5 pp, over ≥12 weeks, and the difference is significant at 90%.

### 6.4 Customs / trade compliance
- **Organisation:** one UK importer with ≥£2m a year of *dutiable* imports (i.e. not mostly zero-tariff goods).
- **Process:** tariff classification and preference claims on import declarations.
- **Baseline:** 36 months of Get Customs Data exports. The % of lines with a disputed classification or an unclaimed eligible preference, and the duty value involved.
- **Intervention:** corrected classification and preference claims on *future* declarations (the productive part), plus C285 claims for the past 3 years (the redistributive part, reported separately).
- **Comparison:** cash look-back (repayment received vs zero counterfactual). For future declarations, duty per unit before vs after at constant product and origin mix.
- **Economic outcome:** repayments received (redistribution; labelled so), and duty avoided going forward net of any underpayment disclosed.
- **Data required:** CDS exports, invoices, supplier origin statements.
- **Access:** the importer's customs/finance lead; their broker's cooperation.
- **Duration:** analysis 2–4 weeks; C285 outcome within about 30 days of a valid claim (T3); forward effect 8–12 weeks.
- **Cost:** £1–4k.
- **Expertise:** tariff classification, rules of origin.
- **Major risk:** little net overpayment is found, or underpayments are found (liability). The outcome is mostly redistribution, and the analytic is commoditised.
- **Success criterion:** net verified overpayment ≥1% of dutiable duty paid over 3 years, repaid in cash; and forward duty per unit falls without any HMRC challenge in the window.

### 6.7 MRO spares (secondary)
One asset-intensive site. Process: stores for one asset class. Baseline: stock value, dead stock (>24 months without movement), critical stock-outs. Intervention: criticality-based min/max reset and a disposal list. Comparison: treated vs untreated asset classes. Outcome: stock value released, with critical stock-outs not higher. Duration 16–26 weeks (disposal decisions are slow). **Fails the 12-week measurability standard; kept only for completeness.**

---

## PART 7 — POST-BLIND COMPARISON

Opened only after Part 1 was locked (19:00:43Z) and Parts 2–6 were written (19:13:04Z). Files opened are listed in the audit log (P1–P13).

**Arena mapping to prior IDs:** 1 Accountancy = N21; 2 Order entry = C30; 3 Construction = C27b; 4 Customs = C25b (the broader arena; the narrower recovery version C25 was parked by the prior analyst); 5 HRB = N05; 6 Inventory = N19; 7 MRO = N18; 8 Planning = C12; 9 SME manufacturing = N08.

**Formula check:** `scoring/v2/score_v2.py` computes WEDGE and CEILING exactly as I did (the CEIL block is the mean of the ten sub-factors, weighted 50). Differences are therefore differences of **judgement**, not arithmetic.

### 7.1 Side by side

| Arena | Prior WEDGE / CEILING / √ (rank) | Blind WEDGE / CEILING / √ (rank) | Prior gates | Blind gates | Prior conf | Blind conf |
|---|---|---|---|---|---|---|
| Construction (C27b) | 69.8 / 92.0 / **80.1 (1)** | 59.0 / 66.6 / 62.7 (4) | pass | **park (WEDGE)** | M | L–M |
| Inventory (N19) | 68.4 / 87.0 / 77.1 (2) | 66.4 / 76.0 / **71.0 (1)** | pass | pass | M | L |
| SME mfg (N08) | 62.6 / 93.0 / 76.3 (3) | 54.2 / 85.6 / 68.1 (3) | pass | **park (WEDGE)** | M | L–M |
| Customs (C25b) | 63.6 / 90.0 / 75.7 (4) | 73.6 / 65.4 / 69.4 (2) | pass | pass (CEILING marginal after revisions: 64.4) | L | L–M |
| HRB Gateway 2 (N05) | 69.8 / 79.4 / 74.4 (5) | 54.6 / 57.0 / 55.8 (7) | pass | **park** | M | L–M |
| Planning (C12) | 67.2 / 70.4 / 68.8 (6) | 65.6 / 45.4 / 54.6 (8=) | pass | **park (CEILING)** | M | L |
| MRO (N18) | 62.8 / 75.0 / 68.6 (7) | 57.6 / 64.4 / 60.9 (5) | pass | **park (WEDGE)** | L | L |
| Accountancy (N21) | 65.4 / 70.0 / 67.7 (8) | 57.4 / 52.0 / 54.6 (8=) | pass | **park** | L | L |
| Order entry (C30) | 62.6 / 61.0 / 61.8 (9) | 68.8 / 52.0 / 59.8 (6) | pass | **park (CEILING)** | M | L |

Mean difference per code (blind minus prior, over the 9 arenas): **A (AI usefulness) −2.2**, T −1.3, COMP −1.1, REP/MOAT/LEARN −1.0, MEAS −0.9, E −0.9, J −0.9, V −0.8, TTP −0.6. The other codes differ by ≤ 0.4.

### 7.2 Agreements
- The **same four arenas** make up the top four in both analyses (construction, inventory, SME manufacturing, customs), and both put Planning, Accountancy and Order entry at the bottom.
- Neither analysis selects anything. Both find no arena passes the evidence-confidence gate.
- Both flag N08's shop-floor access problem, N19's crowded tool market and missing independent mid-market evidence, C25b's US-centric and one-off scale signal, and N05's improving regulator.
- No arena's combined **rank** moves by more than 3 places. So by the prior analyst's own E1 rule ("> 3 places ⇒ unstable") none is formally unstable. Construction (1 → 4) and Order entry (9 → 6) sit exactly at the boundary.

### 7.3 Disagreements (explained, not averaged)
1. **Absolute CEILING levels, and therefore gate outcomes: material.** The prior analysis passes **9 of 9** arenas through both gates. The blind analysis passes **2 of 9**. Gates are absolute thresholds, so a systematic 10–25-point CEILING inflation turns "parked" into "survivor". The rank-based E1 rule cannot detect this. **The prior E1 test is insufficient; gate status must be compared too.**
2. **Sub-factor A (usefulness as AI improves).** The prior analysis scored A = 4–5 for almost everything, including Accountancy (5), Order entry (4) and Planning validation (4). Those are pure information-processing tasks that frontier AI commoditises directly. The rubric defines 5 as "better models make the capability *more* valuable". The prior scoring reads as "AI helps do this", which is a different question. This single code explains about 2 points of CEILING per arena on its own, and it is **the most likely location of a pro-AI bias**. That bias is exactly what CLAUDE.md rule 11 warns against.
3. **Construction MEAS (prior 4, blind 2).** The prior analysis's own red team says "disputes are rare per contract, so proving prevention needs many contracts or a long time… a look-back design… shows correlation, not prevention". That is inconsistent with MEAS = 4. The blind MEAS = 2 matches the prior red-team text. Correcting only this one code takes C27b's WEDGE from 69.8 to 64.2, still above 60. But the blind view also scores URG, SOLV and TTP lower (a payer's notice discipline is not a budget-holder emergency, and part of the problem is power), which puts it below the gate.
4. **Construction CEILING (prior 92, blind 67).** The prior analysis gives T = 4, REP = 5, COMP = 5, V = 4. The blind view: the capability is specific to contract forms and to UK statute (HGCRA). It transfers to other contract-heavy sectors only loosely, and outcome data compounds slowly because disputes are rare and private (COMP 3). The prior DR-002 itself warned: "Treat the rank as inflated until an independent re-score confirms it." **This re-score does not confirm it.**
5. **Customs (C25b) CEILING (prior 90, blind 65 → 64).** The prior analysis gives T 5, K 5, A 5, J 5 and says "AI makes the rule base more valuable". The evidence found in Part 2 points the other way: multiple vendors already sell AI classification tied to duty recovery (T7), and HMRC's free four-year data export (T4) lowers the barrier for every competitor. The prior analysis also flagged C25b as reframed in-session (halo risk), and the blind score supports that concern. The blind analysis scores C25b's *WEDGE* **higher** (73.6 vs 63.6), because a cash look-back is causally clean and the data is routinely available. This is the one place the blind review is *more* favourable. It rests on a redistribution wedge, which rule 21 discounts.
6. **HRB Gateway 2 (prior MEAS 4, TTP 3; blind 1 and 1).** One project, a regulator with a months-long clock whose own performance is changing fast, and no counterfactual. The blind scores follow from design logic. The prior's own ledger notes "regulator performance improving fast", which also argues against MEAS 4.
7. **Order entry.** This is the only arena whose WEDGE the blind review scores higher (MEAS 5: historic orders give ground truth). Its CEILING is lower. The prior-venture disclosure was respected in both analyses. Neither gives it a bonus.

### 7.4 Unexplained divergence
- The prior analysis rated evidence confidence **M** for C27b, N19, N08, N05, C12 and C30. It also records that every figure behind those ratings is REPORTED from search excerpts. The blind review cannot reconcile "M" with "no primary source read". Excerpt consistency is not verification. **I treat the prior M ratings as unexplained optimism.**
- Prior N19 CEILING 87 vs blind 76: much of the gap is A (5 vs 3) and T (5 vs 4). There is no evidence either way; it is pure judgement.

### 7.5 Possible shared assumptions (the residual independence limitation)
- **Same model family.** The blind reviewer and the prior analyst are the same underlying model family. Shared training priors probably explain why both analyses picked the *same top-four set* and similar kill logic. The blinding guards against anchoring on numbers, not against shared priors about what "sounds like" a good arena.
- **Same evidence base.** Both used the same source registers as leads and the same blocked network. The blind review's Part 2 retrieved little that is new and independent. The exceptions are HMRC's Get Customs Data service, 2026 BSR approval rates, the correct wording of KCL's "63% of respondents", the Bloom RCTs and the IRC report. So agreement on direction is *not* independent corroboration.
- **Task framing.** The brief named the same four arenas for the evidence sprint that both analyses rank top. That is a further channel of non-independence.
- **Shared untested assumption.** Both analyses treat "throughput or inventory gains convert into money" as given. Neither has evidence that a typical UK SME manufacturer is capacity-constrained, or that a typical distributor's excess stock is decision-driven rather than driven by supplier minimum order quantities (MOQs) and lead times.

### 7.6 Strength that disappears under primary evidence
No primary document could be opened, so no arena's strength was *refuted* by primary evidence. Under the best available (REPORTED) evidence, these apparent strengths weakened:
- **C27b:** "42% lack of competence" and "most common claim £125k–£500k" were **not found in any excerpt**. "63%" is respondents' *experience*, not a share of cases. Causal measurability of the economic outcome is weak.
- **C25b:** commoditisation is visible now. Near-term value is redistribution. The dutiable pool is bounded (86.7% of imports duty-free, 87.8% preference use). The IEEPA signal is US-only and one-off.
- **N05:** the problem is shrinking (84% approvals; median times falling).
- **N08:** the Made Smarter headline finding *as briefed to me* could not be verified. If true, it undermines measurability at firm level, and it shows a free state competitor in diagnosis.

---

## FINAL GATE

Legend: PASS / FAIL / UNC (uncertain, not demonstrated) / PART (partial).

| Arena | (1) Problem independently established | (2) Access plausible | (3) Causally measurable | (4) Affordable and reversible | (5) Wedge not eliminated by competitors | (6) Transferable capability | (7) More leveraged as AI improves | (8) Path to larger consequence | Result |
|---|---|---|---|---|---|---|---|---|---|
| 9 SME mfg throughput | **FAIL** (REPORTED only; RCT abroad) | PASS | PART (process yes, firm economics no) | PASS | UNC (Made Smarter free diagnosis; OEE tools) | PASS | PASS (B→A) | PASS | **Not selectable** |
| 6 Inventory & WC | **FAIL** (consultancy + one conference paper, REPORTED) | PASS | PASS (SKU randomisation), subject to buyer compliance | PASS | UNC (mature tools; unserved segment size unknown) | PASS | PART (B) | PASS | **Not selectable** |
| 3 Construction contract admin | **FAIL** (KCL not opened; strongly REPORTED) | PASS | **FAIL** for the economic outcome in window (process metric only) | PASS | UNC (mechanical layer served) | PASS | PART (wedge C, ceiling B) | PASS | **Not selectable** |
| 4 Customs / trade compliance | **FAIL** (mechanism verified via C285; error magnitude not) | PASS | PASS (cash) | PASS | **FAIL** (AI recovery tools on sale) | PART | **FAIL** (C) | **FAIL** (mostly redistribution) | **Not selectable** |
| 7 MRO spares | FAIL (vendor-only) | PART | FAIL (in window) | PASS | UNC | PASS | PART | PART | Not selectable |
| 5 HRB Gateway 2 | FAIL | PART | FAIL | PART | FAIL (specialist consultancies) | FAIL (low N) | PART | FAIL (shrinking, K11) | Not selectable |
| 8 Planning validation | FAIL | PASS | PASS | PASS | FAIL (state-funded project) | FAIL | FAIL | FAIL | Not selectable |
| 1 Accountancy capacity | FAIL (vendor) | PASS | PART | PASS | FAIL | FAIL | FAIL | FAIL | Not selectable |
| 2 B2B order entry | FAIL (vendor) | PASS | PASS | PASS | FAIL | FAIL | FAIL | FAIL | Not selectable |

**Can condition (1) honestly be marked PASS when the primary document could not be opened?** **No.**
Under CLAUDE.md rule 4 and evidence/README rule 2, a claim seen only through a search excerpt is `REPORTED`, never `FACT`. "Independently established" requires at least one independent source that was actually read. Several consistent secondary summaries (e.g. >8 law firms quoting 2,264 adjudications) raise the *probability* that the claim is correct. They do not change its evidence status, and this review found an excerpt distorting a finding ("63% of adjudications"). The honest ceiling for condition (1) is "REPORTED, highly consistent" for construction (count of referrals) and "REPORTED, strong causal evidence abroad" for SME manufacturing. Neither is PASS.

**Sensitivity:** even if condition (1) were relaxed to "REPORTED and consistent", no arena clears all eight. SME manufacturing (3 PART, 5 UNC), Inventory (5 UNC, 7 PART) and Construction (3 FAIL) each have at least one condition not demonstrated.

**Outcome: SELECT NOTHING.**

---

## REVIEWER CONCLUSION

1. **Arenas independently scored:** **9** (all nine, blind, Part 1, sha256 `a5864d07…d5abb8`).
2. **Arenas surviving primary-source verification:** **0**. Definition: an arena counts only if its core problem claim was confirmed by a primary or authoritative full-text source that I actually opened and read. Only two documents were opened: IRC Report 044 (qualitative, about adoption barriers) and an archived gov.uk C285 page (which verifies a repayment *mechanism*, not a problem magnitude). Neither establishes any arena's problem. Secondary count, for information only: **2** arenas survive at REPORTED level without a clear FAIL on conditions 2–8, provisionally: SME manufacturing throughput and Inventory & working capital. Construction drops out on condition (3).
3. **Do the blind findings materially disagree with the previous analysis?** **Yes.** They agree on the top-four *set* and on selecting nothing. They disagree materially on absolute levels: 2 of 9 arenas pass both gates blind vs 9 of 9 previously. The previous #1 (construction contract administration, 80.1) falls to #4 (62.7) and fails the WEDGE gate. The main source is sub-factor A, where the prior scoring reads as a pro-AI bias (mean −2.2), plus construction MEAS. Shared model family and shared evidence base limit how independent even the agreements are.
4. **Surviving arenas:** none verified. Provisional (REPORTED-level): SME manufacturing throughput; Inventory & working-capital decisions.
5. **Strongest remaining arena:** **none** (no arena clearly survives).
6. **Smallest real-world experiment (PROVISIONAL, for the strongest provisional arena: Inventory & working capital, the only provisional arena passing both blind gates):** one UK wholesale distributor (£10–50m turnover) with an ERP and no specialist planning tool. One product family of 500–2,000 SKUs at one warehouse. Baseline: 12 months of routine ERP exports (sales, stock, POs, lead times). Intervention: segmented reorder-point and order-quantity reset on a **randomly assigned half** of the SKUs, stratified by velocity; the other half is the control. The purchasing manager orders to the new parameters. Duration 12–20 weeks. Cost about £2–6k. Success: treated SKUs hold **≥10% lower average stock value than controls with fill rate no worse than −0.5 pp over ≥12 weeks, significant at 90%**. Economic outcome: cash released × cost of capital plus carrying cost, and lost sales avoided. Not to be run in Phase Zero.
7. **The single fact most likely to prove the selection wrong:** that the distributor's excess stock is driven by supplier MOQs, lead-time variability and deliberate strategic buffers, **not** by replenishment-decision quality. Equivalently: firms that already run their ERP's replenishment logic show no material reducible excess, so a randomised parameter reset releases <10% of stock at equal service.
8. **GO / NO GO on ending Phase Zero: NO GO.** Condition (1) cannot honestly pass for any arena, because no primary document could be read in this environment. Every magnitude remains REPORTED, and the prior analysis's gate passes appear inflated by the CEILING sub-factors, above all AI usefulness (A).

   **Single next action:** the project owner should manually download these primary documents into `evidence/primary/`, so that condition (1) can be tested against read text rather than excerpts. The network cannot reach them.
   - KCL/Adjudication Society *2024 Construction Adjudication in the UK*
   - *Made Smarter Adoption: impact and process evaluation* (Jul 2026) with its technical annex
   - DBT/HMRC *Preference utilisation of UK trade in goods 2024* tables
   - ONS *Management practices in the UK 2016–2023*
   - PwC *Working Capital Study 25/26*
   - Drakeley & Perera (2022)

---

## Appendix — calculation script (as run for Part 1)

See `scratchpad/ir/score.py` (Part 1 inputs, formulas, and 5,000-draw Dirichlet(1) robustness). Post-lock revisions: `scratchpad/ir/rev.py`. Prior-vs-blind comparison: `scratchpad/ir/cmp.py`. The formulas are identical to the prior `scoring/v2/score_v2.py`.

```python
# score.py — Part 1 blind scores (as run; seed 1)
import math, json, random
W={'WSEV':14,'MEAS':14,'URG':14,'ACC_A':14,'SOLV':12,'TTP':10,'SAT':10,'RISK':7,'IMPL':5}
C={'COMP':12,'REP':10,'MOAT':10,'ACC_B':10,'LEARN':8}
SUB=list('TKSPIEZVAJ')
A={
'ACCOUNTANCY CAPACITY':      ([3,3,3,3,4,3,1,3,2],[3,2,2,4,3,2,4,2,1,3],[2,4,1,4,2]),
'B2B ORDER ENTRY':           ([3,5,3,3,5,4,1,4,2],[3,2,2,3,3,2,5,2,1,3],[2,4,1,4,2]),
'CONSTRUCTION CONTRACT ADMIN':([4,2,3,3,3,2,3,3,4],[2,4,4,3,3,4,4,2,3,4],[3,3,3,4,4]),
'CUSTOMS / TRADE COMPLIANCE':([3,5,4,4,4,3,2,3,5],[3,3,4,2,3,4,4,3,2,3],[4,4,2,4,3]),
'HRB GATEWAY 2':             ([5,1,4,2,3,1,3,2,3],[1,4,5,4,3,3,3,2,3,3],[3,1,3,3,3]),
'INVENTORY & WORKING CAPITAL':([4,3,3,4,4,2,2,4,4],[4,4,3,4,4,4,4,4,3,4],[4,5,2,4,4]),
'MRO SPARES':                ([4,2,2,3,4,2,3,3,3],[3,4,3,3,3,3,4,3,3,3],[4,3,3,3,3]),
'PLANNING VALIDATION':       ([2,4,2,5,4,3,2,4,4],[1,2,4,3,2,2,4,1,1,3],[3,2,1,3,2]),
'SME MFG THROUGHPUT':        ([4,3,2,2,3,2,3,3,2],[5,5,4,5,5,5,3,4,3,5],[4,5,3,4,5]),
}
def score(w,sub,c,Wt=W,Ct=C):
    wedge=sum(Wt[k]*v for k,v in zip(Wt,w))/5
    ceil_mean=sum(sub)/10
    ceil=50*ceil_mean/5+sum(Ct[k]*v for k,v in zip(Ct,c))/5
    return wedge,ceil_mean,ceil,math.sqrt(wedge*ceil)
rows=[]
for n,(w,s,c) in A.items():
    we,cm,ce,g=score(w,s,c)
    rows.append((n,we,cm,ce,g))
    print(f"{n:30s} WEDGE={we:5.1f} CEILmean={cm:.1f} CEILING={ce:5.1f} GEO={g:5.1f} gates={'PASS' if we>=60 and ce>=60 else 'PARK'}")
# robustness: dirichlet(1) within each axis, 5000 draws, share in top5 by geo and share passing gates
random.seed(1)
def dirich(keys):
    x=[random.expovariate(1) for _ in keys]; s=sum(x); return {k:100*v/s for k,v in zip(keys,x)}
cnt={n:0 for n in A}; gate={n:0 for n in A}; top1={n:0 for n in A}
N=5000
for _ in range(N):
    Wt=dirich(list(W)); Ct0=dirich(['CEIL']+list(C)); cw=Ct0.pop('CEIL')
    res=[]
    for n,(w,s,c) in A.items():
        wedge=sum(Wt[k]*v for k,v in zip(Wt,w))/5
        ceil=cw*(sum(s)/10)/5+sum(Ct0[k]*v for k,v in zip(Ct0,c))/5
        res.append((math.sqrt(wedge*ceil),n,wedge>=60 and ceil>=60))
    res.sort(reverse=True)
    for i,(g,n,p) in enumerate(res):
        if i<5: cnt[n]+=1
        if i==0: top1[n]+=1
        if p: gate[n]+=1
print("\nRobustness (Dirichlet(1) within axes, N=5000): top5 share / top1 share / both-gates-pass share")
for n in A: print(f"{n:30s} {cnt[n]/N:5.0%} {top1[n]/N:5.0%} {gate[n]/N:5.0%}")
```

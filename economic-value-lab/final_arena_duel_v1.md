# Final Arena Duel v1 — Phase Zero step 1D

Date: 2026-09-30. Arenas: **A. SME manufacturing throughput / constraint discovery** and
**B. Inventory & working-capital decision quality**.

**Independence disclosure.** I did not open any previous ranking, score or decision file for
this step. I am the same analyst (same session) that produced the earlier Phase Zero rankings, so
those rankings are in my working memory. That cannot be undone. To compensate, every judgement
below cites a primary document and page, or is explicitly labelled `ESTIMATE`, `HYPOTHESIS` or
`UNVERIFIED` (from general knowledge, not checked in this session).

**Evidence base.** Four primary documents, P01–P04 (see `evidence/primary/README.md`). No other
document was read for this step. Documents cited in earlier steps but not supplied (KCL
adjudication report, preference-utilisation tables, Drakeley & Perera 2022) are not used.

---

## 1. Primary-evidence register

| # | Source | Date | Exact claim supported | Quality | Limitations |
|---|---|---|---|---|---|
| E1 | P01 p.8, p.85, p.60 | Jun 2025 | 78% of participants report adopting some IDT after the programme | Self-report survey, n=97+182 beneficiaries, response rate 15–18% | Not causal; survey representativeness "uncertain" (p.72) |
| E2 | P01 p.74, 76, 85–86; P02 A.7.1–A.7.2, Table A.9 | Jun 2025 | Against firms that engaged but did not progress (Model 2) and early-vs-late joiners (Model 3), there are no statistically significant effects on turnover, employment or turnover per worker. Coefficients: turnover 0.01 (p=0.62) and −0.03 (p=0.30); employment 0.00 and −0.01 | Staggered DiD (Callaway–Sant'Anna), 2,402 firms linked to ONS BSD; the strongest design in the evaluation | The formal parallel-trends test was rejected in most specifications, including Models 2–3 (P02 p.16, Table A.9) |
| E3 | P02 A.7.4–A.7.5; P01 p.78 | Jun 2025 | Year 3 only: GVA/GVA per worker +51% / +34% / +42% (Models 1/2/3); intermediate consumption −33% / −54% / −41%. Average post-period effect on GVA per worker is not significant in Models 2–3 (0.05, p=0.39; 0.08, p=0.20) | ABS-linked subsample of 1,151 firms | **Fewer than 10% of firms reach year 3** (P01 p.79). Evaluators call the magnitudes "implausibly large" and say they imply >£1bn GVA from a £19.8m programme, "not considered credible" (P01 p.78) |
| E4 | P01 p.71 | Jun 2025 | "Many firms were unable to report specific gains in performance – due to the difficulty of isolating the impact of IDTs from other factors or a lack of focus on measuring and tracking financial outcomes" | Qualitative, 25 firm case studies | Case selection not random |
| E5 | P01 p.56–57 | Jun 2025 | Successful implementations "were typically underpinned by a clear vision and clearly identified problems … [and] set measurable performance indicators to track progress" | Qualitative | Selected on success; correlational |
| E6 | P01 p.42–44, 15 | Jun 2025 | The public diagnostic assesses "need for Industrial Digital Technology" and a Digital Readiness Level (PAS 1040). Some roadmaps were "too broad ('a 10 year plan')", which "made it difficult for some businesses to prioritise tasks, potentially leading to inaction" | Programme documentation + qualitative | Describes one programme's framing only |
| E7 | P01 p.48, 59 | Jun 2025 | Firms plateau at DRL5; projects treated as "stand-alone" and not aligned with "wider business improvement projects" | Survey + case studies | Short follow-up |
| E8 | P01 p.10 | Jun 2025 | Benchmarking against alternative models was not possible "owing to the absence of evaluation evidence (including on comparable programmes internationally)" | Evaluator's statement | Refers to comparable programmes, not all operational interventions |
| E9 | P01 p.31 | Jun 2025 | 2,026 enrolled firms = 4% of manufacturing SMEs in the five regions | ONS/NOMIS counts | Implies roughly 50,000 manufacturing SMEs in those regions (`ESTIMATE`: 2,026 / 0.04) |
| E10 | P01 p.78 fn 20, p.73 | Jun 2025 | Supported firms average GVA per worker £74,600, 33 workers; survey participants average turnover ≈ £8.7–8.9m | Admin + survey | Averages; skewed |
| E11 | P01 p.50–51 | Jun 2025 | Funding was the most-reported barrier to adoption. Lack of time, leadership priority and knowledge of solutions were "less widely reported" | Survey | Asks about barriers to *technology*, not to operational improvement |
| E12 | P03 §3–5 | May 2024 (corrected Jul 2024) | 2023 mean management score 0.55. Production 0.52 vs services 0.56, with production having "a longer tail". KPI category lowest (0.42); continuous improvement highest (0.80) | ONS official statistics in development; 53,433 sampled, 27% response | Self-reported practices; firms with 10+ employees only |
| E13 | P03 §4 | 2024 | Score rises with size: 0.51 (10–19 employees) to 0.68 (250+); size gap 0.15 after controls | As above | Correlational |
| E14 | P03 §5 | 2024 | Productivity is statistically significantly associated with management score. Main barrier to improving management: "too little time" (36%); 32% report "no barriers"; only 13% hire consultants | As above | ONS itself calls management "a significant driver"; its own evidence is correlational (it cites Bloom et al. for causation) |
| E15 | P03 §6 | 2024 | Below-median firms are 4× more likely to use "little to no analysis" for important decisions | As above | Correlational |
| E16 | P04 p.1, 6–7, 11–12 | 2025 | UK NWC days +48% since 2015, "fuelled by a sharp rise in DIO in 2019-20 and, more recently, a fall in DPO". Mid-size DIO +24.2% (15 days). UK cash-intensive-sector DIO 62.8 days vs EU 90.2. €1.84tn "excess working capital" globally | Consultancy analysis of >17,000 **listed** companies | No method for "excess"; no split of causes; "mid-size" means listed mid-caps, not private mid-market; seller of the remedy |

---

## 2. Hypothesis A — SME manufacturing constraint discovery

**Proposition tested:** "An economically important and accessible problem exists among SME
manufacturers where the binding constraint on production or resource productivity is not being
identified, prioritised or economically verified well enough; an external operator could
potentially diagnose one such constraint, make or recommend a bounded intervention, and causally
measure the resulting economic improvement."

### A1. What evidence proves the underlying problem exists?

| Element of the proposition | Evidence | Status |
|---|---|---|
| Improvement is not **economically verified** well enough | E4: many firms could not report gains, partly from "a lack of focus on measuring and tracking financial outcomes". E12: KPI use is the weakest management dimension (0.42). E15: weaker firms use little or no analysis. E3: even a £19.8m government evaluation with ONS microdata could not produce a credible magnitude | **Established** (FACT, but descriptive) |
| Improvement is not **prioritised** well enough | E6: roadmaps too broad to prioritise; E7: projects not linked to business improvement | **Partly established** (qualitative) |
| The **binding constraint** is not being **identified** | No document measures how often SME managers misidentify their constraint | **Not established** |
| The problem is **economically important** | E9–E10 give scale (~50k manufacturing SMEs in 5 regions; ~£2.5m GVA per average supported firm, `ESTIMATE` 33 × £74,600). No document quantifies the loss from unidentified constraints | **Not established** |
| An external operator can **access** it | E9: 2,026 firms enrolled, 60% above target (P01 p.7); firms valued "impartial advice" and on-site visits (P01 p.43). One firm wanted "ongoing support that they could buy into" (P01 p.44–45, n=1) | **Plausible** |

### A2. Diagnosis / intervention-selection / measurement problem, or just low adoption?

The evidence points **away from "low adoption"**:
- 97% of participants had already adopted at least one IDT before joining (P01 p.49).
- 78% adopted more afterwards (E1).
- Yet the robust models show no measurable firm-level effect (E2).

Adoption is not the scarce thing. The evaluation's own explanations are:
1. It is too early.
2. Firms cannot isolate or measure gains (E4).
3. General systems such as ERP deliver slower, less quantifiable benefits than targeted
   equipment (P01 p.71).
4. Successful projects started from a clearly identified problem with KPIs (E5).

Explanations 2–4 are consistent with a diagnosis, selection and measurement gap. **But the
evidence equally supports a rival explanation:** small, light-touch interventions may simply not
move SME firm-level performance measurably, whatever the diagnosis. The documents cannot tell
these apart. That rival explanation is the main threat to Hypothesis A.

### A3. Reconciling the Made Smarter facts

| Fact | What it proves | What it does NOT prove |
|---|---|---|
| 78% reported post-programme adoption | Participants bought or implemented something after support (self-report) | That adoption was caused by the programme (most would have digitalised anyway, "at a slower pace", p.62), or that it improved performance |
| Robust models: no significant effect on turnover, employment, productivity | Measured against comparable firms, **the programme cannot be shown to change firm growth**. The naïve model (Model 1) overstated impact: participants were already growing faster before joining (p.68; significant pre-trends in 6 of 11 years) | That the programme had zero effect. Confidence intervals are wide and follow-up is short. Parallel trends are formally rejected even in Models 2–3, so the null is itself fragile |
| Positive GVA / GVA-per-worker effects in year 3 | Something may be happening late: the pattern is consistent across all three models, driven by lower input consumption | Any credible size. Fewer than 10% of firms reach year 3. The evaluators themselves reject the magnitudes (>£1bn GVA from a £19.8m programme) |
| "Some magnitudes appear unrealistic; future validation needed" | Standard econometrics on SME microdata **cannot currently tell whether operational investments pay off** | Anything about the real effect size |

**Net effect on Hypothesis A: mixed. It strengthens the "verification" half and weakens the
"economic importance" half.**
- **Strengthens.** A national programme, a professional evaluator and ONS microdata could not
  establish whether the interventions worked, and firms themselves mostly could not say (E4).
  The gap between *doing* improvements and *knowing their economic effect* is documented at
  national scale.
- **Weakens.** If a programme that engaged 2,000+ firms and funded real investments produced no
  robust firm-level effect, then single-firm interventions may produce effects too small to
  matter commercially. Our experiment must be designed to detect that possibility, not assume it
  away.

### A4. ONS management practices: what is and is not established

- **Firm size:** smaller firms score lower (0.51 for 10–19 employees vs 0.68 for 250+). The gap
  survives controls (0.15). Correlation.
- **Production firms:** the production sector scores lower than services (0.52 vs 0.56) and has
  "a longer tail" of low scorers. The document gives only the construction and non-manufacturing
  bottom-decile values (0.15, 0.24), **not manufacturing's**.
- **Structured decision-making:** below-median firms are 4× more likely to use little or no
  analysis for important decisions.
- **KPI usage:** the weakest dimension economy-wide (0.42).
- **Continuous improvement:** the highest dimension (0.80), but it is self-reported "how
  businesses respond to problems". It says nothing about whether firms find the *right* problem.
- **Productivity association:** positive and statistically significant, but correlational.
  Causality is not shown here.

**What ONS does not establish:** that better KPIs or constraint identification would *raise*
productivity in UK manufacturing SMEs. It also shows that time, not money or knowledge, is the
main barrier (36%), and that only 13% hire consultants. Both are **warnings** about buyer
bandwidth and willingness to pay for outside help.

### A5. Competitive landscape. What exactly would we do that is not commoditised?

| Provider type | What they do | Evidence status |
|---|---|---|
| Made Smarter advisers | Free diagnostic, roadmap and grants; **technology-framed** (IDT need, DRL; E6) | FACT (P01) |
| Catapults / Manufacturing Technology Centre | Technology demonstration; one firm found it "too advanced" for them (P01 p.53) | FACT (P01) |
| Lean / Theory of Constraints / industrial-engineering consultants | Constraint finding, SMED, flow; TOC is literally "find the constraint" | UNVERIFIED in session (general knowledge); long-established field |
| Operational-excellence consultancies | Larger-firm programmes | UNVERIFIED |
| MES / OEE / machine monitoring (incl. SME-focused monitoring products) | Measure machine states and OEE | UNVERIFIED in session |
| ERP (Sage, Epicor, Syspro and others) | Planning and records; ERP was a common roadmap priority (P01 p.43) | FACT that ERP is common; vendors UNVERIFIED |
| Systems integrators | Automation implementation | UNVERIFIED |

**What is commoditised:** constraint-finding *as a concept* (TOC/Lean), machine monitoring,
technology advice (free via Made Smarter), and ERP.

**What the evidence says is not being supplied:** **economic verification.** Nobody in this
landscape routinely delivers a pre-registered, causally interpretable measurement of whether a
specific intervention changed throughput and contribution at a specific firm, and nobody
accumulates those results across firms. Evidence for the gap:
- E4: firms can't measure.
- E3: the national evaluation couldn't measure credibly.
- E8: evaluators found an "absence of evaluation evidence" to benchmark against.

**Credible answer to "what would we do":**
> Confirm the binding constraint with measured evidence rather than opinion, choose the smallest
> reversible intervention on it, prove or disprove its economic effect with a pre-registered
> reversal design, and keep the outcome in a cross-firm evidence base of *constraint type ×
> intervention × measured effect*.

**Honest weakness of that answer:**
- Each individual delivery looks like a Lean/TOC consultant with better statistics.
- The differentiation exists only if the evidence base accumulates.
- ONS shows buyers are time-poor and rarely hire consultants.

**Verdict:** there is a credible, narrow answer, so manufacturing is **not killed** under the
brief's rule. It is not a strong answer until the first cases show that firms value
verification, not just improvement.

### A6. Smallest real experiment (4–8 weeks)

| Element | Specification |
|---|---|
| Manufacturer | One UK SME manufacturer, 20–100 employees, batch or job-shop (e.g. fabricated metal, CNC machining, plastics moulding), with an **order backlog or regular overtime**. Without a backlog, extra capacity has no cash value |
| Production flow | One routing family through one department |
| Suspected constraint | One work centre suspected of limiting the flow. Pre-registered confirmation rule: persistent queue ahead of it, downstream starvation, and highest utilisation, from 2 weeks of observation |
| Baseline (weeks 1–2) | Daily **good output in standard hours per scheduled hour** for the flow (standard hours neutralise product-mix changes); constraint state by work sampling (running / setup / starved / blocked / down / unstaffed); WIP ahead of the constraint twice daily; scrap/rework |
| Bounded intervention | One reversible, zero-capex change that protects constraint time. Examples: cover breaks and shift changes at the constraint; stage tooling and material before changeovers (external setup); release work to the constraint's pace. Chosen from the baseline data, not in advance |
| Comparison | **A-B-A-B reversal:** baseline 2 weeks → intervention 2 weeks → withdrawal 1 week → reinstate 2 weeks (7 weeks). Plus a within-firm check that non-constraint stations did not change output |
| Primary outcome | Good standard hours per scheduled hour for the flow, phase B vs phase A |
| Economic outcome | Additional constraint hours × **contribution margin per constraint hour** (sales price − truly variable cost), counted only for output the backlog absorbs; or overtime hours avoided × loaded rate |
| Success criterion (pre-registered) | Throughput ≥ 10% higher in both B phases than in both A phases; the gain falls during withdrawal and returns on reinstatement; scrap rate no more than 1 point worse; economic value ≥ £500/week |
| Data | Shop-floor tallies (paper is fine), job/ERP timestamps if they exist, price and variable-cost data for the flow |
| Access | Owner/works manager sponsorship; about 1–2 site days a week; supervisors' cooperation |
| Duration | 7–8 weeks |
| Likely cost | £3–8k (observer time, travel, a manufacturing-engineering practitioner if the operator lacks shop-floor expertise). `ESTIMATE` |
| Expertise | Industrial engineering / TOC / SMED practice, and time-series or experimental analysis |
| Major risks | Hawthorne effect (observation alone raises output; the long baseline and reversal help); demand or mix shocks; the firm refusing withdrawal; the "constraint" not being binding (a *useful* negative result) |

**Is 4–8 weeks genuinely enough? Yes, for the operational outcome.** Constraint throughput
responds within days, so each phase contains 10+ working days. The economic outcome is valid
only where a backlog exists.

---

## 3. Hypothesis B — Inventory & working-capital decision quality

**Proposition tested:** "An economically important and accessible portion of excess inventory
and working capital in mid-market firms is caused by systematically improvable planning and
replenishment decisions rather than unavoidable commercial or supply-chain constraints."

### B1. What independent evidence proves the magnitude?

**None that meets the standard.**
- **P04 is the only magnitude source.** It is a consultancy that sells working-capital services
  (P04 p.16).
- It analyses **listed** companies, with no stated method for "excess" (€1.84tn).
- The UK headline (+48% NWC days) is attributed partly to a **fall in DPO**, i.e. paying
  suppliers faster, which is not an inventory decision.
- UK cash-intensive-sector DIO (62.8 days) is *lower* than both the EU (90.2) and North America
  (68.6).
- Its "mid-size" category (+24.2% DIO) is listed mid-caps, not the private mid-market.

**Magnitude for the target population (private UK mid-market): not established.**

### B2. Separating causes

| Cause | Decision-improvable? | Evidence in P01–P04 |
|---|---|---|
| Poor forecasting | Yes | P04 recommends "sharpen demand forecasting" (advice, not measurement) |
| Reorder parameters | Yes | None |
| Safety-stock policy | Yes | None |
| Supplier MOQs | Mostly no (negotiable at the margin) | None |
| Supplier lead-time variability | No (buffer is a rational response) | P04: "long lead times … key to driving asset utilisation" (narrative) |
| Purchasing discounts | Trade-off; partly | None |
| Seasonality | No (pre-build is rational) | None |
| Customer service targets | Policy choice | None |
| Obsolete items | Partly (SKU discipline) | P04: "disciplined SKU management to eliminate dead stock" (advice) |
| Master-data problems | Yes | None |
| Deliberate resilience buffers | No (by definition deliberate) | P04: shift from "just in time" to "just in case" to "just because" stocking (narrative; no measure of the "just because" share) |

### B3. What proportion is decision-improvable?

**Cannot be evidenced from any available primary document.** P04 hints that part of the
post-pandemic stock is "just because" (a decision problem) and part is "just in case" (a
resilience choice). It gives no split.

Per the brief: **total excess working capital must not be treated as our addressable problem.**
The addressable share is unknown, and could be small.

### B4. Incumbents. What exactly is unsolved?

Incumbents (general knowledge; not verified in this session):
- ERP reorder points and MRP, standard in mid-market ERPs;
- inventory-optimisation products aimed at the mid-market;
- demand-forecasting and supply-chain planning suites;
- consultancies, including PwC's own working-capital practice (P04 p.16, FACT);
- AI forecasting products.

Parameter optimisation (safety stock, reorder point, order quantity) is textbook operations
research, and is packaged in all of these.

**What may be unsolved:**
- *adherence*: buyers overriding parameters;
- *master-data hygiene*;
- *verification*: proving at a given firm that a parameter change released cash without hurting
  service.

These are real but narrow. The mature tools already sit on the data, and their vendors see far
more firms than we would. **No evidence of an unsolved layer that incumbents cannot reach.**

### B5. Smallest credible causal experiment

| Element | Specification |
|---|---|
| Organisation | One UK wholesale distributor, £10–50m turnover, ERP-based replenishment, no dedicated planning tool |
| Scope | One warehouse, one product family, 500–2,000 active SKUs |
| Randomisation | **Randomise by supplier cluster**, not SKU. SKUs from the same supplier share MOQs and order combining, so SKU-level randomisation would contaminate the control. Stratify by velocity (ABC) |
| Treatment | Recalculated reorder point and order quantity to a pre-set service level, respecting MOQs, and applied by the buyer |
| Control | Unchanged parameters |
| Service constraint (pre-registered) | Treated line-fill no more than 0.5 points below control; stop rule if a treated A-item stocks out twice |
| Outcome | Average on-hand inventory value per SKU vs the SKU's own baseline, treated vs control; cash released × (cost of capital + carrying cost) |
| Duration | **12–20 weeks.** Stock levels move only as replenishment cycles turn (lead time + review period), and service effects need enough demand events. Within 4–8 weeks only order-intake value is observable, a leading indicator rather than the outcome |
| Cost | £2–6k. `ESTIMATE` |
| Risks | Buyer non-compliance or override; contamination via shared suppliers; stock-outs damaging customers; too few supplier clusters for statistical power |

**Time-to-proof penalised honestly: 4–8 weeks is not enough** for the working-capital outcome.

---

## 4. Direct duel

Ratings: ▲ stronger, ▼ weaker, = similar. Each is justified by the sections above.

| Dimension | A. Manufacturing | B. Inventory | Edge |
|---|---|---|---|
| Problem reality | Measurement/verification gap documented at national scale (E3, E4, E12). Constraint misidentification and economic magnitude unmeasured | Only consultancy data on listed firms; cause split absent | **A** |
| Causal measurability | n=1 time series with reversal; fair | Randomised supplier clusters; strong in principle | **B** |
| Time to proof | 7–8 weeks for the operational outcome | 12–20 weeks | **A** |
| Accessibility | Plausible (2,000+ SMEs engaged an outside adviser), but needs shop-floor presence | Plausible; ERP exports suffice | = |
| Economic consequence (per firm) | Contribution per constraint hour; valid only with a backlog | Cash release (one-off) + carrying cost (recurring) | = (both unquantified) |
| Competitive white space | Verification layer is thin (E8); diagnosis concept is commoditised | Tools mature and hold more data | **A** |
| Repeatability | ~50k manufacturing SMEs in five regions alone (E9, `ESTIMATE`) | Large, but served by incumbents | = |
| Operator learning | Physical operations, economics, experimentation | Supply-chain analytics | **A** |
| AI leverage | Better AI makes messy-data analysis cheap; physical confirmation stays scarce → **more valuable** | Better AI commoditises forecasting and parameter setting → **leaning commoditised** | **A** |
| Risk | Shop-floor safety (low if changes are scheduling/prep); Hawthorne | Stock-outs harming customers | = |
| Cost of first experiment | £3–8k | £2–6k | B (slightly) |
| Transferability | Constraint logic transfers across all flow processes (manufacturing, labs, kitchens, logistics hubs, healthcare flow) | Transfers across stocking businesses | **A** |
| Moat trajectory | Cross-firm causal effect library, which no one publishes (E8) | Incumbents already learn from larger fleets | **A** |
| Long-term ceiling | Productivity creation in the physical economy | Capital efficiency; one-off cash release | **A** |

## 5. The 100-intervention test

**Manufacturing: what #100 knows that #1 did not**
1. **Base rate of misdiagnosis.** How often the manager's suspected constraint was not the
   binding one, by process type. This fact does not exist anywhere today.
2. **Effect-size distributions with confidence intervals** for each (constraint type ×
   intervention) pair, e.g. break coverage at a CNC constraint, external setup at a moulding
   press, release control in fabrication.
3. **Time-to-effect and decay curves.** Which gains persist once observation stops.
4. **The Hawthorne component.** How much of the measured gain is observation alone, estimated
   from withdrawal phases.
5. **A validated minimal-data diagnostic.** Which cheap signals (WIP counts, job-ticket
   timestamps, work sampling) locate the true constraint in firms without MES, with accuracy
   measured against outcomes. This becomes a labelled evaluation set.
6. **Demand-conversion rules.** When freed capacity became cash, and when it did not
   (market-constrained firms).
7. **Contribution-per-constraint-hour benchmarks** by sub-sector.

**Inventory: what #100 knows that #1 did not**
1. Distribution of reducible excess by SKU class and sector.
2. Share of excess caused by MOQs and lead times vs parameters.
3. Randomised effect sizes of parameter resets.
4. Buyer override rates and their causes.

Items 1–2 and 4 are **already visible** to planning-software vendors across thousands of
customers. Only item 3 (randomised causal effects) would be distinctive, and it is narrow.

## 6. Copy test

A competitor is given our website, pitch, prompts, public software, £500k and six engineers. What
can they **not** reproduce in 90 days?

- **Manufacturing:** at deployment 0, **nothing**; they could hire Lean engineers and a
  statistician. After roughly 20 or more deployments, they cannot reproduce:
  - the outcome-labelled library (items 1–7 above);
  - validated diagnostic accuracy;
  - calibrated effect priors that let us promise realistic gains.

  All of these need calendar time *inside* factories.
- **Inventory:** a parameter-optimisation engine is buildable in 90 days, and incumbents already
  have one. They also hold more cross-firm data than we would reach in years. **Moat weak at
  every stage.**

## 7. Verdicts

- **B. Inventory & working capital: KILLED as a Case 001 candidate.** The problem is not killed
  as a problem in the world. Grounds:
  1. magnitude for the target population is unevidenced (only a consultancy study of listed
     firms);
  2. the decision-improvable share is unevidenced;
  3. the likely wedge is packaged by mature incumbents holding more data;
  4. better AI pushes it towards commoditisation;
  5. 4–8 weeks is not enough for the outcome.
- **A. Manufacturing: SURVIVES, but NOT SELECTABLE yet.**
  - Its verification/measurement gap is established from primary evidence, and its first
    experiment is fast, bounded and reversible.
  - Its central economic claim is not established: that constraints go unidentified *and* that
    fixing them is worth material money in a typical SME.
  - The strongest evidence available (a national evaluation's null result) is compatible with a
    rival explanation that would kill it: light-touch interventions do not move SME performance.

  See `phase_zero_gate_v1.md` for the gate and the pre-registered next test.

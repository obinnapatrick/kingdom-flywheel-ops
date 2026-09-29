# Sector Map — where economic loss concentrates

Built from economic **functions** (what work the economy does), not software categories. For each
function: the loss mechanisms that recur, representative evidence, and what that implies for a
solo operator. Evidence labels follow `CLAUDE.md` (`FACT`, `REPORTED`, `ESTIMATE`, `ASSUMPTION`,
`HYPOTHESIS`). Source IDs refer to `evidence/source_register.csv`.

> **Limitation.** During this scan the environment's network policy blocked direct retrieval of
> primary documents (gov.uk, nao.org.uk, wrap.ngo, ama-assn.org, and others). Figures below were
> taken from search-engine excerpts of named sources and are therefore `REPORTED`, not `FACT`,
> unless stated otherwise.

## 1. The shape of the economy's waste

Across functions, loss clusters into seven recurring mechanisms. They matter more than sectors,
because the same mechanism reappears in many sectors and builds transferable skill.

| # | Mechanism | Description | Typical sign |
|---|---|---|---|
| M1 | **Leakage at a document boundary** | Money is lost where one organisation bills, deducts or pays another and nobody reconciles the documents properly. | Deductions, overcharges, duplicate payments, missed refunds |
| M2 | **Waiting / idle capacity** | Assets or people wait on information, approvals or other parties. | Detention, downtime, validation delays, payment delay |
| M3 | **Rework** | Work done twice because the first attempt was wrong or incomplete. | Construction rework, invalid applications, repeat visits |
| M4 | **Unclaimed entitlement** | A right to money exists (refund, relief, preference, guarantee) but is not exercised. | Missed tariff preferences, SLA refunds, retentions not chased |
| M5 | **Coordination overhead** | Human labour spent moving information between systems and parties. | Order entry, customs declarations, prior authorisation |
| M6 | **Mispricing / information asymmetry** | One side overpays because it cannot see the true price. | Energy broker commissions, contract price non-compliance |
| M7 | **Physical waste** | Materials, energy or goods consumed for no output. | Food waste, out-of-hours energy use, returns |

**Observation (HYPOTHESIS):** M1 and M4 are unusually well suited to a first laboratory. The value
appears as discrete, verifiable cash; historical data often allows a *look-back* measurement
(counterfactual = "this money would not have been recovered"); and the work is analysis of data
the buyer already holds. M2, M3 and M7 often have larger totals but weaker measurability and
longer proof cycles.

## 2. Function-by-function map

| Function | Main loss mechanisms | Representative evidence | Solo-operator implication |
|---|---|---|---|
| **Production / manufacturing** | M2 downtime, M3 scrap/rework | `REPORTED` Siemens *True Cost of Downtime 2024*: Fortune Global 500 lose ~$1.4tn/yr (≈11% of revenue) to unplanned downtime; large plant ≈27 h/month [S03] | Enormous, but needs plant access, sensors and long proof cycles. Poor first arena. |
| **Construction** | M3 rework, M1/M4 payment leakage, M2 delay | `REPORTED` Get It Right Initiative: direct avoidable-error cost ≈5% of project value, up to 21% incl. indirect [S08]. `REPORTED` BEIS 2017: £7.8bn of retentions unpaid over 3 years to 2016; £3.2–5.9bn withheld per year [S11]. `REPORTED` Payapps survey: 79% of subcontractors almost always paid late, 73% face routine disputes over applications [S27, vendor] | Rework is too hard to attribute. Subcontractor cash-cycle leakage is document-bound and measurable. |
| **Healthcare operations** | M5 admin, M1 claims | `REPORTED` AMA 2024: ~13 h/week of physician+staff time on prior authorisation [S05]. `REPORTED` Premier 2024: ~15% of claims to private payers initially denied; adjudication cost $25.7bn [S06]. `REPORTED` NHS outpatient DNA 5.6% of 146.1m appointments [S04] | Large and measurable, but regulated (PHI), US-centric or NHS-procured. Blocked by licence/access. |
| **Logistics** | M2 detention, M1 freight billing errors | `REPORTED` ATRI 2024: detention at 39% of stops, $3.6bn direct + $11.5bn productivity loss (2023) [S07]. Freight/parcel billing error rates 3–15% `REPORTED` (vendor sources only) [S20] | Detention: incentives misaligned. Billing errors: measurable, but evidence is vendor-grade. |
| **Energy (as a cost for businesses)** | M7 waste, M1 billing error, M6 broker mispricing | `REPORTED` DESNZ: Q1 2026 non-domestic electricity avg 23.61p/kWh ex-CCL; smallest band 34.31p [S36]. `REPORTED` Carbon Trust: 5–10% savings available through no/low-cost measures in every business [S26]. `REPORTED` Ofgem (via secondary sources): brokers "in some cases nearly doubling" contract costs; 77% of broker users believed service free [S22] | Measurable from meter data. Broker problem is being regulated away. |
| **Financial operations** | M1 duplicate/erroneous payments, M2 late payment | `REPORTED` DBT/London Economics 2025: late payment costs UK ≈£11bn/yr, 133m staff hours chasing, £26bn outstanding at any time [S01]. `REPORTED` APQC: 0.8–2% of disbursements duplicate or erroneous [S14]; but recovery audits typically recover only ~0.1% of spend [S35] | Late payment is largely structural (power). AP recovery is real but small per client and crowded. |
| **Professional services** | M2 lock-up, M5 admin | `REPORTED` Clio: realisation ~88%; median lock-up 75 days [S10] | Well served by practice-management software. |
| **Commerce / retail supply** | M1 deductions, M7 returns | `REPORTED` NRF/Appriss 2024: returns 13.21% of sales; $103bn fraudulent returns [S21]. `REPORTED` deductions 2–5% of gross revenue, 1–3% invalid (vendor sources) [S02]. `REPORTED` GCA 2025: 17% of UK grocery suppliers report invoice discrepancies, 11% payment delays [S31] | Deductions: measurable, repeatable, but crowded in the US. UK grocery code reduces the UK version. |
| **International trade** | M5 declaration labour, M4 unclaimed preferences, M1 misclassification | `REPORTED` HMRC/Ipsos: GB–EU customs admin burden £1.8bn for 38.6m declarations in 2022 (≈£48/declaration) [S24]. `REPORTED` gov.uk: 90.0% of GB imports from EU used available preferences in 2024 [S25]. `REPORTED` 251,000 importing businesses in 2024 [S32]. `REPORTED` UKGT: 47% of tariff lines zero [S33] | Recoverable, verifiable cash (HMRC repayments) with a 3-year look-back. Evidence on *how much* is recoverable is weak. |
| **Property / housing** | M2 voids, M3 repairs | `REPORTED` Scottish Housing Regulator: void rent loss £39.8m, 1.3% of rent (2024/25) [S19] | Void loss small; repairs sit inside public-style procurement. |
| **Hospitality** | M7 food waste | `REPORTED` WRAP: ~£3.2bn/yr, ≈£10k per outlet [S16] | Per-site value small; hardware incumbents. |
| **Government-adjacent (commercially accessible)** | M3 invalid applications, M2 delay | `REPORTED` 324,300 planning applications in England in year to Dec 2025 [S34]; `REPORTED` invalidation up to ~45–50% in some contexts (single council/appeals, not national) [S12] | Public data allows baseline measurement without any company. Buyer budgets are thin. |
| **Procurement** | M6/M1 contract value leakage | `REPORTED` WorldCC: 8.6% average value erosion (self-reported survey) [S09]. `REPORTED` UK public spend with SMEs ≈20% [S15] | "Leakage" metric is survey-based and ill-defined; public tenders have slow, noisy outcomes. |
| **Revenue operations** | M1 failed payments, M2 lead response | `REPORTED` Recurly: involuntary churn 20–40% of churn (vendor) [S13]. Missed-call statistics are vendor-only [S17] | Commoditised tooling. |
| **Customer service / field service** | M3 repeat visits | `REPORTED` Aberdeen: FTF avg 75% vs 89% best-in-class; $200–300 per extra dispatch [S23] | Owned by large FSM platforms. |
| **Insurance operations** | M1 claims leakage | `REPORTED` 5–10% of claim payments (industry estimate, sources vary) [S18] | Enterprise buyers, regulated. |
| **Wholesale distribution** | M5 order entry | `REPORTED` vendor claims: 30–40% of orders arrive by email; Rexel Canada had 70% manual entry pre-automation [S30] | Clear mechanics; rapidly crowding with AI vendors. **Overlaps a prior venture of the operator — disclosed, no bonus.** |
| **Agriculture, education, workforce, compliance/KYC, cloud/SaaS spend** | Various | Screened only; no evidence gathered in this scan (see ledger rows X01–X10) | Deferred, not rejected. |

## 3. What the map suggests (HYPOTHESES, not conclusions)

1. The largest totals (downtime, rework, healthcare admin) are the least accessible to a solo
   operator. Size and accessibility are negatively correlated in this scan.
2. The most measurable problems are **document-boundary leakage** (M1) and **unclaimed
   entitlements** (M4), because recovered cash is its own proof.
3. Many M1 problems in the US are already crowded (deductions, parcel audit, recovery audit).
   Crowding in the UK appears lower but is **not yet evidenced**.
4. Several candidates are shrinking through regulation (energy brokers, construction retentions,
   late payment reform). Regulatory change is also a source of *new* entitlements and obligations
   — worth a dedicated scan in the next phase.

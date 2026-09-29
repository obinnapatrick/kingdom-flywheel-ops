# C25 — Import duty overpaid by UK importers (misclassification, valuation, unclaimed preferences)

Status: **SURVIVOR — suspended on soft kill S2 (magnitude cannot yet be bounded).**
Evidence confidence: **L**. Highest rubric score (78.4) and robust to weights, but the score rests
on judgement about a magnitude we have not measured.

## Mechanism

Every import declaration carries a commodity code, a customs value and (where relevant) a claim to
preferential origin. Errors that overstate duty are rarely noticed, because the importer's broker
declares what they are told, and nobody downstream loses anything visible. HMRC allows repayment
of overpaid duty for **3 years** from acceptance of the declaration (C285 process) [S40].
Mechanism class: M4 unclaimed entitlement + M1 document-boundary leakage.

## Supporting evidence

| Claim | Label | Source |
|---|---|---|
| 251,000 VAT-registered businesses imported goods in 2024 | REPORTED | S32 |
| 90.0% of GB imports from the EU27 used a preference where one was available (2024), i.e. ~10% of eligible value did not | REPORTED | S25 |
| In Q1 2021, UK *export* preference utilisation to the EU was ~73%; €2.5–3.5bn of exports paid avoidable tariffs | REPORTED | S38 |
| A classification vendor claims "two in five" tariff codes are wrong across 1.5m products audited | REPORTED (vendor) | S39 |
| Repayment covers classification, valuation and missed-preference errors, within 3 years | REPORTED | S40 |
| GB–EU declarations cost ~£48 each to produce (£1.8bn across 38.6m in 2022) — i.e. importers already pay for declaration work and rarely re-examine it | REPORTED | S24 |

## Disconfirming evidence

| Claim | Effect | Source |
|---|---|---|
| 47% of UK Global Tariff lines are zero and ~70% of MFN imports enter duty-free | Large share of imports cannot be overpaid at all; recoverable pool is narrower than import values suggest | S33 |
| 90% preference utilisation is already high, and non-use is often *rational* (duty saved smaller than cost of proving origin) | Much of the 10% gap may not be recoverable or worth recovering | S25, S38 (reasoning) |
| Vendor 40%-wrong figure does not state the direction of error; misclassification can under-declare as often as over-declare | Audits may find liabilities, not refunds; clients may prefer not to know | S39 |
| AI and consultancy offers for C285 recovery already exist | Market not empty | S42 |

## Estimates

- `ESTIMATE` Upper bound of the recoverable pool is **not computable yet**. It requires: value of
  dutiable imports × share with over-declared duty × average excess rate × 3 years, minus
  claims where evidence (e.g. origin statements) cannot be obtained retrospectively. None of these
  inputs is yet evidenced except the 10% non-use share for EU preferences.
- `ESTIMATE` Per-client value for a mid-sized importer paying £500k/yr duty: if 2–5% of duty were
  recoverable (`ASSUMPTION`, unevidenced), 3-year look-back = £30k–£75k. This is illustrative only
  and must not be used for selection.

## Open gaps (ranked)

1. Value of GB imports that were eligible for a preference but paid MFN duty, by commodity and
   importer size (gov.uk preference utilisation tables — blocked in this session).
2. Annual customs duty receipts and HMRC repayment statistics (number/value of C285 claims) —
   would show whether recovery is common and what it yields.
3. Direction of classification errors (over vs under declaration) from any independent audit
   study or HMRC post-clearance audit statistics.
4. Whether importers can self-serve their own historic declaration data from CDS.
5. How brokers and consultancies price this work, and how many operate (competitor density).

## Red team

1. **Why unsolved?** Because the loser (importer) cannot see the loss, and the party who could
   (broker) is paid per declaration, not for accuracy. Plausible — but it is equally plausible that
   the pool is small and nobody bothers.
2. **Who solves it well?** Big importers have in-house customs teams; Big Four indirect-tax teams
   do this for large clients; boutique consultancies and new AI entrants exist (S42).
3. **Why trust us?** A contingency fee removes the financial risk, but handing over three years of
   declarations and supplier invoices to an unknown individual is a real trust barrier.
4. **Build internally?** Mid-market importers lack customs expertise; unlikely.
5. **Big tech / incumbents?** Customs platforms (Descartes, broker software) could add
   classification checks; HMRC itself could flag obvious errors. Forward-looking accuracy will
   likely be commoditised; historic recovery less so.
6. **AI much cheaper?** Classification suggestions get commoditised. What remains valuable is
   verified outcomes: which claims HMRC accepts and why.
7. **Copy in a weekend?** A classifier, yes. A claims track record, an origin-evidence playbook
   and an outcome dataset, no.
8. **Hard to copy?** A dataset of accepted/rejected repayment claims by commodity and error type.
9. **Recoverable?** Unknown. This is the central weakness.
10. **Large vs accessible?** Risk of confusing £ hundreds of billions of import value with a
    recoverable pool that could be tiny.
11. **Motivated to change?** Found money with no up-front cost is attractive; fear of HMRC
    scrutiny is a real counter-motivation.
12. **Real data?** Only via importers; no public dataset of individual declarations.
13. **Causation?** Excellent: an HMRC repayment would not have occurred without the claim.
14. **Solo operator?** Plausible: analysis of exported data plus claim preparation. No licence
    needed to prepare claims as an agent (`HYPOTHESIS` — verify HMRC agent authorisation rules).
15. **Learning if it fails?** High: trade rules, tax administration, B2B trust-building,
    evidence-based selling.

**Red-team verdict:** not killed, but cannot be selected on current evidence. The magnitude gap is
potentially fatal and cheap to test with public statistics.

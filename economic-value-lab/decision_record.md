# Decision Record

## DR-001 — First global scan (Phase Zero), 2026-09-29

### Decision

**No arena selected.** The evidence is not strong enough to proceed to selection. Four candidates
remain on the shortlist for targeted evidence gathering. Six weaker survivors are parked. The
rest are killed and kept on record.

### Process followed

1. Mapped economic functions and recurring loss mechanisms (`sector_map.md`).
2. Generated 40 candidate problems. 10 were screened at desk level only (X01–X10: no evidence
   gathered, so not counted as investigated). **30 were investigated** with evidence searches.
   Of these, C28 duplicated C20 and was merged, leaving **29 distinct problems**.
3. Applied `kill_criteria.md`. **18 killed outright, 1 partially killed and merged (C11 into C27),
   10 survived.**
4. Evidence test: labelled each claim; flagged vendor-only magnitudes (soft kill S1/S2 →
   C02, C20, C25, C29 suspended rather than killed).
5. Rubric scoring with sensitivity across 5 weight sets (`scoring/`). 4 survivors robust.
6. Competitor, access and economic tests; red teams for the robust four
   (`evidence/candidates/`).

### Candidates killed and why

| ID | Problem | Kill | Reason |
|---|---|---|---|
| C01 | UK SME late payment | K16, K6 | Cheap tools exist; residual is payer power; reform under way |
| C03 | Manufacturing downtime | K1, K8, K15 | Plant access, capital, enterprise sales |
| C04 | NHS outpatient no-shows | K15, K6 | NHS procurement; saturated reminder tech |
| C05 | US prior authorisation | K7, K1 | US patient data; EHR access |
| C06 | US claim denials | K7, K1, K6 | Regulated data; well-funded incumbents |
| C07 | Truck detention | K10, K16 | Party bearing cost is not the party causing it |
| C08 | Construction rework | K9, K5 | Savings not attributable within months |
| C09 | Contract value leakage | K2, K15 | Survey metric not measurable as defined; enterprise |
| C10 | Law-firm billing lock-up | K6 | Practice-management vendors own it |
| C11 | Construction retentions (new flow) | K11 | Ban confirmed (S37); legacy stock kept in C27 |
| C13 | Involuntary subscription churn | K6, K18 | Solved inside billing platforms |
| C15 | SME public tenders | K9, K5 | Win-rate causation unprovable quickly |
| C16 | Hospitality food waste | K3, K6 | Small per-site value; hardware incumbents |
| C17 | Missed calls in trades | K6, S1 | Commoditised; vendor-only evidence |
| C18 | Insurance claims leakage | K15, K1 | Enterprise insurers only |
| C19 | Social housing voids/repairs | K3, K15, K13 | Small void loss; public procurement; safety |
| C21 | Retail returns fraud | K15, K6 | Enterprise incumbents |
| C22 | Energy broker commissions | K11, K14 | Being regulated; residual is claims-farming |
| C23 | Field-service repeat visits | K6, K9 | Incumbent platforms; weak causation |

### Survivors

| Tier | IDs | Note |
|---|---|---|
| Shortlist (robust) | C25, C02, C27, C26 | See `shortlist.md`. None selectable: confidence below M on a required dimension |
| Parked (not robust) | C20, C12, C14, C30, C29, C24 | Re-examine only if new evidence changes a score by ≥1 point on a weight-9+ dimension |

### Disclosures and bias checks

- **C30 (distributor order entry) overlaps a prior venture of the operator.** It was evaluated
  with no bonus and ranked 8th of 10; it is not robust. Its inclusion is recorded so that it is
  not later re-selected by familiarity.
- **AI bias check:** of the four shortlisted, AI is core to none. Recovery (C25, C02, C27) and
  energy analytics (C26) could all start with spreadsheets and rules. Recorded as consistent with
  rule 11.
- **Size bias check:** the three largest problems found (downtime, rework, healthcare admin) were
  all killed on access or causation, not on size.
- **Single-analyst scoring:** all scores are one analyst's judgement. Differences under ~5 points
  are treated as ties.

### Material limitations of this scan

1. **Primary documents were not read.** The environment's network policy blocked direct access
   to gov.uk, nao.org.uk, wrap.ngo, ama-assn.org, londoneconomics.co.uk and others. Every figure is
   `REPORTED` (seen via search excerpts), none is `FACT`.
2. **Operator context is assumed** (UK-based, solo, ≤£25k, unlicensed). A wrong assumption changes
   accessibility scores, mostly for the US-centric candidates (C02, C05, C06, C07).
3. **No buyer evidence.** Willingness to pay has been inferred from existing services' pricing,
   not observed. That is correct for Phase Zero (no company contact), but it caps URG confidence.

### Unresolved questions

1. For each shortlisted candidate, what is the **capturable value per typical buyer**, from an
   independent source or a derivation from official statistics?
2. C25: how much duty is paid on imports that were eligible for a preference, and is
   misclassification skewed towards over- or under-payment?
3. C27: what share of applied value is never paid to subcontractors, excluding retentions?
4. C26: how long do no-cost energy savings last, and do multi-site operators pay for verified
   savings?
5. C02: is there any independent measurement of invalid deductions, and any segment vendors
   do not serve?
6. Are the UK versions of document-boundary leakage problems (M1) less crowded than the US
   versions, as assumed?
7. Regulation-created entitlements (new rights to refunds, reliefs or compensation) were not
   scanned systematically — a possible blind spot.

### Evidence gaps (the Evidence Gap Sprint)

This is the one next action. It is desk research only: no company contact, no building.

| Gap | Candidate | Primary source to obtain | Kill or promote rule |
|---|---|---|---|
| G1 | C25 | gov.uk *Preference utilisation of UK trade in goods 2024* tables: value of eligible imports not using preference, by chapter | Kill C25 if the implied avoidable duty on EU imports is < £100m/yr and no other overpayment source is evidenced |
| G2 | C25 | HMRC customs duty receipts and repayment/C285 statistics (published or via FOI) | Promote if repayments are material and concentrated in mid-sized importers |
| G3 | C25 | Any independent study of classification error direction (HMRC post-clearance audit results, NAO, academic) | Kill if errors are predominantly under-declarations |
| G4 | C27 | Original BEIS 2017 retention research + ONS/DBT construction business population; any independent study of certified vs applied value | Kill if capturable value per subcontractor < K3 threshold after removing retentions |
| G5 | C26 | Carbon Trust / DESNZ / academic evidence on out-of-hours share and savings persistence | Kill if typical persistent savings fall under K3 threshold for multi-site operators |
| G6 | C02 | Credit Research Foundation or academic evidence on deduction rates; vendor coverage map by retailer | Kill if no independent corroboration or no uncovered segment |
| G7 | All | Re-read every `REPORTED` figure in the original document and upgrade to `FACT` or strike it | Re-score; rerun `scoring/score.py` |

**Precondition:** the environment needs network access to at least `gov.uk`,
`assets.publishing.service.gov.uk`, `nao.org.uk` and `ac.uk` domains, or the sprint must be run
somewhere that has it.

**Exit condition for the sprint:** each shortlisted candidate is either killed or reaches
confidence ≥ M on SEV, MEAS, ACC and URG. If all four die, return to the parked list and the
unscanned regulation-created-entitlements space. Do not lower the bar.

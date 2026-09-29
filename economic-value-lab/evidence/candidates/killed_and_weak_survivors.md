# Evidence notes — killed candidates and weak survivors

Kept so that these ideas are not rediscovered as if they were new. Full rows are in
`candidate_ledger.csv`; sources in `source_register.csv`.

## Weak survivors (passed kills, not robust in scoring)

| ID | Key evidence | Strongest disconfirming evidence | Why weak |
|---|---|---|---|
| C20 Carrier invoice / SLA refunds (UK) | Vendor error rates 3–22% (S20, S28) | Vendor-only; claim windows of 15–21 days prevent look-back (S28) | Ordinary rules-based software already sold; suspended on S1 |
| C12 Planning invalidation (England) | 324,300 applications/yr (S34); up to ~45% invalid at one council (S12) | No national invalidation rate found; the government's digital planning programme may give this away free | Thin buyer budgets; not robust |
| C14 AP overpayment recovery | APQC 0.8–2% erroneous disbursements (S14) | Recovery audits actually yield ~0.1% of spend (S35) — the headline overstates capturable value by ~10× | Small per-client value, high trust barrier |
| C30 Distributor order entry | Vendor: 30–40% of orders by email (S30) | Vendor-only; category crowded with AI and ERP vendors | **Overlaps a prior venture of the operator — disclosed, no bonus.** Not robust |
| C29 Energy billing errors | Ofgem-attributed 27% of small businesses found errors (S29, via vendor) | 12-month back-billing limit caps look-back; bureaus exist | Small per-buyer value; suspended on S1 |
| C24 Customs declaration production | £1.8bn / 38.6m declarations (S24) | Requires liable intermediaries; crowded software | Lowest-scoring survivor |

## Killed

| ID | Kill criteria | One-line reason |
|---|---|---|
| C01 UK SME late payment | K16, K6 | Cheap chasing tools exist; what remains is payer power; being addressed by reform (S37) |
| C03 Manufacturing downtime | K1, K8, K15 | Plant access, sensors, enterprise sales |
| C04 NHS outpatient DNAs | K15, K6 | NHS procurement and IG; reminder tech saturated |
| C05 US prior authorisation | K7, K1 | US PHI; EHR access |
| C06 US claim denials | K7, K1, K6 | Regulated data; well-funded incumbents |
| C07 Truck detention | K10, K16 | Loser (carrier) is not the actor (shipper) |
| C08 Construction rework | K9, K5 | Cannot attribute savings within months |
| C09 Contract value leakage | K2, K15 | Survey metric, not measurable as defined; enterprise |
| C10 Law-firm lock-up | K6 | Practice-management vendors own the data |
| C11 Construction retentions (new flow) | K11 | Ban confirmed; legacy stock merged into C27 |
| C13 Involuntary churn | K6, K18 | Built into billing platforms |
| C15 SME public tenders | K9, K5 | Win-rate causation unprovable quickly |
| C16 Hospitality food waste | K3, K6 | ~£10k/outlet total loss; hardware incumbents |
| C17 Missed calls (trades) | K6, S1 | Vendor-only evidence; commoditised AI receptionists |
| C18 Insurance claims leakage | K15, K1 | Enterprise insurers only |
| C19 Social housing voids/repairs | K3, K15, K13 | Void loss 1.3% of rent (Scotland); repairs public and safety-critical |
| C21 Retail returns fraud | K15, K6 | Enterprise, strong incumbents |
| C22 Energy broker commissions | K11, K14 | Being regulated; residual value is claims-farming |
| C23 Field-service repeat visits | K6, K9 | FSM incumbents own workflow |

## Merged

- C28 Parcel audit (UK) → merged into C20 (same mechanism).

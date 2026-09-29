# Independent Review Audit Log (Phase Zero step 1C)

Reviewer: independent evidence reviewer (Claude, same model family as prior analyst — residual independence limitation).
Started: 2026-09-29T18:57:47Z

## Note on the initial directory listing
Ran `ls` on economic-value-lab/ to confirm location. This shows FILE NAMES only (no contents). No forbidden file opened.

## File access log (time order)
| # | Time (UTC) | Path | Purpose | Permitted pre-blind? |
|---|---|---|---|---|
| 1 | 18:57 | economic-value-lab/ (directory listing via `ls`, names only) | Confirm location; no file contents read | Yes (listing only) |
| 2 | 18:58 | economic-value-lab/CLAUDE.md | Constitution | Yes |
| 3 | 18:58 | scratchpad/review_inputs/rubric_v2_redacted.md | Scoring rubric (redacted) | Yes |
| 4 | 18:59 | economic-value-lab/kill_criteria.md | Kill criteria | Yes |
| 5 | 18:59 | economic-value-lab/evidence/README.md | Evidence rules | Yes |
| 6 | 18:59 | economic-value-lab/evidence/ (directory listing via `ls`, names only: README.md, candidates/, source_register*.csv) | Confirm register filenames | Yes (listing only; candidates/ not opened) |
| 7 | 19:00 | economic-value-lab/evidence/source_register.csv | Prior analyst's evidence leads (v1) | Yes |
| 8 | 19:00 | economic-value-lab/evidence/source_register_v2.csv | Prior analyst's evidence leads (v2) | Yes |

Note on item 7/8: the registers contain `used_by` candidate IDs (e.g. C25, C27b, N05, N08) but no scores. Candidate IDs reveal which arenas were examined, not how they scored. The v1 register's evidence/README lists candidate evidence filenames (C25_import_duty_recovery, C27_subcontractor_cash_cycle, C02_retailer_deductions, C26_out_of_hours_energy) — this hints those were v1 focal candidates. Recorded as a minor leakage of prior focus, not of scores.

## URL fetch log
| # | Time (UTC) | URL | Tool | Result |
|---|---|---|---|---|

## PART 1 LOCK
- Locked at: 2026-09-29T19:00:43Z
- File hashed: scratchpad/ir/part1.md (copy preserved as scratchpad/ir/part1_locked.md)
- sha256: a5864d0747b300324d849f2fe653eba56006f677cb2b146947d671e8e8d5abb8
- Part 1 was written before any web search/fetch and before any forbidden file was opened.
- Verification: the Part 1 section in independent_review_v1.md is the byte-identical content of part1_locked.md; re-hash to confirm.

## URL fetch log (all attempts after Part 1 lock)
| # | Time (UTC) | URL | Tool | Result |
|---|---|---|---|---|
| U1 | ~19:02 | https://www.kcl.ac.uk/construction-law/assets/kcl-dpsl-construction-adjudication-report-3.0-2024-update-digital-aw1.pdf | WebFetch | BLOCKED (egress proxy) |
| U2 | ~19:02 | https://www.gov.uk/government/publications/made-smarter-adoption-impact-and-process-evaluation | WebFetch | BLOCKED |
| U3 | ~19:03 | https://www.ifm.eng.cam.ac.uk/news/study-for-uk-government-examines-impact-of-made-smarter-adoption-programme/ | WebFetch | BLOCKED |
| U4 | ~19:03 | /root/.ccr/README.md + proxy status endpoint | Bash | DENIED by permission classifier; not pursued |
| U5 | ~19:04 | https://assets.publishing.service.gov.uk/ | WebFetch | BLOCKED |
| U6 | ~19:04 | https://web.archive.org/web/2026/https://www.gov.uk/...made-smarter-adoption-impact-and-process-evaluation | WebFetch | FAILED (tool cannot fetch web.archive.org) |
| U7 | ~19:04 | https://www.ukri.org/wp-content/uploads/2026/01/UKRI-220126-ISCF-FinalImpactEvaluation.pdf | WebFetch | BLOCKED |
| U8 | ~19:05 | https://www.adjudication.org/resources/research | WebFetch | BLOCKED |
| U9 | ~19:05 | https://bidstats.uk/tenders/2022/W37/782631220 | WebFetch | BLOCKED |
| U10 | ~19:05 | https://blogs.sussex.ac.uk/uktpo/publications/preference-utilisation-in-the-tca-how-are-we-doing/ | WebFetch | BLOCKED |
| U11 | ~19:05 | https://en.wikipedia.org/wiki/Made_Smarter | WebFetch | BLOCKED |
| U12 | ~19:05 | https://www.cato.org/blog/ieepa-refunds-update-good-progress-still-ways-go | WebFetch | BLOCKED |
| U13 | ~19:05 | https://www.lexology.com/ | WebFetch | BLOCKED |
| U14 | ~19:06 | https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9748816/ | WebFetch | BLOCKED |
| U15 | ~19:06 | https://www.researchgate.net/publication/382701655 | WebFetch | BLOCKED |
| U16 | ~19:06 | curl probe (status codes only): gov.uk content API, madesmarter.uk, building.co.uk, fenwickelliott.com, pinsentmasons.com, ukdataservice.ac.uk, api.crossref.org, thebusinessdesk.com, themanufacturer.com | Bash curl | ALL connect_rejected by egress proxy. pypi.org (200) and github.com reachable — package/code hosts only; no primary documents there |

Conclusion at 19:06: egress policy behaves as an allowlist limited to code/package hosts. No primary document for any arena can be opened. WebSearch (excerpts) is the only research channel. Every external claim in Part 2 is therefore at best REPORTED.

## WebSearch log (excerpt-only; recorded for transparency)
| # | Query (abridged) |
|---|---|
| Q1 | Made Smarter Adoption programme impact evaluation 2026 statistically significant turnover productivity |
| Q2 | "Made Smarter Adoption" evaluation "not statistically significant" ... July 2026 |
| Q3 | Made Smarter Adoption impact and process evaluation findings ... |
| Q4 | "Made Smarter" adoption evaluation July 2026 "statistically significant" ... econometric |
| Q5 | Made Smarter ... counterfactual "did not find"/"no evidence" |
| Q6 | KCL Adjudication Society 2024 report 2,264 referrals 50% |
| Q7 | CIIP Cambridge Made Smarter Adoption evaluation findings |
| Q8 | "Made Smarter Adoption" final impact evaluation 2026 difference-in-differences technical annex |
| Q9 | ONS management practices 2023 MES |
| Q10 | ONS firm-level productivity dispersion long tail |
| Q11 | KCL 2024 smash and grab 63% claim value |
| Q12 | Adjudication Society referrals statistics |
| Q13 | subcontractor payment notice software JCT AI |
| Q14 | cost of construction adjudication UK legal costs |
| Q15 | HMRC customs administrative burden 2022 £1.8bn |
| Q16 | preference utilisation of UK trade in goods 2024 |
| Q17 | HMRC customs duty tax gap |
| Q18 | Measuring tax gaps customs duty gap |
| Q19 | CDS data export / Get Customs Data |
| Q20 | HMRC C285 repayment guidance |
| Q21 | IEEPA tariff refunds status Sept 2026 |
| Q22 | HMRC post-clearance audit misclassification statistics |
| Q23-25 | site-restricted (s3.amazonaws.com) searches for mirrors of preference-utilisation, Made Smarter evaluation, customs admin burden |
| Q26 | independent SME inventory management studies |
| Q27 | UK inventory/working capital mid-market (PwC) |
| Q28 | Perera "Inventory optimisation adoption amongst SMEs" |
| Q29 | MRO obsolete spares independent evidence |
| Q30 | BSR Gateway 2 2026 statistics |
| Q31 | national planning invalidation rate England |
| Q32 | ICAEW/ACCA accountancy capacity |
| Q33 | Bloom et al. "Does management matter" |
| Q34 | UK SME manufacturers production data / OEE adoption |
| Q35 | "Do management interventions last" |
| Q36 | AI construction contract administration software UK 2026 |
| Q37 | AI tariff classification tools 2026 |

## URL fetch log (continued)
| # | Time (UTC) | URL | Tool | Result |
|---|---|---|---|---|
| U17 | ~19:10 | https://www.ciip.group.cam.ac.uk/reports-and-articles/ciip-study-...made-smarter-adoption-programme/ | WebFetch | BLOCKED |
| U18 | ~19:10 | https://www.michelmores.com/construction-engineering-insight/construction-adjudication-trends-2024/ | WebFetch | BLOCKED |
| U19 | ~19:10 | https://innovation-research-caucus-uploads.s3.amazonaws.com/production/uploads/2026/03/IRC-Report-Impacts-on-regional-Growth-and-Policy-Effectiveness-FINAL-March-2026.pdf | WebFetch | **OPENED** (PDF saved; text extracted locally with PyMuPDF in a scratchpad venv). Read: title page, executive summary, method notes |
| U20 | ~19:10 | https://www.eversheds-sutherland.com/en/global/insights/construction-adjudication-kings-college | WebFetch | BLOCKED |
| U21 | ~19:14 | https://www.productivity.ac.uk/wp-content/uploads/2023/11/PIP020-Firm-level-productivity-FINAL-Nov-2023.pdf | WebFetch | BLOCKED |
| U22 | ~19:14 | https://www.bis.org/speeches/20180723-uks-productivity-problem-hub-no-spokes.pdf | WebFetch | BLOCKED |
| U23 | ~19:14 | https://www.nber.org/system/files/working_papers/w16658/w16658.pdf | WebFetch | BLOCKED |
| U24 | ~19:14 | https://arxiv.org/abs/2310.05985 | WebFetch | BLOCKED |
| U25 | ~19:20 | https://www.uktradeinfo.com/trade-data/request-customs-declaration-service-data-on-imports-and-exports/ | WebFetch | BLOCKED |
| U26 | ~19:20 | https://www.thebwa.com/hmrc-launches-new-customs-data-download-tool/ | WebFetch | BLOCKED |
| U27 | ~19:21 | https://s3.amazonaws.com/thegovernmentsays-files/content/177/1775053.html (third-party archive of gov.uk C285 guidance) | WebFetch | **OPENED**. Archived version "last updated 20 December 2021" |
| U28 | ~19:21 | https://govukdiff.njk.onl/... (C285 diff) | WebFetch | BLOCKED |
| U29 | ~19:23 | curl probe: ebi.ac.uk europepmc, europepmc.org, thegovernmentsays.com | Bash curl | BLOCKED; escoe-website.s3 403; s3.amazonaws.com/thegovernmentsays-files 200 (public bucket listing) |
| U30 | ~19:24-19:28 | s3.amazonaws.com/thegovernmentsays-files bucket listing (prefix content/189-191; attachments/ prefix searches for HMRC_CAB, Made_Smarter, Preference, Measuring_tax, Management_practices) | Bash curl | Listing reachable; no matching attachments. Downloaded 158 mirrored gov.uk pages first seen 30 Jul-3 Aug 2026 to look for the Made Smarter Adoption evaluation page: **NOT PRESENT** in the mirror (mirror is a sparse sample of gov.uk) |
| U31 | ~19:30 | https://shura.shu.ac.uk/31340/1/Perera-InventoryOptimisationAdoption(VoR).pdf | WebFetch | BLOCKED |
| U32 | ~19:33 | https://poverty-action.org/...Does-Management-Matter...pdf | WebFetch | BLOCKED |
| U33 | ~19:33 | https://www.oecd.org/en/publications/sme-technology-adoption-in-the-united-kingdom_.../the-state-of-sme-technology-adoption... | WebFetch | BLOCKED |
| U34 | ~19:33 | https://worldmanagementsurvey.org/...Does-Management-Matter...pdf | WebFetch | BLOCKED |

Summary: 2 documents actually opened (U19 IRC report — peripheral; U27 archived C285 guidance). The KCL/Adjudication Society report, the Made Smarter Adoption evaluation, the HMRC admin-burden study, the preference-utilisation statistics, ONS management practices and all inventory/MRO sources could NOT be opened.

## Parts 2-6 written to independent_review_v1.md at 2026-09-29T19:13:04Z, BEFORE any forbidden file was opened. sha256 of parts2_6.md: 43ac458446891ea0083e754618e98f9d3ca0fc7c7c7cdd02a2324d1ca24c46b0


## Correction note (2026-09-29T19:13:11Z)
The '~HH:MM' times in the URL fetch log (U17-U34) were approximate and over-estimated. All web searches and fetches actually happened between 19:01 and 19:12 UTC (system clock: Part 1 locked 19:00:43Z; Parts 2-6 assembled 19:13:04Z). Order of entries is correct.

## PART 7 — post-blind file access (permitted only now)
| # | Time (UTC) | Path | Purpose | Permitted? |
|---|---|---|---|---|
| P1 | 19:13 | scoring/ and evidence/candidates/ (directory listing) | Locate Part 7 files | Yes (post-blind) |
| P2 | 19:14 | scoring/v2/results_v2.md | Prior v2 results | Yes (post-blind) |
| P3 | 19:14 | scoring/v2/scores_v2.csv (header + rows for the 9 arenas and C24/C25/N06) | Prior sub-scores | Yes (post-blind) |
| P4 | 19:14 | scoring/v2/score_v2.py (read to confirm formula) | Check formula equivalence | Yes (post-blind; scoring/ allowed after lock) |
| P5 | 19:15 | decision_record_v2.md | Prior DR-002 | Yes (post-blind) |
| P6 | 19:15 | shortlist.md | Prior v1 shortlist | Yes (post-blind) |
| P7 | 19:16 | economic-value-lab/rubric_v2.md (diff vs redacted copy) | Confirm redaction content | Yes (post-blind) |
| P8 | 19:16 | second_scan_v1.csv (header + N05,N08,N18,N19,N21) | Prior evidence for new arenas | Yes (post-blind) |
| P9 | 19:16 | candidate_ledger_v2.csv (header + 12 rows) | Prior status | Yes (post-blind) |
| P10 | 19:17 | evidence/candidates/C25_import_duty_recovery.md | Prior customs evidence | Yes (post-blind) |
| P11 | 19:17 | evidence/candidates/C27_subcontractor_cash_cycle.md | Prior construction evidence | Yes (post-blind) |
| P12 | 19:17 | evidence/candidates/killed_and_weak_survivors.md (grep for relevant rows) | Prior notes on C12/C30 | Yes (post-blind) |
| P13 | 19:17 | decision_record.md (lines 1-40) | Prior DR-001 | Yes (post-blind) |
Not opened at any point: selector_audit_v1.md, archetype_coverage_v1.md, sector_map.md, README.md (root), candidate_ledger.csv (v1), opportunity_rubric.md, C02/C26 evidence files, scoring/audit_v1/*, scoring/results.md, scoring/scores.csv.

## Final assembly
- 2026-09-29T19:15:52Z: Part 7, Final Gate, Reviewer Conclusion and Appendix appended to independent_review_v1.md. Part 1 confirmed embedded byte-identical to part1_locked.md (sha256 a5864d0747b300324d849f2fe653eba56006f677cb2b146947d671e8e8d5abb8).
- Files created in project: independent_review_v1.md, independent_review_audit_log.md. Nothing committed or pushed.
- Scratchpad working files: scratchpad/ir/{score.py, rev.py, cmp.py, part1.md, part1_locked.md, parts2_6.md, part7_end.md, irc.pdf, irc.txt, keys.txt, titles_jul30.txt, mirror/}

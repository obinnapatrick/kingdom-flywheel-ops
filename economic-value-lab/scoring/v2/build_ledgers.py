"""Builds second_scan_v1.csv and candidate_ledger_v2.csv from scores_v2.csv,
archetypes.csv, the preserved v1 ledger and the qualitative notes below."""
import csv, math, pathlib, importlib.util
here = pathlib.Path(__file__).parent; lab = here.parent.parent
spec = importlib.util.spec_from_file_location("s", here/"score_v2.py")
import io, contextlib
with contextlib.redirect_stdout(io.StringIO()):
    s = importlib.util.module_from_spec(spec); spec.loader.exec_module(s)
S = {r["id"]: r for r in s.rows}
A = {r["id"]: r for r in csv.DictReader(open(here/"archetypes.csv"))}
v1 = {r["id"]: r for r in csv.DictReader(open(lab/"candidate_ledger.csv"))}

# qualitative fields for second-scan candidates:
# id: (sector, workflow, exact_problem, sources, key_evidence, current_handling, who_pays, competitors, strongest_against, v2_status_note)
N = {
"N01":("Healthcare operations","Hospital discharge and social-care handover","Patients medically ready to leave stay in acute beds while health and care organisations coordinate onward care","S43","~324,000 bed days lost in Jan 2025; avg delay 6.1 days (REPORTED)","Discharge hubs, transfer-of-care teams, trusted assessors","ICBs, trusts, councils","Care-coordination software, NHS digital discharge tools, consultancies","Root cause is mostly social-care capacity (structural); public buyers with long cycles; tier-A wedge unclear","PARKED (fails WEDGE gate)"),
"N02":("Healthcare operations","Elective theatre scheduling","Theatre lists under-booked or finishing early, wasting scarce surgical capacity","S44","85% capped utilisation target; early finishes and under-booking main drivers (REPORTED)","GIRFT programme, trust schedulers","Trusts/ICBs","Theatre scheduling software vendors, GIRFT (free), consultancies","NHS-only buyer; national programme already targets it; no tier-A access","PARKED (fails WEDGE gate)"),
"N03":("Logistics","Road freight capacity use","~30% of HGV km run empty","S45","Empty running 30-31% (REPORTED, DfT)","Backhaul boards, freight exchanges, fleet planners","Hauliers, shippers","Freight exchanges and load-matching platforms (not verified in this scan)","Much empty running is structural (specialist vehicles, directional imbalance); crowded matching market","PARKED (fails both gates)"),
"N04":("Energy","Grid connections","Generation/demand projects wait years for grid connection","S46",">700 GW queue; >300 GW removed by reform (REPORTED)","NESO reform; developers' consultants","Developers","Grid consultancies","Reform restructuring the queue now; physical capacity is the bottleneck; tier C for operator","KILLED (K11; K16)"),
"N05":("Construction / regulation","High-risk building approval (Gateway 2)","Applications to the Building Safety Regulator fail validation or stall for missing/poor design information, delaying high-rise projects","S47;S72","44-56% failed validation (2025); delays of 12-18 months; ~1,500 decisions/yr now at 77-82% approval (REPORTED)","Principal designers, fire engineers, specialist Gateway 2 consultancies","Developers/clients","Gateway 2 consultancies; law firms; BSR guidance","Regulator performance improving fast; low volume (~1,500/yr); life-safety domain requires specialists","SURVIVOR (passes both gates)"),
"N06":("Cross-economy","Management practices in SMEs","Weak structured management practices associated with lower productivity","S48","MES 2023 score 0.55; positive association after controls (REPORTED, ONS)","Business-support programmes, consultants, Help to Grow","SME owners","Consultancies, Help to Grow: Management, coaching","Causal effect slow and hard to measure; low urgency; interventions are consulting","PARKED (fails WEDGE gate)"),
"N07":("Social care","Workforce retention and homecare rostering","High turnover and unpaid travel time erode care capacity","S49;S50","Turnover 23.7%; ~19% of homecare day travelling (REPORTED)","Rostering software, recruitment","Care providers (thin, publicly set margins)","Birdie, Access, CarePlanner and others (not verified)","Buyers have thin margins set by council fees; safety-adjacent","PARKED (fails both gates)"),
"N08":("Manufacturing","Shop-floor throughput in SMEs","Machines and lines deliver far below available capacity (availability, speed, quality losses)","S51","Typical OEE ~60% vs 85% world class; Made Smarter reports 10-15% gains (REPORTED, programme/vendor)","Lean consultants, MES/OEE tools, Made Smarter adoption support","Operations directors/owners","OEE monitoring vendors, MES providers, Made Smarter","Requires shop-floor access and sensor data (tier B); OEE norms are practitioner lore","SURVIVOR (passes both gates)"),
"N09":("Food manufacturing","Production planning vs demand","Overproduction and forecast error create surplus and waste","S52","706kt waste, £0.85bn, 3.8% of food handled (REPORTED, WRAP)","Planners, WRAP programmes, redistribution","Manufacturers","Demand-planning software; WRAP (free)","Much waste is process loss not forecasting; access needs plant data","PARKED (fails WEDGE gate)"),
"N10":("Healthcare","Medication process","Medication errors cause harm and cost","S53","237m errors/yr; £98m definitely avoidable ADE cost (REPORTED, academic)","EPMA systems, pharmacists","NHS","EPMA vendors","Safety-critical at proof stage","KILLED (K13)"),
"N11":("Cross-economy","Customer service","Service failures generate repeat contacts and lost staff time","S54","£7.3bn/month (REPORTED, trade body)","Contact centres, CCaaS, AI agents","Service leaders","Salesforce, Microsoft, Zendesk, Genesys, many AI-agent start-ups","Hyper-contested by Big Tech and funded AI start-ups","KILLED (K6: named incumbents; SME and enterprise segments both served)"),
"N12":("Utilities","Water network maintenance","~20% of water put into supply leaks","S55","2,869 Ml/d leakage (REPORTED, Ofwat)","Acoustic loggers, satellite, pressure management","17 regulated water companies","Many specialist leak-detection vendors","Monopoly buyers with regulated procurement; dense specialist incumbents","KILLED (K6)"),
"N13":("Public services","Children's residential placements","Councils pay high prices in a dysfunctional placement market","S56","~£5.7bn market; 22.6% profit for largest providers (REPORTED, CMA)","Commissioning teams, frameworks","Councils","Regional commissioning, CMA remedies","Scarcity of placements is structural","KILLED (K16)"),
"N14":("Healthcare procurement","Trust purchasing","Trusts pay different prices for identical products","S57","£0.7bn procurement opportunity (REPORTED, Carter 2016)","NHS Supply Chain, price benchmarking programmes","Trusts","NHS Supply Chain, national price-transparency programmes","National programmes own the data and mandate","KILLED (K6)"),
"N15":("Education","SEND assessment","Statutory assessments exceed the 20-week limit","S58","46.1% within 20 weeks (REPORTED, DfE)","Council SEND teams","Councils","Case-management software","Driven by educational-psychologist shortage and demand (structural)","KILLED (K16)"),
"N16":("Healthcare","Waiting-list validation","Waiting lists contain patients no longer needing care","S59","£33 per validated removal; one trust removed 14,148 (REPORTED)","Validation teams, vendors","Trusts","Validation vendors","Temporary incentive scheme; perverse-incentive risk","KILLED (K11; K14)"),
"N17":("Workforce","Sickness absence","Working days lost to sickness","S60","148.9m days lost in 2024 (REPORTED, ONS)","Occupational health, absence management","Employers","OH providers, HR software","Causal effect of interventions not attributable within any practical design","KILLED (K9)"),
"N18":("Asset-intensive industry","Maintenance spares","Spare-parts inventories hold obsolete and excess stock while critical parts stock out","S61","15-25% obsolete (REPORTED, vendor-only)","Stores managers, CMMS","Operations/finance","Verusen, Sparetech, CMMS vendors","Vendor-only magnitude evidence","SURVIVOR (passes gates; suspended on S1)"),
"N19":("Distribution/manufacturing","Inventory and working-capital decisions (mid-market)","Mid-market firms hold the wrong inventory: excess slow stock alongside stock-outs, locking up cash and losing sales","S62;S66","UK NWC days up ~50% since 2015 (REPORTED, PwC, listed cos); OOS ~8% (academic)","Spreadsheets, ERP reorder points, planners","Finance/ops directors","Netstock, Slimstock, Inventory Planner, ERP planning modules (not individually verified)","Crowded planning-software market; mid-market magnitude not evidenced independently","SURVIVOR (passes both gates)"),
"N20":("Engineering","Knowledge transfer","Retiring engineers take tacit maintenance knowledge with them","S63","~18% of technicians retiring (REPORTED, unclear origin)","Mentoring, documentation","Employers","Knowledge-management and AR vendors","Outcome not measurable as a standalone problem","KILLED (K2; K9) - retained as a capability feature of maintenance arenas"),
"N21":("Professional services","Accountancy practice capacity","Firms turn away work for lack of qualified staff","S64","73% turned away work (REPORTED, outsourcer survey)","Offshoring, hiring, practice software","Practice owners","Dozens of AI accounting tools, offshore providers","Vendor-sourced evidence; extremely crowded","SURVIVOR (passes gates; suspended on S1)"),
"N22":("Manufacturing","Quoting (RFQ)","Slow quotes lose orders in job-shop manufacturing","S65","67% of buyers expect a quote in 24h (REPORTED, vendor)","Estimators, spreadsheets","Owners","Paperless Parts, aPriori and others","Vendor-only; win-rate causation noisy","PARKED (fails WEDGE gate)"),
"N23":("Retail","On-shelf availability","Out-of-stocks lose sales","S66","OOS ~8%; UK OSA 89.7% (REPORTED)","Replenishment systems","Grocers/brands","Enterprise replenishment vendors, shelf-scanning","Enterprise buyers with strong incumbents","KILLED (K6)"),
"N24":("Energy","Demand flexibility","Businesses under-use flexibility markets","S67","DFS winter 2024-25 savings £483k nationally (REPORTED)","Aggregators, suppliers","Businesses","Aggregators","Value per participant tiny","KILLED (K3)"),
"N25":("Justice","Court and tribunal throughput","Record backlogs delay justice","S68","Crown Court 80,200 outstanding; ET 59.6 weeks (REPORTED)","HMCTS","State","n/a","Judicial function; tier C","KILLED (access tier C)"),
}
D = {
"C25b":("International trade","Customs classification, origin and duty strategy","Firms make costly customs decisions (classification, origin, valuation, special procedures, sourcing) under volatile tariffs with poor evidence","S24;S25;S33;S73","US IEEPA refunds ~$165bn ordered after Feb 2026 ruling shows scale/volatility; UK recoverable pool unknown (REPORTED)","Brokers, in-house customs teams, Big Four","Importers' finance/supply-chain leads","Brokers, Descartes, Avalara, Big Four, AI customs start-ups","UK magnitude unevidenced; US wedge needs licensed brokers; refund events are one-off","SURVIVOR (passes gates; confidence L)"),
"C27b":("Construction","Contract administration (pre-dispute)","Payment/pay-less notices, change and variation records, time-bar notices and valuations are administered badly, generating avoidable disputes on both sides of the contract","S69;S70;S71;S77","2,264 adjudications/yr (record); 50% cite inadequate contract administration; smash-and-grab experienced by 63%; typical claim £125k-£500k (REPORTED, KCL)","QSs, commercial managers, CEMAR on NEC projects, lawyers after the fact","Main contractors and subcontractors (both lose)","Thinkproject CEMAR (NEC), Payapps/TrakPro, CDEs, QS firms","Magnitude of avoidable cost not independently quantified; NEC tier-1 segment served; construction trust barrier","SURVIVOR (passes both gates)"),
}
def num(r):
    return dict(wedge=f"{s.wedge(r):.1f}", ceiling=f"{s.ceiling(r):.1f}", combined=f"{s.combined(r):.1f}",
                passes_gates=("n/a (killed)" if r["kill_v2"] else ("yes" if s.wedge(r)>=60 and s.ceiling(r)>=60 else "no")))
cols2 = ["id","archetype_primary","archetype_secondary","sector","workflow","exact_problem","sources","key_evidence","current_handling","who_pays","access_tier","competitors","strongest_argument_against","evidence_confidence","value_type","v2_kill","wedge","ceiling","combined","passes_gates","status_v2"]
with open(lab/"second_scan_v1.csv","w",newline="") as f:
    w = csv.writer(f); w.writerow(cols2)
    for i,(sec,wf,prob,src,ev,cur,pay,comp,ag,st) in N.items():
        r=S[i]; n=num(r)
        w.writerow([i,A[i]["primary"],A[i]["secondary"],sec,wf,prob,src,ev,cur,pay,r["access_tier"],comp,ag,r["confidence"],r["value_type"],r["kill_v2"],n["wedge"],n["ceiling"],n["combined"],n["passes_gates"],st])
# ledger v2: every candidate ever, v1 status preserved
V2NOTE = {
 "C02":"KILLED v2 (K6): independent CRF data confirms problem (6-10% of deduction $ invalid) but every checked segment now served (S76)",
 "C03":"PARKED v2: reinstated (v1 kills were constraint-based); fails WEDGE gate - no tier-A entry",
 "C04":"KILLED v2 (K6)","C05":"KILLED v2 (K6: funded PA-automation incumbents + regulation)","C06":"KILLED v2 (K6)",
 "C12":"SURVIVOR v2 (passes gates; not robust) - candidate adjacency to N05 'regulatory submission quality'",
 "C14":"PARKED v2 (fails CEILING gate: redistributive)","C18":"PARKED v2: reinstated from v1 constraint kill; fails WEDGE gate",
 "C19":"KILLED v2 (K3 voids); repairs not separately investigated","C20":"PARKED v2 (fails CEILING gate)",
 "C24":"PARKED v2 (fails WEDGE gate); absorbed as adjacency of C25b","C25":"MATERIALLY WEAKENED -> PARKED v2 (fails CEILING gate); broad recovery thesis replaced by C25b arena",
 "C26":"KILLED v2 (K6): free supplier portals already provide half-hourly out-of-hours reporting (S74)",
 "C27":"MATERIALLY WEAKENED -> PARKED v2 (fails CEILING gate); retentions K11, ordinary late payment K16; pre-dispute layer re-entered as C27b",
 "C29":"PARKED v2 (fails CEILING gate)","C30":"SURVIVOR v2 (passes gates narrowly; not robust); overlaps prior venture - no bonus",
}
colsL = ["id","name","scan","archetype_primary","archetype_secondary","value_type","access_tier","status_v1","v1_decision_basis","v2_kill","wedge","ceiling","combined","passes_gates","evidence_confidence","status_v2"]
with open(lab/"candidate_ledger_v2.csv","w",newline="") as f:
    w = csv.writer(f); w.writerow(colsL)
    for i,r in S.items():
        n=num(r); a=A[i]
        st1 = v1[i]["status"] if i in v1 else ("DERIVED in step 1B" if a["scan"]=="derived" else "NEW in scan 2")
        b1 = v1[i]["decision_basis"] if i in v1 else ""
        if i in V2NOTE: st2 = V2NOTE[i]
        elif i in N: st2 = N[i][-1]
        elif i in D: st2 = D[i][-1]
        elif r["kill_v2"]: st2 = f"KILLED v2 ({r['kill_v2']})"
        else: st2 = "SURVIVOR v2" if n["passes_gates"]=="yes" else "PARKED v2"
        w.writerow([i,r["name"],a["scan"],a["primary"],a["secondary"],r["value_type"],r["access_tier"],st1,b1,r["kill_v2"],n["wedge"],n["ceiling"],n["combined"],n["passes_gates"],r["confidence"],st2])
    for i,r in v1.items():
        if i not in S:  # merged / screened rows kept for history
            w.writerow([i,r["exact_problem"],"1" if i.startswith("C") else "screened","","","","",r["status"],r["decision_basis"],"","","","","",r["evidence_confidence"],"unchanged from v1"])
print("ok")

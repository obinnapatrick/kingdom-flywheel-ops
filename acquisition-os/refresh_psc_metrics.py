#!/usr/bin/env python3
import io, json, os, re, time, urllib.error, urllib.request, zipfile
from datetime import datetime
from pathlib import Path

PSC_INDEX="https://download.companieshouse.gov.uk/en_pscdata.html"
PSC_BASE="https://download.companieshouse.gov.uk/"
INGEST_URL=os.environ.get("INGEST_URL","").strip()
OIDC_TOKEN=os.environ.get("OIDC_TOKEN","").strip()
OIDC_OBTAINED_AT=time.monotonic() if OIDC_TOKEN else 0.0
OUT=Path("out")
OUT.mkdir(exist_ok=True)
BATCH_SIZE=500

def oidc_token():
    global OIDC_TOKEN,OIDC_OBTAINED_AT
    request_url=os.environ.get("ACTIONS_ID_TOKEN_REQUEST_URL","").strip()
    request_token=os.environ.get("ACTIONS_ID_TOKEN_REQUEST_TOKEN","").strip()
    if request_url and request_token and (not OIDC_TOKEN or time.monotonic()-OIDC_OBTAINED_AT>180):
        sep="&" if "?" in request_url else "?"
        req=urllib.request.Request(
            request_url+sep+"audience=acq-os-supabase",
            headers={"Authorization":f"bearer {request_token}","User-Agent":"KingdomFlywheelAcquisitionOS/1.0"},
        )
        with urllib.request.urlopen(req,timeout=60) as r:
            OIDC_TOKEN=json.loads(r.read().decode())["value"]
            OIDC_OBTAINED_AT=time.monotonic()
    if not OIDC_TOKEN:
        raise RuntimeError("GitHub OIDC token unavailable")
    return OIDC_TOKEN

def post_json(payload):
    data=json.dumps(payload,separators=(",",":")).encode()
    for attempt in range(2):
        req=urllib.request.Request(
            INGEST_URL,data=data,method="POST",
            headers={
                "Authorization":f"Bearer {oidc_token()}",
                "Content-Type":"application/json",
                "User-Agent":"KingdomFlywheelAcquisitionOS/1.0",
            },
        )
        try:
            with urllib.request.urlopen(req,timeout=180) as r:
                return json.loads(r.read().decode())
        except urllib.error.HTTPError as e:
            detail=e.read().decode(errors="replace")
            if e.code==401 and attempt==0:
                globals()["OIDC_TOKEN"]=""
                continue
            raise RuntimeError(f"Ingest HTTP {e.code}: {detail[:1200]}") from e

def fetch_text(url):
    req=urllib.request.Request(url,headers={"User-Agent":"KingdomFlywheelAcquisitionOS/1.0"})
    with urllib.request.urlopen(req,timeout=120) as r:
        return r.read().decode("utf-8",errors="replace")

def download(url,target):
    req=urllib.request.Request(url,headers={"User-Agent":"KingdomFlywheelAcquisitionOS/1.0"})
    with urllib.request.urlopen(req,timeout=240) as r, open(target,"wb") as f:
        while True:
            chunk=r.read(1024*1024)
            if not chunk:
                break
            f.write(chunk)

def latest_parts():
    html=fetch_text(PSC_INDEX)
    pat=re.compile(r'psc-snapshot-(\d{4}-\d{2}-\d{2})_(\d+)of(\d+)\.zip')
    hits=[(m.group(1),int(m.group(2)),int(m.group(3)),m.group(0)) for m in pat.finditer(html)]
    if not hits:
        raise RuntimeError("Could not discover Companies House PSC split snapshot files")
    latest=max(x[0] for x in hits)
    rows=sorted({(part,total,name) for date,part,total,name in hits if date==latest})
    total=max(x[1] for x in rows)
    if len(rows)!=total:
        raise RuntimeError(f"Expected {total} PSC parts for {latest}, discovered {len(rows)}")
    return latest,[name for _,_,name in rows]

def ownership_min(natures):
    best=None
    for nature in natures or []:
        if not isinstance(nature,str) or "ownership-of-shares" not in nature:
            continue
        if "75-to-100-percent" in nature:
            val=75
        elif "50-to-75-percent" in nature:
            val=50
        elif "25-to-50-percent" in nature:
            val=25
        else:
            continue
        best=val if best is None else max(best,val)
    return best

def main():
    if not INGEST_URL:
        raise RuntimeError("INGEST_URL missing")

    target_response=post_json({"action":"psc_targets"})
    target_list=target_response.get("company_numbers") or []
    if isinstance(target_list,dict) and "result" in target_list:
        target_list=target_list["result"]
    if not isinstance(target_list,list):
        raise RuntimeError(f"Unexpected target list shape: {type(target_list)}")
    targets=set(str(x).strip() for x in target_list if str(x).strip())
    if not targets:
        raise RuntimeError("No DEEPEN target numbers returned")
    print(f"DEEPEN targets: {len(targets):,}",flush=True)

    snapshot,parts=latest_parts()
    begin=post_json({"action":"begin_psc","snapshot_date":snapshot})
    ingest_run_id=begin["ingest_run_id"]
    print(f"PSC snapshot={snapshot}, parts={len(parts)}, ingest_run={ingest_run_id}",flush=True)

    metrics={
        co:{
            "company_number":co,
            "active_psc_count":0,
            "individual_psc_count":0,
            "corporate_psc_count":0,
            "other_psc_count":0,
            "max_individual_ownership_min_pct":None,
            "max_any_ownership_min_pct":None,
            "earliest_notified_on":None,
            "latest_notified_on":None,
        } for co in targets
    }

    total_records=matched_records=ignored_statements=ceased_records=malformed=0

    for idx,filename in enumerate(parts,1):
        zpath=OUT/filename
        print(f"[{idx}/{len(parts)}] downloading {filename}",flush=True)
        download(PSC_BASE+filename,zpath)
        part_total=part_match=0

        with zipfile.ZipFile(zpath) as zf:
            txts=[n for n in zf.namelist() if n.lower().endswith((".txt",".json"))]
            if not txts:
                raise RuntimeError(f"No PSC text/json file inside {filename}")
            with zf.open(txts[0]) as raw, io.TextIOWrapper(raw,encoding="utf-8",errors="replace") as text:
                for line in text:
                    line=line.strip()
                    if not line:
                        continue
                    total_records+=1
                    part_total+=1
                    try:
                        rec=json.loads(line)
                    except Exception:
                        malformed+=1
                        continue
                    company_number=str(rec.get("company_number") or "").strip()
                    if company_number not in targets:
                        continue
                    data=rec.get("data") or {}
                    kind=str(data.get("kind") or "")
                    if "statement" in kind:
                        ignored_statements+=1
                        continue
                    if data.get("ceased_on"):
                        ceased_records+=1
                        continue

                    m=metrics[company_number]
                    m["active_psc_count"]+=1
                    if "individual" in kind:
                        m["individual_psc_count"]+=1
                    elif "corporate-entity" in kind or "legal-person" in kind:
                        m["corporate_psc_count"]+=1
                    else:
                        m["other_psc_count"]+=1

                    pct=ownership_min(data.get("natures_of_control") or [])
                    if pct is not None:
                        cur=m["max_any_ownership_min_pct"]
                        m["max_any_ownership_min_pct"]=pct if cur is None else max(cur,pct)
                        if "individual" in kind:
                            curi=m["max_individual_ownership_min_pct"]
                            m["max_individual_ownership_min_pct"]=pct if curi is None else max(curi,pct)

                    notified=str(data.get("notified_on") or "").strip()
                    if re.fullmatch(r"\d{4}-\d{2}-\d{2}",notified):
                        if m["earliest_notified_on"] is None or notified<m["earliest_notified_on"]:
                            m["earliest_notified_on"]=notified
                        if m["latest_notified_on"] is None or notified>m["latest_notified_on"]:
                            m["latest_notified_on"]=notified

                    matched_records+=1
                    part_match+=1

        zpath.unlink(missing_ok=True)
        print(f"[{idx}/{len(parts)}] records={part_total:,} matched_active={part_match:,}",flush=True)

    rows=list(metrics.values())
    uploaded=0
    for i in range(0,len(rows),BATCH_SIZE):
        batch=rows[i:i+BATCH_SIZE]
        response=post_json({
            "action":"psc_metrics_batch",
            "ingest_run_id":ingest_run_id,
            "snapshot_date":snapshot,
            "rows":batch,
        })
        updated=int(response.get("updated",0))
        if updated<=0:
            raise RuntimeError(f"PSC metric batch updated zero targets at offset {i}")
        uploaded+=updated
        if uploaded%5000< BATCH_SIZE:
            print(f"PSC company metrics uploaded={uploaded:,}/{len(rows):,}",flush=True)

    completed=post_json({"action":"complete_psc","ingest_run_id":ingest_run_id})
    summary={
        "snapshot_date":snapshot,
        "target_companies":len(targets),
        "parts":len(parts),
        "psc_records_scanned":total_records,
        "active_target_psc_records":matched_records,
        "ceased_target_psc_records_ignored":ceased_records,
        "psc_statements_ignored":ignored_statements,
        "malformed_lines":malformed,
        "company_metrics_uploaded":uploaded,
        "supabase_complete":completed,
        "privacy_mode":"company-level aggregates only; no names or dates of birth stored",
    }
    (OUT/"psc_metrics_summary.json").write_text(json.dumps(summary,indent=2),encoding="utf-8")
    print(json.dumps(summary,indent=2),flush=True)

if __name__=="__main__":
    main()

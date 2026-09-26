#!/usr/bin/env python3
import csv, io, json, os, re, time, urllib.error, urllib.request, zipfile
from collections import Counter
from datetime import datetime
from pathlib import Path

INDEX="https://download.companieshouse.gov.uk/"
INGEST_URL=os.environ.get("INGEST_URL","").strip()
OIDC_TOKEN=os.environ.get("OIDC_TOKEN","").strip()
OIDC_OBTAINED_AT=time.monotonic() if OIDC_TOKEN else 0.0
OUT=Path("out")
OUT.mkdir(exist_ok=True)
BATCH_SIZE=500
MIN_AGE_YEARS=5

# Tier A/B only. REVIEW sectors stay in reserve.
PREFIXES=("71200","43210","43220","43290","33120","33140","33190","80200","81100","62030")

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
    if not INGEST_URL:
        raise RuntimeError("INGEST_URL missing")
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
            with urllib.request.urlopen(req,timeout=120) as r:
                return json.loads(r.read().decode())
        except urllib.error.HTTPError as e:
            detail=e.read().decode(errors="replace")
            if e.code==401 and attempt==0:
                globals()["OIDC_TOKEN"]=""
                continue
            raise RuntimeError(f"Ingest HTTP {e.code}: {detail[:1000]}") from e

def month_candidates(months_back=6):
    today=datetime.utcnow().date()
    y,m=today.year,today.month
    out=[]
    for _ in range(months_back):
        out.append(f"{y:04d}-{m:02d}-01")
        m-=1
        if m==0:
            m=12
            y-=1
    return out

def url_exists(url):
    req=urllib.request.Request(url,method="HEAD",headers={"User-Agent":"KingdomFlywheelAcquisitionOS/1.0"})
    try:
        with urllib.request.urlopen(req,timeout=60) as r:
            return 200<=r.status<400
    except Exception:
        return False

def latest_snapshot():
    for snapshot in month_candidates():
        filename=f"BasicCompanyDataAsOneFile-{snapshot}.zip"
        if url_exists(INDEX+filename):
            return snapshot,filename
    raise RuntimeError("Could not locate current Companies House monthly snapshot")

def download(url,target):
    req=urllib.request.Request(url,headers={"User-Agent":"KingdomFlywheelAcquisitionOS/1.0"})
    with urllib.request.urlopen(req,timeout=180) as r, open(target,"wb") as f:
        while True:
            chunk=r.read(1024*1024)
            if not chunk: break
            f.write(chunk)

def parse_date(s):
    s=(s or "").strip()
    for fmt in ("%d/%m/%Y","%Y-%m-%d"):
        try: return datetime.strptime(s,fmt).date()
        except ValueError: pass
    return None

def sic_codes(row):
    out=[]
    for i in range(1,5):
        raw=(row.get(f"SICCode.SicText_{i}") or "").strip()
        m=re.match(r"(\d{2,5})",raw)
        if m: out.append(m.group(1))
    return out

def in_scope(codes):
    return any(any(code.startswith(p) for p in PREFIXES) for code in codes)

def main():
    snapshot,filename=latest_snapshot()
    snapshot_date=datetime.strptime(snapshot,"%Y-%m-%d").date()
    cutoff=snapshot_date.replace(year=snapshot_date.year-MIN_AGE_YEARS)
    run=post_json({"action":"begin_basic_metadata","snapshot_date":snapshot})
    ingest_run_id=run["ingest_run_id"]
    print(f"metadata ingest run: {ingest_run_id}",flush=True)

    zpath=OUT/filename
    print(f"downloading {filename}",flush=True)
    download(INDEX+filename,zpath)

    counts=Counter()
    batch=[]

    def flush():
        nonlocal batch
        if not batch: return
        result=post_json({"action":"basic_metadata_batch","ingest_run_id":ingest_run_id,"rows":batch})
        updated=int(result.get("updated",0))
        if updated<=0:
            sample=[r["company_number"] for r in batch[:5]]
            raise RuntimeError(f"Metadata batch updated zero targets; sample={sample}")
        counts["updated"]+=updated
        batch=[]

    with zipfile.ZipFile(zpath) as zf:
        names=[n for n in zf.namelist() if n.lower().endswith(".csv")]
        if not names: raise RuntimeError("No CSV inside snapshot")
        with zf.open(names[0]) as raw, io.TextIOWrapper(raw,encoding="utf-8-sig",errors="replace",newline="") as text:
            reader=csv.DictReader(text)
            reader.fieldnames=[(h or "").strip() for h in (reader.fieldnames or [])]
            for row in reader:
                counts["rows_seen"]+=1
                if (row.get("CompanyStatus") or "").strip().lower()!="active":
                    continue
                inc=parse_date(row.get("IncorporationDate"))
                if not inc or inc>cutoff:
                    continue
                codes=sic_codes(row)
                if not in_scope(codes):
                    continue
                company_number=(row.get("CompanyNumber") or "").strip()
                if not company_number:
                    counts["blank_company_number"]+=1
                    continue
                counts["matched"]+=1
                batch.append({
                    "company_number":company_number,
                    "accounts_category":(row.get("Accounts.AccountCategory") or "").strip(),
                    "accounts_last_made_up_date":(parse_date(row.get("Accounts.LastMadeUpDate")) or ""),
                    "accounts_next_due_date":(parse_date(row.get("Accounts.NextDueDate")) or ""),
                    "mortgages_outstanding":(row.get("Mortgages.NumMortOutstanding") or "").strip(),
                    "confirmation_statement_next_due_date":(parse_date(row.get("ConfStmtNextDueDate")) or ""),
                })
                # Convert date objects to ISO strings.
                for key in ("accounts_last_made_up_date","accounts_next_due_date","confirmation_statement_next_due_date"):
                    if hasattr(batch[-1][key],"isoformat"):
                        batch[-1][key]=batch[-1][key].isoformat()
                if len(batch)>=BATCH_SIZE:
                    flush()

    flush()
    zpath.unlink(missing_ok=True)
    completed=post_json({"action":"complete_basic_metadata","ingest_run_id":ingest_run_id})

    summary={
        "snapshot_date":snapshot,
        "generated_at_utc":datetime.utcnow().isoformat()+"Z",
        "scope":"PRIORITY+ALLOW acquisition sectors",
        "prefixes":PREFIXES,
        "counts":dict(counts),
        "supabase_complete":completed,
    }
    (OUT/"basic_metadata_summary.json").write_text(json.dumps(summary,indent=2),encoding="utf-8")
    print(json.dumps(summary,indent=2),flush=True)

if __name__=="__main__":
    main()

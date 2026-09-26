#!/usr/bin/env python3
import csv, io, json, os, re, urllib.request, zipfile
from collections import Counter
from datetime import datetime
from pathlib import Path

INDEX = "https://download.companieshouse.gov.uk/"
OUT = Path("out")
OUT.mkdir(exist_ok=True)
INGEST_URL = os.environ.get("INGEST_URL","").strip()
OIDC_TOKEN = os.environ.get("OIDC_TOKEN","").strip()
BATCH_SIZE = 250

PREFIXES = {
    "71200":"PRIORITY","43210":"PRIORITY","43220":"PRIORITY","43290":"ALLOW",
    "33120":"PRIORITY","33140":"PRIORITY","33190":"ALLOW","80200":"PRIORITY",
    "81100":"PRIORITY","62020":"REVIEW","62030":"PRIORITY","62090":"REVIEW",
    "46":"REVIEW",
}
MIN_AGE_YEARS = 5

def get(url, target=None):
    req = urllib.request.Request(url, headers={"User-Agent":"KingdomFlywheelAcquisitionOS/1.0"})
    with urllib.request.urlopen(req, timeout=180) as r:
        if target:
            with open(target, "wb") as f:
                while True:
                    chunk = r.read(1024*1024)
                    if not chunk: break
                    f.write(chunk)
            return None
        return r.read().decode("utf-8", errors="replace")

def post_json(payload):
    if not INGEST_URL or not OIDC_TOKEN:
        raise RuntimeError("INGEST_URL/OIDC_TOKEN missing")
    data=json.dumps(payload,separators=(",",":")).encode()
    req=urllib.request.Request(
        INGEST_URL,data=data,method="POST",
        headers={"Authorization":f"Bearer {OIDC_TOKEN}","Content-Type":"application/json","User-Agent":"KingdomFlywheelAcquisitionOS/1.0"}
    )
    with urllib.request.urlopen(req,timeout=120) as r:
        body=r.read().decode()
        if r.status < 200 or r.status >= 300: raise RuntimeError(body)
        return json.loads(body)

def month_candidates(months_back=6):
    today = datetime.utcnow().date()
    y, m = today.year, today.month
    out = []
    for _ in range(months_back):
        out.append(f"{y:04d}-{m:02d}-01")
        m -= 1
        if m == 0:
            m = 12
            y -= 1
    return out

def url_exists(url):
    req = urllib.request.Request(
        url,
        method="HEAD",
        headers={"User-Agent":"KingdomFlywheelAcquisitionOS/1.0"},
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return 200 <= r.status < 400
    except Exception:
        return False

def latest_parts():
    # Probe Companies House's stable one-file monthly naming convention.
    # This avoids scraping the human-facing HTML index.
    for snapshot in month_candidates():
        filename = f"BasicCompanyDataAsOneFile-{snapshot}.zip"
        if url_exists(INDEX + filename):
            return snapshot, [filename]
    raise RuntimeError("Could not locate a current Companies House monthly snapshot")

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

def disposition(codes):
    matches=[]
    for code in codes:
        for pref,disp in PREFIXES.items():
            if code.startswith(pref): matches.append((pref,disp))
    if not matches: return None,[]
    rank={"PRIORITY":3,"ALLOW":2,"REVIEW":1}
    return max(matches,key=lambda x:rank[x[1]])[1],matches

def main():
    snapshot,parts=latest_parts()
    snapshot_date=datetime.strptime(snapshot,"%Y-%m-%d").date()
    cutoff=snapshot_date.replace(year=snapshot_date.year-MIN_AGE_YEARS)

    begin=post_json({"action":"begin","snapshot_date":snapshot})
    ingest_run_id=begin["ingest_run_id"]
    print(f"Supabase ingest run: {ingest_run_id}",flush=True)

    out_csv=OUT/f"companies_house_candidates_{snapshot}.csv"
    counts=Counter(); sic_counts=Counter(); part_counts={}; batch=[]

    def flush_batch():
        nonlocal batch
        if not batch: return
        result=post_json({"action":"batch","ingest_run_id":ingest_run_id,"rows":batch})
        counts["uploaded"] += int(result.get("accepted",0))
        batch=[]

    fields=["company_number","company_name","company_status","company_type","incorporation_date",
            "sic_codes","matched_rules","disposition","registered_postcode","region","uri","snapshot_date"]
    with open(out_csv,"w",newline="",encoding="utf-8") as fo:
        w=csv.DictWriter(fo,fieldnames=fields); w.writeheader()
        for idx,filename in enumerate(parts,1):
            zpath=OUT/filename
            print(f"[{idx}/{len(parts)}] downloading {filename}",flush=True)
            get(INDEX+filename,zpath)
            kept=seen=0
            with zipfile.ZipFile(zpath) as zf:
                names=[n for n in zf.namelist() if n.lower().endswith(".csv")]
                if not names: raise RuntimeError(f"No CSV inside {filename}")
                with zf.open(names[0]) as raw, io.TextIOWrapper(raw,encoding="utf-8-sig",errors="replace",newline="") as text:
                    for row in csv.DictReader(text):
                        seen+=1; counts["rows_seen"]+=1
                        status=(row.get("CompanyStatus") or "").strip()
                        if status.lower()!="active":
                            counts["reject_status"]+=1; continue
                        inc=parse_date(row.get("IncorporationDate"))
                        if not inc or inc>cutoff:
                            counts["reject_age_or_missing"]+=1; continue
                        codes=sic_codes(row)
                        disp,matches=disposition(codes)
                        if not disp:
                            counts["reject_sector"]+=1; continue
                        for c in codes: sic_counts[c]+=1
                        kept+=1; counts["kept"]+=1; counts[f"kept_{disp.lower()}"]+=1
                        record={
                            "company_number":(row.get("CompanyNumber") or "").strip(),
                            "company_name":(row.get("CompanyName") or "").strip(),
                            "company_status":status,
                            "company_type":(row.get("CompanyCategory") or "").strip(),
                            "incorporation_date":inc.isoformat(),
                            "sic_codes":codes,
                            "registered_postcode":(row.get("RegAddress.PostCode") or "").strip(),
                            "region":(row.get("RegAddress.County") or row.get("RegAddress.Country") or "").strip(),
                            "uri":(row.get("URI") or "").strip(),
                        }
                        batch.append(record)
                        if len(batch)>=BATCH_SIZE: flush_batch()
                        w.writerow({
                            **record,
                            "sic_codes":"|".join(codes),
                            "matched_rules":"|".join(f"{p}:{d}" for p,d in matches),
                            "disposition":disp,
                            "snapshot_date":snapshot,
                        })
            flush_batch()
            part_counts[filename]={"seen":seen,"kept":kept}
            zpath.unlink(missing_ok=True)
            print(f"[{idx}/{len(parts)}] seen={seen:,} kept={kept:,} uploaded={counts['uploaded']:,}",flush=True)

    flush_batch()
    final=post_json({"action":"finalize","ingest_run_id":ingest_run_id})
    summary={
        "snapshot_date":snapshot,
        "generated_at_utc":datetime.utcnow().isoformat()+"Z",
        "min_age_years":MIN_AGE_YEARS,
        "cutoff_incorporation_date":cutoff.isoformat(),
        "sector_prefixes":PREFIXES,
        "counts":dict(counts),
        "parts":part_counts,
        "top_sic_codes":sic_counts.most_common(50),
        "supabase_finalize":final,
        "output_file":str(out_csv),
    }
    (OUT/"summary.json").write_text(json.dumps(summary,indent=2),encoding="utf-8")
    print(json.dumps(summary,indent=2),flush=True)

if __name__=="__main__":
    main()

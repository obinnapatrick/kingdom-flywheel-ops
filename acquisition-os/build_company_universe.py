#!/usr/bin/env python3
import csv, io, json, os, re, sys, urllib.request, zipfile
from collections import Counter
from datetime import datetime
from pathlib import Path

INDEX = "https://download.companieshouse.gov.uk/"
OUT = Path("out")
OUT.mkdir(exist_ok=True)

# Mirrors acq.sector_rules V1. Broad wholesale prefix 46 is retained but tagged REVIEW.
PREFIXES = {
    "71200":"PRIORITY","43210":"PRIORITY","43220":"PRIORITY","43290":"ALLOW",
    "33120":"PRIORITY","33140":"PRIORITY","33190":"ALLOW","80200":"PRIORITY",
    "81100":"PRIORITY","62020":"REVIEW","62030":"PRIORITY","62090":"REVIEW",
    "46":"REVIEW",
}
MIN_AGE_YEARS = 5

def get(url, target=None):
    req = urllib.request.Request(url, headers={"User-Agent":"KingdomFlywheelAcquisitionOS/1.0"})
    with urllib.request.urlopen(req, timeout=120) as r:
        if target:
            with open(target, "wb") as f:
                while True:
                    chunk = r.read(1024*1024)
                    if not chunk: break
                    f.write(chunk)
            return None
        return r.read().decode("utf-8", errors="replace")

def latest_parts():
    html = get(INDEX)
    pat = re.compile(r'BasicCompanyData-(\d{4}-\d{2}-\d{2})-part(\d+)_(\d+)\.zip')
    hits = [(m.group(1), int(m.group(2)), int(m.group(3)), m.group(0)) for m in pat.finditer(html)]
    if not hits:
        raise RuntimeError("Could not discover Companies House split snapshot files")
    latest = max(x[0] for x in hits)
    parts = sorted({(p,n,f) for d,p,n,f in hits if d == latest})
    expected = max(n for p,n,f in parts)
    if len(parts) != expected:
        raise RuntimeError(f"Expected {expected} parts for {latest}, discovered {len(parts)}")
    return latest, [f for _,_,f in parts]

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
        m=re.match(r"(\d{2,5})", raw)
        if m: out.append(m.group(1))
    return out

def disposition(codes):
    matches=[]
    for code in codes:
        for pref, disp in PREFIXES.items():
            if code.startswith(pref):
                matches.append((pref,disp))
    if not matches: return None, []
    rank={"PRIORITY":3,"ALLOW":2,"REVIEW":1}
    best=max(matches,key=lambda x:rank[x[1]])[1]
    return best, matches

def main():
    snapshot, parts = latest_parts()
    snapshot_date=datetime.strptime(snapshot,"%Y-%m-%d").date()
    cutoff=snapshot_date.replace(year=snapshot_date.year-MIN_AGE_YEARS)
    out_csv=OUT/f"companies_house_candidates_{snapshot}.csv"
    counts=Counter(); sic_counts=Counter(); part_counts={}
    fields=["company_number","company_name","company_status","company_type","incorporation_date",
            "sic_codes","matched_rules","disposition","registered_postcode","region","uri","snapshot_date"]
    with open(out_csv,"w",newline="",encoding="utf-8") as fo:
        w=csv.DictWriter(fo,fieldnames=fields); w.writeheader()
        for idx,filename in enumerate(parts,1):
            zpath=OUT/filename
            print(f"[{idx}/{len(parts)}] downloading {filename}", flush=True)
            get(INDEX+filename,zpath)
            kept=seen=0
            with zipfile.ZipFile(zpath) as zf:
                names=[n for n in zf.namelist() if n.lower().endswith(".csv")]
                if not names: raise RuntimeError(f"No CSV inside {filename}")
                with zf.open(names[0]) as raw, io.TextIOWrapper(raw,encoding="utf-8-sig",errors="replace",newline="") as text:
                    reader=csv.DictReader(text)
                    for row in reader:
                        seen += 1; counts["rows_seen"] += 1
                        status=(row.get("CompanyStatus") or "").strip()
                        if status.lower() != "active":
                            counts["reject_status"] += 1; continue
                        inc=parse_date(row.get("IncorporationDate"))
                        if not inc or inc > cutoff:
                            counts["reject_age_or_missing"] += 1; continue
                        codes=sic_codes(row)
                        disp,matches=disposition(codes)
                        if not disp:
                            counts["reject_sector"] += 1; continue
                        for c in codes: sic_counts[c] += 1
                        kept += 1; counts["kept"] += 1; counts[f"kept_{disp.lower()}"] += 1
                        w.writerow({
                            "company_number":(row.get("CompanyNumber") or "").strip(),
                            "company_name":(row.get("CompanyName") or "").strip(),
                            "company_status":status,
                            "company_type":(row.get("CompanyCategory") or "").strip(),
                            "incorporation_date":inc.isoformat(),
                            "sic_codes":"|".join(codes),
                            "matched_rules":"|".join(f"{p}:{d}" for p,d in matches),
                            "disposition":disp,
                            "registered_postcode":(row.get("RegAddress.PostCode") or "").strip(),
                            "region":(row.get("RegAddress.County") or row.get("RegAddress.Country") or "").strip(),
                            "uri":(row.get("URI") or "").strip(),
                            "snapshot_date":snapshot,
                        })
            part_counts[filename]={"seen":seen,"kept":kept}
            zpath.unlink(missing_ok=True)
            print(f"[{idx}/{len(parts)}] seen={seen:,} kept={kept:,}", flush=True)
    summary={
        "snapshot_date":snapshot,
        "generated_at_utc":datetime.utcnow().isoformat()+"Z",
        "min_age_years":MIN_AGE_YEARS,
        "cutoff_incorporation_date":cutoff.isoformat(),
        "sector_prefixes":PREFIXES,
        "counts":dict(counts),
        "parts":part_counts,
        "top_sic_codes":sic_counts.most_common(50),
        "output_file":str(out_csv),
    }
    (OUT/"summary.json").write_text(json.dumps(summary,indent=2),encoding="utf-8")
    print(json.dumps(summary["counts"],indent=2), flush=True)

if __name__=="__main__":
    main()

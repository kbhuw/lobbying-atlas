"""Export filings-detail sqlite (from parse_house_xml.py) into site shards.

Outputs under public/data/lobbying/:
  index.json.gz                 — years, counts, issue index, top firms
  filings/{xx}.json.gz          — full filing detail, sharded by md5(doc_id)[:2]
  issues/{CODE}-{year}.json.gz  — per issue code + year org leaderboard
  firms/{registrant_id}.json.gz — per-firm rollup (clients, spend, issues)
  orgs/{key}.json.gz            — per-organization rollup (group_id or c<client_id>)

Periods: LD-2 filing types Q1..Q4, {n}A amendments, {n}T terminations all
collapse to quarter period Q{n}; LD-1 registrations get period 'Registration'.
Amounts count once per (client, registrant, year, period) — latest posted doc.
Run after parse_house_xml.py and build_entity_map.py.
Usage: python3 build_lobbying_index.py <db_path> <repo_root> <out_dir>
"""
import gzip, hashlib, json, re, sqlite3, sys, unicodedata
from collections import defaultdict
from pathlib import Path

ISSUE_CODES = json.loads((Path(__file__).parent / "issue-codes.json").read_text())
if isinstance(ISSUE_CODES, list):
    ISSUE_CODES = {c.get("code") or c["value"]: c["name"] for c in ISSUE_CODES}


def money(v):
    try:
        return float(v) if v not in (None, "") else None
    except ValueError:
        return None


def wjson(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(gzip.compress(json.dumps(obj, separators=(",", ":")).encode(), 9))


def period_of(form, ftype):
    if form == "LD-1" or not ftype:
        return "Registration"
    m = re.match(r"([1-4])", ftype)
    return f"Q{m.group(1)}" if m else ftype


def type_label(form, ftype):
    if form == "LD-1" or ftype in ("1", "2", "3"):
        return "Registration"
    m = re.match(r"([1-4])(A|T)?$", ftype or "")
    if not m:
        return ftype or form
    q = f"Q{m.group(1)}"
    return {"A": f"Amended {q}", "T": f"Termination ({q})"}.get(m.group(2) or "", f"{q} report")


def norm(s):
    s = unicodedata.normalize("NFKC", s or "").upper().replace("&", " AND ")
    s = re.sub(r"[.\u2019']", "", s)
    s = re.sub(r"[^\w ]", " ", s, flags=re.UNICODE)
    return " ".join(s.split())


def org_key(group_id, client_name):
    return group_id or "n" + hashlib.sha1(norm(client_name).encode()).hexdigest()[:16]


def split_agencies(s):
    if not s:
        return []
    return [p.strip() for p in re.split(r"[;\n]", s) if p.strip()]


def main():
    db_path = Path(sys.argv[1])
    repo = Path(sys.argv[2])
    out = Path(sys.argv[3])
    db = sqlite3.connect(db_path)
    db.row_factory = sqlite3.Row
    emap = json.loads((db_path.parent / "entity-map.json").read_text())

    filings = {}
    for f in db.execute("SELECT * FROM filings"):
        d = dict(f)
        d["group_id"] = emap.get(norm(d["client_name"]), {}).get("group_id")
        filings[d["doc_id"]] = d

    acts = defaultdict(list)
    for a in db.execute("SELECT * FROM activities"):
        acts[a["doc_id"]].append(dict(a))
    lobs = defaultdict(list)
    for l in db.execute("SELECT * FROM lobbyists"):
        lobs[(l["doc_id"], l["activity_idx"])].append({
            "name": f'{l["first_name"] or ""} {l["last_name"] or ""} {l["suffix"] or ""}'.strip(),
            "covered_position": l["covered_position"], "new": (l["new"] or "") == "Y"})

    # Latest version per (client name, firm, year, period).
    latest = {}
    for uuid, f in filings.items():
        year = f["filing_year"] or int((f["dt_posted"] or "0000")[:4] or 0)
        key = (norm(f["client_name"]), f["registrant_id"], year, period_of(f["form"], f["filing_type"]))
        cur = latest.get(key)
        if cur is None or (f["dt_posted"] or "") > (filings[cur]["dt_posted"] or ""):
            latest[key] = uuid
    latest_uuids = set(latest.values())

    shards = defaultdict(list)
    firm = defaultdict(lambda: {"clients": defaultdict(lambda: {"amount": 0.0, "filings": 0, "issues": set()}),
                                "issues": defaultdict(float), "total": 0.0, "filings": 0})
    org = defaultdict(lambda: {"amount": 0.0, "filings": 0, "issues": defaultdict(float),
                               "firms": defaultdict(lambda: {"amount": 0.0, "filings": 0}),
                               "years": set(), "sample_texts": set(), "filing_ids": [],
                               "lobbyists": set()})

    n_act = 0
    for uuid, f in filings.items():
        is_latest = uuid in latest_uuids
        amt = (money(f["income"]) or money(f["expenses"])) if is_latest else None
        year = f["filing_year"] or int((f["dt_posted"] or "0000")[:4] or 0)
        fa = []
        for a in sorted(acts.get(uuid, []), key=lambda x: x["idx"]):
            i = a["idx"]
            if not a["issue_code"]:
                continue
            fa.append({"code": a["issue_code"], "issue": ISSUE_CODES.get(a["issue_code"], a["issue_code"]),
                       "text": a["description"], "agencies": split_agencies(a["agencies"]),
                       "lobbyists": lobs.get((uuid, i), [])})
            n_act += 1
        shard = hashlib.md5(uuid.encode()).hexdigest()[:2]
        shards[shard].append({
            "id": uuid, "senate_id": f["senate_id"], "form": f["form"],
            "group_id": f["group_id"],
            "client": f["client_name"], "firm_id": f["registrant_id"],
            "firm": f["registrant_name"], "kind": type_label(f["form"], f["filing_type"]),
            "year": year, "period": period_of(f["form"], f["filing_type"]),
            "amount": amt, "income": money(f["income"]), "expenses": money(f["expenses"]),
            "posted": f["dt_posted"], "terminated": f["termination_date"],
            "latest": is_latest, "activities": fa})

        fr = firm[f["registrant_id"]]
        fr["name"] = f["registrant_name"] or f'Registrant {f["registrant_id"]}'
        fr["filings"] += 1
        ckey = org_key(f["group_id"], f["client_name"])
        c = fr["clients"][ckey]
        c["name"] = f["client_name"]
        c["filings"] += 1
        if amt:
            fr["total"] += amt
            c["amount"] += amt
        for a in fa:
            c["issues"].add(a["code"])
            if amt:
                fr["issues"][a["code"]] += amt

        okey = org_key(f["group_id"], f["client_name"])
        o = org[okey]
        o["name"] = f["client_name"]
        o["group_id"] = f["group_id"]
        o["filings"] += 1
        o["filing_ids"].append(uuid)
        if year:
            o["years"].add(year)
        if amt:
            o["amount"] += amt
            if f["registrant_id"]:
                rf = o["firms"][f["registrant_id"]]
                rf["name"] = f["registrant_name"]
                rf["amount"] += amt
                rf["filings"] += 1
        for a in fa:
            if amt:
                o["issues"][a["code"]] += amt
            if a["text"] and len(o["sample_texts"]) < 5:
                o["sample_texts"].add(a["text"][:240])
            for l in a["lobbyists"]:
                if len(o["lobbyists"]) < 25:
                    o["lobbyists"].add(l["name"])

    for pre, rows in shards.items():
        wjson(out / "filings" / f"{pre}.json.gz", rows)

    issue_index = {}
    iy = defaultdict(lambda: defaultdict(lambda: {"amount": 0.0, "filings": 0}))
    for uuid, f in filings.items():
        if uuid not in latest_uuids:
            continue
        amt = money(f["income"]) or money(f["expenses"])
        year = f["filing_year"] or int((f["dt_posted"] or "0000")[:4] or 0)
        for a in acts.get(uuid, []):
            if a["issue_code"]:
                key = org_key(f["group_id"], f["client_name"])
                e = iy[(a["issue_code"], year)][key]
                e["name"] = f["client_name"]
                e["filings"] += 1
                if amt:
                    e["amount"] += amt
    for (code, year), clients in iy.items():
        rows = sorted(({"id": k, "name": v["name"], "amount": round(v["amount"], 2) or None,
                        "filings": v["filings"]} for k, v in clients.items()),
                      key=lambda r: -(r["amount"] or 0))
        wjson(out / "issues" / f"{code}-{year}.json.gz",
              {"code": code, "name": ISSUE_CODES.get(code, code), "year": year, "organizations": rows})
        issue_index.setdefault(code, {})[str(year)] = {
            "organizations": len(rows),
            "amount": round(sum(v["amount"] for v in clients.values()), 2)}

    for rid, fr in firm.items():
        if rid is None:
            continue
        wjson(out / "firms" / f"{rid}.json.gz", {
            "id": rid, "name": fr["name"], "total": round(fr["total"], 2),
            "filings": fr["filings"],
            "clients": sorted(({"key": k, "name": v["name"],
                                "amount": round(v["amount"], 2), "filings": v["filings"],
                                "issues": sorted(v["issues"])}
                               for k, v in fr["clients"].items()),
                              key=lambda r: -r["amount"]),
            "issues": {k: round(v, 2) for k, v in sorted(fr["issues"].items(), key=lambda x: -x[1])}})

    for okey, o in org.items():
        wjson(out / "orgs" / f"{okey}.json.gz", {
            "id": okey, "group_id": o["group_id"],
            "name": o["name"], "total": round(o["amount"], 2), "filings": o["filings"],
            "years": sorted(o["years"]),
            "issues": {k: round(v, 2) for k, v in sorted(o["issues"].items(), key=lambda x: -x[1])},
            "firms": sorted(({"firm_id": k, "name": v["name"],
                              "amount": round(v["amount"], 2), "filings": v["filings"]}
                             for k, v in o["firms"].items()), key=lambda r: -r["amount"]),
            "lobbyists": sorted(o["lobbyists"]),
            "filing_ids": sorted(o["filing_ids"]),
            "sample_texts": sorted(o["sample_texts"])})

    wjson(out / "index.json.gz", {
        "years": sorted({f["filing_year"] or int((f["dt_posted"] or "0")[:4] or 0) for f in filings.values()} - {0, None}),
        "filings": len(filings), "activities": n_act,
        "clients": len(org), "firms": len(firm),
        "top_firms": sorted(({"id": rid, "name": fr["name"], "total": round(fr["total"], 2),
                              "filings": fr["filings"], "clients": len(fr["clients"])}
                             for rid, fr in firm.items() if rid),
                            key=lambda r: -r["total"]),
        "issue_codes": ISSUE_CODES, "issue_index": issue_index})
    print(json.dumps({"filings": len(filings), "activities": n_act,
                      "orgs": len(org), "firms": len(firm),
                      "shards": len(shards), "issue_years": len(iy)}))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Extract disclosed organization descriptions from House bulk XML archives.

The extractor is archive-resumable: a ZIP is marked complete only after all of
its members have been parsed and committed.  It intentionally stores
observations rather than inferred/current profiles.
"""
from __future__ import annotations

import argparse, datetime as dt, gzip, hashlib, json, os, pathlib, re, sqlite3, zipfile
from xml.etree import ElementTree as ET

HERE = pathlib.Path(__file__).resolve()
PROJECT = HERE.parents[2]
ROOT = pathlib.Path(os.environ.get("LOBBYING_DATA_DIR", str(PROJECT.parent / "work" / "federal-directory")))
RAW = ROOT / "raw"
OUT = pathlib.Path(os.environ.get("LOBBYING_RESEARCH_DIR", str(PROJECT.parent / "work" / "organization-research")))
DB_PATH = pathlib.Path(os.environ.get("BULK_PROFILES_DB", str(OUT / "bulk-profiles.sqlite")))
PARSER_VERSION = "2026-09-04-v3"
PROGRESS_PATH = OUT / "bulk-progress.json"

WS = re.compile(r"\s+")
def clean(v):
    if v is None: return None
    v = WS.sub(" ", v).strip()
    return v or None
def tag(root, name):
    x = root.find(".//" + name)
    return clean(x.text if x is not None else None)
def norm(s):
    return WS.sub(" ", re.sub(r"[^a-z0-9]+", " ", (s or "").lower())).strip()
def date_val(s):
    return clean(s)

def schema(c):
    c.executescript("""
    PRAGMA journal_mode=WAL;
    CREATE TABLE IF NOT EXISTS organizations (
      organization_key TEXT PRIMARY KEY, name TEXT NOT NULL,
      first_seen TEXT, last_seen TEXT, observation_count INTEGER NOT NULL DEFAULT 0
    );
    CREATE TABLE IF NOT EXISTS descriptions (
      id INTEGER PRIMARY KEY AUTOINCREMENT, organization_key TEXT NOT NULL,
      name TEXT NOT NULL, description TEXT NOT NULL, source_field TEXT NOT NULL,
      form_type TEXT NOT NULL, source_zip TEXT NOT NULL, source_member TEXT NOT NULL,
      filing_id TEXT, report_year TEXT, report_type TEXT, effective_date TEXT,
      signed_date TEXT, reporting_date TEXT, state TEXT, city TEXT, country TEXT,
      principal_state TEXT, principal_city TEXT, principal_country TEXT,
      government_flag TEXT, self_select TEXT, source_url TEXT, extracted_at TEXT NOT NULL,
      UNIQUE(source_zip, source_member, source_field, organization_key, description)
    );
    CREATE TABLE IF NOT EXISTS errors (
      id INTEGER PRIMARY KEY AUTOINCREMENT, source_zip TEXT NOT NULL,
      source_member TEXT, error_type TEXT NOT NULL, error_message TEXT NOT NULL,
      recorded_at TEXT NOT NULL
    );
    CREATE TABLE IF NOT EXISTS archive_state (
      source_zip TEXT PRIMARY KEY, status TEXT NOT NULL, members INTEGER,
      descriptions INTEGER DEFAULT 0, errors INTEGER DEFAULT 0,
      completed_at TEXT, last_member TEXT, parser_version TEXT
    );
    CREATE INDEX IF NOT EXISTS descriptions_name ON descriptions(organization_key);
    CREATE INDEX IF NOT EXISTS descriptions_source ON descriptions(source_zip);
    """)
    cols = {r[1] for r in c.execute("PRAGMA table_info(descriptions)")}
    if "source_url" not in cols:
        c.execute("ALTER TABLE descriptions ADD COLUMN source_url TEXT")
    for col in ("principal_state", "principal_city", "principal_country"):
        if col not in cols: c.execute("ALTER TABLE descriptions ADD COLUMN " + col + " TEXT")
    if "parser_version" not in {r[1] for r in c.execute("PRAGMA table_info(archive_state)")}: c.execute("ALTER TABLE archive_state ADD COLUMN parser_version TEXT")
    c.execute("UPDATE descriptions SET source_url='https://disclosurespreview.house.gov/data/LD/' || source_zip WHERE source_url IS NULL")

def parse_member(raw, archive, member, now):
    root = ET.fromstring(raw)
    form = root.tag.upper()
    is_ld1 = "DISCLOSURE1" in form
    is_ld2 = "DISCLOSURE2" in form
    if not (is_ld1 or is_ld2): return []
    org = tag(root, "organizationName")
    client = tag(root, "clientName")
    self_select = (tag(root, "selfSelect") or "").upper()
    # A self-select registration represents the organization itself.  Prefer
    # the client description when present, then the registrant description.
    if is_ld1:
        name = client or (org if self_select in {"Y", "YES", "TRUE", "1"} else None)
        if not name: return []
        fields = []
        client_desc = tag(root, "clientGeneralDescription")
        registrant_desc = tag(root, "registrantGeneralDescription")
        # Prefer the client description. A self-select registrant description
        # is a fallback only when it is the same disclosed organization.
        if client_desc:
            fields.append(("clientGeneralDescription", client_desc))
        elif registrant_desc and self_select in {"Y", "YES", "TRUE", "1"} and norm(org) == norm(client):
            fields.append(("registrantGeneralDescription", registrant_desc))
        else: fields.append(("clientGeneralDescription", ""))
        city, state, country = tag(root, "clientCity"), tag(root, "clientState"), tag(root, "clientCountry")
        government = tag(root, "clientGovtEntity")
        if self_select in {"Y", "YES", "TRUE", "1"}:
            city, state, country = city or tag(root, "city"), state or tag(root, "state"), country or tag(root, "country")
        common = ("LD1", tag(root, "houseID"), tag(root, "reportYear"), tag(root, "reportType"), tag(root, "effectiveDate"), tag(root, "signedDate"), None, state, city, country, tag(root, "principal_state"), tag(root, "principal_city"), tag(root, "principal_country"), government, self_select)
    else:
        name = client
        if not name: return []
        desc = tag(root, "generalDescription")
        if not desc:
            x = root.find(".//updates/generalDescription")
            desc = clean(x.text if x is not None else None)
        # Blank updates are retained as observations so location and filing
        # provenance can still be joined by downstream identity matching.
        fields = [("updates.generalDescription", desc or "")]
        common = ("LD2", tag(root, "houseID"), tag(root, "reportYear"), tag(root, "reportType"), None, tag(root, "signedDate"), None, tag(root, "clientState"), tag(root, "clientCity"), tag(root, "clientCountry"), tag(root, "prinClientState"), tag(root, "prinClientCity"), tag(root, "prinClientCountry"), tag(root, "clientGovtEntity"), self_select)
    key = norm(name)
    if not key: return []
    return [(key, name, description, field, *common) for field, description in fields]

def write_progress(c, started=None):
    rows = c.execute("SELECT status,count(*) FROM archive_state GROUP BY status").fetchall()
    counts = dict(rows)
    aliases = set(); company_ids = set(); alias_company = {}
    directory = PROJECT / "public" / "data" / "directory-v2.json.gz"
    if directory.exists():
        try:
            data = json.loads(gzip.open(directory, "rt", encoding="utf-8").read())
            for g in data.get("companies", []):
                cid = str(g.get("id", "")); company_ids.add(cid)
                for a in g.get("aliases", []): aliases.add(norm(a)); alias_company[norm(a)] = cid
        except Exception as e:
            c.execute("INSERT INTO errors(source_zip,error_type,error_message,recorded_at) VALUES(?,?,?,?)",("directory-v2.json.gz","coverage",str(e),dt.datetime.now(dt.timezone.utc).isoformat()))
    names = {r[0] for r in c.execute("SELECT DISTINCT organization_key FROM descriptions WHERE trim(description)<>''")}
    matched = len(names & aliases) if aliases else None
    disclosed_ids = {str(r[0]) for r in c.execute("SELECT DISTINCT organization_key FROM descriptions WHERE trim(description)<>''")}
    id_matched = len({alias_company[n] for n in names & aliases if n in alias_company}) if company_ids else None
    out = {"updated_at": dt.datetime.now(dt.timezone.utc).isoformat(), "database": str(DB_PATH), "archives": counts,
           "descriptions": c.execute("SELECT count(*) FROM descriptions WHERE trim(description)<>''").fetchone()[0],
           "observations": c.execute("SELECT count(*) FROM descriptions").fetchone()[0],
           "organizations_with_descriptions": len(names), "errors": c.execute("SELECT count(*) FROM errors").fetchone()[0],
           "directory_alias_count": len(aliases) if aliases else None, "directory_company_id_count": len(company_ids) if company_ids else None,
           "exact_normalized_name_coverage": {"matched": matched, "eligible": len(names), "percent": (100*matched/len(names) if matched is not None and names else None)},
           "directory_company_id_coverage": {"matched": id_matched, "eligible": len(company_ids), "percent": (100*id_matched/len(company_ids) if id_matched is not None and company_ids else None)}}
    tmp = PROGRESS_PATH.with_suffix(".tmp")
    tmp.write_text(json.dumps(out, indent=2) + "\n")
    tmp.replace(PROGRESS_PATH)

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--reports", action="store_true", help="include LD2 report archives after registrations")
    ap.add_argument("--all", action="store_true", help="include registrations and reports")
    args = ap.parse_args(); OUT.mkdir(parents=True, exist_ok=True)
    c = sqlite3.connect(DB_PATH); schema(c)
    files = sorted(RAW.glob("*.zip"))
    selected = [p for p in files if "Registrations_XML" in p.name]
    if args.reports or args.all: selected += [p for p in files if p not in selected]
    for path in selected:
        already = c.execute("SELECT status FROM archive_state WHERE source_zip=?", (path.name,)).fetchone()
        if already and already[0] == "complete":
            pv = c.execute("SELECT parser_version FROM archive_state WHERE source_zip=?", (path.name,)).fetchone()[0]
            if pv == PARSER_VERSION: continue
        try:
            with zipfile.ZipFile(path) as z:
                members = [n for n in z.namelist() if n.lower().endswith(".xml")]
                c.execute("INSERT INTO archive_state(source_zip,status,members,parser_version) VALUES(?,?,?,?) ON CONFLICT(source_zip) DO UPDATE SET status='running',members=excluded.members,parser_version=excluded.parser_version", (path.name,"running",len(members),PARSER_VERSION)); c.commit()
                made = 0
                processed_members = 0
                for member in members:
                    try:
                        rows = parse_member(z.read(member), path.name, member, dt.datetime.now(dt.timezone.utc).isoformat())
                        for row in rows:
                            key,name,desc,field,form,fid,year,rtype,effective,signed,reporting,state,city,country,pstate,pcity,pcountry,gov,selfsel = row
                            c.execute("INSERT INTO organizations(organization_key,name,first_seen,last_seen,observation_count) VALUES(?,?,?,?,1) ON CONFLICT(organization_key) DO UPDATE SET last_seen=excluded.last_seen,observation_count=observation_count+1",(key,name,signed or effective,signed or effective))
                            meta = path.with_name(path.name + ".meta.json")
                            source_url = None
                            if meta.exists():
                                try: source_url = json.loads(meta.read_text()).get("url")
                                except Exception: pass
                            source_url = source_url or "https://disclosurespreview.house.gov/data/LD/" + path.name
                            c.execute("INSERT OR IGNORE INTO descriptions(organization_key,name,description,source_field,form_type,source_zip,source_member,filing_id,report_year,report_type,effective_date,signed_date,reporting_date,state,city,country,principal_state,principal_city,principal_country,government_flag,self_select,source_url,extracted_at) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",(key,name,desc,field,form, path.name,member,fid,year,rtype,effective,signed,reporting,state,city,country,pstate,pcity,pcountry,gov,selfsel,source_url,dt.datetime.now(dt.timezone.utc).isoformat()))
                            made += c.execute("SELECT changes()").fetchone()[0]
                        processed_members += 1
                        if processed_members % 500 == 0 or processed_members == len(members):
                            c.execute("UPDATE archive_state SET last_member=?,descriptions=descriptions+? WHERE source_zip=?",(member,made,path.name)); c.commit(); made=0
                    except Exception as e:
                        c.execute("INSERT INTO errors(source_zip,source_member,error_type,error_message,recorded_at) VALUES(?,?,?,?,?)",(path.name,member,type(e).__name__,str(e),dt.datetime.now(dt.timezone.utc).isoformat()))
                        c.execute("UPDATE archive_state SET errors=errors+1,last_member=? WHERE source_zip=?",(member,path.name)); c.commit()
                c.execute("UPDATE archive_state SET status='complete',completed_at=?,parser_version=? WHERE source_zip=?",(dt.datetime.now(dt.timezone.utc).isoformat(),PARSER_VERSION,path.name)); c.commit()
            write_progress(c); print(path.name, "complete")
        except Exception as e:
            c.execute("INSERT OR REPLACE INTO archive_state(source_zip,status,members,completed_at) VALUES(?,?,?,?)",(path.name,"error",None,None)); c.execute("INSERT INTO errors(source_zip,error_type,error_message,recorded_at) VALUES(?,?,?,?)",(path.name,type(e).__name__,str(e),dt.datetime.now(dt.timezone.utc).isoformat())); c.commit(); write_progress(c); print(path.name,"ERROR",e)
    write_progress(c); c.close()
if __name__ == "__main__": main()

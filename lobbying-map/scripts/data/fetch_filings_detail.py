"""Fetch full LDA filing detail (lobbying activities, lobbyists, government
entities, client/registrant canonical IDs) for a year range into sqlite.

Resumable: progress is checkpointed per (year, page) in the meta table.
Source: https://lda.gov/api/v1/filings/ — the list endpoint returns full nested
detail, so no per-filing detail calls are needed.

Usage: python3 fetch_filings_detail.py [start_year] [end_year] [db_path]
"""
import json, sqlite3, sys, time, urllib.parse, urllib.request

API = "https://lda.gov/api/v1/filings/"
PAGE_SIZE = 500
DELAY = 3.0

SCHEMA = """
CREATE TABLE IF NOT EXISTS filings(
  filing_uuid TEXT PRIMARY KEY,
  filing_type TEXT, filing_type_display TEXT,
  filing_year INTEGER, filing_period TEXT,
  income TEXT, expenses TEXT, expenses_method TEXT,
  dt_posted TEXT, termination_date TEXT, posted_by_name TEXT,
  client_id INTEGER, client_name TEXT, client_state TEXT,
  client_country TEXT, client_description TEXT, client_self_select INTEGER,
  registrant_id INTEGER, registrant_name TEXT, registrant_description TEXT,
  registrant_country TEXT,
  n_lobbying_activities INTEGER, n_affiliated INTEGER, n_foreign INTEGER,
  n_convictions INTEGER,
  document_url TEXT
);
CREATE TABLE IF NOT EXISTS activities(
  filing_uuid TEXT, idx INTEGER,
  issue_code TEXT, issue_code_display TEXT, description TEXT,
  foreign_entity_issues TEXT,
  PRIMARY KEY(filing_uuid, idx)
);
CREATE TABLE IF NOT EXISTS lobbyists(
  filing_uuid TEXT, activity_idx INTEGER, lobbyist_id INTEGER,
  first_name TEXT, last_name TEXT, covered_position TEXT, new INTEGER,
  PRIMARY KEY(filing_uuid, activity_idx, lobbyist_id)
);
CREATE TABLE IF NOT EXISTS gov_entities(
  filing_uuid TEXT, activity_idx INTEGER, entity_id INTEGER, name TEXT,
  PRIMARY KEY(filing_uuid, activity_idx, entity_id)
);
CREATE TABLE IF NOT EXISTS meta(key TEXT PRIMARY KEY, value TEXT);
"""


def fetch(url):
    for attempt in range(6):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "lobbying-atlas research"})
            with urllib.request.urlopen(req, timeout=90) as r:
                return json.load(r)
        except Exception as e:
            wait = min(90, 10 + attempt * 15)
            print(f"  retry {attempt + 1} after {type(e).__name__}: {e} (sleep {wait}s)", flush=True)
            time.sleep(wait)
    raise RuntimeError(f"page failed permanently: {url}")


def insert_filing(db, f):
    acts = f.get("lobbying_activities") or []
    c = f.get("client") or {}
    r = f.get("registrant") or {}
    db.execute(
        """INSERT OR REPLACE INTO filings VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
        (
            f["filing_uuid"], f.get("filing_type"), f.get("filing_type_display"),
            f.get("filing_year"), f.get("filing_period"), f.get("income"),
            f.get("expenses"), f.get("expenses_method"), f.get("dt_posted"),
            f.get("termination_date"), f.get("posted_by_name"),
            c.get("id"), c.get("name"), c.get("state"), c.get("country"),
            c.get("general_description"), int(bool(c.get("client_self_select"))),
            r.get("id"), r.get("name"), r.get("description"), r.get("country"),
            len(acts), len(f.get("affiliated_organizations") or []),
            len(f.get("foreign_entities") or []), len(f.get("conviction_disclosures") or []),
            f.get("filing_document_url"),
        ),
    )
    db.execute("DELETE FROM activities WHERE filing_uuid=?", (f["filing_uuid"],))
    db.execute("DELETE FROM lobbyists WHERE filing_uuid=?", (f["filing_uuid"],))
    db.execute("DELETE FROM gov_entities WHERE filing_uuid=?", (f["filing_uuid"],))
    for i, a in enumerate(acts):
        db.execute(
            "INSERT OR REPLACE INTO activities VALUES(?,?,?,?,?,?)",
            (f["filing_uuid"], i, a.get("general_issue_code"),
             a.get("general_issue_code_display"), a.get("description"),
             a.get("foreign_entity_issues")),
        )
        for lb in a.get("lobbyists") or []:
            L = lb.get("lobbyist") or {}
            db.execute(
                "INSERT OR REPLACE INTO lobbyists VALUES(?,?,?,?,?,?,?)",
                (f["filing_uuid"], i, L.get("id"), L.get("first_name"),
                 L.get("last_name"), lb.get("covered_position"), int(bool(lb.get("new")))),
            )
        for ge in a.get("government_entities") or []:
            db.execute(
                "INSERT OR REPLACE INTO gov_entities VALUES(?,?,?,?)",
                (f["filing_uuid"], i, ge.get("id"), ge.get("name")),
            )


def main():
    start = int(sys.argv[1]) if len(sys.argv) > 1 else 2024
    end = int(sys.argv[2]) if len(sys.argv) > 2 else 2026
    db_path = sys.argv[3] if len(sys.argv) > 3 else "filings-detail.sqlite"
    db = sqlite3.connect(db_path)
    db.executescript(SCHEMA)
    for year in range(start, end + 1):
        row = db.execute("SELECT value FROM meta WHERE key=?", (f"page:{year}",)).fetchone()
        page = int(row[0]) if row else 0
        total = None
        while True:
            page += 1
            q = urllib.parse.urlencode({
                "filing_year": year, "page_size": PAGE_SIZE,
                "page": page, "format": "json", "ordering": "dt_posted",
            })
            d = fetch(API + "?" + q)
            total = d["count"]
            for f in d["results"]:
                insert_filing(db, f)
            db.execute("INSERT OR REPLACE INTO meta VALUES(?,?)", (f"page:{year}", str(page)))
            db.commit()
            if page % 10 == 0 or page == 1:
                pages = (total + PAGE_SIZE - 1) // PAGE_SIZE
                print(f"{year} page {page}/{pages} ({total} filings)", flush=True)
            if not d.get("next"):
                break
            time.sleep(DELAY)
        db.execute("INSERT OR REPLACE INTO meta VALUES(?,?)", (f"done:{year}", "1"))
        db.commit()
        print(f"{year} DONE — {total} filings", flush=True)
    print("ALL DONE", flush=True)


if __name__ == "__main__":
    main()

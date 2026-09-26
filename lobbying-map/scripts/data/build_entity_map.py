"""Map LDA filing client names to directory name groups.

The House bulk XML does not expose canonical client ids — senateID is
'<registrant_senate_id>-<document_sequence>'. Client identity is therefore
the normalized client name, matched against directory group aliases with the
same normalization used by lib/directory.ts.

Emits work/filings-detail/entity-map.json:
  { norm_name: {name, group_id, match: "exact_alias"|"ambiguous", filings} }
plus entity-map-report.json for triage of unmatched/ambiguous names.

Usage: python3 build_entity_map.py <db_path> <repo_root>
"""
import gzip, json, re, sqlite3, sys, unicodedata
from pathlib import Path


def norm(s: str) -> str:
    s = unicodedata.normalize("NFKC", s or "").upper().replace("&", " AND ")
    s = re.sub(r"[.\u2019']", "", s)
    s = re.sub(r"[^\w ]", " ", s, flags=re.UNICODE)
    return " ".join(s.split())


def main():
    db_path = sys.argv[1] if len(sys.argv) > 1 else "work/filings-detail/filings-2024-2026.sqlite"
    repo = Path(sys.argv[2]) if len(sys.argv) > 2 else Path(".")
    base = json.load(gzip.open(repo / "lobbying-map/research/directory-base.json.gz"))

    alias_to_group = {}
    for c in base["companies"]:
        for a in c["aliases"] + [c["name"]]:
            key = norm(a)
            if key:
                alias_to_group.setdefault(key, set()).add(c["id"])

    db = sqlite3.connect(db_path)
    clients = db.execute(
        "SELECT client_name, COUNT(*) FROM filings WHERE client_name IS NOT NULL GROUP BY client_name"
    ).fetchall()

    out, unmatched, ambiguous = {}, [], 0
    mapped_filings = total_filings = 0
    for name, n in clients:
        total_filings += n
        key = norm(name)
        groups = alias_to_group.get(key)
        if groups and len(groups) == 1:
            out[key] = {"name": name, "group_id": next(iter(groups)),
                        "match": "exact_alias", "filings": n}
            mapped_filings += n
        elif groups:
            ambiguous += 1
            out[key] = {"name": name, "group_id": sorted(groups)[0],
                        "candidates": sorted(groups), "match": "ambiguous", "filings": n}
            mapped_filings += n
        else:
            unmatched.append({"name": name, "filings": n})

    unmatched.sort(key=lambda x: -x["filings"])
    report = {
        "client_names": len(clients),
        "mapped_exact": sum(1 for v in out.values() if v["match"] == "exact_alias"),
        "ambiguous": ambiguous,
        "unmatched": len(unmatched),
        "filings_mapped": mapped_filings,
        "filings_total": total_filings,
    }
    dest = Path(db_path).parent
    (dest / "entity-map.json").write_text(json.dumps(out))
    (dest / "entity-map-report.json").write_text(json.dumps(
        {**report, "unmatched_top": unmatched[:300]}, indent=1))
    print(json.dumps(report, indent=1))


if __name__ == "__main__":
    main()

# Reproducing the directory

Requires Python 3.10+ and lxml. Run from the site directory.

```sh
mkdir -p work/data
cp scripts/data/*.json work/data/
uv run --with lxml python scripts/data/index_archive.py
uv run --with lxml python scripts/data/download.py
uv run --with lxml python scripts/data/extract_issues.py
python3 scripts/data/export_directory.py
python3 scripts/data/test_cleaning.py
```

`LOBBYING_DATA_DIR` optionally overrides the cache directory. The cache retains government HTML responses and query provenance, raw XML ZIPs, and an SQLite filing index. Search requests are paced and resumable. The checked-in annual API counts are the September 2026 snapshot; remove the cached year-counts.json and run count_years.py to refresh them. Refreshing live data also requires a fresh search-pages cache. The upper acquisition date in index_archive.py must advance for future snapshots.

The full-text XML archive has historical gaps and only supplements issue labels. Completeness is measured against LDA API totals independently for every reporting year. Name groups standardize Unicode, case and spaces, without resolving corporate identity. Registrations and latest No Activity reports do not establish activity years. All source report versions remain available.

## Readable directory

Run `python3 scripts/data/dedupe_directory.py` after the original export. This writes directory-v2.json.gz while preserving the original index and every report shard. It groups punctuation and equivalent suffix variants, and joins bare names only when the base has one legal-form family. It does not resolve ownership, subsidiaries or intermediary clients. Activity years are recalculated using the latest posting across combined names.

Run `node --experimental-strip-types scripts/test-directory.mjs` for report-version and Anthropic regression checks.

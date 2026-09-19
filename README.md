# Lobbying Atlas

Federal lobbying directory, focusing organization enrichment on clients active in 2026.

## Saved progress (September 19, 2026)

- 18,036 original filing-name entries; 17,734 displayed organizations after verified splits/merges.
- 14,143 identity-confirmed; 3,893 incomplete (3,070 partial, 823 unresolved).
- 14,612 verified websites; 10,939 full official logos.
- Identity confirmation does not imply complete ownership, logo, or website fields.
- Latest local app commit before this backup: `eda46db`.
- Website publication is behind: recorded deployed version 219 has 13,840 confirmed identities. Subsequent archive upload failed. This GitHub backup does not deploy the site.

## Contents

- `lobbying-map/`: complete current tracked application snapshot, compressed research ledger, verified merges/splits, assets, and build scripts.
- `work/`: research pipeline scripts, per-batch decisions and JEV results, saved handoff notes.
- `outputs/`: progress records and output documentation.
- `progress/`: coverage snapshot, local commit history, backup manifests.
- Release `research-backup-2026-09-19`: compressed retained research evidence and current 2026 output records. Download all parts before restoring; see its manifest.

The larger archive preserves retained fetched source pages, before-profiles snapshots, classifier results, scripts, decisions, and data inputs. Repeated bulk web caches, deployment tarballs, repeated live-site download copies, dependencies, build artifacts, bytecode, and potentially credential-bearing files are excluded. Exclusions are recorded in manifests. Original local files are retained.

## Run the app

```sh
cd lobbying-map
npm ci
npm run dev
```

Build and validate:

```sh
npm run build
node scripts/test-reviewed-2026.mjs
node scripts/test-verified-merges.mjs
```

## Resume research

Read `progress/current-progress.json`, `work/research-2026/latest-handoff.md`, and the current queue after restoring the research archive. Last JEV batch 230 completed 31 items with one error; its candidates still need review. There is no running research process represented by this backup.

Source ledger: `lobbying-map/research/reviewed-2026.json.gz`. The archive also includes `work/research-2026/reviewed.json`. Scripts run from the repository root unless documented otherwise. JEV requires the separately installed jev-sift plugin and locally configured authentication; credentials are not included.

Keep original filing labels and source links. JEV scores are triage, not verified identities. Do not merge parents/subsidiaries or mark announced acquisitions completed without evidence. Preserve unknown ownership and identity conflicts.

This repository is a fresh snapshot rather than the 4 GB local Git object history. The local history remains intact and its commit log is included.

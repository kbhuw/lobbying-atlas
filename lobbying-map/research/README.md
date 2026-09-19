# Organization research

The requested objective is to research every directory entry individually, explain the organization, cite evidence, distinguish organization type and ownership, and highlight a curated selection of well-known organizations.

## Files
- `profiles.json`: manually researched annotations keyed by exact directory ID. Do not overwrite this file with the original seed script.
- `../scripts/data/export_profiles.py`: combines this ledger with collected LDA descriptions and regenerates `public/data/directory-v3.json.gz`.
- Outside the site: `../work/organization-research/queue.jsonl`, `research-progress.json`, `collector-progress.json`, and `research.sqlite`. Paths are relative to site root for these outside files.
- `../work/organization-research/pages/`: original sanitized API pages, without registrant contact fields.

## Continue one entry at a time
1. Read the saved queue. Pick entries with `pending` or `self_reported` status in name order. A small initial curated batch of recognizable names has been prioritized. Do not repeatedly redo those profiles.
2. Inspect the organization's original filing, including disclosed name, location and business description. Find authoritative organization websites, registry records, SEC reports, IRS records or other reliable evidence. Resolve ambiguous identities using location, dates and business details, not name resemblance alone.
3. Write a concise neutral description. Every factual classification needs a source with URL and a note identifying the supported claim. Preserve each source's effective date where ownership may have changed. Record `checked_at` as the actual research date. Do not imply that a current owner owned the organization in every historical filing year.
4. Save a profile keyed by the existing directory ID. Required fields follow existing profiles. `sourced` means a sourced profile exists, not that every identity or historical fact is verified. Use `unresolved` when research could not establish the entity, and explain what was checked and what remains unclear. Do not infer privately held status from Inc., LLC or absence of a ticker. Public benefit corporation is legal form, not public listing. Do not merge parents, subsidiaries or similarly named organizations without evidence.
5. `featured` is an editorial navigation aid for recognizable organizations, not a popularity score, endorsement or lobbying-importance metric.
6. Run the exporter, `node --experimental-strip-types scripts/test-directory.mjs`, `node --experimental-strip-types scripts/test-profiles.mjs`, and build when publishing. UI type/ownership filters derive their choices from the actual annotation values.
7. Publish incremental improvements using Sites, preserving current owner-only access. Use the bundled git executable under `~/.cache/codex-runtimes/codex-primary-runtime/dependencies/bin/fallback/git` for credentialed pushes. Never store credentials. Exact pushed source must match saved deployment.
8. Record progress in `runs.jsonl`: timestamp, IDs attempted, sources/research notes, counts, publication outcome. If every entry has been attempted, report remaining unresolved cases and stop the continuation automation; do not manufacture answers to force completion.

## Source collection
`python3 scripts/data/collect_client_profiles.py` resumes a rate-limited API collector. A process lock prevents duplicates. Check recent progress before restarting. Preserve pacing, retries and pagination checkpoints. This gathers self-reported descriptions and does not perform independent research. The LDA client table is not identical to the directory; match only exact disclosed aliases and keep ambiguous names explicitly unverified. Do not equate API client rows with unique organizations.

## Publication caveats
The original 76,884 directory groups were made by name cleanup, not a fully verified corporate identity registry. An annotation does not verify every grouped alias. Source filings and name variants remain accessible. No annotation should assert a lobbying outcome, a legislator's position, or a causal effect from the fact that a filing exists.

## Accelerated pass (September 4, 2026)
The user rejected the hourly trickle and explicitly requested cheaper subagents and same-day work. The hourly automation is PAUSED. Two lighter subagents research disjoint batches; their output is reviewed before merging. The first review caught a reversed-name/founding-date mismatch, so original filing dates and location checks are mandatory. Do not invent timing metrics; benchmark start is recorded externally in the work directory.

`extract_bulk_profiles.py` gathers descriptions and location observations from the already downloaded ZIPs. `collect_sec_profiles.py` and `collect_irs_candidates.py` collect official registry records. `match_registry_profiles.py` requires legal-name and city/state corroboration before generating `registry-profiles.json`. These automatic matches are explicitly separate from manually researched profiles, and unmatched records must never be assigned private ownership merely by exclusion. `export_profiles.py` combines these tiers into the website and records exact coverage. Automatic registry matches remain eligible for later individual review. Never claim this automated pass fulfills complete individual research of all entries.

## 2026 individual-review queue
The active scope is the 18,036 directory entries with activity in 2026. The website defaults to 2026; historical records remain selectable. `reviewed-2026.json.gz` stores the complete reviewed profiles and overlays them without changing group IDs, aliases or filing membership. The first stratified sample of 100 includes 10 previously sourced, 25 registry matches, 45 filer descriptions and 20 pending entries. It is a pilot, not complete coverage.

The durable queue and per-entry missing fields are in `../work/research-2026/queue.jsonl`; results and timing in `../outputs/2026-research-trial/`. Preserve this queue when resuming. Do not re-run sample preparation over completed work. All remaining 2026 entries still need individual review, and partial profiles need missing ownership/logo evidence.

`registry-websites.json` contains websites reported in IRS tax returns located by EIN through ProPublica. These remain automatically matched, self-reported historical websites; never count them as individual review. The collector is resumable and stores only extracted organization facts, not officer/contact details.

The pilot caught wrong entity websites, cross-record source contamination and parent/subsidiary errors. Require an actual external check for every entry. Use small disjoint batches with exact IDs, explicit source claims and independent checks; do not blindly scale unreviewed cheap-agent output. Missing evidence stays unknown. Official logo/site-icon assets are fetched from observed URLs and checked; icons must not be described as full logos.

The compressed ledger is the tracked source. An optional ignored `reviewed-2026.json` editing mirror takes precedence locally; `npm run build` synchronizes it into the compressed ledger. Clean checkouts read the compressed ledger directly. This avoids a source-upload object-size limit without removing evidence or profiles.

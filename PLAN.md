# Lobbying Atlas — Deep Plan

## End goal (one sentence)

A public, readable site where anyone can answer **"who lobbied for what"** — by asking in plain English, or by browsing an issue, a company, or a lobbying firm — and every answer is sourced to specific LDA filings.

### The questions it must answer

| Question | Required data |
|---|---|
| Who lobbied on issue X in period Y? Top spenders, which firms? | per-filing issue codes + amounts + client/registrant links |
| What did company C lobby for, how much, through which firms, when? | same, grouped by client |
| Which clients does firm F represent, on what, for how much? | same, grouped by registrant |
| Who lobbied on a *specific topic* ("AI safety", "ticketing fees", a bill number)? | normalized topics over `lobbying_activities.description` free text |
| Who lobbied agency / Congress body Z? | per-activity `government_entities` |
| Who are the lobbyists behind X, and their revolving-door positions? | per-activity `lobbyists[].covered_position` |

The current site answers "who is org X and what filings exist". None of the above are answerable today — per-filing detail was never ingested.

## Inputs — what we have vs. what we need

### Already in the repo (verified, keep)

| Input | Coverage | Status |
|---|---|---|
| Filing index shards (`public/data/reports/`) | 1,956,084 rows, 1999–2026, every year count-verified vs LDA.gov | clean; metadata only (id, registrant name, kind, amount, year, posted) |
| Name groups (`research/directory-base.json.gz`) | 76,884 groups / 85,426 disclosed names | name-joins, identity unverified — known limitation |
| 2026 research ledger (`reviewed-2026.json.gz`) | 18,036 entries: 14,143 confirmed / 3,070 partial / 823 unresolved | good; powers org identity display |
| Verified merges (275) + splits (6) | — | applied at build |
| Registry websites, manual profiles | — | fine |

### Must be fetched (all public, no auth)

| Input | Source | Scale | Notes |
|---|---|---|---|
| Per-filing detail: `lobbying_activities[]` (issue code, specific-issue text, lobbyists, government_entities), `income`/`expenses`, canonical `client.id` + `registrant.id` | LDA API list endpoint `/api/v1/filings/` already returns all of this nested — no per-filing calls needed | ~1.96M filings, paginated | bulk path: House disclosure XML zips (script `extract_issues.py` already exists; XML has issues/lobbyists/entities too) for history + API for 2026 currency |
| Canonical clients/registrants | `/api/v1/clients/`, `/api/v1/registrants/` | ~90k + ~25k rows | gives legal IDs — fixes the fragile name-matching |
| Evidence caches from prior research | GitHub release `research-backup-2026-09-19` (~765MB, 2 parts) | restore only if auditing old decisions |

### Enrichment layer

- **JEV (`typesafe-ai/jev`)** — two jobs: (a) normalize `lobbying_activities.description` free text into a clean topic taxonomy at scale (cheap boolean/prob judgments per batch, same pattern as existing identity triage); (b) assist ambiguous client↔group identity matches.
- Everything JEV produces is **triage, not fact** — shown as derived/topic data, never as verified identity.

## Outputs — the new data model

```
filings_detail   filing_uuid | client_id | registrant_id | year | period | kind
                 amount (income or expenses) | dt_posted | supersedes chain
activity         filing_uuid | issue_code | issue_text | lobbyists[] | gov_entities[]
clients          lda client_id ↔ directory group id ↔ reviewed profile
firms            lda registrant_id → canonical firm (name dedup)
topics           issue_text → normalized topic (JEV-derived)
rollups          issue×year → top clients, top firms, $ totals
                 client → issues by year, spend by period, firms used
                 firm → clients, issues, $ totals
```

## Phases

**0 — Rebuild the ingestion spine** (this is "clean the data" properly)
- SQLite `filings_detail` + `activity` tables populated from House XML zips (resumable, same pattern as `extract_issues.py` but extracting everything) with API gap-fill for recent filings.
- Acceptance: per-year counts reconcile against LDA `coverage` expected totals; every 2026 filing in `reports/` shards has a detail row; parse-error log near zero.

**1 — Entity mapping**
- Join `client_id`/`registrant_id` → directory groups → reviewed profiles. Emit a mapping table plus a coverage report (how many filings land on verified orgs vs name-group-only).
- JEV triages ambiguous matches; humans/decisions ledger already exists for disputes.

**2 — Topic normalization**
- JEV batches over distinct `issue_text` values → topic taxonomy (e.g. maps "H.R. 1234 energy tax credit" → Taxation + Energy + named bill). Output stored with provenance (derived, not filed truth).

**3 — Query surface**
- Server-side query API (the app already targets Cloudflare Workers; D1/SQLite or prebuilt rollup shards) + static leaderboards for head queries.
- UI: issue pages, company "answer panel" (lobbied on X, paid $Y via firms Z), firm pages, ask box (NL → structured query → sourced answer with filing links).

**4 — Publishing**
- Move off `chatgpt.site` (Codex-only deploy path, currently wedged) → Cloudflare. `wrangler` config already exists in `dist/`.

## Decisions to lock

1. **Scope of ingestion**: all 1.96M filings (recommended — the corpus is the product) vs 2024+ only.
2. **Ask box**: structured NL→filters over the clean schema (safe, fast) vs agentic answers with JEV (flexible, needs guardrails). Can ship structured first.
3. **Hosting**: confirm Cloudflare as the target.

## Non-goals / guardrails (inherited from existing project rules)

- No inference of lobbying outcomes, meetings, or legislator positions.
- Filer income vs client expenses never summed together.
- Missing fields stay visibly missing — no manufactured completeness.
- Name groups stay labeled as name groups unless a verified identity decision exists.

---
name: testing-lobbying-map
description: How to run and test the lobbying-map app (vinext SPA, static gzipped JSON data, view-state navigation) in the lobbying-atlas repo.
---

# Testing lobbying-map

## Running
- App lives in `lobbying-map/` under the repo root. Two ways to serve:
  - Dev: `cd lobbying-map && npm run dev` (vinext) → http://localhost:3000. No auth needed.
  - Production preview (what's deployed): `cd lobbying-map && npm run build` then `npx wrangler dev --config dist/server/wrangler.json --port 8788` → http://localhost:8788/. Prod build strips React dev-only warnings, so console looks cleaner than dev.
- This box's Node (22.12) is below the engines requirement (>=22.13) but `vinext dev` works anyway — only warnings appear.
- Servers may not survive machine restarts; check with `curl -s -o /dev/null -w '%{http_code}' <url>` and restart as needed (`nohup` for dev, wrangler for prod).

## App structure (for navigation)
- It is a single-page app (`app/page.tsx`) — there are no routes. Views are switched by React state via the nav buttons: "Worth a look" (default landing — `NotableExplorer`, 4 sub-tabs: Biggest spenders / Revolving door / Foreign-based clients / Hot bills), "Who lobbied for what", "Lobbying firms", "Organizations" (`components/lobbying-views.tsx`: `IssuesExplorer`, `FirmsExplorer`, `OrgLobbyPanel`). Topics/firms render as `.topic-card` buttons in a `.card-grid`; the Worth-a-look views render `.shame-row` rows with `<details class="row-details">` expanders.
- Stance data: `stances.json.gz` = `{bills: StanceBill[350], orgs: Record<key, OrgStances>}` — org stance cards keyed by `group_id || id || name`; bill-expander org links render only when `entry.id` resolves in the directory company map (unresolved names render as plain text — by design). "Hot bills" button only appears once stances.json.gz loads.
- Org detail: clicking a name sets `selected` (directory org profile). Org keys starting with `n` (unmapped name groups) instead set `lobOrg` and render a standalone `OrgLobbyPanel` without the directory profile chrome.
- Quirk: the "Organizations" nav button does NOT clear `selected`, so it does nothing while viewing an org profile — use the "← All organizations" back button.
- Quirk: `IssuesExplorer` shares one search field between the topic/issue list and the org leaderboard inside a topic — the topic search text carries over into the org filter.

## Verifying expected values without guessing
- All data is static gzipped JSON under `lobbying-map/public/data/`: `directory-v3.json.gz` (org directory index) and `lobbying/` (index, topics/*-YYYY, issues/*-YYYY, firms/<id>, orgs/<key>, filings/<sha256-prefix>, notable.json.gz, stances.json.gz).
- Pull ground truth with python before asserting:
  `python3 -c "import gzip,json;d=json.load(gzip.open('public/data/lobbying/index.json.gz'));print(d['years'],len(d['topic_names']),len(d['issue_codes']))"`
- To find an org with NO lobbying shard (graceful-degradation test): `orgfiles=set(f[:-8] for f in os.listdir('public/data/lobbying/orgs')); [c for c in d['companies'] if c['id'] not in orgfiles]`. Example: "Douglas County (Washington)" id `3624b73887546473`.
- To find an n-prefixed (unmapped) org row on a topic board: scan `topics/*-2026.json.gz` for `o['id'].startswith('n')`. Example: "The US Cannabis Roundtable" `n1eff8655d276103b` on the Cannabis board.

## Known pitfalls
- `lib/lobbying.ts` `loadOrgFilings` hashes filing ids to find the right `filings/<hex2>.json.gz` shard. It was re-keyed from MD5 (unsupported by WebCrypto — silently hid "Filing detail" everywhere) to sha256(doc_id)[:2]. If "Filing detail" ever disappears again, check the digest call and whether shard filenames match the client-side hash.
- Use `browser_console` to check for errors; the tool's annotated DOM is reliable for asserting table contents since every row renders in DOM even when offscreen.

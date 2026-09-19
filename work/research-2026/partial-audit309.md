# Partial audit 309

This is a read-only audit of `reviewed.json` and existing `website-cache/` files. It inspected 22 manually selected partial records whose saved identity evidence explicitly says the exact organization/legal name was matched, while ownership remains `Unknown` or the standalone logo is unresolved. Two broader exact-operator/DBA patterns are included: AHAM and Sterling Ranch LLC.

The fastest next queue is logo-only recovery for the candidates with a valid official cache and no identity contradiction. Ownership research should be a separate queue: the saved evidence intentionally withholds public/private status unless a primary source states it. The two APTA rows are likely an alias/duplicate and should be deduplicated before work. ApolloMD retains a parenthetical filing context; preserve it until the client record is checked. AHAM already has an official logo, so it is ownership-only. Sterling Ranch has an exact county owner/developer bridge, but that does not establish beneficial ownership. No record was reclassified.

Recommended workflow:

1. Read the cached body and asset candidates; if the body has an official logo asset, resolve only `logo_url`, `logo_source_url`, and `logo_status`.
2. For ownership, search the organization’s own legal/footer/about page or a primary filing. Treat “LLC,” founder language, funding, and trade-association membership as insufficient by themselves.
3. Recheck exact filing location/name for rows with parenthetical contexts or duplicate aliases before any identity promotion.
4. Escalate only records whose cache body lacks an exact name bridge; do not spend searches re-establishing the 20 identities already supported by saved evidence.

Candidate IDs and exact evidence strings are in `partial-audit309.json`, with source URLs and cache pointers for each row.

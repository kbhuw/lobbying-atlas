# Publication 106 diagnosis

## Scope

Read-only inspection of the current publication record, handoff, prior publication60/74/84 diagnostics, the `lobbying-map` Git checkout, and the bundled Sites 0.1.66 hosting instructions. No source push, credential operation, deployment, repository mutation, or master edit was performed.

## Verified current state

- `publication.json` records the last successful live deployment as version 214, backed by remote revision `08745ef6078f8e7c36f2389ec8e9eff2bf838afa`; authenticated rendered-directory bytes remain unverified.
- The prepared local source is `2dfe0576bee7ae370ffe8bd000ce4cf4acbfbe57`, and Git confirms the known remote revision is an ancestor. The range is 71 commits and about 14,463 KiB of reachable object data by `git rev-list --disk-usage`.
- The checkout has no configured Git remote and no pack files: `git count-objects -v` reports 3,495 loose objects, 2,506,832 KiB of loose-object storage, and `in-pack: 0`. This means the Sites connector owns the actual push destination and local Git cannot independently verify its remote branch or inspect server-side rejection details.
- The current tracked data remains dominated by `research/reviewed-2026.json` (~33 MiB) and `research/verified-entity-merges.json` (~388 KiB). The latest local commit changes both and adds the accumulated source history.
- Prior diagnostics already tested a normal fast-forward snapshot with only about a 293 KiB delta (`df058c7` from the known remote base), plus fresh credentials, HTTP/1.1, and the updated Sites 0.1.66 client. All returned HTTP 500 before version creation.

## Finding

No new local repair route is supported by the evidence. The current commit is a valid fast-forward descendant, but the smallest previously tested fast-forward also failed. That rules out the current archive size, the 71-commit range, and the unpaced large JSON change as sufficient explanations for the persistent failure. The absent local remote and all-loose-object state are repository hygiene facts, but they do not explain a server response that occurs before a Sites version exists.

The Sites 0.1.66 instructions provide only one source path: commit the validated checkout and push it with the per-command write credential, then save/deploy the matching archive. They explicitly provide no archive-only or source-push bypass. Creating a replacement Site, force-pushing, deleting history, changing access, disabling verification, or embedding credentials would violate the documented safe flow and could orphan the existing live Site.

## Actionable next step

The owning agent should stop retrying client-side variants and obtain the Sites source-push request/correlation ID and server-side Git transport logs from the Sites service owner. `publication.json` currently records the HTTP 500 but no request ID, so another local retry would not add diagnostic information. Once server-side cause is known, reconcile the connector’s remote branch, commit/package the exact intended revision, and use the documented native save/deploy sequence. Preserve version 214 and the prepared archives as rollback artifacts until a successful source push and live-byte verification are complete.

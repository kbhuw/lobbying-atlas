# Publication 120 diagnosis

## Scope

Read-only inspection of the current publication record, publication60/74/84/106 diagnostics, latest handoff, and the installed Sites hosting instructions. No source push, credential operation, deployment, archive upload, reset, force push, archive bypass, or source/master mutation was performed.

## Observed state

- `work/research-2026/publication.json` records the last successful publication as version 214 at [lobbying-atlas.kush581812.chatgpt.site](https://lobbying-atlas.kush581812.chatgpt.site), backed by source revision `08745ef6078f8e7c36f2389ec8e9eff2bf838afa`. It says native deployment succeeded, while authenticated rendered-directory/live-byte verification remains false.
- The current record identifies a prepared local revision `a4d5b65e4173426ad1c25e1ab28aa991b78baf2d`, archive `work/site-sept13-featured119.tar`, and archive SHA-256 `5d6b8f2d07e1f8d5a9d38ab4175706513646f5105fc3ab437cf0c05606fa5c55`. The local archive is present and hashes to that value; its size is 98,523,857 bytes.
- The prepared attempt reports build/data checks passed. Its last failed upload was a fresh-credential normal source push at local revision `7371906bda3f4a64c7cd619f0f684a137f4fb780`, returning HTTP 500, exit 1, before deployment. The record explicitly says the updated Sites 0.1.66 client did not resolve the source-server failure.
- The same failure boundary is documented across diagnostics 60, 74, 84, and 106. In particular, diagnostic 74 records an ordinary fast-forward child with only about a 293 KiB delta failing HTTP 500; diagnostic 106 records that fresh credentials, HTTP/1.1, and the newer client also failed before version creation.
- `pending_publication_attempt` is populated with a prepared artifact, but the top-level `pending_attempt` is null. No active server-side attempt or newer version is recorded. The latest handoff likewise says source push HTTP 500 persists and live state remains version 214.

## Tool-path assessment

The current Sites instructions provide read-only post-publication inspection calls such as listing/getting saved versions, checking deployment status, and reading Worker logs. Those can establish whether an already-saved version or live deployment is healthy. Worker logs diagnose deployed request/runtime failures; they cannot explain a source push that returns HTTP 500 before a version exists.

The documented publish path still requires the owning agent to push the exact committed source, then package and save that same revision. The skill exposes no archive-only save/deploy path and no client-side source-push log viewer. The Sites skill also restricts source credentials, push, save, deployment, and Sites calls to the Site-owning agent; this diagnostic therefore did not invoke those tools.

## Diagnosis

The evidence supports a backend/source-repository transport blocker, not a local build, archive, credential-format, protocol, or deployment-runtime problem. The smallest tested fast-forward failed before version creation, and independent client/credential/protocol variants produced the same HTTP 500. Repeating the same push or preparing another archive would add no diagnostic information and could create unnecessary state divergence.

## Safe next action

The Site-owning agent should use the existing project/version metadata only to perform read-only reconciliation if needed, then obtain the source-push request/correlation ID and server-side Git transport logs from the Sites service owner. `publication.json` records the HTTP 500 but no request ID, so the next useful evidence must come from the service side. Once the backend issue is identified or repaired, reconcile the remote revision, rebuild/package the exact intended local revision, and use the documented native push → save → deploy sequence. Preserve version 214 and the prepared archive as rollback artifacts until a new source push succeeds and live bytes are verified.


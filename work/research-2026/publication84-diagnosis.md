# Publication 84 blocker diagnosis

## Scope

Read-only inspection only. No source push, credential operation, save, deployment, or master edit was performed.

## Current state

- `publication.json` still identifies the last successful live deployment as version 214 at `https://lobbying-atlas.kush581812.chatgpt.site`; it does not record a newer successful deployment or a changed remote revision.
- The prepared attempt now points to commit `774372278915deecacea08ba08853aea7d1a1a57` and archive `work/site-sept13-featured82.tar` (98,470,978 bytes recorded in the filesystem; SHA-256 `6275cbffe00266e0de456508f8365557c0af78feb1617b4e03f37ce2156cd704`). Build/data checks are recorded as passed.
- The local checkout has since become dirty: `research/reviewed-2026.json` and `research/verified-entity-merges.json` are modified relative to `7743722`. Therefore the prepared archive is an exact artifact for commit `7743722`, but it is not an artifact for the current working tree. The Sites publishing instructions require the pushed commit and archive to remain aligned; this is a packaging hygiene issue to resolve only after source push recovery.
- The current fast-forward range from known remote base `08745ef` to `7743722` contains 242 object entries and about 303,686,291 bytes of uncompressed object data. This is a larger source delta than the earlier failed ~293 KiB snapshot, but does not change the prior conclusion.

## Route assessment

No changed live state or supported alternate route was found. The Sites skill requires the owning agent to use native Sites calls, push the exact committed source, package that same revision, then save/deploy. It does not provide an archive-only bypass for a source push that fails before version creation. The prior smallest fast-forward source push already returned HTTP 500, including with a fresh credential, HTTP/1.1, and the newer client. Repeating those variants is not supported by the evidence.

The actionable next step remains Sites service-side investigation using a source-push request/correlation ID and server logs. Once that is available, the owning agent should first reconcile the remote revision, then commit/repackage the current intended source so the archive and commit match, and use the native save/deploy path. Until then, version 214 remains the only confirmed live state.

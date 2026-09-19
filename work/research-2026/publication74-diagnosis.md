# Publication 74 blocker diagnosis

## Scope

This is a read-only inspection of `publication.json`, the prior publication diagnosis, the source-push helper, the current checkout, and the prepared archive. No Sites push, save, deployment, credential rotation, or access mutation was attempted.

## New evidence

- The prepared source is still commit `a4d149900e0c60ba1794050319eba33b01e7bc42`, and the prepared archive is still `98,458,346` bytes with SHA-256 `e54b97aee39a259a8fd16fc870355ebee71fdfa0a7afb958f206f73e26f0dab5`, matching `publication.json`.
- The prepared checkout has 403 archive entries and passes the recorded build/invariant checks. Its tracked `research/reviewed-2026.json` blob is 34,518,171 bytes; `research/verified-entity-merges.json` is 378,733 bytes.
- The source repository remains unusually large and unpacked: `git count-objects -v` reports 3,352 loose objects and 2,305,984 bytes of loose-object files, with no pack files. Across all reachable history, Git reports about 2.35 GB of object data. The fast-forward range from the known remote base `08745ef` to the prepared commit contains about 246 MB of object data and 202 object entries.
- The earlier diagnosis already recorded a materially smaller fast-forward snapshot (`08745ef..df058c7`, roughly 293 KiB of source delta) failing with the same HTTP 500 before deployment. That rules out the prepared 98 MB archive, the current 246 MB historical delta, and the large reviewed JSON blob as sufficient explanations by themselves.
- The source-push helper uses a local HTTP proxy only to attach the bearer credential per request; it does not store the credential or alter Git configuration. The recorded failures occurred before any version/deployment response, including with a fresh credential, HTTP/1.1, and the updated Sites client.

## Conclusion

No materially new supported route or local root cause was found. The strongest supported conclusion remains a server-side failure in the Sites source repository push path, because an ordinary fast-forward source delta of roughly 293 KiB failed before deployment. The current archive and source-size measurements explain why larger attempts are risky but cannot explain the smallest reproduced failure.

The next useful action requires Sites service-side diagnostics (request/correlation ID and server logs for the source push). `publication.json` records the HTTP 500 but contains no request ID. Do not retry the same push or alter the Site while that evidence is unavailable; the last succeeded deployment remains the safe published state.

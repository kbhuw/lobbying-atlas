# Publication 60 diagnosis

## Evidence

- The selected Site checkout is `lobbying-map`; its current HEAD is `de4223b` and the working tree reports `main` with no local remote configured. The Sites source push therefore uses the connector's repository transport rather than a normal configured Git remote.
- The repository has only 433 tracked files, but `.git` is 2.1 GiB with 3,289 loose objects and no pack files. `git rev-list --disk-usage --objects --all` reports about 2.26 GiB of reachable history.
- The current tree contains a 34.5 MiB `research/reviewed-2026.json` blob plus several multi-megabyte generated data blobs. Recent commits repeatedly rewrite that large JSON file: the last three commits each change it while adding only a few identity records.
- The saved publication record says the validated build/invariants passed and that fresh credential pushes, normal pushes, HTTP/1.1, and the updated Sites 0.1.66 client all returned HTTP 500 before deployment. The last known remote revision remains `08745ef`; live version 214 is unchanged.

## Diagnosis

The earlier “single snapshot” idea was already attempted in a meaningful form: `df058c7` has parent `08745ef`, so it is a fast-forward child of the known remote base rather than an orphan requiring force-push. Its delta pack is only about 293 KiB. It still did not advance the remote. Therefore total repository history is not sufficient to explain the 500.

The measurable change is the size of the later source delta. Using Git's thin-pack calculation against the known remote base:

- `08745ef..df058c7`: ~293 KiB
- `08745ef..1bbbde6`: ~401 KiB
- `08745ef..7371906`: ~406 KiB
- `08745ef..9cb58fd`: ~5.25 MiB
- `08745ef..de4223b`: ~5.38 MiB

The jump begins when the repeatedly rewritten 34.5 MiB `research/reviewed-2026.json` blob changes substantially. This points to a source-import/request-size or large-delta handling limit, rather than a need to remove history. The current checkout has no configured Git remote; all evidence is from local object/pack calculations and the Sites connector's recorded responses.

## Recommended bounded repair

Do not create another snapshot branch. Publish a sequence of ordinary fast-forward updates from the known remote base, with each update containing a small bounded subset of the large JSON change, and verify the connector accepts each push before proceeding. The final update can then be packaged and saved using the normal Sites flow. This avoids force-pushing and tests the only measured variable that changed at the failure boundary: source delta size.

If the connector cannot accept sequential pushes or still returns 500 for a sub-megabyte delta, stop and provide the connector request ID to the Sites service owner. At that point the failure is server-side independent of local history, archive size, credentials, or HTTP protocol. Preserve version 214 and all existing archives as rollback; do not rewrite or delete the repository history.

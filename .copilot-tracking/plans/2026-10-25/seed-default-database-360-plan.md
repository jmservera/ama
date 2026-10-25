# Plan: seed merge default database path correction (issue 360)

Date: 2026-10-25. After the research artifact of the same slug, before edits.

## Change
* `factory.py`: add `sqlite_path(env)` returning `ZF_SQLITE` or `<ZF_STATE or dirname(data_file(env))>/zavaforward.sqlite`; `open_store` calls it (behaviour unchanged).
* `seed_merge.py`: compute the target with `sqlite_path` from the caller's original environment, then run with the empty `ZF_DATA` and `ZF_SQLITE` set to that resolved path (only when store is sqlite; explicit `ZF_SQLITE`, `ZF_STATE` and all MSSQL/MSI settings pass through unchanged).
* No change to `merge_seed`, schema, README semantics beyond one sentence.

## Tests
1. Default path: `ZF_DATA` points at a populated sqlite's directory, no `ZF_SQLITE`/`ZF_STATE`; the CLI apply updates that original database and no temporary database is created (the temp directory holds only the empty seed).
2. `ZF_STATE` only; and explicit `ZF_SQLITE` still wins.
3. `factory.sqlite_path` unit cases equal the previous `open_store` resolution; MSSQL env passes through unchanged (no `ZF_SQLITE` injected).
4. Existing 18 seed-merge tests and `test_sqlstore` stay green.

## Validation and process
Focused tests, independent critique (before edit), independent review after, commit, full new-head gate against current main in a new external directory with lock timeout 14400, receipt verification. No push or live action before coordinator release. The 2799f236 receipt does not cover this head.

## Live route
Unchanged except the job start image/command/args replace the container and drop inherited env: resupply every env var including secret references, then restore and verify the original definition.

## Independent critique (rubber-duck, before edit)
Verdict PASS, one execution. Findings: plan fixes the defect without duplicating logic; MSSQL and explicit paths unchanged; docs_dir and digest_dir follow the injected database path; JSON store is rejected before open. Suggestion accepted: the default-path test asserts success and added rows in the original database and, by patching `tempfile.TemporaryDirectory` to a retained directory, that no `zavaforward.sqlite` appears there.

# Research: seed merge default SQLite path (issue 360, correction cycle 1)

Date: 2026-10-25. Written before any correction edit, in child worktree `issue360-seed-correction1` (branch `fix/seed-default-database-360`, from unpublished 2799f236). The 2799f236 gate (PID 806216) is still running in the parent checkout, which is not touched.

## Trigger
Coordinator review of 2799f236: MEDIUM at `seed_merge.py:29`. `main` replaces `ZF_DATA` with an empty temporary file before `open_store`. For the SQLite store `factory.open_store` derives the default database as `ZF_SQLITE`, else `<ZF_STATE or dirname(data)>/zavaforward.sqlite`. With neither `ZF_SQLITE` nor `ZF_STATE` set, the override moves the target to the temporary directory (a new empty database), not the populated one. Then the empty-target guard exits 2, so no data is written wrongly, but the intended database is never merged. MSSQL is unaffected (database comes from `ZF_SQL_*`; state dir from `ZF_STATE` or ".").

## Evidence read
* `factory.py` lines 9-21: path resolution lives only inside `open_store`.
* `data_paths.data_file`: resolves `ZF_DATA` (directory, no suffix, or file) and the home default.
* `test_seed_merge.py`: all CLI tests set `ZF_SQLITE` and `ZF_STATE` explicitly, so the default path was never exercised. That is why the defect passed my tests and review.
* Earlier process note: my first review did not examine env-derived paths.

## Options
1. Keep the empty-seed override, resolve the real SQLite path first with the same logic and pass it as `ZF_SQLITE`. Needs that logic reusable, not copied.
2. Stop overriding `ZF_DATA`; give the empty-DB guard by checking before `_seed`. Not possible: `_seed` runs in the constructor.
3. Add a store-construction option to skip seeding. Wider change to `SqlStore`.

Chosen for planning: option 1 with the logic extracted into one small factory helper used by both `open_store` and the CLI.

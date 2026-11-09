<!-- markdownlint-disable-file -->
# Changes: issue 1292 extension E2 and E1 SQL validation (2026-11-09)

Plan: [plan](../plans/2026-11-09-priority-order-1292-e2-plan.md). Review: [review](../reviews/2026-11-09-priority-order-1292-e2-review.md). Original E1 records and review are preserved unchanged: [E1 changes](2026-11-09-priority-order-1292-e1-changes.md), [E1 review](../reviews/2026-11-09-priority-order-1292-e1-review.md). Parent runs `e1-sql-run`, `e1-sql-run2` (failures) and `e1-sql-run3` (Terminated by the coordinator) and the earlier busy admission receipt are untouched.

## Commits (local, no push)

* `fa74e8ed4` fix(core): `MssqlStore._create_indexes` creates indexes inside the `BEGIN IMMEDIATE` write transaction; removes the skip from `MssqlLegacyEdges`.
* `a20472734` test(core): the backfill test reads ordinals with `fetchall()` (the SQL `_Cursor` is not iterable; the SQLite cursor is). Body and thresholds otherwise unchanged. This was a latent defect in a test that had never run on SQL because of the skip, found by the first E2 SQL run (see evidence).

## Divergences and amendments

* E1 admission: nonqueued success after the prior holder finished. E2 consumed: second of five new cycles, three remain (per-source counter, no extra grant).
* The correction was conditional; the SQL reproduction confirmed the coupled bootstrap defect, so it is not speculative. No other refactoring.

## Actual SQL evidence (coordinator files; all owned containers removed, no leftover databases)

| Run | Head | Result |
| --- | --- | --- |
| `e1-sql-admission2-132322-2818937` | `71c7fe0fc` | priority 142 OK (1 skip, R2); resident MssqlResidentControls 91 OK (1 pre-existing skip); R2 unskipped out-of-tree: FAIL, `ix_recs_seq` already exists |
| `e2-sql-admission-134433-2845893` | `fa74e8ed4` | resident 91 OK; priority 142 with 1 ERROR (`_Cursor` not iterable) after the race assertions passed |
| `e2-sql-admission2-140248-2869281` | `a20472734` | priority 142 OK, zero skips; includes `MssqlLockTimeoutBegin`, `MssqlBeginRecovery`, C0 metadata, C2/C4 edges, large-backfill concurrent open |

Each run: one `flock -n`, fresh disposable container, image `sha256:cf8f0ab2ebe6...` (SQL Server 2022 16.0.4305.5), per-phase exit files, import provenance for `sqlstore.py` and `mssqlstore.py`. Resident SQL on `fa74e8ed4` stands for `a20472734` because `mssqlstore.py` (sha256 `1825dc5f...`) is byte-identical and only a test file changed.

## Local checks on the final head

ruff check and format (core, api) pass; mypy core 275 files no issues; core `test_priority_order` plus `test_resident_decisions` 398 OK (158 opt-in SQL skips, not SQL evidence); API ruff check and format pass; API `discover -s tests` OK (365 opt-in skips, not SQL evidence), including the shipped `app.js` DOM harness.

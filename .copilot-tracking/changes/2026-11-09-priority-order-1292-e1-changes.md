<!-- markdownlint-disable-file -->
# Changes: issue 1292 extension E1 (2026-11-09)

Plan: [plan](../plans/2026-11-09-priority-order-1292-e1-plan.md). Extension cycle E1 of five owner-approved new cycles; four remain; no renewal or count reset by the admission continuation. Original C1-C5 and adverse records are untouched. Owner-selected demo-targeted tier (no `rpi-checks --all`).

## Implementation (preserved from the E1 run, not altered by the continuation)

* `src/core/src/zava_forward/core/sqlstore.py`: `_suspect_ranges` reads `rec_order_legacy` with a direct `SELECT` so absent and present differ. A present row must be a JSON object with a positive integer `rows` (not bool); anything else returns the whole range as suspect. Absent still means no legacy backfill. Producer evidence: `_backfill_zero_ordinals` writes the row only when rows were backfilled, so a zero count has no documented meaning.
* `src/api/src/zava_forward/api/web/app.js`: `priorityPanel.ask` guards on `pending`/`checkHistory`, latches `checkHistory = mutationNeedsHistory(e)` on a committed, uncertain or transport outcome, and shows a `role="status"` note instead of the creation button.
* `src/core/tests/test_priority_order.py`: `LegacyMetadata` matrix (12 malformed classes, valid bounds, absent), `OwnedMssql` mixin with portable fixtures (`native_ddl`, `lift_audit_guard`), SQL Server subclasses for the legacy, C3 and C4 edge classes, `MssqlLockTimeoutBegin` (second connection, real `@LockTimeout` expiry, `@@TRANCOUNT`). One named SQL Server test is skipped with a recorded reason (see review finding R1).
* `src/api/tests/test_case_journey.py`: real `ThreadingHTTPServer` committed (409) and ordinary refusal responses fed to the shipped `app.js` in the Node DOM harness.
* `src/core/README.md`: sentence stating the strict `rec_order_legacy` validity rule (added in this continuation).

## Continuation actions

* Phase 0: ordinary `git merge --no-ff origin/main` (no rebase, no force). Pre-merge head `51f2d8731`, merged `origin/main` `ad679b96b` (contains the merged #144 queue adapter `4fcd1934f`). No overlap with the four modified files. Dirty files preserved.
* Non-queued SQL admission: one `flock -n /tmp/ama-rpi-heavy.lock` probe, rc=1 (busy). Holder proven by command line to be another lane (`e3-sql-1288-b2800513`, `.venv-1288`, pids 2801862, 2801863, 2802427), not this task. Not killed, not stolen, no retry. Evidence: coordinator `e1-sql-admission-*/admission.txt`. SQL Server tests were NOT run in this continuation.
* Earlier runs `e1-sql-run`, `e1-sql-run2` (failures, 36859 bytes stderr) and `e1-sql-run3` (runner stdout `Terminated`, coordinator stop) are preserved unmodified and are not success.

## Validation run in this continuation (head `fa5a9f371`, dirty source on top)

| Check | Result |
| --- | --- |
| `src/core`: `PYTHONPATH=tests:../agents/tests python -m unittest tests.test_priority_order` | Ran 142, OK, skipped 65 (opt-in SQL Server classes) |
| `src/api`: `PYTHONPATH=../core/tests:../agents/tests python -m unittest tests.test_case_journey` | Ran 31, OK |
| `ruff check tests src` and `ruff format --check` (core, api) | pass |
| `mypy` (core) | success, 275 files |
| Selected SQL Server tests | BLOCKED, not run (busy shared lock) |

<!-- markdownlint-disable-file -->
# Details: issue 1292 extension E2 (2026-11-09)

Plan: [plan](../plans/2026-11-09-priority-order-1292-e2-plan.md).

## Phase 1: serialize index creation

File `src/core/src/zava_forward/core/mssqlstore.py`, `_create_indexes`. After `_migrate_chat_memory()` (which commits its own transaction), open `BEGIN IMMEDIATE` under the existing `dblock`, execute the idempotent index statements, `COMMIT`, and on any exception `ROLLBACK` and re-raise, exactly the shape of `_migrate_chat_memory` and `_create_schema`. The application lock `zavaforward_write` makes the check-then-create atomic across connections. No retry, no catch-and-ignore of the duplicate-index error.

## Phase 2: restore the SQL case

File `src/core/tests/test_priority_order.py`: delete the `@unittest.skip` override in `MssqlLegacyEdges` so the inherited test runs on owned SQL Server unchanged.

## Phase 3: validation

Local: `ruff check`, `ruff format --check`, `mypy` as configured, `test_priority_order` (SQLite), API `test_case_journey`. SQL: a single `flock -n /tmp/ama-rpi-heavy.lock` run into a new unique output directory with fresh owned container; phases `test_priority_order` and `test_resident_decisions.MssqlResidentControls`. If the lock is busy, record a partial and stop.

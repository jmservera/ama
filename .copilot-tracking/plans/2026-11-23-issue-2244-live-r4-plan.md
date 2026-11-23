# Plan 2244 live r4 (2026-11-23)

Tier FULL (src change). Details: `.copilot-tracking/details/2026-11-23-issue-2244-live-r4-details.md`.

1. Add `MssqlDb._schema_current()` in `src/core/src/zava_forward/core/lawstore.py`: read-only; all five tables exist; ledger database needs append-only ledger kind on the four append-only tables, otherwise the four `*_append_only` triggers exist.
2. In `MssqlDb.__init__` skip the `BEGIN IMMEDIATE` DDL block when current.
3. Tests in `src/core/tests/test_mssql_startup_lock.py`: current schema (ledger and trigger) takes no write lock; missing table, missing trigger and wrong ledger kind take the locked path.
4. Validate: that test module, mypy and ruff in `src/core`.

## Critique (executed once)

Verdict compatible. Risks: a wrong ledger kind must still reach the SystemExit in the locked path (handled: not current). Read-only queries run outside the lock; a race only leads to the idempotent locked path. No finding conflicts with owner decisions.

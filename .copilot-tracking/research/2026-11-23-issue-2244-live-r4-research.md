# Research 2244 live r4 (2026-11-23)

Disposition: executed. Planning Readiness: Ready.

Earlier runs (r1 to r3) covered the schema fast path, the retry with backoff, the law store retry and the probe window. Not covered: the other start-up steps in `SqlStore._initialize` that still open `BEGIN IMMEDIATE` (the global `sp_getapplock`) on every start of a fully populated database.

## Findings

* `_migrate`, `_migrate_recommendations`, `_ensure_queue_membership` and `_seed` each take the write lock unconditionally (`sqlstore.py`).
* `_seed` is the cheapest to fix: on a populated database it takes the lock only to run `SELECT COUNT(*) FROM cases` and then commits with no write. A read-only count first removes one lock wait per start.
* Fix shape: count `cases` without the lock; return when non-zero; otherwise take the lock and re-check (check-then-act stays safe because the locked path re-counts).
* Live: `ca-cutover-test-demo-api` active revision 0000057 Healthy (read-only `az containerapp revision list`). No Azure change is needed or made.

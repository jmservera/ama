# Plan 2244 live r2 (2026-11-23)

Tier FULL (src/core change). Local commit only.

## Phases

* [x] Phase 1: `lawstore.MssqlDb` sets `startup_retries = LOCK_RETRY_ATTEMPTS - 1` right after creating `_Conn`; add `end_startup()` that resets it; `LawStore.__init__` wraps `RuleCardStore` creation and `seed()` in try/finally calling `end_startup` when present.
* [x] Phase 2: tests in `src/core/tests/test_mssql_startup_lock.py`; run them, plus ruff and mypy on src/core.
* [x] Phase 3: research note, README index and log entry, changes record with per-criterion table.

## Critique (executed once)

* `_Conn.startup_retries` is a plain attribute read per BEGIN, so setting it from MssqlDb is safe and needs no new retry logic. Verdict: compatible, proceed.
* If init raises, the `finally` still resets retries so runtime BEGINs fail fast. A test covers it.
* Rejected as out of scope: changing the StartUp probe (production setting), a lock drill (owner decision), a read-only precheck for rule cards (they seed data).

# Research: issue 2244 start-up write lock crash loop

Research disposition: executed. Planning Readiness: Ready.

## Findings

* `SqlStore._initialize` (src/core/src/zava_forward/core/sqlstore.py) runs `_create_schema`, `_migrate`, `_migrate_queues`, `_create_indexes` (which also runs `_migrate_chat_memory`) and `_migrate_recommendations`. Each takes `BEGIN IMMEDIATE`.
* On SQL Server, `_Conn.execute("BEGIN IMMEDIATE")` (src/core/src/zava_forward/core/mssqlstore.py) runs `BEGIN` = `sp_getapplock` with 15 s timeout, then `THROW 50002 'could not take the write lock'`. Nothing retries; the error propagates out of the constructor, the API exits 1, and the StartUp probe fails. That is the crash loop of #2244.
* Lock holder is not proven (issue says Log Analytics unreadable).
* Issue has no acceptance checkboxes; the suggested defect fixes are (a) retry with backoff, (b) read-only schema check first. Scope here: (a), the stated goal. (b) is a routed follow-up.

## Decision

Retry only the lock-timeout failure of BEGIN, only during store initialisation, with bounded exponential backoff (injectable sleep for tests). Runtime writes keep the single 15 s attempt. Other errors propagate unchanged.

## Acceptance evidence plan

Unit tests with a fake driver prove retry-then-success, bounded exhaustion, non-lock errors not retried, and no retry outside start-up. A live proof (holding the app lock against the demo DB and restarting the app) is a shared-system production-like change and is not needed for the demo; recorded as unproven live.

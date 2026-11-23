---
title: Research issue 2237 live3
ms.date: 2026-11-23
---

Task: issue-2237-live3. Disposition: executed (reconciles four earlier dated 2237 notes, adds a fresh live probe).

## Evidence found

* The cause note and the 0055 re-proof (docs/reference/research/issue-2237-live-cause-and-fix-2026-11-23.md and issue-2237-live-reproof-2026-11-23.md) already prove cause, fix (#2290 on main) and live 200.
* Existing tests cover the retention 503 mapping (test_error_logging.py) and the helper (test_mssql_startup_lock.py).
* Live now on revision 0000056 (created 2026-11-23 17:06 UTC). Fresh probe: /api/retention 200 for the Programme Manager, 55 of 55 requests 200. Log Analytics, last 12 h: no http-error line for /api/retention; 34 sql-write-lock-busy 503 lines on 0000055 for other paths.

## Remaining gap a test can close

The audit write fails closed with a 503, but no test shows the listing recovers on the next request (no stuck state, no partial audit). A regression test for that retry belongs in src/api/tests/test_error_logging.py.

Planning Readiness: Ready.

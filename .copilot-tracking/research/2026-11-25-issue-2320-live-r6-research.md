---
title: Issue 2320 live r6 research
ms.date: 2026-11-25
---

Research disposition: executed. Planning readiness: Ready.

Task: revision 0000070 removed 503s but 9 of 70 briefing requests took 5 s or more (max 7.64 s) under concurrent forecasts. Local main already holds the #2377 fallback (503 becomes an unrecorded answer).

Findings from `src/core`:

* `Store.briefing` on a cache miss calls `ai_tasks.run_text_task`, whose `finish` calls `add_record`; `add_record` holds `store.lock` (Python RLock) while `store.audit` and `store.save` open a SQL transaction.
* `mssqlstore.BEGIN` waits up to `@LockTimeout = 15000` ms for `sp_getapplock`. While a forecast writer holds the SQL lock, the briefing GET waits up to 15 s, and holds `store.lock` the whole time, which also stalls other requests. That wait is the 5 to 7.6 s tail.
* A GET that finds an unchanged version and cached answer takes no write lock (tested in #2358 tests).
* The fallback added in #2377 fixes the 503 but not the wait.

Bounded fix chosen: a per-thread short write-lock wait (2 s) used only for the briefing recording step, so a busy lock fails fast into the existing unrecorded fallback.

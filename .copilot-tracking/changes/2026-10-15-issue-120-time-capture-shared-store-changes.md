---
title: Issue 120 time capture shared store changes
description: Changes made for shared-store time capture and role separation
ms.date: 2026-10-15
---

* `mvp/zavaforward_mvp/timecapture.py`: shared-store tables with SQLite and T-SQL DDL, `request_enable`, `SeparationOfDuties`, `TimeCapture(store, env, db_path)`.
* `mvp/zavaforward_mvp/server.py`: `TimeCapture(store)`, `POST /api/time/request-enable`, enabling audit names the requester.
* `mvp/web/timecapture.js`: request and enable steps.
* `mvp/tests/test_timecapture.py`, `mvp/tests/test_mssqlstore.py`: new coverage; `time_*` tables added to the SQL Server wipe list.
* `mvp/README.md`, `docs/reference/log.md`: documented; log conflict resolved keeping both sides.
* No divergence from plan.

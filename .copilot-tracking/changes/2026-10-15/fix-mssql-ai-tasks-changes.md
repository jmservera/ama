---
title: mssql CI fix changes
task_slug: fix-mssql-ai-tasks
ms.date: 2026-10-15
---

## Changes

* `mvp/zavaforward_mvp/sqlstore.py`: `_proc_write` uses `_meta_set`.
* `mvp/tests/test_mssqlstore.py`: portability tests; `wipe()` covers assistant tables.

## Validation

* Full suite: 521 tests OK (85 skipped, need SQL Server).
* CI mssql command against a SQL Server 2022 container: 85 tests OK.
* The new portability tests fail on the pre-fix code (verified).

No divergences from the plan.

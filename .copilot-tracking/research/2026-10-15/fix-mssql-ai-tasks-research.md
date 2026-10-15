---
title: mssql CI failure after #260/#261/#262 research
task_slug: fix-mssql-ai-tasks
ms.date: 2026-10-15
---

## Scope

Failing job `mssql` (run 38732895074): `Incorrect syntax near the keyword 'OR'` and `Invalid object name 'assistant_attempts' / 'assistant_tasks'`.

## Evidence

* All six `test_mssqlstore` / `MssqlDurabilityTests` errors share one stack: `store.log_call -> sqlstore.save -> _proc_write` (sqlstore.py:406) runs `INSERT OR REPLACE INTO meta` directly. That is SQLite only. `_meta_set` already exists as the dialect hook (MssqlStore uses MERGE) but `_proc_write` bypassed it.
* `Invalid object name` is a cascade, not a missing-DDL defect: `Assistants.migrate()` already creates `assistant_tasks`, `assistant_allowance`, `assistant_attempts` and `assistant_events` on SQL Server (`MSSQL_DDL`, assistants.py). In `test_blocked_provider_does_not_hold_domain_or_sql_lock` the `manual()` thread crashed on the OR error, the test failed, `tearDown`/next `setUp` dropped the tables, and the still-running worker thread then hit the dropped tables.
* `ai_tasks.py` and `ai_registry.py` contain no SQL. `lawstore.py` and `timecapture.py` use their own local SQLite files (not the Azure SQL path), so their `INSERT OR IGNORE` is out of scope.
* `test_mssqlstore.wipe()` did not drop the assistant tables (hygiene gap).
* Docker is available via sudo and mssql-python installs from `mvp/requirements.txt`, so the CI job can be reproduced locally.

Research disposition: executed. Planning Readiness: Ready.

---
title: mssql CI fix plan
task_slug: fix-mssql-ai-tasks
ms.date: 2026-10-15
---

## Plan

* [x] Phase 1: route `SqlStore._proc_write` through `_meta_set` (SQLite upsert, MERGE on SQL Server).
* [x] Phase 2: add server-free regression tests that fail on SQLite-only syntax outside the dialect hooks; make `wipe()` drop the assistant tables.
* [x] Phase 3: validate with the full unittest suite and the CI mssql command against a SQL Server 2022 container.

Details: [fix-mssql-ai-tasks-details.md](../../details/2026-10-15/fix-mssql-ai-tasks-details.md)
Critique: [fix-mssql-ai-tasks-critique.md](fix-mssql-ai-tasks-critique.md)

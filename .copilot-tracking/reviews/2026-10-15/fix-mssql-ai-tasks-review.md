---
title: mssql CI fix review
task_slug: fix-mssql-ai-tasks
ms.date: 2026-10-15
---

Execution: executed once. Outcome: conformant, no open material findings.

* Root cause fixed at the single offending call. SQLite behaviour is unchanged (`_meta_set` is the same statement there).
* A real SQL Server run reproduces the CI job and passes, including the previously failing durability test.
* Follow-up: `lawstore.insert_ignore` and `timecapture.acknowledge` use SQLite-only syntax on their own local files; make them portable if those stores move to Azure SQL.

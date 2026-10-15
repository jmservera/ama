---
title: mssql CI fix plan critique
task_slug: fix-mssql-ai-tasks
ms.date: 2026-10-15
---

Execution: one pass. Verdict: proceed.

* The task brief assumed the assistant tables were not created. Evidence shows `migrate()` creates them; the error is a test-order cascade. Disposition: fix the root cause, do not add duplicate DDL, record the correction in the PR.
* Risk: MERGE without HOLDLOCK under concurrency. Disposition: accepted, writers are serialised by the exclusive application lock inside the transaction.
* Out of scope: lawstore and timecapture local SQLite files. Disposition: noted as a follow-up.

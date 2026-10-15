---
title: PR 282 CI test failure research
ms.date: 2026-10-15
---

* Disposition: executed. Planning Readiness: Ready.
* CI run 38751617631, job `test`: `test_chatthreads.SqlChatTests.test_concurrent_appends_get_distinct_sequences` failed with `ChatNotFound`. The `mssql` job failed the same test with "Connection is busy with results for another command".
* After merging origin/main the full suite passes locally (631 tests, 92 skipped); the failure is intermittent (6 of 40 isolated runs).
* Root cause: `SqlRepo.get`, `list` and `messages` ran on the shared connection without `store.dblock`, interleaving with another thread's `BEGIN IMMEDIATE` transaction.
* Azure SQL parity suite has not run against a real server; the `mssql` job result is unverified here.

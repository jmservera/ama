---
title: "Details: #146 RAI SQL restart reconstruction"
ms.date: 2026-11-14
task_slug: 146-rai-sql-reconstruct-0115
---

## Phase details

* Phase 1: three tests; real review, execute and provider validation-failure flow plus raw audit rows; restart closes store and service and opens a fresh `SqlStore` on the same file.
* Phase 2: `classify` maps `invocation`/`direct-call-claimed`, `send-refused`/`permit-denied`/`throttled`/`result-rejected`, `disabled`/`exhausted`, `review` (`reject` and `edit-accept` add override), `completed` (quarantined or held is withheld; returned but not ready is validation failure; other is fallback; all count as consumption), `direct-call-completed`.
* Phase 3: window is half-open on `at`; latency samples pair `claimed` and `completed` by task and fence.
* Phase 4: ruff, format, mypy per component; targeted tests.

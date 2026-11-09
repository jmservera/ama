---
title: Quality sensor demo 1288 C8 recovery plan
ms.date: 2026-11-09
---

Written 2026-11-09T08:05Z after the C8 research, before any C8 edit. Refs #1288, #107. No closing claim. Owner-selected demo-targeted tier (no full gate).

## Phases

* [ ] P1 Fix `test_assistants.MssqlFixture.setUp` so the SQL Server tests start from the C5 to C7 tables dropped too (`assistant_schedule`, `assistant_dispatch_gate`). Test-only; no product change unless P2 proves a defect.
* [ ] P2 Rerun the two failing SQL Server files and `test_assistants` under the nonqueued heavy lock with an owned disposable container; remove only that container.
* [ ] P3 Browser check: run the existing quality/technical-screens browser check for the changed `assistants.js` if a browser prerequisite exists; else record blocked.
* [ ] P4 Documentation: changes, one original review, state, handoff with AC matrix and live-walkthrough recipe.
* [ ] P5 Commit a clean candidate with repository-local noreply identity.

## Scenarios

* S1 After isolation, `MssqlPerHome` (all) and `MssqlHttp` withdrawal test pass on SQL Server.
* S2 If any still fails, it is a product defect; at most one scoped correction cycle before reporting the blocker.
* S3 Heavy lock busy at P2 or P3: record blocked, continue lightweight work, no queueing.

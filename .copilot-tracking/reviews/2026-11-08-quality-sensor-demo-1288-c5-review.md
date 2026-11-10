---
title: Quality sensor demo 1288 C5 review
ms.date: 2026-11-08
---

Recorded 2026-11-08T22:11Z. One self-review, executed once; outcome partial because heavy gates are pending. Boundary: C5 diff over `b938ed73`.

## Execution and outcome

* Execution: done, author self-review against the eight findings and the light suites in the changes artifact.
* Outcome: source and light SQLite evidence conform; SQL Server, query plans, browser, FULL not run.

## Findings (routed to later work, not re-reviewed here)

* Fail-closed: a changed control, an older marker or a missing guard withholds consent; migration restores it without touching policy or consent.
* Risk: the MSSQL trigger and `assistant_schedule` DDL are unexercised; a trigger with `AFTER` on SQL Server runs inside the writer's transaction, which needs the real engine to confirm.
* Risk: refresh at claim changes the stored snapshot of a queued task; the original event trail records `refreshed` but not the previous snapshot digest.
* Risk: a withdrawal after the last pre-call check and before bytes leave cannot be excluded by any caller-side check; output is withheld by projection.
* Risk: the schedule slot is occupied by manual and proactive tasks alike, so a manual request at a coarse schedule can defer a proactive scan for that schedule (cheaper, not a safety loss).
* Overlap: `sensor_consumer.py` also changes in #184; semantic merge needed after it lands.
* Not a proof of real AI: all provider tests use a local mock.

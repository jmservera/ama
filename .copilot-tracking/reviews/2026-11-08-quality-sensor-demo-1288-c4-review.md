---
title: Quality sensor demo 1288 C4 review
ms.date: 2026-11-08
---

Recorded 2026-11-08T21:48Z. One self-review, executed once; outcome partial because heavy gates are pending. Boundary: C4 diff over `699ec528`.

## Execution and outcome

* Execution: done, author self-review against the five findings and the light suites in the changes artifact.
* Outcome: source and light SQLite evidence conform; SQL Server, query plans, browser and FULL not run.

## Findings

* Fail-closed: a missing, unreadable or mismatching marker withholds consent; reconcile failure never grants.
* Risk: the marker proves counts and per-home digests, not full control bodies; an out-of-band edit restoring both is undetected.
* Risk: `_serviced` reads all tasks of one case and capability; bounded by the retention of that pair but not indexed by scope.
* Risk: MSSQL DDL for the marker table is unexercised; the epoch test simulates the epoch.
* Overlap: `sensor_consumer.py` also changes in #184; semantic merge needed.

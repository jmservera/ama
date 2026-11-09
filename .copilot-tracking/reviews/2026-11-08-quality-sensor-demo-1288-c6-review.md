---
title: Quality sensor demo 1288 C6 review
ms.date: 2026-11-08
---

Recorded 2026-11-08T22:50Z. One self-review, executed once; outcome partial because heavy gates are pending. Boundary: C6 diff over `5f89248b`.

## Execution and outcome

* Execution: done, author self-review against the eight C5 findings and the light suites in the changes artifact.
* Outcome: source and light SQLite evidence conform; SQL Server, query plans, browser, axe and FULL not run.

## Findings (routed to later work, not re-reviewed here)

* Residual: a direct SQL control write that bypasses `SensorConsumer.configure` can still commit during a call; the guard trigger only invalidates the marker.
* Risk: the hold's ordering depends on writer serialization. SQLite `BEGIN IMMEDIATE` is exercised; the SQL Server isolation behaviour of the hold and `configure` is unproven.
* Tradeoff: a withdrawal can wait up to the provider timeout plus 5 s; beyond 45 s it fails with `SENSOR_DISPATCH_IN_FLIGHT` rather than being silently dropped.
* Risk: replacement tasks add events and rows (at most three per schedule without a dispatch); retention is unchanged.
* Gap: the assessment-change migration test is not discriminating.
* Gap: `test_quality_sensors.py` has long-line lint findings in new test text.
* Overlap: `sensor_consumer.py` and `assistants.py` also change in #184 and #1292.
* Not a proof of real AI: all provider tests use a local mock.

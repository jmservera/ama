---
title: Issue 2201 live5 research, 2026-11-22
---

Refs #2201. Goal: root-cause the failed live receiver runs from Log Analytics now that query access is enabled, and count consecutive successes since SQL moved to S3 (14:00Z). Read only; no job change.

Research disposition: executed. Planning Readiness: Ready (scope fixed by the brief; prior notes: `docs/reference/research/issue-2201-live-receiver-recheck-2026-11-22.md`).

## Findings

* Query works on table `ContainerAppConsoleLogs` (`JobName`, `ContainerGroupName`, `Log`). Failure lines: `SENSOR_SQL_UNAVAILABLE` (10:35 to 11:50), argument error (11:32 operator start), `IOT_CALLBACK_FAILED` (13:30).
* Database is Standard 100 DTU (S3); DTU max 100 until 14:00, then 81 to 89.
* Executions: 14:00 and 14:30 scheduled Succeeded (streak two); 15:00 not started at 14:57.
* Evidence: `.copilot-tracking/evidence/2026-11-22/issue-2201-live5/`. Deliverable: `docs/reference/research/issue-2201-live-receiver-logs-2026-11-22.md`.

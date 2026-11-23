---
title: Issue 2201 receiver streak, failure logs and map probe (demo, 2026-11-23)
description: Fourteen consecutive scheduled receiver runs Succeeded, the 09:30 to 11:30 failures logged only IOT_RECEIVE_FAILED, and fresh readings reach the map
ms.date: 2026-11-23
ms.topic: reference
---

Scope: synthetic demo, desktop only, resource group `ama`. Azure was read only; nothing was created, so nothing needs deleting. Sign-in values were read at runtime and never printed. Refs #2201, #184.

Evidence is under `.copilot-tracking/evidence/2026-11-23/issue-2201-live10/` (probe script, `probe-readings.json`, `executions.json`, `employee-map.png`).

* Log Analytics (`log-cutover-test`, `ContainerAppConsoleLogs`): the 09:30, 10:00, 10:30, 11:00 and 11:30 UTC scheduled runs each wrote only `Cannot run: IOT_RECEIVE_FAILED`. The class of the receive error was not logged, so the cause stays unproven. Operator debug runs at 12:43 and 12:47 logged an Event Hub `ConnectError` (socket timed out) and a missing `websocket-client` import; they are not the scheduled failures.
* Scheduled runs 12:00 to 18:30 UTC all Succeeded (14 in a row); the 19:00 run was still Running at 19:07.
* Map probe at 19:10 UTC: `/api/map?zoom=14` returned 200 with 443 items; `ZF-2025-0030` and `ZF-2025-0331` returned state `ok`, 12 readings, latest `observed_at` `2026-11-23T19:05:00Z`, freshness `fresh`.
* Code: `live_receiver.main` now adds the exception class to `Cannot run: RECEIVER_FAILED`; the running image (digest `541068a6...2c38`) does not yet carry it, nor the earlier class fields.

| Criterion | Verdict |
| --- | --- |
| Root cause recorded with evidence | Partly proven; 09:30 to 11:30 cause unproven |
| Fix merged and deployed | Proven for earlier fixes; this change local only |
| Three consecutive scheduled runs Succeeded | Proven (12:00 to 18:30) |
| Readings in store and employee map with timestamps | Proven for the demo (latest 19:05:00Z) |

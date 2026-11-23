---
title: Issue 2201 live10 research
ms.date: 2026-11-23
---

Research disposition: executed. Opening note: all four criteria are ticked and the issue was reopened for live proof. Goal: read the 09:30 to 11:30 UTC 23 Nov failures from Log Analytics (unproven in live7 to live9), re-probe the run streak and the map, and find an untested code path. Findings follow below.

## Findings

* Log Analytics now answers (`log-cutover-test`, table `ContainerAppConsoleLogs`). The 09:30, 10:00, 10:30, 11:00 and 11:30 UTC scheduled runs each logged only `Cannot run: IOT_RECEIVE_FAILED` on stderr; no exception class, so the cause of those five failures stays unproven. Operator debug runs at 12:43 and 12:47 logged `ConnectError ... SocketError ... timed out` from the Event Hub client (a connection timeout) and a missing `websocket-client` import, but those are operator probes, not the scheduled failures.
* Every scheduled run from 12:00 to 18:30 UTC Succeeded (14 consecutive); the 19:00 run was Running at 19:07.
* Map probe 19:10 UTC (Playwright, runtime sign-in): `/api/map?zoom=14` 200 with 443 items; cases `ZF-2025-0030` and `ZF-2025-0331` state `ok`, 12 readings, latest `observed_at` `2026-11-23T19:05:00Z`, ids `LIVE-STQEOYP62W2-20261123T1905Z` and `LIVE-SIBP5GIQWTN-20261123T1905Z`, freshness `fresh`. Evidence: `.copilot-tracking/evidence/2026-11-23/issue-2201-live10/`.
* Code gap (new): `live_receiver.main` ends with a bare `except Exception` that prints `Cannot run: RECEIVER_FAILED` and no class, and no test covers that branch. Earlier workers covered only the StreamError branch (callback and receive class).

## Decision

Print the exception class name only (never message or traceback) with the `RECEIVER_FAILED` line and add one regression test. Planning Readiness: Ready.

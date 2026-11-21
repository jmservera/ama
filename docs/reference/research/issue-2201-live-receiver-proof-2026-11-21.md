---
title: Issue 2201 receiver proof, root-cause log capture and SQL retry (demo, 2026-11-21)
description: Live evidence for job-live-receiver after the bounded-window fix, the captured failure code SENSOR_SQL_UNAVAILABLE, the store and map readings proof, and a per-criterion table
ms.date: 2026-11-21
ms.topic: reference
---

Scope: synthetic demo, desktop only, resource group `ama`. Owner decisions of 2026-11-18 apply. Azure was read only (`az containerapp job` list, show, logs; staff app through Playwright). No resource was created, so none needs deleting, and no network rule, image or job was changed. Sign-in values were read at runtime and never printed. It extends the [earlier diagnosis](./issue-2201-live-receiver-failure-2026-11-21.md). Refs #2201, #184.

## Correction to the earlier note

The earlier note counted 26 retained executions, all Failed. The list read at 2026-11-21 22:43 UTC held 50: 41 Failed and 8 Succeeded. Failures are intermittent, so "all recent runs Failed" no longer describes the job.

## Evidence

Recorded under `.copilot-tracking/evidence/2026-11-21/issue-2201-live2/` (executions list, probe JSON, map screenshot, log captures, watcher script).

* Image and config: job image digest `sha256:60b1d026...7878`, equal to the demo API image; job last modified 21:33 UTC; schedule `*/30 * * * *`, window `--seconds 1500`, replica timeout 1620 s, 0.25 vCPU, 0.5Gi. #2210 (bounded window, skip refused events) is on main.
* Succeeded run: execution `job-live-receiver-29921670` (22:30 UTC) ended 22:55:56 with stdout `receipts=5220` and no `rejected=` line, so the bounded-window fix works as designed and no refused event occurred in that window.
* Failed run, cause captured: execution `job-live-receiver-29921700` (23:00 UTC) failed one minute in; the live replica stream recorded `2026-11-21T23:01:11Z stderr F Cannot run: SENSOR_SQL_UNAVAILABLE`. That is the exit-2 `StreamError` path of `live_receiver.main`. Finished replicas are not retained (`ExecutionReplicaNotFound`) and the Log Analytics workspace still denies this client (`NspValidationFailedError`), so older failures remain unexplained and the numeric exit code is inferred from the code path, not read.
* Why it fails the whole window: `SensorConsumer._connect` and `_write` map any SQL driver error to `SENSOR_SQL_UNAVAILABLE`, and `HubReceiver.on_event` turns the first one into a fatal failure. One transient database refusal therefore costs the remaining 24 minutes of the window. The reason the database refused (for example a transient token or connection fault) is not observable from here and is unproven.
* Store and map (signed in, staff app, 22:45 UTC): `/api/map` returned 443 homes; the first item carried `sensor.observed_at` `2026-11-21T22:45:00Z`, `age_seconds` 24, `state` `fresh`, source "Synthetic simulator reading". `/api/cases/{id}/sensors` for `ZF-2025-0029`, `ZF-2025-0030` and `ZF-2025-0031` returned `state` `ok`, `freshness` `fresh`, twelve readings at five minute steps (21:50 to 22:45 for `ZF-2025-0031`), reading ids `LIVE-S...-<UTC slot>`. `ZF-2025-0148` and `ZF-2025-0331` returned `consent-withheld`. The [overview screenshot](../../../.copilot-tracking/evidence/2026-11-21/issue-2201-live2/employee-map.png) shows the map section with 443 homes.

## Source change (full tier)

`HubReceiver` in a bounded window now retries an unavailable SQL store up to four times (2, 5, 15 and 30 seconds) before failing; `SENSOR_COMMIT_UNCERTAIN` and every other code stay fatal at once. `live_receiver` prints `sql_retries=N` on a normal end. Tests in `src/api/tests/test_iot_stream.py`: a transient failure is retried and stored once, exhausted retries stay fatal after three attempts, an uncertain commit is never retried. Local results: 104 tests in `test_iot_stream`, `test_live_control` and `test_live_receiver_sql` pass (2 skipped), `ruff check`, `ruff format --check` and `mypy` (src/api) clean. The complete gate is a coordinator step and was not run.

## Per-criterion table

| Criterion | Verdict | Basis |
| --- | --- | --- |
| Root cause recorded with evidence (logs, exit code) | Partly proven | Two causes with evidence: the old deadline-as-failure defect (source, test, then a Succeeded 25 minute run on the fixed image) and captured `Cannot run: SENSOR_SQL_UNAVAILABLE` stderr lines for executions 29921700 and 29921730. Not proven: the cause of the database refusal, the numeric exit code, and the cause of older failures (logs unavailable) |
| Fix merged and deployed | Partly proven | The bounded-window fix is merged (#2210) and the job image was updated at 21:33 UTC (Succeeded run 29921670 follows). The SQL retry is a local commit only; no push, image build or job update was authorised, and the registry denies this client |
| Three consecutive scheduled runs Succeeded | Unproven | Latest executions after the 21:33 update: 22:00 Failed, 22:30 Succeeded, 23:00 Failed, 23:30 Failed. No three-in-a-row streak exists, and the retry that targets the observed failure is not deployed |
| Readings from IoT Hub appear in the store and the employee map, with timestamps | Proven for the demo | Map item and case sensors responses above carry UTC `observed_at` within 30 seconds of the request, contiguous at five minute steps through 22:45. Reading ids follow the `LIVE-<sensor>-<slot>` form of the receiver and simulator; the hub-to-store hop is inferred from the live path, not isolated by a per-message trace |

## Final read

Read at 2026-11-21 23:53 UTC: 52 retained executions, 43 Failed and 9 Succeeded. Executions after the 21:33 job update: 22:00 Failed, 22:30 Succeeded, 23:00 Failed, 23:30 Failed. Execution `job-live-receiver-29921730` (23:30) was also captured: `2026-11-21T23:47:05Z stderr F Cannot run: SENSOR_SQL_UNAVAILABLE`, 17 minutes into the window, which matches the earlier unexplained failures about 16 minutes in. Two captured failures, one minute and 17 minutes into a window, name the same code, so the cause is a transient SQL refusal at an arbitrary moment, not a fixed event offset. The retry in this commit targets exactly that.

## Next steps

* Owner or coordinator: build and deploy the image to `job-live-receiver` (and the simulator if desired), then observe three scheduled windows and read `sql_retries=` in the replica stream.
* Optional, owner decision: allow this client in the Log Analytics network rule to read `ContainerAppConsoleLogs_CL` and name the database fault.

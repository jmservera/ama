---
title: Issue 184 live chain from simulator to map (demo, 2026-11-22 20:20 UTC)
description: Read only proof that scheduled simulator runs reach IoT Hub, the receiver and the employee map, with the resident side and per-message tracing stated as unproven
ms.date: 2026-11-22
ms.topic: reference
---

Scope: synthetic demo, desktop only, resource group `ama`. Azure was read only (job execution lists, hub route and metrics, Log Analytics queries, one browser session per app); nothing was created or changed, so nothing needs deleting. Sign-in values were read at runtime and never printed; screenshots show no credential and emails are masked. Refs #184.

## Evidence

Recorded under `.copilot-tracking/evidence/2026-11-22/issue-184-live/`: `job-live-simulator-executions.json`, `job-live-receiver-executions.json`, `hub-routes.txt`, `hub-metrics.txt`, `summary-lines.json`, `sim-publish-counts.json`, `secret-scan.json`, `probe.py`, `probe-result.json`, `employee-map.png` and `resident-signed-in.png`. Reads ran between 20:18 and 20:23 UTC.

## Chain, hop by hop

| Hop | Observation | Strength |
| --- | --- | --- |
| Simulator job | `job-live-simulator`, schedule `0,7,15,22,30,37,45,52 * * * *`; the latest 8 executions to 20:16:58 are all Succeeded; slot lines show `homes=288 sent=251 to 270 failed=0 retries=0` from 18:00 to 20:05 | Observed |
| Devices | 12,198 publish lines in 6 hours across 288 distinct devices; every device id starts `SYN-`, none other | Observed |
| IoT Hub | `iot-cutover-test-rzsrg` (B1, Active); route `all-device-messages` (DeviceMessages) to `api-telemetry`, enabled | Observed |
| Hub to endpoint | `d2c.telemetry.ingress.success` equals `d2c.endpoints.egress.eventHubs` in every hour: 2092, 2078, 2063, 2087, 2054, 2086 (14:00 to 19:00) and 784 for the partial 20:00 hour | Observed |
| Receiver job | `job-live-receiver`, every 30 minutes; 19:30 Succeeded (ended 19:55:30); the 20:00 run was still Running at 20:18, normal for a run of about 25 minutes; `receipts=1024` to `1052` at 18:25, 18:55, 19:25 and 19:55 | Observed |
| Receiver errors | no `Cannot run`, `Traceback`, `IOT_CALLBACK` or `SENSOR_SQL` lines in the 6 hour summary query | Observed |
| SQL | the receiver and the staff app use the SQL store (jobs carry `ZF_STORE`, `ZF_SQL_SERVER` and `ZF_SQL_DATABASE`; values not read); readings written by the receiver are served by the case sensors route, below | Inferred, not traced per message |
| Employee map and sensors | `/api/map?zoom=14` returned 200 with 443 items; `/api/cases/ZF-2025-0030/sensors` returned `ok`, `fresh`, 12 readings, latest `2026-11-22T20:15:00Z` (about 7 minutes before the probe at 20:22Z); the map page rendered (see `employee-map.png`) | Observed |

Other probed cases: `ZF-2025-0331` returned `ok`, `stale`, latest `2026-11-22T20:05:00Z`, which is consistent with the simulator skipping 18 to 37 of 288 homes per slot; `ZF-2025-0031` returned `consent-withheld`, which hides values by design.

## Resident side

The resident showcase login returned 200 and `/demo/view` carries a `sensors` block (48 history points, 6 forecast points, `synthetic: true`). For this test account the history ends at `2026-11-22T03:30:00Z` and the freshness text is retained, "stored readings, not live". The account's sensor consent state is `declined` and the card says new readings are not stored for the home. The resident view therefore shows stored synthetic history, not the live stream, for this account. Switching consent on is a write to the demo store and was outside a read only run.

## Secrets

A Log Analytics count over 6 hours of all `job-live-*` console lines for `SharedAccessKey=`, `HostName=...;DeviceId=` and `SharedAccessSignature sr=` returned 0. Job environment names were listed without values, and the SDK debug lines print `REDACTED` for identity headers. A source search for the same patterns matches only `src/core/tests/test_live_provisioning.py`, `src/api/tests/test_iot_credential_hygiene.py` and `infra/tests/test_network_posture.py`, which hold the patterns as test data. Whole-source exclusion over history was not re-run.

## Per-criterion table

| Criterion | Verdict | Basis |
| --- | --- | --- |
| All child stories closed or deferred | Proven | #185, #186, #187, #188 and #189 report `closed` via the sub-issues API |
| Simulator never connects to, discovers or represents installed real devices | Proven for live traffic; code guard not re-read | 288 of 288 devices in 6 hours of publish lines are `SYN-` ids; the simulator source accepts only `SYN-` file names (`live_simulator.py` line 48) |
| No device key or connection string in source, logs or telemetry | Proven for the last 6 hours of logs and the current source tree; telemetry content not inspected | 0 secret pattern matches in logs; source matches are test fixtures only |
| Live simulator to Hub to receiver to SQL to employee map | Proven for the demo, with the SQL hop inferred | Tables above; no per-message trace |
| Resident view shows live readings | Unproven | Test account declined consent; history ends 2026-11-22T03:30Z |

## Defects

None found, so no source change was made and the focused tier applies.

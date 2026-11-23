---
title: Issue 184 live re-check (demo, 2026-11-23)
description: Fresh read-only proof for the three acceptance criteria of the live IoT Hub streaming issue, with the limits stated
ms.date: 2026-11-23
ms.topic: reference
---

Scope: synthetic demo, desktop only, resource group `ama`. Azure was read only (job executions, hub metrics, one Log Analytics count query, one container log read); nothing was created, so nothing needs deleting. No credential was read or printed. All three criteria were already ticked in the issue; this note re-checks them. Refs #184.

## Evidence

Recorded under `.copilot-tracking/evidence/2026-11-23/issue-184-live/`: `sim-executions.json`, `receiver-executions.json`, `hub-metrics.txt` and `secret-scan.json`. Reads ran at about 03:30 to 03:40 UTC.

## Per-criterion result

| Criterion | Result | Evidence and limits |
| --- | --- | --- |
| All child stories closed or deferred | Proven for the demo | `gh api repos/jmservera/ama/issues/184/sub_issues` returns #185 to #189, all `closed` with reason `completed` (2026-11-23). Earlier notes: [demo](issue-184-child-stories-demo-2026-11-19.md) and [live re-check](issue-184-child-stories-live-2026-11-19.md). A backlog state, not a quality verdict on each child |
| Simulator never connects to, discovers or represents installed real devices | Proven for the demo, constructed plus live | Local: `test_iot_stream.py` rejects an `installed-real-device` binding and an `installed-device.invalid` activation; 170 tests across the IoT stream, credential hygiene, simulator, control and receiver suites pass (2 skipped), run from `src/api` at this commit. Live: all simulator job executions to 03:30 UTC are Succeeded, devices are `SYN-` ids only (12,251 `SYN-` log lines in 6 hours, see the [chain note](issue-184-live-chain-2026-11-22.md) for the per-device count). Limit: the data-plane device list is unauthorised for the CLI identity (401002), so the Hub identity registry itself was not enumerated |
| No device key or connection string in source, logs or telemetry | Proven for source and logs; telemetry unproven | Source: `test_iot_credential_hygiene.py` scan of `src`, `infra`, `docs`, `.github` passes. Logs: Log Analytics count over 260,243 `ContainerAppConsoleLogs` rows in 6 hours matched 0 for `SharedAccessKey=`, `SharedAccessSignature sr=`, a device connection string or a private key block. Hub metrics: ingress 2117, 2054, 2092, 2066, 2080, 2110 equals egress within retry noise (2118, 2033, 2114, 2062, 2075, 2118) per hour. Limit: payload bodies in Event Hubs were not read, so absence of secrets in message content is shown only by the constructed fake-SDK test, not live |

## Live chain still healthy

Simulator job `job-live-simulator` ran every 7 to 8 minutes, latest execution `job-live-simulator-29923410` Succeeded at 03:30; `job-live-receiver` runs every 30 minutes (03:00 Succeeded, 03:30 Running). Hub `iot-cutover-test-rzsrg` is B1, Active, route `all-device-messages` (DeviceMessages) to `api-telemetry`, enabled.

## Outcome

No code gap found; no source change. The only unproven element is secret absence in live message bodies, which needs an Event Hubs data read that was not made.

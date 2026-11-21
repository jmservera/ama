---
title: Issue 184 live demo simulator and consent mix research
ms.date: 2026-11-20
---

Task: issue-184-live. Owner request 2026-11-20 (authoritative): start the live simulator in the demo so
fresh readings reach `sensor_reading` under 15 minutes old, and give about half of the synthetic homes
granted monitoring consent through repository code. Research disposition: executed. Planning Readiness: Ready.

## Live baseline (read-only, 2026-11-21 00:30 UTC, through a throwaway job as `id-cutover-test-api`)

* No simulator or receiver job exists; `ca-cutover-test-demo-api` image already contains `live_simulator`, `live_receiver`, `live_control`, `iot_stream`, `sensor_ingestion` and `azure.iot.device` (X.509 client). `azure.iot.hub` is not installed, so the repo registry adapter cannot run in that image.
* SQL: `sensor_reading` 830 rows, newest synthetic live readings 2026-11-19 10:50 for ZF-2025-0029/30/31; `sensor_consumer_control` 3 (all granted), `sensor_consumer_control_home` 3, index marker count 3 v2; policy and mapping windows ended 2026-11-19, so new readings would be rejected even for the granted homes. 443 open cases.
* Hub `iot-cutover-test-rzsrg` B1, public access Disabled, local auth disabled, route `all-device-messages` to endpoint `api-telemetry` (`eh-iot-cutover-test-rzsrg/sensor-readings`, consumer group `api-consumer` present, 2 partitions, 24 h retention). `id-cutover-test-api` holds Event Hubs Data Receiver on that event hub.
* Storage account `stcutovertestrzsrg` has shared-key access disabled, so the Azure Files environment storage that `live-simulator-job.bicep` and `live-receiver-job.bicep` assume cannot be registered without an estate security change.
* `az containerapp exec` is rate limited (429, retry 600 s); throwaway Container Apps jobs started from an ARM body work and return logs.

## Source facts

* `SensorConsumer.configure(policy, controls)` replaces the whole policy and control set (at most 100) and rewrites `sensor_consumer_control_home` and the index marker; `sensor_view.consent` returns granted only when every control of the home is granted and indexed, declined when any control declines, otherwise unknown. A home with no control therefore shows Readings withheld.
* The receiver reads Event Hub from the start of retention each window (no checkpoint) and counts duplicates against `--events`, so the window event cap must exceed the retained backlog.
* `IotHubSink` is X.509 only; device identity is `SYN-` plus `sensor_identity.sensor_key(home)`. The control document allows at most 100 homes and 14 days.

## Approach options considered

| Option | Result |
| --- | --- |
| Deploy the two Bicep jobs unchanged with Azure Files storage | Blocked: no shared-key storage |
| Enable shared key on the existing account or create a new shared-key account | Estate security change; rejected |
| Add a `Secret` volume source and optional schedule to the two job templates, keep every other guard | Chosen: no new resource, certificates and control document held as job secrets |
| Ad-hoc driver with SAS keys | Rejected: owner asked for the repository jobs |

## Acceptance criteria of #184 (all three already ticked on the issue)

Research for each is carried to the changes record table. Child stories #185 and #189 remain open without owner deferral and cannot be closed by this run.

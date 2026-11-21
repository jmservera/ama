---
title: Issue 184 live demo, simulator running and consent mix
description: Record of starting the IoT simulator and receiver on the live synthetic demo and giving about half of the cohort homes granted monitoring consent through repository code, with live readbacks
author: AMA RPI agent
ms.date: 2026-11-20
ms.topic: reference
keywords:
  - issue 184
  - iot hub
  - simulator
  - sensor consent
estimated_reading_time: 8
---

Refs #184. Scope is the synthetic desktop demo in resource group `ama`. The owner asked on 2026-11-20 for fresh readings flowing IoT Hub, Event Hub, receiver and `sensor_reading`, and for roughly half of the demo homes to show granted monitoring consent while the rest show none or declined. All data is synthetic and no resident consent is claimed. Owner decisions of 2026-11-18 apply (cap USD 700, no drills, no Key Vault rotation, no production change). Sign-in values were read at run time and never printed.

## What was set up

* Cohort of 20 synthetic homes: ZF-2025-0029, 0030, 0031, 0032, 0041, 0054, 0090, 0098, 0101, 0111, 0113, 0119, 0122, 0123, 0141, 0148, 0150, 0151, 0152, 0153. Each has one X.509 device identity (self-signed EC certificate generated locally, thumbprint registered on the hub). Key material lived only in a 0700 directory and a secure parameter file, both shredded afterwards.
* `job-live-simulator` (Container Apps job, cron `*/5 * * * *`, identity `id-cutover-test-internal`) publishes one reading per cohort home per 5 minute slot over MQTT on WebSocket.
* `job-live-receiver` (cron `*/30 * * * *`, identity `id-cutover-test-api`, `--seconds 1500 --events 20000`) reads Event Hub consumer group `api-consumer` over AMQP on WebSocket and ingests through `SensorIngestion`. Windows do not overlap, and the gap between windows is about 5 minutes.
* Both jobs deploy from `infra/live-simulator-job.bicep` and `infra/live-receiver-job.bicep` with the new opt-in parameters (Secret volume instead of Azure Files, `containerHardening=off`, `useWebSockets=true`, `systemOrigin=true` on the receiver). Approval reference `OWNER-2026-11-20-demo-184`. The parameters are documented in [infra/README.md](../../../infra/README.md).
* Consent mix by `tools/demo_consent_mix.py`, which calls `SensorConsumer.configure` (policy, controls, per-home index and index marker rewritten together). Result: 10 controls granted, 10 declined, 20 `sensor_consumer_control_home` rows, 20 index markers. Control window now-2h to +13 days, so the controls expire on 2026-12-04. Homes outside the cohort have no control and show Readings withheld.

## Why the code needed changes

Each point was found by a live failure, then fixed with a test.

* The hub and Event Hub private endpoints answer on 443 only (8883 and 5671 time out), so both clients needed WebSocket transport (`ZF_SIM_WEBSOCKETS=1`, off by default).
* Azure Files is unusable here because storage shared-key access is disabled, so the jobs mount a Container Apps Secret volume (41 secrets). `certStorageName` is now optional.
* The image refuses `ZF_CONTAINER_HARDENING=enforced` on Container Apps (the same refusal the app shows), so the jobs use `off`, as the app does. This is a demo-only deviation.
* The live `sensor_reading` table is an updatable ledger table with four hidden `ledger_*` columns, which made `SensorConsumer.configure` raise `SENSOR_SCHEMA_UNSUPPORTED`. `_check_reading_schema` now ignores `ledger_*` columns (test `LedgerSchemaTests`). The first consent run used a runtime shim for the same filter because the deployed image predates the fix.
* The hub stamps the device id and auth method as message annotations, while the repository treated those keys as ambiguous. With `ZF_SIM_SYSTEM_ORIGIN=1` the receiver reads the origin from the annotations, still refuses any origin copy in device-set application properties and refuses modules. The hub writes the auth type as `x509Certificate`, which is accepted only in this mode. This is a security-relevant decode change and needs independent review before any wider use.
* WebSocket close takes about 1 s, above the 0.5 s cleanup allowance, so the allowance is 3 s only when `ZF_SIM_WEBSOCKETS=1`.

## Live proof

Probe jobs ran read-only SQL through `id-cutover-test-api` and were deleted after each run.

| Check | Result |
| --- | --- |
| Hub d2c metrics (`az monitor metrics list`, hourly total) | `d2c.telemetry.ingress.success` 160 and `d2c.telemetry.egress.success` 160 in the first hour after start |
| Newest `sensor_reading`, probe at 02:30:32 UTC | slot 02:20:00 (10 minutes old, receiver window ended 02:25) |
| Newest `sensor_reading`, probe at 02:56:10 UTC | slot 02:55:00 (about 1 minute old) |
| Rows and delivery, 02:56 UTC | 1030 readings; `sensor_delivery`: 317 ACCEPTED, 200 rejected CONSENT (declined homes), 3 IDENTITY_CONFLICT and 3 OUT_OF_ORDER (the older baseline) |
| Cron cadence | simulator `Succeeded` every 5 minutes from 01:35; receiver scheduled windows at 02:00 and 02:30 ran their full window |
| Granted home ZF-2025-0031 in the staff app | `/api/cases/ZF-2025-0031/sensors` returns state `ok`, freshness `fresh`; the Home sensors tab reads "Recent reading (within 15 minutes)" and "Latest reading 21 Nov 2026, 01:55 (UK time), less than a minute ago" ([screenshot](./issue-184-live-demo-granted-home-2026-11-20.png)) |
| Granted home ZF-2025-0032 | state `ok`, freshness `fresh` |
| Non-granted home ZF-2025-0148 (declined) and ZF-2025-0331 (no control) | state `consent-withheld`; the tab reads "Readings withheld: monitoring consent is not granted" ([screenshot](./issue-184-live-demo-withheld-home-2026-11-20.png)) |
| App hardening | `ZF_CONTAINER_HARDENING` is `off` on `ca-cutover-test-demo-api`; the app was not redeployed or changed |

The staff sign-in used Playwright against `ca-cutover-test-demo-api`; the account email and password came from the owner's files at run time and appear in no output.

## Backlog and freshness behaviour

The receiver starts at the retention start with no checkpoint, so each window replays the retained backlog and `sensor_delivery` records duplicates and out-of-order frames as rejections. The first window after the fix (started 01:49:38 UTC) ingested the backlog and fresh slots within about 2 minutes (newest 01:50 at 01:51:57). With 20 homes every 5 minutes, volume is 5,760 messages a day, well inside the B1 hub quota.

A window that reaches its deadline ends with the repository's fixed code `RUN_DEADLINE` and exit code 2, so the Container Apps execution shows `Failed` at the end of every window. This is the repository's designed exit, not a delivery failure, and the next cron tick starts a fresh window. The age of the newest reading stays at most about 10 minutes (5 minute gap plus one slot), under the 15 minute target.

## ACR push window

Three images were pushed (`demo184-ws`, `demo184-ws2`, `demo184-ws3`; the jobs use digest `sha256:899670a114856ce864424feb136c9f2b31b9205cfa0aba3c4d3379d10bf57cc5`). Each push followed the documented short window: export policy enabled, public access enabled, one IP rule for the worker address, push, then the rule removed, public access disabled and export disabled. Final readback of `crcutovertestrzsrg`: `publicNetworkAccess` Disabled, default action Deny, 0 IP rules, export policy disabled.

## Stop and teardown

* Stop sending: `python -m zava_forward.api.live_control stop` against the control file, or let it expire on 2026-12-04. Then `az containerapp job delete -n job-live-simulator -g ama` and the same for `job-live-receiver`.
* The device identities remain registered on the hub. Remove them (and the secret values in the job definitions) when the demo ends.
* Temporary resources removed: role "IoT Hub Registry Contributor" on `id-cutover-test-api` (read back as 0 assignments), every throwaway probe job (the final job list shows the three pre-existing demo jobs plus the two live jobs), local certificate directory and parameter files (shredded).
* A secret scan of the diff and new files found no private key, shared access key or connection string.

## Acceptance criteria of #184

| Criterion | Status | Evidence |
| --- | --- | --- |
| All child stories closed or deferred | Proven for the demo | `gh issue view 185` and `gh issue view 189` read CLOSED on 2026-11-20 |
| Simulator never connects to, discovers or represents installed real devices | Proven for the demo | Only the 20 registered synthetic device identities publish; each reading carries `source_type SYNTHETIC` and a cohort `ZF-` home; the simulator job has no discovery code path ([simulator tests](../../../src/api/tests/test_iot_stream.py), 40 passing) |
| No device key or connection string in source, logs or telemetry | Proven for the demo | The diff scan found none; job logs showed only fixed codes; keys were supplied through a secure parameter file that is now shredded. Key material remains in the Container Apps Secret volume of the two jobs until teardown |

## Limits

* This is a demo-profile run. The Secret volume, hardening off and WebSocket settings are not a production design.
* The `ledger_*` filter and system-origin decode have unit tests but no independent review yet.
* Hosted CI and the full local gate were not run here; the coordinator owns them. No `rpi-checks.py --all` was run.
* The staff app now runs revision `ca-cutover-test-demo-api--0000038`; this run did not create it.

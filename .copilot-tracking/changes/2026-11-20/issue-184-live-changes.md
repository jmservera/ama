---
title: Issue 184 live changes record
ms.date: 2026-11-20
---

Refs #184. Tier: FULL applies (src and infra changed); the coordinator owns the complete gate. No `rpi-checks.py --all` was run here.

## Changes

| Path | Change |
| --- | --- |
| `infra/live-simulator-job.bicep`, `infra/live-receiver-job.bicep` | Optional `certStorageName`; `@secure() secretFiles` Secret volume; `containerHardening`; `useWebSockets`; receiver `cronExpression`, `maxEvents`, `systemOrigin`. Defaults keep earlier behaviour. |
| `infra/tests/test_bicep_containerapp_demo_wiring.py` | Assertions updated for the opt-in secret volume. |
| `infra/README.md` | Single-environment demo profile section. |
| `src/core/src/zava_forward/core/sensor_consumer.py` and test | Hidden `ledger_*` columns ignored in the schema check. |
| `src/api/src/zava_forward/api/iot_stream.py` and tests | Opt-in WebSocket transport, opt-in system-origin decode (security-relevant, needs independent review), 3 s cleanup allowance under WebSocket. |
| `src/api/src/zava_forward/api/live_simulator.py` | `ZF_SIM_WEBSOCKETS` selects WebSocket MQTT. |
| `tools/demo_consent_mix.py`, `tools/test_demo_consent_mix.py` | Cohort planner and apply through `SensorConsumer.configure`. |
| `docs/reference/research/issue-184-live-demo-sim-consent-mix-2026-11-20.md` (+2 PNG), `docs/reference/README.md`, `docs/reference/log.md` | Evidence note, index and log. |

## Live actions (resource group `ama`)

* 20 device identities registered; 2 jobs deployed (`job-live-simulator` every 5 minutes, `job-live-receiver` every 30 minutes with a 1500 s window); consent mix applied 10 granted and 10 declined.
* Three images pushed through the documented ACR window; final readback Disabled, Deny, 0 rules, export disabled.
* Temporary registry role removed; throwaway jobs deleted; key files shredded. App untouched (`ZF_CONTAINER_HARDENING=off`).
* Not done: stopping or deleting the live jobs (they must keep running for the demo); device registrations remain.

## Local validation

* `test_iot_stream` 40 tests OK; `test_sensor_consumer*` 52 OK; `tools/test_demo_consent_mix.py` 3 OK; infra Bicep wiring tests 22 OK; both Bicep files compile; ruff check and format clean on changed files; mypy shows only the pre-existing `opentelemetry` import errors (7 in `src/core/tests`). `test_container_hosting_144` cannot import `opentelemetry` locally (pre-existing).
* Hosted CI, the full gate and the web-UI gates were not run (no web UI file changed).

## Per-criterion table

| Criterion | Proven or unproven | Evidence |
| --- | --- | --- |
| Owner: simulator running, readings flow hub to `sensor_reading` | Proven | Hub d2c ingress and egress 160 each; 1030 readings by 02:56 UTC |
| Owner: readings under 15 minutes old | Proven for observed samples (2, 10 and 1 minutes); bound about 10 minutes by cadence | Research note, live proof table |
| Owner: about half of homes granted through repository code | Proven | 10 granted, 10 declined, 20 index markers via `SensorConsumer.configure` |
| Owner: granted home shows Recent reading, non-granted shows Readings withheld | Proven | Playwright text and two screenshots |
| Owner: no app redeploy, hardening off, ACR window restored | Proven | App env `off`; ACR readback |
| #184: all child stories closed or deferred | Proven | #185 and #189 CLOSED |
| #184: never connects to real devices | Proven for the demo | 20 synthetic identities only |
| #184: no device key or connection string in source, logs or telemetry | Proven for the demo; keys sit in the jobs' Secret volume until teardown | Diff scan, fixed-code logs |
| Independent review of the decode and ledger changes | Unproven | Required before any non-demo use |

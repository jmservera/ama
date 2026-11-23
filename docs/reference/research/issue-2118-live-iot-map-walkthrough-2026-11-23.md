---
title: Issue 2118 live IoT Hub to SQL to map walkthrough (demo, 2026-11-23)
description: Read only walkthrough of the live chain from simulator and IoT Hub through the receiver to a fresh employee map reading, with the per message SQL hop and the resident live view stated as unproven
ms.date: 2026-11-23
ms.topic: reference
---

Scope: synthetic demo, desktop only, resource group `ama`, live API revision `ca-cutover-test-demo-api--0000054` and resident revision `ca-resident-demo--0000026`, `origin/main` at `dbf4e45fa7`. Azure was read only and one Playwright session per app was used; nothing was created or changed, so nothing needs deleting. Sign-in values were read at runtime and never printed. Refs #2118.

## Evidence

Recorded under `.copilot-tracking/evidence/2026-11-23/issue-2118-live/`: `hub.json`, `hub-routes.txt`, `hub-metrics.json`, `job-live-simulator-executions.json`, `job-live-receiver-executions.json`, `revisions.txt`, `probe.py`, `probe-result.json`, `trace.py`, `trace-result.json`, `employee-map.png` and `resident-signed-in.png`. Reads ran 01:44 to 01:47 UTC.

## Walkthrough, hop by hop

| Hop | Observation | Strength |
| --- | --- | --- |
| Simulator job | `job-live-simulator` latest six executions, 01:00 to 01:37 UTC, all Succeeded | Observed |
| IoT Hub | `iot-cutover-test-rzsrg` (B1, Active); route `all-device-messages` on DeviceMessages, enabled | Observed |
| Hub to endpoint | in the metric window `d2c.telemetry.ingress.success` and `d2c.endpoints.egress.eventHubs` both total 2095 | Observed |
| Receiver job | `job-live-receiver` executions at 23:00, 23:30, 00:00, 00:30 and 01:00 Succeeded; the 01:30 run was Running at 01:45 | Observed |
| SQL | the receiver and staff app use the SQL store; the freshest reading is served from it, but no per message trace was taken | Inferred |
| Employee map | `/api/map?zoom=14` returned 200 with 443 items; for `ZF-2025-0030` the map `sensor` object was `fresh`, label "Recent reading (within 15 minutes)", `observed_at` `2026-11-23T01:45:00Z`, age 79 s, source "Synthetic simulator reading. Not calibrated" | Observed |
| Case sensors route | `ZF-2025-0030` and `ZF-2025-0331` returned `ok`, `fresh`, 12 readings, latest `2026-11-23T01:35:00Z` at 01:45 UTC; `ZF-2025-0031` returned `consent-withheld` by design | Observed |

A reading whose timestamp is 79 seconds old at the map implies the live stream reaches the UI faster than the 30 minute receiver cadence alone suggests; the mechanism for the 01:45 reading was not traced and is not claimed here.

## Resident side

The resident showcase login returned 200 and `/demo/view` carries a `sensors` block (48 history points, 6 forecast points, `synthetic: true`). History ends `2026-11-22T03:30:00Z` and the text reads "stored readings, not live". Sensor consent for this account is `declined`, so new readings are not stored for the home. Enabling consent is a write to the demo store and was outside a read only run.

## Limits

* The follow-up trace call for reading identifiers and provenance returned empty values for the sensors route (`trace-result.json`); the map object is the evidence for the fresh reading. Reading ids were therefore not recorded this run, unlike the [2026-11-22 recheck](./issue-2201-live-receiver-recheck-2026-11-22.md).
* The map screenshot caught the overview in its loading state ("Loading map records"); the verdict rests on the API responses, not the picture.
* The Log Analytics workspace is private-link only for this caller, so job log lines were not read.
* Earlier notes: [live chain 2026-11-22](./issue-184-live-chain-2026-11-22.md) and the [1818 walkthrough](./issue-1818-live-iot-map-walkthrough-evidence-2026-11-18.md).

## Comparison with main

`src/api/tests/test_map_sensors.py` passes (16 tests) on `dbf4e45fa7`. The map projection, freshness labels and consent handling the live probe saw match the tested behaviour. No code gap was found, so no source file changed.

## Per-criterion table

| Criterion | Verdict | Basis |
| --- | --- | --- |
| Live Azure IoT Hub to SQL to UI map walkthrough is recorded separately once live transport is active | Proven for the demo, with the per message SQL hop inferred | Live transport is active (Succeeded simulator and receiver runs, ingress equals egress) and the walkthrough above ends in a fresh map reading 79 s old. Tick it only if the owner accepts the inferred SQL hop |
| Resident sensor view shows live readings | Unproven | Test account consent is `declined`; the view shows stored history. Not a criterion of this issue, listed for clarity |

No box is ticked by this note.

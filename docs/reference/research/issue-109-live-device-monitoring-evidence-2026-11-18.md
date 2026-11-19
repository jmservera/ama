---
title: Live in-use device monitoring evidence for issue 109 (demo)
description: Recorded run on 2026-11-18 against the demo IoT Hub showing device connection state, the behaviour of lastActivityTime and a connectivity metric alert, with a per-criterion proven or unproven table for epic 109
author: AMA RPI agent
ms.date: 2026-11-18
ms.topic: reference
keywords:
  - issue 109
  - IoT Hub
  - device connectivity
  - lastActivityTime
estimated_reading_time: 6
---

Refs #109. Scope is the synthetic desktop demo, authorised by the owner on 2026-11-18 (resource group `ama`, cap USD 700, no drills, no Key Vault rotation, no production changes). Nothing here is production, calibration or resident evidence. No source files changed and no browser proof applies, because no user interface was touched.

## Method

The hub `iot-cutover-test-rzsrg` (Basic B1, uksouth) is private (public network access Disabled, local auth disabled), so a throwaway Container Apps job `job-109-probe` in `cae-cutover-test-demo` ran the probe with the demo API image and the managed identity `id-cutover-test-api`. The identity held IoT Hub Registry Contributor on the hub for the run only. The probe (kept outside the repository) did this, with no credentials printed:

* Created one SAS device `probe109-<epoch>` through the registry REST API and read its identity.
* Connected over MQTT on WebSockets (the earlier plain MQTT attempt failed with `ConnectionFailedError`; the demo hub is only reachable this way) and sent two simulated humidity and temperature messages.
* Re-read the identity while connected (about 20 s and 60 s) and after disconnect (5 s, 65 s, 185 s), then deleted the device.
* Created a throwaway Azure Monitor metric alert on the hub: `avg devices.connectedDevices.allProtocol < 1`, window 5 minutes, frequency 1 minute, severity 3, no action group.

## Observed

| Time (UTC) | Observation |
| --- | --- |
| 08:38:58 | Device created. `connectionState` Disconnected, `lastActivityTime` `0001-01-01T00:00:00Z` (never active). |
| 08:39:19 and 08:39:59 | `connectionState` Connected, `connectionStateUpdatedTime` 08:38:58.96Z. |
| 08:40:04, 08:41:04, 08:43:05 | `connectionState` Disconnected, `connectionStateUpdatedTime` 08:39:59.76Z. |
| all reads | `lastActivityTime` stayed `0001-01-01T00:00:00Z`, including about four minutes after two successful messages. |
| 08:40 (metric) | `d2c.telemetry.ingress.success` total 2 for the probe messages. A total of 3 at 08:28 predates the probe and is unrelated hub traffic. |
| 08:40 (metric) | `devices.connectedDevices.allProtocol` maximum 1 in the minute of the probe connection; 0 in all other minutes from 08:24 to 08:43. |
| 08:38:41 | Alert `alert-109-probe-connectivity` fired (monitor condition Fired, state New) because no device was connected. |

## Interpretation

* Connection state is observable per device from the hub, with a state-change timestamp, and the hub exposes fleet connectivity as a metric.
* The IoT Hub `lastActivityTime` field is not a usable per-device last-activity signal for MQTT telemetry in this setup: it never moved. A last-activity view for the demo has to come from the stored readings (for example the newest `observed_at` per sensor, which is what `sensor_view.py` freshness and `sensor_analysis.py` `STALE` already use) rather than from the hub identity.
* The metric alert rule can be created and evaluates on the hub metric. It fired on the "no device connected" condition. Notification delivery was not tested, because no action group was attached, and the metric reported the single connected minute with a delay, so alert timing is not an operational latency figure.

## Per-criterion result

| Criterion in #109 | Result | Evidence or reason |
| --- | --- | --- |
| Complete the #440 stabilisation checkpoint before epic closure | Unproven | It is a coordinator and owner process outcome (reconcile BRD, PRD and ADR, regression runs, bug disposition, residuals, pivot or defer decision). A live hub probe cannot satisfy it, and merged children alone do not. Two #440 criteria are also still unticked there (finding triage, review artifacts). |
| All child features closed or deferred | Unproven | On 2026-11-18 children #110, #111, #184 and #1818 are open and no deferral decision is recorded. This run adds device connectivity and alert evidence only. |
| No sensor signal diagnoses a hazard, starts a clock, releases a hold or changes ranking | Already ticked; this run adds nothing | No signal logic was exercised or changed. |
| Demo aim: device last-activity visible on the hub | Partly proven | Connection state and its timestamp were observed. `lastActivityTime` did not update, so last-activity is not proven from the hub; it remains a stored-reading concept. |
| Demo aim: connectivity alert | Proven for rule creation and firing, not delivery | Alert fired on the hub connected-devices metric. No notification, owner routing or human review task was tested. |

## What this does not prove

* X.509 device authentication, the production `api-consumer` receiver and a Standard tier hub are out of scope and unproven.
* One device, one run: no fleet behaviour, no staleness thresholds approved by an owner, no resident consent path.
* The "no signal changes ranking" guarantee relies on the existing code and tests, not on this run.

## Resources and residue

* Created and removed: job `job-109-probe` (two earlier attempts failed before reaching the hub and were deleted; the third ran), metric alert `alert-109-probe-connectivity`, role assignment IoT Hub Registry Contributor for `id-cutover-test-api` on the hub, and the SAS device (delete returned 204).
* After cleanup the hub still reports public network access Disabled and local auth disabled; remaining hub role assignments are the two that existed before.
* Hub metrics (`d2c.telemetry.ingress.success`) retain two datapoints from the probe; nothing was written to SQL.
* Validation tier: focused, no source or test changes.

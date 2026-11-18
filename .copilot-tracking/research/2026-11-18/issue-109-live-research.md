---
title: Issue 109 live research (opening)
ms.date: 2026-11-18
---

Opening note. Goal: prove in-use monitoring of simulated IoT devices on the demo hub `iot-cutover-test-rzsrg` (device last-activity, connectivity alert), no X.509. Disposition: executed. Demo, desktop only, authorised 2026-11-18.

Issue #109 has two unticked criteria: the #440 stabilisation checkpoint and "all child features closed or deferred". Children #110, #111, #184 and #1818 are open.

## Findings (2026-11-18)

* Disposition: executed. Planning Readiness: Ready.
* The repository defines no "device last-activity" or "connectivity alert" feature: FR-048 and AC-090 (BRD) only require stale or missing data to show as insufficient, which `sensor_analysis.py` implements (`STALE`, `max_staleness_hours`). The platform signals are Azure IoT Hub `lastActivityTime`/`connectionState` on the device identity and the Azure Monitor metric `devices.connectedDevices.allProtocol`.
* Hub `iot-cutover-test-rzsrg` (Basic B1, uksouth) is private (public access disabled, local auth disabled), so identity reads need a throwaway Container Apps job with the managed identity `id-cutover-test-api`, which currently holds only Event Hubs Data Receiver on the hub.
* Image has `azure-iot-device`; registry REST can use the managed identity token.
* Children #110, #111, #184 and #1818 are open, so "all child features closed or deferred" cannot be proven. The #440 checkpoint criterion is a coordinator/owner process item, not Azure evidence.

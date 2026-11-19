---
title: Live IoT Hub to Azure SQL ingestion rerun for issue 110 (demo)
description: Recorded 2026-11-18 run of the bounded synthetic live_demo job on the deployed demo, showing three Hub devices sending six readings that were stored in Azure SQL, with cleanup verified
author: AMA RPI agent
ms.date: 2026-11-18
ms.topic: reference
keywords:
  - issue 110
  - iot hub
  - azure sql
  - ingestion
estimated_reading_time: 4
---

Refs #110. Synthetic desktop demo, authorised by the owner on 2026-11-18 (resource group `ama`, cap USD 700, no drills, no Key Vault rotation, no production changes). It extends the [earlier identity note](issue-110-live-iot-identity-evidence-2026-11-18.md), which stopped at Event Hub read-back, with the SQL leg. Nothing here is production evidence.

## Method

* Reused the prior evidence and the #1818 round 7 approach; no new source code.
* Created throwaway job `job-110-live2` in `cae-cutover-test-demo` with the deployed demo API image (the one `ca-cutover-test-demo-api` runs), identity `id-cutover-test-api`, command `python3 -m zava_forward.api.live_demo`.
* Granted that identity two temporary roles: IoT Hub Registry Contributor on the hub, Azure Event Hubs Data Receiver on `evhns-cutover-test-demo`.
* Settings: homes `ZF-2025-0029` to `ZF-2025-0031`, 2 slots each (6 messages, far below the 200 message demo cap), seed 110, cleanup on.
* Retrieved the output with `az containerapp job logs show`; the raw job output was not retained in the repository.

## Result

Execution status Succeeded. Raw output, verbatim:

```text
homes=['ZF-2025-0029', 'ZF-2025-0030', 'ZF-2025-0031'] registered=3 planned_messages=6
homes=3 sent=6 failed=0 stored=6 at=2026-11-18T13:56:40Z
seconds=21.6
```

The module exits 0 only when stored equals sent equals planned. It registers `SYN-` devices with Hub-generated keys, sends each reading with the device's own key, reads Event Hub with Entra and writes through `SensorIngestion` into the demo Azure SQL `sensor_reading`. The module prints no key or token.

## Cleanup (independent read-back)

* Job deleted; no job containing `110` remains.
* Both temporary role assignments deleted; the identity again holds only its five earlier roles.
* `az iot hub show-stats`: 0 total, 0 enabled, 0 disabled devices.
* Hub still has public network access Disabled and local authentication disabled.

## Per-criterion result

| Criterion in #110 | Result | Basis |
| --- | --- | --- |
| C1 Distinct IoT Hub identity per simulated device with schema version and stable reading ID | Observed; raw output not retained | Identity, schema version and message ID per event: earlier note (3 distinct identities, 7 of 7 events with schema version and message ID equal to reading ID). This run adds 3 devices registered, 6 of 6 sent and 6 of 6 stored in SQL |
| C2 Idempotent append on sensor ID plus reading ID | Already ticked; not re-proven | Covered by merged tests |
| C3 Duplicate, out-of-order, unmapped, wrong-unit, clock-skewed, uncalibrated input handled | Already ticked; not re-proven | Merged tests |
| C4 No public unauthenticated ingestion endpoint | Already ticked; consistent with this run | Hub public access Disabled, local auth disabled |
| C5 No device key or connection string in source or telemetry | Already ticked; consistent with this run | No key text in the job output |

## What this does not prove

* Per-device identity detail (device ID, schema version, message ID) is not in this run's output; it rests on the earlier note.
* Row-level SQL contents were not read back independently; the claim rests on the module's `stored=6` self-report and its exit code. No SQL console access was used.
* Identities are Hub-generated symmetric keys over the demo path, an owner decision. Production X.509, the `api-consumer` group receiver and the unmerged receiver fix for new homes stay unproven.
* Tier, sizing, cost, network and credential-owner decisions for production remain human decisions. Message count is 6 of the 200 message cap; no cost was measured.
* No criterion is ticked by this note; the owner ticks.

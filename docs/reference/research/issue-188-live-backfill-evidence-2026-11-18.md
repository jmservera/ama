---
title: Live Azure backfill and live series evidence for issue 188 (demo)
description: Recorded run on 2026-11-18 against live Azure SQL showing backfill and live series queried together per home, the handover seam, and an idempotent re-run
author: AMA RPI agent
ms.date: 2026-11-18
ms.topic: reference
keywords:
  - issue 188
  - sensor backfill
  - handover
  - idempotency
estimated_reading_time: 6
---

Refs #188. Scope is the synthetic desktop demo, authorised by the owner on 2026-11-18 (resource group `ama`, cap USD 700, no drills, no Key Vault rotation, no production changes). Nothing here is production, calibration or resident evidence.

## Method

The SQL server `sql-cutover-test-rzsrg` is private only, so the run used a throwaway Container Apps job in `cae-cutover-test-demo` with the demo API image and the `id-cutover-test-api` managed identity, then removed the job. The driver (kept outside the repository) did this for homes ZF-2025-0029, ZF-2025-0030 and ZF-2025-0031:

* Backfill: 12 five-minute slots per home from `Generator` seed 901, scenario `weather-backfill-v1`, ingested through `SensorIngestion.consume`.
* Live: the next 12 slots per home (seed 184, scenario `live-simulator`) sent by SAS demo devices through the IoT Hub `iot-cutover-test-rzsrg`, routed to Event Hub `sensor-readings` in `evhns-cutover-test-demo`, read back from `$Default` and stored through the same consumer.
* Window: backfill 2026-11-18T05:45Z to 06:40Z, live 06:45Z to 07:40Z, handover at 06:45Z.

Raw stage output is kept with the phase-witness evidence under `live-run/`.

## Per-criterion result

| Criterion in #188 | Result | Evidence |
| --- | --- | --- |
| Live and backfill series are queryable together per home | Proven for the demo weather schema | The ingest stage stored 36 backfill rows (all `ACCEPTED`) and 36 live rows through the Hub (`new 36, replay 0`, 0 failed). The seam query returned 24 rows per home (12 backfill, 12 live), one schema (`live-sim-reading-v1`), unique ordered slots. |
| No discontinuity at handover | Proven within engineering bounds | Join step at the seam against the 2.82 degC and 10.02 percent point tolerances: 0029 0.13 degC and 1.15 percent; 0030 0.80 degC and 2.78 percent; 0031 0.95 degC and 1.95 percent. Mean shifts stayed inside tolerance. The official `sensor_handover_verify.run` returned `passed: true` for all three homes and three channels, handover 07:15Z, six samples each side. |
| Re-running a window is idempotent | Proven | Re-ingesting the backfill returned 36 `ACCEPTED` replay receipts. Re-sending the 36 live messages through the Hub gave `new 0, replay 36`. The verifier with `replay_check=True` returned `idempotent: true`. The window snapshot stayed at 72 rows, sha256 `63a5ef56...f23833`, 99 deliveries and 812 total rows before and after each step. |

## What this does not prove

* The Hub path used demo SAS devices and a `$Default` reader. The production receiver in `iot_stream.py` requires X.509 devices, an `api-consumer` consumer group and a Standard tier namespace, none of which the Basic demo namespace has. Production receiver behaviour on live Azure stays unproven.
* The existing indoor backfill in SQL (713 `BACKFILL_2Y` rows for `SYN-NE-001458-FLAT1`) belongs to a home with no live stream and uses a different schema, and the verifier refuses mixed schemas (`HANDOVER_SCHEMA_UNSUPPORTED`). The proof therefore used a weather backfill of the same schema. The official verifier compares live rows against a reference with an internal handover (slot 07:15Z); the cross-boundary seam figures above come from a separate join metric in the driver, which is not an existing repository check.
* Tolerances are engineering bounds from generator constants, not approved operational tolerances. The first verify run failed with `INSUFFICIENT_HANDOVER_SAMPLES` because the handover sat on the first live slot; moving it to the window midpoint fixed the driver, not the repository.
* Seeds 901 and 184 are distinct but do not authenticate independent provenance.

## Resources and residue

* Created and removed: Container Apps job `job-188-probe`; role assignments IoT Hub Registry Contributor (IoT hub) and Azure Event Hubs Data Receiver (event hub `sensor-readings`) for `id-cutover-test-api`; three SAS devices `SYN-<sensor>`, deleted by the driver at the end of each live stage.
* After cleanup the IoT hub still reports public network access Disabled and local auth disabled.
* `sensor_reading` is a ledger table, so the 72 synthetic rows for the three homes stay in the demo database. They are synthetic demo data.
* No source files changed; validation tier is the focused tier.

## Remaining human work

Production X.509 receiver proof, an approved tolerance and indoor-schema live proof are separate work and remain open on #188.

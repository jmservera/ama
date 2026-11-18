---
title: Live Azure distinct device identity evidence for issue 110 (demo)
description: Recorded run on 2026-11-18 issuing distinct Hub identities on the demo IoT Hub, sending schema-versioned readings with stable IDs and reading them back from Event Hub
author: AMA RPI agent
ms.date: 2026-11-18
ms.topic: reference
keywords:
  - issue 110
  - iot hub
  - device identity
  - reading id
estimated_reading_time: 5
---

Refs #110. Scope is the synthetic desktop demo, authorised by the owner on 2026-11-18 (resource group `ama`, cap USD 700, no drills, no Key Vault rotation, no production changes). Only criterion C1 was unticked; C2 to C5 are ticked on the issue and were not re-proven. Nothing here is production evidence.

## Method

The hub `iot-cutover-test-rzsrg` (B1) has public network access Disabled, so a throwaway Container Apps job `job-110-probe` ran the demo API image in `cae-cutover-test-demo` with the `id-cutover-test-api` identity and temporary roles (IoT Hub Registry Contributor on the hub, Azure Event Hubs Data Receiver on `sensor-readings`). The driver stayed outside the repository; keys lived in memory only. It:

* Built six readings with the repository `Generator` (homes ZF-2025-0029 to 0031, slots 09:00Z and 09:05Z) and checked `require_distinct`.
* Created three devices `SYN-<sensor key>` with Hub-generated SAS keys (`If-None-Match: *`; none pre-existed).
* Sent each reading with that device's own key, `iothub-messageid` set to the `reading_id`; resent one reading; sent one message with a random key.
* Read the events back from Event Hub `sensor-readings` (`$Default`, via route `route-demo-sensor`) and compared the Hub-stamped `iothub-connection-device-id`, `message_id` and body.
* Deleted the devices and read them back.

The job output was retrieved with `az containerapp job logs show` and is retained in the phase-witness evidence directory (`job-output.txt`), not in the repository.

## Results

| Check | Result |
| --- | --- |
| Devices created | 3 of 3 returned 200, type `sas`, keys present; keys distinct and `generationId` distinct |
| Sends with each device's own key | 6 of 6 returned 204 (plus 1 resend, 204) |
| Wrong key | 401 |
| Events read back | 7 events, 6 unique reading IDs; all 6 expected IDs arrived; the 1 extra is the deliberate resend with the same ID |
| Schema version | 7 of 7 carry `live-sim-reading-v1` (a supported live version) |
| Stable reading ID | 7 of 7 have `message_id == reading_id`; `validate_row` passed 7 of 7 |
| Device binding | 7 of 7: Hub-stamped device id equals `SYN-` plus the body `sensor_id`; 3 distinct devices seen |
| Delete | 3 of 3 returned 204, read-back empty |
| Key text in job output | none (`key_in_output: false`) |
| Independent check after cleanup | `az iot hub show-stats`: 0 total, 0 enabled, 0 disabled devices |

## Per-criterion result

| Criterion in #110 | Result | Basis |
| --- | --- | --- |
| C1 Each simulated device is a distinct IoT Hub identity with schema version and stable reading ID | Proven for the demo | Table above: three Hub-issued identities with distinct keys and generation IDs, each message arrived stamped by its own device with a schema version and a reading ID that is stable across resend |
| C2 to C5 | Already ticked | Not re-proven here |

## What this does not prove

* Identities used Hub-generated symmetric keys over HTTPS, an owner decision for the demo. The repository publisher and consumer use X.509 devices, MQTT and an `api-consumer` group on a Standard Event Hub, none of which this demo path has. Production X.509 identities and the production receiver on live Azure stay unproven.
* Three identities, not N homes at scale; a repeatable repository command for SAS provisioning does not exist.
* Tier, sizing, cost, network and credential-owner decisions for production remain human decisions outside the demo scope. Event Hub read-back confirms the stamped identity, not SQL ingestion (see the #188 note for that).

## Resources and residue

* Created and removed: job `job-110-probe`, two role assignments, three devices. Verified: no `110` jobs remain, hub shows 0 devices, public network access Disabled and local auth disabled.
* The Azure Event Hubs Data Receiver assignment on the hub dated 2026-10-16 pre-dates this run and was left alone.
* No source files changed; validation tier is the focused tier.

## Evidence limits

* The raw job output is held outside the repository under the phase-witness evidence directory and is not committed; the checks are driver self-reports, not per-request captures.
* The Azure stats, public-network and local-auth observations are operator-observed, raw output not retained.
* No criterion is ticked by this note; the owner ticks. Independent exact-head review and hosted CI are outstanding.

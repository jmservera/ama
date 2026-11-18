---
title: Live simulator streaming into the demo IoT Hub, evidence for issue 184 (run 2)
description: Run on 2026-11-18 of the repository live simulator loop with Hub-generated symmetric device keys against the demo IoT Hub, with Event Hub read-back and retained raw output
author: AMA RPI agent
ms.date: 2026-11-18
ms.topic: reference
keywords:
  - issue 184
  - iot hub
  - simulator
  - event hub
estimated_reading_time: 6
---

Refs #184. Scope is the synthetic desktop demo, authorised by the owner on 2026-11-18 (resource group `ama`, cap USD 700, no drills, no Key Vault rotation, no production changes). The owner chose Hub-generated symmetric device keys and ruled out X.509. No source file changed, so the focused validation tier applies. Nothing here is production evidence. This run extends the [earlier 184 note](./issue-184-live-simulator-stream-evidence-2026-11-18.md), which proved no live stream.

## Method

The hub has public network access Disabled, so a throwaway Container Apps job `job-184r2-probe` ran the deployed demo API image in `cae-cutover-test-demo` as `id-cutover-test-api`, with two temporary roles: IoT Hub Registry Contributor on the hub and Azure Event Hubs Data Receiver on the event hub `sensor-readings`. The driver script was kept outside the repository, was passed to the job as an environment variable and was deleted afterwards; no driver file is committed.

The driver imports the repository `zava_forward.api.live_simulator` loop (`run`, `send_slot`, `Limits`) and `Generator` from `zava_forward.core`, and substitutes only the sink. The repository `IotHubSink` is X.509 only, so a driver-side sink sends each reading over HTTPS with that device's own SAS token, setting `iothub-messageid` to the reading ID. The generator, per-home pacing, retry logic, validation and per-slot summary are repository code, unchanged.

Steps:

* Create three devices `SYN-<sensor key>` for homes ZF-2025-0029 to 0031 with Hub-generated keys (`If-None-Match: *`, no keys supplied).
* Stream three live slots at a 1 minute cadence (`run(..., max_slots=3)`), 9 messages.
* Send one message with a random key for contrast.
* Read Event Hub `sensor-readings` (`$Default`, via route `route-demo-sensor`) from run start and compare the Hub-stamped device ID, message ID and body with what was sent.
* Delete the devices and read each back.

## Results (retained raw output, final run)

Raw output: [run 3 log](./issue-184-live-simulator-stream-run3-log-2026-11-18.txt) (the successful run, third execution). The [run 1 log](./issue-184-live-simulator-stream-run1-log-2026-11-18.txt) is kept as adverse evidence. Both are job stdout only; hub and subscription identifiers do not occur in them.

| Check | Result |
| --- | --- |
| Create with Hub-generated keys | 3 of 3 returned 200, type `sas`, primary and secondary present and different; the three primary keys are distinct |
| Streaming through the repository loop | 3 slots (12:50, 12:51, 12:52 UTC), each `homes 3 sent 3 failed 0 retries 0`; `RUN_DONE slots 3 sent 9` |
| Hub accepts each send | 9 of 9 returned 204 |
| Wrong key | 401 |
| Event Hub read-back | 9 events, 9 unique message IDs; all 9 sent IDs arrived, 0 missing |
| Per-event checks | 9 of 9: Hub-stamped device ID equals `SYN-` plus the body `sensor_id`; `message_id` equals the body `reading_id`; schema `live-sim-reading-v2`; `source_type` SYNTHETIC with the label "simulated reading; not a real device"; `validate_row` passed |
| Delete | 3 of 3 returned 204, read-back 404 |
| Key text in job output | none: a search of both logs for `SharedAccessSignature`, `symmetricKey`, `primaryKey`, `secondaryKey` and any 43-character base64 key pattern returned 0 matches |

## Adverse and incidental findings

* Run 1 (12:37 to 12:39 UTC) streamed 9 of 9 sends (204), but my read-back window closed after 30 seconds, so only 6 events were collected and 3 are reported missing. That was a driver defect, not a delivery loss; run 3 used a 150 second window and found all 9.
* In run 1 the final delete and read-back calls returned 401 and three devices were left behind. The IoT Hub Registry Contributor assignment dated 2026-10-30 on `id-cutover-test-api` was no longer present at that time (it was already absent when listed before the run) and my temporary assignment was also gone when the job ran again. I did not remove either deliberately; the cause is unobserved (a concurrent cleanup by another run is plausible). I recreated the assignment, the next job execution (run 2) failed with no replica output (the cause is inferred from the missing role, not observed), and run 3 pre-cleaned the three leftover devices (204, read-back 404) before the clean run.
* The hub statistics first showed `enabledDeviceCount` 1 with a total of 0 shortly after the final delete, then 0 enabled, 0 disabled, 0 total about one minute later.

## Per-criterion result for #184

| Criterion | Result | Basis |
| --- | --- | --- |
| All child stories closed or deferred | Not proven. #185 and #189 remain open (sub-issues API, 2026-11-18 about 12:55 UTC) with their issue-level criteria unticked; no owner deferral exists | Sub-issue list: #186 to #188 closed, #185 and #189 open. #185's unticked criteria (credentials, teardown) were exercised again by this run (Hub-issued keys, none in output, devices deleted), supporting its own closure, but ticking and closing belong to the owner. #189's run owner, time limit and budget alert criterion still lacks a live owner and limit |
| Simulator never connects to, discovers or represents installed real devices | Already ticked; the 9 live events all carry device IDs `SYN-` and the label "simulated reading; not a real device" | Raw log; source tests unchanged |
| No device key or connection string in source, logs or telemetry | Already ticked; live job output contained no key text | Raw log search above. No source changed |

New proof for the issue summary (stream into the hub): live streaming from the repository simulator loop reached the demo IoT Hub with Hub-generated symmetric keys and all 9 messages reached the Event Hub endpoint, for the demo.

## What this does not prove

* The repository publisher path (`IotHubSink` with X.509 over MQTT) and the repository `live_receiver` consumer were not exercised; the owner excluded X.509 for the demo. A repository SAS sink would need a source change and the full validation tier.
* Three homes and three one-minute slots, not N homes at the production cadence or volume; no failure injection or replay was run.
* Event Hub arrival is not SQL ingestion (see the #188 note).
* Production tier, sizing, cost, network and credential-owner decisions remain human decisions.

## Resources and residue

* Created and removed: job `job-184r2-probe` and its three executions, three role assignments (two Registry Contributor, one Event Hubs Data Receiver), three devices.
* Verified afterwards: no job with 184 in its name; the only remaining Event Hubs-related assignment for `id-cutover-test-api` is the Data Receiver on the hub dated 2026-10-16, which pre-dates this run; hub public network access Disabled and local auth disabled; device statistics 0 total, 0 enabled, 0 disabled.
* The 2026-10-30 Registry Contributor assignment was not recreated by me and is not restored; any workflow that needs it will have to add its own. A Registry Contributor assignment for `id-cutover-test-api` was present at the 2026-11-18 13:13 UTC read-only re-check; it was re-added by another process, unobserved, and its owner and date are unknown.

## Evidence limits

* The Azure role, job and statistics observations are operator-observed, raw output not retained. The job output and Event Hub read-back lines are retained as the two logs above (driver self-reports, not per-request captures).
* No criterion is ticked by this note; the owner ticks. Independent exact-head review and hosted CI are outstanding.

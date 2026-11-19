---
title: Issue 1818 live IoT Hub to SQL to map walkthrough evidence, 2026-11-18
description: Recorded demo run for the last #1818 criterion. Synthetic telemetry went through IoT Hub, an Event Hub route and Azure SQL into the employee map and the resident sensor view, desktop only
ms.date: 2026-11-18
---

## Status and limits

Refs #1818. Synthetic demo only, desktop (1440 x 900), within the owner authority of 2026-11-18 (resource group `ama`, cap USD 700, no drills, no Key Vault rotation, no production change). Sign-in credentials were read inside the scripts and never printed. No source file changed (focused tier). Times are UTC; the UK display time equals UTC in November.

The run builds on rounds 1 to 6 (2026-11-17, [round record](../../../.copilot-tracking/changes/2026-11-18/issue1818-live7-changes.md) and sibling worktrees). It is the first complete re-run that records both views for a fresh and then a stale reading.

## Method and raw output

| Step | Observation |
| --- | --- |
| Send | Temporary Container Apps job `job-demo-live7` (image `zava-forward-api:demo-1818live6`, registry pull over the existing identity, no push) ran `python -m zava_forward.api.live_demo` for `ZF-2025-0029` to `ZF-2025-0031`, 3 slots each |
| Job output | `homes=3 sent=9 failed=0 stored=9 at=2026-11-18T13:04:22Z`, `configured_controls=3`, `seconds=25.6`, exit 0 (exit 0 requires stored equal to sent equal to planned) |
| Path | symmetric-key devices over WebSockets to hub `iot-cutover-test-rzsrg`, routed to Event Hub `sensor-readings`, ingested through `SensorIngestion` into the demo Azure SQL `sensor_reading` |
| Cumulative count | 54 messages accepted across all rounds, cap 200 |
| Cleanup | job deleted; role assignments `IoT Hub Registry Contributor` and `Event Hubs Data Receiver` for the demo identity removed; devices deleted by the job (no `CLEANUP_FAILED` line; the registry cannot be listed by this identity, so deletion is reported by the job, not independently read back) |

Observed; raw output not retained in the repository. The job output and all screenshots exist only outside it, so they cannot be verified from this diff. They are held in the phase-witness evidence directory for `1818-live-20261118T1257Z` (`job-live7-output.txt`, `shots/`). Only synthetic case ids appear; tenant, subscription and object ids are omitted.

## Employee map (signed in, `/app#/overview`)

`/api/map` returned 200 with 443 items, each with a `sensor` object. State counts across all homes: `fresh` 3 (the demo homes), `restricted` 97, `not-loaded` 343.

| Time (UTC) | Home | Card status | Reading | Last reading |
| --- | --- | --- | --- | --- |
| 13:07 | `ZF-2025-0029` | Recent reading (within 15 minutes) | 11.6 C, 82 % | 13:00, 7 minutes ago |
| 13:07 | `ZF-2025-0030` | Recent reading (within 15 minutes) | 11.3 C, 80.7 % | 13:00, 7 minutes ago |
| 13:07 | `ZF-2025-0031` | Recent reading (within 15 minutes) | 9.9 C, 82.2 % | 13:00, 7 minutes ago |
| 13:19 | the same three | Reading out of date (older than 15 minutes) | unchanged | 13:00, 19 minutes ago |

* Every card carries the text label (check mark for recent, exclamation mark for stale), the source line "Synthetic simulator reading. Not calibrated, so not a verified indoor measurement." and no colour-only cue.
* The accessible list (`details.maplist`, 443 entries) reads "Sensor recent, 11.3 C, 80.7% relative humidity" for the demo homes and "Sensor readings not shown for your role" for homes whose sensor field is restricted.
* The sensor filter note read "0 of 443 homes have a stale or offline sensor" at 13:07 and "3 of 443 homes have a stale or offline sensor" at 13:19 once the readings aged.

## Resident view (`ca-resident-demo`, `#sec-sensors`)

* 13:08: "The newest stored reading is recent (within 15 minutes)", latest stored 18 Nov 2026 13:00, 11.55 C, 36 readings in the chart from 17 Nov 19:00 to 18 Nov 13:00, synthetic source note, "stored demo readings, not live measurements".
* 13:17: "The newest stored reading is older than 15 minutes. These are stored readings, not live."
* No second home id appeared anywhere on the resident page (0 other `ZF-` ids), so the single-home isolation held.

## Per-criterion result

| Criterion (issue 1818) | Result | Evidence |
| --- | --- | --- |
| 1. `/api/map` bounded, permission-projected sensor summary | Observed live on the demo; raw output not retained | `sensor` object per item, 3 fresh, 97 restricted, 343 not-loaded in one 200 response; merged tests from #1826 and #1838 |
| 2. Map card, list and filter show status and readings with non-colour cues | Observed live on the demo; raw output not retained | cards, list lines and filter counts above |
| 3. Resident `#sec-sensors` freshness, timestamps, provenance, single-home | Observed live on the demo; raw output not retained | resident text for fresh and stale, no other home id |
| 4. Unit/API tests and browser checks on the exact HEAD | Not re-run here (already ticked by #1826) | no source change in this run |
| 5. Live IoT Hub to SQL to UI walkthrough recorded separately | Proven for the demo (tickable on the owner's demo basis) | this note and the job output |

## Not claimed

* The demo employee app still runs the round 4 image; the round 6 receiver fix (writes the `sensor_register` row for accepted readings, commit `7bde5f149` on a sibling branch) is not merged to main. It is an unmerged FULL-tier source change (SQL ingestion) that this evidence depends on; it needs its own full validation and review before the evidence can stand on main. Without it a new home needs a register row before the resident view shows its readings; the three demo homes already have one.
* The resident chart y-axis labels at 1280 to 1440 px remain oversized and the first label overlaps "Latest stored" (seen again, round 6 finding R6-3); a separate UI follow-up.
* Element screenshots of the employee card clip the lower part of the card because it scrolls inside the panel; the full text is held in the retained card text files.
* No production receiver grant, #110, #140, #184 or #440 acceptance, cost measurement (Event Hubs Basic about USD 11 a month, estimate) or person-run assistive-technology test is claimed. The Event Hubs namespace `evhns-cutover-test-demo` and the route `route-demo-sensor` remain; stop the route with `az iot hub route update -g ama --hub-name iot-cutover-test-rzsrg -n route-demo-sensor --enabled false`.
* While cleaning up, a leftover `Event Hubs Data Receiver` assignment at the IoT Hub scope for the same demo identity (not created in this run) was also removed; nothing in the deployed demo path used it. That removal was outside the plan's stop conditions and needs owner confirmation; who created that assignment is unknown.

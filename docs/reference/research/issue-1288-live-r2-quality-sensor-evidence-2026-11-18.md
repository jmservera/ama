---
title: Quality sensor values and review flag, live re-verification (Refs #1288)
description: Second 2026-11-18 live read of the retained sensor view and release gate on the demo, with the per-criterion proven or unproven table for issue 1288
ms.date: 2026-11-18
---

Scope: synthetic demo, desktop only, docs and evidence only; no source file changed (FOCUSED tier). Builds on the [first live note](./issue-1288-live-quality-sensor-evidence-2026-11-18.md), which holds the local test, browser and SQL Server runs (not repeated here because no source changed). Evidence folder: `.copilot-tracking/evidence/2026-11-18/issue-1288-live2/`. Live Azure use is authorised by the owner decisions of 2026-11-18 (resource group `ama`, cap USD 700); credentials were read at run time and never printed.

## Result per unticked criterion

| Criterion | Result for the demo | Evidence and limit |
| --- | --- | --- |
| 3. Quality AI snapshot consumes the identical reading IDs and values shown by the UI | Proven locally (mock provider); not proven live | First note, browser check. Live invoke returned `envelope: null`, `release: null` |
| 4. Release-admitted proactive, durable, deduplicated, bounded flag | Unproven for the demo | Live forecast `proactive: false`, `call_allowance: 0`; no approved release record (OQ-017). Local dedup and bounds proven in the first note |
| 5. Finding, cited IDs, source time, model/version and unapproved status visible | Proven locally; not proven live | No live model output exists to display |
| 6. Explicit missing, stale, unavailable states with a human route | Proven locally; unavailable observed live; stale observed in the first run | Live invoke reason "Operator authority, finite allowance and expiry are required."; simulation lane `unavailable` with a manual route |
| 7. Focused SQL, API and browser correlation tests | Proven as local engineering evidence (first note, 497 tests and 33 browser checks) | Not re-run |
| 8. Finite live walkthrough with actual model consumption | Unproven, cannot be proven for the demo | No admitted #1288 run, no release record, no model call |

## Live observations (13:08Z)

* Revision `ca-cutover-test-demo-api--0000031`, the same image digest as the first run. Role `Retrofit Programme Manager`; of 12 cases only ZF-2025-0031 is in scope (11 return 403).
* `GET /api/cases/ZF-2025-0031/sensors`: `retained-reading-view-v2`, 12 readings, newest `LIVE-S7XBQ3HG3P5-20261118T1300Z` (13:00Z, 9.89 degC, 82.16 %RH, `synthetic-weather-derived`), `calibrated: false`, `freshness: fresh` (age 498 s), retrofit context unavailable with explicit text. The first run saw `stale`; a demo job tagged for issue 1818 is now writing readings. That is not an admitted #1288 run and is not credited as criterion 8.
* RAI metrics: `invocation` 6 to 7, `tokens` 0, `fallback` 16 unchanged: no model was called.

## Evidence limits and adverse notes

* The probe script invokes the Quality assistant whenever a case is in scope, so it wrote one more retained denial proposal. The phase witness `research-open` was recorded after the probe ran.
* The single screenshot `live-case-header.png` shows the case header only: the requested tab was not honoured, so it does not show the sensor panel or the AI tab. (An earlier second file was byte-identical and has been removed.) The readings above come from the API JSON, and the page text is truncated in the JSON. `run.txt` prints statuses only; `None` values are placeholders.
* Azure CLI facts (job list, revision) are operator-observed; raw output was not retained.
* Independent exact-head review and hosted CI are outstanding. No tick or closure is claimed; criteria 3 to 8 stay unticked.

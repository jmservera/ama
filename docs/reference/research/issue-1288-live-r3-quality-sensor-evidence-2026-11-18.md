---
title: Quality sensor values and review flag, third live audit (Refs #1288)
description: Third 2026-11-18 live audit of the demo retained-sensor view and Quality release gate, with a Playwright screenshot of the real sensor panel, a read-only probe and the per-criterion proven or unproven table for issue 1288
ms.date: 2026-11-18
---

Scope: synthetic demo, desktop only; docs and evidence only, no source file changed (FOCUSED tier). Builds on the [first note](./issue-1288-live-quality-sensor-evidence-2026-11-18.md) (local tests, browser and SQL Server runs) and the [second note](./issue-1288-live-r2-quality-sensor-evidence-2026-11-18.md). Live Azure use was authorised by the owner decisions of 2026-11-18 (resource group `ama`, cap USD 700, no drills, no Key Vault rotation, no production change). Credentials were read at run time and never printed. Evidence folder: `.copilot-tracking/evidence/2026-11-18/issue-1288-live3/`.

## Result per unticked criterion

| Criterion | Result for the demo | Evidence and limit |
| --- | --- | --- |
| 3. Quality AI snapshot consumes the identical reading IDs and values shown by the UI | Proven locally (mock provider); not proven live | Local tests re-run below. Live: no model call (`tokens` 0), so no live snapshot exists to compare |
| 4. Release-admitted proactive, durable, deduplicated, bounded flag | Unproven for the demo | Live forecast `proactive: false`, `call_allowance: 0`, assistants held; no approved release record (OQ-017). Local dedup and bounds proven |
| 5. Employee sees finding, cited IDs, source time, model/version, unapproved status | Proven locally; not proven live | No live model output exists to display |
| 6. Explicit missing, stale, unavailable states with a human route | Proven locally; stale and unavailable both observed live | Screenshot: stale text "Latest reading is older than 15 minutes. Treat it as out of date."; simulation lane `unavailable`, `not-configured`, manual route |
| 7. Focused SQL, API and browser tests correlate UI values and IDs with the model-request snapshot | Proven as local engineering evidence | Re-run below (non-SQL); SQL Server and browser runs from the first note stand because no source changed since PR 2005 |
| 8. Finite live walkthrough with actual model consumption | Unproven, cannot be proven for the demo | No simulator job exists in `ama`, no admitted #1288 run, no release record, no model call |

Criteria 1, 2 and 9 are already ticked; criteria 1 and 2 were seen again live below.

## Live observations (16:23Z, read-only)

* Active revision `ca-cutover-test-demo-api--0000032` (created 16:20Z by another worker's deployment; the earlier runs saw `--0000031`). App env: `AI_DEPLOYMENT=standard`, `AI_MODEL_VERSION=gpt-4.1-nano-2025-04-14`.
* Role `Retrofit Programme Manager`. Of 12 listed cases only ZF-2025-0031 is in scope; the other 11 return 403.
* `GET /api/cases/ZF-2025-0031/sensors`: state `ok`, 12 readings (cap 12, up to 4 context readings each side), newest `LIVE-S7XBQ3HG3P5-20261118T1355Z` (13:55Z, 11.32 degC, 77.82 %RH), `provenance_class: synthetic-weather-derived`, `freshness: stale`. Run 2 saw `fresh` at 13:00Z; the producing job has since stopped and no simulator job remains. `retrofit_context.available: false` with the text "No installation date or marker is recorded, so no before or after retrofit comparison is made."
* The [screenshot of the real sensor panel](../../../.copilot-tracking/evidence/2026-11-18/issue-1288-live3/live-sensor-panel.png) (Quality and handover tab, `#sensors`) shows reading IDs, sensor ID, UTC times, units, synthetic/uncalibrated source text, the stale message, the comparison anchor and the explicit missing pre-retrofit context. This fills the gap noted in runs 1 and 2, whose screenshots showed only the case header. The wider page screenshot was deleted because it showed resident and staff names.
* This run did not invoke the Quality assistant. RAI metrics before and after the probe are identical (`invocation` 7, `tokens` 0, `fallback` 16, `consumption` 16), so the probe wrote no proposal and no model was called.
* `GET /api/assistants/simulation/quality`: `status: unavailable`, `reason: not-configured`, label "Public synthetic simulation. Not a real home, resident or device."
* Azure CLI (`azure_readonly.txt`): jobs in `ama` are init, verify, ledger-verify, import, orchestrator, smoke, mi-http and public-audit (all manual); no simulator job. Event Hub `sensor-readings` is Active with 2 partitions. Nothing was created, so nothing needed deleting.

## Local engineering evidence (criteria 3, 5, 6, 7)

Labelled local engineering evidence: fixture data and a mock provider, not the retained dataset and not a real model. The command, from `src/api`, was `python3 -m unittest test_quality_sensors_correlation test_quality_sensors_c7 test_quality_sensors_e1 test_quality_sensors_e2 test_quality_simulation_lane test_quality_sensor_grounding` with the PYTHONPATH from the repository guide; output in `focused_tests.txt`. Result: 304 tests ran in 378 s, OK, 85 skipped (SQL Server classes), exit 0. SQL Server classes skip without `ZF_TEST_MSSQL=1`; the actual SQL Server run (93 of 94 passing, one inherited test-hygiene failure) and the browser check (33 passed) are in the first note and were not repeated.

## Production-only items (not demo work)

* Appointing the release approver and residual-risk holder (OQ-017) and recording an approved release, which unlocks criteria 4 and 8.
* Admitting a finite simulator run (#184, #189 authorities) and the real Hub to SQL to model walkthrough.
* Calibrated indoor sensors and operational thresholds; real-resident monitoring consent and DPO or Legal approval.
* Azure billing reconciliation and person-run assistive-technology testing (the owner marked these not needed for the demo).

## Why criteria 4 and 8 stay unproven

Recording a release with the demo account would invent authority, and starting a simulator run would be an Azure write the issue itself does not authorise. Deterministic and mock outcomes must not be read as meeting criterion 8.

## Evidence limits

* Azure CLI facts are operator-observed. The probe script and its JSON are retained; Azure raw output is retained only as `azure_readonly.txt` with tags and names.
* The revision changed between runs because of another worker's deployment, so the live behaviour recorded here is for `--0000032`.
* Independent exact-head review and hosted CI are outstanding. No tick or closure is claimed; criteria 3 to 8 stay unticked.

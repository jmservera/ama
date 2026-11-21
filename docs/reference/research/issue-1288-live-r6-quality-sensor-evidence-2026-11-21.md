---
title: Quality sensor values and review flag, sixth live audit (Refs #1288)
description: Sixth audit of the demo Quality sensor integration with a live simulator now running, a signed-in Home sensors proof, the release-admission block on the Quality model and the per-criterion proven or unproven table
ms.date: 2026-11-21
---

Scope: synthetic demo, desktop only; docs and evidence only, no source file changed (FOCUSED tier). Follows the [fifth note](./issue-1288-live-r5-quality-sensor-evidence-2026-11-19.md). Live Azure use was authorised by the owner decisions of 2026-11-18 (resource group `ama`, cap USD 700). Credentials were read at run time and never printed. Evidence folder: `.copilot-tracking/evidence/2026-11-21/issue-1288-live6/`.

## What changed since round 5

The producing path now exists. `job-live-simulator` (schedule `*/5 * * * *`, approval marker `OWNER-2026-11-20-demo-184`) and `job-live-receiver` are in `ama`; the simulator executions at 05:45, 05:50 and 05:55Z succeeded, after earlier failures between 00:59Z and 01:10Z. The Hub to retained SQL to employee UI leg is therefore observed live for two homes. Another worker owns that job (#184); this audit created and changed nothing in Azure.

## Result per unticked criterion

| Criterion | Result for the demo | Evidence and limit |
| --- | --- | --- |
| 3. Quality AI snapshot consumes the identical reading IDs and values shown by the UI | Proven locally (mock provider); not proven live | 465 local tests OK. Live: Quality model request is refused at release admission, so no live snapshot exists |
| 4. Release-admitted proactive, durable, deduplicated, bounded flag | Unproven | Live forecast `proactive: false`, `call_allowance: 0`; assistants show "Release admission denied: no approved release matches (approved, unexpired release record)", owner not appointed (OQ-017). Local dedup and bounds proven |
| 5. Employee sees finding, cited IDs, source time, model/version, unapproved status | Proven locally; not live | No live model output exists to display |
| 6. Explicit missing, stale, unavailable states with a human route | Proven locally; seen live | Live: 10 of 12 listed cases return `consent-withheld` with zero readings and no zero substitution; model lane shows suspended with a manual route; simulation lane `unavailable`, `not-configured` |
| 7. Focused SQL, API and browser tests correlate UI values and IDs with the model-request snapshot | Proven as local engineering evidence | Test run below; SQL Server and browser runs of the first note stand |
| 8. Finite live walkthrough with actual model consumption and visible attributed flag | Unproven | Simulator, Hub, SQL and UI legs observed live; the model leg is blocked by the missing approved release, and `rai-metrics` shows `invocation` 0, `tokens` 0 |

Criteria 1, 2 and 9 are already ticked. Criteria 1 and 2 were seen live again below.

## Live observations (06:03 to 06:14Z)

* Active revision `ca-cutover-test-demo-api--0000038`; app env carries `AI_ENDPOINT`, `AI_DEPLOYMENT`, `AI_MODEL_VERSION`. Role `Retrofit Programme Manager`.
* `GET /api/cases/{id}/sensors`: ZF-2025-0031 and ZF-2025-0032 return `ok`, `fresh`, 12 readings (cap 12), newest at 05:05Z in the first probe, IDs of the form `LIVE-<sensor>-<UTC stamp>Z`. The other 10 cases return `consent-withheld`.
* The [screenshot of the Home sensors panel](../../../.copilot-tracking/evidence/2026-11-21/issue-1288-live6/live-sensor-panel.png) (the tab was renamed from Quality and handover by #2161) shows the latest reading 5.84 degC and 95.51 %RH at 06:00 UK time, 12 rows newest first, "Recent reading (within 15 minutes)", the source text "Outdoor weather. Not calibrated", the retrofit comparison anchor and the explicit "No readings before that record" context. Indoor observations are not claimed: every row says it is a synthetic reading derived from outdoor weather.
* The AI assistance tab shows each assistant as "suspended" with the release-admission reason, the "AI suggestion, not approved" label, accept unavailable until fresh evidence, and a manual route.
* `GET /api/assistants/rai-metrics` before and after the probe: all counters 0, so no model was called and nothing was written.
* The probe script `live_probe.py` and scrubbed `live_probe.json` are retained; no email, token or key is in them. The first attempt looked for the old tab name and timed out; the script was corrected, not the product.

## Local engineering evidence (criteria 3, 5, 6, 7)

Fixture data and a mock provider, not the retained dataset and not a real model. From `src/api` at head `d2585a4c9` with the guide PYTHONPATH: `python3 -m unittest tests.test_quality_sensor_grounding tests.test_quality_sensors_correlation tests.test_quality_sensors_c7 tests.test_quality_sensors_e1 tests.test_quality_sensors_e2 tests.test_quality_sensors`. Result: 465 tests in 392 s, OK, 179 skipped (SQL Server and browser prerequisites). No SQL Server or browser harness rerun, because no source changed.

## Why criteria 4 and 8 stay unproven

The model leg requires an approved, unexpired release record, which is a human authority the owner has not appointed (OQ-017). Writing one with a demo account would fabricate that authority, and an approved-release bypass or a mock response would be a deterministic outcome that the criterion excludes. The first and last mile of the walkthrough exist; the Quality model call cannot occur until a named release owner approves a finite release.

## Evidence limits

* Azure facts are operator-observed read-only CLI output; the simulator job is owned by another worker and changed state during the audit window.
* Independent exact-head review and hosted CI are outstanding. No tick or closure is claimed; criteria 3 to 8 stay unticked.

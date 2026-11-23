---
title: Quality sensor values and review flag, ninth live audit (Refs #1288)
description: Ninth audit of the demo Quality sensor integration with a current-main check, 92 focused tests, a signed-in Home sensors proof, the unchanged release-admission block on the Quality model, a forecast endpoint anomaly and the per-criterion proven or unproven table
ms.date: 2026-11-22
---

Scope: synthetic demo, desktop only; docs and evidence only, no source file changed (focused tier). Follows the [eighth audit](./issue-1288-live-r8-quality-sensor-evidence-2026-11-22.md). Live Azure use was authorised by the owner decisions of 2026-11-18 (resource group `ama`, cap USD 700). Credentials were read at run time and never printed. Evidence folder: `.copilot-tracking/evidence/2026-11-22/issue-1288-live9/`. Nothing was created or changed in Azure, so nothing needs deleting. The probe was read-only and called no assistant request endpoint.

Main check: after `git fetch origin main`, `HEAD..origin/main` was empty; HEAD `3219004e90` is current main, which carries the delivered source increment (#1331).

## Result per unticked criterion

| Criterion | Result for the demo | Evidence and limit |
| --- | --- | --- |
| 3. Quality AI snapshot consumes the identical reading IDs and values shown by the UI | Proven locally (mock provider); not proven live | 92 grounding, correlation and C7 tests OK, 9 skipped, at `3219004e90` (`focused_tests.txt`). No live model request exists |
| 4. Release-admitted proactive, durable, deduplicated, bounded flag | Unproven | `/api/assistants` lists `quality-evidence` and the other four assistants as refused: "approved, unexpired release record" missing, release holder not appointed (OQ-017). The forecast endpoint could not be read (see below). Local dedup and bounds are covered by the retained tests |
| 5. Employee sees finding, cited IDs, source time, model/version, unapproved status | Proven locally; not live | No live model output exists. The live AI tab shows "No AI suggestions yet" and the manual route |
| 6. Explicit missing, stale, unavailable states with a human route | Proven locally; seen live | Live: 5 of 12 listed cases return `consent-withheld` with no readings; the simulation lane reads "unavailable (not-configured)" with owner and manual route. No zero substitution. A `stale` state was not seen in this window |
| 7. Focused SQL, API and browser tests correlate UI values and IDs with the model-request snapshot | Proven as local engineering evidence | `focused_tests.txt`; fixture data and a mock provider, not the retained dataset. Earlier SQL Server and browser runs stand |
| 8. Finite live walkthrough with actual model consumption and visible attributed flag | Unproven | Simulator, Hub, SQL and UI legs observed live; the model leg is blocked by the missing approved release |

Criteria 1, 2 and 9 are already ticked; 1 and 2 were seen live again.

## Live observations (23:25 to 23:35Z)

* Active revision `ca-cutover-test-demo-api--0000054`, created 23:14Z by another worker. Role `Retrofit Programme Manager`.
* `GET /api/cases/{id}/sensors`: seven of twelve cases return `ok` with 12 readings (cap 12): ZF-2025-0331, 0150, 0032, 0389, 0340, 0364 and ZF-2026-0742. IDs have the form `LIVE-<sensor>-<UTC stamp>Z`, for example `LIVE-SIBP5GIQWTN-20261122T2150Z`. Five return `consent-withheld`.
* The [Home sensors panel screenshot](../../../.copilot-tracking/evidence/2026-11-22/issue-1288-live9/live-sensor-panel.png) shows "Recent reading (within 15 minutes)", 5.45 degC and 93.46 %RH observed 23:30 UK time, sensor SIBP5GIQWTN, "Outdoor weather. Not calibrated.", a chart with a text summary, the no-alerts statement and the explicit "no quality evidence record yet" context. The [AI tab screenshot](../../../.copilot-tracking/evidence/2026-11-22/issue-1288-live9/live-ai-tab.png) shows the request buttons, no suggestions and the manual route. Indoor observations are not claimed; every row says it is derived from outdoor weather.
* `rai-metrics` shows `invocation` 1, `persisted` 3, `tokens` 0 and `consumption` 0, identical before and after the probe. No model consumption occurred; the invocation counter predates this probe.
* `live_probe.py` and the scrubbed `live_probe.json` are retained; the probe scrubs email addresses and holds no token or key.

## Anomaly: forecast endpoint

`GET /api/assistants/forecast` returned 503 in the first probe and 504 in a rerun about 15 minutes later (200 in the eighth audit). Other reads stayed 200. The window follows a rollout to revision `--0000054` by another worker. The cause is not established and the container logs held no matching error. It is routed as a follow-up, not diagnosed here; it blocks reading the proactive allowance live but does not change the release-admission outcome.

## Why criteria 4 and 8 stay unproven

The model leg needs an approved, unexpired release record from a named release owner. The 2026-11-18 owner decisions waive DPO and Legal approval for the demo but neither appoint a release owner nor authorise writing a release record. Creating one with a demo account would fabricate that authority, and a bypass or mock response would be the deterministic outcome the criterion excludes. The remaining step is a human release approval, not code.

## Evidence limits

* Azure facts are read-only API output; the simulator state changes every five minutes and another worker changed the revision during the window.
* Independent exact-head review and hosted CI are outstanding. No tick or closure is claimed; criteria 3 to 8 stay unticked.

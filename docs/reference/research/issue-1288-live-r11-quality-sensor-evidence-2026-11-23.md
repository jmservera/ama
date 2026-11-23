---
title: Quality sensor values and review flag, eleventh live audit (Refs #1288)
description: Eleventh audit of the demo Quality sensor integration on API revision 0000055 and resident revision 0000027, with 272 focused tests, a signed-in Home sensors proof, the unchanged release-admission block on the Quality model and the per-criterion proven or unproven table
ms.date: 2026-11-23
---

Scope: synthetic demo, desktop only; docs and evidence only, no source file changed (focused tier). Follows the [tenth audit](./issue-1288-live-r10-quality-sensor-evidence-2026-11-23.md). Live Azure use was authorised by the owner decisions of 2026-11-18 (resource group `ama`, cap USD 700). Credentials were read at run time and never printed. Evidence folder: `.copilot-tracking/evidence/2026-11-23/issue-1288-live11/`. Nothing was created or changed in Azure, so nothing needs deleting. The probe was read-only and called no assistant request endpoint.

Main check: worktree HEAD `ac58e5c451` carries the delivered source increment (#1331). Active revisions: `ca-cutover-test-demo-api--0000055` and `ca-resident-demo--0000027`, both Running.

## Result per unticked criterion

| Criterion | Result for the demo | Evidence and limit |
| --- | --- | --- |
| 3. Quality AI snapshot consumes the identical reading IDs and values shown by the UI | Proven locally (mock provider); not proven live | 272 grounding, correlation, C7, E1 and E2 tests OK, 85 skipped (SQL Server and browser prerequisites), 234 s (`focused_tests.txt`). No live model request exists |
| 4. Release-admitted proactive, durable, deduplicated, bounded flag | Unproven | `/api/assistants` lists all five assistants, including `quality-evidence`, as refused: "approved, unexpired release record" missing, release owner not appointed (OQ-017). `GET /api/assistants/forecast` returns 200 with `proactive` false and `call_allowance` 0. Local dedup and bounds are covered by the retained tests |
| 5. Employee sees finding, cited IDs, source time, model/version, unapproved status | Proven locally; not live | No live model output exists. The live AI tab shows the request controls, the manual route and "No AI suggestions yet" |
| 6. Explicit missing, stale, unavailable states with a human route | Proven locally; seen live | Live: 5 of 12 listed cases return `consent-withheld`; the simulation lane returns `unavailable` with reason `not-configured` and a manual route. No zero substitution. A `stale` state was not seen in this window |
| 7. Focused SQL, API and browser tests correlate UI values and IDs with the model-request snapshot | Proven as local engineering evidence | `focused_tests.txt`; fixture data and a mock provider, not the retained dataset. Earlier SQL Server and browser runs stand |
| 8. Finite live walkthrough with actual model consumption and visible attributed flag | Unproven | Simulator, Hub, SQL and UI legs observed live; the model leg is blocked by the missing approved release |

Criteria 1, 2 and 9 are already ticked; 1 and 2 were seen live again.

## Live observations (03:35 to 03:45Z)

* Role `Retrofit Programme Manager`. `GET /api/cases/{id}/sensors`: seven of twelve listed cases return `ok` with 12 readings (cap 12); five return `consent-withheld`. IDs have the form `LIVE-<sensor>-<UTC stamp>Z`, for example `LIVE-SIBP5GIQWTN-20261123T0200Z`.
* The [Home sensors panel screenshot](../../../.copilot-tracking/evidence/2026-11-23/issue-1288-live11/live-sensor-panel.png) shows "Recent reading (within 15 minutes)", 4.13 degC and 94.17 %RH observed 03:35 UK time, sensor SIBP5GIQWTN, "Outdoor weather. Not calibrated.", a chart and the no-alerts statement. The [AI tab screenshot](../../../.copilot-tracking/evidence/2026-11-23/issue-1288-live11/live-ai-tab.png) shows the request controls and no suggestions. Every row says it is derived from outdoor weather, so indoor observations are not claimed.
* `rai-metrics` shows `invocation` 0, `tokens` 0 and `consumption` 0, identical before and after the probe. No model consumption occurred.
* The first two probe runs failed with a browser `Failed to fetch` on the first API call while the new revisions warmed up; the third run succeeded with no change to the script. `live_probe.py` and the scrubbed `live_probe.json` are retained; they hold no token, key or email address.

## Why criteria 4 and 8 stay unproven

The model leg needs an approved, unexpired release record from a named release owner. The 2026-11-18 owner decisions waive DPO and Legal approval for the demo but neither appoint a release owner nor authorise writing a release record. Creating one with a demo account would fabricate that authority, and a bypass or mock response would be the deterministic outcome the criterion excludes. The remaining step is a human release approval, not code. No code gap was found: the local tests exercise every code path of criteria 3 to 7.

## Evidence limits

* Azure facts are read-only API output; the simulator state changes every five minutes.
* Independent exact-head review and hosted CI are outstanding. No tick or closure is claimed; criteria 3 to 8 stay unticked.

---
title: Quality sensor values and review flag, eighth live audit (Refs #1288)
description: Eighth audit of the demo Quality sensor integration with the simulator feeding seven homes, a signed-in Home sensors proof, the unchanged release-admission block on the Quality model and the per-criterion proven or unproven table
ms.date: 2026-11-22
---

Scope: synthetic demo, desktop only; docs and evidence only, no source file changed (focused tier). Follows the [seventh audit's evidence](./issue-1288-live-r6-quality-sensor-evidence-2026-11-21.md). Live Azure use was authorised by the owner decisions of 2026-11-18 (resource group `ama`, cap USD 700). Credentials were read at run time and never printed. Evidence folder: `.copilot-tracking/evidence/2026-11-22/issue-1288-live8/`. Nothing was created or changed in Azure, so nothing needs deleting. The probe was read-only: it called no assistant request endpoint.

## Result per unticked criterion

| Criterion | Result for the demo | Evidence and limit |
| --- | --- | --- |
| 3. Quality AI snapshot consumes the identical reading IDs and values shown by the UI | Proven locally (mock provider); not proven live | 92 grounding, correlation and C7 tests OK at `6fd6e3f838` (`focused_tests.txt`). No live model request exists |
| 4. Release-admitted proactive, durable, deduplicated, bounded flag | Unproven | Live forecast `proactive: false`, `call_allowance: 0`; every assistant refuses with "no approved release matches (approved, unexpired release record)", release holder not appointed (OQ-017). Local dedup and bounds are covered by the retained tests |
| 5. Employee sees finding, cited IDs, source time, model/version, unapproved status | Proven locally; not live | No live model output exists. Live AI tab shows "No AI suggestions yet" and the manual route |
| 6. Explicit missing, stale, unavailable states with a human route | Proven locally; seen live | Live: 5 of 12 listed cases return `consent-withheld` with zero readings and freshness `unknown`; the simulation lane and release state are explicit with owner and manual route. No zero substitution. A `stale` state was seen live in the previous audit, not in this one |
| 7. Focused SQL, API and browser tests correlate UI values and IDs with the model-request snapshot | Proven as local engineering evidence | `focused_tests.txt`; fixture data and a mock provider, not the retained dataset. Earlier SQL Server and browser runs stand |
| 8. Finite live walkthrough with actual model consumption and visible attributed flag | Unproven | Simulator, Hub, SQL and UI legs observed live; the model leg is blocked by the missing approved release |

Criteria 1, 2 and 9 are already ticked; criteria 1 and 2 were seen live again.

## Live observations (20:55 to 20:58Z)

* Active revision `ca-cutover-test-demo-api--0000053`. Role `Retrofit Programme Manager`.
* `GET /api/cases/{id}/sensors`: seven of twelve cases return `ok` and `fresh` with 12 readings (cap 12): ZF-2025-0331, 0150, 0032, 0389, 0340, 0364 and ZF-2026-0742. Reading IDs have the form `LIVE-<sensor>-<UTC stamp>Z`, for example `LIVE-SIBP5GIQWTN-20261122T1835Z`. The other five return `consent-withheld`.
* The [Home sensors panel screenshot](../../../.copilot-tracking/evidence/2026-11-22/issue-1288-live8/live-sensor-panel.png) shows "Recent reading (within 15 minutes)", 7.31 degC and 86.91 %RH observed 20:50 UK time, sensor SIBP5GIQWTN, the source text "Outdoor weather. Not calibrated.", a chart with a text summary and the no-alerts statement. The [AI tab screenshot](../../../.copilot-tracking/evidence/2026-11-22/issue-1288-live8/live-ai-tab.png) shows the request buttons, no suggestions and the manual route.
* The Quality model stays blocked: release admission is denied with authority gaps for release, residual-risk acceptance, suspension and restart (OQ-017). The bound model is `gpt-4.1-nano-2025-04-14` on the demo endpoint, with `tokens` 0 and `consumption` 0 in `rai-metrics`, which was identical before and after the probe.
* `live_probe.py` and the scrubbed `live_probe.json` are retained; the probe scrubs email addresses and holds no token or key.

## Why criteria 4 and 8 stay unproven

The model leg needs an approved, unexpired release record from a named release owner. The 2026-11-18 owner decisions waive DPO and Legal approval for the demo but neither appoint a release owner nor authorise writing a release record. Creating one with a demo account would fabricate that authority, and a bypass or mock response would be the deterministic outcome the criterion excludes. The remaining step is a human release approval, not code, so no source change is justified.

## Evidence limits

* Azure facts are read-only API output and the simulator state changes every five minutes.
* Independent exact-head review and hosted CI are outstanding. No tick or closure is claimed; criteria 3 to 8 stay unticked.

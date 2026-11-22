---
title: Issue 2202 final live proof on API revision 0000053 and resident revision 0000025 (2026-11-22)
description: Desktop Playwright and Azure CLI proof on the deployed demo after the 2245 meter fix, map retry and 2008 xlsx preview, with a per-criterion pass or fail table for 2202
ms.date: 2026-11-22
ms.topic: reference
---

Scope: synthetic demo, desktop 1440x900, resource group `ama`, owner decisions of 2026-11-18. Sign-in values were read at run time and never printed; every saved result was checked for their absence (and for any `@`). Probes, JSON outputs and screenshots: [issue-2202-finalproof-2026-11-22/](./issue-2202-finalproof-2026-11-22/). Refs #2202 (also exercises #2245 and #2008). Focused tier, documentation only: nothing was changed, deployed or pushed, and no Azure resource was created. The build commit (main `7a125f470`) is taken from the task brief; only image digests were read.

## Deployed state

[az-state.txt](./issue-2202-finalproof-2026-11-22/az-state.txt): `ca-cutover-test-demo-api--0000053` (Running, Healthy, 100 percent, created 19:38 UTC) with `ZF_CONTAINER_HARDENING=enforced`, and `ca-resident-demo--0000025` (RunningAtMaxScale, Healthy, 100 percent, created 19:38 UTC). The agents app also has hardening `enforced`; the resident app has no such variable. Receiver executions at 18:00, 18:30 and 19:00 Succeeded; simulator executions from 19:22 to 19:45 Succeeded.

## Requested checks

| Check | Result | Evidence |
| --- | --- | --- |
| Employee chat, 10 timed asks | Pass for latency | 10 of 10 returned HTTP 200 in 3.09 to 5.37 s (median about 4.1 s); thread creation 0.28 s. Two control requests were refused with the human-decision message; eight asks returned kind `fallback` saying AI answers are on hold. [asks10_probe.json](./issue-2202-finalproof-2026-11-22/asks10_probe.json) |
| First ask through the widget | Pass | Dedicated UI probe: ask started 0.4 s after load, answered after 7.2 s (HTTP 6.48 s). [firstask_ui_probe.json](./issue-2202-finalproof-2026-11-22/firstask_ui_probe.json) |
| Chat AI hold label | Pass | `/api/chat/status` disclaimer ends "AI answers are on hold: an open suspension covers AI work, so replies use rules only." and replies say so. No generative answer exists to prove (see unproven items). [probe-staff-chat-result.json](./issue-2202-finalproof-2026-11-22/probe-staff-chat-result.json) |
| Map loads | Pass | Markers appeared after 3.3 s; 443 markers; `/api/map` HTTP 200, 443 items; sensor states fresh 59, consent-withheld 22, no-readings 19, not-loaded 343. [probe-staff-result.json](./issue-2202-finalproof-2026-11-22/probe-staff-result.json), [screen](./issue-2202-finalproof-2026-11-22/screens/staff-overview-map.png) |
| Check a spreadsheet with the synthetic `.xlsx` | Pass | Input `accept` now lists `.xlsx`; [demo-case-list.xlsx](./demo-workbook/demo-case-list.xlsx) returned `/api/import-check` 200: sheet "Cases", 6 rows ready, 4 to fix, mapping table, "Duplicate reference DEMO-002 on rows 3 and 11"; workbook SHA-256 unchanged. [probe-xlsx-result.json](./issue-2202-finalproof-2026-11-22/probe-xlsx-result.json), [screen](./issue-2202-finalproof-2026-11-22/screens/xlsx-02-result.png) |
| Resident chart | Pass | Four SVG labels render at 19 px, 8 stored-reading circles, legend and "Latest stored" text present. [probe-resident-result.json](./issue-2202-finalproof-2026-11-22/probe-resident-result.json), [screen](./issue-2202-finalproof-2026-11-22/screens/resident-sensors-chart.png) |
| Safety count | Pass | Tile 23, 23 safety markers, filtered list 23, `/api/cases?flag=hazard` total 23; no "elapsed time unknown" text. |
| Handoff waiting view | Pass | 4 unaccepted handoffs listed with "Unknown. The offered time has no recorded timezone"; ZF-2025-0030 case page still says "Offered to Miguel Garcia, not yet confirmed". [screen](./issue-2202-finalproof-2026-11-22/screens/staff-handoff-waiting.png) |
| Chat meter (#2245) | Pass for the disclosure | The hold is shown as a hold, not a meter or limit message. The employee path never reached the model. |

## Per-criterion table for #2202

| Criterion | Result | Basis |
| --- | --- | --- |
| API, resident, simulator and receiver images rebuilt from main and rolled | Partly proven | API and resident revisions 0053 and 0025 exist with new digests, created 19:38 UTC. Simulator and receiver jobs run on digests set in the earlier rollout ([receipt](./issue-2202-live-deploy-2026-11-22.md)); this pass did not rebuild them and cannot show their source commit. |
| Revisions Running and Healthy; hardening enforced with rollback noted; agents app difference explained | Partly proven | Running and Healthy and `enforced` shown above. Rollback: earlier API revisions are not retained, so a rollback is a re-deploy of a prior digest or setting the variable back; it was not exercised. The agents app is also `enforced`, so no api versus agents difference was found; the resident app carries no hardening variable and no explanation was recorded. |
| Owner demo checks: sensor charts | Pass | Resident chart above. |
| Owner demo checks: map gauges | Partly proven | Map loads with sensor states; individual gauge rendering was not inspected in this pass. |
| Owner demo checks: consent checkbox | Unproven on these revisions | Proven earlier on resident 0024 ([2192 r4](./issue-2192-live-r4-2026-11-22.md)); not re-run on 0025. |
| Owner demo checks: chat routing | Pass | Employee reply "Routed to the Funding evidence agent"; resident replies routed to the Safety route helper and Documents helper. |
| Owner demo checks: half of homes with readings | Unproven in this pass | 59 of 443 map items show a fresh state in the map snapshot; the 15-of-15 series above half is in [2191 re-proof](./issue-2191-live-coverage-reproof-2026-11-22.md) and was not repeated. |
| Live receipt and `docs/reference/log.md` entry | Pass | This note and the log entry; earlier receipt linked above. |

## Unproven or blocked

* No generative AI answer exists in either chat. The employee path is on hold under an open suspension and the resident path reports "AI usage limit was reached" (label "Summary by rules - AI unavailable: the AI usage limit was reached"); both need owner decisions ([2202 deploy proof](./issue-2202-deployproof-2026-11-22.md)).
* The earlier widget probe `probe_staff_chat.py` again timed out on its first ask (no `/ask` response event in 120 s) while its second ask succeeded and the direct API asks and the dedicated UI first-ask probe answered in under 8 s. The timeout is not reproduced by the UI probe and is treated as a probe artefact, not diagnosed. The first `probe_staff.py` run failed to render the app once (page timeout) and passed on a single rerun.

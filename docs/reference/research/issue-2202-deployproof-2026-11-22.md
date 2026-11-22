---
title: Issue 2202 live proof of the merged demo fixes (2026-11-22)
description: Desktop Playwright proof on the deployed demo that fixes 2255, 2245, 2243, 2253, 2254 and 2256 work, with the map check, screenshots and a per-item pass or fail table
ms.date: 2026-11-22
ms.topic: reference
---

Scope: synthetic demo, desktop 1440x900, resource group `ama`, owner decisions of 2026-11-18. Sign-in values were read at run time and never printed; every saved result was checked for their absence. Probes, JSON outputs and screenshots: [issue-2202-deployproof-2026-11-22/](./issue-2202-deployproof-2026-11-22/). Refs #2202. Focused tier, documentation only; nothing was changed, deployed or pushed, and no Azure resource was created.

## Deployed state

`az containerapp revision list` shows `ca-cutover-test-demo-api--0000051` (Running, Healthy, 100 percent traffic) and `ca-resident-demo--0000023` (RunningAtMaxScale, Healthy, 100 percent traffic), the revisions named in the brief as built from main `a6c0910c9`. Images were read by digest only; the build commit was taken from the brief, not re-derived.

## Results

| Item | Result | Evidence |
| --- | --- | --- |
| 1. Target clock and named owner on demo hazards (#2255, #76) | Pass | Safety list of 23 cases: 22 hazard cases show "N hours elapsed; service response due ...; response open or overdue. Accountable owner: Karen Lawson" (5 open, 17 overdue); the 23rd is the safeguarding case ZF-2025-0148 with its own clock and "Synthetic Safeguarding Lead (demo)". No "elapsed time unknown" text remains (0). The backfill tool was not needed: the earlier live run is still in place. [probe-clock23-result.json](./issue-2202-deployproof-2026-11-22/probe-clock23-result.json), [probe-clock4-result.json](./issue-2202-deployproof-2026-11-22/probe-clock4-result.json), [probe-staff-result.json](./issue-2202-deployproof-2026-11-22/probe-staff-result.json), [screen](./issue-2202-deployproof-2026-11-22/screens/staff-safety-list.png) |
| 2a. Generative answer in employee chat (#2245) | Fail (blocked) | Two asks returned HTTP 200 with answer origin "decision_rule ... not generative AI" and model `workflow-only`; one ask produced no response in 120 s. `/api/chat/status` now states "AI answers are on hold: an open suspension covers AI work, so replies use rules only", so the disclosure fix works, but no model call was made. `/api/continuity` lists one open suspension, scope all, "Demo probe: negative test", recorded 2026-11-18. Lifting it is a named-human restart, which was not done. [probe-staff-chat-result.json](./issue-2202-deployproof-2026-11-22/probe-staff-chat-result.json), [probe-continuity-result.json](./issue-2202-deployproof-2026-11-22/probe-continuity-result.json), [screen](./issue-2202-deployproof-2026-11-22/screens/employee-chat.png) |
| 2b. Generative answer in resident app (#2243) | Fail (blocked) | Label for a supported question ("How is my case going?"): "Summary by rules - AI unavailable: the AI usage limit was reached". The old "AI exercise has ended" message is gone, so the env-driven expiry fix is live, but `resident_ai.reserve` still refuses. Probable cause: the ledger `expires_at` column defaults to 2026-11-01 ([infra/sql/resident-assistant.sql](../../../infra/sql/resident-assistant.sql)); the other refusal reasons are 5 attempts per resident per hour and 2000 attempts in total. Not read directly: SQL has public access Disabled. [probe-resident-ai-b.json](./issue-2202-deployproof-2026-11-22/probe-resident-ai-b.json), [probe-resident-result.json](./issue-2202-deployproof-2026-11-22/probe-resident-result.json), [screen](./issue-2202-deployproof-2026-11-22/screens/resident-ai-b.png) |
| 3. Resident chart text size and stored-reading markers (#2253) | Pass | On Sensors, the four SVG labels (-10, 17.5, 45, "Latest stored") render as normal text with no overlap; 8 circle markers on the stored line (48 readings; the legend says circles mark some of them). [screen](./issue-2202-deployproof-2026-11-22/screens/resident-sensors-chart.png), [chart crop](./issue-2202-deployproof-2026-11-22/screens/resident-chart-svg.png) |
| 4. Safety count matches tile and map (#2254) | Pass | Overview tile 23, 23 safety markers of 443, "Show only: Safety issue open" list 23, `/api/cases?flag=hazard` total 23. The earlier 23 versus 22 split is gone. [probe-staff-result.json](./issue-2202-deployproof-2026-11-22/probe-staff-result.json), [screen](./issue-2202-deployproof-2026-11-22/screens/staff-overview-map.png) |
| 5. Handoff waiting view shows untimed offers (#2256) | Pass | `#/handoff-waiting` lists 4 unaccepted handoffs (ZF-2025-0029 to 0032), each with chase owner and receiver, waiting and due shown as "Unknown. The offered time has no recorded timezone". ZF-2025-0030 now appears; its case page still says "Offered to Miguel Garcia, not yet confirmed". [screen](./issue-2202-deployproof-2026-11-22/screens/staff-handoff-waiting.png) |
| 6. Map loads with readings | Pass | Markers appeared after 3.3 s; 443 markers; `/api/map` HTTP 200 with 443 items, sensor states fresh 58, stale 1, consent-withheld 22, no-readings 19, not-loaded 343 (shown on demand). |

## Limits of this proof

* Item 1 counts are parsed from list text; three rows were matched out of order by the per-case parser, so the case-level count is 19 of 22 while the page-level count is 22 of 22. The 23 rows were all present.
* The employee chat has no generative evidence: the one ask that timed out is not explained. The cause of the timeout was not diagnosed.
* "Half of homes with readings" is not a #2202 item here; 59 of 443 map items carry a fresh or stale reading, with the rest not loaded, withheld or empty.

## Owner decisions still needed for generative AI

* Suspension: accept the open suspension as evidence and lift it through the route in [issue-221-live-suspension-restart-evidence-2026-11-18.md](./issue-221-live-suspension-restart-evidence-2026-11-18.md), or approve another removal.
* Resident ledger: extend `resident_ai.budget.expires_at` through a private SQL path as the owner-reviewed data change in `infra/README.md`, then run `probe_resident_ai.py` again.

Related: [2245 and 2243 live diagnosis](./issue-2245-live-2026-11-22.md), [2255 clock backfill](./issue-2255-live-2026-11-22.md) (its note names the held tool in worktree issue-2255-live-20261122T152731Z).

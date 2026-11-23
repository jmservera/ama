---
title: Issue 2253 live r5 research
ms.date: 2026-11-23
---

Refs #2253. Opening note: prior rounds r1 to r4 and merged fix #2305 exist. Live revision is now ca-resident-demo--0000028 (created 2026-11-23T12:31Z). This round probes that revision for each Expected criterion; findings follow below.

## Findings

* Live probe ([probe](../../docs/reference/research/issue-2253-live-2026-11-23/probe_r5.py), [json](../../docs/reference/research/issue-2253-live-2026-11-23/live-r5-0000028.json), [png](../../docs/reference/research/issue-2253-live-2026-11-23/live-r5-0000028.png)), 1440x900, synthetic resident: axis labels render at 12 user units x 1.396 = 16.8 px against 16 px body text; 0 text overlaps; 18 stored-reading circles; 1 touching circle pair; 0 forecast squares and no "Latest stored" label because the stored history ends 22 Nov 2026 03:30 and the page states no forecast is shown for readings older than 24 hours.
* Deployed script (`/demo.js`, fetched from the live app) contains neither `roomLeft` nor `markerGap`, so merged fixes #2258 and #2305 are not in the live image (digest ...e6c7e755, revision 0000028). No deploy is authorised for this task.
* Local source: `src/api/checks/resident_sensors_browser_check.py` all PASS (0 FAIL), including forecast shape and dash, 6 forecast rows, stale-history flag; `test_epic149_child_ux_contracts` 15 tests OK, including the guards for marker replacement and label flip.
* Planning Readiness: Ready. No source change is needed; source already carries the fix.
* Critique: the plan below was challenged once; verdict proceed with record-only scope.

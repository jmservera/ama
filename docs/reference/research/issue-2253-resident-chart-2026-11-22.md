---
title: Issue 2253 resident sensor chart fix evidence
description: Live reproduction and local after-fix proof for oversized chart labels and merged markers
ms.date: 2026-11-22
---

Scope: synthetic demo, desktop 1440x900, owner decisions 2026-11-18. Refs #2253, found in the #2202 walkthrough.

## Cause

* Chart text was sized `1.25rem` in SVG user units, so it scaled with the SVG (factor 1.396 at 1440 px) to 27.9 px against 16 px body text and overlapped.
* 48 stored readings about 4 user units apart with r=3 circles merged into a thick stroke (46 of 48 circles touched a neighbour).

## Evidence

| Run | Source | Text px | Text overlaps | Circles | Touching circles |
| --- | --- | --- | --- | --- | --- |
| Before | live `ca-resident-demo`, signed in as the synthetic resident ([json](issue-2253-resident-chart-2026-11-22/before-live.json), [png](issue-2253-resident-chart-2026-11-22/before-live.png)) | 27.9 | 1 | 48 | 46 |
| After | worktree sources with the sensor browser-check fixtures ([json](issue-2253-resident-chart-2026-11-22/after-local.json), [png](issue-2253-resident-chart-2026-11-22/after-local.png)) | 16.8 | 0 | 25 | 0 |

Scripts: [probe_chart.py](issue-2253-resident-chart-2026-11-22/probe_chart.py) (credentials read at runtime, never printed) and [after_local.py](issue-2253-resident-chart-2026-11-22/after_local.py).

## Limits

* The deployed demo was not redeployed (no production change authorised), so the fix is not proven live; deploy and rerun `probe_chart.py` to close that.
* Circles now mark some readings (about every 9 user units, always the latest); the line and the table carry every reading and the legend says so.
* Narrow screens are out of scope for the demo; a 30rem rule raises the text size there but was not browser-tested.

## Live verification 2026-11-22 (second run, after #2258 deployed)

Main holds the fix (`a6c0910c97`, #2258). The live `ca-resident-demo` revision `ca-resident-demo--0000025` (created 2026-11-22T19:38:51Z, after the fix commit at 17:31Z) was probed with the unchanged `probe_chart.py`, signed in as the synthetic resident, desktop 1440x900 ([json](issue-2253-resident-chart-2026-11-22/after-live-main.json), [png](issue-2253-resident-chart-2026-11-22/after-live-main.png)). No source or Azure change was made.

| Criterion (issue "Expected") | Live result | Status |
| --- | --- | --- |
| Axis and marker labels sized like body text | 16.8 px against 16 px body text (was 27.9 px) | Proven |
| No overlap of 'Latest stored' and the 45 tick | 0 text overlaps; screenshot shows separate labels | Proven |
| Circle markers on stored readings as the legend states | 8 circles drawn on the line, legend now says circles mark some readings | Proven |
| Stored readings no longer one thick stroke | 1 of 8 circle pairs touches (the always-drawn latest marker); the line is thin | Proven, with the touching pair noted |

The earlier "not proven live" limit is closed. The 30rem narrow-screen rule stays untested because the demo is desktop only.

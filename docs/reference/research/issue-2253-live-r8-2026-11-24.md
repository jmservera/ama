---
title: Issue 2253 resident chart live re-proof on current revision (r8)
description: Live Playwright proof of the resident sensor chart on ca-resident-demo revision 0000030
ms.date: 2026-11-24
---

Refs #2253. Synthetic demo, desktop 1440x900, resident account from the runtime credential file (not recorded). No deploy and no Azure change. The issue lists no checkbox criteria, so the five "Expected" statements are treated as the criteria.

## Method

* `az containerapp revision list -n ca-resident-demo -g ama`: one active revision, `ca-resident-demo--0000030`, created 2026-11-24T14:32:22Z, 100% traffic.
* [probe_r8.py](issue-2253-live-r8-2026-11-24/probe_r8.py) signs in, opens Sensors, measures computed SVG text size, text box overlaps, circle markers and legend. Output: [live-r8-0000030.json](issue-2253-live-r8-2026-11-24/live-r8-0000030.json), [live-r8-0000030.png](issue-2253-live-r8-2026-11-24/live-r8-0000030.png).
* Local: `python3 -m unittest tests.test_epic149_child_ux_contracts` in `src/api` (17 tests OK, includes the label geometry and out-of-range clamp tests).

## Live results

| Measure | Result |
| --- | --- |
| Axis tick font | 12 px in viewBox units, scale 1.396, so about 16.75 px rendered; body text 16 px |
| Text box overlaps | 0 |
| Stored circle markers | 17 circles, 0 touching; line plus separate circles, not a blob |
| Forecast squares and "Latest stored" label | 0 and absent: live stored data ends 22 Nov 2026 03:30, so the page correctly says no forecast is shown because the reading is over 24 hours old |

## Criteria

| Criterion | Status |
| --- | --- |
| Axis labels sized like body text | Proven live on 0000030 |
| No overlap of labels | Proven live for axis ticks; "Latest stored" overlap proven locally only (label not rendered live) |
| Circle markers on stored readings | Proven live |
| Stored readings not one thick stroke | Proven live |
| Forecast squares render normally | Not provable live: needs fresh telemetry within 24 h, and injecting readings is a data change outside the brief. Proven by local tests |

The earlier "Latest stored" label overlap fix (#2305) is therefore verified only by the local geometry test until fresh readings exist.

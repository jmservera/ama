---
title: Issue 2254 map markers on screen, live proof (2026-11-23)
description: Playwright count of Safety issue open map markers on the employee Overview against the tile, the All cases filter and the API, closing the map gap left by earlier 2254 notes
ms.date: 2026-11-23
ms.topic: reference
---

Scope: synthetic demo, desktop 1440x900, `ca-cutover-test-demo-api`, role Retrofit Programme Manager. Read-only; no Azure change and no throwaway resource. Sign-in values were read at runtime and are not recorded. Earlier evidence: [reproduction](./issue-2254-live-probe-2026-11-22.md), [API verification](./issue-2254-verify-2026-11-22.md) and [on-screen tile and list](./issue-2254-ui-2026-11-23.md).

| Surface | Count | Source |
| --- | --- | --- |
| Overview tile "Safety issues open" | 23 | [probe-map-result.json](./issue-2254-map-2026-11-23/probe-map-result.json) |
| Map markers titled "Safety issue open" (of 443 rendered) | 23 | same result, [01-overview-map.png](./issue-2254-map-2026-11-23/screens/01-overview-map.png) |
| `/api/map` hazard items (mode points, total 443) | 23 | same result |
| `/api/cases?view=all&flag=hazard` total | 23 | same result |
| `/api/stats` hazards KPI | 23 | same result |
| All cases page, Show only = Safety issue open | "23 cases" | [on-screen note](./issue-2254-ui-2026-11-23.md) |

All five surfaces use one definition and agree at 23 on 2026-11-23. The marker count was read from the DOM after the map drew; the screenshot was taken at the same moment and may show the map area before tiles load. Script: [probe_map.py](./issue-2254-map-2026-11-23/probe_map.py).

Limits: the deployed image digest is not mapped to a source commit, and the stored `hazard` column of the earlier mismatch row cannot be read because SQL public access is disabled. The agreement is observed, not a proof of the cause.

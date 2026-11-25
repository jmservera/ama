---
title: Issue 2202 live research 2026-11-25
description: Research record for re-proving the open acceptance criteria of #2202 on the deployed synthetic demo
ms.date: 2026-11-25
---

Refs #2202. Research disposition: executed. Planning Readiness: Ready.

## Scope

All four criteria of #2202 are unticked. Prior evidence: `docs/reference/research/issue-2202-live-r68-2026-11-24.md` (API 0000068). Estate now: API `--0000072` (digest 14f917d6...), resident `--0000030`, agents `--0000004`, jobs on digest 06f3170c... Evidence directory: `docs/reference/research/issue-2202-live-r72-2026-11-25/`.

## Findings

* Revisions Healthy at 100%, `ZF_CONTAINER_HARDENING=enforced` on three apps and both jobs (az-state.txt). Jobs run a different API digest than the API app; provenance is not readable (registry firewall).
* Map: 443 homes, 261 with readings (58.9%); fresh share 8.8% at read time because the 15 minute window had just passed and the simulator emits at :00/:07/:15/:22/:30/:37/:45/:52 (coverage-result.json). Not a defect.
* Map gauges: two `meter` elements with text, no animation (live-map-card-probe.json).
* Resident consent checkbox visible, unchecked, checkable, wrapped label (probe-resident-result.json). First attempt got 429 from the login throttle after a failed run, cleared on retry.
* Chat routing: six questions routed or refused as expected; workflow-only because the AI allowance is not available. Four retries after a 5xx (live_routing_probe.json).
* Defect: the Home sensors tab stayed on "Loading home sensors" and `GET /api/cases/ZF-2025-0331/sensors` returned 503 at 17:43:57 while the receiver job held the SQL write lock (same minute: proposals and chat thread creation 503 with `cause=sql-write-lock-busy`). With no contention the same tab renders the two-axis chart (live-chart-probe.json) and 30 sensor GETs returned 200 (max 4.24 s). Cause in code: `AssistantService.sensors` and `map_sensors` read through `transaction()`, which takes the application-wide exclusive write lock, although they write nothing (`sensor_view`, `sensor_map` contain no writes). `_read_connection()` is the existing lock-free read path used by the forecast.

## Routing

Change `sensors` and `map_sensors` to `_read_connection()`. The wider receiver lock duration (#2320) stays out of scope.

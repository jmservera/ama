---
title: Issue 2257 live research (2026-11-23)
ms.date: 2026-11-23
---

Research disposition: executed (opened; findings below are completed after the live probe).

## Scope

Issue #2257 has no checkbox list. Its Expected section gives two criteria: the map retries or recovers without a reload, and the cause is found. A third implied criterion is that fresh sign-ins no longer fail.

## Prior evidence

* Main contains 0234e8e79d (#2261, `fetchReadRetrying`) and 10cad2e413 (#2283, map-path regression test in `test_workspace_scripts.py`).
* Live API revision at open: `ca-cutover-test-demo-api--0000054`, Healthy, 100 percent traffic, created 2026-11-22 23:14 UTC.
* Earlier notes: `docs/reference/research/issue-2257-mapfetch-live-2026-11-22.md` and `issue-2257-verify-live-2026-11-22.md` (revision 0000053).

## Planning Readiness

Ready: re-prove on revision 0000054 and decide whether any code gap remains.

## Findings (live, revision 0000054, 2026-11-23 01:44 to 01:52 UTC)

* Injected reset: first `/api/map` aborted, retried, 200, 443 markers, no error (deployed client already has #2261).
* Eight fresh sign-ins: 7 loaded 443 markers; run 5 showed "Map unavailable" after a server `GET /api/map` 500 (JSON error, not a dropped connection). Console log: `exc=ProgrammingError` at 01:46:19 UTC, also at 00:47:00 and 00:54:52 UTC. Message text is deliberately not logged, so the exact driver error is unknown.
* 40 sequential and 6 parallel `/api/map` calls in one warm session: all 200 (`load-probe-result.json`). The failure appears only on fresh sessions, when boot reads overlap.
* A second failure mode therefore exists besides the dropped connection (#2261): an application 500 the client rightly does not retry (`test_workspace_scripts` pins JSON 500 as an error).
* Code gap: `AssistantService.map_sensors` opens a SERIALIZABLE transaction on the assistant connection; only per-home reads are guarded by `sensor_map.summary`. A failure in the transaction itself (begin, authorise, commit) escapes and turns an optional sensor overlay into a whole-map 500. The origin of the live ProgrammingError is not proven to be this path.

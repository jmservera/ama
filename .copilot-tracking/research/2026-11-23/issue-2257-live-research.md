---
title: Issue 2257 live research (2026-11-23, run 084412Z)
ms.date: 2026-11-23
---

Research disposition: executed. Planning Readiness: Ready.

## Scope

Issue #2257 has no checkbox list. Its Expected section gives two criteria: the map retries or recovers without a reload, and the cause is found. The owner goal for this run adds a bounded retry, a visible retry control and a regression test.

## Audit (main at f40302db55)

* Route `GET /api/map` (`server.py` line 1303): only `ValueError` is mapped (to 400); any other exception is a JSON 500.
* Overlay: `AssistantService.map_sensors` already degrades to `unavailable` on a transaction failure (#2292, merged 2026-11-23 03:14 UTC).
* Client: `api()` reads through `fetchReadRetrying`, which retries a dropped connection twice (400 and 1200 ms) and a non-JSON gateway failure three times. A JSON 500 is deliberately shown, not retried.
* Gap 1: `mapPanel.draw` shows "Map unavailable: ..." with no control. After the bounded read retries (about 1.6 s) fail, the panel stays empty until a reload or a map move; this matches "0 markers for 90 s" in the issue.
* Gap 2: no test pins a recovery path for the map panel after the read retries are exhausted.

## Live evidence (revision 0000055, Healthy, 100 percent, created 2026-11-23 03:25 UTC)

* Eight fresh sign-ins at 08:45 to 08:50 UTC: 8 of 8 loaded 443 markers, no "Map unavailable", `/api/map` 200 each time, wait 11.9 to 32.6 s (`docs/reference/research/issue-2257-retry-control-2026-11-23/probe-result-085002.json`, probe `live_probe.py`, credentials read at runtime only).
* API console log, last 300 lines: 0 lines matching `ProgrammingError` or `map sensor summary unavailable`.
* The earlier failures (0000054: 1 of 8, JSON 500 with `ProgrammingError`) are in `docs/reference/research/issue-2257-live-2026-11-23.md`. The Azure estate was not changed by this run.

## Root cause status

Two failure modes are evidenced: a dropped connection while a replica leaves the pool (retried since #2261) and a server 500 from the overlay transaction (hardened by #2292). The exact driver message of the live `ProgrammingError` was never recorded, so that origin stays unproven. After the hardening, 8 of 8 fresh sessions loaded, which is consistent with but does not prove the fix (small sample, intermittent fault).

## Decision for this task

Add a visible "Try the map again" control and one bounded automatic redraw for a status-less (network) failure, plus a regression test. Do not retry JSON 500 responses in the client.

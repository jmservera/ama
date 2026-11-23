# Issue 2257 r6 research

Scope: synthetic demo, desktop only. Issue body has no tick-list; criteria come from its Expected line ("the map retries or recovers without a reload, and the cause is found") and the r5 table.

## Findings

* Read first: r5 research and changes, r3 and r2 notes. Covered already: retry button, one automatic redraw after a dropped connection, `fetchReadRetrying` (network drops and non-JSON 500/502/503/504 startup failures), backlog 128, keep-alive timeout 300, lock and SQLSTATE log tags.
* New angle, not covered: `api()` sets `error.status` on any non-OK response, and the map's automatic redraw runs only when `!error.status`. A gateway failure (non-JSON 500/502/503/504) that outlasts `STARTUP_RETRY_DELAYS` (5 s in total) therefore ends with a visible notice and no automatic redraw, while a dropped connection gets one. A replica restart is the likeliest cause of the 90 s empty map in the issue, and it presents as this gateway response.
* The check `startupFailure(res)` already identifies these responses; `api()` does not record the result on the error.
* Criteria: cause logged (r5, code and test); recovery without reload (extended here to gateway failures; unit-tested, live proof needs a deployed image); fresh-session failure rate not provable by sampling; billing, DPO or Legal, assistive-technology testing not needed (owner decision 2026-11-18).
* No Azure change or credential use is needed: the deployed image predates the change.

## Planning Readiness

Ready. Research disposition: executed.

# Research: connected-home check anchor (#149, 20261113T1509Z)

* Failing test: `test_every_exclusion_rests_on_its_source_anchor_and_reads_no_home_field`, `programme-queue` / `Shared queue`, anchor `loadPage(0)`.
* The check lives at `src/api/checks/connected_home_browser_check.py` (not `src/checks/connected_home_check.py`); the renderer is `src/api/src/zava_forward/api/web/role-screens.js`.
* After #233 `programmeQueue` takes `start` and calls `loadPage(start)` (line ~534); `loadPage(0)` no longer exists.
* The exclusion stays valid: the panel renders a paged all-homes queue (portfolio call), reads no `c.` home field, and its connected-view links carry only row ids.
* The scenario manifest does not reference the check file, so no digest update is needed.
* Planning readiness: Ready.

# Issue 2257 r6 plan

* [x] Record `error.gateway` in `api()` when a non-OK read matches `startupFailure(res)`.
* [x] Let the map's automatic redraw run when `!error.status || error.gateway`.
* [x] Extend `test_map_failure_offers_a_visible_retry_and_one_bounded_redraw` with a gateway case and a JSON 500 case.
* [x] Run the test, ruff and the web-file tests; record the research note, index and log.

Details: `.copilot-tracking/details/2026-11-23/issue-2257-live-r6-details.md`.

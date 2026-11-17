# Research: resident demo bulkhead retry guidance (#1054)

* Date: 2026-11-14. Refs #1054, Refs #462. Base 656bf1cf1 (#1639).
* Finding: `_route` in `src/api/src/zava_forward/api/resident_demo/app.py` already sheds with 503, `Retry-After: 3` and `retry_after`; `demo.js` `loadView` retries once.
* Gaps: payload key not machine-explicit (`retry_after_seconds`), wording generic, banner did not state the wait.
* Scope: bulkhead only; callback agenda UI (#1053) untouched. Planning readiness: Ready.

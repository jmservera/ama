# Issue 2190 live details, 2026-11-23

## Phase 1

* `_region_passed`: result is the header remainder equal to `ok`, or any line equal to `ok`; failing patterns unchanged.
* `tools/test_rpi_checks.py`: add rejected shapes `header ... log` + `log status ok`, and a log line ending `ok` with the real result missing.

## Phase 2

* `test_rai_release_readiness_api_218.py`: replace the constant-pinning test with a local delayed server. Real budget returns the reply; a budget below the delay raises `TimeoutError`.

## Phase 3

* `employee_chat_browser_check.py`: add `settle_route(page, destination)` waiting for `#workspace-status` to start with `Perspective:` when the destination is `#/`, then `networkidle`; call it in the route and keep the comparison unchanged.
* Test the call order and predicate with a recording page double.

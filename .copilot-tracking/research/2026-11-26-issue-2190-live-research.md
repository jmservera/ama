# Research: issue 2190 gate flakes (2026-11-26)

Disposition: executed (re-verification). Planning Readiness: Ready.

Issue criteria: each flake reproduced or explained; fixed with a regression test; no check relaxed. Fixes exist on main from earlier runs (notes under docs/reference/research/issue-2190-live-*). This run re-verifies on head ae73889080 and looks for new defects.
Scope: tools/rpi-checks.py parsers, src/api/checks/employee_chat_browser_check.py, src/api/tests/test_rai_release_readiness_api_218.py. No Azure change needed.

## Evidence (head ae73889080)

* tools: `python3 -m unittest test_rpi_checks`: 133 tests OK (flake 1 parsers).
* chat browser check (flake 2): 3 of 3 runs PASS with pinned axe 4.10.3 (sha256 matches AXE_SHA256).
* 218 suite: 5 tests OK (flake 3), but verbose output shows a BrokenPipeError traceback from the Slow handler in `test_request_budget_is_the_read_timeout_against_a_slow_server`, printed into the gate log (the same log-noise class as flake 1). Real defect: noise only, not a failure.

Decision: silence the expected broken pipe in the test handler (no check relaxed).

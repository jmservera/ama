# Issue 2190 research (2026-11-22, run 20261122T231555Z)

Main 3219004e90 already carries the three fixes (c9350f3a3b, cd687ef558). Re-run on this head:

* `python3 -m unittest tools.test_rpi_checks`: 127 tests OK (log-interleaving fix and rejection tests).
* `src/api` `tests.test_rai_release_readiness_api_218`: 5 tests OK (timeout budget).
* Flake 2 (`late_success`): fix is `page.wait_for_load_state("networkidle")` before the first `state.snapshot()` in `src/api/checks/employee_chat_browser_check.py`. No regression test pins that ordering; a real-browser race cannot be forced deterministically.

Planning readiness: Ready. Proposal: a structural AST test in `tools/test_rpi_checks.py` (tools, not src) asserting the settle precedes the baseline snapshot. No Azure involvement; synthetic demo, desktop only.

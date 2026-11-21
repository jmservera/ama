# Research: issue 2190 gate flakes (2026-11-21)

Disposition: executed. Planning readiness: Ready.

Criteria (issue body): each flake reproduced or explained; fixed with a regression test; no check relaxed.
Flakes: (1) log interleaving in `_classes_executed`/`_region_passed`/`check_skips` in tools/rpi-checks.py; (2) `late_success` in src/api/checks/employee_chat_browser_check.py; (3) urllib TimeoutError in test_rai_release_readiness_api_218.

Finding: main (62496349e8) still has all three defects. A sibling local branch `test/gate-flakes-live-20261121T090344Z` (commit 17461b0291, never merged) holds fixes plus its own research note with before/after runs. Plan: independently re-verify, then port its src/tools/test changes.

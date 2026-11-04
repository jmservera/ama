# Issue 129 slice 2 plan

* [x] Add src/core/src/zava_forward/core/learning_test_bundles.py (pure, no AI, no data).
* [x] Add src/core/tests/test_learning_test_bundles.py.
* [x] Update protocol, reference index row and log.md.
* [x] Run unit tests, ruff, mypy (cache /tmp/mypy-530). No gate, benchmark or full suite.
* Critique (single pass, self-run): validation rejects missing/negative effort; comparator win is valid; stop rule not averaged; no UI so Fluent/WCAG unaffected. Verdict: proceed, no conflicts.

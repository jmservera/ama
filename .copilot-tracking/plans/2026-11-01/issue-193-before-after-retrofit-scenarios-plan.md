# Issue 193 plan

* [x] Phase 1: add `retrofit_exercise_scenarios()` and `expected_direction` helper in `sensor_scenarios.py` (analysis rows separate from labelled exercise expectation; label "EXERCISE VALUE, not sourced").
* [x] Phase 2: add tests in `src/core/tests/test_sensor_scenarios.py` covering four outcomes, direction/size labels, and that consumer-facing records carry no truth in rows.
* [x] Phase 3: update `src/core/README.md` pointer and the R3 note that #111/#133 use remains unproven.
* [x] Phase 4: run unittest, ruff check, ruff format --check, mypy for src/core; commit, push, PR with `Refs #193`.

Critique (single pass): keep API minimal; do not claim AC3; no new fixtures or files outside src/core. Compatible, applied directly.

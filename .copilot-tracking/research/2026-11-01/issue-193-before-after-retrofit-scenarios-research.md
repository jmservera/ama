# Issue 193 research: before and after retrofit scenarios

* Date: 2026-11-01; task: issue-193-before-after-retrofit-scenarios; Research disposition: executed; Planning Readiness: Ready.

## Evidence

* `src/core/src/zava_forward/core/synthetic/sensor_scenarios.py` already generates four retrofit cases (improvement +2 C/-10 RH, no change, delayed effect from day 21, adverse -1 C/+8 RH) and `retrofit_comparison` returns baseline/early/late means and deltas. Truth lives in `Truth`, separate from analysis rows.
* `src/core/tests/test_sensor_scenarios.py` proves exact deltas, delay, insufficiency and truth separation. Docs: research plan R3 section and `src/core/README.md` already label every magnitude an exercise value.
* AC1 (improvement, no change, adverse; plus delayed) and AC2 (exercise labels) are met in code and docs.
* AC3: #111 (sensor analysis, open) and #133 (evaluator view, open) have no code consuming the scenarios. `src/core/tests/test_sensor_privacy.py` is the only other mention. #180 is closed.

## Gap and decision

* No consumer-ready accessor exists: consumers must reach into `Case`/`Truth`. Add a small `retrofit_exercise_scenarios()` API returning measure date, analysis-only rows and a labelled expected direction/size record, plus tests that drive it through `retrofit_comparison`.
* This does not prove AC3: #111/#133 tests do not yet use it. PR must use `Refs #193`.
* Scope boundaries: no mvp/ or prototype/ code, no real data, no thresholds beyond labelled exercise values.

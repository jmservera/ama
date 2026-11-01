# Issue 193 research: scenario consumers (2026-11-01)

* Disposition: executed. Planning Readiness: Ready.
* PR 635 (merged) exposed `retrofit_exercise_scenarios` with exercise labels; PR 631 (merged) added a classifier contract test; PR 699 (open) is the damp family only.
* Criteria 1 and 2 are delivered. Criterion 3 (used by #133 and #111 tests) is unmet: no `src/` test uses `retrofit_exercise_scenarios`; neither #111 nor #133 code exists (open issues).
* Remaining slice: tests driven by the labelled scenario view covering the #133 evaluator view (descriptive, no blame or savings promise) and #111 properties (reproducible, INSUFFICIENT never lowers priority).
* Limit: helpers are test oracles with exercise values; production consumers remain unimplemented.

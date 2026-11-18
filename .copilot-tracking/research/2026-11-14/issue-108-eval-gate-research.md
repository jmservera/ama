# Issue #108 research: regression gate and single-lever comparison

* Task: issue-108-eval-gate. Research disposition: executed. Planning Readiness: Ready.
* Evidence: `src/agents/src/zava_forward/agents/candidate_comparison.py` already counted critical misses, unsupported claims, overrides, reopened cases and dropped accepted proposals, and returned outcome `failure`, but exposed no boolean `passed`, no named blocking reasons and no per-lever deltas.
* Single lever was enforced (`changes` has exactly one of model, routing, caching, prompt) with no explicit composite path.
* Existing tests: `src/agents/tests/test_candidate_comparison.py` (19 pass).
* Gap: criteria 5 and 6 lacked a fail-closed boolean and a composite flag.

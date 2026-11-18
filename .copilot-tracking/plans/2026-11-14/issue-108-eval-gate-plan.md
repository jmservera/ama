# Plan: issue #108 criteria 5 and 6

1. Add `passed` and `blocking_reasons` to each candidate verdict (fail closed on delta > 0). Done.
2. Accept multi-lever `changes` only when `composite` is true; record `levers`, `composite`, `lever_deltas`. Done.
3. Add `src/api/tests/test_eval_candidate_regression_gate.py`; register in mypy overrides. Done.
4. Validate with the fast formula. Done.
Critique: one pass, no conflicting findings; scope kept to the comparison module.

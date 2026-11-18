# Changes: Issue #108 E501 correction

## Change

* `src/agents/src/zava_forward/agents/candidate_comparison.py`: rewrapped the `compare_candidates` docstring paragraph so no line exceeds 100 characters (ruff E501, 101 > 100). Text unchanged.

## Validation (focused tier, `TMPDIR=/dev/shm/zf-tmp`)

* `python3 -m ruff check src/agents src/api`: all checks passed.
* `python3 -m ruff format --check --line-length 100` on `candidate_comparison.py` and `test_eval_candidate_regression_gate.py`: 2 files already formatted.
* `src/api`: `python3 -m unittest tests.test_eval_candidate_regression_gate -q`: 7 tests OK.

## Notes

* Docstring-only change; no behaviour, dependency, workflow or gate change. Not pushed.

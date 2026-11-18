# Changes: issue #108

* `src/agents/src/zava_forward/agents/candidate_comparison.py`: verdict `passed`/`blocking_reasons`; `_lever_valid` with explicit `composite`; `levers`, `composite`, `lever_deltas` per candidate.
* `src/api/tests/test_eval_candidate_regression_gate.py`: new tests (4 metrics, no-regression pass, cost does not offset, routing/caching one lever, composite, invalid levers).
* `src/api/pyproject.toml`: mypy override for the new test module.
* Validation: fast formula 64 tests OK, ruff and mypy clean; agents `test_candidate_comparison` 19 OK.
* Not run: full unittest discover, hosted CI, full local gate. Candidate observations are synthetic.

# Issue 167 changes

* Plan: [plan](../../plans/2026-11-01/issue-167-generator-coverage-baseline-plan.md)
* Added `check_register_labels` and `--register` to `src/core/.../synthetic/coverage.py`.
* Added `RegisterLabelTests` (3 tests) to `src/core/tests/test_generator_coverage.py`.
* Updated `src/core/README.md`, the retrofit-synthetic-data README and `docs/reference/log.md`.
* Validation (venv, pip): 12 coverage tests OK, ruff check, ruff format --check, mypy clean.
* Local run on the SN-01 register: 60,000/60,000 labelled (counts only).
* No divergences from the plan.

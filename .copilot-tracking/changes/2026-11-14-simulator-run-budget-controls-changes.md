# Changes: simulator run budget controls (#189)

Date: 2026-11-14.

* Added `src/core/src/zava_forward/core/synthetic/run_governance.py`.
* Added `src/core/tests/test_simulator_run_budget_controls.py`.
* Validation (focused tier): new tests and `test_run_plan` pass; mypy, ruff check and ruff format clean in `src/core` with /tmp caches. Full gate, hosted CI not run.
* Divergence: none. Not yet wired into the publisher; library contract only.

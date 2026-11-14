# Plan: simulator run budget controls (#189)

Date: 2026-11-14. Research: ../research/2026-11-14-simulator-run-budget-controls-research.md

* [x] Add `RunGovernance` validating non-empty `run_owner`, `time_limit_seconds` in 1..3600 (unbounded rejected) and `budget_alert_gbp` positive and below `budget_cap_gbp`.
* [x] Add `RunMeter`: one deterministic `budget_alert` event at projected or accumulated cost >= alert; `budget_halt` before cap breach; `time_limit_halt` at deadline.
* [x] Add `src/core/tests/test_simulator_run_budget_controls.py`.
* [x] Validate: unittest, mypy and ruff with /tmp caches in `src/core`.

Critique (executed once): compatible; keep USD run_plan untouched. Follow-up: wire `RunMeter` into the publisher path.

---
title: Issue 189 changes
ms.date: 2026-11-01
task_id: issue-189
---

## Added

* `src/core/src/zava_forward/core/synthetic/run_plan.py`: `RunPlan`, `Estimate`, `record`, `RunController`, CLI.
* `src/core/tests/test_run_plan.py`: 16 tests.

## Modified

* `src/core/README.md`: "Cost estimate and run controls (#189)" section.

## Validation (focused tier, venv with pip)

* `unittest tests.test_run_plan tests.test_sensor_stream`: 26 tests OK.
* `ruff check`, `ruff format --check`, `mypy` in `src/core`: clean.
* No heavy local gate; CI is the evidence.

## Review amendments (PR 637 Copilot threads)

* Quota check now counts the whole run (units per day x days) against the B1 daily allowance; multi-day regression added.
* `estimate` refuses runs above the `RunBudget` 100,000-message limit (`RUN_MESSAGE_LIMIT`), so the plan-to-budget handoff is valid; the 60,000-home example is now refused and the README example uses 30,000 homes.
* `RunController.start` compares the complete recorded body (plan, estimate, alert amount) with the current expected body; non-object JSON returns `ESTIMATE_NOT_RECORDED`.

## Divergences

None from the plan.

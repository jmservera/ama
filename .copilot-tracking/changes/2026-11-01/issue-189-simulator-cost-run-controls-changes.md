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

## Review amendments, second round (PR 637 Copilot threads)

* `RunPlan.daily_used_units` is recorded in the plan, subtracted from quota headroom and passed to the `RunBudget`.
* `RunPlan.replay_speed` (default and maximum 1000) is recorded, passed to the `Pacer`, and the replay span (days x 86,400 s / speed) must fit `max_seconds`.
* Cost is based on provisioned time (whole days of `max_seconds`), not the simulated replay span.
* `Pacer.set_max_per_second` reschedules the pending admission; `admit_send` rechecks the moved target; `scale_down` uses it. Regression added.

## Review amendments, third round (PR 637 Copilot thread)

* The time-limit check now sums send spacing (messages / rate), replay spacing (days x 86,400 s / speed) and the publisher's 0.5 s cleanup reserve, matching the publisher's sequential waits and sends. Regression added for the 100-home, speed 1000, 1/s, 300 s plan.

## Correction cycle, PR 707 Copilot threads

* `run_controlled` raises `RUN_HOME_LIMIT` when distinct frame homes exceed `plan.homes`, before `controller.start` and any client.
* `run` accepts `active_homes`; homes are ranked by first appearance and frames of homes beyond the current limit are skipped, so `scale_down` stops removed homes publishing.
* Tests added: home-limit rejection with no client; two-home scale-down stops the removed home.
* Validation: ruff check/format clean; test_iot_stream 32 OK; mypy shows no errors in touched files (13 pre-existing errors elsewhere from missing optional stubs); full api discover has environment-related failures also present on baseline.

## Correction cycle 2026-11-01 (PR 707 review threads)

Research/plan/change/review note: two Copilot threads on iot_stream.py were valid. Active-home eligibility is now rechecked after admit_send and before send_message, skipping removed frames without sent counts or sent truth events. Skipped frames no longer advance the replay clock. Regression: scale down during connection (test_iot_stream). Validation: ruff check and format clean; mypy clean on touched files; tests.test_iot_stream 33 OK. Wider api suite and mypy show environment failures that are identical on the base commit.

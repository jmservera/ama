---
title: Issue 111 parent adoption research
ms.date: 2026-11-10
task_id: 111-parent-adoption-1855
---

## Objective

Adopt the declared parent `feat/demo-sensor-review-109-1110` into child `feat/demo-sensor-drafts-111-1110` with an ordinary `--no-ff` merge, completing integration of the already selected inherited correction. No second logic correction.

## Evidence

* Child head `325cb5c0c3efcd666145fe234c8fded1b50db89d`, tree `59963a5b065c258b8f38f9a0e13d45d017c50bc5`, clean, on `feat/demo-sensor-drafts-111-1110`.
* After `git fetch`, `origin/main` and the declared parent are both `06374dfcac47cf6bcce9e7b91f573e8565ab45e8`; the parent is an ancestor of main (zero unique commits). The child keeps the parent as its target; it is not retargeted to main.
* Merge base `0d262beee2dfa6feca27680aa1d596111154c8d9`; the parent has 19 commits not in the child, 497 changed paths (mostly `.copilot-tracking` records) versus the merge base.
* Child source files changed since the base: `quality_sensors_browser_check.py`, `server.py`, `ops.js`, `test_sensor_review_draft_api.py`, `src/core/pyproject.toml`, `projection.py`, `sensor_review_draft.py`, `test_sensor_review_draft.py`. The parent did not change `pyproject.toml`, `sensor_review_draft.py` or `test_sensor_review_draft.py` since the base.
* `git merge-tree --write-tree HEAD <parent>` predicts a clean merge (no conflict markers, tree `f85f0d51697a933102ef3b32b1aa45c047877140`). Server, projection, ops.js and browser-check overlap, if any, merges mechanically.
* Independent approvals (same reviewer 1b06482a): inherited repair approve with 0 findings; supplemental 22-case actual MSSQL (0 skips, exit 0) approve with 0 findings. Unforced `ConflictError` and `CommittedReloadError` branches are nonblocking coverage gaps, not passes. The scoped `disallow_untyped_calls` exemption remains disclosed; it is not unchanged strict mypy.

## Validation inputs (existing selectors)

* Core draft: `python -m unittest tests.test_sensor_review_draft`; analysis `test_sensor_analysis*`; API `tests.test_sensor_review_draft_api`; the sensor browser check only if the merge touches the sensor screen served path and its existing recipe applies.
* Configured Core mypy plus Core ruff check and format.
* Actual MSSQL `MssqlDraftCases` (22 before) through a non-queued `flock -n` admission with an own disposable container.

## Planning readiness

Ready. Disposition: Research executed (read-only).

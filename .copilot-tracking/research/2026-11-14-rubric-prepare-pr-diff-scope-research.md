# Research: rubric prepare PR diff scope (Refs #198)

Date: 2026-11-14. Disposition: executed. Planning Readiness: Ready.

## Finding

* `compute_state` in `.github/rubric/scripts/prepare.py` derives `changed_artifacts` from fingerprint differences against `scores/latest.json` on the base ref.
* When `latest.json` lags the base ref, artifacts merged after the baseline differ on every PR, even when the PR's `base_ref...HEAD` diff touches none of their files. `should_score` becomes true and the full LLM scorer runs (about 90 AI credits) with empty `changed_files` for that artifact.
* Non-PR events (push, workflow_dispatch) must keep the full comparison so main catches up.

## Scope

Only `prepare.py` and `test_prepare.py`. Workflows, `artifacts.json` and `scores/*` are untouched.

## Pre-existing validation state

17 tests in `test_gate.py`, `test_safe_output_runtime.py` and one in `test_prepare.py` (`test_given_pr_deleting_scored_file_when_gated_then_drop_counts`) fail before the change; `unittest discover` finds no pytest-style tests; ruff reports RUF100 on two existing noqa lines.

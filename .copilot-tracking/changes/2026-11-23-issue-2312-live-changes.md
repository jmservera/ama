---
title: Issue 2312 live changes (2026-11-23)
ms.date: 2026-11-23
---

## Changes

* Added `src/agents/src/zava_forward/agents/eval_harness.py`: `validate_manifest` (schema subset plus `check_freeze`), `run_eval` (per-threshold and per-critical-error pass or fail, deterministic, offline) and `verify_recorded` (invalidates on any version or digest change).
* Added `src/agents/evals/eval-manifest.schema.json`, `synthetic-eval-manifest.json`, `synthetic-eval-predictions.json`, registered in `src/agents/evals/registry.json` (required by `test_eval_registry`).
* Added `src/agents/tests/test_eval_harness.py` (8 tests) and a README section.
* No new dependency (a small schema validator replaced `jsonschema`, which is not a project dependency).
* No Azure resource created or changed; nothing to delete. No live model call.
* Tier: FOCUSED per the owner brief; `rpi-checks.py --all` not run. This is a src change, so the coordinator's full gate remains outstanding and is not claimed.

## Validation

* `unittest tests.test_eval_harness tests.test_heldout_freeze tests.test_eval_registry`: pass.
* `mypy` (src/agents): no issues in 69 files. `ruff check` and `ruff format --check`: clean.
* Full `src/agents` suite: 556 run, 13 failures, all in `test_paired_report_command`; the same 13 fail on the untouched base (verified with `git stash`), so they are pre-existing and unrelated.

## Per-criterion table

| # | Criterion | Result |
| --- | --- | --- |
| 1 | Manifest schema and synthetic example checked in and validated by a test | Proven: `test_checked_in_example_matches_schema_and_is_frozen`, `test_schema_rejects_malformed_manifest` |
| 2 | Runner reports pass or fail per threshold and critical error, deterministic offline | Proven: `test_report_is_per_threshold_and_critical_error_and_deterministic`, `test_critical_error_and_accuracy_failures_are_reported`, `test_undeclared_critical_error_and_unknown_case_fail_the_run`, `test_unfrozen_manifest_is_refused` |
| 3 | Changing any frozen version invalidates the recorded result (test) | Proven for all five versions and the split: `test_changing_any_frozen_version_invalidates_the_recorded_result`, `test_changing_the_held_out_split_invalidates_the_recorded_result` |
| 4 | No live model call or approved threshold claimed; approvals stay under #108 | Proven by construction and statement: no network code, every result carries the note, synthetic approver named "not an approval". Approval itself remains unproven and owner-gated under #108 |

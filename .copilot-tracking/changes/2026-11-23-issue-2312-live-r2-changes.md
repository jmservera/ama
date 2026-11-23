---
title: Issue 2312 live r2 changes (2026-11-23)
ms.date: 2026-11-23
---

## Changes

* `src/agents/src/zava_forward/agents/eval_harness.py`: missing or malformed predictions (non-object, non-string `answer`, non-list `critical_errors`) are now sorted input errors that fail the run (a string `critical_errors` was iterated per character before); a critical error counts once per case; new `main()` CLI (`python -m zava_forward.agents.eval_harness MANIFEST PREDICTIONS [--recorded RESULT]`, exit 0, 1 or 2).
* `src/agents/tests/test_eval_harness.py`: 3 new regression tests (missing and malformed predictions, duplicate error counted once, CLI exit codes and deterministic output).
* `src/agents/README.md`: CLI and strict-input paragraph.
* No Azure resource created or changed; nothing to delete; no live model call.

## Validation

* `unittest tests.test_eval_harness tests.test_heldout_freeze tests.test_eval_registry`: 32 tests pass.
* `mypy` (src/agents): no issues in 69 files; `ruff check` and `ruff format --check`: clean.
* Tier: FULL applies because src changed; `rpi-checks.py --all` not run per the brief, so the full gate is the coordinator's and is not claimed. Hosted CI, human review and approvals are outstanding.

## Per-criterion table

| # | Criterion | Result |
| --- | --- | --- |
| 1 | Manifest schema and synthetic example checked in and validated by a test | Proven: `test_checked_in_example_matches_schema_and_is_frozen`, `test_schema_rejects_malformed_manifest` (re-run, pass) |
| 2 | Runner reports pass or fail per threshold and critical error, deterministic offline | Proven, now also via CLI and strict inputs: `test_report_is_per_threshold_and_critical_error_and_deterministic`, `test_cli_exit_codes_and_deterministic_output`, `test_missing_and_malformed_predictions_are_input_errors` |
| 3 | Changing any frozen version invalidates the recorded result (test) | Proven: `test_changing_any_frozen_version_invalidates_the_recorded_result`, held-out split test, and the CLI `--recorded` path |
| 4 | No live model call or approved threshold claimed; approvals stay under #108 | Unproven as an approval, by design: the code makes no network call and every result carries the note; approval stays owner-gated under #108 and is not needed for the demo |

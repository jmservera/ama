<!-- markdownlint-disable-file -->
# Review: Issue #107 SQL restart and independent-connection proof

* Review execution: `executed` once, post-implementation. Outcome: `conformant with qualifications`.
* Plan: [plan](../../plans/2026-11-14/107-sql-restart-allowance-0106-plan.md); changes: [changes](../../changes/2026-11-14/107-sql-restart-allowance-0106-changes.md); critique: [critique](../../critiques/2026-11-14/107-sql-restart-allowance-0106-critique.md)
* Tier: Focused. System `python3`, pip tools only, no `uv`; `PYTHONPATH` set to this worktree because editable installs point at `/home/azureuser/source/ama`. Not a full gate receipt.

## Validation actually run

* `src/api`: `ruff check`, `ruff format --check`, `mypy` (240 files) clean.
* `src/core`: `ruff check`, `ruff format --check`, `mypy` (300 files) clean.
* Tests: `test_assistant_restart_non_replenishment` 11 OK (run twice), `test_assistant_release` and `test_ai_consumption_api` OK (116 tests in the combined run, 7 MSSQL skips), `test_rai_release` 9 OK, `test_scenario_manifest` (core) 8 OK.

## Assessment

* Suspension and revocation on one connection block claim, dispatch (paused worker), completion and fresh-store restarts with zero provider calls and unchanged controlled records.
* Consumed calls and tokens persist; larger env cannot raise the stored ceiling; three concurrent connections spend a one-call allowance once; a revoke plus new record does not refund consumption.
* Prompt, policy, permission, scope and serving-version mismatches deny dispatch, revoke the record, survive restart and quarantine late completions.

## Qualifications and routing

* Follow-up 1 (blocking for full criterion 8): a changed `ZF_ASSIST_AUTHORITY` creates a fresh allowance pool (probe executed a call after a one-call pool was spent). Needs a decision to bind the pool to the release record or a named authority register.
* Follow-up 2: MSSQL variants not executed (SQLite only, local proxy, not actual SQL acceptance).
* No #107 criterion is ticked; independent exact-head review, human approval and hosted CI remain required.

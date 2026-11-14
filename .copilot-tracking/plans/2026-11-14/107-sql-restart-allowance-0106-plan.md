<!-- markdownlint-disable-file -->
# Plan: Issue #107 SQL restart and independent-connection proof

* Research: [107-sql-restart-allowance-0106-research.md](../../research/2026-11-14/107-sql-restart-allowance-0106-research.md)
* Details: [107-sql-restart-allowance-0106-details.md](../../details/2026-11-14/107-sql-restart-allowance-0106-details.md)
* Critique: [107-sql-restart-allowance-0106-critique.md](../../critiques/2026-11-14/107-sql-restart-allowance-0106-critique.md)
* Validation tier: Focused (system `python3`, pip only; worktree `PYTHONPATH`). Not a full gate receipt.

## Phases

* [x] P1: Add `src/api/tests/test_assistant_restart_non_replenishment.py` using file-backed SQLite with a fresh `SqlStore` and `Assistants` per worker or restart.
* [x] P2: Cover suspension and revocation across connections and restarts, finite call and token allowance non-replenishment, and prompt, policy, permission, scope and serving-version mismatch.
* [x] P3: Register the module in the existing typed-test mypy override; keep production code untouched unless a failing-first persistence gap appears (none found).
* [x] P4: Focused validation, critique disposition, review, commit with `Refs #107`; no push.

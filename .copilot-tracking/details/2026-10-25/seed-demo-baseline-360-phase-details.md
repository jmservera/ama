# Phase details: seed the demo database (issue 360)

Date: 2026-10-25. Prospective, written with the plan and before any edit.

## Phase 1: store operation and CLI
* `src/core/src/zava_forward/core/sqlstore.py`: add `merge_seed` beside `_seed` (about 60 lines); no change to `_seed`, `save` or schema.
* `src/core/src/zava_forward/core/seed_merge.py`: argparse CLI, env-built store (`MssqlStore` when `ZF_STORE=mssql`, else `SqlStore` at `ZF_DATA`), JSON counts output only.
* Seed SHA-256 computed over the file bytes and stored in the audit detail.

## Phase 2: tests
* `src/core/tests/test_seed_merge.py` (SQLite, items 1-6 and 8 of the plan).
* `src/api/tests/test_mssqlstore.py`: a `MssqlSeedMerge` class (item 7), local-server guard before any connection, same fixture pattern as `MssqlLedgerMigration`.

## Phase 3: docs
* `src/core/README.md` Azure SQL store section: the merge command, its insert-only effects and the dry-run default. `infra/README.md`: one pointer for the demo seeding runbook.

## Phase 4: rehearsal and review
* Generate the seed externally; rehearse on a throwaway SQL Server container (own container, distinct port, removed after).
* Independent code review; commit; full gate with a new external output; push PR.

## Rollback
Code: revert the PR. Live data: the transaction is all-or-nothing; after commit no automatic undo (inserts only), so the dry run report and `--expect-added` check gate the apply.

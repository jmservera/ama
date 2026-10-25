<!-- markdownlint-disable-file -->
---
title: Ledger-Safe Migration Review
description: Independent post-implementation review and routing
ms.date: 2026-10-24
---

## Review Metadata

Task ID: ledger-safe-migration-360
Plan: .copilot-tracking/plans/2026-10-24/ledger-safe-migration-360-plan.md
Changes: .copilot-tracking/changes/2026-10-24/ledger-safe-migration-360-changes.md
Reviewer: independent code-review agent, one execution, read-only, did not run tests.
Outcome: PASS with three test-quality findings (1 Medium, 2 Low).

## Verified by the reviewer

* All previous column-adding ALTER sites route through the new hook; no stale references remain.
* Ordinary SQL Server and SQLite statements are equivalent to HEAD, including named chat_memory defaults.
* LEDGER_TYPES covers every text CASE_COLS column and matches the fresh-create DDL; an unmapped TEXT column is refused.
* No identifier injection; the transaction and lock use matches `_migrate`.
* The new tests fail without the fix and assert CHECK, defaults, rollback and append-only audit.

## Findings and dispositions (applied after the review, not re-reviewed)

* F1 Medium: new test classes sat after the `__main__` guard; moved above it.
* F2 Low: the ledger-history assertion compared ledger table counts and could not detect anything; replaced with `sys.database_ledger_transactions` counts (increase after migration, stable on rerun).
* F3 Low: ordinary-database test compared one column name; now compares full column facts. It documents that the ordinary path keeps the pre-existing legacy `TEXT` type for decision/fstatus, a pre-existing behaviour deliberately not changed here.

## Residual risk

* Azure SQL ledger behaviour is inferred from SQL Server 2022, not proven; the fixed image must be started against the live database through the approved route.
* The live column gap was never read. On a ledger database the migrated columns report nullable in metadata, enforced by CHECK.
* The post-review test edits were validated by running the tests, lint and type checks, not by a second review.

## Addendum: external PR 450 review and correction cycle 1 (2026-10-24)

The original review above is unchanged. A later fresh external review of PR 450 raised two valid test findings; the coordinator held the merge.

* External 1 (Medium): the destructive `MssqlLedgerMigration` fixture accepted any `ZF_SQL_SERVER`. Corrected with the established local-server guard before cleanup or connection, plus a regression proving refusal.
* External 2 (Medium, thread discussion_r4368820916): no populated chat-memory rollback and retry test. Corrected with a seeded-row test that fails after the first real backfill, and was shown to fail when the transaction is removed.
* Disposition: test-only; the source fix is unchanged. The correction has not had a separate independent review other than the external review that raised it and the coordinator's assessment of the follow-up.

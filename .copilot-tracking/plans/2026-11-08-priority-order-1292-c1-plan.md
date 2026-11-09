---
title: Issue 1292 C1 correction plan
description: Plan to correct the independent review findings with a cross-process zero-ordinal fence, audit-recovered legacy order, per-batch ambiguity records, linear backfill and a loopback guard for SQL tests
ms.date: 2026-11-08
---

Task `1292-priority-order-reload`, correction C1. Original plan, critique and the 2026-11-08 gate-tier amendment are preserved unchanged. Details: `.copilot-tracking/details/2026-11-08-priority-order-1292-c1-details.md`. Research: `.copilot-tracking/research/2026-11-08-priority-order-1292-c1-research.md`.

## Phases

1. Commit this research, plan and details before any source or test edit.
2. Add failing tests first (red on unchanged source), then correct `sqlstore.py` (the SQL Server module needs no change unless a hook is required) and the test guards.
3. Run light SQLite and in-memory red/green, lint and type checks with unique retained logs.
4. Write the C1 changes record and one original review, then commit.

## Findings to tests

* F1: `test_old_writer_insert_after_startup_is_repaired_before_a_later_new_write`, `test_zero_ordinal_read_fails_closed_when_repair_is_blocked`.
* F2: `test_audited_same_second_creations_keep_order_after_edit_of_the_older` (actual `ai_priority` A then B, edit A, legacy rewrite, reopen), `test_ambiguous_group_is_recorded_when_audit_evidence_is_absent`, `test_broken_audit_chain_is_not_trusted` (SQLite only, needs to drop an audit trigger).
* F3: `test_rollback_batch_is_recorded_without_erasing_earlier_metadata`.
* F4: `test_large_legacy_backfill_is_linear_and_survives_concurrent_openers` (SQLite only).
* F5: `test_task_owned_sql_fixtures_refuse_non_loopback_before_any_connection` and the same guard in `MssqlResidentControls.setUp`.

## Gates

* Light only in this session: unittest red/green, ruff, mypy, `git diff --check`.
* PENDING and not started: native SQL Server red/green (new class and the two original selectors), ledger-enabled migration, FULL local gate with external receipt, independent exact-head review, hosted CI. These need separate coordinator admission to the shared heavy resource.
* Decisions that stay human: how a named data owner resolves recorded ambiguity for a live database, and the rolling-deployment release boundary.

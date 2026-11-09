---
title: Issue 1292 priority recommendation creation order plan
description: Plan for an immutable creation ordinal on SQL recommendations with ordered reload, legacy backfill and focused SQLite, in-memory and SQL Server regression
ms.date: 2026-11-08
---

## Scope and tier

Task `1292-priority-order-reload`, branch `fix/priority-reload-1292`, PR target `main`, base `6354b13f7abf1441a815e92f2b01dc184ce0b0ac`. Research: `.copilot-tracking/research/2026-11-08-priority-order-1292-research.md` (executed, Ready). Details: `.copilot-tracking/details/2026-11-08-priority-order-1292-details.md`.

Tier FOCUSED (default for the gate). This is a small executable data-ordering fix with a schema addition; the complete local gate is not claimed and not required by this task. Local frozen candidate only: no push, PR, issue or board write, merge or deployment. Heavy checks (SQL Server, Docker, browser, image build) are not started without coordinator admission to `/tmp/ama-rpi-heavy.lock`; the SQL Server regression is PENDING.

## Objectives (issue acceptance criteria)

1. Deterministic newest-created ordering across cold and incremental SQL reload, equal to in-memory, respecting requesting user and `ai_task` exclusion.
2. Same-second and same-transaction batches, edits of older proposals, multiple users; no reliance on mutable `seq` or second-resolution `created`; truthful legacy transition.
3. Focused regression failing on old behaviour, passing after; SQLite and in-memory parity; actual SQL Server with zero skips when admitted (PENDING).
4. No change to review, approval, consent or ranking policy.
5. RPI research, plan, changes and review evidence on this branch.

## Phase 1. Evidence and plan commit (this commit, no product or test change)

* [x] 1.1 Research record, plan, details, issue metadata artifact and state record written and committed before any code or test change.
* [x] 1.2 One independent critique of the final plan; compatible findings applied directly (recorded in the critique file), then commit.

## Phase 2. Red regression

* [ ] 2.1 Add `src/core/tests/test_priority_order.py` with shared cases for in-memory, SQLite and opt-in SQL Server (`ZF_RESIDENT_MSSQL=1`): batch ties, edit of oldest, incremental reload, multiple users plus `ai_task`, legacy migration, tie-break parity.
* [ ] 2.2 Run it against the unchanged source and keep the exact failing output; the SQLite edit, incremental and legacy cases must fail for the right reason (not a harness error).

## Phase 3. Fix

* [ ] 3.1 `sqlstore.py`: add `created_ord` to the `recommendations` DDL, a `_migrate_recommendations` step (column add, backfill for `created_ord = 0` rows, `rec_order_legacy` meta on first backfill), `ix_recs_created_ord`, ordinal assignment in the insert, and `ORDER BY created_ord, id` in `_sync`.
* [ ] 3.2 `mssqlstore.py`: DDL column and index, column-existence hook; reuse `_add_column_default`.
* [ ] 3.3 Document the ordering contract, legacy transition and rolling-deployment limit in `src/core/README.md`.

## Phase 4. Validation (light, local, no heavy resource)

* [ ] 4.1 New file green on SQLite and in-memory; confirm red-to-green evidence.
* [ ] 4.2 Original issue selectors on SQLite: `MssqlResidentControls` methods are skip-guarded; run their `SqlResidentDecisions` parents (`test_challenge_source_exact_dependency_manifest_and_original_reviews`, `test_failed_priority_accept_edit_remove_disposition_and_audit`) on SQLite and the JSON parent. Native SQL Server counterparts are PENDING.
* [ ] 4.3 Related light suites: `test_resident_decisions`, `test_sqlstore*`/`test_seed_merge`/`test_taskqueues` in `src/core`, plus ruff and mypy on touched files.
* [ ] 4.4 PENDING (coordinator admission): task-owned SQL Server run of the new class (zero skips, record individual counts) and of the two original `MssqlResidentControls` selectors, including a before/after comparison on the unchanged source.

## Phase 5. Records and review

* [ ] 5.1 Changes record with exact commands, exits, counts and identities; review record from one independent post-implementation Review; commit with the Co-authored-by trailer using the repository-local privacy-safe email.

## Boundaries and risks

* Human approval, resident consent and ranking policy are untouched; no recommendation becomes a decision.
* Synthetic data only; no private dataset, live Azure or model call. No cleanup of existing ignored, foreign or runtime inputs; scratch is `/tmp/ama-1292-scratch` only.
* Legacy ambiguity is documented, not resolved. Residual: old-writer rolling deployment, unreproduced native SQL Server before/after.
* Stop rule: if the red regression cannot fail for the stated reason, or the fix requires a ranking or approval change, stop and report instead of widening scope.

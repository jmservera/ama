---
title: Issue 86 formal-complaints review corrections, changes
description: Changes record for the first correction cycle of three Medium findings (Refs #86)
ms.date: 2026-11-07
---

Scope: Refs #86 only. Plan: `.copilot-tracking/plans/2026-11-07/issue-86-formal-complaints-review-corrections-plan.md`. Planning commit 8e3ab67, amendment ece2972 (both before any source edit).

## Changes

* `complaints_route.py`: new `Unconfirmed` status, `NotSent` exception, `NOT_SENT_REASON`, `UNCONFIRMED_REASON`.
* `resident_decisions.py`: reservation id generated in `_forward`, lookup and stale guard under `store.lock`, send outside the lock, per-store in-flight registry cleaned in `finally`; exceptions and malformed replies give `Unconfirmed`; only `NotSent` gives `Failed` with `not_sent`; legacy `Failed` without `not_sent` is unresolved and needs `retry_unresolved`; outcome bound to `reservation_id`; independent review uses `_require_named_reviewer` (code/oid continuity, no manager bypass, unknown fails closed). Complaint route keeps manager rights.
* `tests/test_resident_decisions.py`: new tests for each finding plus legacy reopen; old failed-then-acknowledged test deliberately changed to expect `Unconfirmed` and `retry_unresolved`.
* `src/core/README.md`: formal-route section updated.

## Evidence

* RED (before source): `-k forward` 51 tests, 14 failures, 2 errors; `/mnt/ama-gates/restart-1107-86-corrections/red-full.txt`.
* GREEN: `tests.test_resident_decisions` 308 tests OK, 110 skipped (MSSQL and Azure variants skipped without service; not a full pass). Baseline was 281 tests, 101 skipped.
* Strict mypy: 267 files, no issues. Ruff check and format check pass. Modules import from this worktree.
* One ruff F821/E501 set found and fixed during the work.

## Limits

No real receiver, receiver dedupe, cross-process duplicate-send proof, or operational criterion proof. FULL, independent exact-head, hosted and human gates pending. Residual risk is an engineering limitation for inactive synthetic development, not owner or legal approval.

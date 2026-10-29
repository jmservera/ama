---
title: Issue 96 PR 510 fix cycle 1 changes
description: Report-local freshness reuse implementation evidence
ms.date: 2026-10-29
---

## Metadata

Task ID and slug: `issue-96-pr-510-fix-cycle-1`.
Plan: `.copilot-tracking/plans/2026-10-29/issue-96-pr-510-fix-cycle-1-plan.md`.
Details: `.copilot-tracking/details/2026-10-29/issue-96-pr-510-fix-cycle-1-phase-details.md`.

## Execution Status

Complete; full-plan scope P01, P01-T01 and P01-T02 complete. Source boundary is the core
form-review module, existing external test module and related core README.
Critique Complete / Pass, no findings. No implementation blocker.

## Completed Work

### P01-T01: Report-local freshness reuse

Added a local `dict[tuple[str, int, str, str], bool]` in `_report`, keyed by
source ID/version/hash/kind. Only cache misses invoke `_current`; false results
are cached too. Existing schema short circuit and visibility checks remain.
No cache crosses report boundaries, including diagnose requests.

Added two test methods and one shared-source helper in
`src/core/tests/test_form_review.py`. Both JSON and SQLite exercise view and
diagnose with two fields sharing one real staged source. A later report reads
again and marks both fields stale on changed bytes with unchanged metadata.
Separate copied-draft subtests distinguish all four key dimensions.

Regression-first evidence: the shared-source test on original production code
ran one method with four failing subtests (Store/SqlStore x view/diagnose);
each observed `2 != 1` reads. Exit 1, expected.
After the fix, both new methods pass (2 tests, no skips, exit 0).
Command from `src/core`, with required PYTHONPATH:
`/tmp/mv/bin/python -m unittest
test_form_review.FormReview.test_shared_source_read_once_per_report_and_rechecked_on_later_reports
test_form_review.FormReview.test_report_freshness_separates_exact_source_identity -q`.

### P01-T02: Documentation and validation

The core guide now documents exact-key, report-only reuse and later rechecking.
No new dependency, tests inside packages or changes outside approved targets.

## Implementation-Time Plan and Detail Updates

No amendment or significant divergence. Ordinary local formatting correction:
the first format check requested collapsing one test fixture list. Applied
Ruff format to that file and reran all three static checks successfully.
No scope, acceptance, dependency or user-decision changes. Plan markers and
phase-details completion reconciled with the actual results.

## Validation Record

All commands from `src/core`, using `/tmp/mv/bin/python`.

| Check | Scope | Status | Evidence |
| --- | --- | --- | --- |
| `-m ruff check .` | Core source/tests | Passed | All checks passed, exit 0 |
| `-m ruff format --check .` | Core source/tests | Passed after formatting correction | 112 files already formatted, exit 0 |
| `-m mypy` | Core configured source/tests | Passed | No issues in 165 source files, exit 0 |
| Relevant unittests | Seven modules below | Passed | 201 tests, 54 existing optional SQL skips, exit 0 |
| `git diff --check` | Changed tracked files | Passed | No whitespace errors |

Unittest command with `PYTHONPATH=src:tests:../agents/src:../agents/tests`:
`/tmp/mv/bin/python -m unittest test_form_review test_form_staging
test_finance_match_controls test_finance_signoffs test_grant_lifecycle_controls
test_change_provenance test_document_rescan -q`.
147 tests executed, no failures. Synthetic fault-injection tests intentionally
log lost-acknowledgement/rollback/rescan errors; unittest result is OK.

The first static chain stopped on one formatting difference (exit 1), so mypy
did not run in that initial chain. After Ruff formatting the existing test
file, the entire static chain passed. No failure is represented as a pass.
The original-code red regression and fixed-code green regression are above.

## Pre-Review Reconciliation

Plan P01/P01-T01/P01-T02 checked; phase details, changes, handoff, test counts
and known boundaries reconciled. No active implementation work remains.
Ready for the single independent Review; no acceptance claimed before it.

## Blockers

None for this bounded fix. Human finance and publication gates are unchanged.

## Remaining Work

One independent Review. Commit locally after evidence reconciliation;
never push. Full `rpi-checks.py --all` publication gate and exact-head receipt
verification are not run or claimed: this is a local-only, unpublished cycle.
Any future push/publication requires the complete gate and independent
exact-head assessment under repository policy.

## Follow-Up Items

Original finance acceptance and historical review outcomes are not superseded.

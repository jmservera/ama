---
title: Resident SQL fixture authorization window changes
description: Scoped correction and validation evidence for PR 479
ms.date: 2026-10-27
---

## Metadata

Task ID: pr-479-resident-sql-fixture-window. Scope: full correction plan,
with publication P03 after original Review. P01 complete, P02 checks complete,
original Review Complete / Conformant with no findings, P03 pending.
Plan/details/critique share the resident-sql-fixture-window slug and date.

## P01: Approved correction

Independent critique Complete / Revise retained; PC-001 and PC-002 applied
directly before implementation. Added SQL_AUTHORIZATION_END at November 1 UTC
and used it only for allowed_case inserts; application authority stays
December-bound. The image check already shares this fixture and needs no edit.
Moved the browser dependency to main()/TYPE_CHECKING so regression discovery
and shared SQL setup do not require Playwright. Added two API tests observing
both actual fixture insert parameter sets, cleanup and import isolation.

Red evidence: both new tests failed against original code (later application
cap inserted; Playwright eagerly imported). Green evidence: both passed with
the correction. Missing pinned tools restored with pip in the external session
venv after missing-tool results. No manifests changed, uv, secret read, private
dataset access or cloud operation. Ruff/mypy initially exposed test import
ownership/sorting issues; direct core imports and repository sort fixed them.

## P02: Validation and Review

| Check | Result | External evidence |
| --- | --- | --- |
| New regression red | 2 expected failures against original fixture | fixture-red.log |
| API resident unit discovery | 108 tests, OK, 7 existing opt-in skips | fixture-api-resident-tests.log |
| Core showcase unit discovery | 77 tests, OK, 19 existing real-SQL opt-in skips | fixture-core-tests.log |
| Changed Python Ruff/format/mypy | Passed, 2 files | terminal output; repeated at final candidate |
| Real browser check | Passed, 55 assertions | fixture-browser-image.log |
| Exact Dockerfile resident image check | Passed, 22 assertions | fixture-browser-image.log |

External root:
`/home/azureuser/.copilot/session-state/0a4240b1-3166-41ab-9abc-f42623b6a0cf/files/`.
Commands ran from src/api or src/core with explicit absolute API/core/agents
source roots plus core/tests and agents/tests. Browser/image execution was
foreground through `flock -w 0 -E 75 /tmp/ama-rpi-heavy.lock`; no wait or bypass.
SQL readiness used SELECT 1, exact task label and random loopback port. Its
container was removed in finally; image checker removed its own image and
containers. Only fake local fixture credentials were generated/used.

Current src/README.md small-issue policy and owner scoped-only direction apply:
this is not a full-matrix receipt, SQL schema change or live acceptance.
Original parent Review and live blockers are unchanged. Plan/detail status,
test ownership (two additions, zero removals), validation and remaining P02/P03
work are reconciled. The one original independent Review executed Complete /
Conformant with no RV findings:
`.copilot-tracking/reviews/logs/2026-10-27/resident-sql-fixture-window-review.md`.
Its assessed source fingerprints bind the working diff, not a future commit.
P01/P02 are complete; no in-task Review repair or second Review.

## P03: Publication

Pending final candidate synchronization, fresh scoped evidence, independent
exact-head assessment, normal push and review-thread response/resolution.

This committed record is the pre-publication snapshot, not a receipt. Fresh
candidate checks and exact-head assessment remain external to avoid
self-reference. Actual publication/thread disposition will be posted to PR
479; no completion is inferred from this prospective section.

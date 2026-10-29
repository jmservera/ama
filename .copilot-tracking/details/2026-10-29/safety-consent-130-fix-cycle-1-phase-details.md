---
title: Issue 130 PR 509 fix cycle 1 phase details
description: Task-level implementation and validation boundaries
ms.date: 2026-10-29
---

Task ID: issue-130-pr-509-fix-cycle-1. Plan:
.copilot-tracking/plans/2026-10-29/safety-consent-130-fix-cycle-1-plan.md.
Research C1-C7 is adequate. No unresolved decision or dependency.

Execution reconciliation: P01 and P02 complete. Three shared regression
methods failed on original source and now pass on JSON and SQLite. Two existing
ID fixtures use returned IDs; no deletion/retention metadata changes, no removed
tests. Complete core static checks and selected core/API modules pass, with
explicit skips and environment details in changes. P03-T01 Review is Complete /
Conformant with justified divergence, no substantive findings. P03-T02 local
commit remains, and is not represented as already complete.

<!-- P01 -->
## P01: Regression and implementation

<!-- P01-T01 -->
### P01-T01: Add bounded regressions

In the existing shared JSON/SQLite resident test class add up to three tests.
For tenure, accept both measures, snapshot exact heuristic output with a
constructed competitor that would reveal the +20 ordering regression, record
tenure, reopen and compare status/output while checking both holds.
For identity, start with legacy NOM-1, retain a prepared correction with
expected_version=1, expire/delete/reopen/create and assert a distinct ID,
explicit refusal with unchanged durable state/audit, and a valid new
correction. Cover another deletion and failed creation after deletion.
Third test starts from an already-deleted legacy tombstone with no nomination
history; a NOM-1/version-1 correction must not match the new UUID record.
Update existing core/API correction tests to use returned IDs. Record baseline
failures before runtime edits.

<!-- P01-T02 -->
### P01-T02: Correct shared logic and document

Move all non-tenure resident gate checks unchanged to a private decision-only
helper. resident_gate retains its tenure fast-path then delegates; status uses
the helper directly. No new flags or field-stripping copies.
After PC-001, allocate NOM- plus uuid.uuid4().hex. Existing uuid4 prior art
includes forms and assistant records. No counter, tombstone or deletion
modification; no change to legacy ID lookup/version validation.
Deletion is not wrapped by resident_action's _operation. This design adds no
deletion-persistence dependency, so pre-existing deletion recovery is not
misrepresented as tested or rewritten. Intake UUID assignment remains in the
existing operation; test failure rollback after deletion.
Update the existing intake section of src/core/README.md only.

<!-- P02 -->
## P02: Validation and evidence

<!-- P02-T01 -->
### P02-T01: Required validation

From src/core with /tmp/mv, run complete Ruff check, format check and mypy.
Run focused new tests first, then the plan's relevant unittest modules with
PYTHONPATH=src:tests:../agents/src:../agents/tests. Use constructed temporary
datasets only. No configured database or Azure. Report counts and skip reasons
without treating opt-in MSSQL or Azure skips as acceptance.
Do not install packages unless the requested command reports missing tools or
dependencies. Preserve existing formatter/type-check exclusions.
The requested tools exist. Their installed editable projects point to another
worktree, so use the explicit source/test PYTHONPATH and verify module origins;
do not mutate the shared environment. The API module additionally needs this
worktree's api/src, api/tests and api project root for its tests package import.

## Plan Amendment

The one critique exposed previously deleted legacy histories with no recoverable
counter. Replace the initial counter proposal with random full UUID identities,
which the user's non-reused-ID requirement permits. No personal metadata is
retained and existing deletion privacy tests need no change. PC-001 accepted;
PC-002/003 resolved by removing the counter dependency; PC-004 rejected as an
unsupported worker restriction conflicting with explicit caller tools.

<!-- P02-T02 -->
### P02-T02: Reconcile handoff

Record command exits and baseline/fixed results in changes. Reconcile plan
markers, implementation details, accepted critique dispositions and scope.
Review cannot claim full local publication, real SQL, browser, human or hosted
acceptance. No latest.json write.

<!-- P03 -->
## P03: Review and local commit

<!-- P03-T01 -->
### P03-T01: One independent Review

Fresh worker, exact supplied artifacts and candidate diff. Read-only except
the review output. No nested agents. Record execution separately from outcome.
Route findings to later work, never repeat Review or source edits in this task.

<!-- P03-T02 -->
### P03-T02: Local completion

Resolve gh api user and configure repository-local noreply email before commit.
Stage only owned source/docs/tests and current dated artifacts. Use Conventional
Commit, Refs #130 and PR #509, required Copilot trailer. Do not push. Check the
committed worktree/status and preserve publication/approval limits explicitly.

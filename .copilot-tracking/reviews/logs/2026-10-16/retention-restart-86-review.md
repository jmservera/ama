---
title: Resident retention restart review
ms.date: 2026-10-16
---

## Metadata

* Task ID: issue-86-retention-restart
* Task slug: retention-restart-86
* Execution: Complete
* Outcome: Conformant
* Boundary: completed P01 local code/tests/documentation and validation.
  Commit/push/PR are a subsequent publication handoff, not prior evidence.

## Compared artifacts

* .copilot-tracking/research/2026-10-16/retention-restart-86-research.md
* .copilot-tracking/plans/2026-10-16/retention-restart-86-plan.md
* .copilot-tracking/details/2026-10-16/retention-restart-86-phase-details.md
* .copilot-tracking/reviews/plans/2026-10-16/retention-restart-86-plan-critique.md
* .copilot-tracking/changes/2026-10-16/retention-restart-86-changes.md

## State

P01 and all three tasks are checked, with validation and documentation evidence.
One critique completed; compatible corrections applied, unsupported environment
restriction rejected. No product divergence or unresolved decision.

## Opening Review State

Goal: assess the owner-directed restart against completed P01 and its locked
test ownership. Evidence is available: current source/test/documentation diff,
all five phase artifacts, local suite/static-check results and original-module
mutation output. Acceptance basis is the latest issue #86 decision and plan.
Read-only assessment; only this review record is changed during Review.
No blockers. Publication has not yet occurred and is not claimed.

## Requirement and evidence comparison

| Requirement | Evidence and conclusion |
| --- | --- |
| First contact after deletion, not original contact/deletion/decision | first_contact slices the retained general-contact prefix and deletion clears cached origin; separate route tests assert exact new dates after an Unknown interval |
| Returning resident and no revived consent | Both contact routes independently recover; old scope/answer removed and fresh scope/Accepted answer establishes current readiness; persisted stores reopen |
| Same-day boundary | General-contact test retains an old contact at the exact same timestamp as the appended contact; count boundary, not date guessing, distinguishes them |
| Period remains fixed and can expire again | Later safe contact/withdrawal retains the new due date; repeat loop checks expiry holds release before deletion, then second deletion/renewal and eventual expiry |
| Legacy date-only records | Old cached marker, old/same-day contacts and invalid/future dates ignored; later-day contact establishes exact due date and new scoped readiness |
| Tombstone privacy | Exact whitelist equality: deletion date and integer contacts_before_deletion; personal canaries absent, scoped fields/cached marker removed while separately purposed contact remains |
| Existing controls preserved | Manager/legal-hold checks unchanged; existing leap-anniversary/disclosure/permissions/audit tests pass for JSON/SQLite |
| Required layout and portability | Only existing core package implementation and external tests changed; no SQL, schema or dependency changes |
| Documentation | Superseded known limit removed, restart/legacy behavior described, routing updated and dated log appended |
| Required failure proof | Entire baseline module executes before Store imports; original alias/MRO verified, all ten new inherited cases fail assertion checks, no setup/import errors; changed module passes afterwards |

## Critique and implementation update assessment

PC-001/002 corrections are implemented and validated with independent positive
routes, reopen checks, fresh acceptance and a coherent full-original-module
mutation. PC-003 asserted an environment restriction absent from caller evidence;
rejecting it did not weaken a user requirement.

The test correction from direct-answer refusal to release refusal preserves the
existing distinction: supplied resident answers may be recorded, but expired
evidence cannot release work. No unrelated production behavior was changed.
Moving publication to a post-Review handoff resolves a process dependency cycle
without changing user delivery requirements. Plan, details, changes and markers
are reconciled; all local P01 work is complete.

## Validation

* Passed: full core suite 482 tests with one opt-in Azure skip; 481 executed.
* Passed: targeted resident suite 40 tests with same one skip; 39 executed.
* Passed: resident API suite, three tests.
* Passed: core Ruff check, formatter-selected files and configured mypy.
* Passed: diff whitespace check.
* Mutation accepted: ten assertion failures against original code, zero errors,
  followed by passing changed-code resident suite; no on-disk code mutation.
* Skipped: isolated Azure SQL test, requires explicit synthetic cloud opt-in.
  No Docker, live SQL Server, deployment, private data or human acceptance run.
* Existing static-check exemptions, sensor fixture ResourceWarnings and explicit
  API fixture law-store-unavailable logs are not concealed or claimed resolved.

## Findings and routing

No substantive in-scope defects or unresolved implementation decisions found.
Severity summary: zero Critical, High, Medium or Low findings.

The plan's existing issue #86 operational/human acceptance and historical erasure
follow-up remains outside this rule correction. Route to the owner as distinct
future work; this review does not claim acceptance of those wider criteria.
No new discovery or implementation loop is authorized by this review.

## Outcome and handoff

Execution Complete. Outcome Conformant for P01 local implementation, tests and
documentation. No blockers. Parent may publish using normal commit/push and
references-only PR, leaving hosted checks and merge decision to the owner.

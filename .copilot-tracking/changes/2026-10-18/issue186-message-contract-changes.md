<!-- markdownlint-disable-file -->
# RPI Changes: Issue186 shared message contract and volume

## Metadata

* Task ID: issue186
* Task slug: issue186-message-contract
* Plan: .copilot-tracking/plans/2026-10-18/issue186-message-contract-plan.md
* Details: .copilot-tracking/details/2026-10-18/issue186-message-contract-phase-details.md
* Implementation date: 2026-10-18

## Execution Status

* Status: Complete
* Declared scope: full plan P01/P02
* Completed markers: P01, P01-T01, P01-T02, P02, P02-T01
* Remaining markers: none
* First execution boundary: offline public example measurement, no source edits

## Execution Summary

Research and one independent critique complete. Original critique verdict Revise
retained; PC-001/002 directly disposed by pinning SQLite and owned TMPDIR.
Six existing canonical docs and issue186 tracking are the complete write boundary.
No implementation worker, source/test change, private stock or cloud action.

## Completed Work

### P01-T01: Measured current shared-contract example

Unchanged observations()[0] from existing sensor_consumer_fixture, sorted ASCII
default-separator JSON encoded UTF-8, no newline:366 bytes.
SHA256:efccea5eb698a3310aca7409837ad9b5ad3673b949ddb3c2395da21a8b01dc6c.
Verified exact imported field set,13 strings, imported version, current
preflight/_shape and equality with existing _reference digest. No new API.
N1:3 rows/day,1/28800 mean/s,1098 sample-scaled bytes/day.
N60000:180000 rows/day,25/12 mean/s,65880000 sample-scaled bytes/day.
Raw actual output: issue186-message-contract-measurement.log in this directory.
This is one constructed fixture sample, not a bound/distribution/live packet.

### P01-T02: Existing documentation integrated

Six planned canonical docs updated in one coherent batch: existing sensor
synthesis carries exact source-derived field table, paired-record accounting,
sample/reproduction and explicit incompatibility; core/API READMEs, addendum
and KB index route to it. KB log only appended. Material dates2026-10-18.
No runtime/test/new schema/tooling files. Existing history and accepted ADR intact.

## Implementation-Time Plan and Detail Updates

No scope divergence. Apply safe offline execution pins from critique dispositions.
System python import failed during Research; src installations in isolated task
venv are permitted after that observed missing-dependency failure.

### P02-T01: Temporary-root refinement after observed generator refusal

Initial full80-test invocation forced SQLite and repository-local TMPDIR as
planned. It returned exit1/errors16: all failures came from generator output
guards that require outputs outside the repository. Core/API tests did not
report failures; preserve full failed output in issue186-message-contract-tests.log.
Read stock_fabric._destination: repository outputs are deliberately refused.
Direct local execution refinement: keep ZF_SENSOR_MSSQL=0, use a specifically
created issue-owned session files/issue186-temp directory outside the repo,
verify effective TMPDIR and clean it exactly. No source/test edits, guard
bypass, private stock read or additional critique. PC-002 isolation intent
retained; current plan/details/disposition updated before rerun.

## Validation Record

| Check | Scope | Status | Evidence |
| --- | --- | --- | --- |
| Current source binding | System python | Failed prerequisite | ModuleNotFoundError zava_forward; no application check executed there |
| Measurement | P01-T01 | Passed | Explicit source/shape/digest and exact Fraction arithmetic assertions; measurement log |
| Existing semantic suites initial | P02-T01 | Failed | 80 tests,16 errors from repository-output guard; full failed log retained |
| Existing semantic suites final | P02-T01 | Passed | 80 tests in18.040s, no failures/skips; SQLite-only, session-owned TMPDIR; final log |
| Docs and diff | P02-T01 | Passed | Exact field table/fixture bytes/reproduction, added links/anchors, append-only log, six-doc-only diff; doc-check log |
| Static/image/UI/SQL Server/Azure | Unchanged runtime | Not applicable | Docs-only; no code/test changes, no new runtime behavior assertion |

## Pre-Review Reconciliation

Plan P01/P02 and all three task markers complete, details/current handoff
reconciled. Exact documentation reproduction and focused semantic suites pass.
Original failed test attempt retained, followed by execution-only temp-root
refinement and passing unchanged suite. No runtime/test changes.
Cleanup complete: exact empty repository/session scratch directories removed.
Final diff check and runtime/source parity pass; origin/main still pinned base.
Review ready; one original Review only.

## Blockers

None. Missing local distributions resolved by installing src/core, src/agents
and src/api in task-owned session venv; no manifest changes.

## Remaining Work

No active implementation tasks. One original Review and authorized draft
publication remain lifecycle actions. Coordinator owns independent final-head
assessment, issue criteria and merge. Correction count0.

## Follow-Up Items

Canonical list in plan: separate downstream187/188 stock/live compatibility
decision and independent live/privacy/AI/Azure/human acceptance gates.

## Return-to-Caller State

Implementation Complete, full plan, automatic parent, no source changes.
One critique Complete/Revise with direct dispositions and documented TMPDIR
refinement; no repeat. Ready for one original Review.

## Original Review and Publication Handoff

The one original independent Review executed Complete, outcome Conformant for
bounded documentation, with zero substantive RV findings. Review artifact:
.copilot-tracking/reviews/logs/2026-10-18/issue186-message-contract-review.md.
Original adverse critique/test output remains intact. Correction count0.
No source/document-content changes after Review; lifecycle state/log/inventory
only. Draft publication and full-PR exact-head coordinator assessment remain
separate from this Review. All issue criteria remain unchanged.

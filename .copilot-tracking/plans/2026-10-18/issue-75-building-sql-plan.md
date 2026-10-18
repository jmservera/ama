<!-- markdownlint-disable-file -->
---
title: Issue 75 building SQL conformance plan
description: Implementation-ready candidate for independent critique
ms.date: 2026-10-18
---

## Task Metadata

Task ID: 75. Slug: issue-75-building-sql. Date: 2026-10-18.
Planning status: Ready after one independent critique and direct dispositions.
Mode: parent-authorized automatic bounded task.
Phase details: `.copilot-tracking/details/2026-10-18/issue-75-building-sql-phase-details.md`.
Critique: `.copilot-tracking/reviews/plans/2026-10-18/issue-75-building-sql-plan-critique.md`.

## Executive Summary

Add focused constructed building tests to the existing opt-in SQL Server module
and replay its existing loopback HTTP building suite through the same factory.
Do not change runtime. Delete the constructed seed before reopen, verify
independent connection visibility and stale rejection, exercise scoped work
instructions and independent approvals, and retain role projections.

### What You May Not Know

Building runtime already exists from PR310. This closes a real-engine evidence
gap only, not operational FR-002 acceptance. PR398's governance source stays
untouched. A skipped SQL suite cannot establish acceptance.

### Unresolved Decisions or Blockers

No planning blocker. System Python lacks installed source packages; restore
dependencies in an isolated task virtualenv after the observed import failure.
No production fix authorized without attributable failing real-engine evidence.

## User Decisions and Requirements

* Run ordered Research, Plan/details/one independent critique/disposition,
  Implement and one original Review; preserve adverse originals.
* Preserve exact base 9d625a09e34491ecf9fd27ffc7d59e67c2373b29 and supplied branch.
* Use constructed fixtures and task-owned disposable SQL only; no private
  sources, configured dataset, sensor plumbing, AI, Azure or mvp implementation.
* Reuse fixture and wipe/factory; no new service, generic abstraction, editor,
  allocation policy or hold-release authority.
* Local-first evidence then commit all issue artifacts/tests together, push
  and draft PR to main using Refs #75 only; leave issue/review checkboxes open.
* Stop after one original Review and publication, no corrections or second Review.

## Goals

Supply auditable actual SQL-engine evidence for the six bounded acceptance
points without widening runtime or operational authority.

## Scope and Non-Goals

Canonical executable target: `src/api/tests/test_mssqlstore.py` only.
Direct documentation target: building section of `src/api/README.md`.
Tracking artifacts are evidence, not application inputs. No generated source.
No production, workflow, manifest, Dockerfile or shared fixture changes planned.
Image/nonroot rerun not applicable if those inputs remain unchanged.

## Functional Requirements

* Shared systems/dependencies/holds/works/cost record and per-home allocation
  persist without a seed.
* Independent sessions see committed holds; stale conflicting shared document
  update raises ConflictError and cannot erase the winning hold/version.
* Matching home/package advance/issue/reissue refuses; explicitly other package
  and sibling can still proceed with existing approval/appointment fixtures.
* Clear building cannot supply resident, funding, technical or QA approval.
* Existing Finance/non-Finance/Contractor HTTP projections retain separation.

## Non-Functional Requirements

* Existing opt-in guard unchanged; skips reported as Not run.
* Unique task-owned local SQL2022 container plus database, loopback ephemeral
  port, no mounted datasets, exact container-ID cleanup even on failure.
* Independent connections are distinct raw driver sessions; no fake SQL.
* Preserve existing semantics; no broad catches or hidden passing fallback.

## Acceptance Criteria

* A1: Full record equality and each home's allocation/evidence retained after
  close, seed deletion and reopen; allocation absent from shared projection.
* A2: Two independent connections observe committed hold; controlled stale
  write conflicts, third independent reopen confirms exact winning record.
* A3: Matching progression/issue/reissue refuses without case/order mutation;
  other package and sibling remain usable using explicit supplied fixtures.
* A4: Three independently missing home prerequisites refuse progression and
  retain state; unaccepted QA cannot borrow accepted/closed sibling's handover.
* A5: Existing loopback HTTP role suite executes on MSSQL, not just SQLite.
* A6: Actual throwaway SQL run executes without skips for selected building
  classes; all owned resources cleaned. No operational acceptance inferred.

## Test Ownership and Coverage Lock

Owner: this issue's existing MSSQL test module. Exact removals: none.
Maximum additions: two test classes, five focused semantic test methods plus
three inherited HTTP regressions; bounded fixture/lifecycle helpers as needed.
Close existing wipe's short-lived connection in finally (no table changes).
Canonical fixture: `src/core/tests/building_fixture.py`, unchanged.
Generated targets: none. No test service and no import of sensor consumers.
Semantic coverage: A1-A4 real-engine tests. Regression coverage: A5 HTTP replay
and existing core/API building/procurement/role/portable SQL suites.

## Sources

Research: `.copilot-tracking/research/2026-10-18/issue-75-building-sql-research.md`,
especially C2-C6. Exact source remains frozen base plus this test-only patch.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Add focused conformance evidence

Dependency: finalized critique disposition.

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Add MSSQL semantics and HTTP replay

Implement A1-A5 using existing fixture/wipe/factory, then document opt-in
commands and test-only limits. Details own test-level assertions.

<!-- rpi:phase id=P02 -->
### [x] P02: Execute local validation and reconcile evidence

Dependency: P01.

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Run focused regressions and actual owned SQL

Restore missing packages with pip in task virtualenv. Run core building,
quality/procurement; API building, procurement, role matrix and portable SQL
tests, disambiguating identically named core/API building modules by cwd.
Run new MSSQL classes on owned SQL, record image/version, exact commands,
counts, failures/skips and cleanup. Run migration regression and configured
API Ruff/format/mypy. Record application image check as redundant if unchanged.

<!-- rpi:phase id=P03 -->
### [x] P03: One original Review and publication

Dependency: P02 evidence reconciled.

<!-- rpi:task id=P03-T01 -->
#### [x] P03-T01: Review once, freeze evidence and publish draft

Activate rpi-review exactly once. Preserve original findings; no post-review
source correction without coordinator authorization. Commit tests/docs and all
issue artifacts using current gh identity noreply and required trailer, push
supplied branch and create draft PR main with Refs #75. Record frozen head/base,
inventory, actual SQL proof/cleanup and unmet human/live/operational gates.

## Dependencies

Dependency290 closed. Parent74 is hierarchy only. PR398 merged at frozen base.
Docker responsive; SQL image already local. Source Python prerequisites absent,
as observed in Research C7. Do not reuse another task's container or database.

## Critique Disposition

Original independent critique executed once, verdict Revise; preserved unchanged.
All findings are compatible direct planner corrections; no user decision needed.

| Finding | Owner / disposition | Resolving plan evidence |
| --- | --- | --- |
| PC-001 High | Planner, accepted/directly resolved | P01-T01 now requires valid bindings and exact refusal causes, not merely exceptions |
| PC-002 Medium | Planner, accepted/directly resolved | P01-T01 specifies target/other-package and sibling/same-package controls |
| PC-003 High | Planner, accepted/directly resolved | P02-T01 requires allowlisted env, local docs/scanner/auth and workspace scratch |
| PC-004 Medium | Planner, accepted/directly resolved | P01-T01 specifies immediate connection cleanup, partial HTTP lifecycle cleanup and wipe finally |

Final readiness: Ready. These are prospective implementation requirements;
execution evidence still belongs to Implement. No second critique.

## Follow-Up Items

* Operational register/update rights, allocation policy, human/accessibility
  acceptance and live application evidence belong to coordinator assessment,
  outside this bounded synthetic conformance task.

## Handoff

Changes record: `.copilot-tracking/changes/2026-10-18/issue-75-building-sql-changes.md`.
All execution markers complete. Source/evidence commit:
7eb509e9e382b48a940cbd555c1328a80a02a69f.
Draft PR410: https://github.com/jmservera/ama/pull/410.
Publication bookkeeping is evidence-only; no source changes after original Review.
Automatic session stopped on explicit caller direction. Original Review path:
`.copilot-tracking/reviews/logs/2026-10-18/issue-75-building-sql-review.md`.

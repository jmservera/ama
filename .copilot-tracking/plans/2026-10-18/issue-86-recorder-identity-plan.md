<!-- markdownlint-disable-file -->
---
title: Issue 86 recorder identity implementation plan
ms.date: 2026-10-18
---

## Task Metadata

Task ID: 86; slug: issue-86-recorder-identity.
Base: 6c1e376ff1241316272df22a5a3a6853aae9f87b.
Status: P01/P02/P03 complete, original Review Complete / Conformant, PR406 published;
ONE independent critique executed, Revise, PC-001
resolved directly below without altering the original.
Details: .copilot-tracking/details/2026-10-18/issue-86-recorder-identity-phase-details.md.

## Executive Summary

Capture immutable server-derived recorder identity on new measure decision
versions and bind independent reviews to that exact historical version/identity.
Compare email/code/oid consistently at opening and redress reassignment.
Fail closed only for review assignment whose historical independence cannot be
established. Keep legacy history unchanged and unrelated resident service usable.

### What You May Not Know

Today's owner of an old email is not historical evidence. Retention deliberately
preserves service requests after resident decisions are deleted, so each new
review must retain its own original identity binding. Actual SQL Server parity
is required even though the new fields live in existing JSON bodies.

### Unresolved Decisions or Blockers

None for implementation; original issue acceptance is outside this bounded fix.

## Sources

Research: .copilot-tracking/research/2026-10-18/issue-86-recorder-identity-research.md,
C1-C10 including eight actual failing-first probes. Repository/component guides,
issue #86 and the coordinator's explicit task scope govern delivery.

## User Decisions and Requirements

* Run all phases in order with one independent critique and one original Review.
* Historical recorder code/oid must defeat legitimate email-change bypasses at
  opening and reassignment; use server evidence, never supplied identity claims.
* Preserve existing history; no backfill from current staff lookup or client.
* Legacy insufficient identity is Unknown; fail closed narrowly on independent
  review assignment, not unrelated consent, complaint or service recording.
* Preserve privacy, consent isolation, hazards, ranking and outstanding remedies.
* Actual local MSSQL parity, focused API/core and configured quality checks before
  normal push/PR. No private inputs, Azure, inference, web or unrelated work.
* Commit all evidence, preserve original assessments unchanged, maximum two
  corrective source cycles, stop after publication for coordinator exact-head review.

## Goals

Remove recorder self-review across staff email changes without widening authority
or making any claim that independent human/formal complaints acceptance is met.

## Scope and Non-Goals

Primary resident module, directly dependent projection, existing core/API tests,
narrow component contracts and dated evidence only. No new service, schema
migration, MVP code, UI, role, retention or review-authority redesign.
Do not close #86 or authorize #130/#76; #122/#92 remain untouched.

## Functional Requirements

* New decision versions copy registered `_identity` evidence, not body fields.
  Use existing `_operation` replay/rollback for decision recording and retain
  its existing recorder-role restriction explicitly.
* Local same-person helper normalizes nonblank email/code/oid and is shared by
  current handler/reviewer and historical recorder/reviewer comparisons.
* Exact measure/version selection must resolve that version, not the latest.
  New requests retain `reviewed_identity`, measure/version and legacy email label.
  Reassignment uses only the request's bound historical snapshot. Unbound legacy
  requests remain Unknown: ordinal measure/version may be reused after retention
  deletion and is never enough to reconstruct the original binding.
* Missing/malformed/no shared stable historical code-or-oid is explicitly Unknown,
  never inferred from name or today's email owner. Unknown blocks redress review
  assignment; service-owner reassignment and other routes retain their controls.
* View-derived identity status may expose Known/Unknown to entitled resident
  roles without mutating legacy records; snapshots are removed for other roles.

## Non-Functional Requirements

Denied mutations leave case and successful audit unchanged, including restart.
Snapshot and binding survive JSON/SQLite/MSSQL reload. No new identity appears in
unauthorized detail/export/model inputs. Existing server actor checks are reused
and SQL replay revalidates the actor before committing a decision snapshot.

## Acceptance Criteria

* AC1: code-only and oid-only changed-email original recorder denied both paths.
* AC2: genuinely distinct reviewer opens and can replace another distinct reviewer.
* AC3: body or forged caller identity cannot override registered snapshots;
  current-registry race refuses without successful case/audit mutation.
* AC4: legacy email-only/missing/malformed historical identity is Unknown;
  refusal does not rewrite old history or block unrelated supplied consent/service.
* AC5: exact old version remains binding after newer decisions, registry changes,
  restart and resident payload removal/recreation; unbound legacy requests cannot
  adopt a recreated measure/version snapshot. Denied cases/audit stay unchanged.
* AC6: actual authenticated HTTP denials/positive controls match core; role
  projection/export canaries and existing measure/hazard/remedy regressions pass.
* AC7: actual task-owned loopback SQL Server exercises changed persisted contract;
  configured Ruff/format/mypy and coupled tests run before push.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Implement bounded identity contract

Dependencies: research ready and critique disposition resolved.

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Historical identity, review guard and projection

Use `_identity`, `_actor`, `_operation` and existing normalized comparison prior
art; preserve old records. Update directly related core/API contract prose.

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Regression coverage in existing suites

Depends on P01-T01. Semantic tests cover identity/legacy/exact version; regression
tests cover transaction, privacy and persistence. No test removals. Maximum eight
new core test methods and two API methods; prefer subtest matrices and inherited
JSON/SQLite/MSSQL coverage. Canonical tests are existing
src/core/tests/test_resident_decisions.py and src/api/tests/test_resident_api.py;
no generated code/tests. Research probe is retained unchanged as before/after
evidence, not a replacement suite.

<!-- rpi:phase id=P02 -->
### [x] P02: Validate and freeze candidate

Depends on P01.

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Local evidence and runtime parity

Run focused and directly coupled suites, configured quality commands, actual
local SQL Server parity with task-owned container promptly removed afterward.
Exercise actual local app through HTTP. Container/non-root check if packaged
behavior affected, or accurately record justified N/A. Record exact commands,
outputs, errors/skips and source hashes. No unexecuted check marked Pass.

<!-- rpi:phase id=P03 -->
### [x] P03: Original Review and publication

Depends on P02.

<!-- rpi:task id=P03-T01 -->
#### [x] P03-T01: One independent original Review, reconcile and publish

Commit candidate delivery/evidence, then one independent original Review against
the exact candidate. Preserve original bytes/hash. Findings route to coordinator
or separately receipted correction, maximum two cycles; never repeat original.
Reconcile plan/details/state, commit final evidence, privacy-safe authenticated
Git identity, normal push and PR main with Refs #86, no closure keywords.
If main moves, report it; no integration/rebase without explicit authorization.

## Dependencies

Existing editable component distributions and task-local synthetic fixtures;
available local SQL Server image and mssql-python. No issue dependencies.

## Critique Disposition

Executed once: original verdict Revise, one High PC-001. Planner-direct resolution:
unbound legacy requests always Unknown, no decision-pointer fallback. Include
actual deletion/recreation/restart collision test plus retained-bound positive
control on JSON/SQLite/MSSQL and HTTP within existing test caps. No new policy
decision, no second critique. Original assessment preserved unchanged at:
.copilot-tracking/reviews/plans/2026-10-18/issue-86-recorder-identity-plan-critique.md.

## Follow-Up Items

* Formal complaints integration, historical erasure, contact identity and human
  accessibility/without-detriment acceptance remain coordinator-owned #86 work.

## Handoff

Next: STOP for coordinator full independent exact published-head review of PR406.
All plan tasks complete, critique disposition resolved,
original independent Review executed once Complete / Conformant against
671ec03ac0e2e99478e9ae2c71537030d0541413. No implementation defects; RV-001 Low
keeps broader acceptance open. No source correction cycles or repeated Review.
Normal push/PR main verified; final publication receipt commit is evidence-only
and defines final HEAD, recorded exactly in PR body and CLI handoff. No source
approval or owner merge decision is inferred. Session is stopped as requested.
Actual validation: 232 coupled core, 26 coupled API, 44 actual local SQL Server,
eight adverse probes now deny, configured core/API quality pass, packaged UID10001
read-only/capability-free HTTP pass. Existing skips remain explicit in changes.
Changes: .copilot-tracking/changes/2026-10-18/issue-86-recorder-identity-changes.md.
Review: .copilot-tracking/reviews/logs/2026-10-18/issue-86-recorder-identity-review.md.

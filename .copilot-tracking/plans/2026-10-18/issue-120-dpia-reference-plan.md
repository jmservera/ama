---
title: Issue 120 DPIA reference implementation plan
description: Bounded time-capture reference-presence guard and verification
ms.date: 2026-10-18
---
<!-- markdownlint-disable-file -->

# RPI Plan: issue-120-dpia-reference

## Task Metadata

* Task ID: issue-120
* Task slug: issue-120-dpia-reference
* Planning status: Ready; sole critique complete, compatible correction applied
* Date: 2026-10-18
* Base: a86282c4badebc58eabbf9e441410d930a201ac2
* Details: .copilot-tracking/details/2026-10-18/issue-120-dpia-reference-phase-details.md
* Critique: .copilot-tracking/reviews/plans/2026-10-18/issue-120-dpia-reference-plan-critique.md

## Executive Summary

Enforce the already documented requirement that DPIA_APPROVED contain a
reference rather than a feature flag. One derived status predicate will deny
all existing admission paths, including matching historical controls, without
changing storage, HTTP routes, roles, notice policy or reference formats.
Existing short valid strings and trimming stay supported.

### What You May Not Know

Both real direct calls and authenticated existing HTTP returned success on the
exact base with ` yes `; the existing 16-test suite passed. Stored historic
controls must remain intact, not be migrated or deleted. This fix cannot verify
a DPIA's authenticity, obtain consultation, ratify the notice or complete issue 120.

### Unresolved Decisions or Blockers

No implementation decision is unresolved. Independent critique executed once;
original Revise retained, PC-001 disposition below.
Human governance and coordinator acceptance are separate unmet gates.

## User Decisions and Requirements

* Execute Research, Plan plus exactly one independent critique, Implement, then
  exactly one original Review; retain adverse originals; maximum two later corrections.
* Work only from supplied branch/base; commit all task evidence in the same PR.
* Production boundary is timecapture.py, existing test_timecapture.py and narrow API README.
* Reject missing/blank and trimmed case-insensitive yes/true/on/1 without writes;
  seeded invalid controls cannot bypass the rule.
* Preserve valid references, manager separation, notice acknowledgement/version,
  aggregate minimum groups, own entries, audit and shared persistence.
* No format invention, unrelated approval service, live approval or issue/board writes.
* Normal push and new main-target PR, Refs #120 only; stop for coordinator review.

## Goals

* Make status and write admission agree on bounded DPIA reference presence.
* Demonstrate the regression before changing production and prove retained behavior.
* Deliver reproducible, honest evidence without claiming legal or issue acceptance.

## Scope and Non-Goals

In scope: three permitted production/test/doc paths plus task-owned evidence.
No server, shared fixture, schema, web, consultation/notice validator changes.
No private env/data/support, Azure/IAM/Graph, model calls or live enabling.
No changes in #92 procurement or #122 continuity workstreams.

## Functional Requirements

* FR1: Derive DPIA validity from the existing stripped string: nonempty and not
  case-insensitive yes/true/on/1. Return false dpia_recorded and enabled plus
  plain DPIA-reference reason for configured-on invalid input.
* FR2: All four writers raise TimeCaptureOff before inserting rows. A fresh
  unused local fallback file and parent directory remain absent.
* FR3: Even matching seeded request/activation/ack history cannot enable capture;
  history stays byte-for-byte row-equivalent after denial and restart.
* FR4: A valid-to-flag switch disables immediately. Different valid reference
  needs fresh request and activation; existing matching/trim semantics remain.
* FR5: Keep storage, role, audit, notice and reporting paths unchanged.

## Non-Functional Requirements

* No SQL, schema, connection lifecycle or runtime boundary changes. Compare AST
  outside status and explicit DDL constants against exact base.
* Run full test_timecapture locally, not CI-first. Run configured API Ruff,
  format check and mypy; disclose existing legacy exclusions.
* Attempt existing source Docker image, non-root/read-only/cap-drop with loopback
  synthetic probe if practical. No browser or WCAG claim.
* Do not run destructive MSSQL fixtures against shared systems. If persistence
  stays unchanged, record original engine evidence as historical, not rerun.

## Acceptance Criteria

| ID | Measurable condition |
| --- | --- |
| AC1 | Missing/blank and each token/case/whitespace variant yield dpia_recorded=false, enabled=false, reference reason |
| AC2 | Request/activate/ack/record refused; all four tables unchanged; fresh local path absent |
| AC3 | SQL-seeded invalid matching controls and ack retained after restart and denied writes on fallback and shared SQLite |
| AC4 | Same instance valid-to-flag immediately disabled; different valid reference requires both renewed steps |
| AC5 | D1, padded DPIA-2026-007 and non-prefix references accepted; trimmed values stored; existing invariant suite green |
| AC6 | README rejects flags, explains presence only and preserves human approval boundary |

## Test Ownership and Evidence Lock

Canonical owner: src/api/tests/test_timecapture.py; removals: none.
Maximum additions: seven test methods, plus at most two small shared test helpers.
No new fixture files or test modules outside task evidence. Existing research
probe is task evidence, not a replacement suite. No generated production targets.
Semantic coverage: token matrix, no writes, retained invalid history, immediate
switch, renewal and valid trimming. Regression coverage: rerun existing full suite,
its actual HTTP role/audit tests and shared-store restart assertions.
Add one existing-handler HTTP regression in the same test file; no separate
auth/role suite needed unless a coupled defect requires it.
Preserve failing-first new-test output before production edit and preserve the
earlier direct/HTTP baseline failures. Record actual commands and exit codes.
Validation scratch precondition: create ignored `.venv/task-tmp` beneath this
worktree; set TMPDIR to its absolute path before every subsequent Python
test/probe process, record tempfile.gettempdir(), and clean task-owned scratch
after use. For Docker, bind this same task-owned path as writable `/scratch`
with TMPDIR=/scratch; do not change the Dockerfile or existing fixtures.

## Implementation Context Record

| Item | Path or state |
| --- | --- |
| Research | .copilot-tracking/research/2026-10-18/issue-120-dpia-reference-research.md, executed, Ready |
| Plan/details | This file and metadata path |
| Critique | Metadata path, sole run complete, original Revise; PC-001 addressed |
| Changes | .copilot-tracking/changes/2026-10-18/issue-120-dpia-reference-changes.md, implementation-owned |
| Review | .copilot-tracking/reviews/logs/2026-10-18/issue-120-dpia-reference-review.md, one original run |
| Continuation | Explicit automatic execution; stop after delivery, coordinator owns integration |

## Sources

* Research C1-C12, original failure log and contrarian log.
* src/api/pyproject.toml: existing component check configuration.
* src/api/Dockerfile: source image context, non-root runtime.
* Open issue 120: all live acceptance checkboxes remain unchecked.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Add failing-first bounded regressions

Dependency: finalized critique disposition.

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Exercise token rejection and retained history

Add direct invalid/valid/change tests and local/shared seeded historical cases.
Run selected new tests against unchanged production and retain their failures.
Details: P01-T01.

<!-- rpi:phase id=P02 -->
### [x] P02: Implement predicate and narrow documentation

Dependency: P01.

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Wire shared status admission

One local derived predicate; use for reason and dpia_recorded output.
Update module contract/README without implying authenticity. Details: P02-T01.

<!-- rpi:phase id=P03 -->
### [x] P03: Verify and reconcile handoff

Dependency: P02.

<!-- rpi:task id=P03-T01 -->
#### [x] P03-T01: Run focused checks and prove boundary

Run full time suite/probe/configured tooling, unchanged-boundary comparison,
and practical hardened image check. Reconcile changes, markers and validation
before the single original independent Review. Details: P03-T01.

## Dependencies

Research complete; source distributions now installed after actual missing
import failure. No live approvals needed for synthetic tests; no upstream code
dependency. Required human approvals remain outside implementation completion.

## Critique Disposition

| Finding | Disposition | Response |
| --- | --- | --- |
| PC-001, Medium | Applied compatible execution improvement | Added task-local TMPDIR precondition to plan/details; implementation will record resolution and cleanup. The critique's claim of an explicit caller no-/tmp prohibition is not present in the parent request; retain original unchanged rather than endorse that unsupported provenance. Local scratch remains a safe bounded choice. |

Critique execution: complete, exactly once. Original verdict: Revise.
Planning readiness: Ready after direct disposition; no second critique.

## Follow-Up Items

* Human DPIA/consultation/notice/admin ratification: issue owner, outside reference validation.
* Independent coordinator acceptance and integration: coordinator, after this delivery.

## Handoff

Implementation changes-record path: .copilot-tracking/changes/2026-10-18/issue-120-dpia-reference-changes.md.
Implementation complete: P01-P03 and all tasks checked with changes-record
evidence. Full suite 23 passed, probe 2 passed locally and again in hardened
installed image; configured checks and exact-base boundary proof passed.
Next: the single original independent Review; no implementation blocker.

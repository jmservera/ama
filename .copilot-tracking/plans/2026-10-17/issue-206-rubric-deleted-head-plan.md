---
title: Issue 206 rubric deleted-head implementation plan
description: Exact-head recording with explicit obsolete-run handling
ms.date: 2026-10-17
---

## Task Metadata

* Task ID: 206
* Task slug: issue-206-rubric-deleted-head
* Status: Implemented; ready for one post-implementation Review
* Details: .copilot-tracking/details/2026-10-17/issue-206-rubric-deleted-head-phase-details.md

## Executive Summary

The original defect remains: recording checks out a mutable PR branch before
checking its SHA. Check current PR state before immutable-SHA checkout, retain
moved-head failure behavior, and refuse a push unless the server advertises
exactly the scored head. Closed PRs are explicitly obsolete, not successful
rubric evaluations. API errors remain failures.

### What You May Not Know

Changing checkout to a SHA alone would silently remove the old moved-head
signal. An ordinary push can also recreate a branch deleted after the API
check. A workflow-owned pre-push hook can enforce the advertised old OID
without force pushing or enabling PR-controlled hooks.

PR closure and git ref updates are not one transaction; state is checked again
before record/publication, while the ref update itself has exact-head protection.
The existing baseline has 21 failures, 117 passes and 7 skips. Those failures
are not authorized work and must remain separately reported.

## Sources

* .copilot-tracking/research/2026-10-17/issue-206-rubric-deleted-head-research.md:
  C1-C5 and W1-W3, all research questions answered, Ready.
* Caller: preserve names, pins, semantics, permissions, safety and exclusions.

## User Decisions and Requirements

* Complete Research, Plan, Implement and Review in order with dated artifacts
  and explicit phase completion events in the persistent session log.
* Repair #206 only if current evidence requires it. Use existing local pytest
  and gh-aw tooling, no live scoring or inference credits.
* Cover closed/deleted, active unchanged, moved and API-error behavior.
* Never score/push main as fallback, recreate deleted refs, bypass gates, or
  publish success for a different scored SHA.
* Commit source and compiler-produced lock together; push the assigned branch
  and open Refs #206 PR; no merge/rewrite/closure; stop after publication.
* Do not touch #370/#176, Azure, private data, primary environment files or secrets.

## Goals

* Eliminate obsolete deleted-branch checkout failures without hiding real errors.
* Preserve exact-SHA score recording and fail-closed publication.

## Scope and Non-Goals

* In scope: rubric workflow source/compiled lock, existing rubric test runner,
  focused workflow regressions, rubric README and requested tracking artifacts.
* Out of scope: score values, deterministic gate logic, model, permissions,
  action pins, unrelated workflow fixtures, live scoring and deployment.

## Functional Requirements

* Explicit closed PR state skips recording and verdict side effects with notice.
* Open PR checkout always uses event SHA; moved heads block score recording.
* API failures propagate; they cannot become obsolete or passing.
* Recheck PR state before recording and before publishing. Push requires exact
  advertised scored SHA and a normal non-force update of an existing full ref.
* Keep main/manual/calibration behavior and all deterministic gates intact.

## Non-Functional Requirements

* No permission, action-version, check/job-name or scoring-semantic changes.
* Test real extracted workflow code, not a reimplemented decision approximation.
* Use local temporary repos/mocked API only; no agent execution or paid inference.

## Acceptance Criteria

| ID | Criterion | Required evidence |
| --- | --- | --- |
| AC1 | Historical failure and current-code status established | Research C1/W2/W3 |
| AC2 | Closed/deleted run exits before checkout, no verdict or ref recreation | Mocked API and extracted-step conditions |
| AC3 | Active unchanged head records/publishes at scored/bot SHA only | Extracted JS/shell plus temporary git remote |
| AC4 | Moved head cannot record or pass, including late deletion/move | API tests and pre-push hook race tests |
| AC5 | API errors fail, no success-shaped fallback | 404/403/500 mocked API regressions |
| AC6 | Existing safety invariants remain | Lock/source parity, permissions/pins/semantic comparison |
| AC7 | Compiler output and full local results reported honestly | gh-aw compile, targeted tests, baseline comparison |
| AC8 | Review and publication complete without issue closure | Review artifact, commit/PR/SHA evidence |

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Repair recording boundary

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Guard PR lifecycle and exact head

Add pre-checkout state inspection; immutable checkout; fresh pre-record state
inspection; exact advertised-OID pre-push hook; fail-closed/obsolete publication.
Dependencies: completed research and critique disposition.

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Focused executable regressions

Add tests under the existing rubric pytest directory, using its YAML/Node/git
patterns. Dependencies: P01-T01. Test canonical source and compiled behavior.

<!-- rpi:phase id=P02 -->
### [x] P02: Compile, document and reconcile

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Compile and validate

Run installed gh-aw v0.89.21; update rubric README; run focused and existing
rubric suites; compare failures with baseline. Dependencies: P01.

<!-- rpi:task id=P02-T02 -->
#### [x] P02-T02: Reconcile implementation evidence

Record exact results, amendments, acceptance audit and remaining limitations
before one post-implementation Review. Dependencies: P02-T01.

## Locked Test Ownership and Change Budget

* Canonical target: .github/workflows/rubric-score.md.
* Generated target: .github/workflows/rubric-score.lock.yml, compiler only.
* Test owner: .github/rubric/scripts/; reuse pytest, PyYAML, Node and temporary git.
* Exact removals: none.
* Maximum additions: one focused test module; no runtime dependency or framework.
* Semantic coverage: explicit PR state/API and exact event SHA.
* Regression coverage: lifecycle races, normal recording, error propagation,
  pinned actions/permissions, gate/verdict preservation.
* Validation: focused module, existing full rubric suite, compiler and git diff.

## Critique Disposition

Execution: Complete; verdict: Revise; exactly one critique. All findings are
compatible with caller direction and resolved in the details before implementation.

| Finding | Disposition | Resolving planning evidence |
| --- | --- | --- |
| PC-001 | Applied directly | Exact one-update hook contract and post-advertisement race tests |
| PC-002 | Applied directly | Lifecycle producer/consumer table; all outcomes participate in pass eligibility |
| PC-003 | Applied directly | Recognized state/full SHA validation at every API boundary |
| PC-004 | Applied directly | Publication expects NEW_SHA only after push, otherwise SCORED_SHA after legitimate no-commit |

Critique: .copilot-tracking/reviews/plans/2026-10-17/issue-206-rubric-deleted-head-plan-critique.md.
No divergent decision or second critique required.

## Follow-Up Items

* Existing rubric fixture failures: outside issue #206; maintain baseline evidence,
  do not fix unrelated score seeds or retired source-path assumptions.

## Handoff

All P01/P02 tasks complete with focused validation and baseline comparison.
One post-implementation Review is next. Implementation evidence:
.copilot-tracking/changes/2026-10-17/issue-206-rubric-deleted-head-changes.md.
No required human operational approval is inferred from this local repair.

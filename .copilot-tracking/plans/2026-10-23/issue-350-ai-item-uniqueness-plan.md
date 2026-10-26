---
title: Issue 350 AI item uniqueness correction plan
description: Bounded second correction checklist and validation contract
ms.date: 2026-10-23
---

## Task Metadata

* Task ID/slug: issue-350-ai-item-uniqueness.
* Date: 2026-10-23. Status: Ready; one critique executed and disposed.
* Details: .copilot-tracking/details/2026-10-23/issue-350-ai-item-uniqueness-phase-details.md.
* Critique: .copilot-tracking/reviews/plans/2026-10-23/issue-350-ai-item-uniqueness-plan-critique.md.

## Executive Summary

Reject repeated case IDs only after captured items satisfy existing shape
checks. Add genuine red-first duplicates and distinct-ID regression coverage;
preserve every other offline check. Complete one original RPI Review, commit
the correction/evidence, then run exactly one fixed-base gate and verify its
official receipt. Stop without publication.

### What You May Not Know

The complete gate does not discover this tools suite, so the focused test run
is separate. A component PASS is never actual AI/deployed/SQL acceptance.
Published PR #436 ancestry is divergent; the coordinator resolves it separately.
That blocks publication but not the authorized local correction and validation.

## User Decisions and Requirements

* Run Research, Plan, Implement, Review in order; complete research and this
  checklist before any source edits. Preserve every previous artifact.
* Correct only duplicate case IDs on top of a01b36f86e36092cbe4d90a1b9db87a95a34531d.
* Demonstrate duplicates fail red-first and distinct runtime-shaped IDs pass.
* No semantic membership/citation verification, arbitrary limits, checker
  networking, credentials, writes or activation.
* Preserve branch/PR #436; no push, rewrite, rebase, merge, new PR, PR-body edit
  or issue-criteria change. Issue #350 stays OPEN and criteria unticked.
* Resolve GitHub account and repository-local privacy-safe identity, commit
  with Conventional Commit and Copilot co-author trailer.
* Run one --all at committed head against
  140d8f494482c78e84d15f3d46b9223d3c487af0 with unique external output and
  --lock-timeout 86400; wait without duplicating/interfering with other gates.
  Verify receipt against that exact base and report SHA-256/head.

## Goals

Remove the reproduced uniqueness false positive without broader acceptance
changes; retain auditable red/green and original one-pass RPI evidence.

## Scope and Non-Goals

Only `tools/check-demo-feedback.py`, `tools/test_check_demo_feedback.py` and
this new task's dated tracking artifacts may change. Module documentation may
clarify unique IDs. No runtime, web, dependency, gate or old-artifact changes.
No independent coordinator review, hosted approval, cloud/paid action or live
acceptance is within the task.

## Functional Requirements

* FR1: All equal case-ID strings in otherwise valid captured items cause
  `ai_evidence=fail`, including adjacent and nonadjacent duplicates.
* FR2: Distinct runtime-shaped IDs retain component PASS. Compare raw strings
  without normalization, membership/source checks or count limits.
* FR3: Malformed IDs still fail through existing structural checks, not crashes;
  preserve other component and overall/acceptance behavior.

## Non-Functional Requirements

* NFR1: Reuse existing Verdict/problems and helpers; no new dependency or IO.
* NFR2: Installed namespace packages and external venv, `-B`/no-cache options;
  no PYTHONPATH source workaround or task-created ignored inputs at gate.
* NFR3: Exactly one final-candidate critique, exactly one original RPI Review,
  exactly one complete gate. No repeated review or post-gate evidence commit.

## Acceptance Criteria

* AC1: New duplicate regression fails before checker edits; distinct-ID positive
  stays green. Record command, test/failure counts and actual logs.
* AC2: Entire focused feedback suite passes after correction; existing 70 tests
  retained. Targeted Ruff and whitespace checks pass.
* AC3: Valid fixtures keep SQL durability blocked, spend/admin not-run, overall
  blocked and acceptance not-accepted; duplicates report component FAIL with
  explicit duplicate-ID diagnostic.
* AC4: Source diff remains uniqueness-only and prior RPI artifacts untouched.
* AC5: Reviewed correction/evidence committed with proper identity/trailer;
  official complete gate and verifier pass on exact committed head/base,
  receipt SHA-256 recorded externally; lineage remains an explicit blocker.

## Sources

Research: .copilot-tracking/research/2026-10-23/issue-350-ai-item-uniqueness-research.md,
C1-C5, Planning Readiness Ready. Existing code, prior evidence and package/gate
guide were read. No research gap or unsupported design dependency remains.

## Test Ownership and Locked Critique Boundary

Canonical tests: tools/test_check_demo_feedback.py, AiEvidence.
Removals: none. Generated targets: none. Maximum additions: two test methods.
One duplicate matrix covers identical, differing-payload and nonadjacent
repetition; one distinct-ID matrix uses runtime-shaped synthetic items and
preserves explicit offline boundaries. Existing runtime-validator positive
remains. Regression coverage only; no semantic/source acceptance is added.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Red-first bounded implementation

Dependency: completed research, plan/details and one disposed critique.

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Add uniqueness regressions and capture genuine red

Add at most two methods in AiEvidence. Run AiEvidence before checker changes;
duplicate method must fail, distinct and existing methods must pass.

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Add shape-guarded uniqueness and capture focused green

Use `elif` after valid-item predicate, set cardinality versus item count and
explicit existing-problems diagnostic. Update module description. Run full
focused suite, targeted Ruff and git diff --check; reconcile evidence.

<!-- rpi:phase id=P02 -->
### [ ] P02: Original Review and committed candidate

Dependency: P01 complete.

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Execute exactly one original RPI Review

Assess requirements, source diff, real red/green and critique dispositions.
Preserve outcome. In-scope blocking findings stop commit/gate; route later work
without another Review. Human/coordinator approval is not self-review.

<!-- rpi:task id=P02-T02 -->
#### [ ] P02-T02: Commit reviewed correction and original evidence

Resolve gh account, configure local noreply identity for author/committer and
commit with Conventional Commit/trailer. Fetch main read-only and confirm fixed
base; never alter branch ancestry or remote. Snapshot may mark exact commit/gate
pending because later outcomes must be external to avoid receipt invalidation.

<!-- rpi:phase id=P03 -->
### [ ] P03: One complete gate and exact receipt

Dependency: P02 complete and clean committed candidate.

<!-- rpi:task id=P03-T01 -->
#### [ ] P03-T01: Run one gate, verify, hash and stop

Use one new external directory and exact caller base with lock timeout 86400.
Wait for lock; no parallel/duplicate/interrupted gate. Retain failed evidence
honestly if prerequisites block. Explicit official verifier, receipt SHA-256
and head recorded externally. No publication or later candidate writes.

## Dependencies

Existing installed-package venv verified usable, 70 baseline tests passed.
Complete gate uses documented existing tools/runner; missing prerequisites
block acceptance, not a skipped or cloud replacement.

## Critique Disposition

One independent final-candidate critique executed, original verdict Revise.
Original artifact is retained unchanged. Both findings assume a `/tmp`
prohibition that is not present in the parent's applicable instructions or
caller request. Parent authority explicitly includes unique external logs and
the unchanged complete runner with its documented shared lock.

| Finding | Owner / disposition | Resolving evidence |
| --- | --- | --- |
| PC-001 | Parent / rejected as inapplicable worker-local restriction | C3/C4 and actual successful baseline through named installed venv; pip show confirms editable distributions in this worktree and Ruff 0.17.1. No parent TMPDIR prohibition exists. |
| PC-002 | Parent / rejected as inapplicable worker-local restriction | Caller expressly requires unchanged full gate with shared-lock wait; C5 documents `/tmp/ama-rpi-heavy.lock`. No parent prohibition exists; do not patch or bypass lock. |

No source change or user decision required by these findings. Gate success is
not promised in advance: actual prerequisite/matrix failures still block AC5.
Plan and details remain implementation-ready; summary and checklist reconciled.
No second critique will run.

## Follow-Up Items

* PR lineage resolution: outside correction; coordinator owns separately.
* Independent coordinator exact-head assessment: later authority, not executed.
* Original owner-governed deployed acceptance remains outside offline scope.

## Handoff

Ready after critique disposition. Implementation evidence:
.copilot-tracking/changes/2026-10-23/issue-350-ai-item-uniqueness-changes.md.
P01 complete: genuine six-subtest red, final 72-test green, targeted Ruff and
whitespace pass. P02-T01 complete: one original Review, Complete / Residual work,
no in-scope blocking defect. RV-001 routes commit/pre-gate hygiene/gate to parent;
RV-002 preserves separate lineage and independent/live acceptance. Parent
continues P02-T02 then P03 with no repeated Review or routine approval.
Exact-head delivery is not yet complete; downstream results remain external.

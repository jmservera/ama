<!-- markdownlint-disable-file -->
# RPI Plan: PR 507 evidence corrections

## Task Metadata

* Task ID and slug: pr507-evidence-corrections
* Date: 2026-10-30
* Planning status: Ready; sole critique disposition recorded
* Details: .copilot-tracking/details/2026-10-30/pr507-evidence-corrections-phase-details.md
* Critique: .copilot-tracking/reviews/plans/2026-10-30/pr507-evidence-corrections-plan-critique.md

## Executive Summary

Correct the integrated documentation's stale delivery claims and B6 recovery
route, retaining the original candidate as explicitly historical evidence.
Prepare a replacement PR body and suggested documentation-only title without
writing to GitHub. Validate focused contracts and links, then obtain one
independent Review and commit locally.

### What You May Not Know

The original 374/1/7 result is not the integrated 355/18/7 result.
Neither the evidence pack nor rubric guide is registered B6 evidence. A later
real src README change can reopen B6 but cannot guarantee a score increase.
The prior integrated frozen hash remains historical after these corrections.

### Unresolved Decisions or Blockers

None to bounded implementation. Inherited suite/runtime and publication gates
remain unmet and are not part of this local-only correction's acceptance.

## User Decisions and Requirements

* Execute Research, Plan, Implement and Review with dated tracking artifacts.
* Correct both supplied Copilot findings in the existing evidence pack.
* Retain Refs #198, with no closing-keyword references.
* Write corrected description to /tmp/pr507-body.md for owner application.
* Use registered B6 recovery evidence and name a later PR when it changes.
* Validate relevant tests/link checks using /tmp/mv; commit locally with
  Conventional Commit and required Copilot trailer; no push or score edits.

## Goals

Make current delivery, historical evidence and prospective recovery unambiguous.

## Scope and Non-Goals

Change the pack, its KB index/log and new dated RPI artifacts; create the
requested external PR body. Do not edit scored source, guide, fixtures, registry,
scores, workflows, original evidence or unrelated prior audit defects.
No new PR creation, remote metadata update, rebase, merge or push.

## Functional Requirements

* Correct downstream registry/test prose and both acceptance rows, not just
  append another contradictory disclaimer.
* Separate original de87d9e0/09099ecd boundary from integrated
  8059b4aa/ffd8f35e boundary, identifying each historical assessed candidate.
* Replace the rubric-guide B6 route with src/README.md (solution-code) and
  proposed later PR "docs(src): strengthen B6 navigation and evidence".
  No PR number exists yet; identify it as proposed, not delivered.
* Replacement body uses a stable commit-linked integrated frozen diff and
  includes the same original/current test and scoring boundaries.

## Non-Functional Requirements

Preserve all old tracking bytes, the full existing log prefix and all scored/
executable inputs. Do not claim green CI, fresh score, issue acceptance or
publication approval. Label prepare no-score as a decision, not a model score.

## Acceptance Criteria

* Both review comments addressed at their cited sentences/rows.
* Current candidate described as documentation-only, 355 passed/18 failed/
  7 skipped; original fixture/guide results explicitly historical/discarded.
* Proposed B6 path matches actual registry and only a future changed path
  can support incremental reassessment.
* /tmp/pr507-body.md exists, contains Refs #198 and no closing-keyword reference,
  includes suggested replacement title and both frozen-boundary qualifications.
* Focused tests, actual prepare, registry match assertions and changed local
  links/anchors are checked; exact failures and skips recorded.
* One independent critique, one independent Review and a clean local commit
  with required identity/trailer; no remote write or latest.json modification.

## Implementation Context Record

Research: .copilot-tracking/research/2026-10-30/pr507-evidence-corrections-research.md,
Complete / executed / Ready. Changes:
.copilot-tracking/changes/2026-10-30/pr507-evidence-corrections-changes.md.
Parent owns explicitly requested progression through all four phases.

## Sources

Research C1-C8/W1; exact PR comments and prior integrated Review.
Main comparison base: ffd8f35e63b24905b9aeb937dbf2a7fe9968747f.
Starting HEAD: 254d2274693c8190f827067c3732e03d102a563d.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Correct delivery and recovery evidence

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Reconcile pack, KB and external PR body

Qualify historical fixture/guide claims throughout reconciliation; correct
acceptance rows; retain score provenance; add dated review correction and
historical frozen references, update index and append KB log.

<!-- rpi:phase id=P02 -->
### [x] P02: Validate and prepare independent Review

Depends on P01.

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Validate focused tests and evidence contracts

Existing tests owned by rubric maintainers; removals none, additions zero,
no test source edits. Run relevant existing prepare/gate selectors and migration
regressions. Assert real matching for src/README.md versus rubric guide and
prepare should_score=false. Check changed links/anchors, protected bytes,
append-only log, closing-reference prohibition and whitespace.
Use /tmp/mv; if pytest missing, install only missing pytest/dependencies into
task-owned external storage, not the shared venv, and record exact invocation.
Full rubric rerun may confirm the inherited 355/18/7 boundary without repairs.
No full API/browser/SQL/image suite or publication receipt claimed.

<!-- rpi:task id=P02-T02 -->
#### [x] P02-T02: Reconcile evidence, freeze correction and hand off

Depends on P02-T01. Complete plan/details/changes and freeze non-tracking
worktree diff plus external body hash; independent Review reads exact artifacts
and body. Then parent commits only task-owned files and verifies Git metadata
and clean status. Any Review findings route later, with no same-task fix loop.

## Dependencies

One independent final-candidate critique before P01. Existing /tmp/mv and
temporary external test storage. Owner later applies body/title to PR.

## Critique Disposition

Sole independent critique executed Complete / Revise, one High PC-001.
Disposition: rejected. PC-001 proposes replacing the explicitly requested
/tmp/pr507-body.md and /tmp/mv paths based on a worker-local filesystem
restriction not present in the parent's execution contract. Caller direction
already resolves the choice; no parent restriction forbids these paths.
Do not silently substitute outputs or claim a blocker. Keep the requested
paths, isolate missing pytest tooling in task-owned session storage, and do
not mutate the shared venv. No second critique. The original critique remains
unchanged. No substantive correction, frozen-reference or B6 defect was found.

## Follow-Up Items

* Proposed later B6 src README PR, only upon actual scoped content change.
* Rubric owner: inherited 18 failures and 7 runtime skips, outside doc repair.
* Owner/coordinator: historical #198 gaps, metadata application and publication
  gates. Prior audit-path RV-001 remains outside these two requested findings.

## Handoff

Planning and implementation Complete; P01/P02 and all task markers complete.
Changes record contains actual results and frozen correction/body hashes.
Ready for the sole independent Review; local commit remains parent lifecycle
work afterward. No unresolved decision; inherited adverse results preserved.

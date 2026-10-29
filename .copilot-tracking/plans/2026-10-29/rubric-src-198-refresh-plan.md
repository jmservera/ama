---
title: PR 507 integration plan
ms.date: 2026-10-29
---

## Task Metadata

Task ID: pr-507-refresh-2026-10-29. Slug: rubric-src-198-refresh.
Planning status: Ready; independent critique Complete / Pass.
Details: .copilot-tracking/details/2026-10-29/rubric-src-198-refresh-phase-details.md.

## Executive Summary

Rebase the existing draft onto fetched main and keep both documentation
contributions. Main owns every rubric file and the scenario manifest.
Run focused local checks, preserve dated adverse historical evidence, and
commit the refreshed candidate and this new RPI loop without pushing.

### What You May Not Know

Main has substantial application changes, but this PR's surviving delta is
documentation and original tracking evidence. `/tmp/mv` points editable installs
at another worktree, so explicit local namespace roots must win during tests.
No new hosted-CI result or publication receipt can be inferred from local checks.

## User Decisions and Requirements

* Refs #198 / draft PR #507; reuse `feat/rubric-src-198`, fetch and rebase main.
* Preserve both additive document sides; take main's rubric and manifest.
* Keep application source in src, tests outside packages, no legacy source.
* Use /tmp/mv for Ruff, formatting, applicable core/API mypy and relevant tests.
* Full API discovery only if `flock -n /tmp/ama-rpi-heavy.lock true` succeeds;
  hold that lock throughout any heavy suite actually selected.
* No Azure resource changes, push, closure keywords or inferred approval.
* Conventional Commit and required Copilot coauthor; record commands/results.
* Complete Research, Plan, Implement and one independent Review in this task.

## Goals

* Eliminate integration conflicts without losing either documentation history.
* Verify the actual checkout and report local versus hosted acceptance precisely.

## Scope and Non-Goals

Rebase/resolution, authoritative main restoration, related documentation,
focused validation and dated evidence are in scope. No new application feature,
rubric redesign, Azure operation, issue acceptance or remote mutation.

## Functional Requirements

* Fetched main must be an ancestor of the local candidate.
* Rubric tree and scenario manifest must be byte-identical to reviewed main.
* Main log is a byte prefix of resolved log; branch-only entries remain.
* Preserve all original 2026-10-27 RPI artifacts without rewriting outcomes.

## Non-Functional Requirements

* No dirty unrelated work is moved, discarded or committed.
* Explicit PYTHONPATH selects this checkout; dependencies remain pinned.
* Missing or failing checks remain failures, never success-shaped substitutes.

## Acceptance Criteria

* No conflicts or conflict markers; whitespace check passes.
* Ruff check, format check and mypy pass for core and API.
* Scenario integrity, namespace/dependency and relevant rubric regression checks
  run with explicit results. Any failure receives bounded investigation.
* Independent critique and Review each execute once, preserving original verdicts.
* Local commit uses authenticated account's privacy-safe author/committer email
  and required trailer; no push is performed.

## Sources

Research: .copilot-tracking/research/2026-10-29/rubric-src-198-refresh-research.md,
C1-C6 and W1. Original evidence remains under the same phase directories dated
2026-10-27. Reviewed main: `5653547507f3056f09a726a18516237728da5e5b`.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Integrate authoritative main

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Rebase and reconcile documents

Resolve three known documentation conflicts with both sides preserved. Restore
main-owned rubric and manifest even where Git reports no conflict.

<!-- rpi:phase id=P02 -->
### [x] P02: Validate the integration

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Run bounded local checks and record exact results

Run core/API Ruff and mypy, scenario and dependency selectors, and surviving
rubric regression checks using available existing tooling. Do not select full
API discovery merely because a lock probe succeeds; focused coverage suffices
for a documentation-only surviving delta.

<!-- rpi:task id=P02-T02 -->
#### [x] P02-T02: Reconcile evidence for independent Review and local commit

Update changes, plan and details for the Review handoff. The parent lifecycle
then performs one independent Review and commits the candidate plus original
new evidence; these are post-implementation actions, not unchecked source work.
Publication/full exact-head gate and
fresh hosted checks remain coordinator work, not claimed locally.

## Locked Test and Output Ownership

Test additions maximum: zero. Test removals: none. Restore main rubric tree,
including removal of branch-only edits to its existing tests. No generated
application output or manifest re-pinning is authorized. Canonical targets:
three documentation files and dated tracking artifacts. Regression: existing
test_scenario_manifest and project dependency rules; semantic preservation:
exact git blob/tree comparisons, main log prefix and original-artifact hashes.
Use /tmp/mv Python with local source/test roots; do not mutate shared editable
install pointers. A missing tool may be restored only after an actual failure.

## Dependencies

P02 depends on P01. Local validation requires existing /tmp/mv tooling.
Review requires reconciled actual changes and validation evidence.

## Critique Disposition

One independent critique executed: Complete / Pass, no PC findings.
Artifact: .copilot-tracking/reviews/plans/2026-10-29/rubric-src-198-refresh-plan-critique.md.
No repeat critique, new user decision or scope expansion.

## Follow-Up Items

* Rubric owner: inherited main suite has 18 failures and seven missing-runtime
  skips. Fixing rubric inputs would violate this task's explicit main-copy
  policy; no green complete-suite claim is made.
* Coordinator: required complete exact-head publication gate and fresh hosted CI
  after authorized push. No publication is performed here.
* Owner: original historical #198 score/sequence acceptance remains separate.

## Handoff

Changes path: .copilot-tracking/changes/2026-10-29/rubric-src-198-refresh-changes.md.
P01 and P02 complete. Ready for the parent's one independent Review, followed
by local commit. No source implementation remains. Complete rubric-suite
acceptance and publication remain blocked/deferred as recorded above.

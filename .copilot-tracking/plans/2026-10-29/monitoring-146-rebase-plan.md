---
title: Monitoring 146 rebase plan
description: Reconcile draft PR 512 with main and validate without publication
ms.date: 2026-10-29
---

Task ID: pr-512-rebase-2026-10-29. Slug: monitoring-146-rebase.
Planning execution: Complete; readiness: Ready after direct critique disposition.

## Executive Summary

Rebase the existing two-commit monitoring branch onto fetched main, retaining
both log/index contributions and upstream rubric/scenario content. Exercise
the merged Bicep and relevant Python contracts locally, then preserve one
independent Review and commit dated evidence. No push or Azure operation.
Hosted rubric access failure and final publication gates remain separate.

## User Decisions and Requirements

* Full dated Research, Plan, Implement and Review loop for draft PR #512.
* Explicitly authorized `git fetch origin; git rebase origin/main`.
* Preserve both sides' intent, particularly index/log entries; use main's
  rubric and scenario manifest, and retest pinned scenario sources.
* Application source only under src; tests outside package directories.
* Use `/tmp/mv`, Ruff check/format, applicable core/API mypy and relevant units
  with sibling source/test paths. No full API discovery without free heavy lock.
* Do not create/modify Azure resources or push. Use Conventional Commit and
  specified Copilot trailer; use Refs #146, no closure language.

## Goals

G1: Locally conflict-free ancestry including fetched main.
G2: Preserve monitoring behavior and upstream intent.
G3: Reproducible, truthful coordinator handoff and validation evidence.

## Scope and Non-Goals

Scope: rebase conflicts, tightly related integration/CI fixes, dated evidence.
Non-goals: monitoring activation, application redesign, human acceptance,
rubric permission changes, private data, cloud validation, push/merge.

## Functional Requirements

FR1: Retain every original monitoring and upstream log/index entry.
FR2: Keep upstream rubric and scenario manifest byte-identical.
FR3: Retain upstream model configuration and monitoring Bicep wiring together.

## Non-Functional Requirements

NFR1: Preserve original RPI evidence and adverse outcomes without amendment.
NFR2: No private data reads, Azure writes, full API suite or heavy operations
without the specified lock/authority.
NFR3: All new/rewritten commits use resolved privacy-safe identity; new commit
has Conventional Commit subject and required co-author trailer.

## Acceptance Criteria

AC1: Rebase completes; fetched base is an ancestor and no unmerged paths remain.
AC2: Both sides' index blocks and log additions are present; no conflict markers;
upstream rubric/scenario files unchanged and upstream Bicep inputs retained.
AC3: Core/API Ruff check, format check and mypy pass; focused scenario/dependency
units and relevant infrastructure regressions/compile pass, or concrete blockers
are recorded rather than hidden.
AC4: One independent critique and one independent post-implementation Review
are preserved with dispositions, commands/results, amendments and limitations.
AC5: Implementation and evidence committed, clean worktree, no push. Successful
local handoff requires no unresolved in-scope correctness or required-check
blocker. A blocked/evidence-only handoff is not acceptance. Hosted CI and full
publication receipt cannot be claimed from this local-only boundary.

## Evidence and Readiness

Research: .copilot-tracking/research/2026-10-29/monitoring-146-rebase-research.md.
Fetched base: 356a3cfbaa2cd63a6fbf80e87e11a29cacaaf4c7.
Original head: 3faac99513fff0e73ebd8a2bcef4e91a0ae4946f.
Conflict preview: reference README/log only; source merges automatically.
All implementation decisions supplied. Candidate ready for one critique.

## Locked Test and Output Ownership

Existing infrastructure tests own Bicep contracts; core owns scenario/dependency
contracts; API owns dependency/related API regressions. Exact removals: none.
Maximum new test modules: zero; maximum added regression methods: two, only
if a real tightly coupled bug is discovered. No weakening hashes or assertions.
Canonical manifest: docs/reference/research/retrofit-synthetic-data/scenario-manifest.json,
upstream copy. No generated tracked outputs. External logs/compiled ARM stay in
the session files directory. Semantic checks: ancestry, both-side preservation,
main-owned file equality and Bicep compile; regression checks: existing tests.

## Phase Checklist

<!-- P01 -->
### P01: Rebase and reconcile

* [x] P01-T01: Rebase onto fetched main and resolve log/index conflicts.
* [x] P01-T02: Verify both-side preservation and upstream-owned content.

<!-- P02 -->
### P02: Validate

* [x] P02-T01: Run core/API Ruff/mypy and relevant units in /tmp/mv.
* [x] P02-T02: Run focused infrastructure tests and offline Bicep compilation;
  investigate and fix only tightly coupled failures, preserve command outcomes.

<!-- P03 -->
### P03: Review and commit

* [x] P03-T01: Reconcile plan/details/changes and execute one independent Review.
* [ ] P03-T02: Commit evidence and permitted fixes without pushing; record final
  clean status and ancestry. Do not claim hosted or full-gate approval.

## Critique Disposition

Execution: Complete. Original verdict: Revise. Output:
.copilot-tracking/reviews/2026-10-29/monitoring-146-rebase-plan-critique.md.

* PC-001 (High): Applied directly. AC5 and P03 distinguish new local correctness/
  required-check blockers from historical operational/hosted residuals.
  Any unresolved local blocker prevents successful handoff; preserve the one
  Review outcome without looping or claiming that committing cures a defect.
* PC-002 (Medium): Rejected its alleged no-`/tmp` constraint: no such constraint
  exists in the caller, repository or parent execution instructions; caller
  explicitly names `/tmp/mv` and the shared `/tmp` heavy lock. Reviewer's
  context-specific assertion is not evidence of parent authority. Existing
  tests may use their normal TemporaryDirectory cleanup. Tool caches/logs will
  be directed to the session files directory where practical; no historical
  or unrelated files will be removed. No user decision is needed.

No repeat critique. All applicable findings disposed; candidate Ready.

## Follow-Up Items

* Coordinator publication with exact-head full gate, independent assessment
  and hosted checks; rubric integration access failure may require authorized
  hosted administration, not candidate permission/protection edits.
* Original monitoring RV-001 through RV-004 remain historical operational
  follow-ups, outside this rebase task.

## Handoff

Details: .copilot-tracking/details/2026-10-29/monitoring-146-rebase-phase-details.md.
Implementation record:
.copilot-tracking/changes/2026-10-29/monitoring-146-rebase-changes.md.
No implementation begins until critique dispositions are resolved.

Implementation handoff: P01/P02 complete at rebased source
c254fa097e96079a4c5d0ae8a6f93f22eda843e5. No application/test additions
or source correctness blockers. P03-T01 is complete: one independent Review
Complete / Conformant at that boundary, zero new findings. P03-T02 remains
the local evidence commit and clean-state confirmation; no second Review.

<!-- markdownlint-disable-file -->
---
title: Documentation PR preparation plan
description: Isolated rebase and guarded publication plan for three documentation PRs
ms.date: 2026-10-27
---

## Task Metadata

* Task ID: docs-prs-rebase-2026-10-27; slug: docs-prs-rebase.
* Status: implementation-ready; one critique completed and directly disposed.
* Details: .copilot-tracking/details/2026-10-27/docs-prs-rebase-phase-details.md
* Critique: .copilot-tracking/reviews/plans/2026-10-27/docs-prs-rebase-plan-critique.md

## Executive Summary

Prepare only #454, #439 and #429 on isolated remote-head worktrees, preserving
main and topic documentation, then validate, commit evidence, review and publish
eligible heads with exact leases. Mark ready, observe checks and report to the
coordinator without merging.

### What You May Not Know

Existing local branches contain unpublished or divergent work; preserve them
untouched. Full local gates remain required by explicit repository guidance
despite the newer partial-tier documentation. Gate failures block publication,
not truthful reporting of local preparation.

## User Decisions and Requirements

* Run research, plan, implement and review in order; commit dated evidence.
* Rebase only #454, #439 and #429 onto latest origin/main in separate worktrees.
* Preserve both sides, especially all append-only docs/reference/log.md entries.
* Fix links, perform Markdown/link review and git diff validation.
* Push with --force-with-lease, mark ready, let checks run and report mergeability.
* No merges, main pushes, closing keywords or changes to the eight excluded code PRs.
* Include the specified Copilot coauthor trailer in every new commit.

## Goals

Produce docs-only, reviewable, conflict-free candidate branches and reliable
per-PR publication/check state for the coordinator's subsequent merge gate.

## Scope and Non-Goals

Only the three remote PR snapshots, in-scope documentation/link repairs and
dated tracking artifacts. No code, live service, budget or product-scope changes.
Do not delete historical evidence, alter old outcomes or publish local-only work.

## Functional Requirements

Create fresh local preparation branches tracking the respective remote branches.
Use rebase with explicit conflict resolution. Preserve original refs and record
old head/new head/base. Each final PR diff must contain only docs/, tracking and
the permitted rubric score file. Keep main's current rubric score rather than
replay obsolete generated scores; original score commits remain in original refs.
Copy this task's original RPI evidence into each candidate before its final gate.

## Non-Functional Requirements

No uncommitted input loss, broad cleanup, main write or protection change.
Use authenticated GitHub noreply identity locally. Record observed results
without converting skipped, unavailable or pending checks into success.

## Acceptance Criteria

* Three distinct clean worktrees, reviewed main ancestor and allowed-path diff.
* Main log is a byte-preserved prefix, and every topic-added log entry survives.
* Changed Markdown local paths and anchors resolve, or historical/archive-backed
  exceptions are identified precisely; semantic diff preserves topic intent.
* Dated research, plan, details, critique, changes and original Review are committed.
* Each eligible publication has a verified external full receipt for that exact
  clean head/base, no unresolved publication-blocking Review finding and an
  affirmative independent exact-head publication assessment. Failed, blocked or
  incomplete assessment blocks that PR's push and ready transition.
* Explicit old-SHA lease succeeds; PR is ready, not merged; actual current-head
  checks and mergeability are reported, including unresolved blockers.

## Sources

Research: .copilot-tracking/research/2026-10-27/docs-prs-rebase-research.md,
C1-C5 and W1-W2. Owner's 2026-10-27 request governs the bounded remote actions.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Isolate and rebase

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Capture remote heads and create fresh worktrees

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Rebase each snapshot and resolve semantic/log conflicts

<!-- rpi:phase id=P02 -->
### [x] P02: Validate and preserve evidence

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Review Markdown, links, allowed paths and append-only preservation

<!-- rpi:task id=P02-T02 -->
#### [x] P02-T02: Commit implementation and original RPI evidence after Review

<!-- rpi:phase id=P03 -->
### [ ] P03: Gate and publish

<!-- rpi:task id=P03-T01 -->
#### [ ] P03-T01: Run full gates and independently assess exact eligible heads

<!-- rpi:task id=P03-T02 -->
#### [ ] P03-T02: Verify leases, push, mark ready and observe hosted checks

## Dependencies and Locked Validation Contract

P01-T02 depends on P01-T01; P02-T01 on P01-T02; P02-T02 on P02-T01 and the
one post-implementation Review; P03-T01 on P02-T02; P03-T02 on passed gates
and exact-head independent assessment. Per-PR failures are isolated.

Test ownership: existing repository full-gate runner, no new repository tooling.
Exact removals: none. Maximum new executable tests: zero. Canonical targets:
three remote PR docs diffs and dated RPI artifacts. Generated targets: external
audit output and full receipts; no generated source or fabricated rubric score.
Semantic coverage: conflict intent and approval boundaries. Regression coverage:
link/path/anchor checks, diff whitespace, allowed-path assertion, main-log prefix
and topic-entry preservation, then tools/rpi-checks.py --all and verification.

## Critique Disposition

Execution: complete. Original verdict: Revise. One critique only.

| Finding | Disposition | Resolving change |
| --- | --- | --- |
| PC-001 | Applied directly | Publication requires no blocking Review findings and affirmative exact-head disposition; corrections invalidate old receipts/assessment, not a repeat original Review |
| PC-002 | Applied directly | Assemble available evidence before validation/Review; repeat final staged Markdown/link, path and diff checks after original Review is added |
| PC-003 | Applied directly | Resolve authenticated id/login immediately before committing; configure local email and verify author/committer headers and trailer |

## Follow-Up Items

* None.

## Handoff

Changes path: .copilot-tracking/changes/2026-10-27/docs-prs-rebase-changes.md.
P01 and P02 are represented by this candidate commit, including the original
adverse Review and separately recorded bounded preservation correction. P03
remains pending: full receipts and affirmative independent exact-head publication
assessment are distinct prerequisites, not another original RPI Review.

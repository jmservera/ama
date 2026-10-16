---
title: Task queue filter implementation plan
ms.date: 2026-10-16
---

Task: #327. Slug: task-queue-filters-327. Scope: full plan.

## Executive Summary

Replace repeated queue scans with a snapshot-scoped inverted membership index.
Preserve all queue definitions, role projection, authorisation, filters, global
ranks, cursors, sorts and CSV. Cold-build and warm-read costs are separate claims.

## User Decisions and Requirements

* Implement #327, measure before/after on 60,000 generated homes.
* Src-only code, tests outside packages; no private data, .env, .vscode or
  .copilot-tracking/github-issues access.
* No new nonportable SQL, uv, Docker, Azure or force-push.
* Local pip venv unit suites, ruff, mypy and a failing-without-fix mutation.
* Update README, append knowledge log, produce RPI artifacts, commit/push/PR.
* PR body uses Refs #327 and no issue-closing directive.

## Goals

Eliminate repeated work_context evaluation for non-output cases.

## Scope and Non-Goals

Store membership selection, queue regressions, generated timings and docs.
No queue-definition change, migration, live deployment or operational acceptance.

## Functional Requirements

Index all six queues using the canonical evaluator, retain no user narratives,
recheck user visibility on every read and invalidate on every membership input.

## Non-Functional Requirements

Warm 50-row pages evaluate at most 50 contexts; timing budget 1500 ms on 60k.
Report cold build honestly. Existing SQL path for unfiltered pages stays intact.

## Acceptance Criteria

JSON/SQLite parity, six queues, paging/sorts/search/filters/CSV, permission
denials/redaction, snapshot/policy/day/shared/cross-process invalidation.
Tests fail against original selection, all relevant local checks pass.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### P01 Evidence and implementation
Status: complete.
<!-- rpi:task id=P01-T01 -->
* [x] P01-T01 Record generated baseline and implement snapshot membership index.
<!-- rpi:phase id=P02 -->
### P02 Verification and delivery
<!-- rpi:task id=P02-T01 -->
* [x] P02-T01 Run parity, mutation, scale timings, unit suites, ruff and mypy.
<!-- rpi:task id=P02-T02 -->
* [ ] P02-T02 Update docs, review once, commit, push and publish PR.

## Critique Disposition

Final candidate critique executed once: Pass, no PC findings, artifact
reviews/2026-10-16/task-queue-filters-327-critique.md. Exact test ownership: core test_taskqueues.py
and test_sqlreads.py, existing API queue suite reused. No tests removed; maximum
eight added test methods. Canonical src code and docs only; generated datasets
stay temporary. Mutation reverts only queue selection in memory at test runtime.

## Follow-Up Items

Cold rebuild remains an explicit limitation, not live-platform acceptance.
If workload measurements later show frequent invalidations dominate, the owner
can prioritise incremental membership maintenance as a separate performance
task; this is not needed for the accepted snapshot-cache slice.

## Current Handoff

Implementation and verification complete. Documentation is updated. P02-T02
has only the single Review, commit, push and PR publication remaining. No
unresolved code issue or material divergence; no second critique required.

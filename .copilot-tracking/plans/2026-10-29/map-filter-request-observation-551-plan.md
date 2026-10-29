---
title: Map filter request observation correction plan
description: Scoped correction of the PR 553 duplicate-read test oracle
ms.date: 2026-10-29
---

## Task Metadata

Task ID: 551. Slug: map-filter-request-observation-551.
Status: Complete; independent Review Complete / Conformant with justified divergence.

## Executive Summary

Observe every map request during the first and repeated safety-filter
activation, rather than counting the single intercepted route. Compare a
baseline count after two animation frames and clean up the listener reliably.
No application behavior changes.

### What You May Not Know

The route holder intentionally passes later requests through, so its length
is incapable of detecting the regression. A negative-control browser run
will remove the guard in memory to prove that the corrected assertion fails.
The full publication gate is not requested: it requires prohibited Azure
operations; this work will be committed locally and never pushed.

## Sources

Research: .copilot-tracking/research/2026-10-29/map-filter-request-observation-551-research.md.
Existing issue Review: .copilot-tracking/reviews/logs/2026-10-29/map-filters-551-review.md.

## User Decisions and Requirements

* Fix the named Copilot finding using the check_browser_shortcuts listener pattern.
* Run the complete RPI loop with dated artifacts and commit locally.
* Use /tmp/mv and the caller's explicit current-source PYTHONPATH.
* Run focused API tests, Ruff lint/format check, JS syntax and actual browser checks where possible.
* Do not push, invoke az or hand-edit rubric scores.

## Goals

Make the duplicate-read assertion sensitive to every matching request and
prove both passing behavior and detection of a deliberate regression.

## Scope and Non-Goals

Canonical targets: the named Python browser check and its directly related
API README description. Tracking artifacts record all RPI phases.
No app/CSS, dependencies, shared utility or unrelated cleanup.
Generated reports and the mutation runner remain external session artifacts.

## Functional Requirements

Record every /api/map? request with page.on and a typed Request callback.
Install before first activation, verify first-request observation, save the
count before repeated activation, wait two animation frames and compare.
Always remove the listener in finally before unrelated area requests.
Preserve the existing held-route race and cleanup behavior.

## Non-Functional Requirements

Use the established local pattern without sleeps or production changes.
Keep existing checks intact; no broad exception handling or skipped failures.

## Acceptance Criteria

The corrected check passes against current app and fails at the duplicate-read
assertion when an in-memory served script removes the selected-flag guard.
Focused tests, lint, formatting and JS syntax pass; browser outcomes and
unavailable gates are recorded honestly. Local Conventional Commit includes
the requested coauthor trailer and uses GitHub-derived privacy-safe identity.

## Test Ownership and Budget

Owner: existing check_expanded_filters in map_fullscreen_browser_check.py.
Removals: only the ineffective len(held) assertion.
Maximum additions: one local request listener, two assertions (first-read
non-vacuity and unchanged repeated-read count), zero new test files/helpers.
Semantic regression proof: real Playwright positive and in-memory mutation
negative control. Existing source-contract tests remain unchanged.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Correct observation and documentation

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Observe all map requests and document coverage

Depends on research readiness and critique disposition.

<!-- rpi:phase id=P02 -->
### [x] P02: Validate the oracle and deliver locally

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Run focused checks and positive/negative browser checks

Depends on P01-T01.

<!-- rpi:task id=P02-T02 -->
#### [x] P02-T02: Reconcile evidence, run one independent Review and commit

Depends on P02-T01. Do not repair new Review findings within this task.
Implementation and validation reconciled; independent Review completed with
no findings. This final snapshot is prepared for the authorized atomic local
commit of source and original dated RPI evidence. Commit success and clean
worktree are verified outside the commit to avoid self-referential evidence.

## Critique Disposition

Execution: Complete. Original verdict: Revise. PC-001 (Medium), planning
parent-owned, is resolved by specifying nonblocking shared lock admission and
project-local browser scratch in P02-T01 details. No user decision is needed
and no second critique is run. The critique's unsupported statement that
all /tmp writes are forbidden is not adopted; its documented lock coordination
and isolated scratch recommendations are compatible with caller direction.

## Follow-Up Items

* None.

## Handoff

Details: .copilot-tracking/details/2026-10-29/map-filter-request-observation-551-phase-details.md.
Changes record to create during implementation:
.copilot-tracking/changes/2026-10-29/map-filter-request-observation-551-changes.md.

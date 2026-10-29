<!-- markdownlint-disable-file -->
---
title: Workspace script retry correction plan
description: Bounded correction plan for original RV-001 and RV-002
ms.date: 2026-10-28
---

# RPI Plan: workspace-script-retry-524-correction1

## Task Metadata

Task ID: 524-correction1. Date: 2026-10-28. Planning status: Ready.
Details: .copilot-tracking/details/2026-10-28/workspace-script-retry-524-correction1-phase-details.md.
Critique: .copilot-tracking/reviews/plans/2026-10-28/workspace-script-retry-524-correction1-plan-critique.md.

## Executive Summary

Prevent script recovery from restoring authenticated status or invoking a view
after the session ends or changes. Strengthen real-browser evidence of initial
failure, retry, recovery and late lexical execution without changing script bytes.
Preserve earlier artifacts and bounded retry policy.

### What You May Not Know

A 401 opens the same-document login screen without aborting the route. Tag
removal does not guarantee late script execution is cancelled. Shared-resource
contention can block validation and publication, not justify bypassing it.

## User Decisions and Requirements

* Continue #524 on fix/workspace-script-retry-524 and preserve original evidence.
* Correct RV-001 and RV-002; run research, plan, implement and independent review.
* Run heavy checks ourselves after nonblocking flock attempts every 60 seconds
  for at most 40 minutes. No Azure, secrets, .env or private datasets.
* Ruff line limit 100. Commit with privacy-safe identity and Copilot trailer;
  push without force and create PR with gh pr create using Refs #524.
* Live verification remains pending the owner.

## Goals

* Keep ended/replaced sessions isolated from asynchronous route completion.
* Produce deterministic actual-browser recovery and late-settlement evidence.

## Scope and Non-Goals

Canonical targets: app.js, test_workspace_scripts.py,
workspace_scripts_browser_check.py and src/api/README.md. Exact removals: none.
Maximum executable additions: zero files; extend the two existing test owners.
Tracking artifacts are new correction1 records, never historical rewrites.
No styling, auth redesign, retry-policy change, dependency additions or live work.

## Functional Requirements

* Compare current session identity before restoring status/dispatch after await,
  and before stale error rendering. No-session route entry must be harmless.
* Unit checks invalidate/replace sessions without an artificial abort.
* Browser checks exercise actual api() 401/login, assert initial script failure,
  absent global, recovery request, eventual actual global/view and no refresh.
* Late lexical response settles deterministically; measure real evaluation count
  and compare exact independent route/status before and after settlement.
* If browser cancels detached execution, explicitly assert zero evaluation and
  cached terminal failure on revisit; never assume cancellation.

## Non-Functional Requirements

* Preserve original messages, native Reload workspace, status/alert semantics,
  healthy dependency behavior, shared two-retry budget and terminal timeout.
* Browser traffic restricted to owned synthetic loopback server.
* All new Python lines <=100 characters, package Ruff/mypy and syntax checks pass.

## Acceptance Criteria

* AC1: null and replaced sessions cannot restore status, invoke view or render error.
* AC2: real 401/login persists unchanged after pending recovery completes.
* AC3: failed initial load is observed before retry; real script then renders map
  or specialist view, with exact request bounds and one document request.
* AC4: late response deterministically executes once or explicitly cancels with
  zero evaluations; no stale view, error or status before route revisit.
* AC5: API discovery and focused Chromium pass under shared lock; original
  adverse findings remain preserved and owner live verification stays pending.
* AC6: one independent critique and Review; committed exact-head full gate,
  external receipt verified against freshly fetched main before branch push/PR.

## Sources

Research: .copilot-tracking/research/2026-10-28/workspace-script-retry-524-correction1-research.md.
Original Review: .copilot-tracking/reviews/logs/2026-10-28/workspace-script-retry-524-review.md.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Correct session boundary and regression proof

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Guard session identity and extend unit contracts

Capture session before asynchronous recovery, guard entry and post-await success
and catch; cover null/replaced session, success/error and same-document 401.

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Make browser proof deterministic and update API guide

Observe initial failure and readiness absence, pending retry, actual-script
evaluation, settled route/status, real 401 and unchanged page lifetime.

<!-- rpi:phase id=P02 -->
### [x] P02: Validate and prepare independent Review

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Run required checks with bounded shared-lock admission

Run syntax, focused unit, package Ruff/mypy, line checks; under nonblocking lock
run full API discovery and workspace Chromium. Retain external output and
actual failures. Stop on exhausted admission budget; do not bypass.

<!-- rpi:task id=P02-T02 -->
#### [x] P02-T02: Reconcile evidence and hand off once for independent Review

Review complete stable candidate, then commit dated evidence. Publication uses
full exact-head gate and verified external receipt; no later source correction
or new commit can reuse the receipt.

## Dependencies

P01-T02 follows P01-T01; P02-T01 follows both source tasks. P02-T02 follows
validation. Existing /tmp/ama-524-venv, installed distributions and Chromium.
No generated deliverable targets; external logs/receipts are execution evidence.

## Critique Disposition

One independent critique executed, original verdict Revise, preserved at the
metadata path. Both compatible findings resolved directly; no second critique.

| Finding | Owner | Disposition and resolving evidence |
| --- | --- | --- |
| PC-001 | Parent | Applied: details P02-T02 specifies nonblocking full-gate admission, 60-second contention retries, 40-minute budget and unique external output per attempt. |
| PC-002 | Parent | Applied: details P02-T02 requires read-only independent exact-head receipt/source-boundary assessment before push, without repeating RPI Review. |

## Follow-Up Items

* Owner: historical live response/cold-start/auth correlation and post-deploy check,
  outside authorized local correction scope (original RV-004).

## Handoff

Changes path: .copilot-tracking/changes/2026-10-28/workspace-script-retry-524-correction1-changes.md.
Full implementation scope complete and reconciled; ready for one independent
Review. Full API discovery passed (1149 tests, 314 existing skips); focused real
Chromium passed under the shared lock after a single 60-second contention retry.
Final syntax, 32 focused units, package Ruff/format, mypy (92 files) and explicit
100-character Python limit passed. Publication remains a future exact-head gate.

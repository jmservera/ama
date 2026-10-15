---
title: Transactional hazard hold correction plan
description: Bounded follow-up for PR 314 review findings
ms.date: 2026-10-15
---

## Task Metadata

Task: hazard-hold-rv001. Parent: src-hazard-referral-85. Issue 85, PR 314.
Mode: explicit rpi-quick parent continuation. Readiness: Ready.

## Executive Summary

Register safety dependencies at the shared guard, then reload and validate
persisted hazards and rowversion inside the transaction that commits each
guarded mutation. Refuse stale/held writes atomically, including their audit.
Document that role/release authority and response timing remain unratified.

### What You May Not Know

Touching an unchanged case alone does not fix procurement: save skips it.
The existing SQL Server adapter already serializes writers across replicas.
Local synthetic SQLite evidence cannot establish live SQL Server acceptance.

## Sources

Evidence: .copilot-tracking/research/2026-10-15/hazard-hold-rv001-research.md
and the parent review. User-supplied RV-001/RV-002 and constraints are authoritative.

## User Decisions and Requirements

* Stay in the supplied worktree and feat/src-hazard-referral-85; merge main
  conflicts using the supplied log helper, never rewrite or force-push.
* Fix every guarded transition with transaction-local hazard reads, portable
  SQL and existing optimistic concurrency. Add interleaved actual-store tests.
* Code only in src; no mvp, .env, .vscode or github-issues tracking edits.
* Preserve unratified release/timing policy and unmet acceptance checkboxes.
* Test core/API with CI paths, ruff/mypy from /tmp/zf164/bin, pip only.
* Commit tracking evidence, push same branch, edit existing PR with Refs #85,
  mark ready only after fixing the code; no new PR or merge.

## Goals

Prevent a committed emergency hold from being bypassed by concurrent progression.

## Scope and Non-Goals

Shared SQL store dependency validation, directly coupled regression tests and
core/API documentation. No policy ratification, new transport or live platform
approval. Preserve the original loop and record this as a distinct child task.

## Functional Requirements

* Register each successful safety precheck as a save dependency.
* In save's existing writer transaction, read current hazards and rowversion
  before any mutation; active holds raise GateError, stale versions ConflictError.
* Refusal discards case/procurement edits, pending audit and dependencies.
* Clear unsaved dependencies on outer lock exit and after successful save.
* Keep withdrawal, referral and unrelated-home writes available.

## Non-Functional Requirements

Reuse writer serialization and parameterized portable SELECT/version checks.
No new SQLite-only syntax, exceptions by driver-name assumption, or dependencies.

## Acceptance Criteria

* Two actual SQLite stores interleave emergency intake after early validation:
  no Completed work order, no refused transition audit, hold survives restart.
* Exercise all guarded procurement, quality, technical and advance transitions.
* Confirm stale clear case version refuses write and a subsequent clean request
  is not polluted by old dependencies; validate transaction-local reload.
* Requested local suites/lint/format/types pass; commands/results recorded.
* RV-002 remains explicitly unratified; all original issue criteria unchecked.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Correct and verify

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Register and validate transactional safety dependencies

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Add interleaved regression and clarify policy boundaries

<!-- rpi:phase id=P02 -->
### [ ] P02: Validate, review and deliver

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Run requested local gates and reconcile evidence

<!-- rpi:task id=P02-T02 -->
#### [ ] P02-T02: One review, commit/push, update existing PR and readiness

## Critique Disposition

One final-candidate independent critique executed, verdict Pass, no findings.
Evidence: .copilot-tracking/reviews/plans/2026-10-15/hazard-hold-rv001-plan-critique.md.
No further critique required or performed.

## Follow-Up Items

* RV-002: Repairs/Safety/Housing must ratify release authority, response and
  resident-update timing/escalation policy; no local code can supply approval.
* RV-003: permitted verified service/model/SQL Server/Azure and human evidence.

## Handoff

Details: .copilot-tracking/details/2026-10-15/hazard-hold-rv001-phase-details.md.
Changes: .copilot-tracking/changes/2026-10-15/hazard-hold-rv001-changes.md.
Implementation and P02-T01 complete: integrated core 325 passed, API 477 run/OK with 97
skipped, core/API ruff/format/mypy passed. P02-T02's one review complete;
authorized delivery bookkeeping remains. No implementation blocker or plan divergence.
Do not repeat the parent Review.

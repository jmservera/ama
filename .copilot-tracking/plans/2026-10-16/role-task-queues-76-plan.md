---
title: Role task queues 76 plan
ms.date: 2026-10-16
---

Task: #76; slug: role-task-queues-76. Scope: full bounded offline plan.

## Executive Summary

Preserve delivered identity, role navigation, full-screen case and domain
controls. Add a shared projected task context, six visible engineering queue
definitions and versioned reset. Approved priority remains unavailable while
the existing ranking policy is draft. Prove behavior with local synthetic
JSON/SQLite, HTTP and browser checks, not live-platform or owner acceptance.

## User Decisions and Requirements

* Implement #76 gaps only in src following ADR 0006 and parity matrix.
* Preserve merged #116/#317/#318 functionality; no perspective simulator.
* Read issue comments and audit each criterion before changing source.
* Keep role/redaction/queue/ranking owner decisions open; no invented approval.
* Use /tmp/zf164, pip only, absolute PYTHONPATH per project, ruff/mypy,
  real loopback app and Playwright for UI changes.
* No forbidden private files or SQLite-only SQL additions. No deployment.
* Update docs and append reference log. Commit/push/PR with Refs #76,
  verified GitHub privacy email and required Copilot co-author trailer.

## Goals

Make queue membership understandable and case context consistent without
granting rights, mutating records or replacing domain workflows.

## Scope and Non-Goals

Core derived read model, Store/SqlStore read wiring, API metadata and filters,
web rendering/reset, tests, supporting docs and RPI evidence. No schema
migration, new task-writing endpoint, new auth provider, deployment, source
policy ratification or full PRD acceptance.

## Functional Requirements

Six independent filters: newly arrived (current stage within seven elapsed
days), approved priority (only if existing ranking policy is approved; draft
is visibly unavailable), stale evidence (EPC 30 days/Survey 180 days or
technical reassessment), blockers (recorded control prerequisites),
overdue (recorded pending handoff/resident-update/external-response due dates),
unowned handoffs (pending acceptance, never loss of sender accountability).
Missing/future dates remain unknown, not passing evidence.

Shared projected current owner/reason/next action, handoff accountability,
source/as-of/version, blocked-step reason/named owner/next action and hazard
clock observations are reused by list, detail, history context and suggestions.
Role-only blockers show named owner Unknown; no inferred assignment.

Server publishes one reset version/state/order/selection contract; browser
clears every queue override, returns own queue first page with no selection,
preserves focus and announces results. Existing actions remain server checked.

## Non-Functional Requirements

Respect default-deny contractor allowlists and existing need-to-know free-text
restrictions. Filter before count/page/export and preserve deterministic ranks.
No new SQL dialect dependency. Keep responsive rendering and cancellation.

## Acceptance Criteria

All seven issue criteria have an explicit before/after disposition. Synthetic
tests cover definition boundaries/unknowns, policy unavailability, unchanged
state, JSON/SQL/export parity, projected metadata and direct action denial.
Browser checks verify filters, case switching, reset, focus/status and reflow.
Operational approval and live-platform evidence remain unmet.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### P01: Shared queue contract (Complete)

* [x] P01-T01: Implement derived read context, visible definitions and JSON/SQL filtering.
* [x] P01-T02: Wire server metadata and projected context with regression tests.

<!-- rpi:phase id=P02 -->
### P02: Workbench and validation (Complete)

* [x] P02-T01: Reuse shared context in queue/case/history/suggestions and versioned reset.
* [x] P02-T02: Run targeted then per-project suites, ruff/mypy and local Playwright.

<!-- rpi:phase id=P03 -->
### P03: Evidence and delivery

* [x] P03-T01: Update docs/index/log, record review and reconcile evidence.
* [ ] P03-T02: Commit, push and create PR with Refs #76.

## Test Ownership and Candidate Lock

Core owns queue semantic tests; API owns HTTP/projection and browser tests.
Remove none. Maximum three new test/check files; extend existing checks where
appropriate. No generated assets required. Tests use constructed public fixture
data, not a private dataset. Preserve all existing tests and manifests.

## Critique Disposition

Single critique executed: reviews/2026-10-16/role-task-queues-76-critique.md,
verdict Revise. PC-001 through PC-004 applied directly in phase details:
explicit snapshot clock/lifecycle predicates, projected provenance/source
consumer, discriminating paged/reset oracles and structured blocker mapping.
PC-005 rejected: its alleged temporary-path prohibition is not an applicable
parent instruction and conflicts with the user's explicit /tmp/zf164 choice.
The existing venv was verified; retain it. No second critique.

## Follow-Up Items

* Owner/control owners: approve queue definitions and ranking policy owner.
* OQ-005 / OD-14/19: ratify role/field/redaction/delegation policies.
* Separate work: live SQL Server/Azure/AI and direct human acceptance.

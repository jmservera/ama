---
title: Employee progress dashboard 533 implementation plan
description: Stock-scale regression and publication plan for the existing employee views
ms.date: 2026-10-31
---

Task: 533 / employee-progress-dashboard-533.

## Executive Summary

Preserve the existing complete source feature and add missing 60,000-home
fixture coverage using seed-174 fictional homes and explicit lifecycle overlays.
Run the requested API/static checks and actual local Playwright, then exactly
one independent Review. Commit dated evidence and pass/verify the complete
external gate before authorized topic push/PR. Live-site acceptance stays open.

## User Decisions and Requirements

* Run Research, Plan, Implement, Review in order with dated committed artifacts.
* Deliver issue #533, including daily/weekly progress, additional statistics,
  chart tables, demo labels and URL-backed filtered/paged closed cases.
* Use existing synthetic 60,000-home data; never credentials/private datasets.
* New code belongs under src; tests outside the package; no mvp or framework swap.
* Preserve recorded AI briefing acceptance/change/rejection, not new AI authority.
* Run the exact requested API discovery, Ruff check and format check; local UI
  exercise uses Playwright. Use pip, never uv.
* Commit with required Copilot trailer, push named branch and create main PR
  using Refs #533, no closing keyword. Never touch main/other worktrees.

## Goals

Establish fresh reproducible local acceptance at stock scale while preserving
semantic, authority, provenance and URL-state contracts already delivered.

## Scope and Non-Goals

Canonical targets: src/api/tests/test_progress_dashboard.py,
src/api/checks/progress_browser_check.py, src/api/README.md and dated tracking
artifacts. No generated dataset bytes committed. No runtime edits absent a
demonstrated coupled defect. No live sign-in/deployment/issue checkbox changes.

## Functional Requirements

* Reuse scale_fixture.homes default 60,000/seed 174. Explicit test-only overlays
  reuse known small-fixture lifecycle cases; never infer lifecycle from random
  generic events or claim private geography/980-case lineage.
* Assert exact coverage, opened/closed/reopened totals, backlog, duration,
  current statistics, AI provenance and archive filtered page IDs at scale.
* Browser exercise real endpoints and rendered bounded page controls, retained
  URL filters/reload, six chart/table values and demonstration labels at scale.
* Retain all existing small-fixture tests and browser/error/keyboard/axe checks.

## Non-Functional Requirements

Read-only application behaviour; no inferred usage, legal compliance or consent.
Native Fluent-derived patterns unchanged. System Python missing namespace
packages: use existing pip-installed /tmp/mv environment with caller PYTHONPATH;
do not mutate another checkout. Bytecode and lint/type caches must stay external.
Inspect actual lock ownership and use nonblocking standalone admission on
/tmp/ama-rpi-heavy.lock; runner owns its lock with --lock-timeout 0 and no
outer flock. Busy means blocked; no duplicate gate or foreign-output inspection.
Official Fluent usage retrieval returned not-found; disclose rather than assert
a fresh complete official component review.

## Acceptance Criteria

* AC1: daily/weekly flow and four-plus additional statistics retain exact values.
* AC2: all six charts have semantic equal-value tables.
* AC3: status/date/team/text filters precede stable paging; first/final/empty/
  beyond boundaries and URL/reload/history are covered.
* AC4: only synthetic figures labelled demonstration data.
* AC5-local: requested unit/static and actual local browser checks pass with
  skips individually disclosed; complete gate required for publication.
* AC5-live: owner-required deployed check remains a separate unmet criterion.

## Test Ownership and Locked Candidate

Exact removals: none. Maximum additions: one shared scale fixture function,
one JSON/SQLite-inherited scale unit method, one opt-in scale browser function
and CLI flag in the existing checker. No new abstraction, tool or dependency.
Semantic coverage stays in the existing unit/browser suite; scale additions
check exact cohort output and paging, not a speculative performance SLA.
Original critique and Review outcomes must remain unchanged.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### P01: Scale regression coverage

* [ ] P01-T01: Implement existing-home test overlay and exact scale unit checks.
  Authored, but RV-001 identifies a missing initialized funding fixture contract;
  complete/validated status is not established.
* [x] P01-T02: Add opt-in scale Playwright and update directly related guide.

<!-- rpi:phase id=P02 -->
### P02: Validation and evidence

* [ ] P02-T01: Execute focused regressions, full requested API discovery,
  Ruff/format/types and small plus scale browser checks with pinned axe.
* [x] P02-T02: Reconcile plan/details/changes and conduct one independent Review.
  Complete / Not accepted; original RV-001 through RV-003 retained.

<!-- rpi:phase id=P03 -->
### P03: Authorized publication administration

* [ ] P03-T01: Resolve authenticated noreply identity and commit source/evidence.
* [ ] P03-T02: Run complete exact-candidate gate, fetch/verify current-base receipt
  and obtain independent exact-head assessment without a second RPI Review.
* [ ] P03-T03: Push requested branch and create PR to main with Refs #533,
  sources, validation, original outcomes and unmet live/human/hosted boundaries.

## Critique Disposition

One actual independent critique executed: Complete / Revise, four findings,
original preserved. Prior phase-authoring worker refused without critique or
file changes; a compatible general-purpose worker performed the one critique.

* PC-001: Rejected worker-specific inability to operate /tmp as a parent blocker.
  Actual parent baseline used the existing pip-installed /tmp/mv distributions
  and caller's exact PYTHONPATH, successfully ran 43 tests in 8.175s under the
  fixed shared lock. Parent can create external evidence/scratch. Accept clean
  preflight/external caches; no runner/helper change or missing-prerequisite
  success is inferred. Caller explicitly requires source PYTHONPATH.
* PC-002: Accepted mandatory publication stop for material open Review findings.
  Rejected same-task correction/re-review advice conflicting with the one-pass
  RPI contract: route defects to later work and block affected publication.
* PC-003: Accepted concrete independent exact-head administrative assessment
  and fresh receipt verification before push; it is not a second source Review.
* PC-004: Accepted current root-guide nonqueued admission. Initial baseline
  already queued before this finding and actually passed; preserve that
  operational deviation, use nonblocking admission for all later heavy checks.

Readiness: Ready after these direct dispositions; no second critique.

## Follow-Up Items

Rank 1: RV-001 later bounded fixture-contract correction, then affected inherited
unit execution. Rank 2: RV-002 collect required changed-candidate unit/browser
and complete-gate evidence after explicit free-lock coordination. Publication
is blocked by both; no same-task correction or second Review.
Rank 3: RV-003 separately authorized deployed employee-site dashboard/archive acceptance,
direct human accessibility/usability and hosted PR checks/owner merge.
These are not active source tasks or locally completed approval.

## Sources and Handoff

Research: .copilot-tracking/research/2026-10-31/employee-progress-dashboard-533-research.md,
C1-C6/W1-W3. Changes destination:
.copilot-tracking/changes/2026-10-31/employee-progress-dashboard-533-changes.md.
Readiness: candidate ready; final readiness depends on critique dispositions.

## Original Review and Publication State

One independent Review Complete / Not accepted at
.copilot-tracking/reviews/logs/2026-10-31/employee-progress-dashboard-533-review.md.
RV-001 identifies a static failure path in the raw test fixture replacement,
RV-002 required candidate execution is missing, RV-003 separate approvals stay
open. Do not publish or claim completion. Local WIP/evidence commit is authorized.

---
title: Employee progress dashboard 533 correction plan
description: Initialized fixture correction and complete validation before publication
ms.date: 2026-10-31
---

Task 533 / employee-progress-dashboard-533-correction; parent
employee-progress-dashboard-533. Plan candidate ready for independent critique.

## Executive Summary

Reuse initialized reader templates in the scale unit overlay without changing
browser fixture loading or runtime. Obtain exact JSON/SQLite regression, full
API unit, Ruff and small/scale local Playwright evidence. Preserve rejected
original Review; perform one independent successor Review. Commit the stable
candidate and evidence, require the complete local gate and exact-head assessment,
then publish a Refs #533 PR if all publication gates pass.

## User Decisions and Requirements

* Continue on feat/employee-progress-dashboard-533 in this worktree.
* Fix RV-001 and all implement-routed defects; original Review identifies only RV-001.
* Run requested full API discovery, ruff check and ruff format --check.
* Use flock -n /tmp/ama-rpi-heavy.lock for standalone heavy steps; retry later
  in this session if busy. Full runner self-locks with --lock-timeout 0.
* Pip only; no secrets, private data, Azure changes or force push.
* Commit with required Copilot trailer; push -u origin HEAD and PR to main
  including dated artifacts. Use Refs #533 while owner live acceptance is unmet.

## Goals

Restore the initialized fixture contract and prove changed-candidate behavior.

## Scope and Non-Goals

One test module and directly related guide; dated successor artifacts and
append-only updates to original changes/review. No runtime, framework, dependency,
SQL persistence-contract, live acceptance or cloud changes.

## Functional Requirements

Scale helper accepts initialized templates for unit overlays; browser retains
raw templates followed by real store initialization. All lifecycle, cohort,
AI exclusion and ordered paging expectations remain intact.

## Non-Functional Requirements

Never encode a partial funding-only default. Preserve synthetic-only provenance,
existing test ownership and exactly-once critique/Review. Heavy generated outputs
are external. Missing checks/prerequisites fail closed.

## Acceptance Criteria

* Corrected inherited scale method passes on JSON and SQLite.
* Full requested API suite and Ruff checks pass with skips individually recorded.
* Existing small and scale progress Chromium/axe checks actually pass.
* Independent successor Review reports a conformant local correction boundary
  only when no material finding remains.
* Publication requires a clean committed candidate, verified full external
  receipt at current origin/main and independent exact-head assessment.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### P01: Correct and validate

* [x] P01-T01: Optional initialized templates in existing helper; use reader templates in inherited unit regression.
* [x] P01-T02: Focused two-backend regression, full API discovery, Ruff and actual small/scale Playwright; record commands/exits/skips.

<!-- rpi:phase id=P02 -->
### P02: Review and publish

* [x] P02-T01: Reconcile evidence and perform one independent successor Review (Blocked / Not accepted due external evidence access; preserved).
* [ ] P02-T02: Commit original correction evidence; full gate and current-base receipt verification; independent exact-head assessment; push and PR.

## Test Ownership and Change Budget

Canonical test: src/api/tests/test_progress_dashboard.py inherited scale method.
Maximum additions: one optional helper argument and initialized-template call;
zero new test methods, zero removals. Browser checker unchanged. Any newly
observed out-of-budget defect blocks publication and routes to later work.
Semantics already covered by exact
scale expectations; correction adds contract-safe construction, not new metrics.
Generated logs, screenshots, axe and receipt go to new external directories.

## Critique Disposition

One independent critique executed: Complete / Revise, PC-001 Medium.
Accepted directly: removed the browser-checker escape clause and made
out-of-budget defects publication blockers routed to later work.
No significant unconfirmed choice remains. Critique:
.copilot-tracking/reviews/plans/2026-10-31/employee-progress-dashboard-533-correction-plan-critique.md.
Planning Readiness: Ready after disposition; no second critique.

## Follow-Up Items

Owner-required deployed dashboard/archive acceptance remains unmet. Human
accessibility/usability, full Fluent acceptance and hosted/owner approval remain
separate; local source conformance does not establish them.
Correction Review RV-001 routes the inaccessible external raw evidence to a
distinct evidence-access task. Source Review is not repeated in this task;
P02-T02 publication remains blocked until that material gap is resolved.

## Handoff

Details: .copilot-tracking/details/2026-10-31/employee-progress-dashboard-533-correction-phase-details.md.
Changes: .copilot-tracking/changes/2026-10-31/employee-progress-dashboard-533-correction-changes.md.

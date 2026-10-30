---
title: Capacity and work orders issue 523 plan
description: Acceptance coverage for the already merged capacity repair
ms.date: 2026-10-30
---

Task: 523 / capacity-work-orders-page-523. Base:
5634f9a077d175a931c15e3400114665d8c071ee.

## Executive Summary

The runtime repair is already in main through #528. Preserve it and strengthen
the existing local browser check with optional pinned axe scans of capacity's
seeded, error and empty states, plus keyboard retry. Re-run local SQL-backed
manager navigation and package validation. No deploy or live claim follows.

## User Decisions and Requirements

* Full ordered RPI loop with dated research, plans/details, changes and reviews.
* Exactly issue #523; use the supplied branch and base, source in src/, tests
  outside packages, pip only, native semantics and existing Fluent 2 standards.
* Required API unittest discovery, Ruff, formatting, mypy and local browser/axe.
* Heavy gates serialized with `flock -w 600 /tmp/ama-rpi-heavy.lock`.
* No Azure, deploy, live sign-in, credentials, secrets or push. Commit locally
  with the required coauthor trailer and Refs #523 only.

## Goals

Provide fresh local proof for the issue without duplicating merged code.

## Scope and Non-Goals

Canonical targets: src/api/checks/capacity_browser_check.py,
src/api/tests/test_capacity_browser_check.py and src/api/README.md.
No generated source targets. No runtime/design changes unless a directly
related reproducible failure requires a documented amendment.
No broader accessibility audit, product feature or unrelated cleanup.

## Functional Requirements

* Optional `--axe PATH` reads the pinned 4.10.3 asset with the existing digest.
  Validate bytes before starting any app or SQL container.
* Scan #app with existing WCAG 2 A/AA and 2.1/2.2 AA tags at seeded, each initial
  failed-read and empty capacity state; fail explicitly on violations.
* Activate initial-read retry with native keyboard input and verify recovery.
* Keep existing no-axe behavior, owned-store isolation, session and draft tests.

## Non-Functional Requirements

Existing CSS, Fluent-derived native controls, motion, auth and approval boundaries
remain unchanged. Use constructed fixtures only; no external browser traffic.
Keep stdout evidence useful and fail closed for bad axe bytes/results.
Use a fresh external venv and external logs, not the shared mutable environment.

## Acceptance Criteria

* AC1: Historical `/api/workorders` missing contract version cause is traced to
  existing null-preserving fix and passing regression; no new live claim.
* AC2: Real owned SQL Server seeded and empty capacity loads as manager.
* AC3: Both read failures show named plain-language errors and keyboard retry.
* AC4: Existing legacy HTTP regression passes; new scan input/violation tests pass.
* AC5: Actual manager navigation inventory checked, outcomes recorded.
* AC6: Live verification explicitly pending owner; it cannot be performed here.
* Additional: seeded/error/empty capacity axe runs and required local quality
  commands recorded with honest failures/skips. Full publication gate attempted
  after local commit, without Azure/cloud fallback.

## Test Ownership and Budget

API owns the existing regression, check and new test module. Exact removals:
none. Maximum additions: one test file and four test methods for valid pinned
input, invalid input, clean scans and violations. Reuse existing HTTP/root-cause
and SQL/browser cases rather than cloning them. Semantic coverage is unchanged
runtime behavior; regression coverage adds executable accessibility failure
handling and keyboard recovery. No generated test artifacts in git.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Scoped acceptance implementation

<!-- rpi:task id=P01-T01 -->
* [x] P01-T01: Add optional pinned axe input and seeded/error/empty scans, keyboard
  retry and up to four focused helper tests. Update the existing API guide.

<!-- rpi:phase id=P02 -->
### [x] P02: Validation and review

<!-- rpi:task id=P02-T01 -->
* [x] P02-T01: Install source distributions in an owned external venv if needed.
  Run regression and required API discovery/Ruff/format/mypy under heavy lock.
<!-- rpi:task id=P02-T02 -->
* [x] P02-T02: Run the enhanced local SQL browser check with pinned axe; retain
  exact manager route and error/empty results. No SQLite substitution.
<!-- rpi:task id=P02-T03 -->
* [x] P02-T03: Reconcile changes, invoke one independent Review, record outcome,
  commit implementation and original evidence; attempt complete local gate.

## Critique Disposition

One final-candidate independent critique executed: Revise, one Medium PC-001.
Disposition: applied directly. The external runner must preserve main's exact
environment allowlist and clear inherited settings before generating data or
constructing App/store. Details P02-T02 specifies this boundary. No divergent
decision and no second critique. Original artifact:
.copilot-tracking/reviews/plans/2026-10-30/capacity-work-orders-page-523-plan-critique.md.

## Follow-Up Items

Owner-authorized post-deployment verification remains pending and outside this
local task. Human/hosted approval and coordinator publication are not local proof.
The complete exact-head gate remains blocked by shared heavy-lock admission.
Coordinator must run it on the final committed head before publication; no
passing receipt exists. This is separate from completed scoped local checks.

## Handoff

Research C2-C6 and W1-W3 support this narrow plan. Implementation and local validation are complete.
P02-T01 passed: 1374 API tests, 318 optional skips, Ruff, formatting and mypy.
First full unittest admission timed out after 600 seconds; the second completed
after the owned SQL/browser gate released the lock. P02-T02 SQL/browser passed,
including twelve actual manager destinations and four clean axe scans.
P02-T03 completed its actions: one original independent Review (Complete /
Residual work, no source defects), local implementation/evidence commit
774be1549ad78eac144d659e8e957a238607bc3f, and post-commit complete-gate attempts.
The first refused ignored validation scratch; after archive/restore-verified
cleanup, the second refused shared-lock admission. Neither is a passing gate.
Final bookkeeping is committed separately without changing reviewed source.
Independent Review will assess this boundary honestly, not establish runtime
acceptance from static results. Details:
.copilot-tracking/details/2026-10-30/capacity-work-orders-page-523-phase-details.md.
Changes target:
.copilot-tracking/changes/2026-10-30/capacity-work-orders-page-523-changes.md.

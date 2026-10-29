---
title: Progress lifecycle element-type correction plan
description: Bounded correction for malformed synthetic lifecycle evidence
ms.date: 2026-10-29
---

Task: progress-dashboard-533-correction3. Status: implemented; ready for one
independent Review with full/browser validation explicitly blocked.

## Executive Summary

Reject non-dictionary history elements and non-string synthetic actions as
unknown lifecycle evidence. Expand the existing persisted JSON/SQLite matrix
across history, closures and returns, preserving legitimate non-transition rows.
API/core strict checks and targeted units pass. Busy nonblocking lock admission
blocks full suites/browser. Obtain one independent Review with that limitation
and preserve local commits; do not imply full validation acceptance.

## User Decisions and Requirements

* Full RPI loop for PR #540, Refs #533, on feat/progress-dashboard-533.
* First git pull --rebase succeeded; preserve bot commits and earlier evidence.
* Audit lifecycle and all three collections in one pass; reject malformed
  history rows and non-string synthetic actions before replay.
* JSON and SQLite regressions, source only in src; no push, az or force push.
* API/core mypy, ruff check . and ruff format --check . using /tmp/mv tools.
* Runtime/tests must prioritize this worktree's three package src/test paths.
* Full suites require flock -n /tmp/ama-rpi-heavy.lock; if busy, targeted fallback.
* Update scenario-manifest SHA-256 only if pinned files change.
* Conventional Commits and requested Copilot trailer; no closing keywords.
  Stop with local commits after review.

## Sources

.copilot-tracking/research/2026-10-29/progress-dashboard-533-correction3-research.md,
C1-C6. Existing correction2 artifacts are historical, not editable targets.

## Goals

Both reads remain available and disclose incomplete admitted synthetic evidence.

## Scope and Non-Goals

Only API progress.py, test_progress_dashboard.py, API README and dated RPI
evidence. No core behavior, storage schema, synthetic generation, web asset,
dependency-manifest, Azure, deployment or publication changes.

## Functional Requirements

All three collections require list containers with dictionary elements.
Only explicitly synthetic dictionary history rows participate in replay;
their action must be a string, including actions unrelated to lifecycle.
Unlabelled dictionary history and non-transition auxiliary dictionaries remain
ignored. Existing timestamp/ordering/current-state rules remain unchanged.

## Non-Functional Requirements

Explicit guards, not broad exceptions or string coercion. Preserve type safety
and existing admission, authorization, read-only and unknown-coverage semantics.

## Acceptance Criteria

* Persist/reopen malformed evidence through both JSON and SQLite for closed
  ZF-1 and open ZF-2 with explicit synthetic admission. Preserve valid history
  around malformed rows; assert None lifecycle, exact known/unknown coverage,
  no fabricated episode counts, null archive date and exclusion by either bound.
* Cover null, strings, empty/nonempty lists, dictionaries where invalid, bool,
  integer and float elements/actions; missing synthetic action also unknown.
  Exercise invalid rows before/after valid transitions so skipped rows fail.
* Sibling collections cover malformed containers and every non-dictionary
  JSON element kind, including empty/nonempty nested arrays and mixed rows.
  History whole-container replacements also roundtrip null, string, mapping,
  boolean, integer and float; distinguish container replacement, invalid row
  insertion and synthetic-action mutation in the persistence matrix.
* Positive controls preserve valid replay for missing/empty auxiliary lists,
  non-transition dictionaries with malformed ignored tags/timestamps/flags,
  valid synthetic narrative actions and non-synthetic dictionary history.
* Existing endpoint, valid lifecycle and read-only tests remain unchanged.
* Execute required static checks, lock-admitted full suites or honest targeted
  fallback, existing real-server progress browser check and one independent Review.

## Test Ownership and Change Budget

Canonical semantic/regression owner: src/api/tests/test_progress_dashboard.py.
No removals. Extend the existing inherited persistence method and add at most
two inherited methods; expand existing positive controls. No generated targets.
No pinned file is in scope. Browser/assets are validated, not modified.

## Phase Checklist

<!-- P01 -->
### P01: Guard and regressions

* [x] P01-T01: Extend persisted malformed matrix and positive controls; capture red.
* [x] P01-T02: Add guards and document lifecycle contract; capture green.

<!-- P02 -->
### P02: Validation and review

* [x] P02-T01: Execute API/core static checks and targeted units; record busy-lock
  fallback with full suites/browser explicitly blocked.
* [ ] P02-T02: Reconcile evidence, commit candidate, execute one independent Review
  and preserve original outcome in local closeout commit.

P01-T02 depends on P01-T01. P02 depends on P01.

## Critique Disposition

One independent final-candidate critique: Complete / Revise, PC-001 Medium
and PC-002 High. Original findings remain unchanged in
.copilot-tracking/plans/2026-10-29/progress-dashboard-533-correction3-critique.md.

* PC-001 applied directly: explicitly roundtrip malformed history containers
  alongside element/action cases, including floats, without new methods.
* PC-002 rejected as inapplicable to the parent execution context. The critic
  reported its own filesystem limitation; no such restriction applies to this
  parent's tools. The owner explicitly identifies /tmp/mv and the exact /tmp
  lock. Parent read access to both venv executables has already succeeded.
  Use the owner's paths and external scratch; probe actual lock/dependencies
  during validation and record genuine blockers, not a worker-local assumption.
  No permission override, replacement lock or publication claim is involved.

No unresolved significant/divergent user decision. Finalize directly without
a repeated critique.

## Follow-Up Items

Existing human accessibility and publication gates remain outside this correction.
No additional implementation work is currently supported.
Required full suites and browser are blocked by actual nonblocking admission
failure (exit 75, foreign PID 679022); run targeted fallback, do not poll or
mutate shared venvs. A later coordinated validation run owns these checks.

## Handoff

Details: .copilot-tracking/details/2026-10-29/progress-dashboard-533-correction3-phase-details.md.
Changes: .copilot-tracking/changes/2026-10-29/progress-dashboard-533-correction3-changes.md.

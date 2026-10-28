---
title: Capacity page 523 plan
description: Legacy package read compatibility and recoverable capacity loads
ms.date: 2026-10-28
---

## Task Metadata

Task 523, slug capacity-page-523. Branch fix/capacity-page-523.

## Executive Summary

Render legacy seeded work orders without inventing contract authority. Give
capacity load failures a useful message and the existing route retry.
SQL Server, browser and publication remain blocked by foreign heavy-lock
ownership. Lightweight source regression work can proceed independently.

### What You May Not Know

The demo generator omits the contract version expected by appointment bindings.
Newer procurement fixtures include it and did not expose the failure.
SQLite reproduces this exact exception; live causality is not yet verified.

## Sources

Issue #523 and .copilot-tracking/research/2026-10-28/capacity-page-523-research.md
(C1-C7). Details: .copilot-tracking/details/2026-10-28/capacity-page-523-phase-details.md.

## User Decisions and Requirements

* Run research, plan, implement, review in order; commit dated evidence.
* Use src/, the supplied topic/worktree, local SQL and generated demo data.
* No Azure, secrets, environment files or private data; heavy work needs nonblocking lock.
* Run API discovery and browser checks; preserve Ruff's 100-column limit.
* Publish only after required gates; use Refs #523 unless all criteria are proven.

## Goals

Recover manager visibility and keep unknown authority fail-closed.

## Scope and Non-Goals

Appointment read binding, capacity load error, focused tests and check harness,
directly related API guide. No generator rewrite, schema migration, identity
change, deployment or visual redesign.

## Functional Requirements

* Missing package contract_version projects null, never a fabricated version.
* Existing authority validation still denies work with no current version.
* Capacity request failures identify the affected data in plain language,
  preserve abort/session behavior and expose Try again.
* Known-empty packages and orders display explicit empty states.

## Non-Functional Requirements

Keep native semantics, existing Fluent styling, focus and unsaved draft behavior.
No global API fallback or unrelated manager repair.

## Acceptance Criteria

Track issue criteria independently: root-cause evidence; SQL manager capacity
read; error and retry; regression; other manager pages; pending-owner live check.
Actual SQL Server/browser criteria cannot be marked met by SQLite or source review.

## Test Ownership

Canonical tests: src/api/tests/test_procurement_api.py, inherited by existing
test_mssqlstore.MssqlProcurementApi. Add at most three methods there (legacy,
known-empty, permission controls); no removals. Add one bounded browser harness
under src/api/checks for seeded data, endpoint failures/retry and manager navigation.
Existing generator fixture supplies fictional register rows; generated JSON is
temporary, never a tracked target. No snapshots or generated source changes.
Semantic coverage: null unknown and authority denial. Regression coverage: the
exact absent-key legacy package read and real route rendering.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Repair read compatibility

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Add legacy contract-version regression and safe read

<!-- rpi:phase id=P02 -->
### [x] P02: Recover capacity loads

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Add scoped load message, retry coverage and empty state

<!-- rpi:phase id=P03 -->
### [ ] P03: Validate and review

<!-- rpi:task id=P03-T01 -->
#### [ ] P03-T01: Run lightweight tests and record blocked runtime gates

<!-- rpi:task id=P03-T02 -->
#### [ ] P03-T02: Independent one-pass Review, commit and gated publication

## Critique Disposition

One final-candidate critique executed; original verdict Revise retained at
.copilot-tracking/reviews/plans/2026-10-28/capacity-page-523-plan-critique.md.

* PC-001: partially applied. Require separate independent exact-head publication
  assessment after full receipt verification. Blocking Review findings block
  publication and route to later selected work, not an in-task repeat Review
  or implementation loop (RPI wrapper's explicit one-pass rule).
* PC-002: applied. All destructive inherited MSSQL tests require the gate's
  newly created labelled disposable container and constructed connection settings.
  Never run against ambient configuration or any pre-existing database.
* PC-003: applied. Browser inventory derives from actual manager navigation;
  assert heading/legitimate empty state, successful relevant reads and no page
  errors per route. Record all unchecked/failed routes, no unrelated repairs.
* PC-004: applied. Browser scenarios include both unstructured 503s, transport
  failure, structured actionable error, session expiry, abort and successful retry.
* PC-005: applied. Stable capacity_browser_check command documented in API README;
  separate exact-candidate browser result required, never inferred from full gate.

Readiness: Ready for bounded implementation. Runtime/publication gates blocked.

## Follow-Up Items

* Owner performs live verification after a separately approved deployment.

## Handoff

Implementation P01/P02 source has been delivered. The one independent Review
is Complete with full-task execution Partial and outcome Not accepted.
RV-002/RV-003 require later implementation; P03 remains incomplete and
publication blocked. Heavy validation requires explicit coordination and
admission. Original critique and Review are preserved, not repeated.
Changes path: .copilot-tracking/changes/2026-10-28/capacity-page-523-changes.md.

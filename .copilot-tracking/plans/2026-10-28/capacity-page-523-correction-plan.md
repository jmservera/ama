<!-- markdownlint-disable-file -->
# RPI Plan: Capacity page correction

## Task Metadata

* Task ID: 523-correction
* Task slug: capacity-page-523-correction
* Plan date: 2026-10-28
* Planning status: Ready; one critique Complete / Revise, PC-001 applied
* Phase details: .copilot-tracking/details/2026-10-28/capacity-page-523-correction-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-10-28/capacity-page-523-correction-plan-critique.md

## Executive Summary

Keep retry inside the capacity screen so repeated read failures retain editable
drafts and never replay a saved action. Strengthen the existing browser harness
to prove actual destination content and successful package/work-order reads.
Run real local SQL/browser validation, then original independent Review, commit,
complete exact-head gate and publication assessment before push/PR.
Recovery-path cancellation and 401 scenarios also prove the changed closure
cannot overwrite the next workspace or login.

### What You May Not Know

The prior implementation already restores unsaved appointment forms after a
successful refresh. Its new retry bypassed that behavior by calling the global
router, which replaces the screen on failure. SQLite-only or heading-only
checks do not establish the requested SQL/browser acceptance.

### Unresolved Decisions or Blockers

No unresolved design decision. Heavy lock admission, local prerequisites and
runtime results remain unknown; any failed material check blocks publication.
Live verification stays pending the owner.

## User Decisions and Requirements

* Continue #523 on fix/capacity-page-523; run a new complete correction cycle.
* Preserve all earlier artifacts; correct RV-002 and RV-003.
* Personally run local heavy SQL/browser checks after nonblocking flock attempts
  every 60 seconds for at most 40 minutes.
* No Azure, secrets, .env or private datasets; Ruff line length 100.
* Commit with Conventional Commits, privacy-safe authenticated identity and supplied
  Copilot trailer; push without force and create PR with evidence, Refs #523 only.

## Goals

* Recover failed reads without losing drafts or repeating mutations.
* Replace permissive test success with direct route/read/render proof.
* Obtain trustworthy runtime and publication evidence.

## Scope and Non-Goals

In scope: ops.js recovery closure, existing capacity browser harness, directly
related API README and new correction-cycle evidence. Retain the prior legacy
package compatibility repair and regression.
Non-goals: shared-router overhaul, redesign, RV-004/005/006 changes, deployment,
live acceptance, private/configured databases or foreign gate resources/output.

## Functional Requirements

* Retry only reads. Failed retry keeps the original editable screen; successful
  retry restores other unsaved forms, values, checks, expansion and context.
* Saved forms lose their unsaved marker only after successful mutation.
* Navigation abort/session expiry do not overwrite a new route or login.
* The browser inventories actual manager navigation and verifies exact heading,
  relevant content or legitimate empty state, successful expected browser GETs,
  unexpected HTTP/transport failures and real capacity row identities/counts.

## Non-Functional Requirements

* Use native status/button semantics and preserve Fluent/plain-language patterns.
* Keep Python lines at most 100; use existing lint/types/tests and no new dependency.
* Construct local fictional data; own and clean every created SQL/browser resource.
* Preserve full gate and independent/hosted/owner approval boundaries.

## Acceptance Criteria

* AC1: Mutation succeeds once; subsequent failed refresh and failed retry preserve
  another unsaved appointment draft; final successful retry restores it and the
  saved form remains clean.
* AC2: Capacity browser rendering has the expected package and work-order IDs/counts
  from successful actual browser GETs on real SQL Server.
* AC3: Every actual manager navigation entry has its exact expected heading,
  content/empty-state and successful relevant read contract; unexpected transport
  failures cannot pass. Cancellation reaches Staff time capture.
* AC4: Scoped regressions/static checks, SQL-backed browser and full API evidence
  pass; original Review is preserved and new single Review has no material open defect.
* AC5: After commit, complete full local gate with current-base receipt and separate
  final exact-head assessment before push/PR. No issue closure or live verification claim.

## Implementation Context Record

Research: .copilot-tracking/research/2026-10-28/capacity-page-523-correction-research.md
(executed, Ready). This automatic parent owns transitions. Implementation creates
.copilot-tracking/changes/2026-10-28/capacity-page-523-correction-changes.md.

## Sources

* Original capacity-page-523-review.md: RV-002/RV-003 and runtime gap RV-001.
* Correction research C1-C8/W1: current recovery, page and local gate contracts.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Correct recovery and browser proof

Dependency: critique disposition.

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Keep capacity retry read-only and draft-safe

Use the existing go/status closure without a mutation. Guard obsolete/session-ended
error rendering. Add the exact AC1 interaction to the canonical browser harness.
Exercise held refresh/retry navigation and 401 through this changed closure,
not only through initial-route loading.

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Prove manager destination/read/render success

Add route contracts, successful GET tracking, unexpected transport failure tracking,
capacity row proof and exact cancellation destination to the same harness.
Update owning README.

<!-- rpi:phase id=P02 -->
### [x] P02: Validate and review

Dependency: P01.

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Run scoped and heavy local validation

Run focused procurement tests, Node syntax, strict Ruff/format and API mypy.
Use explicitly authorized 60-second nonblocking heavy admission attempts, 40-minute
maximum. Run generated-demo --mssql browser and full API on owned local data.
Record per-route and failure/draft scenarios. Do not substitute SQLite for SQL.

<!-- rpi:task id=P02-T02 -->
#### [x] P02-T02: Reconcile and obtain one original independent Review

Reconcile all markers/evidence, then one independent Review for this new task.
Material findings route later; do not erase or rerun that Review.

<!-- rpi:phase id=P03 -->
### [ ] P03: Publish exact candidate

Dependency: P02, no material Review finding.

<!-- rpi:task id=P03-T01 -->
#### [ ] P03-T01: Commit, complete gate, verify and create PR

Resolve gh identity and configure only local privacy-safe email, include trailer.
Commit source and original dated RPI records. Run tools/rpi-checks.py --all with a
new external output and owned heavy admission. Fetch current main, verify receipt,
obtain separate exact-head publication assessment, push branch and gh pr create.
Keep authoritative final receipt and publication assessment external to avoid a
self-invalidating later evidence commit. Hosted and owner gates remain separate.

## Dependencies

Generated test fixture and installed source/dev distributions; real local SQL Server,
Chromium, required full-gate tools; heavy lock; unchanged current base/candidate.

## Test Ownership

* Canonical browser target: src/api/checks/capacity_browser_check.py; maximum two
  new helpers plus route-contract data and inline scenarios. No new test file,
  generated test target or production test export.
* Canonical HTTP regression: existing test_procurement_api and inherited SQL tests.
  Additions none; removals none; run existing legacy/empty and module suite.
* Semantic proof: real SQL browser row counts/IDs, route/read matrix and one
  persisted configure mutation with other unsaved form. HTTP regression separately
  preserves unknown contract binding and fail-closed writes.
* Inject only named failing GETs. Count actual POSTs and successful GETs; assertions
  must fail rather than print PASS after missing destination/read/content.

## Critique Disposition

| Finding | Disposition | Resolving evidence |
| --- | --- | --- |
| PC-001, Medium, original verdict Revise | Applied directly | P01-T01 and phase details now require recovery-origin cancellation and 401, exact destination/login, scoped injected failures, no late capacity reads/POST replay |

One critique executed. No repeated critique; no user decision required.

## Follow-Up Items

* Owner live verification after separately authorized deployment.
* Earlier RV-004/005/006 remain distinct UI/performance follow-ups.

## Handoff

P01 and P02 complete; PC-001 implemented and browser-proven. The one correction
Review is Complete / Conformant, no new findings. Real SQL/Chromium covers 1 package/601 orders, all
11 manager destinations, both draft retry scenarios and lifecycle isolation.
Full API PASS (1154 tests, 316 opt-in skips); full publication gate still required.
P03 stays unchecked until post-commit full gate/current-base verification and
independent exact-head assessment permit publication.
This committed checklist is the pre-publication evidence snapshot. Final receipt,
publication assessment and operational state remain external as specified by P03,
so recording them does not create a self-invalidating later candidate commit.

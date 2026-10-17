<!-- markdownlint-disable-file -->
# RPI Plan: Resident update and remedy controls

## Task Metadata

* Task ID: 88
* Slug: resident-update-remedy-controls-88
* Date: 2026-10-17
* Planning status: authorized correction ONE implemented/validated; external disposition pending
* Details: .copilot-tracking/details/2026-10-17/resident-update-remedy-controls-88-phase-details.md
* Critique: .copilot-tracking/reviews/plans/2026-10-17/resident-update-remedy-controls-88-plan-critique.md

## Executive Summary

Complete the existing resident-update record and add an independently owned remedy
status to existing service requests. Closing the response cannot close the remedy.
Keep delivery, handover and finance in their existing domain records.

Completed coordinator-authorized scope is the departed response-owner correction
under P01/P02. Add explicit manager-only versioned service/redress reassignment,
preserving captured owner history and all independent clocks. Original Review/
critique stay unchanged; no new full Review, base change or new policy authority.

### What You May Not Know

Handoff currently creates incomplete owner/date pairs. New commitments will instead
be recorded in the existing resident panel and preserved by handoffs. Old pairs
remain visible as unknown provenance until explicitly confirmed. Full PRD lease
governance and real operational acceptance are not established by these three criteria.

### Unresolved Decisions or Blockers

None in scope. Single critique returned Revise; PC-001 through PC-004 are resolved
by the explicit contracts below. No second critique.

## User Decisions and Requirements

* Complete actual ordered RPI phases, retaining one critique and one original Review.
* Exact issue criteria: purpose/owner/due/basis; independent response/remedy/defect/charge-query closure; each status has its own owner/date.
* Work solely on supplied main-based branch; no other dirty worktrees, #92 hold or unmerged source.
* Current named registered identities, writer-time validation, preserved captured provenance, explicit legacy unknowns and truthful persistence outcomes.
* No sending, paid AI, new IAM/Azure/spend, real approvals, private datasets or portal.
* Local installed-src validation and owned loopback SQL; commit/push/main PR, no merge/closure/rewrite.

## Goals

Make resident commitments actionable and retained; make closing one clock incapable
of erasing another open issue, including after reopen/return and process restart.

## Scope and Non-Goals

Existing resident actions, handoff creation compatibility, detail projection, minimal
existing-panel controls, tests/guides/KB and RPI artifacts. No quality/procurement/
finance domain redesign, general permission service or automatic controlled mutation.

## Functional Requirements

* Explicit full commitment create/revise/reassign with expected version, purpose,
  current owner identity, timezone-aware due date, supplied basis, safe-route reference
  or Unknown, Outstanding/Proposed state and original-history snapshots.
* Handoff preserves commitments; optional old update metadata cannot create incomplete new ones.
* Each new service request keeps existing response status and a separate remedy object
  with named owner, state, original open date, current status date and versioned history.
* Explicit remedy progress/resolve/close/reopen by its current named owner or resident
  manager; response reopen/close changes only response. Add charge-query and household
  dispute routes, not Legal answers. Legacy absent remedy/clock provenance is Unknown;
  explicit confirmation required before mutation.
* Restrict new reference/text fields to existing resident-view roles; contractor allowlist
  unchanged. No prompt payload changes.
* An existing resident-workflow manager can explicitly recover service or redress
  responsibility with current request version, eligible new named owner and reason.
  Capture old/new identities and actor/time without requiring a historical departed
  owner to remain eligible. Preserve complaint/review independence and remedy owner.

## Non-Functional Requirements

* Recheck actor, assigned identities, identity-bound decision rights, supplied date/version
  and current case state inside existing writer transaction. Preserve rowversion conflicts.
* Pre-COMMIT failure restores state/audit prefix before fallible reload. Post-COMMIT failure
  reports committed outcome and quarantines audit so retries cannot replay success events.
* Native labelled Fluent-foundation controls, inline live errors and keyboard access,
  no new animation or full WCAG claim.

## Acceptance Criteria

* Incomplete purpose/owner/date/basis or stale/missing owner refuses without mutation/audit.
* New/reassigned commitments retain history and do not imply messages sent/received.
* Response Closed with remedy Open remains visible through order completion, quality
  handover, financial note, case return/reopen and restart; defect/charge query independent.
* Each status retains its own named owner and server event date; legacy unknown dates
  and identities are never filled from today's actor.
* Current registry changes without case-sequence bump and concurrent writers are refused;
  audit/save/recovery and post-COMMIT faults produce truthful, non-replayed outcomes.

## Implementation Context Record

Research: .copilot-tracking/research/2026-10-17/resident-update-remedy-controls-88-research.md.
Changes: .copilot-tracking/changes/2026-10-17/resident-update-remedy-controls-88-changes.md
(created by Implement). Automatic parent continues after final critique dispositions.

## Sources

Research C1-C11/W1 and actual installed-src 59-test baseline (one opt-in skip).
Owner-selected Fluent/content/WCAG-baseline documents read; fresh web guidelines fetched.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Implement bounded resident controls

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Domain and persistence

Complete commitment/remedy actions, writer checks, rollback and unknown projections.
Completion evidence: actual failing-first failures, then 65 JSON/SQLite/HTTP tests
OK (two opt-in skips), including adverse writer/recovery and mixed closure tests.

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Existing web and HTTP journey

Wire existing resident forms and remove implicit handoff creation inputs; preserve routes.
Completed: actual authenticated Chromium create/reassign, response-only closure,
remedy close/reopen and response reopen; scoped controls retain inputs/live errors.
Correction ONE: core recovery/HTTP negatives and actual manager-only browser
recovery pass. Fresh guidelines and full changed-file read recorded in separate
correction evidence; existing unrelated web findings are not conformance claims.

<!-- rpi:phase id=P02 -->
### [x] P02: Validate and document

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Regression and real local SQL

Run focused and directly dependent writer/closure suites, Ruff/format/mypy, actual unique
loopback SQL probes, local browser and relevant image/non-root check.
Completed: 378 dependent regressions (five opt-in skips), 81 focused including
actual browser (one opt-in SQL skip), 11 actual MSSQL probes, configured full
core/API Ruff/format/mypy and final API image/container controls.

<!-- rpi:task id=P02-T02 -->
#### [x] P02-T02: Evidence and handoff

Update component guides, existing residents synthesis, KB route and append-only log;
reconcile plan/details/changes/state before one Review.
Completed: existing guides/resident synthesis, additive index route, exact upstream
log byte prefix plus append. Broader PRD/human acceptance explicitly not claimed.

Correction ONE completion: 145 resident/browser/handoff/report tests, 134 pass/
11 existing skips; 24 workflow/quality/hazard guards pass; eight targeted actual
MSSQL tests pass/no skips, final configured statics and JS syntax pass. Interrupted
broader replay is not a completed run. Original Review/critique unchanged;
separate correction receipt maps all three exact criteria to source/test proof.
Source/evidence published normally as5cfa8e53 on same PR392; final metadata
receipt follows without source changes. Independent final-head disposition remains
external and pending. No merge/issue closure.

## Dependencies

None issue-level; #81 hierarchy only. P01-T02 depends on P01-T01, P02 depends on P01.
Actual shared-file overlap expected: sqlstore.py save hooks/recovery (#91/#102),
store.py detail projection, finance.py payment-note owner/date, server.py and API panel. Do not touch quality.py,
assistants.py, progress.py or their pending fixtures. Coordinator owns main sequencing.

## Test Ownership and Evidence Lock

Core semantic tests extend existing test_resident_decisions.py (maximum 18 new methods)
and dedicated SQL subclass in that file; HTTP/browser extend test_resident_api.py
(maximum 5 new methods). Existing handoff tests amended for intentional creation change,
no removals. No generated dataset changes. Regression coverage reuses existing finance,
grant, stock, hazard, procurement, quality and workflow tests; do not duplicate fixtures.
Capture commands/counts and negative writer probes in changes evidence, not invented CI.
One unique owned loopback SQL container and UUID databases only. Existing migrated
lint/type exemptions remain; no blanket new exemptions.

## Final Contract Amendments

* PC-001: update_record doubles as explicit legacy confirmation, requires
  expected_version=0 for an unversioned/absent record and all complete fields.
  History retains the original raw snapshot, not reconstructed event time.
  remedy_confirm bootstraps an absent remedy with expected_version=0, supplied
  basis and current eligible owner; original opened_at/identity remain null.
  Confirmation records its own time and leaves even a Closed response untouched.
  Ordinary remedy actions refuse absent provenance until confirmed.
* PC-002: update and remedy assignees/writers use exact RESIDENT_VIEW_ROLES:
  Resident Liaison Officer, Retrofit Coordinator, Retrofit Programme Manager,
  Programme Support Officer. Only captured current owner or the two existing
  manager roles may revise/reassign/transition. Existing service/redress selection
  is restricted to these same actionable roles; independent-review restrictions
  retained. No new role or real delegation. Writer rechecks all subjects.
* PC-003: scoped ResidentCommittedError carries a trusted outcome from domain
  COMMIT to resident HTTP handling. After successful domain write, subsequent
  detail failure also returns explicit outcome=committed and reload/reconcile text.
  New scoped forms retain errors/input, forbid ordinary resubmit on committed
  outcome until reload. Original diagnostics logged/chained, not silently swallowed.
* PC-004: allocate one grouped mixed-state method (with mutually exclusive quality
  subcases) across JSON/SQLite/MSSQL. Canonical fields: request response
  status/status_owner/status_at; remedy status/owner/at/opened_at/history;
  quality defect owner/raised_at plus quality history, handover.by/at;
  work order completed_by/completed_at/history; finance payment status actor/time.
  Assert unchanged open remedy/defect/charge query and original history after
  every unrelated transition/restart; no substitution for absent owner/date.
  Group legacy confirmation, role/writer and HTTP faults within locked allowances.

## Critique Disposition

| Finding | Owner | Disposition | Resolving evidence |
| --- | --- | --- | --- |
| PC-001 High | planning parent | directly resolved | Final Contract Amendments legacy confirmation; P01-T01/T02, P02-T01 grouped regression |
| PC-002 Medium | planning parent | directly resolved | exact assignee/writer matrix and same writer-time checks |
| PC-003 High | planning parent | directly resolved | scoped domain/API committed outcome and projection-fault HTTP assertion |
| PC-004 Medium | planning parent | directly resolved | canonical field oracle and mixed-state grouped semantic test |

## Follow-Up Items

* Full PRD lease/scope-change and Housing/Complaints age-band governance remain
  outside exact issue criteria; no full AC-063/AC-089 acceptance claimed.
  Follow-up routing owner: planning parent/repository owner. Next action at the
  next parent #81 backlog triage: identify an existing separately owned governance
  item or assign one for Legal-reviewed lease positions, scope re-review and
  Housing/Complaints-approved bands. Professional policy approval stays with
  Legal/Housing/Complaints; no person, authority, threshold or item is invented.
  This addresses original Review RV-001's handoff without starting new work.

## Handoff

Implementation and original Review complete; Review execution Complete, outcome
Residual work, RV-001 separately routed above. Original Review retained unchanged,
no second Review or source correction. Independent final-head coordinator
acceptance is separate. Continue authorized publication, no human approval claimed.

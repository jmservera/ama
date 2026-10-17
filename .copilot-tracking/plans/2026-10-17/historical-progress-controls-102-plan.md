---
title: Historical progress controls 102 implementation plan
description: Bounded event-derived reporting and deterministic scenario forecast
ms.date: 2026-10-17
---

Task ID: 102. Slug: historical-progress-controls-102. Status: implementation-ready.

## Executive Summary

Add explicit progress mode to existing stats and case CSV report paths, leaving
current-state behavior intact. A shared read-only report normalizes existing
timestamped return/reopen and handoff events. Unknown clocks, missing source,
malformed records and contradictory transitions remain unresolved, not zero.
Forecasts simulate independent installation and QA pools from declared
synthetic assumptions; they are not capacity commitments or real outcomes.
No web edits, domain writer changes, AI service, SQL schema or migration.

## User Decisions and Requirements

* Execute Research, Plan/critique, Implement and one Review in this session.
* Preserve audit and domain events; never invent history from current snapshots.
* Reuse role permissions and source cohort filters; no other worktree reads.
* Exact issue criteria: event history; labelled forecast uncertainty/limits;
  export definitions/sources/denominators/exceptions and explicit as-of.
* Complete safe engineering even where missing domain evidence blocks complete
  historical or operational acceptance.
* Commit dated artifacts and own changes, push supplied topic, open PR Refs #102.

## Sources

Research artifact and C1-C11 in
.copilot-tracking/research/2026-10-17/historical-progress-controls-102-research.md.
PRD FR-022/023/024; BRD BG-011. Current BRD FR-022/023/024 numbering differs.

## Goals

Inspectable event intervals and conservative unknowns, reproducible scenarios,
and one consistent visible/export report contract.

## Scope and Non-Goals

Existing Store report paths, additive API routing, new dedicated tests and
directly related README/KB synthesis. Do not edit assistants.py, sqlstore.py,
shared fixtures, quality/procurement domain logic or web files.
Shared Store/API/docs overlap with #91/#92 is declared; coordinator integrates.

## Functional Requirements

* Require timezone-aware as-of and optional period start <= as-of; future
  as-of refused. Normalize UTC; exclude well-formed events after as-of.
* Cohort is selected using existing current-record filters and role rights.
  Declare that membership is selected now, not reconstructed historically.
  Report baseline/selected/excluded counts and exact case IDs/filters.
* Normalize exact return/reopen and handoff states, retaining source locator,
  version and role-safe actor/source status; do not expose notes, identities,
  reasons, commercial amounts or raw references to roles without a need.
* Derive stage intervals only between consistent timestamped stage transitions;
  first entry, missing transitions, simultaneous conflicts and broken chains
  yield unknown duration with exceptions. Paused stage intervals remain
  separate. Returns and reopenings never collapse to completion.
* Handoff elapsed time derives only from an observed offer and terminal state;
  receipt never establishes acceptance or ownership. Unsupported legacy events
  are reported unknown. Narrative never establishes operational history.
* Forecast inputs declare eligible cohort count, capacity, dependency/resource
  assumptions, horizon and stage duration; strict bounded positive integers.
  Use EXA-009 two sequential independent resource pools; show capacity-one/
  central/two-week/three sensitivities, uncertainty not statistical confidence,
  missing/stale evidence and accepted-handover outcome as scenario only.
* CSV encodes the exact report contract with typed rows/JSON cells, including
  metadata, definitions, sources, denominators, assumptions and exceptions.
  Empty cohorts/history are explicitly unresolved, not success.

## Non-Functional Requirements

No persistence writes; Store lock refresh preserves SQL consumers. No change
to audit hashing, lifecycle authority, consent or approvals. Default deny
contractor/unknown roles; allow-list output fields independent of raw records.
No paid model/provider. Baseline does not assert absence of AI programme-wide.

## Acceptance Criteria

1. Known fictional return/reopen/pause/handoff events produce exact elapsed
   seconds and ordered source locators; gaps/legacy/malformed contradictions
   produce nulls and explicit exceptions.
2. Identical declared scenario inputs reproduce exact cumulative outcomes,
   labelled Forecast with assumptions, uncertainties and data limits.
3. Visible and exported report agree on as-of, period, cohort/denominators,
   sources, exceptions and approval status; sensitive sentinels never appear.
4. Existing stats/CSV default behavior and audit bytes remain unchanged.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### P01: Report baseline

Status: Complete.

* [x] P01-T01: Add typed pure history/scenario/report/CSV helpers.
* [x] P01-T02: Wire Store lock/filter adapter and existing API report mode.

<!-- rpi:phase id=P02 -->
### P02: Evidence and validation

Status: Complete.

* [x] P02-T01: Add owned tiny fictional domain/HTTP/persistence tests.
* [x] P02-T02: Run local focused tests, configured lint/format/mypy, actual
  uniquely named loopback MSSQL consumer tests, build/non-root image behavior.
* [x] P02-T03: Update related component and existing KB synthesis/index/log.

<!-- rpi:phase id=P03 -->
### P03: Review and publication

* [x] P03-T01: Execute one full Review and retain original adverse findings.
* [x] P03-T02: Correction ONE resolves concrete RV-001/RV-002 with failing-first
  and targeted final evidence; no second full Review, no Correction TWO.
* [ ] P03-T03: Fresh GitHub identity, own-only commit, push and main PR.

## Validation Ownership and Change Budget

Canonical new tests: src/core/tests/test_progress_reports.py and
src/api/tests/test_progress_report_api.py. Maximum additions: these two test
files plus one dedicated local MSSQL adapter if needed. Exact removals: none.
Generated committed targets: none. Existing shared fixture files unchanged.
Semantic tests cover malformed/contradictory inputs, event clocks, pause/reopen,
forecast queues and role projection. Regression tests cover legacy stats/CSV,
immutable ledger, SQLite refresh/reopen and real MSSQL read consumers.
Commands follow src project READMEs, pip editable local packages first.
No PYTHONPATH=mvp; no browser required without web asset changes.
Unperformed environment checks must be separately marked, never passed.

## Critique Disposition

One independent final-candidate critique executed. Verdict: correction required.
PC-102-001 applied: explicit staff-only direct/HTTP authorization.
PC-102-002 applied: exact source-backed kinds/states and pause labels; Completed
is allowed as the source-defined reopen origin, not a pause or accepted outcome.
PC-102-003 applied: canonical versioned report/CSV serialization and byte tests.
All are planner-owned compatible corrections; no unresolved human decision.
Critique artifact:
.copilot-tracking/reviews/plans/2026-10-17/historical-progress-controls-102-plan-critique.md.
No second critique.

## Follow-Up Items

Source-authorized complete forward-event capture and owner-approved operational
capacity/forecast validation remain outside this read-only report task.
Programme/Data owns prospective event dictionary/capture; Programme/Finance/QA
owns verified resources/dependencies/calibration. Coordinator owns shared
integration and independent final-head acceptance. These are not source
approval or full historical completeness claims.

## Handoff

Details: .copilot-tracking/details/2026-10-17/historical-progress-controls-102-phase-details.md.
Changes: .copilot-tracking/changes/2026-10-17/historical-progress-controls-102-changes.md.
Ready after critique dispositions are resolved.

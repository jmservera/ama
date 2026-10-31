---
title: AI metering Copilot threads implementation plan
description: Five bounded source corrections for PR 602
ms.date: 2026-10-31
---

Task: 432-copilot-threads / ai-metering-432-copilot-threads.

## Executive Summary

Preserve shared document-call admission, validate report periods without SQL,
and make human rejection independent of incomplete financial attribution.
Keep acceptance/dispatch fail-closed and reports Unknown for unresolved joins.
Source-only correction, not whole-issue or human/live financial acceptance.

## User Decisions and Requirements

* Continue branch feat/ai-metering-432 and PR #602; pull first, merge main,
  use main rubric if conflicted. Both completed without conflict.
* Fix five unresolved threads, including the priority path, with regressions.
* Run core/API unit tests, Ruff and mypy. CI is the gate; do not wait for
  the complete local gate.
* Commit with requested Copilot trailer, push without force, retain Refs #432,
  reply to and resolve all five threads.
* Pip only; no secrets, paid calls, or private data.

## Sources

Research: .copilot-tracking/research/2026-10-31/ai-metering-432-copilot-threads-research.md
(C1-C7, W1-W5). Original RPI evidence remains unchanged.

## Goals

Bound all calls and preserve human withdrawal without misreporting economics.

## Scope and Non-Goals

Core AI/consumption/legacy/assistant review, API JSON reporting, existing focused
test modules and related README/knowledge-base notes. No UI, schema migration,
deployment, financial authority, issue closure or broader attribution project.

## Functional Requirements

* look_at uses CURRENT when present; only standalone calls get a document root.
* Report timezone/exclusive-period/as-of validation precedes SQL branching.
* Unlinked legacy/priority reject writes intent and human review; acceptance
  still fails, and original missing output remains recoverable and incomplete.
* Unlinked metered assistant reject creates an ineligible link and disposition
  in its authoritative transaction, without modifying existing eligibility.
* DispatchHeld during assistant rejection writes explicit unresolved financial
  metadata atomically with withdrawal. Reporting excludes unresolved outputs
  from acceptance and reconciliation, including after scan capacity recovery.

## Non-Functional Requirements

Use closed content-free immutable ledger events and existing authorisation/
revision/transaction controls. Catch only safe DispatchHeld, never arbitrary
database errors. Keep read/dispatch limits unchanged; no silent skip or refund.

## Acceptance Criteria

Five thread-specific regressions prove provider call/depth thresholds,
400 validation under SQL/JSON/unavailable schema, persisted unlinked rejection
on both legacy stores, pending-provider assistant rejection, and over-capacity
accepted-proposal withdrawal with Unknown economics after read recovery.
All targeted/core/API and static checks pass; committed/pushed candidate and
five resolved threads are verified.

## Phase Checklist

<!-- P01 -->
### P01: Source corrections and regressions

* [x] P01-T01: Preserve document context and centralise report-period validation.
* [x] P01-T02: Allow orphan legacy reject intent/disposition; atomic assistant
  ineligible linkage; closed unresolved withdrawal marker/report handling.
* [x] P01-T03: Update related tests and documentation.

<!-- P02 -->
### P02: Validation, review and publication

* [x] P02-T01: Run focused then core/API unit tests and Ruff/mypy.
* [x] P02-T02: One independent post-implementation Review; preserve outcome.
* [ ] P02-T03: Commit and non-force push; reply/resolve and verify five threads.

## Test Ownership and Candidate Lock

Canonical tests: src/core/tests/test_ai_consumption.py and
src/api/tests/test_ai_consumption_api.py. No generated targets or removals.
Update the existing output-link fault expectation for rejection; add at most
eight focused methods. Cover semantic behavior with actual local HTTP and
persisted SQL/JSON, plus exact meter threshold/as-of regressions.
Validate full component suites with their existing opt-in skips unchanged.

## Critique Disposition

Execution: complete, once. Original verdict: Revise (three High, one Medium).
Artifact: .copilot-tracking/reviews/plans/2026-10-31/ai-metering-432-copilot-threads-plan-critique.md.

* PC-001 applied: new closed review-orphan root/output/time association leaves
  v1 event shapes unchanged. Cohort review gaps union pending intents and
  missing original orphan links, de-duplicated by output. Both legacy callers
  supply authoritative root; original output repair removes its gap.
* PC-002 applied: one bounded snapshot stages immutable-link and disposition
  checks before writing assistant ineligible link/review. Catch DispatchHeld
  only around metering, before authoritative task update. Arbitrary event/
  SQL failures roll back all writes. Exact-capacity regression required.
* PC-003 applied: review-unresolved fields are root/output/action/at/reason/
  authoritative task revision. Reject markers dominate financial acceptance
  at equal timestamps, only at/before cutoff and in the call-root cohort.
  Distinct outputs count once; markers remain sticky across reads/restarts/
  repeated reviews. No automatic clearing or guessed financial revision.
* PC-004 applied: eight-method allocation recorded in details; existing
  fault-matrix and HTTP tests extended without removal or rename.

Planner readiness: Ready after direct dispositions. No divergent user decision
or second critique. Original critique preserved.

## Follow-Up Items

Historical/resident attribution, OD-51/Finance/paid held-out evidence remain
outside scope as recorded by original #432 research. Do not close issue #432.

## Handoff

Details: .copilot-tracking/details/2026-10-31/ai-metering-432-copilot-threads-phase-details.md.
Changes record (implementation-owned):
.copilot-tracking/changes/2026-10-31/ai-metering-432-copilot-threads-changes.md.

P01 source/testing/documentation and P02-T01 validation complete. Review-ready
boundary is those completed tasks; P02-T02 independent Review and P02-T03
publication remain pending, not inferred from local checks.

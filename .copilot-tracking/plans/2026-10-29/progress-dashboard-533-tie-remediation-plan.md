<!-- markdownlint-disable-file -->
# RPI Plan: Bounded mixed-source lifecycle remediation

## Task Metadata

* Task ID: 533-tie-remediation
* Task slug: progress-dashboard-533-tie-remediation
* Date: 2026-10-29
* Parent task: 533-correction4
* Scope: bounded implementation of original Review RV-001 and RV-003.
* Details: .copilot-tracking/details/2026-10-29/progress-dashboard-533-tie-remediation-phase-details.md
* Status: Source and scoped validation complete; local commit pending.

## Executive Summary

The original correction completed Research, Plan, Implement and independent
Review. Its original Complete / Not accepted outcome remains unchanged.
RV-001 identified a tightly coupled ambiguity: flattening equal-instant events
from separate collections can manufacture adjacency, allowing duplicate
suppression to erase possible episodes. RV-003 found final-snapshot-confounded
tests for closing-to-return transitions.

This bounded implementation completes the user's requested sibling-sequence
correction rather than knowingly leaving these related defects. It is not a
second critique or Review and does not claim independent acceptance afterward.
Full suites/browser remain blocked by the same busy-lock admission; no retry.

### What You May Not Know

Without cross-collection order or event identity, multiple same-instant closes
and reopens can mean either repeated observations or separate episodes.
The safe result is Unknown, not an arbitrary source-concatenation order.
Single-stream ordered episodes and unambiguous duplicate/corroborating evidence
remain supported.
Implementation now retains collection provenance and complete observation
fields (excluding normalized timestamp spelling) until replay. Ambiguous
mixed-source ties and distinct versions cannot become proven duplicates.
All 77 targeted tests and strict static checks pass; no independent
re-review or full/browser acceptance is claimed.

## User Decisions and Requirements

* Preserve lifecycle kinds, reject incomplete/contradictory histories and cover
  sibling transitions within the user's complete correction scope.
* JSON and SQLite regressions, local Conventional Commits and required trailer.
* No push, az, force-push, closing keywords or heavy-lock bypass.

## Goals

Eliminate the remaining known-history ambiguity without inventing ordering.
Make the illegal closing-to-return tests independently sensitive to that guard.

## Scope and Non-Goals

Only the existing three source/doc targets and dated remediation evidence.
No new schema, event identity, stream-order inference, dataset or UI change.
No repeated Research, critique or Review; supplied original Review is adequate
evidence for this bounded subsequent implementation.

## Functional Requirements

* Retain collection provenance while reconciling equal-instant events.
* Where several collections contain opposing close/reopen events and repeated
  lifecycle evidence, classify as unknown rather than assume duplicates.
* Preserve single-stream alternating same-instant episodes, safe same-instant
  closing corroboration and simple cross-source close/reopen with no repetition.
* Same-kind duplicate observations must also agree on remaining evidence fields,
  including versions; equal kind/time alone cannot prove distinct records equal.
* Return never changes the snapshot's closed flag, including in illegal
  closing-to-return matrix fixtures.

## Non-Functional Requirements

Strict existing typing/lint/format; no dependency or suppression changes.
Linear equal-instant reconciliation after existing sorting.

## Acceptance Criteria

* Persist JSON/SQLite cases for repeated accepted/controlled-reopen and
  human-closure/controlled-reopen ties, before and after a later final closure.
* Cover mixed closing aliases at a reopen instant, mixed original
  identification/reopen ambiguity and safe cross-source controls.
* Raw payload, known/unknown coverage, historical counters/durations and both
  archive filter assertions remain exact through the existing helper.
* A->T/C->T fixture closed=True, so ignoring T cannot pass via snapshot mismatch.
* Focused red/green and API/core static checks; targeted fallback only,
  heavy validation remains blocked and no repeated lock admission.
* Keep original Review immutable; report remediation without claiming a fresh
  conformant independent verdict.

## Sources

* .copilot-tracking/reviews/logs/2026-10-29/progress-dashboard-533-correction4-review.md: RV-001/RV-003 resolving evidence and RV-002 validation boundary.
* Original correction research/plan/details/changes and current component tests.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [ ] P01: Resolve ambiguity and coverage confounding

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Add persisted regressions and fix return fixture flags

Expand existing inherited methods/helpers only, no removals or new test method.

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Reconcile mixed-source timestamp ties before replay

Retain collection source and reject indistinguishable duplicate/episode
interpretations; document the conservative boundary in the API README.

<!-- rpi:task id=P01-T03 -->
#### [ ] P01-T03: Validate and commit local remediation evidence

Run API/core mypy/Ruff and targeted units; no heavy retry or second Review.
Commit source plus original Review and closeout artifacts with required trailer.
Validation done: final 77 tests pass; API/core mypy/Ruff pass. Remaining action
is the local source/evidence commit and state closeout only.

## Critique Disposition

No new critique: bounded later implementation directly resolves existing
RV-001/RV-003. The original Complete / Revise critique remains immutable.

## Follow-Up Items

* RV-002: full suites/browser at later explicit heavy-lock coordination.
* No fresh independent acceptance is claimed for this subsequent amendment.

## Handoff

Direct bounded implementation; stop after local commits. Original Review
outcome and exact assessed source candidate remain unchanged.
No remaining source work. Full/browser validation and independent acceptance
remain open, rather than relabeling the original Review conformant.

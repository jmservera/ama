---
title: Regulatory audit snapshot plan
description: Local-only correction for issue 208 and PR 506
ms.date: 2026-10-29
---

Task ID: 208-audit-snapshot. Slug: regulatory-audit-snapshot-208.
Baseline: 4998090e900082c34bac964d900e919a3f972430.

## Executive Summary

Read only the captured audit-file window, not later appends. Add one
deterministic real-file regression, preserve existing tail behavior, document
the boundary and run focused core tests plus component Ruff lint/format.
One independent critique precedes implementation; one independent Review
follows it. Delivery is a local commit only, not publication.

## User Decisions and Requirements

* Fix the review finding in regulatory_chat.py using read(size-start).
* Add a regression for a below-256-KiB snapshot crossed by a concurrent append.
* Complete research, plan, implement and review with dated tracking artifacts.
* Use feat/regulatory-assistant-208 for issue #208 / PR #506.
* Run focused src/core tests, ruff check and ruff format --check.
* Commit locally using Conventional Commits and required trailer; no push,
  az or hand edits of .github/rubric/scores/latest.json.

## Sources

Research: .copilot-tracking/research/2026-10-29/regulatory-audit-snapshot-208-research.md,
C1-C5. Details: .copilot-tracking/details/2026-10-29/regulatory-audit-snapshot-208-phase-details.md.

## Goals

Prevent later appends entering a captured JSON audit snapshot.

## Scope and Non-Goals

Change regulatory_chat.py, test_regulatory_chat.py and the existing core README
paragraph. No SQL, API, UI, schema, corruption-recovery or deployment changes.
Full publication gate is deferred because no push/publication is requested;
these focused checks are not a full-gate receipt or human approval.

## Functional Requirements

Read exactly size-start bytes and retain existing truncation, actor/role/day
filtering and explicit malformed-audit error behavior.

## Non-Functional Requirements

Keep the 262144-byte bound, no locks/retries or sleeps, constructed fixtures
only, no private data, and no new dependencies.

## Acceptance Criteria

* A real-file regression captures size below MAX_BYTES then appends complete
  valid JSONL beyond MAX_BYTES immediately before read.
* Original code fails on partial JSON; corrected code succeeds, requests the
  captured byte count and returns the pre-append summary.
* A subsequent unpatched read succeeds with bounded_partial coverage.
* Existing JSON/SQL tests pass, including byte/position truncation and restart.
* Component Ruff lint and format checks pass and git diff --check is clean.
* One independent critique and Review are recorded; no human/hosted/full-gate
  approval is implied.

## Phase Checklist

<!-- P01 -->
### P01: Snapshot correction

* [x] P01-T01: Add one deterministic regression and record original-code failure.
* [x] P01-T02: Change read length and update existing component documentation.
* [x] P01-T03: Validate and reconcile implementation evidence before Review.

P01 complete: original-code red, 29 focused tests green, component Ruff
lint/format and diff checks passed. No implementation blockers or follow-ups.

## Test Ownership and Locked Boundary

Canonical test owner: RegulatoryTests in src/core/tests/test_regulatory_chat.py.
Removals: none. Maximum additions: one test method, no shared helper file.
Use wrapped real binary file and an injected read side effect. Assert semantic
summary equality and exact read length; existing tests own SQL and tail cases.
Generated targets: none. Validation: focused regulatory modules and whole
src/core Ruff check/format. Keep original red and green evidence in changes.

## Critique Disposition

Single independent critique Complete / Pass, no PC-xxx findings.
Original evidence: .copilot-tracking/reviews/plans/2026-10-29/regulatory-audit-snapshot-208-plan-critique.md.
No significant/divergent decisions or plan corrections required.

## Follow-Up Items

None identified within scope. Publication remains prohibited by user direction.

## Handoff

Implementation complete and reconciled; ready for one independent Review.
Changes destination: .copilot-tracking/changes/2026-10-29/regulatory-audit-snapshot-208-changes.md.

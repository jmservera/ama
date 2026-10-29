---
title: Issue 130 PR 509 fix cycle 1 plan
description: Surgical resident status and nomination identity corrections
ms.date: 2026-10-29
---

Task ID: issue-130-pr-509-fix-cycle-1.

## Executive Summary

Separate decision validity from tenure readiness without releasing the tenure
hold. Preserve nomination identity across retention deletion with fresh opaque
UUID-based identifiers, including already-deleted legacy records. Add JSON/SQLite regression
coverage, run requested checks and one independent Review, then commit locally.
Implementation Review Complete / Conformant with justified divergence, no
substantive findings. Requested checks pass. Local commit remains.
Original critique Complete / Revise and direct dispositions are preserved.

## User Decisions and Requirements

* Full dated RPI loop for Refs #130, PR #509 fix cycle 1.
* First git pull --rebase: complete, already up to date.
* Source in src/ only; tests outside package; no Azure or latest.json edits.
* Preserve accepted decision status and priority after tenure intake, with hold.
* Reject deleted nomination corrections against recreated intake.
* Validate Ruff check/format, mypy and relevant unittest modules from src/core
  using /tmp/mv and PYTHONPATH=src:tests:../agents/src:../agents/tests.
* Commit locally with required Copilot trailer; no push or issue closure.

## Sources

Research: .copilot-tracking/research/2026-10-29/safety-consent-130-fix-cycle-1-research.md,
C1-C7. Details:
.copilot-tracking/details/2026-10-29/safety-consent-130-fix-cycle-1-phase-details.md.

## Goals

Correct both supplied failure sequences without expanding intake authority or
changing unrelated ranking/consent/retention semantics.

## Scope and Non-Goals

Runtime scope: src/core/src/zava_forward/core/resident_decisions.py.
Tests: src/core/tests/test_resident_decisions.py and one existing API fixture
updated to use the returned opaque identifier. Related documentation:
src/core/README.md. No schema/service/action/version changes, SQL Server/Azure,
web edits, operational acceptance, full publication gate, push or merge.

## Functional Requirements

* resident_status checks current decision scope, retention, review and
  representative authority independently of tenure readiness.
* resident_gate continues to return the same case-wide/scoped tenure hold.
* New nominations use NOM- plus a full random UUID hex identity, independent of
  deletable history and missing legacy counters. Versions begin at 1.
* Existing sequential IDs remain usable for current records and corrections.
  New IDs are opaque and supplied by creation, not reconstructed by clients.
  Deletion and its non-personal tombstone remain unchanged.
* Old corrections fail explicitly before mutation; valid new corrections work.

## Non-Functional Requirements

Reuse existing transaction/replay/rollback and JSON/SQLite persistence.
Keep existing record IDs readable, no new personal retention, dependency or
generated output. Current human/legal/participant acceptance remains unmet.

## Acceptance Criteria

1. With current accepted decisions, tenure intake/reopen leaves status Accepted
   and complete heuristic suggestions/order/reasons/citations identical.
2. Both case and scoped resident gates still hold; stale/expired/review-needed
   and representative decision safeguards continue to pass existing tests.
3. Delete a legacy NOM-1 at version 1, reopen, create a new nomination at
   version 1 with a different ID; the stale correction raises ValueError and
   changes neither the new record nor audit. Verify a valid new correction.
4. Repeat deletion/recreation and start from an already-deleted legacy
   tombstone without any counter; no deleted identity matches a replacement.
   Failure/rollback of new intake cannot cause later ID reuse.
5. Requested static checks and relevant test modules pass; skips are explicit.
6. Original critique/Review preserved, all dated artifacts and source committed
   locally with noreply attribution and required trailer; no push.

## Test Ownership and Locked Coverage

Owner: core tests outside the package. Remove none. Add at most three methods
in JsonResidentDecisions, inherited by SqlResidentDecisions (and opt-in MSSQL).
Canonical target is the shared test file; no generated test/output target.
Update the two existing core/API NOM-1 fixtures to use returned IDs; remove
no assertion or test. Add semantic exact heuristic equality and legacy-delete/recreate/stale-write
regressions, not only format or ID-pattern proxies. Existing intake and
authority/retention suites supply regression coverage. Relevant modules:
test_resident_decisions, test_hazard_referral, test_consultation_controls,
test_quality_procurement, test_dependency_rule. Verify actual module paths
before execution. Also run the affected API resident module with this worktree's
api/src and api/tests ahead of installed editable paths. Static commands from src/core: /tmp/mv/bin/ruff check .;
/tmp/mv/bin/ruff format --check .; /tmp/mv/bin/mypy.

## Phase Checklist

<!-- P01 -->
### P01: Regression and implementation

* [x] P01-T01 Add bounded regressions and record their original failures.
* [x] P01-T02 Extract decision-only gate, use UUID nomination IDs and document.

<!-- P02 -->
### P02: Validation and evidence

* [x] P02-T01 Run exact requested static checks and relevant unit modules.
* [x] P02-T02 Reconcile changes/details and hand off to independent Review.

<!-- P03 -->
### P03: Review and local commit

* [x] P03-T01 Execute one independent Review; route any findings, no second loop.
* [ ] P03-T02 Finalize state/evidence and commit locally with trailer.

## Critique Disposition

One independent critique: Complete / Revise, preserved at
.copilot-tracking/reviews/plans/2026-10-29/safety-consent-130-fix-cycle-1-plan-critique.md.

| Finding | Disposition and resolving evidence |
| --- | --- |
| PC-001 High | Accepted failure mode; replace counter proposal with full UUID identities. User explicitly permits a non-reused identity, not only counters. Sequential IDs were planner preference, not confirmed owner constraint. Add already-deleted legacy test. |
| PC-002 Medium | Resolved by design: no new deletion counter or persistence invariant. UUID issuance is independent of deletion success/retry. Existing intake rollback test plus a failed post-deletion creation exercises the changed boundary. Do not repair unrelated pre-existing deletion transaction behavior. |
| PC-003 Medium | Resolved by design: no tombstone changes; existing exact privacy assertions remain intact. |
| PC-004 Medium | Rejected: no /tmp prohibition exists in parent runtime instructions; user explicitly requires /tmp/mv. Tools successfully report Python 3.12.3, Ruff 0.17.1 and mypy 2.4.0. Do not follow worker-only unsupported restriction. |

No unresolved significant user decision; no second critique. The research's
initial count recommendation is superseded by this safer legacy-compatible
design, with no new authority or service.

## Follow-Up Items

Existing human/operational acceptance and publication/hosted gates remain
outside this local fix cycle. No automatic child work.

## Handoff

Changes path:
.copilot-tracking/changes/2026-10-29/safety-consent-130-fix-cycle-1-changes.md.
Block on failed required validation or material Review findings. Do not claim
final-head publication acceptance; no publication is requested or authorized.

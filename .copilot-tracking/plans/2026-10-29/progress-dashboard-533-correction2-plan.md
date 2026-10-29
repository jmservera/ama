---
title: Progress dashboard correction round 2 plan
ms.date: 2026-10-29
---

Task: 533-correction2-2026-10-29. Status: implemented/validated; independent Review pending.

## Executive Summary

Reject malformed auxiliary lifecycle evidence as unknown and reuse extracted
deadline-only queue evaluation for dashboard overdue counts. Preserve valid
replay, queue row provenance and all UI contracts. Commit locally after strict
checks, backend regressions, progress browser check and independent Review.

## User Decisions and Requirements

* Full RPI loop on feat/progress-dashboard-533, open PR #540, Refs #533 only.
* First git pull --rebase completed, fast-forward to 7bda02a8.
* Fix both supplied findings with JSON/SQLite regressions and previous-behavior parity.
* Source in src; no push, az, force-push or historical evidence replacement.
* Run mypy, ruff check . and ruff format --check . inside API and core.
* Unit/browser imports must prioritize this worktree's src and shared test fixtures.
* Full suites require flock -n /tmp/ama-rpi-heavy.lock; busy means targeted fallback.
* Use /tmp/mv tools; missing browser dependency was observed, so restore only if needed.
* Conventional Commits with requested Copilot trailer; stop after local commits.

## Sources

.copilot-tracking/research/2026-10-29/progress-dashboard-533-correction2-research.md,
C1-C7. Prior correction evidence remains unchanged.

## Goals

Prevent one malformed synthetic case aborting either read and remove full
work-context/building membership evaluation from dashboard overdue counting.

## Scope and Non-Goals

progress.py, core taskqueues.py, their existing semantic tests, API README.
No Store/schema change, new dependency manifest, UI edit, benchmark timing
claim, cloud, publication or whole-PR acceptance.

## Functional Requirements

* Both auxiliary collections must be lists of dictionaries before replay.
  Missing keys mean []; explicit null, scalars, mappings and malformed entries
  mean None lifecycle, including malformed irrelevant rows.
* Unknown cases remain admitted and counted in unknown lifecycle/closure coverage;
  unbounded archive includes them with null date, date filters exclude them.
* Extract overdue_tasks(case, *, as_of, handoff) returning the same ordered
  structured rows; context and dashboard share it. Dashboard passes handoff_view
  without building full context. No building or return narrative dependency.
* Preserve strict deadline/completion/snapshot behavior, owners, source/version,
  released hazards and pending handoff semantics.

## Non-Functional Requirements

Strict types without new exemptions; no broad catches or duplicated clock logic.
No per-open-case building scan; deterministic call-avoidance tests, not flaky
wall-clock thresholds. Overall work scales with case-local evidence.

## Acceptance Criteria

* JSON and SQLite persistence/reopen tests for both fields, malformed collections
  and entries, valid empty/missing/dictionary rows; both endpoints remain readable,
  valid sibling totals unaffected and unknown-date semantics exact.
* Malformed returns on an open synthetic case do not abort dashboard.
* Dashboard overdue count equals previous store.work_context count for registered
  building cases and varied hazards, resident updates and handoffs; no full
  context or building.record call on the new read.
* Core frozen expected rows and existing queue tests preserve all clock boundaries.
* API/core mypy, lint, formatting plus units and progress browser checks executed;
  actual failures, unavailable prerequisites or busy-lock fallback explicitly recorded.
* One final-candidate critique and one independent post-implementation Review,
  dated artifacts committed locally; no publication claim.

## Test Ownership and Change Budget

Canonical semantic owners: API test_progress_dashboard.py and core test_taskqueues.py.
No test/assertion removals. At most four new inherited API methods and two core
methods. Reuse building_fixture; generated logs/browser reports external only.
Regression checks prove persistence, unknown counts, parity and call avoidance;
core semantic checks compare exact rows so shared-helper parity is not circular.

## Phase Checklist

<!-- P01 -->
### P01: Lifecycle validation

* [x] P01-T01: Add strict collection guards, inherited JSON/SQLite tests and docs.

<!-- P02 -->
### P02: Clock-only overdue evaluation

* [x] P02-T01: Extract/reuse helper and add exact clock/parity/call-avoidance tests.

<!-- P03 -->
### P03: Validation and Review

* [x] P03-T01: Run targeted red-green, required static checks, lock-admitted full suites or targeted fallback, and progress browser check.
* [ ] P03-T02: Reconcile evidence, commit implementation, obtain one independent Review and commit original Review/closeout locally.

P01 and P02 are logically independent; both precede P03 validation/Review.

## Critique Disposition

One independent final-candidate critique: Complete / Pass, no findings.
.copilot-tracking/plans/2026-10-29/progress-dashboard-533-correction2-critique.md.
No significant/divergent decision needed. Open-return endpoint regression is
judged after both P01 and P02, as explicitly noted by the critique.

## Follow-Up Items

Human accessibility and any later exact-head publication gates remain separate.
No source defect outside the two caller findings is included.
Browser axe reports zero violations in eleven states; dashboard/recovered-dashboard
color-contrast incompletes still require human assessment. API/core discovery
passed with 316/190 opt-in/integration skips, not full integration acceptance.

## Handoff

Details: .copilot-tracking/details/2026-10-29/progress-dashboard-533-correction2-phase-details.md.
Changes destination: .copilot-tracking/changes/2026-10-29/progress-dashboard-533-correction2-changes.md.
P01/P02 and P03-T01 complete: 49 focused tests, API/core discovery, strict static
checks and progress browser passed. Changes/details reconcile environment and
discovery-order refinements. P03-T02 remains for local implementation commit,
one independent Review and original Review/closeout commit; no push.

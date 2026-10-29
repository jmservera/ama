---
title: Progress dashboard correction plan
ms.date: 2026-10-29
---

Task: 533-correction-2026-10-29. Slug: progress-dashboard-533-correction.
Status: implementation complete; validation reconciled; independent Review pending.

## Executive Summary

Guard malformed history as unknown, and carry structured date-range validation
through the existing API reasons channel to linked native field errors. Keep
actual read failures as page alerts/retry. Validate local current-source tests,
real browser interactions and pinned axe; commit locally without publication.

## User Decisions and Requirements

* Fix the two supplied PR #540 findings, Refs #533, without a closing keyword.
* Use feat/progress-dashboard-533 in this worktree; source in src, not mvp.
* Execute Research, Plan, Implement and Review with dated committed artifacts.
* No push, az or force-push. Conventional Commit plus requested Copilot trailer.
* Run API unit tests, progress browser check and axe, with nonblocking heavy lock for full suites and targeted-only fallback if busy.
* Requested journey venv is absent; use existing /tmp/ama-533-venv with current worktree src and disclose.
* Refresh scenario-manifest SHA-256 pins only if pinned files are edited.

## Sources

.copilot-tracking/research/2026-10-29/progress-dashboard-533-correction-research.md
(C1-C7, W1); design-system.md field contract and existing public constructed fixtures.

## Goals

One malformed synthetic case cannot fail either read; range errors identify and
focus relevant fields without labelling unrelated service failures as invalid input.

## Scope and Non-Goals

progress.py, progress.js, narrowly scoped server serialization, existing progress
unit/browser checks and API README. No shared app rewrite, dataset change, visual
redesign, archive range cap, unrelated busy-state work or publication gate.

## Functional Requirements

* A non-list history returns unknown lifecycle; retain synthetic admission and coverage semantics.
* Reversed dashboard/archive and over-366-day dashboard ranges use a dedicated ValueError subtype.
* Serialize only that exception with reasons.fields = ["start", "end"]; existing API forwards reasons/status.
* Mount a .field-error text adjacent to each affected date input, assign unique IDs, aria-invalid and aria-describedby, and focus the first field after show().
* Actual read failures and unrelated validation errors retain alert/retry without invalid dates.
* Corrected filters replace errors, remain URL-backed, and restore ordinary results.

## Non-Functional Requirements

Native semantics and existing warning styles, plain corrective text, no duplicate
client date algorithm or message parsing. No new runtime/tool dependency; no private
dataset, cloud or live model. Preserve date defaults and inclusive maximum.

## Acceptance Criteria

* Null and representative non-list history values yield identical unknown-lifecycle dashboard counts and archive unknown dates/exclusion under date filters, JSON and SQLite.
* HTTP range errors contain field metadata; unrelated 400s do not.
* Real browser asserts visible linked errors on both date inputs, aria-invalid, first-field focus, retained values, submit correction and clearing for reversed dashboard/archive and oversized dashboard.
* Defaults (omitted end) and inclusive 366-day dashboard boundary remain server-authoritative; wide archive ranges remain valid.
* Browser asserts 503 and unrelated 400 failures leave fields valid; pinned axe covers error states and recovered pages.
* Relevant tests/checks and diff checks pass, or exact blockers/lock fallback are reported honestly.
* One independent critique and one post-implementation Review are preserved; commits local only.

## Test Ownership and Change Budget

Canonical semantic owner: test_progress_dashboard.py; extend its inherited
JSON/SQLite class and HTTP test. Canonical browser owner:
checks/progress_browser_check.py. No new test file or removed test/assertion.
Maximum additions: two unit test methods (inherited across both backends), inline
HTTP assertions and six browser range scenarios plus service/400 assertions.
Generated targets: external logs/axe reports only. Manifest pins checked; no planned
pinned source edit. New production error metadata gets HTTP regression evidence;
field semantics get real DOM/focus assertions, not only a static proxy.

## Phase Checklist

<!-- P01 -->
### P01: Correct backend and expose range errors

* [x] P01-T01: Add history guard, typed range error, serialization and semantic/HTTP regressions.

<!-- P02 -->
### P02: Correct field error experience

* [x] P02-T01: Render linked inline range errors and focus first field; extend browser/axe and README.

<!-- P03 -->
### P03: Validate and review

* [x] P03-T01: Obtain nonblocking heavy lock; run API suite and focused browser/axe, or targeted-only fallback; lint/type/syntax/diff and pin checks.
* [ ] P03-T02: Reconcile all artifacts; execute one independent Review and commit locally, reporting any routed findings.

Dependencies: P02 consumes P01 error metadata; P03 consumes P01/P02.

## Critique Disposition

Exactly one final-candidate critique executed Complete / Pass with no findings:
.copilot-tracking/plans/2026-10-29/progress-dashboard-533-correction-critique.md.
No significant/divergent decision needed. Candidate remains unchanged.

## Follow-Up Items

Human screen-reader/usability acceptance and publication gates remain outside
this correction. Historical parent review outcomes are not rewritten.
Full API discovery was skipped because nonblocking lock admission was busy;
35 targeted tests and the targeted progress browser/axe check passed instead.
Owner/coordinator can schedule full discovery when the lock is free.
Existing axe color-contrast incomplete results remain for human assessment.

## Handoff

Implementation changes record:
.copilot-tracking/changes/2026-10-29/progress-dashboard-533-correction-changes.md.
Automatic parent continues only after critique dispositions resolve plan blockers.

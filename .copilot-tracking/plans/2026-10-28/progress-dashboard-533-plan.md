---
title: Progress dashboard and closed cases implementation plan
ms.date: 2026-10-28
---

Task: #533, progress-dashboard-533. RPI loop executed; independent Review
outcome Defects found. Local delivery is not acceptance or publication.

## Executive Summary

Add separate native dashboard/list modules with read-only server endpoints.
Only explicitly synthetic case records enter the dashboard. Use labelled
simulation events and explicit closure/reopen records, with coverage counts
instead of invented dates. Preserve existing roles and queues. Local delivery
does not authorize publication without the full exact-head gate.

## Sources

Research: .copilot-tracking/research/2026-10-28/progress-dashboard-533-research.md.
Details: .copilot-tracking/details/2026-10-28/progress-dashboard-533-phase-details.md.

## User Decisions and Requirements

* Full research, plan, implement, review loop for #533, commit dated evidence.
* Branch feat/progress-dashboard-533 stacked on feat/case-journey-ux-526,
  dependency PR #529; any PR uses that base and "Refs #533".
* All requested metrics, date range and chart table alternatives.
* Closed list status/date/team/text filters, URL state and paging boundaries.
* Native Fluent 2 foundations; no framework swap, briefing or map edits.
* Synthetic only; no private data, secrets, .env, az or Azure.
* Relevant unit/browser/axe regressions; flock -n with <=40 minute retry.

## Goals

Make demonstrator progress inspectable without implying operational truth,
safety compliance, savings or approval.

## Scope and Non-Goals

New src/api progress.py, web/progress.js and progress.css; small server/router/
navigation/script integration. New focused API/unit/browser regression files
and component README. No data migration, generator changes or shared queue fix.

## Functional Requirements

* GET /api/progress: opened/closed daily and Monday-based weekly counts,
  end-of-day known backlog (including reopen), median/nearest-rank p90 calendar
  days for closures in range; current journey/team workload, 60-day stalled
  signal and recorded overdue tasks; AI briefing review outcomes where linked
  synthetic case evidence exists, separating AI from rules/templates.
* Inclusive ISO date bounds, default last 30 days ending at store.as_of,
  max 366 days. Reject invalid/repeated/unknown query parameters.
* Current workflow/team/stalled/overdue measures explicitly labelled current
  recorded view; they do not pretend historical ownership can be reconstructed.
* Dedicated GET /api/closed-cases preserves manager restriction, searches
  authorised summary fields only, closure-date bounds and exact stage/team.
  Stable ID ordering; page size 20, limit <=100, clamp out-of-range page to
  last page, one empty page for zero results. Return facets and effective page.
* Filters and page stored in hash query; applying filters resets page one,
  previous/next are real links; refresh/back/forward restores state.

## Non-Functional Requirements

Explicit synthetic admission at case level (case.is_synthetic true or nonempty
wholly marked simulation history), no dataset file reads. Aggregate no actual
staff names. Existing stats permission for dashboard, manager for closed.
Native labelled forms, status/error/loading, semantic tables, visible focus,
text counts independent of bar colour and mobile reflow. Date/number locale
formatting. No new dependencies.

## Acceptance Criteria

* All issue measures render with definitions, provenance and missing counts.
* Every visual series has an identical accessible table.
* API tests verify actual numbers, unknowns, reopen and date/week boundaries,
  synthetic exclusion and role denial.
* Closed list tests cover 0,1,20,21, exact/full/last/beyond pages, combined
  filters, malformed input, deterministic ordering and no data mutation.
* Browser checks exercise real endpoints, filter reset/URL/history,
  keyboard and 320/390/1280 reflow, empty/failure/retry, axe both pages.

## Phase Checklist

<!-- phase: P01 -->
### P01: Server read models

* [x] P01-T01 Implement separate progress aggregation and archive read model.
* [x] P01-T02 Wire role-checked routes and focused semantic unit/API tests.

<!-- phase: P02 -->
### P02: Native employee surfaces

* [x] P02-T01 Build separate dashboard/list renderer, stylesheet and navigation.
* [x] P02-T02 Add focused real-browser/axe regression and component guide.

<!-- phase: P03 -->
### P03: Validation and review

* [x] P03-T01 Locked targeted checks, then relevant API suite; lint/types/JS.
* [x] P03-T02 One independent Review; preserve findings, commit evidence.

## Validation Ownership and Test Change Lock

Owning suite: src/api/tests/test_progress_dashboard.py (new, <=20 semantic
tests); src/api/checks/progress_browser_check.py (new focused browser check).
No tests removed. Existing design/accessibility/workbench/script/role tests
are regressions, not altered to conceal failures. No generated targets.
Evidence includes exact commands/outcomes, axe version/hash and browser version.
Full gate remains separate and never runs prohibited az. No push if blocked.

## Critique Disposition

Executed once: Complete / Revise, preserved at
.copilot-tracking/plans/2026-10-28/progress-dashboard-533-critique.md.

| Finding | Disposition | Resolving contract |
| --- | --- | --- |
| PC-001 | Rejected | Worker-only temporary-directory restriction is not a caller restriction; user explicitly requires /tmp/ama-rpi-heavy.lock. Preserve requested lock and owned venv. |
| PC-002 | Accepted, applied | AI records also require is_synthetic=true and nonempty all-admitted case_ids. Return aggregates only; unmarked records never count. |
| PC-003 | Accepted, applied | Replay Reopened - aftercare as reopen; opened includes initial and reopened episodes, with separate reopened count. |
| PC-004 | Accepted, applied | Archive status means Recorded case status (stage), exact stage or Unknown; never legacy constant Completed. |
| PC-005 | Accepted, applied | Latest closure ending latest episode is archive date; unknown dates included unbounded, excluded bounded, with count. Archive default is unbounded. |
| PC-006 | Accepted, applied | AI briefing review outcomes use resolved_at within inclusive UTC dates, source=ai; Edited displays Changed. Missing dates excluded and counted; unreviewed separate. |

Planning disposition was implementation-ready; no significant unresolved
decision and no second critique. Implementation and the one Review subsequently
executed. Original critique and Review outcomes remain unchanged.

## Follow-Up Items

Human screen-reader/user acceptance and full Fluent component adoption remain
existing open work, not #533 completion claims; owner/design-system participants
retain those acceptance decisions. Review RV-001 (date-field error association
and focus, Medium) and RV-002 (loading aria-busy, Low) go to a later
rpi-implement invocation, not an additional active phase in this completed loop.
Coordinator owns parent-lineage reconciliation and permitted complete-gate
execution before publication.

## Handoff

Changes path: .copilot-tracking/changes/2026-10-28/progress-dashboard-533-changes.md.
Review execution Complete, outcome Defects found:
.copilot-tracking/reviews/logs/2026-10-28/progress-dashboard-533-review.md.
P03-T02 records the original assessment and its local evidence commit, not
resolution of RV-001/RV-002 or a full-gate/hosted/human approval.

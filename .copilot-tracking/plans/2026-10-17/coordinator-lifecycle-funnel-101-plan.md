---
title: Coordinator lifecycle funnel issue101 implementation plan
description: Bounded read-only coordinator reporting and local evidence plan
ms.date: 2026-10-17
---

Task: 101 / coordinator-lifecycle-funnel-101. Base:
ebc8dab87ae9bd6a33380b85e86f38be5ed9f213.
Branch: feat/coordinator-lifecycle-funnel-101. Mode: automatic, user requested
Research -> Plan with critique -> Implement -> ONE original Review.

## Executive Summary

Reuse the current workbench, Leaflet clustering, authorized case filtering,
closed field guards, queue signals and validated timestamped progress events.
Add a coordinator view linked from the existing overview, backed by one read-only
staff endpoint and synchronized population. Heatmap, map and bounded record
drillthrough share all filters. Distinguish current occupancy from observed
transition counts; historical exclusions/conversions remain Unknown when no writer
exists. This is engineering delivery, not independent coordinator or human approval.

## Sources

Research: .copilot-tracking/research/2026-10-17/coordinator-lifecycle-funnel-101-research.md
(C1-C10, W1-W4). Details:
.copilot-tracking/details/2026-10-17/coordinator-lifecycle-funnel-101-phase-details.md.
Critique target:
.copilot-tracking/plans/2026-10-17/coordinator-lifecycle-funnel-101-critique.md.

## User Decisions and Requirements

* Complete explicit ordered RPI phases with real dated committed artifacts.
* Keep read-only, reuse existing map/list/filter/roles, preserve all controls.
* Show denominators, stops, priority-policy status, missing geocodes and coverage.
* Use actual timestamped events; legacy and unsupported exclusions remain unknown.
* Do not touch issue117 runtime/document/provenance writer paths or another worktree.
* Local tests, configured lint/format/types, JS syntax, actual browser before push;
  SQL parity for changed aggregation/count access and hardened image checks.
* Synthetic fixtures only; no Azure, paid AI, tile change, new service or authority.
* Commit/push designated branch, PR to main with Refs #101; no merge/rebase/force.

## Goals

Make coordinator counts explainable and their record membership reproducible.
Retain useful existing map/list work without widening into timeline/forecast/export.

## Scope and Non-Goals

In scope: new core read-only coordinator module; staff GET /api/coordinator with
explicit validated query; existing app scoped coordinator mode; module/API/browser
tests and directly related guides/KB synthesis/index/log.
Out: Store writers/schema, document/provenance integration, orchestrator, auth model
redesign, ranking changes, new generated stock, general closure/exclusion capture,
real deployment, operational/human/WCAG acceptance.
KB index/log overlap with117 is declared, not resolved by an unauthorized rebase.

## Functional Requirements

* FR1: own/all open-case scopes reuse Store._filtered with existing source filters
  and text search under the existing sync lock. Unknown scope/metric/parameters
  and repeated/empty fields refuse explicitly; endpoint and direct module deny
  contractors and unregistered/unknown staff.
* FR2: current denominator, current stopped cases from existing current_stop plus
  explicit paused stages, and priority availability from unchanged policy.
* FR3: heatmap by area/building/recorded home type and current stage; Unknown is an
  explicit group. Every cell drills to permitted records.
* FR4: event window uses inclusive UTC progress validation; count distinct cases
  per stage and metric (entries to, exits from, returns/reopens to stage), not raw
  event occurrences. Invalid/ambiguous streams do not become trusted counts.
  Cases can appear in several rows, so rows are not an additive conversion funnel.
  Current `stage` source filter and `metric_stage` event/occupancy drill selector
  are independent: exit-A can include a case now in B. Both intersect the source
  cohort, never silently replace it. Cohort denominator and drill total differ.
* FR5: filter exclusions are baseline authorized open cases minus source selection,
  never lifecycle exclusion. Lifecycle exclusions and true conversion are Unknown.
  Whole-home closure/accepted handover are not inferred.
* FR6: map population total equals drillthrough total; mapped, missing/invalid
  geocodes and in-viewport counts are separate. Existing map field guards remain.
  Pagination uses stable ID order and total independent of page size.
* FR7: labelled native controls, table equivalents, keyboard record links,
  visible loading/empty/error/unknown states, shareable URL selection, reduced
  motion and existing Fluent tokens. Manual case routes remain available.

## Non-Functional Requirements

* Server authority before aggregation, closed output fields, no narratives/diagnoses/
  raw event actors/source references/finance evidence in aggregate or record rows.
* No new dependencies. Read-only results do not mutate cases/audit/SQL sequence.
* Preserve legacy map/stats/list behavior outside explicit coordinator mode.
* Local synthetic SQLite and actual task-owned loopback SQL Server parity,
  actual Chromium exercise, configured checks and source-context API image.
* Resources uniquely named, no shared credentials/data, stopped after execution.

## Acceptance Criteria

* AC1: displayed counts include current denominator, stopped cases, draft versus
  approved policy, coverage and historical unknowns.
* AC2: same-filter aggregate/map/paged records reconcile, including no coordinates,
  combined source/search/group/metric filters, empty results and pagination.
* AC3: current and observed funnel cells drill through to exact records; invalid/
  legacy history cannot create fictional transitions or exit times.
* AC4: server denials, field minimization and unchanged audit verified; actual
  browser exercises keyboard filters/drillthrough/counts/unknowns and denials.
* AC5: artifacts, actual command/count receipts, original Review and limits retained;
  clean commit, exact remote branch head and PR main with Refs #101.
* Human independent coordinator acceptance remains unchecked.

## Phase Checklist

<!-- P01 -->
### P01 Read-only aggregation and HTTP contract

* [x] P01-T01 Implement one coordinator module with validated selection, safe
  summaries, reused event validation, heatmap/funnel/map and bounded record pages.
* [x] P01-T02 Wire staff endpoint and add semantic/core/API denial/parity tests.

<!-- P02 -->
### P02 Existing workbench coordinator mode

* [x] P02-T01 Reuse mapPanel in scoped mode; add native filter/heatmap/funnel/
  record drillthrough with URL state and unchanged legacy views.
* [x] P02-T02 Add actual local Chromium journey and update guides/KB.

<!-- P03 -->
### P03 Local validation and handoff

* [x] P03-T01 Run focused core/API regressions, configured ruff/format/mypy and
  node syntax. Escalate only on evidence.
* [x] P03-T02 Run actual SQL parity/external refresh/read-only invariance and
  Docker build/nonroot image/source checks; stop task resources.
* [x] P03-T03 Reconcile changes/details/state, execute ONE original Review, retain
  its complete findings; route findings separately, not a second review.
* [ ] P03-T04 Fresh authenticated privacy-safe author/committer, conventional
  commit with Copilot trailer; normal push/PR; clean and remote-head verification.
  Delivery is blocked by unresolved mandatory correctness/authorization findings.
  Non-blocking deferrals need rationale. Any permitted later correction must keep
  original finding IDs/verdict and separate focused receipts, never another Review.

## Test Ownership and Candidate Lock

Canonical core semantic tests: src/core/tests/test_coordinator.py (maximum 18
new methods). Canonical HTTP/SQL/browser tests:
src/api/tests/test_coordinator_api.py (maximum 12 new methods; backend subclasses
reuse methods). Optional reusable journey helper lives in this same test module,
not another framework. Existing suites are regression ownership; removals: none.
Generated targets: none. Fixtures: existing public dataset.DATA with tiny explicit
constructed event/unknown mutations, never generated private stock reads.
Production targets: coordinator.py, server.py, projection.py, app.js/style.css only
as needed; avoid shared Store/runtime writer paths. Validation receipts live in
changes and review, not generated acceptance results or CI-first claims.

## Critique Disposition

Execution: Complete, exactly one final-candidate worker. Original verdict: Revise
(one High, two Medium). All findings directly dispositioned; no second critique.
PC-001 accepted: independent `stage` source and `metric_stage` drill parameters;
assign now-B/exit-A regression and browser navigation to P01-T02/P02-T02.
PC-002 accepted: force cluster mode in canonical tests using test-only cap patch,
sum cluster membership and exercise browser cluster-to-zoom with retained scope.
PC-003 accepted as delivery gate: never claim completion/push as corrected while a
mandatory boundary/correctness blocker remains. Preserve original Review verbatim;
if it finds a blocker, record separate follow-up/correction evidence without
rerunning Review or self-awarding independent acceptance. Forbidden-path correction
stops the affected delivery. Candidate finalized Ready after these compatible edits.

## Follow-Up Items

* General lifecycle closure/exclusion and initial-entry capture are not implemented
  by this read-only task; remain explicit unknown, not manufactured history.
* Direct human task/understanding/WCAG review and coordinator acceptance remain
  separate. No new customer approval is implied.

## Handoff

P01/P02 implemented; P03-T01/T02 completed with actual local receipts. P03-T03
original Review executed Complete, outcome Defects found, retained at
.copilot-tracking/reviews/logs/2026-10-17/coordinator-lifecycle-funnel-101-review.md.
RV-001 Medium exposes false403 for mixed-case legitimate registered emails.
P03-T04 publication/completed delivery blocked by PC-003; local persistence does
not close it. Route correction to later selected rpi-implement, no repeat Review.
Critique ran once and remains unchanged. Closed scalar summaries reuse export_fields
rather than building full private Store summaries. Changes record:
.copilot-tracking/changes/2026-10-17/coordinator-lifecycle-funnel-101-changes.md.

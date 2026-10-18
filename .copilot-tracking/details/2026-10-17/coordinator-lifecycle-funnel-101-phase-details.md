---
title: Coordinator lifecycle funnel issue101 phase details
description: Task implementation boundaries, evidence and completion expectations
ms.date: 2026-10-17
---

Task101, base ebc8dab87ae9bd6a33380b85e86f38be5ed9f213, automatic.
Research disposition executed/Ready; one focused wider/deeper/contrarian cycle.
Canonical plan: .copilot-tracking/plans/2026-10-17/coordinator-lifecycle-funnel-101-plan.md.

<!-- P01 -->
## P01 Read-only aggregation and HTTP contract

<!-- P01-T01 -->
### P01-T01 Coordinator module

Use existing Store boundary under lock; no new Store methods or writers.
Server must resolve existing registered actor, not body/query-supplied authority.
Module validates actor against current store.staff before any population read.
Own scope means owner_code; all means existing staff-wide open access.
Use insights.matches via _filtered and existing closed scalar field projection,
without constructing full private summaries or duplicating queue/resident rules.
Current stock selection is never a
historical reconstruction.

Compose progress.report/history in the same snapshot, preserving UTC validation,
precision and exception evidence. On bad ledger, observed transition counts are
unavailable, not zero. On contradictory/invalid stage stream, retain unknown
coverage and exclude its transitions from trustworthy observed sets. Missing
initial entry/final exit are normal partial history, not invented times.

Stable sets keyed by metric/stage allow distinct-case drillthrough. Record pages
use stable ID order with limit1..100/offset >=0, total before paging. Exclusions
from source filters use authorized baseline, explicitly separate from absent
lifecycle exclusion capture. Null true conversion and lifecycle exclusions.
`stage` always selects current source cohort; `metric_stage` selects observed
entry/exit/return/reopen stage (or occupancy row). It must never replace `stage`.
Explicit now-B exit-A and intersected current-stage tests own this invariant.

Current stop means paused stage OR existing work_context blocker.current_stop.
Only stop count, never private reason. Policy from ranking.CURRENT and
taskqueues.approved_priority; unapproved count null, not zero. Geocode numeric,
finite and geographic range checks; absent/invalid stays in record population.
Mapped records must still pass existing export_fields.map_case checks.

<!-- P01-T02 -->
### P01-T02 Endpoint and tests

One explicitly staff-authorized endpoint /api/coordinator, closed query allowlist
and scalar repetitions/blank checks. Response contains shared selection metadata,
heatmap/funnel, mapped population, safe record page. No detail/narrative data.
Endpoint tests run real loopback authenticated HTTP on tiny fictional data.
Tests cover own/all, source/search/queue/group/metric composition, pagination,
unknown legacy/malformed/precision, roles, private fields and unchanged audit.
SQLite+SQL Server use exact same semantic tests and compare existing list totals.
Force cluster mode with a test-only lower cap; cluster sums equal mapped viewport
records while population includes unmapped/out-of-viewport records.

<!-- P02 -->
## P02 Workbench

<!-- P02-T01 -->
### P02-T01 Scoped coordinator view

Existing overview links to coordinator mode rather than a new nav framework.
Reuse mapPanel parameterization: legacy default preserved; coordinator supplies
shared query and list target. Map count text distinguishes full population,
mapped coordinates and viewport, and missing records link to read-only records.
Native labelled form controls and explicitly named scroll regions/tables.
Count links carry exact URL selection into coordinator record view, preserving
filters and date window. Case links use current detail authorization.
Loading/error states must clear stale counts, offer retry and remain keyboard
usable; abort/version guards prevent stale requests replacing newer selection.
No tile provider/licence change or public-page design work.

<!-- P02-T02 -->
### P02-T02 Browser and documentation

Actual local Chromium with fixture server, no external tiles (test-only
app.tiles override), no model calls. Keyboard apply filters and count links,
compare server totals/map/list, page/record drillthrough, unknown geocodes/history,
contractor/unknown denials, 320/390/1280 reflow and reduced motion.
Exercise forced cluster zoom and preserve independent stage/metric_stage URL state.
Guidelines fetched fully before edits and again before original Review.
Fluent/plain-language rules override irrelevant font/animation/copy suggestions.
Update existing programme journey synthesis and its index/log; preserve all
previous entries and do not edit memory. Record117 KB overlap explicitly.

<!-- P03 -->
## P03 Validation and durable delivery

<!-- P03-T01 -->
### P03-T01 Local commands

Use task-local .venv source pip installation (missing modules already observed).
Core/API targeted tests plus map/list/queue/progress/sensor/role regressions.
Run each owning project's configured ruff check, ruff format --check and mypy;
node --check app.js. Record actual pass/fail/skip counts and every rerun cause.
No full-suite statement unless an entire suite is actually executed.

<!-- P03-T02 -->
### P03-T02 SQL and image

Only UUID/task-owned SQL Docker container on loopback with disposable named
database. Existing mssql-python adapter, same fixture/HTTP test contract, refresh
from second writer and invariance of ledger/cases/sequence. Credentials generated
locally, never committed or printed. New aggregate/count surface justifies parity
despite no schema/query changes. Stop container immediately after test.
Build API Dockerfile with src context; run shipped app nonroot/read-only/drop
capabilities/NoNewPrivs on synthetic mounted fixture; verify actual endpoint and
source hashes and existing src/check-container.py contract where appropriate.

<!-- P03-T03 -->
### P03-T03 One original Review

Reconcile plan markers, completed/blocked checks, changes/details/state and actual
source/base. Refresh fetched guidelines, execute rpi-review exactly once and retain
the original complete artifact including adverse findings. No rewritten verdict
or invented human review. Route findings as later work; do not run another Review.
An unresolved mandatory correctness/authorization finding blocks completed delivery.
Any separately permitted correction keeps original finding IDs and focused receipts
separate, never rewriting or repeating Review. Forbidden-path corrections stop.

<!-- P03-T04 -->
### P03-T04 Commit and PR

Fresh gh api user before commit; repository-local author and committer privacy-safe
ID+login noreply address. Conventional commit and required Copilot trailer.
All issue artifacts/source/docs committed; normal own branch push and main PR
with Refs #101 (not closure). Describe exact commands, evidence and limits.
Verify clean worktree and local==remote head; report main advancement without
rebasing. No merge or resource left running.
Push/completion require disposition of every Review finding and no unresolved
mandatory boundary/correctness blocker; non-blocking deferrals need rationale.

## Current Gate

Coordinator authorization 2026-10-17 selects P03-C01 correction ONE, then P03-T04
publication, on the same original session/worktree/topic. First execution: add
failing-first mixed-case direct and authenticated HTTP tests on JSON/SQLite.
Normalize only the coordinator staff lookup key using the existing lowercase
index convention; preserve exact current email/code/role identity checks.
Exercise unknown/revoked/rebound/changed-or-missing-role denials, focused real
browser and configured core/API ruff/format/mypy plus JS syntax. No web edit,
writer change, Low formatting fix, new critique or Review. Prior actual MSSQL and
image receipts remain historical unless the correction changes their contracts.
Review SHA256 2c740ce1d81719153530139cebd703870795f669337856ea788b537115e81de3;
critique SHA256 247f17ca6c30d54efe0a61c3a25701f19c2d2e1739e0ece3aa34064cfbe09f1d.

P01/P02 complete. P03-T01/T02 complete: coupled154/97 checks and final26/18 focused
checks, actual SQL6run/5pass/one browser skip, hardened installed image checks,
configured core/API lint/format/types and JS syntax. Exact commands, rerun causes
and current-versus-historical evidence are in changes. P03-T03 original Review
executed Complete with Defects found. RV-001 Medium originally exposed false403
for mixed-case staff. P03-C01 now complete: normalize lookup key only, retain exact
identity checks. Failing-first four tests exposed two errors/two failures;
corrected four passed. Coordinator modules49 run/41 pass/eight skips; final core
plus identity30 pass, actual mixed-case browser1 pass, rebuilt installed image
checks pass. Configured static gates pass after one test-variable type correction.
Pure lookup has no SQL query/schema/refresh contract change; actual MSSQL remains
historical, not rerun or relabelled. P03-T04 may proceed under PC-003 based on
separate correction evidence, without another Review or independent Pass.
This invocation owns the minimal lookup/regression correction and
subsequent publication; no second Review. One critique original
Revise retained; PC001-003 dispositions applied. No117 writer changes/dependency.
Human/coordinator/WCAG acceptance remains open.

P03-T04 publication completed: fresh authenticated id8036360/loginjmservera,
local author/committer privacy-safe email and Copilot trailer; correction source
commit5464f8da69bbc979171d8cffd23c4013843aeb96 pushed normally and main PR396
opened with Refs #101. Fresh main remainedebc8dab8; no rebase/force/main write.
Source and all original RPI artifacts are published; this metadata receipt is
persisted in a final ordinary commit, followed by exact remote-head/clean check.
PR initial check rollup empty, not a CI pass. Independent coordinator final-head
review is pending; original Review remains Complete/Defects found byte-exact.

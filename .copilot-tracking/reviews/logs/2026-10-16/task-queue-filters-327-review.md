---
title: Task queue filter review
ms.date: 2026-10-16
---

## Opening Review State

Task #327, task-queue-filters-327. One post-implementation Review.
Scope: complete source, tests, measurement and documentation boundary; delivery
actions remain after this gate. Evidence ready: plan/details, research, critique
Pass, reconciled changes and local results. Acceptance basis: explicit user
constraints and plan acceptance criteria. First comparison: original filter
ordering against indexed candidate selection and authorisation. Read-only
source authority; only this review record receives review findings. No blockers.

## Inputs

* .copilot-tracking/research/2026-10-16/task-queue-filters-327-research.md
* .copilot-tracking/plans/2026-10-16/task-queue-filters-327-plan.md
* .copilot-tracking/details/2026-10-16/task-queue-filters-327-phase-details.md
* .copilot-tracking/reviews/2026-10-16/task-queue-filters-327-critique.md
* .copilot-tracking/changes/2026-10-16/task-queue-filters-327-changes.md

## Execution and Outcome

Execution: Complete. Outcome: Conformant for implementation, measurements,
tests and documentation. Publication remains the parent's P02-T02 action.

## Complete comparison

* Queue definitions are unchanged. The canonical evaluator determines all
  memberships; index values are case IDs in original iteration order, not
  viewer-projected narratives or permissions.
* Invalid queue, contractor and closed-view checks still precede selection.
  Existing row visibility, insights.matches, search, sorting, global ranks,
  cursors, output context and role projection remain in their existing paths.
  Closed-view queue behavior remains unchanged. No new SQL was introduced;
  ordinary SqlStore indexed reads are untouched.
* Cache identity covers Store.version, dataset as_of, current resident day and
  the entire ranking policy. SQL sync catches another writer's sequence before
  Store filtering; shared documents advance that sequence. Membership publishes
  only after a successful full build. Failure cannot publish a partial index.
* Existing list/detail and loopback HTTP redaction/permission tests pass.
  New tests compare all queue/filter/sort/view variants with canonical uncached
  selection and demonstrate local/shared/cross-process and clock/policy refresh.
* Five test methods were added, none removed, within the locked budget of eight.
  The 60k regression records all six match counts, separates cold construction
  from warm pages and verifies evaluator-count complexity independently of
  timing. Original source failed all six new scale assertions; the later
  original-scan mutation failed both JSON and SQLite subtests (91 versus 2).
* Paired measurements are honestly scoped to generated Python/SQLite stock,
  not private data or Azure: warm nonempty medians 2102.7-2567.9 ms before,
  129.6-611.3 ms after; cold first new page 3217.4/3090.6 ms. There is no
  material cold improvement claim. The discarded heavyweight Mock trial is
  explicitly distinguished from the published lightweight-count comparison.
* README documents process-local cache, invalidation, authorisation and cold/
  CSV costs; API links it, knowledge routing updated and log appended.
* No executable changes outside src, tests inside a package, dependency
  manifest change, prohibited SQL addition, private input, Azure/Docker/uv
  invocation, workflow/check rename or unrelated source change.

## Validation assessment

| Evidence | Result |
| --- | --- |
| Core full suite | 468 tests, OK, 1 existing SQL Server skip |
| API full suite | 542 tests, OK, 103 existing conditional skips |
| Agents / orchestrator / importer | 70 / 21 / 39 tests, all passed |
| Five projects' ruff, formatting and mypy | Passed |
| Existing queue HTTP suite | 3 passed |
| 60k queue regression | Passed after; six failures before |
| Runtime original-scan mutation | Killed by new JSON and SQLite regressions |
| git diff --check | Passed |
| Live SQL Server, browser, Docker and Azure | Not run; outside local-only requested boundary |

The existing API development extra was restored only after a missing-playwright
type-check failure, without a manifest change. Initial expiry test failure was
resolved by supplying its absent first-contact evidence; no production rule was
weakened. Changes record chronology retains both failures and later successes.

## Critique and reconciliation

One final-candidate critique executed, Pass, zero PC findings. No significant
implementation divergence or unresolved user decision. P01-T01/P02-T01 complete;
P02-T02 source documentation complete, publication pending. No marker claims
unperformed commit/push/PR. No second critique or Review is required.

## Findings and routing

No substantive RV findings. Severity counts: zero critical/high/medium/low.
No implementation, planning or research defect is routed.
The documented cold rebuild/CSV output cost is an accepted design boundary,
not an unmet in-scope requirement. If future workload evidence shows frequent
invalidations dominate, the owner may select incremental maintenance separately;
no such follow-up is started or claimed necessary now.

## Next action

Parent: record Review Complete/Conformant, commit with the required identity and
trailer, push the existing branch and open a main-based PR using Refs #327 only.
Hosted checks are separate pending evidence. No merge or issue disposition is
authorised by this review.

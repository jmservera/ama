<!-- markdownlint-disable-file -->
# RPI Plan: Progress lifecycle event-kind correction

## Task Metadata

* Task ID: 533-correction4
* Task slug: progress-dashboard-533-correction4
* Plan date: 2026-10-29
* Planning status: Ready; original critique Complete / Revise, both findings resolved directly
* Phase details: .copilot-tracking/details/2026-10-29/progress-dashboard-533-correction4-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-10-29/progress-dashboard-533-correction4-plan-critique.md

## Executive Summary

Retain event identity through replay and reject missing or contradictory
lifecycle steps rather than inventing episodes. Enumerate the initial and
five-by-five event transition table and exercise every cell through reopened
JSON and SQLite stores, checking both historical measures and archive dates.
No API response shape or web assets change.
Implementation and the complete persisted matrix now pass scoped checks.
Full suites/browser remain blocked by busy nonblocking heavy admission.
The single independent original Review completed / Not accepted at source
60004dde, identifying mixed-source ties (RV-001), masked illegal-return tests
(RV-003) and blocked heavy validation (RV-002). Bounded subsequent implementation
is recorded separately under progress-dashboard-533-tie-remediation; it does not
rewrite the original outcome or claim independent acceptance afterward.

### What You May Not Know

A controlled return moves an already-open case to an earlier stage, not to a
new episode. Same-kind actions at distinct times are not proven duplicates.
Exact UTC instant/kind repeats and same-instant closure corroboration are safe
to deduplicate only without an intervening lifecycle-changing transition;
ordered alternating same-instant episodes remain intact. Distinct missing steps remain unknown. Heavy checks require
nonblocking shared-lock admission; a busy lock means targeted fallback and an
explicit validation gap, not an inferred pass.

### Unresolved Decisions or Blockers

No unresolved behavioral decision. Heavy admission returned busy (exit 75);
full API/core discovery, editable setup and progress browser remain unperformed.
All four phases are explicitly requested; local commits only and no automatic
follow-up task.

## User Decisions and Requirements

* Correct the review finding in progress.py, retaining event kinds and marking
  contradictory/incomplete sequences unknown without losing true duplicates.
* Enumerate all transitions for identified, accepted handover, closure,
  reopened and returned; persist JSON and SQLite regressions.
* Full dated RPI round on feat/progress-dashboard-533, PR #540, Refs #533.
* git pull --rebase first (done); Conventional Commits and required Copilot
  trailer; no closing keywords, push, force-push or az.
* API/core mypy, Ruff lint/format, unit suites and relevant browser check;
  worktree-local src/test PYTHONPATH; /tmp/mv editable setup under lock.
* Nonblocking /tmp/ama-rpi-heavy.lock for heavy work; busy means targeted
  tests and honest reporting. Update SHA pins only if pinned files change.

## Goals

* Prevent false known coverage, backlog, reopen and completed-episode counts.
* Establish exhaustive, independently specified transition regression evidence.

## Scope and Non-Goals

In scope: src/api progress.py, test_progress_dashboard.py, API README and dated
RPI records. Read-only producer investigation and existing checks.
Non-goals: schemas, producer behavior, datasets, UI, cloud, publication and
unrelated existing defects.

## Functional Requirements

* Only identification starts the first episode. Closing events require open;
  reopen requires closed; return requires open and never changes episodes.
* Preserve identity until replay completes; maintain output date/bool shape.
* Deduplicate exact UTC instant/kind repeats; same-instant closing kinds
  corroborate one closure, bounded to the current lifecycle transition only.
  Never deduplicate across an intervening close/reopen.
  Different-time repeated lifecycle changes are
  unknown without their required intervening transition.
* Preserve input chronology sorting, stable same-instant source order and
  zero-day episodes; final replay state must agree with the recorded closed flag.
* Keep malformed/non-synthetic/ignored-evidence controls, admission,
  authorization, read-only behavior and unknown archive filtering unchanged.

## Non-Functional Requirements

* Strict mypy, existing Ruff rules, no overrides or dependencies added.
* Replay remains O(n log n) sorting with linear validation/deduplication.
* No private dataset or external service; backend tests use temporary fixtures.

## Acceptance Criteria

* All 5 initial-event and 25 pair cells in the research transition table
  explicitly represented once per backend, with known expected transitions
  specified independently of production code. Prior R/T prefixes establish
  valid state. Every illegal cell remains unknown even when final state agrees.
* Exact duplicate tests cover all five kinds, normalized timezone equivalence,
  both reopen sources, closure aliases, same-instant closing corroboration,
  out-of-order collection input, legal zero-day and multi-episode histories,
  including I before t then A,R,A,R at t, and closing aliases separated by R.
* Report assertions cover known/unknown coverage, exact daily/weekly totals,
  ending backlog, durations and archive unknown dates/start/end filters.
* Persist, reopen and read JSON and SQLite; no in-memory-only matrix claim.
  Use JSON save/reopen and existing test-only SQLite constructed-body injection/
  reopen. Assert exact history/closure/return/closed-field readback first.
* Original two counterexamples fail before the production fix and pass after.
* Required static checks pass. Heavy full API/core unit and progress browser
  checks run only under admitted nonblocking lock; otherwise preserve blockers.
* One final-candidate critique and one independent post-implementation Review
  with original outcomes retained. Source/evidence committed locally.

## Implementation Context Record

Research: .copilot-tracking/research/2026-10-29/progress-dashboard-533-correction4-research.md
(executed, Ready, C1-C8). Changes record will be created during Implement at
.copilot-tracking/changes/2026-10-29/progress-dashboard-533-correction4-changes.md.
Source candidate: 60004dde. Original Review:
.copilot-tracking/reviews/logs/2026-10-29/progress-dashboard-533-correction4-review.md.
Planning-time context is superseded by this original candidate and Review;
later implementation evidence is separate, not a revised verdict.

## Sources

* Research C1-C8, five producer event kinds and existing component checks.
* Explicit user request dated 2026-10-29.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Event-aware replay and exhaustive regressions

Dependencies: completed Research and final-candidate critique.

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Persist the full transition matrix and reproduce the defect

Own tests exclusively in src/api/tests/test_progress_dashboard.py. Remove
none. Maximum additions: four inherited test methods and two local fixture
helpers, no new test file or generated data. The 30-cell matrix is semantic
coverage; two concrete counterexamples and auxiliary controls are regressions.
Canonical fixtures are synthetic_data() and event(); generated targets none.

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Preserve event identity and document replay semantics

Use a small typed event-kind state machine in lifecycle(). Validate before
projecting to existing date/bool output. Reuse observed() and collection guards.
Add no generic framework, schema, dependencies, suppressions or UI changes.

<!-- rpi:phase id=P02 -->
### [x] P02: Validation, original Review and local closeout

Dependency: P01.

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Run scoped and admitted validation

Run focused red/green, API/core mypy and both Ruff commands. Attempt one
nonblocking heavy-lock admission for shared editable installation, full
API/core discovery and existing checks.progress_browser_check using pinned axe.
Hold the lock throughout heavy checks. Busy: do not wait/poll or change shared
venv; run existing-runtime targeted fallback and report remaining validation.
Use absolute worktree src/test PYTHONPATH. Verify pins only for changed inputs.
Execution complete via authorized fallback: 77 targeted tests pass; API/core
mypy and Ruff lint/format pass. Full/browser acceptance remains blocked, not
passed. No pinned file changed; scenario manifest regression passes.

<!-- rpi:task id=P02-T02 -->
#### [x] P02-T02: Commit candidate, obtain independent Review, retain closeout

Configure local noreply author/committer from gh api user (8036360/jmservera).
Commit source plus original evidence, assess the immutable source candidate
once, preserve Review findings/outcome and commit evidence reconciliation.
Do not fix/re-review findings in this task, push or run cloud/publication work.
Original Review Complete / Not accepted retained unchanged. RV-001/RV-003 route
to the distinct bounded subsequent implementation; RV-002 remains blocked.

## Dependencies

Existing /tmp/mv and synthetic-browser runtime, pinned axe, Chromium and
nonblocking lock. Missing prerequisites remain blockers, not substitutes.

## Critique Disposition

One final-candidate critique executed; original verdict Complete / Revise.

| Finding | Owner | Disposition | Resolving evidence |
| --- | --- | --- | --- |
| PC-001 High | Parent | Applied directly | Current-transition-only dedup; ordered I,A,R,A,R and closing-alias controls added to acceptance and P01 details |
| PC-002 Medium | Parent | Applied directly | Explicit JSON save / SQLite body injection, new-reader cleanup and exact payload roundtrip specified |

No unresolved significant/divergent decision. No repeated critique.

## Follow-Up Items

* Required full API/core discovery and progress browser remain unperformed
  after busy lock admission. A later explicitly coordinated validation task
  owns genuine lock admission and these checks; do not retry/poll this round.
  This is an acceptance gap, not an optional or satisfied check.
* Human and hosted/publication gates remain separate; no publication requested.

## Handoff

Original four-phase task execution complete with Review Not accepted; original
source/evidence remains preserved. RV-001/RV-003 are owned by the separate
bounded implementation, not a return to this completed task's Implement/Review.
RV-002 remains an explicitly open acceptance gap. Local-only closeout, no push.

---
title: Issue 76 current-stage blockers plan
description: Bounded offline read-model correction and evidence gates
ms.date: 2026-10-18
---

Task ID: 76. Slug: issue-76-current-stage-blockers. Status: Review complete; publication pending.
Base: 6c1e376ff1241316272df22a5a3a6853aae9f87b.

## Executive Summary

Make the published current-stage blocked definition true without weakening any
gate. Activate final-check requirement records only at final checks, select
reason/action and membership from the same active set, retain inactive future
requirements. Keep public work-queues-1/default/reset contract; add an internal
membership evaluation revision to invalidate previously certified SQL flags.
Validate real stores, HTTP projection and actual disposable local SQL Server.
One independent critique precedes source edits; one original Review follows
candidate freeze. No acceptance of live issue #76 or identity policy is claimed.

## Sources

Research: .copilot-tracking/research/2026-10-18/issue-76-current-stage-blockers-research.md,
C1-C7 and preserved eight-failure real-store baseline.

## User Decisions and Requirements

* Execute Research, Plan with one independent critique, Implement, one original
  Review; preserve originals and hashes; maximum two source correction cycles.
* Use exact supplied branch/base; no rebase, force-push, merge or issue edits.
* Leave #86 resident_decisions.py, projection.py and resident tests untouched.
* Offline synthetic-only, pip-only; no private datasets, secret environment
  files, support, cloud writes, spend, model inference or mvp feature code.
* Publish main-target PR with Refs #76 only, then stop for coordinator review.

## Goals

Restore agreement among queue membership, current_stop and selected action.

## Scope and Non-Goals

Production targets: taskqueues.py and sqlstore.py internal fingerprint, optionally
store.py JSON cache key if necessary. Tests: existing taskqueues, sqlqueues and
task_queue_api suites. Documentation: component queue guides. No gate, authority,
identity, ranking policy, UI or resident recorder changes.

## Functional Requirements

* Funding/resident/technical requirements are current stops at actual Final
  checks before ordering, not earlier or later stages.
* Active safety/stock/building holds retain precedence, ownership and clocks.
* All list/detail/CSV/filter paths reuse canonical projected context.
* Existing populated SQL stores must refresh old flags without body/audit edits;
  other-process hot caches and reopen must agree.

## Non-Functional Requirements

No public schema/default/reset change. Use internal MEMBERSHIP_REVISION in SQL
fingerprint rather than changing VERSION: restoring existing semantics requires
derived-index migration, not a new user-visible definition. Atomic generation
refresh and permission enforcement stay unchanged. Existing mechanism reused.

## Acceptance Criteria

1. Isolated earlier-stage funding/technical future requirements remain visible
   but excluded from blocked, with ordinary current-stage reason/action.
2. Funding/resident/technical final-check controls join blocked; current_stop
   true and selected reason/action coherent, even with pending handoff.
3. Safety/stock/shared-building current holds stay blocking; hazard owner/clock
   remain intact, including combinations with future requirements.
4. Clearing prerequisites and changing stage updates actual persisted flags,
   other-process caches and restart results; old certified flags repaired.
5. Real HTTP staff list/detail/CSV agree and role/query spoofing does not expose
   hidden reasons or grant contractor queue/action rights.

## Test Ownership and Locked Boundary

Primary owns new tests in existing three suite files; no removals, no generated
targets. Maximum 10 new test methods, table-driven cases preferred. Semantic
regressions assert independent expected IDs/current_stop, not only same-evaluator
parity. Original probe retained unmodified. Red regression run before source fix.
Existing SQL membership base class inherits into actual MSSQL harness: prefer
putting applicable new SQL tests there over duplicating test implementations.
Existing resident tests may execute as coupled coverage, but are never edited.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Canonical stage semantics

* [x] P01-T01 Add all semantic, HTTP and certified-index upgrade regressions;
  prove failures on original production base before any source edits.
* [x] P01-T02 Implement active final-check requirements and membership.

<!-- rpi:phase id=P02 -->
### [x] P02: Durable membership compatibility

* [x] P02-T01 Add internal membership revision to SQL fingerprint and upgrade
  regression preserving bodies, rowversions, sequence and audit.
* [x] P02-T02 Exercise clearing, other-process cache and restart on JSON,
  SQLite and task-owned actual MSSQL.

<!-- rpi:phase id=P03 -->
### P03: Validation and publication

* [x] P03-T01 Run focused/coupled suites, configured Ruff/format/mypy,
  original before/after probe and relevant non-root Docker/HTTP evidence.
* [x] P03-T02 Update component docs; freeze source/test candidate and hashes.
* [x] P03-T03 Execute one original independent Review; preserve finding set.
* [ ] P03-T04 Reconcile evidence/state; commit privacy-safe identity and trailer;
  normal push/main PR; stop for complete independent coordinator exact-head review.

## Critique Disposition

Exactly one independent critique executed. Original verdict Revise, three Medium
findings. Original artifact is immutable; no second critique.

| Finding | Disposition | Resolving evidence |
| --- | --- | --- |
| PC-001 | Accepted directly | P01-T01 now requires upgrade regression red run before all production edits |
| PC-002 | Accepted directly | P02-T01 portable test lives in SqlQueueMembership; identical seed path after unlink prevents inherited MSSQL harness wipe |
| PC-003 | Accepted as conservative scratch hardening | Explicit workspace-local TMPDIR for remaining sanitized probes/tests; original baseline already used default temporary synthetic directories, no private data |

No user decision or architecture change needed. The caller did not prohibit
default OS temporary directories explicitly; PC-003's stronger claimed
provenance is not adopted, but its safe execution recipe is.

## Follow-Up Items

Live Entra integration, human role-policy/definition ratification and complete
issue #76 acceptance remain owner/coordinator work, not blockers to this bounded
offline read-model correction. Main movement requires explicit integration
authorization, not unilateral branch rewriting.

Original Review: execution Complete; outcome Residual work; bounded correction
Conformant, no defects. Remote main advanced during Review to observed
9c648b2006e8b2e563823ea7d5aabdf7f1ac7096. Retain original base; do not
integrate. Publish the unchanged topic candidate with drift explicit, then
wait for coordinator integration authorization and exact-head review.

## Handoff

Details: .copilot-tracking/details/2026-10-18/issue-76-current-stage-blockers-phase-details.md.
Critique: .copilot-tracking/reviews/plans/2026-10-18/issue-76-current-stage-blockers-critique.md.
Changes: .copilot-tracking/changes/2026-10-18/issue-76-current-stage-blockers-changes.md.

---
title: Role-screen safety review correction plan
ms.date: 2026-10-27
---

Task ID: 496-r4391306128. Parent: 149 / role-screens-149.

## Executive Summary

Restore the existing projected safety marker and guarded workSummary in the
shared specialist queue. All installed child screens inherit the fix. Keep
server authority, contractor privacy and the original adverse parent Review
unchanged. Add executable unit rendering and actual-browser regressions, run
API/core tests, then commit the candidate/original Review, execute one parent
--changed gate and publish with an explicit lease to draft #496 if valid.

## Sources

* .copilot-tracking/research/2026-10-27/role-screens-149-safety-review-research.md (C1-C8, W1-W2)
* .copilot-tracking/details/2026-10-27/role-screens-149-safety-review-phase-details.md
* Discussion https://github.com/jmservera/ama/pull/496#discussion_r4391306128

## User Decisions and Requirements

* Run the full dated RPI loop for this correction; preserve prior evidence.
* Rebase the run-owned parent onto origin/main with rerere; keep both log sides,
  skip conflicting rubric bot commits, permit force-with-lease.
* Fix the single open safety thread and audit the same pattern in all role queues.
* Run the requested API discovery with explicit worktree source roots and core
  tests; fix stale scenario-manifest hash only on demonstrated failure.
* One scoped --changed gate per parent, never --all; never uv, secrets/.env,
  push main, merge, or close issues. Keep #496 draft and use Refs.
* Report final SHA and test results; retain final-head review evidence.

## Goals

Preserve all available recorded safety timing/ownership context in the specialist
queue without fabricating or exposing context withheld by the server.

## Scope and Non-Goals

Shared host, focused tests/browser check and directly related API documentation.
Conditional public scenario hash correction only. No child integration/rebase,
backend schema changes, Fluent redesign or human/live acceptance claim.

## Functional Requirements

* Show `Safety issue open` using projected hazard and the existing danger flag.
* Use the existing workSummary for every supplied work object, including hazard
  clocks and non-hazard task/handoff/source context.
* Missing/null work must not crash or invent context, especially for contractors.
* Keep case selection, paging, native links, abort/session boundaries and
  read-only role restrictions unchanged.

## Non-Functional Requirements

Reuse native/Fluent-derived presentation, plain language and external timing
authority. Tests must execute real host/helper code, not just match source
strings. No new dependency or test skips.

## Acceptance Criteria

* AC1: A hazard row shows the textual marker, task owner and each distinct
  follow-up owner, awareness time, elapsed/Unknown clock and response/update due
  time, retaining source/version and timing authority.
* AC2: Non-hazard rows still show supplied work; no-work rows render navigation
  with no fabricated marker/work/clock. Contractor API projection stays unchanged.
* AC3: Actual browser exercises a test-only specialist module for staff and
  contractor, remains read-only, supports mobile reflow and native focus.
* AC4: Audit inventories all case-list consumers and distinguishes intentionally
  absent projections from dropped available work; findings are documented.
* AC5: Requested API and relevant core suites pass; stale public source binding
  regenerated only when failure establishes it.
* AC6: One independent critique and one postimplementation Review preserved;
  final committed head receives a separate read-only exact-head assessment.
  Exactly one --changed gate is attempted and verified as partial, never full.
  If it fails, retain evidence and report the publication blocker honestly.
* AC7: Successful gated candidate pushes only to the authorized parent with
  explicit lease, remains draft, and retains dated final-head evidence.

## Phase Checklist

<!-- phase: P01 -->
### P01: Restore context and prove regression (complete)

* [x] P01-T01 Add executable host/helper unit regression, observe failure, then
  restore marker and guarded workSummary.
* [x] P01-T02 Extend owned-loopback browser coverage and API README; record queue
  inventory and unchanged privacy boundaries.

<!-- phase: P02 -->
### P02: Validate and reconcile

* [ ] P02-T01 Run full requested API discovery and core suite using this worktree.
  Repair only demonstrated stale scenario hash; rerun affected tests.
* [ ] P02-T02 Run parent browser/focused static/lint checks and reconcile evidence.

<!-- phase: P03 -->
### P03: Review, gate and draft publication

* [ ] P03-T01 Complete one independent original Review, route findings without
  repeating Review, and commit candidate with dated RPI artifacts.
* [ ] P03-T02 Run one foreground --changed parent gate, verify current-base
  partial receipt and retain exact-head read-only assessment exclusively
  externally until publication is finished (no post-gate candidate writes).
* [ ] P03-T03 Publish only on permitted passing evidence, use explicit lease,
  verify remote head/draft and reply to the existing thread with evidence.
  Only after the last remote write, copy final-head evidence under tracking
  to satisfy the caller's local-retention request; do not claim that resulting
  dirty worktree still verifies or publish another commit.

## Test Ownership and Change Budget

* Canonical unit owner: src/api/tests/test_role_screens.py, maximum two added
  methods executing Node/real host and real workSummary, no removals.
* Browser owner: src/api/checks/role_screens_browser_check.py, maximum one helper
  and parent-only invocation for a synthetic registered screen; no child
  expectation changes or test deletions.
* Generated target: docs/reference/research/retrofit-synthetic-data/scenario-manifest.json
  only if a stale hash is demonstrated. Preserve version/coverage/fixture data.
* Semantic coverage: real helper rendering/recorded fields and no-work cases.
* Regression coverage: exact host link text/classes/navigation and real browser
  staff/contractor responses, existing unit/browser suite behavior.
* API README is directly related documentation; durable audit stays in tracking.

## Critique Disposition

Critique execution: Complete. Original verdict: Revise; no second critique.

| Finding | Disposition | Resolving evidence |
| --- | --- | --- |
| PC-001 High | Applied with explicit caller retention requirement preserved | Final-head assessment exclusively external through final pre-push verification and all publication; local copy only after publication, with receipt validity limitation explicitly stated. No ignored-output bypass or post-gate commit. |
| PC-002 High | Applied | P03 result table below and details block publication for unresolved in-scope review/assessment defects, gate/base/head/lease invalidation. |
| PC-003 Medium | Applied | P02-T02 assigned two-sided verbatim/order-preserving log comparison at exact source SHAs before Review/gate. |

PC-001's suggested exclusively external final retention would not meet the
caller's explicit local tracking requirement. The safe reconciliation is an
external-only publication boundary followed by a clearly post-publication
local evidence copy. Its presence invalidates later receipt verification
until preserved outside the candidate again; no further push is allowed here.

## Publication Result Rules

| Result | Action |
| --- | --- |
| No unresolved in-scope safety/access/privacy/evidence-integrity/engineering Review or assessment finding, valid scoped receipt, same base/head and expected remote | Parent draft push eligible; hosted/human approval remains separate |
| New in-scope adverse Review or exact-head finding | Block publication, retain original Review and route later work; no repeated Review |
| Failed/invalid gate, moved base/candidate/tools, exhausted one-attempt budget or unexpected remote movement | Block push, preserve evidence; no silent rerun/overwrite |
| Inherited child/integrated-journey or human/AT/Fluent limitations | Retain explicit scoped limitations; do not infer acceptance |

## Follow-Up Items

* Owner-controlled child integration and combined-head journey checks remain
  inherited work, not accepted by a parent-only correction.
* Human/screen-reader testing and actual Fluent adoption remain separate.
* Archive/coordinator do not project work today; enriching those backend schemas
  is separate from restoring fields already supplied to open task queues.

## Handoff

Planning readiness: Ready after direct critique dispositions. No unresolved user decision.
Changes record: .copilot-tracking/changes/2026-10-27/role-screens-149-safety-review-changes.md.

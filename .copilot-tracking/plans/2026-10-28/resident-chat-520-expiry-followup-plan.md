<!-- markdownlint-disable-file -->
---
title: Resident chat 520 proposal expiry follow-up plan
ms.date: 2026-10-28
---

# RPI Plan: Reject proposals expiring during confirmation

## Task Metadata

* Task ID: 520-expiry-followup
* Task slug: resident-chat-520-expiry-followup
* Planning status: Ready; original independent critique Complete / Pass
* Plan date: 2026-10-28
* Phase details: .copilot-tracking/details/2026-10-28/resident-chat-520-expiry-followup-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-10-28/resident-chat-520-expiry-followup-plan-critique.md

## Executive Summary

Carry the proposal expiry through the existing booking query, then recheck expiry and
slot start against a single fresh instant after authorization. A conflict at either
deadline rolls back the insert. Add a deterministic regression in the owning unit suite.
Run scoped resident-demo tests plus full API Ruff100/format100 and strict mypy.

### What You May Not Know

The existing idempotent retry path intentionally returns an already committed booking
without requiring an unexpired proposal. It must not be changed. The full gate is blocked
by the explicit az bar; scoped checks are not a full receipt or whole-issue acceptance.

## User Decisions and Requirements

* Complete the full RPI loop for the supplied PR #525 review thread on feat/resident-chat-520.
* Use the smallest correct fix and a regression that fails without it; inject time, no sleep.
* Hold /tmp/ama-rpi-heavy.lock for heavy work using nonblocking attempts every 60s,
  at most 40 minutes; do not bypass it.
* Fetch origin, rebase onto a remote bot commit if present, normal push only, then reply
  and resolve PRRT_kwDOUU8JX86xTMcu after the fix is pushed and tested.
* Conventional Commit with privacy-safe identity and Copilot coauthor trailer.
* No az, full-gate attempt, merge, deployment, secrets, .env, private data or PR closing keyword.

## Goals

* Prevent an authorization delay from turning an expired proposal into a booking.
* Preserve atomicity, authorization, idempotency and static-clock callers.

## Scope and Non-Goals

Scope: agenda.py, its existing unit test file, one README clarification and dated RPI artifacts.
No browser assets, schema, dependencies, public signatures or broader assistant changes.

## Functional Requirements

* Initial lookup and final revalidation both reject expiry/start at or before their instant.
* Final deadline rejection raises AgendaConflict and leaves no booking persisted.
* Existing booking retries remain idempotent and existing authorization checks retain priority.

## Non-Functional Requirements

* Use the existing transaction/clock helpers; one final timestamp, no sleeps or new dependencies.
* Tests use only constructed fixtures and disposable SQLite inventory.
* Full package Ruff100, formatting and mypy preserve repository configuration.

## Acceptance Criteria

* New test fails on original code and passes with fix.
* Test covers just-before, exact and after expiry after authorization; the slot remains future.
* Expired cases leave no persisted booking and the same slot can be booked by another owner.
* All relevant resident-demo unit/API selectors pass; lint/format and mypy pass.
* Original critique and Review are retained with actual outcomes; full-gate block is explicit.
* Normal pushed head and successful thread reply/resolution are verified.

## Implementation Context Record

Research: .copilot-tracking/research/2026-10-28/resident-chat-520-expiry-followup-research.md
(Complete / executed / Ready). Changes record will be owned by implementation at
.copilot-tracking/changes/2026-10-28/resident-chat-520-expiry-followup-changes.md.
Automatic parent continues after exactly one final-candidate critique.

## Sources

* Research C1-C6/W1: transaction, query, clock, test and validation contracts.
* src/api/README.md: synthetic callback behavior and test commands.
* src/api/pyproject.toml: Ruff100 and package-wide strict mypy.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Implement and validate the expiry boundary

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Add regression, prove red, apply minimal fix and clarify docs

Select o.expires; compute one final instant after authorised(); reject either deadline
with the existing conflict message. Add one unit test method with boundary subtests.
Update README to state both deadlines are rechecked after authorization.

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Run locked focused and package-static validation

Restore pinned development tools in an isolated external environment after observed
missing ruff/mypy errors. Run new regression and the resident-demo selectors, then
full API ruff check/format at 100 and mypy. No browser run for backend-only changes.

<!-- rpi:phase id=P02 -->
### [ ] P02: Independent Review and authorized publication

Depends on P01. Review once, retain outcome, commit dated evidence, fetch/reconcile
remote bot commits, rerun affected checks after rebase if required, normal push,
verify head and reply/resolve only the specified thread.

## Dependencies and Locked Test Ownership

* Canonical implementation: src/api/src/zava_forward/api/resident_demo/agenda.py.
* Canonical regression: src/api/tests/test_resident_chat_agenda.py, maximum one new
  test method with boundary subtests. Exact removals: none. Generated targets: none.
* Semantic proof: just-before expiry succeeds; exact/after expiry conflicts while slot
  start is future. Regression proof: new test fails against original implementation.
* Persistence proof: reopened agenda has no booking after rejection and slot is reusable.
* Commands: documented shared fixtures; include test_resident_chat_agenda,
  test_resident_chat_api, test_resident_demo_api, test_resident_assistant_api,
  test_resident_aoai and test_resident_assistant_provider.

## Critique Disposition

Exactly one independent final-candidate critique Complete / Pass, no PC findings.
Original artifact retained at the metadata path. No correction or user decision required.

## Follow-Up Items

* Full gate: blocked by barred az, future authorized validation only; not active fix work.
* Human/AT and hosted acceptance remain separate inherited gates, not claimed by local checks.

## Handoff

P01 complete: final exact-test negative control and regression passed their expected
outcomes; 92 resident tests passed without skips, API Ruff100/format100 and mypy
(94 source files) passed. Ready for the one independent Review in P02, then authorized
publication. No unresolved implementation decision. Full gate remains blocked independently.

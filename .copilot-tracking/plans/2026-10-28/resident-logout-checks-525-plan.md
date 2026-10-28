---
title: Resident logout browser-check correction plan
ms.date: 2026-10-28
---

Task: PR-525-PRRT_kwDOUU8JX86xVDWZ

## Executive Summary

Replace two obsolete cookie-deletion checks with retained-token denial and
explicit signed-out session evidence. Capture the original request fence to
avoid false-positive authorization checks. Application behavior is unchanged.

## User Decisions and Requirements

* Complete research, plan, implementation and independent review for PR #525.
* Preserve no-Set-Cookie logout and PR `Refs #520`, never closing issue text.
* Search all other tests/checks for logout cookie-deletion expectations.
* Validate relevant API units and SQLite/SQL resident browsers; use nonblocking
  flock admission with bounded retries up to 40 minutes. No az/Azure or secret reads.
* Commit dated artifacts, use Conventional Commit and required Copilot trailer,
  push normally, then reply to and resolve the exact thread when publication gates permit.

## Goals

Prove logout revokes authorization despite retained browser cookies, including
successful retry after 403, 503 and aborted logout.

## Scope and Non-Goals

Canonical target: `src/api/checks/resident_demo_browser_check.py`.
Tests: `src/api/tests/test_resident_demo_check.py`.
Directly related documentation: `src/api/README.md`.
No generated targets, runtime changes, UI source, dependency-manifest changes,
Azure, unrelated assertion cleanup or historical RPI evidence replacement.

## Functional Requirements

Both corrected paths must retain the original token, deny a view request carrying
the original session fence, and receive successful session status reporting
`signed_in` false and `session_id` null. Preserve cross-resident isolation and
independent replay denial. Keep failed-logout assertions.
Require exactly 401, not a fence-only 409 or arbitrary error. Before logout,
require a 200 signed-in session with a nonempty string session ID and a protected
view 200 using that exact fence.

## Non-Functional Requirements

Ruff line limit 100. Reuse an assertion helper for both paths. No secret logging.
Use only task-owned loopback SQL resources and delete exactly those resources.

## Acceptance Criteria

* Both stale deletion assertions are absent; no other logout deletion expectation remains.
* Normal and retry logout use the same semantic checks with the original session ID.
* Relevant unit tests, SQLite assistant/account browsers and real SQL demo browser pass.
* Runtime no-Set-Cookie unit and delayed-response browser regressions still pass.
* Original independent critique and Review are committed unchanged.
* Publication remains blocked if the mandatory exact-head full gate cannot run
  under the explicit no-az constraint. Focused success is not a full receipt.

## Test Ownership and Budget

API owns the semantic browser helper and focused mocked helper regressions.
Exact removals: two deletion assertions only. Maximum additions: four helper
unit tests covering success, a live retained token, wrong token, and bad session
status. Preserve all runtime unit tests. Browser exercises remain the integration
authority; mocks only test helper failure sensitivity.

## Phase Checklist

<!-- P01 -->
### P01: Correct and validate checks

* [x] P01-T01: Implement shared retained-token/session-status assertions at both paths.
* [x] P01-T02: Add bounded helper regression tests and update browser documentation.
* [x] P01-T03: Run targeted unit/static and actual SQLite/SQL browser validation under lock.

<!-- P02 -->
### P02: Review and publication

* [x] P02-T01: Perform one independent Review and preserve its outcome.
* [x] P02-T02: Commit source and dated evidence; meet publication gates or record blocker.
* [ ] P02-T03: On eligible publication, normal push, thread reply/resolution, preserve Refs #520.

## Critique Disposition

One final-candidate critique executed: Revise, one HIGH and one MEDIUM.
Original evidence: `.copilot-tracking/plans/2026-10-28/resident-logout-checks-525-critique.md`.

* PC-001 rejected: the worker claims an unavailable governing prohibition of
  `/tmp` writes. No such restriction exists in this parent execution; the user
  explicitly mandates `/tmp/ama-rpi-heavy.lock` and repository policy requires
  an external receipt. Retain the mandated shared lock and task-owned external
  paths; do not substitute a private lock or modify previous receipt environments.
* PC-002 accepted and applied: require pre-logout signed-in status and view 200,
  exact post-logout view 401, false/null session fields with presence enforced,
  and exact fence arguments in four helper test methods using subtests for bad
  statuses and missing/wrong fields. Readiness: Ready after these dispositions.

## Follow-Up Items

No new product follow-ups. Existing whole-issue acceptance is outside this correction.
Publication blocker: the required complete exact-head gate invokes az, forbidden
by the caller. Resolve that authority conflict separately before P02-T03.
Original Review: Complete / Residual work; source correction Conformant, no source
defects. RV-001 HIGH records only the known publication gate blocker.
P02-T02 is satisfied by committing the candidate and explicitly recording the
blocker, not by implying a gate pass. P02-T03 remains incomplete.

## Handoff

Research: `.copilot-tracking/research/2026-10-28/resident-logout-checks-525-research.md`.
Details: `.copilot-tracking/details/2026-10-28/resident-logout-checks-525-phase-details.md`.
Changes will record actual validation, amendments, blockers and publication status.

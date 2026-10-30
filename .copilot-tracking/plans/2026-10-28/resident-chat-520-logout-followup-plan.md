---
title: Resident chat logout and validation follow-up plan
ms.date: 2026-10-28
---

Task: 520-logout-followup. Parent: 520-review-correction. Phase: Review complete /
Not accepted; manual session stopped. Local commit handoff; publication blocked.

## Executive Summary

Shared cookie writes have been removed from logout, retaining old-token revocation
and explicit sign-out confirmation. Actual shared-browser tests prove newer
different/same-resident login state survives delayed logout. All five scenarios
passed with pinned axe (31 states, zero violations, six contrast incompletes),
all five project suites/static/types passed, and permitted non-az matrix and
infrastructure checks passed. One original child Review completed / Not accepted,
with no additional confirmed source defect. Publication is
blocked: mandatory az-dependent full-gate operations are prohibited, and partial
command evidence is not a full exact-head receipt.

## User Decisions and Requirements

* Full Research, Plan, Implement, Review loop in this worktree for #520 / PR #525.
* Fix RV-002 first, within existing files/methods, then establish RV-001 evidence.
* Nonblocking /tmp/ama-rpi-heavy.lock, 60-second retries up to 60 minutes.
* Run required unit suites, Ruff100, mypy and the gate where it does not need az.
* Commit with Conventional Commit and Copilot trailer; fetch, rebase on a new
  remote bot commit if present, normal push only, no closing keyword.
* Reply with fixing commit and resolve only the five actually verified threads.
* No az, merge, deployment, secrets, .env or private data.

## Goals

Remove logout cookie ordering defect and establish reproducible local evidence.

## Scope and Non-Goals

Existing app.py logout, SessionTests logout method, existing
shared_session_checks browser method, directly related src/api/README.md and
dated tracking artifacts. No new runtime method, cookie scheme, dependency,
separate browser harness or unrelated redesign. Earlier evidence is immutable.

## Functional Requirements

Logout revokes only its bound token; no response Set-Cookie can delete/replace
a later login. Ordinary sign-out, replay rejection, strict binding and fresh
per-login record-use permission remain. New login cookies, view and granted
permission survive delayed logout for different and same resident identities.

## Non-Functional Requirements

HttpOnly/Secure/SameSite authentication is unchanged. Actual loopback synthetic
Chromium/axe only; no external model or data. No lock bypass or fabricated receipt.

## Acceptance Criteria

* Existing HTTP logout regression asserts no Set-Cookie, revoked replay and
  signed-out session, with expiry unchanged.
* Shared-browser test holds accepted logout before browser response application,
  completes replacement login and renews permissions, then releases old response;
  exact cookies, own view, transcript and permission survive for both identities.
* All five original scenarios execute with pinned axe and recorded real results.
* Required permitted local checks have actual exits/skips; unavailable az/full
  receipt evidence and inherited human/hosted acceptance stay explicit.

## Test Ownership and Budget

Canonical targets: test_resident_demo_api.SessionTests.test_logout_revokes_and_replay_fails
and checks.resident_assistant_browser_check.shared_session_checks.
Removals: none. Maximum new test methods: zero. Extend these owners only.
Generated browser reports/screenshots and validation logs: new external task
directories. Semantic coverage is server revocation/no cookie effects; regression
coverage is actual delayed response application and all five original scenarios.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Logout correction

* [x] P01-T01: Remove logout Set-Cookie, extend owning HTTP regression and README.
* [x] P01-T02: Extend existing shared-browser regression for both replacement identities.

<!-- rpi:phase id=P02 -->
### [x] P02: Validation

* [x] P02-T01: Run focused regression, then corrected all-five Chromium/pinned-axe
  harness under caller's bounded nonblocking lock contract. Busy timeout blocks.
* [x] P02-T02: Required unit suites, Ruff100, mypy, JS checks; run permitted
  non-az canonical gate groups, retaining actual failures and coverage boundaries.

<!-- rpi:phase id=P03 -->
### [ ] P03: Review and publication

* [x] P03-T01: Reconcile evidence; execute one independent original Review.
* [ ] P03-T02: Commit implementation and dated original evidence; fetch and
  reconcile remote bot ancestry without force. Run exact-head permitted checks,
  respecting full-tier publication prerequisites.
* [ ] P03-T03: Only after publication gates pass, fetch main again, verify the
  external full receipt against current origin/main, obtain independent
  exact-head assessment, normal push and resolve the five verified threads.

Dependencies: P01-T02 depends on P01-T01; P02-T01 depends on P01; P02-T02 follows
browser outcome; P03-T01 depends on P02; P03-T02 depends on original Review;
P03-T03 depends on publication evidence and pushed exact head.

## Critique Disposition

Exactly one independent critique completed, original verdict Revise.
PC-001 adopted directly: use stdlib urllib upstream transport without a cookie
jar, assert browser cookies at acceptance/before/after release, and add a
test-only nonauthentication Set-Cookie marker on fulfillment to prove Chromium
cookie application happens at release. Preserve real response headers/body.
Compare full auth cookie including expiry, but allow /session CSRF expiry
refresh while requiring unchanged CSRF value/attributes.
PC-002 adopted directly: fetch current main, verify full external receipt and
independently assess exact head before normal push. No new user decision;
no repeated critique. Planning Readiness: Ready.

## Follow-Up Items

Human/resident/content, actual AT/native zoom and real-model acceptance remain
separate. Full gate's mandatory az preflight may block publication under explicit
no-az direction; do not silently downgrade or alter runner/protections.
Original child Review RV-001 retains the active publication evidence blocker
for a later authorized rpi-research task. RV-002 routes existing unfixed image
vulnerabilities to the image/base-dependency maintenance owner, outside this
narrow logout change. Neither route repeats the original Review.

## Sources and Handoff

Research: .copilot-tracking/research/2026-10-28/resident-chat-520-logout-followup-research.md.
Details: .copilot-tracking/details/2026-10-28/resident-chat-520-logout-followup-phase-details.md.
Readiness: bounded implementation and permitted validation complete; original
Review Complete / Not accepted. P03-T02 local commit prepared with original
evidence; exact-head full receipt and P03-T03 remain blocked. No push or remote
thread reply/resolution. Latest fetch: remote topic 685547ed, no new bot commit;
main remains 413ccaf253fce4566e855bae9d0a924b2a82b506. No rebase necessary.
Exactly one original critique already completed and disposed. Changes:
.copilot-tracking/changes/2026-10-28/resident-chat-520-logout-followup-changes.md.

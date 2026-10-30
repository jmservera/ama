---
title: Resident chat review correction plan
ms.date: 2026-10-28
---

Task: 520-review-correction. Status: Review Not accepted; publication blocked. Parent: 520.

## Executive Summary

Correct five reviewed session, preference and asynchronous UI bugs without
changing the bounded assistant or manual callback authority. Reuse verified
per-login opaque sid, retain CSRF protection, notify other tabs to clear stale
personal state, and fence protected requests and delayed responses. Extend
existing HTTP and actual Chromium/pinned-axe checks. Publication requires a
clean committed full gate, independent review, normal push and five resolutions.

## User Decisions and Requirements

* Continue open PR #525 on feat/resident-chat-520; fetch then rebase remote topic.
* Fix all five exact GraphQL findings and resolve each only after fixing/pushing.
* New dated RPI artifacts, earlier evidence untouched. No PR body keyword edits.
* No Azure, secrets, .env or private data. Ruff line length 100.
* Heavy lock nonblocking; retry every 60s up to 40m; never interrupt another owner.
* Conventional commit, authenticated noreply identity, exact Copilot trailer,
  normal topic push, never force or main.

## Goals

Prevent cross-login record/permission mixing and preserve resident input/focus.

## Scope and Non-Goals

Scope: resident_demo app/chat/web, owning HTTP fixture/tests, existing resident
assistant browser/axe harness and API README. No codec/schema/model changes,
dependency additions, visual redesign, cloud operations, or real acceptance.
The existing SQL browser, sensor-browser selector and image-check direct view
probes also receive the required binding header; their isolation assertions and
fixtures stay unchanged. This is coupled caller adaptation, not new functionality.

## Functional Requirements

* Return verified opaque per-login session_id on session/login, bind protected
  view/chat/agenda requests using X-Resident-Session and reject missing/mismatched
  ids before personal reads. Header is a binding, never an identity selector.
* Preserve same-CSRF pre-opened sign-in usability. Broadcast login/logout changes
  without personal facts; other tabs clear page/transcript/permissions and pending
  controllers. Fence view and assistant replies across identity changes.
* Share word tokenization for appointment routing/time preference.
* Manual button focuses visible callbacks, sign-in or error retry; launcher while
  loading. New draft survives old answer. Closed chat does not auto-search/focus.

## Non-Functional Requirements

Keep native semantics, manual/assisted routes, no works consent or booking from
chat, no private data/model transport. No persistent transcript or new credential.
Server and browser must both enforce identity rather than rely on notifications.

## Acceptance Criteria

* Two pre-opened tabs in one actual browser context: A permission/transcript and
  callback state clear on B login; stale sid plus B cookie cannot read or mutate.
  Repeat same-resident login proves per-login identity; no sid is an auth cookie.
* Punctuated morning/afternoon questions produce correct search period and only
  matching offered slots in actual HTTP/browser; proposals are not reservations.
* Page-error manual route focuses retry; loading fallback focuses launcher.
* Held successful answer preserves a later draft; unchanged submitted field clears.
* Held appointments answer after Escape or outside focus leaves focus unchanged;
  no automatic agenda request, manual route still available.
* Each browser scenario includes pinned axe and explicit focus/state assertions.
  Automated engineering does not establish human/AT/WCAG acceptance.

## Phase Checklist

<!-- phase: P01 -->
### P01: Correct protocol and browser behavior

* [x] P01-T01: Sid binding, cross-tab clearing, response fencing, shared tokens.
* [x] P01-T02: Visible manual focus, draft preservation, open-chat handoff guard.

<!-- phase: P02 -->
### P02: Regressions and documentation

* [x] P02-T01: Focused HTTP regressions and existing fixture sid support.
* [x] P02-T02: Extend actual browser/axe scenarios for all five; update API README.
* [ ] P02-T03: Targeted units, Ruff100, mypy, JS syntax and actual browser checks.

<!-- phase: P03 -->
### P03: Review and publication

* [x] P03-T01: One original independent post-implementation Review; preserve outcome.
* [ ] P03-T02: Commit evidence/source, full exact-head gate and receipt verification.
* [ ] P03-T03: Independent exact-head assessment, normal push, thread resolution.

## Test Ownership and Validation Contract

Canonical tests: src/api/tests/test_resident_chat_api.py, existing Client fixture
in test_resident_demo_api.py; browser: src/api/checks/resident_assistant_browser_check.py.
Coupled direct probes: resident_demo_browser_check.py, resident_sensors_browser_check.py
and resident_demo_image_check.py in the same checks directory, no added methods.
Removals: none. Maximum additions: 8 unit methods; extend existing browser run,
no new harness or generated tracked outputs. Semantic shared token helper is
covered by actual route/preferences; regression scenarios exercise real HTTP and
explicit held network replies. Keep axe/report/screenshots external.
Use /tmp/ama-520-documents-venv installed packages. Test before widening to API
suite; full gate is required because the changes include session controls.
Run full gate after original Review and commit; use current fetched origin/main,
--all --jobs 3 --lock-timeout 0, new external output directory. Retry only lock
admission every 60s up to 40m; do not retry failed checks as lock contention.

## Critique Disposition

Exactly one independent critique completed, original verdict Revise preserved at
.copilot-tracking/reviews/plans/2026-10-28/resident-chat-520-review-correction-critique.md.

* PC-001 accepted directly: one transition generation fences session discovery,
  login, view, logout and error continuations. Broadcast messages are only change
  hints; compare a fenced fresh /session result with tab-local sid, never adopt
  a message's identity or permission. Ignore hints without a current local sid.
  Delayed hints after newer login therefore do not erase valid current state.
  Server mismatch remains the race-safe security control.
* PC-002 accepted directly: exactly one canonical 16-lowercase-hex sid header,
  constant-time comparison after shape validation, deterministic 409 binding
  denial before personal reads. Invalid cookies still receive 401. Parameterize
  malformed/multiple headers in owning HTTP tests within fixed unit budget.
* PC-003 rejected: the worker asserted an execution prohibition on temporary
  paths that is absent from the parent instructions and conflicts with the
  explicit caller /tmp lock and required external gate policy. Existing installed
  venv and external task-owned temporary evidence are permitted; no foreign
  output will be modified. Do not change runtime or fixture architecture based
  on this unsupported claim.

No unresolved significant decision; finalize without another critique.

## Follow-Up Items

Original independent Review is Complete / Not accepted, preserved at
.copilot-tracking/reviews/logs/2026-10-28/resident-chat-520-review-correction-review.md.
RV-001 High: corrected browser/axe unverified after the bounded lock retry;
complete exact-head gate and publication remain unrun. Route evidence completion
to later rpi-research once heavy ownership is coordinated. Do not retry Review.
RV-002 Medium: a delayed logout response can clear cookies belonging to a newer
login despite JS epoch fences; route the coupled cookie-transition correction
to a distinct rpi-implement follow-up. No closure or acceptance is claimed here.

Human resident/content, AT/native zoom and real-model acceptance remain pending
as inherited; do not expand this correction to claim those gates.

## Sources and Handoff

Research: .copilot-tracking/research/2026-10-28/resident-chat-520-review-correction-research.md
Details: .copilot-tracking/details/2026-10-28/resident-chat-520-review-correction-phase-details.md
Changes: .copilot-tracking/changes/2026-10-28/resident-chat-520-review-correction-changes.md
Critique readiness: all five acceptance criteria and fixed test budget recorded.

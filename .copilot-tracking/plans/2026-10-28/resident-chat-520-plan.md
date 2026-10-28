---
title: Resident chat 520 implementation plan
description: Bounded resident chat and synthetic callback agenda
ms.date: 2026-10-28
---

Task ID: 520. Slug: resident-chat-520. Status: Ready for implementation.

## Executive Summary

Extend the existing resident demonstrator, not the retired MVP. Add a shared
bottom-right launcher and nonmodal keyboard-accessible chat window. Preserve
the bounded Azure advisor; route other supported questions deterministically.
Use a persistent, explicitly local synthetic callback agenda, never the works
agreement controls. Dates/preferences determine suitability; residents confirm
one proposed free slot before booking. Human/AT acceptance remains pending.

## User Decisions and Requirements

* Full ordered RPI loop with dated artifacts, independent critique and Review.
* Work on feat/resident-chat-520 in the specified worktree.
* Read issue #520; build on #469/#164, src-only, tests outside packages.
* Fluent 2, WCAG baseline, content standard; no design-taste app redesign.
* Synthetic only; no secrets, .env, private data, Azure deployment or uv.
* Relevant units, Node, real local HTTP and Playwright/axe; nonblocking heavy lock.
* Conventional commit with required trailer and authenticated noreply identity.
* Full local exact-head gate before one push and PR; Refs #520, never Closes.

## Goals

Accessible optional resident help with bounded own-record answers and a usable,
consent-preserving appointment path independent of model availability.

## Scope and Non-Goals

Resident_demo app/assets, local synthetic agenda, focused tests/checks and API
README. No staff authority changes, SQL showcase writes, works commitments,
cloud resources, operational acceptance or private datasets.

## Functional Requirements

* Launcher available before/after sign-in and on errors; anonymous help has no
  personal data. Native open/close, Escape, focus return, no modal focus trap.
* Preserve fixed questions; bounded free-text host routing, no raw questions
  or resident identity passed to models. Unknown/out-of-scope asks abstain.
* Explicit server-checked `use_record: true` before every personal assistant
  request, including legacy topics, and agenda lookup/mutation. No session-wide
  implied permission; reset UI checkbox and replies on withdrawal/session change.
  Update tightly coupled legacy tests to the intentionally changed contract.
  Own home,
  case, callback bookings and unknown works-consent state; never other cases.
* Dated local regulatory source/provision, source/retrieval dates, unverified
  currentness, no legal conclusion. Safety routes directly to human/emergency
  help, explicitly not sent to staff by chat.
* Explicit local agenda setup only. Stored future slots filtered by earliest
  date and morning/afternoon/any, up to three proposals. Case-bound short-lived
  offer tokens; atomic book only with boolean confirmation. Idempotent retry,
  collision/revocation/expiry refusal, own-booking cancel. No works consent.
  Local operator assisted cancellation uses the explicit agenda CLI with a
  booking reference, not an exposed unauthenticated staff HTTP endpoint.
* Every proposal/confirmation/receipt states synthetic callback only, no live
  contact or works booking. Operational appointments/consents remain Unknown.
  Store aware UTC instants; filter and display Europe/London. Sort ascending by
  start instant then stable slot ID. Recheck future time when confirming.
* Manual slot choice plus housing officer/phone/office route, no invented number.
* Off/unavailable AI explicitly labelled; agenda failure is not empty success.

## Non-Functional Requirements

Exact request schemas, same-origin/CSRF, fresh authorization, no-store.
No local/session storage of chat; clear on sign-out/session loss.
Persistent SQLite agenda file only when explicitly configured, no default data.
Fluent tokens, visible focus, >=44px controls, 320px reflow, reduced motion,
status/error announcements, no overlay obscuring keyboard focus.

## Acceptance Criteria

AC1 launcher keyboard/touch/pointer and focus/reflow evidence on all page states.
AC2 cross-resident HTTP/proposal/book/cancel and model-boundary denial tests.
AC3 regulatory exact metadata/refusal and safety/manual routes.
AC4 real persistent free-slot search, 1..3 proposals, confirmation/cancel/races.
AC5 preserved Azure route, explicitly labelled offline path.
AC6 automated units/browser/axe pass, human and AT explicitly Not run.
AC1 includes rendered 200% root text resizing and 400% equivalent CSS reflow
(320px viewport from 1280px), with method limits recorded, not device scale.
AC2 requires absent/false record-use refusal before case/model calls.
AC4 is scoped to the local synthetic callback inventory, including assisted
cancellation; operational/live appointments and missing record types are unmet.

## Phase Checklist

<!-- phase: P01 -->
### P01 - Backend and agenda

* [x] P01-T01 Add local persistent synthetic callback agenda and exact schemas.
* [x] P01-T02 Add host-routed chat and regulatory answers preserving Azure route.

<!-- phase: P02 -->
### P02 - Resident app

* [x] P02-T01 Add shared launcher/window, consent, transcript and safe teardown.
* [x] P02-T02 Wire proposal/confirmation/cancel and independent manual controls.

<!-- phase: P03 -->
### P03 - Validation and evidence

* [x] P03-T01 Add focused HTTP/agenda tests and update existing browser coverage.
* [x] P03-T02 Run units, lint/types, Node, local Chromium/axe under heavy lock.
* [x] P03-T03 Update API README, changes evidence and original independent Review.
* [ ] P03-T04 Commit then run full exact-head gate, verify current main, publish PR
  only if gates permit.

## Test Ownership and Change Budget

Canonical tests: extend API test_resident_assistant_api.py where appropriate;
add at most two API test modules for agenda/chat contracts. Extend existing
resident_assistant_browser_check.py rather than adding a second competing
browser harness. Reuse pinned axe loading/scan helpers. No test removals.
No generated source targets. Semantic contracts (confirmation, concurrency,
revocation, isolation, unknowns) plus existing route regressions. API units,
ruff/mypy, Node, focused browser and full runner are required evidence.

## Critique Disposition

Executed once, original verdict Revise. All six findings accepted as direct
planner corrections; no conflicting user direction or new decision needed.
PC-001: explicit consent on legacy and new paths; zero-lookup/model negative tests.
PC-002: local operator assisted-cancel CLI and resident instructions.
PC-003: visible synthetic/no-live-contact qualification and scoped acceptance.
PC-004: UTC storage, Europe/London filters/display, sorted first three,
fresh future check and time-boundary/race tests.
PC-005: 200% root text and 400%-equivalent reflow tests with limits.
PC-006: original Review -> commit -> fetched base/full gate -> fresh fetch and
receipt verification -> independent exact-head external assessment -> verify
again immediately before push -> PR. Exact-head assessor must bind commit,
base and receipt; corrections/base/tool/dirty input changes block push and
require a new candidate/gate. Do not commit the authoritative receipt or final
external assessment. Busy lock/missing prerequisites block without fallback.

## Follow-Up Items

Human wording/resident usability, AT acceptance, real-model #164 evaluation and
operational agenda integration remain separate. No live appointment is claimed.
Original Review: Partial / Residual work. RV-001 Low (remaining-work regulatory
summary) is routed to a later documentation amendment, not corrected/reviewed
again in this task. Raw external validation requires inspection at the
separate final exact-head assessment.

## Handoff

Implementation reconciled: P01/P02 and P03-T01/T02 complete, P03-T03 ready
for original independent Review, P03-T04 remains post-Review publication work.
Full API discovery 1160 tests OK (314 opt-in skips); final focused 45 OK;
16 Chromium/axe states zero violations; API static checks and Node pass.
Human/AT, operational agenda and complete exact-head gate remain distinct.

Research: .copilot-tracking/research/2026-10-28/resident-chat-520-research.md.
Details: .copilot-tracking/details/2026-10-28/resident-chat-520-phase-details.md.
Changes: .copilot-tracking/changes/2026-10-28/resident-chat-520-changes.md.

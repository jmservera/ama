---
title: Resident chat fallback and dock plan
ms.date: 2026-10-30
---

Task: resident-chat-dock-520-563. Status: Ready after one critique.

## Executive Summary

Improve locally reproducible admission refusals for common safe wording, explain
bounded inference failures, and add resident-only native sizing/right-edge dock
controls. Preserve consent, own-record projection, all protected routes and
employee defaults. Actual live failure/configuration remains uninspected.

## User Decisions and Requirements

* Full ordered RPI loop with dated artifacts. Refs #520 and Refs #563.
* Use this worktree/branch and main d986c4c4; local commit only, no push.
* No live AI, ledgers, credential files, Azure, deployment or live sign-in.
* Resizable resident chat, full-height right dock, keyboard/native semantics,
  reduced motion; persisted sizing optional.
* Required API discovery, Ruff, formatting, mypy and actual local Playwright.
  Heavy commands use the shared lock.

## Goals

Make ordinary supported questions reach generation without relaxing authority.
Make reasons for fallback observable without private logs. Let residents read
long replies in a larger bounded pane.

## Scope and Non-Goals

API host grammar/adapter, resident integration, shared widget opt-in, tests,
browser check and directly related API documentation. No agents changes:
resident requests do not use its independent employee retrieval.
No new retrieval, model client, activation, budget/expiry changes, arbitrary
question passthrough, persistent browser text or framework/design overhaul.

## Functional Requirements

* Whole-message matching accepts tested polite wrappers/common paraphrases.
* Safety/legal/consent/action/out-of-scope handling remains host-owned.
* Fallback labels/logs use fixed reason categories, never exception details.
* Native range controls adjust width/height; dock toggles full right edge,
  retaining draft, thread, scroll intent, Escape and focus return.
* Employee widget behavior remains opt-out by default.

## Non-Functional Requirements

Fluent tokens, plain wording, visible focus, native names/states and no resize
animation. Bound geometry at 320/390/1280px, short windows and enlarged text.
Consent precedes data/model use. Source IDs, cost, response and payload checks
remain fail closed. No unrelated cleanup.

## Acceptance Criteria

* AC1: common safe wording reaches actual local HTTP/model adapter with
  constructed grounding; protected/appended-action tests still refuse.
* AC2: invalid/expired/limited/unavailable model responses retain rules/human
  help with specific safe reasons and no private diagnostics.
* AC3: native keyboard and pointer sizing, full-height right docking/undocking,
  long-history scrolling, draft retention and focus work in actual Chromium.
* AC4: targeted and full API commands plus web guideline review are recorded;
  live model/live site/AT/human approval are explicitly unproven.

## Test Ownership and Change Budget

Canonical tests outside packages: test_resident_chat_api.py (semantic admission,
privacy and protected routes), test_resident_aoai.py (semantic fallback reason
and parse/accounting contracts). Add at most 5 unit methods, extend existing
question tables rather than duplicate suites. Exact removals: none.
Extend checks/resident_generated_answer_browser_check.py with at most one
focused geometry/keyboard helper and latest-response assertions. Generated
targets: external JSON/screenshots only; no generated runtime sources.
Existing shared-widget browser check remains employee/resident regression
coverage. Validation: required full API discovery, Ruff, format, mypy, JS parse,
generated-answer and shared-widget browser checks; complete final gate after
commit, subject to no-cloud and installed local prerequisites.

## Phase Checklist

<!-- P01 -->
### P01: Repair bounded admission and diagnostics

* [x] P01-T01 Add common complete-message forms and negative suffix coverage.
* [x] P01-T02 Add fixed fallback categories and adapter regression tests.

<!-- P02 -->
### P02: Resident sizing and docking

* [x] P02-T01 Opt-in native controls, responsive CSS and resident integration.
* [x] P02-T02 Extend actual local browser coverage and API guide.

<!-- P03 -->
### P03: Validate and review

* [ ] P03-T01 Run required local commands under lock and refresh web guidelines.
* [ ] P03-T02 Run one independent Review, retain findings and commit locally.
* [ ] P03-T03 Attempt external complete gate and record publication limits.

## Critique Disposition

One independent critique executed, original verdict Revise preserved in
.copilot-tracking/plans/2026-10-30/resident-chat-dock-critique.md.

* PC-001: accepted completion-claim gate. Any material Review finding leaves
  the candidate unaccepted/blocked, not a conformant completion. The one-pass
  Review outcome is immutable; its routed fixes belong to a later task.
* PC-002: rejected as unsupported. The critic reports a temporary-directory
  prohibition that is absent from the actual caller/runtime instructions.
  The caller explicitly mandates /tmp/ama-rpi-heavy.lock. Use that exact lock,
  existing external tools and fresh external evidence. No private lock/bypass.
* PC-003: accepted. Preserve historical message anchor and proportional
  within-message offset during sizing/dock changes, and keep bottom-following
  readers at the end. Test both states with focus retained; reopen retains
  the pre-existing bottom behavior. Details updated.

No unresolved planning blocker or significant user decision remains.

## Follow-Up Items

Live authenticated model evidence for #563 remains outside authority.
Human/AT accessibility and current legal/operational approval remain separate.
Final browser regression is blocked by three exhausted 600-second shared-lock
waits. Preserve earlier passing and failing evidence; no final-candidate browser
pass is claimed. Current origin/main has advanced beyond the owner-selected
base; coordinator integration is required before a publishable complete gate.
P03-T01 remains incomplete for that browser requirement.

## Sources and Handoff

Research: .copilot-tracking/research/2026-10-30/resident-chat-dock-research.md
(C1-C7, W1). Details:
.copilot-tracking/details/2026-10-30/resident-chat-dock-phase-details.md.
Changes destination:
.copilot-tracking/changes/2026-10-30/resident-chat-dock-changes.md.

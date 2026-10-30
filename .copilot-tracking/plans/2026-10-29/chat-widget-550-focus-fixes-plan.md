<!-- markdownlint-disable-file -->
# RPI Plan: Chat focus review follow-up

## Metadata

Task 550-focus-fixes; slug chat-widget-550-focus-fixes; parent 550.
Date 2026-10-29. Ready; one critique Complete/Revise, dispositions below.
Research: .copilot-tracking/research/2026-10-29/chat-widget-550-focus-fixes-research.md.
Details: .copilot-tracking/details/2026-10-29/chat-widget-550-focus-fixes-phase-details.md.

## Executive Summary

Hide the shared nonmodal popup when focus leaves it (except its visible launcher),
without cancelling work or redirecting focus. Remove employee async setup/reply
refocusing; polite live regions announce updates. Prove these independent
behaviors with Node regression tests and the actual-app Playwright check.
Original adverse Review remains preserved; this selected follow-up owns closure.

## User Decisions and Requirements

* Fix original RV-001/RV-002 through short Research, plan update, Implement, Review.
* Keep WCAG 2.2 focus-not-obscured, no reply focus theft, polite live updates;
  move focus only on user actions, not incoming setup/success/error.
* Add regression tests and update local Playwright coverage.
* Use /tmp/mv, specified source/test PYTHONPATH; unittest, ruff check/format,
  mypy, node --check and local browser. No az, push or rubric-score edits.
* Commit with requested Copilot trailer; no publication or human acceptance claim.

## Goals

Resolve both concrete defects, preserving audience privacy, drafts, history,
in-flight operations and disposal fencing.

## Scope and Non-Goals

Shared widget, employee adapter, new bounded unit module, existing browser check,
API README and RPI evidence only. No CSS redesign beyond removing the short-height popup/launcher overlap, modal trap, backend change,
historical deletion, original verdict rewrite or publication.

## Functional Requirements

Document focusin hides using hide(false) for targets outside popup/launcher;
dispose removes that listener. Open/Close/Escape and explicit submit validation
retain their user-driven focus behavior. Async setup/replies never focus input;
access denial must not redirect external focus. Hide never cancels pending work.

## Non-Functional Requirements

Keep native controls, polite named log/status and explicitly polite inline errors,
Fluent tokens and lifecycle guards. No geometry reads in production.

## Acceptance Criteria

RV-001: at 320x800 before resident sign-in, Open then Shift+Tab twice focuses
Sign in, hides popup and leaves focused control visibly hit-testable. Both
audiences: forward and reverse Tab exit hide without trapping or focus return;
draft/history/skill preserved on reopen, pending work continues. At 1280x500 in
both apps, keyboard-focused launcher remains hit-testable above/below no overlay,
and one activation closes/reopens correctly.
RV-002: held setup/thread/ask success/error does not change deliberately chosen
external textarea, visible launcher or internal control focus; no async focus
even if popup stays visible. Reply/status updates remain polite. Both shared
audiences keep external focus through current reply completion.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Focus correction and regressions

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Fix shared focus lifecycle and employee continuations

Add/removable outside-focus handler, remove setup/finally focusInput, guard
access-loss focus routing against external theft. No other authority changes.

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Behavioral unit and actual-app browser coverage

Test ownership: at most one new test module tests/test_chat_widget_focus.py;
actual shared widget/adapter execution using Node VM follows existing prior art.
Browser assertions belong in checks/chat_widget_browser_check.py. Removals: none.
Canonical sources: src/api/src/zava_forward/api/web/{chat-widget,chat}.js.
No generated source targets. Migrate only the employee check's obsolete
post-setup input-focus expectation to heading-focus preservation, retaining its
keyboard/skill/denial/lifecycle coverage. Preserve all other prior assertions; adapt harness to
reopen after intentional outside-focus dismissal. Include regression-negative
evidence against original source to show both tests detect old defects.
Implementation amendment: migrate two resident audience outside-focus oracles
from visible-then-manual-close to hidden-immediately with unchanged target focus.
These checks encode RV-001's old behavior; preserve pending result, no agenda,
retained draft and consent/session assertions. No source scope expansion.

<!-- rpi:phase id=P02 -->
### [x] P02: Validation, evidence and independent Review

Dependency: P01.

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Validate requested local surfaces and document

Run original related 14 unittest modules plus new focus module, opt-in
test_chat_panel; full API ruff check, format --check, mypy; isolated browser-check
lint/format and node syntax. Run shared actual-app Playwright and existing
employee and resident audience checks (mandatory). Output outside repository. Record commands,
counts and limitations; update README/original changes with follow-up evidence.

<!-- rpi:task id=P02-T02 -->
#### [x] P02-T02: One independent Review and local commit

Fresh independent read-only review of changed source/tests and recorded results.
Preserve original findings/verdict; append resolved status with new review pointer
only when evidence supports closure. Route any new findings without source edits
or repeat Review in this task. Resolve privacy-safe gh identity, commit source
and dated evidence with trailer, do not push. No full publication gate claim.

## Critique Disposition

One final-candidate critique Complete / Revise, preserved at
.copilot-tracking/reviews/plans/2026-10-29/chat-widget-550-focus-fixes-plan-critique.md.
PC-001 accepted: remove the short-height override that overlaps launcher; verify
1280x500 hit-testing and single-click toggling for both apps.
PC-002 accepted: migrate employee setup-focus oracle only; run both audiences.
PC-003 accepted: error retains role=alert for existing selectors, explicitly
aria-live=polite and aria-atomic=true; test setup/reply errors without focus.
PC-004 accepted: controlled 403/404 denial at setup/thread/ask must preserve
external/launcher focus and recover popup-owned focus; retain actual 401 session
coverage in the existing employee checker.
PC-005 rejected as inapplicable worker-only environment restriction: parent has
no prohibition on /tmp/mv or external session evidence; owner explicitly selects
that existing runtime and test -x succeeded. No runtime substitution/install.
No new product decision, repeat critique or unresolved planning blocker.

## Follow-Up Items

Original unrelated mobile summary-height baseline, human accessibility/live-site
acceptance and complete exact-head publication gates remain separate.

## Handoff

Changes path:
.copilot-tracking/changes/2026-10-29/chat-widget-550-focus-fixes-changes.md.
All implementation/checks and one independent Review complete (Conformant,
no new findings). Original RV-001/RV-002 resolved through appended evidence,
original adverse outcome preserved. The local commit containing this closeout
is the commit execution receipt; no source changes after Review and no push.
Human/live acceptance and publication gates remain separate.

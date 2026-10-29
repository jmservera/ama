<!-- markdownlint-disable-file -->
# RPI Plan: Shared chat widget

## Task Metadata

* Task ID: 550; slug: chat-widget-550; date: 2026-10-29.
* Planning status: Ready; one critique completed, compatible findings resolved.
* Details: .copilot-tracking/details/2026-10-29/chat-widget-550-phase-details.md
* Critique: .copilot-tracking/reviews/plans/2026-10-29/chat-widget-550-plan-critique.md

## Executive Summary

Build one dependency-free native widget in the staff web asset directory and
serve the same bytes from both applications. Audience-specific adapters retain
the current API, privacy, consent and access boundaries. Fix false home-summary
routing conservatively, with honest human handoff for unsupported questions.

### What You May Not Know

History persists on close/reopen within a session/context, not across identity or
case changes, consent withdrawal or page reload. Raw resident text still never
reaches AI. Existing rules output must not be relabelled as AI-generated.
Local automation cannot prove live-site, screen-reader or operational acceptance.

## User Decisions and Requirements

* Execute Research, Plan, Implement and Review in order, preserving dated evidence.
* One bottom-right icon launcher/popup and persistent scrolling chat for both sites.
* Pinned textarea; Enter sends, Shift+Enter newline, send control, compact skills.
* Employee general plus five bounded skills through #503; resident assistant only.
* Attach/voice controls disabled with visible reasons if unsupported.
* Thin truthful AI/rules label, collapsed sources, explicit prior resident consent.
* Rat/unrelated free-text questions never return the home summary.
* Preserve Fluent 2 tokens, native semantics, visible errors, 200ms loading,
  reduced motion and #503/#525/#541 boundaries.
* Use src source only; tests/checks outside package; local /tmp/mv validation.
* No az/Azure, no push, no rubric-score edits; Conventional Commit with trailer.

## Goals

Normal reusable chat interaction without changing backend authority.

## Scope and Non-Goals

In scope: shared JS/CSS, both adapters/entry points, static serving, narrow resident
routing fix, tests/check and API README. No framework/dependency replacement,
unbounded LLM, persistent browser storage, operational approvals or publication.

## Functional Requirements

Shared factory owns layout, thread, keyboard handling, busy/error feedback,
source disclosure and show/hide; adapters own APIs, consent and invalidation.
Close/reopen preserves conversation and pending reads; hiding is not disposal.
Pending results may append while hidden but never move focus. Context/session/
access loss disposes and invalidates every continuation.
Resident callback suggestions use an explicit manual action, leaving chat open
after answers; no booking or consent decision from text.

## Non-Functional Requirements

Native named controls, named nonmodal dialog/log, focus return and Escape.
No focus trap in a nonmodal popup. User/model strings rendered as text only.
Scrollable bounded-height thread with non-scrolling composer, responsive at
320/390/1280 CSS px, reduced-motion static loading after 200ms.

## Acceptance Criteria

All nine issue criteria map to browser assertions: shared asset bytes/mounting,
launcher, multi-turn retention/newest-bottom/pinned composer, close/reopen,
Enter/Shift+Enter, six/one choices, disabled controls and reasons, truthful
compact label/details, consent before requests, rat HTTP regression, delayed
loading/errors, keyboard/focus/reflow/reduced motion. Existing role, audit,
consent and session regressions remain passing.

## Sources

Research: .copilot-tracking/research/2026-10-29/chat-widget-550-research.md,
C1-C5 and W1-W4. Owner request and issue #550 are authoritative.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Shared widget and adapters

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Implement shared layout and audience adapters

Add web/chat-widget.js and web/chat-widget.css, wire both entry points and
resident allowlisted static assets. Preserve route/session/access disposal.
The existing case assistance panel delegates general questions to the same popup;
its separate proposal and regulatory controls retain their existing boundaries.
Shared employee entry loads the API privacy warning before enabling input.

<!-- rpi:phase id=P02 -->
### [x] P02: Resident intent regression

Dependency: none (can be developed independently of UI).

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Restrict home summary routing to explicit supported intents

Retain safety precedence; unknown concerns get human contact, not diagnosis.

<!-- rpi:phase id=P03 -->
### [ ] P03: Validation and documentation

Dependencies: P01 and P02.

<!-- rpi:task id=P03-T01 -->
#### [x] P03-T01: Test shared browser behavior and retained boundaries

Test ownership: resident route/HTTP regression belongs to
src/api/tests/test_resident_chat_api.py; shared DOM/browser acceptance belongs to
new src/api/checks/chat_widget_browser_check.py. At most one new test module if
static wiring coverage is necessary. No tests removed. Existing employee and
resident browser checks may be updated for intentional DOM/label changes only,
not weakened boundary assertions. No generated source targets.
Run relevant unittest modules from src/api with specified PYTHONPATH and /tmp/mv;
ruff check/format, CI mypy, node syntax and actual local Playwright for both apps.
Record exact commands, results, failures/corrections and limitations in changes.

<!-- rpi:task id=P03-T02 -->
#### [ ] P03-T02: Document, review and commit

Update API README. One independent post-implementation Review, route findings
without another Review. Commit implementation/evidence with privacy-safe identity
and required trailer; never push. Full exact-head publication gate and human
acceptance remain prerequisites to later publication.

## Dependencies

Merged #503 baseline confirmed at 9b74ac8d; existing resident #541 contracts.
Available /tmp/mv Python/ruff/Playwright. Synthetic-only local browser fixtures.

## Critique Disposition

Original verdict Revise preserved. PC-001 resolved directly with hide-versus-
dispose contract and operation-owned cleanup in phase details. PC-002 resolved
with explicit shared-script readiness/recovery and bounded failure scenarios.
PC-003 resolved with measurable timing/layout/keyboard assertions below.
No significant/divergent user decision required; no second critique.

## Follow-Up Items

* Human assistive-technology and live-site acceptance remain owner activities.
* Owner-maintained case-journey baseline: 320px case summary is 1705.97px from
  viewport top against the existing <=1600px oracle, identical before/after this
  change. Investigate separately; no unrelated layout fix or weakened assertion.
* Before future publication, run the full external exact-head local gate and
  required human/hosted approval. This task commits locally without pushing.

## Handoff

Changes path: .copilot-tracking/changes/2026-10-29/chat-widget-550-changes.md.
P01/P02 and local validation/documentation complete. P03-T02 retains one
independent Review and requested local commit as explicit remaining closeout
work. The broader case checker has the documented unchanged baseline failure;
all directly affected chat lifecycle assertions passed before that failure.
Do not publish; no human accessibility or operational acceptance is claimed.

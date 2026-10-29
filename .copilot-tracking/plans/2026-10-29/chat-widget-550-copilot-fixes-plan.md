---
title: Chat widget 550 Copilot findings plan update
description: Four bounded widget corrections with executed regressions
ms.date: 2026-10-29
---

## Task Metadata

Task 550-copilot-fixes; slug chat-widget-550-copilot-fixes; parent 550-rebase.
Continuation of the original chat-widget-550 plan, preserving prior outcomes.

## Executive Summary

Fix chat overlay order, Close hover contrast, reply-follow behavior and
same-context launcher toggling. Existing unit/browser regressions and all
requested local checks now pass. One independent Review is Complete /
Conformant with no source defects. The containing local commit completes
persistence; no push is authorized.
No push, Azure action, rubric edit or publication gate is authorized.

### What You May Not Know

A focused Sources disclosure must suppress following even when the log was
at the bottom. A nonmodal popup still dismisses on outside focus without
redirecting it. Expanded-map native dialogs remain in the browser top layer.

## Sources

Research: .copilot-tracking/research/2026-10-29/chat-widget-550-copilot-fixes-research.md.
Prior plan: .copilot-tracking/plans/2026-10-29/chat-widget-550-rebase-plan.md.

## User Decisions and Requirements

* Fix all four supplied real findings on feat/chat-widget-550, PR 556.
* Run short Research, plan update, Implement and Review in this invocation.
* Pull --rebase first; completed cleanly, already up to date.
* Place employee chat above map (through 1000), below account menu (1200).
* Ensure close hover readable on both applications.
* Follow new messages only when previously at bottom and focus outside history.
* Install opener/decorate only when no employee widget exists.
* Preserve WCAG focus-not-obscured, no focus theft and reduced motion.
* Use /tmp/mv and supplied API source/test PYTHONPATH; requested static,
  chat-unit and local Playwright checks. Extend chat_widget_browser_check.py.
* Commit locally with required coauthor; do not push, use az or edit rubric.

## Goals

Resolve each finding with observable regression protection, no unrelated work.

## Scope and Non-Goals

Three web assets, existing focus unit file, existing browser check and directly
related API README. No dependency, model, infrastructure or framework change.

## Functional Requirements

Popup and launcher use tier 1100. Close hover explicitly uses soft background
and brand text. message captures pre-append bottom state (one CSS-pixel
rounding tolerance) and history focus before adding; only eligible append
follows. install leaves widget-owned toggle/ARIA intact on refresh.

## Non-Functional Requirements

Native controls, polite announcements, existing focus dismissal and reduced
motion retained. No smooth scrolling or new focus calls. Local synthetic
loopback applications only; no external model/private dataset.

## Acceptance Criteria

* Browser hit tests cover real employee map panes, controls and summary card
  under both popup/launcher, and account-menu priority above chat.
* Computed Close hover text/background contrast >=4.5:1 on both sites.
* Delayed replies preserve older-history scroll/focus, including focused
  Sources at bottom; an eligible bottom reader follows.
* Same-context employee route refresh retains widget identity/draft/ARIA and
  launcher closes/reopens correctly from both open and closed states.
* Chat units, Ruff check/format, mypy, JS node --check and extended Playwright
  all pass or precise blockers are recorded without a false acceptance claim.
* One critique and one independent Review retained; local commit, no push.

## Test Ownership and Change Budget

Existing test_chat_widget_focus.py owns executable Node units; existing
checks/chat_widget_browser_check.py owns real-layout and application regression.
Removals: none. Maximum additions: two unit test methods, four bounded browser
helper functions, zero new test files. No generated targets. Semantic focus,
scroll, toggle and contrast checks, not only CSS/source string matching.
Preserve all existing browser assertions. Static checks do not prove UX.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Correct and regress

* [x] P01-T01 Implement four corrections and unit/browser regressions.
* [x] P01-T02 Update directly related README behavior.

<!-- rpi:phase id=P02 -->
### [x] P02: Validate

* [x] P02-T01 Execute requested static, chat unit and local browser checks.
* [x] P02-T02 Record per-finding evidence, adverse attempts and limitations.

139 tests pass without skips; final API/isolated-harness static checks pass.
Complete two-site Playwright attempt5 passes all old/new assertions. Negative
controls reject original JS in both new units and original CSS in both new
browser assertions. Route refresh deliberately focuses the workspace, hiding
the nonmodal widget; retained ownership then proves launcher opens and closes.
This is existing intended behavior, not a new divergence.

<!-- rpi:phase id=P03 -->
### [x] P03: Review and persist

* [x] P03-T01 Reconcile evidence and execute one independent Review.
* [x] P03-T02 Record outcome and commit locally, leaving no push.

The local commit containing this completed checklist is the persistence
receipt, verified afterward with clean worktree, required trailer, private
author/committer identity and unchanged rubric. No publication is performed.

## Critique Disposition

Exactly one independent critique executed by widget-fixes-plan-critique:
Complete / Pass, zero findings, no user decision required. Test ownership,
no removals and addition limits confirmed. Ready for implementation.
Artifact: .copilot-tracking/reviews/plans/2026-10-29/chat-widget-550-copilot-fixes-plan-critique.md.

## Follow-Up Items

* Publication exact-head gate, hosted CI and human/live acceptance remain
  coordinator-owned, outside this local-only correction (Review RV-001, Low
  residual obligation, not a source defect).

## Handoff

Details: .copilot-tracking/details/2026-10-29/chat-widget-550-copilot-fixes-phase-details.md.
Changes: .copilot-tracking/changes/2026-10-29/chat-widget-550-copilot-fixes-changes.md.

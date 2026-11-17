---
title: Issue 159 chat keyboard and live-region research
ms.date: 2026-11-16
---

## Scope

Criterion: panel is keyboard operable, screen-reader tested and announces new messages. Validation tier: focused. Manual assistive-technology (AT) testing stays a human gate.

## Disposition

Research executed. Planning Readiness: Ready.

## Findings

* `chat-widget.js` already provides: role dialog, heading focus on open, Escape and Close return focus to the launcher, Enter sends and Shift+Enter/IME do not, log with `role="log"` polite additions and a scrollable `tabindex=0`, a polite status region, and an `role="alert"` error region (`src/api/src/zava_forward/api/web/chat-widget.js`).
* `chat.js` states answer, withheld, refused and fallback outcomes in the status line (`statusFor`) and errors in plain language with owner and next action.
* Baseline: 75 unit tests (`test_assistant_panel_a11y_159`, `test_chat_widget_focus`, `test_chat_panel`, `test_regulatory_chat_live_region_semantics`) pass; `employee_chat_browser_check` passes with pinned axe 4.10.3 (sha256 880970c0...).
* `chat_widget_browser_check` fails at baseline in its `resident` stage (320px external focus, `signin-button` below the viewport) before any change. This is pre-existing, outside the workbench panel, and not addressed.
* Gap: Enter submits a multi-line textarea but nothing tells keyboard users (WCAG 3.3.2 Labels or Instructions; plain-language standard). The Shift+Enter and Escape behaviours are undiscoverable.

## Boundaries

No manual screen-reader result exists; none is claimed. Resident assistant `aria-describedby` strings are out of scope (workbench only), though the shared widget shows the visible hint there.

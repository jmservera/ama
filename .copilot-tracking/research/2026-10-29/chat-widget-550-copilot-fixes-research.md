---
title: Chat widget 550 Copilot findings research
description: Focused evidence for four shared chat corrections
ms.date: 2026-10-29
---
<!-- markdownlint-disable-file -->

## Research Brief

Task 550-copilot-fixes, parent 550-rebase. Status: Complete.
Output mode: convergence. Posture: focused, selected from the caller's short
research request, four named findings and fixed validation scope.
Evidence root: .copilot-tracking/. Audience: implementation and independent
review. Scope: shared widget CSS/JS, employee adapter and existing browser
check. Non-goals: redesign, model/backend changes, Azure, publication, rubric.
Requested output: verify causes, alternatives and regression strategy.

## Extension Registry and Provenance

Repository instructions apply throughout: Fluent tokens, WCAG 2.2 focus
visibility, no focus theft, reduced motion and local-only persistence.
Selected rpi-research and web-design-guidelines. Current guidelines retrieved
from their source on 2026-10-29. No visual redesign skill: behavioral bug fixes,
not an existing-app design upgrade or public page. Research inline: one small,
continuous trace; no independent research lane warrants delegation.

## Participation, Direction Controls and Prior Knowledge

No clarification needed: caller supplies exact failures, branch, environment,
commands and limits. All four RPI stages explicitly authorized; mode stays
manual. Prior rebase state and plan/changes verified as historical evidence,
not fresh proof. Previous review was conformant at its narrower integration
boundary and is not rewritten. Session-history search returned no matches.
Initial worktree clean; pull --rebase first returned Already up to date.
PR 556 is open, head feat/chat-widget-550, base main.

## Questions and Scope Criteria

* Q1: Which stacking tier preserves map and account-menu intent?
* Q2: Which explicit hover tokens retain readable contrast on both sites?
* Q3: How to preserve older history and focused Sources while following replies
  only for a reader already at the bottom?
* Q4: How to retain the widget toggle across same-context route refresh?
* Each correction needs a browser regression assertion; behavior tests must
  execute the actual shipped widget, not just match source text.

## Research Cycle Log

### Cycle 1, Wider

Read shared widget, employee install/route lifecycle, existing focus units,
two-site browser check and UX baselines. All four supplied causes are present.
Existing local synthetic fixtures and pinned axe provide the required browser
path without external data/model calls. Reflection: preserve these harnesses.

### Cycle 1, Deeper

The history has native overflow and polite live updates; appending currently
always scrolls. A pre-append bottom measurement plus active-element containment
can preserve position without moving focus. install currently unconditionally
overwrites onclick even when an existing widget owns the toggle.
Reflection: two small JS guards and two scoped CSS changes suffice.

### Cycle 1, Contrarian

Verified employee account-panel is 1200, map-home-card 1000, and the header
does not create an intervening stacking context. 1100 is the intended tier.
Expanded map uses the browser top layer and should stay above ordinary chat.
Resident close hover also inherits a dark brand background, so both sites
must be measured. Focus inside the log must suppress follow even at bottom.
Test both open and closed same-context refresh states, preserving identity,
draft and aria-expanded; initial installation still needs an opener.
Reflection: no wider redesign or API change is needed.

## Evidence Log

| ID | Finding | Source |
| --- | --- | --- |
| C1 | Launcher and popup z-index 4; close lacks hover override | src/api/src/zava_forward/api/web/chat-widget.css:1 |
| C2 | message appends then calls bottom unconditionally | src/api/src/zava_forward/api/web/chat-widget.js:83 |
| C3 | install overwrites widget onclick; create installs toggle | src/api/src/zava_forward/api/web/chat.js:23; src/api/src/zava_forward/api/web/chat-widget.js:102 |
| C4 | Same-context query changes call install without reset | src/api/src/zava_forward/api/web/app.js:293 |
| C5 | Existing two-site synthetic browser/focus harnesses | src/api/checks/chat_widget_browser_check.py:1; src/api/tests/test_chat_widget_focus.py:1 |
| C6 | Map summary 1000, account 1200, no header stacking context | src/api/src/zava_forward/api/web/style.css:228; src/api/src/zava_forward/api/web/style.css:57 |
| C7 | Resident dark hover, shared soft/brand tokens available | src/api/src/zava_forward/api/resident_demo/web/demo.css:1 |
| W1 | Focus, hover contrast, reduced motion and native semantics | https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md (retrieved 2026-10-29) |

## Decisions, Risks and Readiness

Proposed: stack chat at 1100, below account 1200 and above map 1000;
surface/brand hover pair with soft background; conditional pre-append follow;
install/decorate only before widget creation. Alternatives: map isolation has
wider effect; scrollIntoView risks ancestor movement; restoring onclick after
each route duplicates widget ownership. No new dependency or test file needed.
All Q1-Q4 answered (C1-C7). Accept the proposed guards/token changes; reject
map isolation and scrollIntoView as unnecessary wider changes. No further
research cycle: named causes and regression path are covered. Residual risk:
browser geometry and pixel rounding require executed checks; assistive-tech
and live acceptance cannot be inferred. Self-check: source pointers, explicit
limits, three waves, alternatives, decisions and readiness recorded.
Research disposition: executed. Planning Readiness: Ready.

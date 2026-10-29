---
title: Map filter duplicate-request observation research
description: Focused research for the PR 553 browser assertion correction
ms.date: 2026-10-29
---
<!-- markdownlint-disable-file -->

## Research Brief

Correct the false-positive duplicate-read assertion in
`src/api/checks/map_fullscreen_browser_check.py`, for issue #551 / PR #553.
Audience: implementation and independent reviewers. Output mode: convergence.
Scope: request observation around repeated filter activation and directly
related validation. Non-goals: application changes, visual changes, Azure,
pushes, rubric-score edits or issue acceptance claims.

## Research Parameters

Focused posture, selected from the caller's named target and failure evidence.
Evidence root: `.copilot-tracking/`. External research is unnecessary.
Questions: why is the old assertion insufficient; how does the existing request
listener synchronize; which local checks exercise the actual browser?

## Extension Registry and Provenance

Repository instructions and RPI phase skills apply. Browser instrumentation
does not change delivered UI; design/restyling skills are not applicable.
Research stays inline because this is one continuous, small code trace.
No interaction is needed: the caller explicitly requests the complete loop
and local commit, with no push.

## Direction Controls and Prior Knowledge Gate

The first shell command was `git pull --rebase`, which fast-forwarded
`b1cbb5b6` to `ea4fb4ec`, absorbing only the bot's rubric update.
The worktree was clean and branch `feat/map-filters-551` matches open PR #553
targeting main. Original issue delivery artifacts remain historical evidence;
this correction uses a distinct task slug rather than rewriting their outcomes.
The original case study, addendum, knowledge-base index and owner memory were
read for context, not treated as application-test evidence.

## Research Cycle Log

### Cycle 1

#### Wave 1: Wider

Inspected the named browser check and located existing issue artifacts,
API tests and README execution guidance. The defect is in the test oracle,
not evidence of a current application duplicate-request bug.
Reflection: prioritize the listener and browser event-loop boundary.

#### Wave 2: Deeper

The existing shortcut helper's two requestAnimationFrame turns provide the
repository's browser-processing boundary. A listener can start before the first
activation, verify that request was seen, snapshot the count before the second
Space press, and check the count after that boundary. Remove the listener in a
nested finally before unrelated area changes. The venv imports Playwright and
has Ruff 0.17.1. Existing changes evidence identifies the six focused unittest
modules and the harness's synthetic loopback server and external-request block.
Reflection: no new helper or application edit is needed.

#### Wave 3: Contrarian

Counting held routes cannot work: hold_first deliberately continues later
routes without appending them. An immediate request count risks observing the
browser before it processes activation. Use the existing two-frame boundary,
not an arbitrary sleep. Verify non-vacuity with the first request and prove
sensitivity by serving an in-memory mutation that removes the application's
already-selected guard; do not persist a product mutation.
Reflection: the actual browser and negative control are stronger than an
additional source-string assertion.

### Parent Synthesis and Re-entry

Accept C1/C2: use an all-request listener plus event-loop synchronization.
Reject held-route counting and fixed sleeps. C3 and existing task evidence
support local execution. No further cycle is needed: the bounded failure,
prior art and executable validation are established.

## Evidence Log

| ID | Source | Finding |
| --- | --- | --- |
| C1 | `src/api/checks/map_fullscreen_browser_check.py:33-82` | Existing shortcut check records every matching page request, waits two animation frames and removes its listener in finally. |
| C2 | `src/api/checks/map_fullscreen_browser_check.py:131-155` | Only the first route is appended; all later matching routes continue, so held length cannot detect duplicates. |
| C3 | `src/api/README.md:416` | Documents the focused constructed-data browser runner. |
| C4 | `src/api/src/zava_forward/api/web/app.js:1965` | Already-selected flag guard supplies a precise negative-control mutation. |
| C5 | `src/api/tests/test_map_fullscreen.py:115-132` | Existing tests already assert the application guard and shared filter state. |

## Current Decisions and Planning Readiness

Research disposition: executed, Complete. Planning Readiness: Ready.
No research blockers. Retain the original issue Review unchanged.
Self-check: all questions answered with local evidence; no external claims;
three ordered waves and alternatives recorded.

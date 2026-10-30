---
title: Map disposal and enlarged-font correction research
description: Focused evidence for the PR 539 correction round
ms.date: 2026-10-29
---
<!-- markdownlint-disable-file -->

## Research Brief

Investigate the two supplied Copilot findings for #532 / PR #539, preparing
implementation and browser regression coverage. Audience: branch reviewers.
Output mode: convergence. Scope: map disposal, expanded-map grid and the
existing constructed-data browser check. No unrelated redesign, private data,
Azure, push, force-push or closing keywords.

## Research Parameters

* Posture: focused, selected for named source targets and supplied failure evidence.
* Resolved evidence root: `.copilot-tracking/`.
* Research source edits: prohibited.
* Questions: how can disposal invalidate a pending successful fit request;
  how can the sidebar preserve map width at 640px with a 32px default font;
  how can the existing browser harness prove both regressions?
* Completion basis: direct source evidence and reproducible browser assertions.

## Extension Registry and Provenance

* Repository instructions: selected for branch, synthetic data and validation boundaries.
* rpi-research: selected for ordered wider/deeper/contrarian evidence.
* web-design-guidelines: selected; current upstream rules retrieved 2026-10-29.
* Research specialist: skipped; this is one tightly coupled, bounded trace.
* Public-page design and app-redesign skills: skipped; no redesign is requested.

## User Participation and Direction Controls

The user explicitly requests all four RPI phases and local commits on the current
branch. This is a bounded full-loop execution, not a persistent automatic session.
No clarification is necessary. Preserve original evidence and leave remote state
unchanged. Hold the nonblocking heavy lock for full validation; if busy, use
targeted checks and disclose the blocked full suites.

## Prior Knowledge Gate

Read original case study, addendum, knowledge-base index and owner memory.
Memory is context, not evidence. Initial worktree was clean on
`feat/map-fullscreen-532`; required first `git pull --rebase` fast-forwarded
`a35d1ffb` to `300a1a10` (bot rubric update). PR #539 is open against main.

## Research Questions

| ID | Question | Status |
| --- | --- | --- |
| Q1 | Disposal and outstanding response ordering | Answered C1, C4 |
| Q2 | Enlarged-font grid sizing and reflow assertions | Answered C2, C3 |
| Q3 | Existing test harness and validation boundaries | Answered C3, C5, C6 |

## Research Cycle Log

### Cycle 1: Wider

The map uses a route signal plus per-draw sequence, native modal relocation and
Leaflet resize events. The browser check already runs the real app with synthetic
fixtures and blocks external requests. It covers normal font widths but not a
32px browser default or simultaneous session-expiry/successful-fit responses.
Reflection: investigate these missing states inline, reusing the harness.

### Cycle 1: Deeper

`api()` invokes login on any non-login 401; login disposes the map but leaves
the route signal live. A successful latest draw only checks that signal and
sequence before mutating layers and calling fitBounds. Area/tile changes start
draw(true) directly. Hold two real map requests, fulfill the earlier one as 401,
then release the later successful response containing bounds. Keep the dialog
expanded to exercise collapse's resize. Reflection: this reproduces the precise
race without changing production exports or abort semantics.

### Cycle 1: Contrarian

Incrementing the sequence before collapse is insufficient because its resize
may start another draw. Null-checking fitBounds merely hides stale rendering;
aborting routeController changes session/login behavior outside scope. Accept
sequence invalidation after collapse instead. A font-relative breakpoint is
viable but broader than the one-track cap; min(19rem,45%) preserves the existing
normal-font desktop width and narrow-screen rule. Browser coverage must set a
real browser default font, not author CSS or only shrink the viewport.
Reflection: no wider discovery is needed; both alternatives support the
requested minimal corrections and exact regressions.

## Evidence Log

| ID | Location | Evidence |
| --- | --- | --- |
| C1 | src/api/src/zava_forward/api/web/app.js:1566 | Disposal collapses before removing and nulling the map. |
| C2 | src/api/src/zava_forward/api/web/style.css:212 | Expanded grid fixes sidebar at 19rem above the 600px breakpoint. |
| C3 | src/api/checks/map_fullscreen_browser_check.py:86 | Existing real-app browser harness and error collection. |
| C4 | src/api/src/zava_forward/api/web/app.js:46,84,1632,1670,1820 | API 401, login cleanup, success guard, fit continuation and area-triggered fit. |
| C5 | src/api/tests/test_map_fullscreen.py:58,77 | Existing source contracts require updated layout and disposal-order assertions. |
| C6 | src/api/README.md:126; src/README.md:74 | Existing browser invocation and nonblocking validation policy. |
| W1 | https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md | Retrieved 2026-10-29; fix overflow at source, preserve native semantics and keyboard behavior. |

## Findings, Alternatives and Decision State

Accepted: increment the draw sequence after collapse, and cap the sidebar at
the smaller of 19rem or 45% of available width. Use request interception to
control actual app response ordering, and a Chromium context configured with
a 32px default font at 640px. Retain all existing browser interactions.
No pinned scenario-manifest inputs are in the proposed edit set.

## Risks and Self-check

The browser regression must verify a live route signal, a successful response
with nonempty bounds, no late fit call, no new requests, no modal/body residue
and no JavaScript errors. Resize can supersede held requests, so assert the
fit request remains latest immediately before releasing it. These are local
synthetic checks, not human accessibility, live SQL or hosted approval.
One inline three-wave cycle completed; material questions answered, cited and
alternatives challenged. No research delegation or additional cycle is needed.

## Planning Readiness

Research disposition: executed, complete. Planning Readiness: Ready.
Parent continuation: Plan, explicitly authorized by the full-loop user request.

---
title: Map fullscreen and home cards research
description: Focused evidence for issue 532
ms.date: 2026-10-28
---
<!-- markdownlint-disable-file -->

## Research Brief

Research issue #532 for employee map expansion and home summary cards. Audience:
implementation and independent reviewers. Output mode: convergence. Posture:
focused, selected from the named issue, source files and pattern references.
Evidence root: `.copilot-tracking/research/2026-10-28/`.

Scope: existing native employee map, its CSS, unit and synthetic browser checks.
Non-goals: framework adoption, briefing changes, #531 async helper, Azure,
private data, secrets, `.env`, human accessibility acceptance.

## Research Parameters and Direction Controls

* Preserve branch `feat/map-fullscreen-532`, stacked on
  `feat/case-journey-ux-526` / open PR #529. PR wording: `Refs #532`.
* Full loop expressly requested; proceed automatically through the four phases.
* Heavy checks require nonblocking `/tmp/ama-rpi-heavy.lock` admission, retry
  for at most 40 minutes. No Azure operations.
* Read the original/addendum, reference index and owner memory. Memory is context,
  not evidence. Preserve consent, safety and manual service boundaries.
* Source changes are prohibited during Research.

## Extension Registry and Participation

Repository instructions and the UX design system, WCAG baseline and content
standard apply. Selected `rpi-research` and `web-design-guidelines`; the latter's
current source was retrieved. Public-page design and visual redesign skills are
not applicable to this bounded app interaction. Research specialist delegation is
unnecessary for a single tightly coupled trace. Independent critique and final
Review will be separate bounded executions. Intake is sufficient; no interaction
is needed or available.

## Questions and Prior Knowledge Gate

Q1: Where are map selection, clustering, filtering and route disposal owned?
Q2: What summary information is already authorized and available?
Q3: How can both modes preserve keyboard/focus/manual access?
Q4: Which existing checks need updating and what blocks publication?

Issue #532 was read with `gh issue view 532 --comments` (no comments) and JSON
body retrieval. The worktree was clean and already on the requested branch.
Parent ancestry is `6d2c2dc4ce4b2e9bf99853698ac5b71e24c02c1c`;
PR #529 is open. Existing checks currently expect marker activation to navigate
directly; this must change intentionally to summary-first.

## Research Cycle Log

### Cycle 1

#### Wave 1: Wider

Read the requested UX references and locate the native Leaflet map in `app.js`,
shared design CSS and synthetic browser harness. Fetched Fluent React Storybook
and its story index, plus current Web Interface Guidelines.

Reflection: no new framework or API is indicated. Native cards and a bounded
expanded map surface can preserve current tokens and map list.

#### Wave 2: Deeper

The map uses one route-scoped AbortSignal and sequence counter. Every redraw
replaces markers and list rows. `map_view` already supplies ID, name, address,
stage and status without another request. Coordinator deliberately replaces the
name with case ID and removes address; that limitation must not be bypassed.
Existing list links navigate directly and are a retained manual path.

Reflection: use existing permitted map fields only. Selection/focus must be
resolved by case ID after redraw, not by an obsolete marker reference.

#### Wave 3: Contrarian

Considered browser Fullscreen API, native modal dialog, CSS-only fixed overlay,
and fetching full case detail for cards. Browser fullscreen adds permission and
platform dependencies; a fixed overlay would require hand-written focus trapping
and background isolation. Native `dialog.showModal()` supplies those semantics,
with an inline left panel within it. No React adoption is needed.
Fetching case detail would widen exposure and introduce races without improving
the bounded summary requirement. Coordinator omission is real counter-evidence
to assuming every point contains an address.

Reflection: choose native near-full-viewport dialog with the existing map moved
into it and restored afterward; use a placeholder, explicit cleanup on route
abort, no animated map movement, and stable-ID focus recovery. Escape closes
the card first and then the expanded map. Clear excluded selections on redraw.

#### Parent Synthesis and Disposition

Accepted native dialog, existing-map-payload summaries, and explicit route
cleanup (C1, C6-C8, W1-W4). Rejected browser fullscreen, custom modal semantics
and extra detail requests for the reasons above. No second cycle is warranted:
Q1-Q4 are answered and remaining human/hosted/full-gate approval is not research.

## Evidence Log

| ID | Evidence | Location |
| --- | --- | --- |
| C1 | Native map, symbols and keyboard helper | `src/api/src/zava_forward/api/web/app.js:1323` |
| C2 | Existing synthetic design/marker browser checks | `src/api/checks/design_system_browser_check.py:127` |
| C3 | Fluent native foundation, not completed framework adoption | `docs/reference/research/ux/design-system.md:19` |
| C4 | Automated checks do not establish human AT acceptance | `docs/reference/research/ux/wcag-conformance-baseline.md:18` |
| C5 | Plain language and approval boundaries | `docs/reference/research/ux/content-standard.md:21` |
| C6 | Map payload already supplies summary fields | `src/core/src/zava_forward/core/insights.py:143` |
| C7 | Coordinator deliberately omits resident name/address | `src/core/src/zava_forward/core/coordinator.py:309` |
| C8 | Route change aborts route-owned work | `src/api/src/zava_forward/api/web/app.js:248` |
| W1 | Fluent React Storybook shell and story index retrieved; pattern reference only | https://storybooks.fluentui.dev/react/ (2026-10-28) |
| W2 | Current web rules: semantics, named close controls, focus, reduced motion, overflow | https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md (2026-10-28) |
| W3 | Inline Drawer: adjacent interactive surface, title dismiss action, explicit focus restoration | https://raw.githubusercontent.com/microsoft/fluentui/master/packages/react-components/react-drawer/stories/src/Drawer/InlineDrawer.stories.tsx (2026-10-28) |
| W4 | Card header action is an explicitly named button; dialog change-focus example manages initial focus | https://raw.githubusercontent.com/microsoft/fluentui/master/packages/react-components/react-card/stories/src/Card/CardTemplates.stories.tsx and https://raw.githubusercontent.com/microsoft/fluentui/master/packages/react-components/react-dialog/stories/src/Dialog/DialogChangeFocus.stories.tsx (2026-10-28) |

## Decisions, Risks and Readiness

Research disposition: executed, Complete. Planning Readiness: Ready.
Self-check: three ordered inline waves, all four questions answered, internal
and external evidence identified, alternatives and scope boundaries recorded.
Two guessed Storybook source paths returned 404; the Storybook index and GitHub
directory listing resolved the actual files and their complete content was read.
No source-retrieval gap remains. No legal currentness or accessibility
conformance claim is made. Full gate/publication and human AT approval remain
separate from local implementation.

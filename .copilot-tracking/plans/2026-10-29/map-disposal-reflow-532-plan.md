---
title: Map disposal and enlarged-font correction plan
description: Implementation-ready correction round for PR 539
ms.date: 2026-10-29
---

## Task Metadata

* Task ID: issue-532-pr-539-map-disposal-reflow
* Task slug: map-disposal-reflow-532
* Planning status: Ready after one critique and direct dispositions
* Date: 2026-10-29

## Executive Summary

Invalidate pending map responses after disposal collapses the dialog, and bound
the expanded sidebar by available width. Add precise regressions to the existing
real-app browser check, preserving current keyboard, focus and manual journeys.
Keep all commits local on the owner-selected branch.

### What You May Not Know

Collapse can itself start another draw through Leaflet resize, so invalidation
must follow collapse. A 640px viewport with a 32px browser default font is not
covered by the existing 600px media query or normal-font mobile checks.

### Unresolved Decisions or Blockers

None at planning time. Full suites require nonblocking heavy-lock admission. Admission returned 75
during Implement; targeted fallback checks passed, browser/negative controls
and full discovery remain unperformed.

## User Decisions and Requirements

* Correct both supplied Copilot findings on feat/map-fullscreen-532, PR #539.
* Run the full Research, Plan, Implement, Review correction round with dated artifacts.
* Pull/rebase first (done); do not push, force-push, use az or closing keywords.
* Commit source and artifacts with Conventional Commits and the supplied trailer.
* Use src, the /tmp/mv venv, this worktree's src/test imports and strict checks.
* Run API/core mypy, Ruff lint/format, unit suites and the relevant browser check;
  hold flock -n /tmp/ama-rpi-heavy.lock for full suites. If busy, target and disclose.
* Refresh scenario-manifest SHA-256 pins only if a pinned input changes.

## Goals

* Ignore successful stale map responses after session-expiry disposal.
* Preserve usable expanded map and sidebar without horizontal overflow at enlarged fonts.

## Scope and Non-Goals

Five existing files: app.js, style.css, map_fullscreen_browser_check.py,
test_map_fullscreen.py and the expanded-map section in src/api/README.md.
No auth redesign, dependency changes, new fixture, cloud work or broad UI audit.
Dated RPI artifacts are additional evidence, not application scope.

## Functional Requirements

* Increment seq immediately after collapse(false), before removing/nulling the map.
* Use min(19rem,45%) for the desktop grid's sidebar track.
* Preserve session-expiry sign-in, existing route aborts and normal map behavior.

## Non-Functional Requirements

* Regression execution uses only constructed loopback data and blocked external traffic.
* Browser helper additions remain strictly typed; no new suppressions or casts.
* Enlarged-font check sets a browser default font, verifies computed root 32px,
  and measures actual dialog/workspace/sidebar/map geometry.

## Acceptance Criteria

* Controlled overlapping real map requests: earlier 401 disposes the map while
  later successful draw(true) response has bounds. Release success after login,
  drain its continuation, assert no pageerror, fitBounds call, new draw or residue.
* Exercise embedded and expanded disposal. Verify route signal remains un-aborted.
* Cover collapse-triggered resize draws; ensure invalidation follows collapse via
  source-order contract as well as controlled browser instrumentation if needed.
* At 640px / 32px browser default: document, dialog and workspace do not overflow;
  sidebar fits its track; map stays >80px wide; selected summary and close action work.
* Existing browser suite remains passing, including normal-font desktop/mobile.
* API/core mypy, ruff check ., ruff format --check ., and unit results recorded
  with actual skips/failures. If full lock is busy, record targeted results instead.

## Implementation Context Record

* Research: .copilot-tracking/research/2026-10-29/map-disposal-reflow-532-research.md
* Details: .copilot-tracking/details/2026-10-29/map-disposal-reflow-532-phase-details.md
* Critique: .copilot-tracking/reviews/plans/2026-10-29/map-disposal-reflow-532-plan-critique.md
* Changes: .copilot-tracking/changes/2026-10-29/map-disposal-reflow-532-changes.md
* Review: .copilot-tracking/reviews/logs/2026-10-29/map-disposal-reflow-532-review.md

## Sources

Research C1-C6 and W1; supplied Copilot findings and branch/test constraints.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Correct disposal and responsive track sizing

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Fix both source defects and update source contracts

Source changes are the two bounded corrections above. Update the existing layout
expectation and add disposal-order assertion in the existing unit method.
Dependencies: finalized critique.

<!-- rpi:phase id=P02 -->
### [ ] P02: Exercise browser regressions and package gates

<!-- rpi:task id=P02-T01 -->
#### [ ] P02-T01: Extend the existing browser check and document its coverage

Test ownership: src/api/checks/map_fullscreen_browser_check.py.
Maximum additions: two focused browser helpers, invoked from the existing run.
Exact removals: none. Source contracts stay in test_map_fullscreen.py;
maximum new unit methods: zero. No new test files or generated code.
Semantic checks: actual response order, live signal and computed geometry.
Regression checks: existing and new browser assertions. Validate each new
regression against pre-fix served assets using test-only response overrides,
then verify corrected behavior. No production test hooks.
Dependencies: P01-T01 for corrected pass; helpers may precede source correction
to capture red evidence.

<!-- rpi:task id=P02-T02 -->
#### [ ] P02-T02: Validate, independently review once and commit locally

Install editable required src distributions in /tmp/mv only if imports show a
missing/stale-worktree distribution. Hold heavy lock nonblocking for full suites,
run both packages' strict/static/unit checks plus browser. Use explicit worktree
PYTHONPATH. Independent Review is one pass after implementation, not a repair loop.
Resolve authenticated privacy-safe commit identity and commit all original evidence.
Dependencies: P02-T01. No publication or complete publication-gate claim.

## Dependencies

Existing Chromium, pinned axe 4.10.3, /tmp/mv tools and constructed fixture harness.
No planned edit is a scenario-manifest pinned input.

## Critique Disposition

Execution: complete, once. Original verdict: Revise, preserved unchanged.

| Finding | Disposition | Resolving evidence |
| --- | --- | --- |
| PC-001 | Applied | Details specify check-only draw Promise observation, request identity, live signal, controlled expanded collapse redraw and disposal-local source ordering. |
| PC-002 | Applied | Details specify isolated Chromium Blink defaultFontSize argument, unstyled probe and computed-root checks; configuration must be demonstrated, not assumed. |
| PC-003 | Rejected as inapplicable to parent | The critique worker reports a filesystem restriction specific to its execution context. Parent tools explicitly support /tmp; user explicitly selects /tmp/mv and the shared /tmp lock. Parent already read tool presence successfully. No parent-level prohibition exists. Preserve finding but do not invent a blocker or replace the requested environment. |

## Follow-Up Items

* Validation follow-up: full API/core units, map browser and defect-specific
  pre-fix asset-override controls need a later explicit heavy-lock coordination
  event. Source and typed targeted checks do not substitute for these results.

## Handoff

Implementation begins only after critique dispositions. User explicitly authorized
all four phases and a local-only stop; no persistent automatic session is entered.

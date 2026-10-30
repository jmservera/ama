<!-- markdownlint-disable-file -->
# RPI Plan: Expanded map filters

## Task Metadata

* Task ID: 551
* Task slug: map-filters-551
* Planning status: Ready; original Revise critique preserved and findings resolved in plan
* Plan date: 2026-10-29
* Phase details: .copilot-tracking/details/2026-10-29/map-filters-551-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-10-29/map-filters-551-plan-critique.md

## Executive Summary

Move the existing Overview filters to the expanded map's top edge and make
them compact there. Restore the same controls on exit, so the header and map
cannot disagree. Update selected-state text in place to preserve keyboard focus.
Include the existing area selector without introducing duplicate IDs or state.
Filter reads use existing map-region progress, not the control-disabling async
wrapper. A bounded scrollable filter region preserves a minimum map height.

### User Decisions and Requirements Highlights

* Run all four RPI stages, locally verify with /tmp/mv and real Playwright,
  commit with the requested trailer, and do not push.
* Preserve native Fluent-derived components, visible state words, manual paths
  and reduced motion; no Azure changes.

### What You May Not Know

Reusing the same DOM nodes removes synchronization machinery. Completed is a
summary, not a filter, and will remain in the header but not the compact map.
Coordinator uses a different cohort model and must retain its current behavior.
Local checks are not WCAG conformance or human approval.

### Unresolved Decisions or Blockers

No implementation blocker. The complete publication gate includes az, which
the caller prohibits; no publication is requested or permitted here.

## User Decisions and Requirements

* Deliver the four acceptance criteria in issue #551 on feat/map-filters-551.
* Source in src/api/src/zava_forward/api/web only; tests outside the package.
* Load/fetch web-design-guidelines and preserve the three UX standards.
* Run relevant unittest modules using /tmp/mv, node syntax and a real-browser
  check against a locally started app; record exact commands/results.
* No az, Azure modifications, push or manual rubric-score changes.
* Commit with Conventional Commit subject and Copilot coauthor trailer.
* A future PR may use Closes only if every issue criterion is proven.

## Goals

* Keep map filtering available while its modal prevents background interaction.
* Preserve one source of truth and keyboard focus throughout filtering.

## Scope and Non-Goals

* In scope: mapPanel optional filter group, Overview state rendering, compact
  expanded styles, existing map tests/browser harness and API README.
* Non-goals: new filter semantics, URL-state migration, new framework,
  Coordinator filter redesign, backend changes, full accessibility certification,
  cloud execution and publication.

## Functional Requirements

* Reparent the existing flag tiles and area selector into the dialog above the
  workspace; restore their original slot on every collapse/disposal.
* Every flag and area change uses existing ovState and draw(true).
* Preserve button nodes and change only aria-pressed and selection words.
* Start map reads without returning their promise to the per-control wrapper;
  mapPanel already owns explicit progress, failure and latest-response handling.
  Ignore activation of the already selected flag; allow distinct selections
  and area reads to supersede earlier responses without disabling controls.
* Keep Completed out of the compact controls without deleting its header tile.
* Preserve empty/error feedback, selected-home cleanup, Escape, list navigation
  and Coordinator behavior.
* Preserve the geographic centre when the map rectangle changes: Leaflet
  invalidateSize uses pan:true with animate:false, a synchronous compensation.

## Non-Functional Requirements

* Native button/select semantics, visible focus, "Selected"/"Select filter"
  text and at least 40px button height.
* No horizontal overflow or clipped filter labels at 320, 390 and 1280px,
  and 640px with 32px browser-default text.
* Keep filters above rather than over map controls and retain usable map space.
* Bound expanded filters to 45% of the panel with native scrolling and
  overscroll containment. Retain at least 14rem map height and 80px map width;
  allow panel overflow for extreme text sizes. Verify 390x568 as well as the
  listed widths and enlarged text, including pending reads.
* No new motion, dependency or request race; existing latest-response guard wins.

## Acceptance Criteria

| ID | Criterion | Proof |
| --- | --- | --- |
| AC1 | Compact header filters along expanded map top | Actual dialog geometry and screenshot |
| AC2 | Filter changes update markers and restored header state | Flag/area changes both directions, DOM identity and selected text |
| AC3 | Keyboard, non-colour state and narrow readability | Enter/Space/Tab, focus, computed styles, 320/390/1280 and enlarged-font layout |
| AC4 | Behavior covered automatically | Extended real-server Playwright harness and source-contract unittest |

## Implementation Context Record

| Item | Artifact |
| --- | --- |
| Plan | .copilot-tracking/plans/2026-10-29/map-filters-551-plan.md |
| Details | .copilot-tracking/details/2026-10-29/map-filters-551-phase-details.md |
| Critique | .copilot-tracking/reviews/plans/2026-10-29/map-filters-551-plan-critique.md; original Revise, all three findings directly resolved |
| Research | .copilot-tracking/research/2026-10-29/map-filters-551-research.md; Ready |
| Changes | .copilot-tracking/changes/2026-10-29/map-filters-551-changes.md; Implementation owns creation |
| Continuation | Explicit full-loop parent continues after critique |

## Sources

* Research C1-C8 and W1-W2: source lifecycle, test fixture and web rules.
* docs/reference/research/ux/design-system.md: native tokens and selection words.
* docs/reference/research/ux/wcag-conformance-baseline.md: engineering targets.
* docs/reference/research/ux/content-standard.md: plain wording.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Implement shared compact filters

* Dependencies: completed Research and one final-candidate critique.

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Reparent existing controls and preserve selected-button focus

* Evidence: C1-C3, C7.
* Expected result: same native controls in header or modal; stable state.
* Details: P01-T01 in the phase-details artifact.

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Add compact responsive styles and usage documentation

* Dependencies: P01-T01.
* Expected result: wrapped readable filters above map; no design-system drift.
* Details: P01-T02.

<!-- rpi:phase id=P02 -->
### [x] P02: Verify acceptance and regressions

* Dependencies: P01.

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Extend and execute local automated checks

* Expected result: all four criteria mapped to actual unit/browser evidence.
* Details: P02-T01.

## Test Ownership and Change Budget

* Canonical targets: app.js, style.css, src/api/README.md.
* Test owners: src/api/tests/test_map_fullscreen.py and
  src/api/checks/map_fullscreen_browser_check.py.
* Exact removals: none. Maximum additions: two unit test methods and one
  browser helper plus assertions in the existing enlarged-font check.
* Generated targets: none committed; JSON reports/screenshots external.
* Semantic proof: actual HTTP-backed filtering and control geometry/focus.
* Regression proof: existing map lifecycle, Coordinator, errors, route cleanup
  and reduced-motion tests remain in the same browser run.
* Validation: relevant unittest modules, node --check app.js, existing browser
  harness with hash-pinned axe; Python Ruff/mypy if available.

## Dependencies

* /tmp/mv installed namespace distributions and Playwright.
* Existing locally constructed synthetic fixture, no private data.
* Pinned axe 4.10.3; verify bytes using the existing harness.

## Critique Disposition

One independent critique executed; original verdict Revise is preserved.

| Finding | Owner and disposition | Resolving plan evidence |
| --- | --- | --- |
| PC-001 High | Planner; resolved directly | Functional requirements and P01-T01 specify non-control reads with map-region progress and selected-flag deduplication; P02-T01 holds responses, tests focus/Tab and stale-selection handling |
| PC-002 High | Planner; resolved directly | NFR and P01-T02 specify 45% scrollable filter cap, 14rem minimum map height, panel overflow and 390x568/enlarged-text vertical checks |
| PC-003 Medium | Planner; resolved directly | P02-T01 explicitly updates the exact function-signature extractor without removing assertions |

No significant/divergent user decision required; no second critique.

## Follow-Up Items

* Rank 1: RV-001, correct the selected-flag duplicate-request browser oracle.
  The original independent Review found that the held-first-request list cannot
  prove no additional request occurred. Production guard and all four issue
  criteria have bounded support. Owner: later authorized rpi-implement; observe
  every actual request and demonstrate that a duplicate makes the assertion
  fail. Outside active P01-P02 and this completed task's one Review; no second
  Review or corrective source edit is performed here.

## Handoff

* Changes: .copilot-tracking/changes/2026-10-29/map-filters-551-changes.md.
* P01-P02 complete. Original independent Review execution Complete, outcome
  Defects found: one Low test-oracle finding RV-001, routed above. No product
  correctness defect identified. Original commands/adverse evidence are in Changes.
* No implementation blocker. Publication gate, human acceptance and hosted
  approval remain separate and unperformed; do not push.

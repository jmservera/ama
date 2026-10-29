<!-- markdownlint-disable-file -->
# RPI Plan: Compact case view

## Task Metadata

* Task ID: 552
* Task slug: case-view-ux-552
* Date: 2026-10-29
* Planning status: Ready; one critique completed, compatible findings resolved
* Details: .copilot-tracking/details/2026-10-29/case-view-ux-552-phase-details.md
* Critique: .copilot-tracking/reviews/plans/2026-10-29/case-view-ux-552-plan-critique.md

## Executive Summary

Reuse the six workflow icons embedded in slide 4 of the tracked capstone deck.
Keep workflow steps compact with labelled status and one-line blocker summaries;
offer complete reasons, owners and next actions in native auto popovers.
Attach a wrapping tablist to its panel surface, with scrolling confined to
the selected panel, not the tabs.

### What You May Not Know

`docs/presentations/` is absent here, but the tracked capstone PPTX contains
the exact six-step set. `/tmp/mv` editable installations reference another
worktree, so commands explicitly select the current source roots. Native
Fluent foundations are retained; this does not complete Fluent library adoption
or establish full WCAG/assistive-technology acceptance.

### Unresolved Decisions or Blockers

None for implementation. Publication is excluded; a complete publication
gate is not claimed or bypassed by focused local validation.

## User Decisions and Requirements

* Deliver issue #552 on feat/case-view-ux-552 through ordered Research, Plan,
  Implement and independent Review, with dated evidence.
* Use presentation/existing web icons; preserve Fluent 2, WCAG and content
  standards, native semantics, non-colour status and reduced motion.
* Source in src/api/src/zava_forward/api/web only; tests/checks outside package.
* Validate using /tmp/mv unittest, Node syntax and a real local Playwright app.
* No az, Azure modifications, push or manual rubric score edits.
* Commit with Conventional Commit subject and supplied Copilot trailer.

## Goals

Reduce vertical workflow noise while keeping task identity, blockers and
navigation operable and all manual/governed actions unchanged.

## Scope and Non-Goals

Touch case-workspace.js, app.js, style.css, six extracted PNG assets, existing
case journey unittest, one focused browser check and directly related API README.
No backend, dependency, role/authority, routing-framework or broad visual changes.

## Functional Requirements

* All six steps retain labels, links, current/status words and exact deck icons.
* Blocked steps and summary show a one-line reason; named native buttons open
  full, safely text-rendered reason/owner/action for every blocker.
* Tablist wraps outside panel scroll; manual Arrow/Home/End focus and
  Enter/Space activation, URL state, mounted panels and draft retention persist.
* Keep persistent safety above the journey and fallback listed sections usable.

## Non-Functional Requirements

* No page overflow at 320, 390 and 1280 CSS px.
* Measure pre/post rendered step heights on the same long-blocker fixture;
  require a reduction and collapsed step height <=132px at desktop, <=116px
  at narrow widths. Text labels may wrap; blocker summary alone is single-line.
* Popover keyboard/touch activation, Escape/light dismissal, visible focus,
  >=40px disclosure targets and reduced-motion behaviour verified in Chromium.
* Icons load locally with explicit dimensions and decorative alternatives.
* Preserve Fluent tokens and plain sentences over conflicting generic web
  typography/copy guidance.

## Acceptance Criteria

1. Six presentation icons plus text proven by image byte provenance and browser.
2. Thinner layout proven by same-fixture before/after step measurements/screenshots.
3. One-line blocker and full details proven via keyboard and touch disclosure.
4. Tabs attach to panel; panel scroll changes without moving tablist.
5. Existing design/accessibility/content regression modules pass and changed-file
   guidelines review finds no new material issue; no conformance overclaim.
6. Desktop and 320/390px browser records/screenshots preserved.

## Sources

Research: .copilot-tracking/research/2026-10-29/case-view-ux-552-research.md,
C1-C6/W1. Issue #552 retrieved with gh. UX standards under
docs/reference/research/ux/.

## Implementation Context Record

Plan and details paths above are canonical. Changes record:
.copilot-tracking/changes/2026-10-29/case-view-ux-552-changes.md.
Research Ready; final candidate ready for critique. Owner explicitly directs
the remaining ordered phases, without open-ended automatic-session activation.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Compact case UI

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Capture baseline and reuse deck icons

Extract six exact PNGs with stable workflow names; capture baseline metrics.
Dependencies: none.

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Compact blockers and attach tabs

Implement labelled icons, one-line summaries, native popovers and wrapping
attached tablist with bounded active panel scrolling. Depends on P01-T01.

<!-- rpi:phase id=P02 -->
### [ ] P02: Evidence and independent Review

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Validate and document

Run focused unittest/Node and real local Chromium desktop/narrow/touch checks.
Update README and changes evidence. Depends on P01-T02.

<!-- rpi:task id=P02-T02 -->
#### [ ] P02-T02: Review and commit locally

Fresh independent rpi-review, preserve its original outcome, record unresolved
findings rather than repeat Review. Resolve GitHub identity, local privacy-safe
email, commit all task changes and evidence, no push. Depends on P02-T01.

## Test Ownership and Change Budget

Canonical source: src/api/src/zava_forward/api/web. Generated targets: six
byte-exact extracted deck PNGs only. Test ownership: src/api/tests/test_case_journey.py
and src/api/checks/case_view_ux_browser_check.py. Exact removals: none.
Maximum additions: six PNGs, one browser check, three unittest methods plus
updating the existing blocker mapping expectation, dated RPI artifacts.
Semantic checks: shipped JS blocker/status and DOM semantics. Regression:
all case-journey, workspace-scripts, design-system, accessibility-baseline and
content-standard tests. Browser checks cover measurable geometry/interaction,
not source-string proxies.

## Dependencies

Installed /tmp/mv dependencies, local Chromium, slide-four media. Browser harness
must isolate constructed data and block external traffic. Full publication gate
is a separate blocked/unperformed boundary; no az invocation is authorized.

## Critique Disposition

Original critique verdict: Revise, two Medium findings. No repeat critique.

| Finding | Disposition | Resolving change |
| --- | --- | --- |
| PC-001 | Directly resolved in plan | Add viewport-bounded, scrollable popover; final reason/owner/action reachable by keyboard/touch at 320px, short height and enlarged text, including missing fields. |
| PC-002 | Directly resolved in plan | Add unavailable-script and post-mutation exception fallback scenarios; remove enhancement-only bounds/tab UI, preserve all sections and ordinary controls. |

These are compatible verification corrections, not significant owner decisions.

## Follow-Up Items

* RV-001 (Medium): a distinct later research/evidence action must reconcile
  external baseline/final JSON and rendered screenshots under valid access
  authority. Review execution remains Partial / Residual work; do not repeat
  Review or infer issue-wide independent acceptance.
* Cross-browser/AT/user acceptance and existing incomplete Fluent library adoption
  remain wider project work, not new completion claims.

## Handoff

One critique and one independent Review have executed. Implementation and local
validation complete; Review Partial / Residual work, RV-001 routed to later
evidence work. Persist locally with Refs #552, no push. P02-T02/P02 completion
wait only on the owner-authorized local commit, not a second Review.

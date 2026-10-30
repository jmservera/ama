<!-- markdownlint-disable-file -->
# RPI Plan Critique: Expanded map filters

## Metadata

* Task ID: 551
* Critique date: 2026-10-29
* Plan: .copilot-tracking/plans/2026-10-29/map-filters-551-plan.md
* Phase details: .copilot-tracking/details/2026-10-29/map-filters-551-phase-details.md
* Critique execution status: Complete
* Assessment count: One independent final-candidate critique.

## Inputs and Criterion Boundary

* Assessed the supplied plan, phase details and research at
  .copilot-tracking/research/2026-10-29/map-filters-551-research.md.
* Assessed AC1-AC4 as recorded in the supplied materials: compact top filters,
  synchronized filtering/header state, accessible narrow-layout interaction
  and durable automatic coverage. The issue's wording was not independently
  re-fetched; research W1 supplies that requirement boundary.
* Honoured the selected design: same-node reparenting/restoration, in-place
  state updates, shared ovState, optional mapPanel argument and unchanged
  Coordinator semantics. No alternative toolbar, redesign or framework is
  proposed.
* Grounded the assessment in research C1-C7 source pointers, the shared
  async-action helper, existing browser fixture and tests, and the three
  supplied UX standards. Required project context was read.
* Preserved the locked test owners, no-removal requirement, maximum two added
  unit methods and one added browser helper, with assertions in the existing
  enlarged-font check. Findings fit those allocations and retain the specified
  unittest, node syntax, real-loopback Playwright and pinned-axe validation.
* No implementation, validation execution, cloud command, Azure change, commit,
  push, score change, further delegation or second critique was performed.
  Only this critique artifact is written.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| AC1; C2/C7; P01-T02 | Partial | Top placement and scoped compact styling are sound; vertical budget and short-height behavior are not operationalized (PC-002). |
| AC2; C1-C3; P01-T01 | Covered | Original controls, one mapArea ID and shared ovState avoid independent synchronization. Repeat expansion, restoration and bidirectional changes have planned proof. |
| AC3; C1/C5/C7; P01-T01/P02-T01 | Partial | Stable nodes do not bypass AsyncAction's native disable, and pending feedback can change layout (PC-001). Height coverage is incomplete (PC-002). |
| AC4; C5/C6; P02-T01 | Partial | Strong real-server behavior assertions and regression retention; existing source extraction must accommodate the optional argument (PC-003). |
| Fluent-derived tokens, plain wording, native semantics, non-colour state | Covered | Existing token/state words and native button/select controls retained; no library-adoption or conformance claim. |
| Reduced motion, forced colours and manual paths | Covered | Existing map motion constraints, list route and Coordinator paths retained in the same browser run. |
| Request sequencing, error/empty results, disposal | Covered with integration risk | Existing latest-response and cleanup contracts retained; delayed filter interaction must also be covered under PC-001. |
| Test ownership, removals, budget and exact validation | Covered with correction | No extra test owner or test allocation needed; PC-003 is an existing setup edit, not removal of regression assertions. |
| Dated RPI artifacts, source boundary and local-only delivery | Covered | Plan names dated artifacts and permitted targets. Publication gate remains explicitly unperformed; no cloud fallback or push is authorized. |

## Verdict

* Verdict: Revise
* Severity counts: 0 Critical, 2 High, 1 Medium, 0 Low.
* Rationale: The selected architecture is credible, but the stated focus fix
  omits a directly coupled shared-helper behavior, while responsive proof
  leaves vertical workspace collapse undetected. A small existing-test setup
  correction is also required. These are direct planner corrections, not
  reasons to change the user's design decisions.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Stable filter nodes still enter native-disabled async handling

* Related IDs: AC3, AC4, C1, P01-T01, P02-T01.
* Evidence: src/api/src/zava_forward/api/web/app.js:16-23 wraps onclick and
  onchange with AsyncAction.handler. Existing Overview handlers at
  src/api/src/zava_forward/api/web/app.js:1958-1965 return mp.draw(true).
  src/api/src/zava_forward/api/web/async-action.js:40-74 sets a pending
  promise's control to disabled unless it already owns aria-disabled=true;
  it does not restore focus. Its feedback at lines 6-14 inserts an adjacent
  status node when a control is supplied. The details at
  .copilot-tracking/details/2026-10-29/map-filters-551-phase-details.md:35-39
  specify stable nodes and original area handling without addressing this.
* Concern: In-place selected text alone does not preserve focus through a
  pending request. Keeping the original promise-returning handler exposes the
  now-stable focused button or select to native disabling. The wrapper also
  inserts status children into the compact control layout, in addition to
  mapPanel's region feedback. Fast settled-response tests do not establish
  focus or layout behavior throughout the operation.
* Impact: Keyboard focus can leave a selected filter, subsequent Tab traversal
  can lose its expected position, and loading text can expand or displace the
  compact toolbar. This undermines the explicit focus-preservation goal.
* Smallest useful change: Specify a map-filter-local async integration that
  keeps the active native control focusable throughout the read, preserves
  duplicate/request sequencing safeguards and accessible progress, and cleans
  up pending state on completion/failure. Choose the integration explicitly;
  do not change shared helper behavior or Coordinator globally. Extend the
  allocated browser helper to hold a map response while activating a flag
  with Space/Enter and changing area, checking identity, activeElement,
  pending semantics, Tab order and toolbar geometry before and after release.
  Include recovery and distinct-control overlapping reads so the existing
  latest-response guard is not bypassed.
* Action owner: Planning parent, with implementation owned by P01-T01 and
  proof owned by P02-T01.
* Exact resolving evidence: Revised P01-T01 names the focus-safe handler and
  progress lifecycle rather than relying solely on node stability. Revised
  P02-T01 specifies held-response assertions in the single budgeted helper,
  with no shared-helper source change. Implementation Changes must later
  record real-browser pending/settled focus and latest-selection results.
* Decision route: Direct planner correction. No user decision is required.

<!-- rpi:critique id=PC-002 -->
### PC-002 [High]: Wrapped controls have no defined vertical workspace safeguard

* Related IDs: AC1, AC3, C5/C7, P01-T02, P02-T01.
* Evidence: src/api/src/zava_forward/api/web/style.css:225-233 fixes the dialog
  to the viewport, makes its panel a height:100% flex column, and gives
  .map-workspace flex:1 with min-height:0. The proposed controls add a wrapping
  group above this workspace. The existing browser width loop in
  src/api/checks/map_fullscreen_browser_check.py:631-660 uses height 900 and
  checks horizontal bounds/map width, not map height. Its enlarged-font check
  at lines 326-400 also uses height 900 and currently measures only widths.
  The details at
  .copilot-tracking/details/2026-10-29/map-filters-551-phase-details.md:48-49,77-79
  say "usable map space" but define neither a vertical threshold nor a
  short-height case or overflow strategy.
* Concern: Six controls, selection words and a labelled area selector can
  consume many rows at 320px or 32px default text. A wrapping filter group can
  shrink the map/sidebar toward zero or push essential controls outside the
  visible dialog. Width-only checks and a tall viewport cannot distinguish a
  readable toolbar above an unusable workspace from a working layout.
* Impact: A narrow or landscape/short-window user may be unable to use the map,
  its list alternative or exit action even while every label fits horizontally.
* Smallest useful change: Define a vertical overflow strategy using existing
  containers and tokens that retains top-of-map filters, reachable exit and
  manual paths, and an explicitly measurable usable map rectangle. Add a
  short-height case, for example 390x568, within the already allocated browser
  helper; assert map height as well as width, control bounds and keyboard
  scrolling/reachability without overlap. Extend the already allocated
  640px/32px-font assertions to measure vertical bounds too. Include pending
  progress from PC-001 in the vertical-space checks. Keep all existing required
  widths, checks and regression cases.
* Action owner: Planning parent, with layout owned by P01-T02 and proof owned
  by P02-T01.
* Exact resolving evidence: Revised details state the overflow behavior,
  numeric minimum map dimensions and short-height fixture, with explicit
  vertical assertions in the existing helper/enlarged-font allocations.
  Implementation Changes must later link geometry and screenshots for both
  short-height and enlarged-text states, including reachable exit/manual path.
* Decision route: Direct planner correction. Selecting a bounded layout
  safeguard within the user's existing constraints is not a redesign decision.

<!-- rpi:critique id=PC-003 -->
### PC-003 [Medium]: The optional mapPanel argument invalidates the existing test extractor

* Related IDs: AC4, C6, P01-T01, P02-T01, locked test ownership/budget.
* Evidence: src/api/tests/test_map_fullscreen.py:9-11 extracts MAP at module
  import by splitting on the exact text
  "function mapPanel(coordinator = null) {". P01-T01 explicitly adds an optional
  filter-group argument to that declaration. P02-T01 mentions added source
  contracts but does not identify this existing setup dependency.
* Concern: Leaving that extractor unchanged causes IndexError before any map
  tests execute once the argument is added. Skipping the module or dropping
  existing contracts would violate the locked regression requirement.
* Impact: The specified unittest validation cannot run, and the promised
  automatic coverage is unavailable regardless of browser results.
* Smallest useful change: Explicitly include an edit to the existing MAP
  extraction setup so it locates the function with its new optional signature,
  without removing or weakening any existing assertion. Keep this within
  src/api/tests/test_map_fullscreen.py; it requires no added test method or
  budget increase.
* Action owner: Planning parent; P02-T01 test owner.
* Exact resolving evidence: Revised P02-T01 identifies the extractor update as
  an allowed existing setup edit, retains every current test method/assertion
  and the maximum two new methods, and retains the locked unittest selectors.
  Implementation evidence must show successful module import and execution of
  the old and new contracts using the final declaration.
* Decision route: Direct planner correction. No user decision is required.

## Strengths and Residual Risk

* One original control group and ovState avoid duplicated IDs and divergent
  filter models. A separate original header slot makes restoration explicit.
* Completed remains a header summary rather than becoming a false filter.
* The optional argument contains the change to Overview; Coordinator remains
  independently exercised with its existing population semantics.
* Existing lifecycle, selected-home removal, error, session-expiry, route
  cleanup, reduced-motion and manual-path checks remain required.
* Reports/screenshots stay outside committed generated targets. No additional
  dependency or test owner is needed for these findings.
* Local Chromium/axe proof is not screen-reader, cross-browser, full Fluent,
  WCAG conformance, human acceptance or publication approval. The supplied
  plan explicitly retains those limits and the prohibited-cloud gate boundary.

## Questions or Blocking Evidence Gaps

* None requiring a user response. The findings can be resolved by direct
  planning-parent revisions within confirmed scope and the locked test budget.

## Limitations

* This is a read-only assessment of the pre-implementation candidate, not an
  executed reproduction or implementation review. Focus and vertical outcomes
  are source-grounded integration risks, not claimed browser observations.
* No new external research or current guideline refresh was performed.
  Research W2 is the supplied dated evidence; implementation must still load
  and fetch web-design-guidelines as the plan requires.
* Existing untracked plan/details/research/session-state files were left
  untouched. No source, plan, details or research edits were made.

## Recommended Next Action

* Highest-impact finding: PC-001.
* Action owner: Planning parent.
* Smallest next action: Revise P01-T01/P02-T01 for focus-safe async integration
  and held-response proof; incorporate PC-002 and PC-003 in the same direct
  revision before finalizing Plan.
* User response required: No.
* Preserve this original Revise verdict and complete finding set. Do not start
  a second critique; the active parent owns disposition and later evidence.

## Artifacts

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-29/map-filters-551-plan.md](.copilot-tracking/plans/2026-10-29/map-filters-551-plan.md) | Assessed final-candidate plan |
| [.copilot-tracking/details/2026-10-29/map-filters-551-phase-details.md](.copilot-tracking/details/2026-10-29/map-filters-551-phase-details.md) | Assessed implementation and verification details |
| [.copilot-tracking/research/2026-10-29/map-filters-551-research.md](.copilot-tracking/research/2026-10-29/map-filters-551-research.md) | Supplied evidence pointers and selected design |
| [.copilot-tracking/reviews/plans/2026-10-29/map-filters-551-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-29/map-filters-551-plan-critique.md) | One complete independent critique |

## Next Steps

The active planning parent should resolve PC-001 through PC-003 directly,
record their dispositions without rewriting this original critique, and
finalize the plan before implementation. No user action is required.
This critique stops here; no peer stage or additional critique is invoked.

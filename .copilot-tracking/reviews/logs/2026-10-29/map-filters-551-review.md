<!-- markdownlint-disable-file -->
# Review: Expanded map filters

## Scope and Evidence

* Task ID: 551
* Review date: 2026-10-29
* Scope: Full task, P01-P02 and all four issue criteria.
* Plan: .copilot-tracking/plans/2026-10-29/map-filters-551-plan.md
* Phase details: .copilot-tracking/details/2026-10-29/map-filters-551-phase-details.md
* Critique: .copilot-tracking/reviews/plans/2026-10-29/map-filters-551-plan-critique.md
* Changes: .copilot-tracking/changes/2026-10-29/map-filters-551-changes.md
* Research: .copilot-tracking/research/2026-10-29/map-filters-551-research.md

## Opening Review State

* Goal: independently assess acceptance evidence, source correctness and
  reconciled plan/critique dispositions after implementation.
* Evidence readiness: all plan markers complete, actual local unittest,
  syntax, static and Playwright evidence available, including original failures.
* Acceptance basis: issue #551, approved plan and required UX standards.
* First boundary: current five-file implementation diff and dated artifacts.
* Read-only: only this review record may be edited; no source or plan changes.
* Initial blockers: none for bounded local review; no publication/human gate
  is satisfied or waived.

## Execution Status

* Execution status: Complete.
* Assessment count: exactly one independent original full-task Review.
* Assessed on 2026-10-29: the five-file working-tree implementation diff
  against HEAD 3e742ef13e45cb9de0590cbb5cb33e4996f5112e.
* SHA-256 of that five-file git diff HEAD:
  9e8ebadf385429dbd681c8e54d7f022d1f601cc7ba1eaf865eb822fd07c5873f.
* Branch: feat/map-filters-551; issue remains open; no matching PR returned
  by read-only gh inspection. Existing source/artifact changes were preserved.
* Read the complete changed app.js and style.css, all five implementation
  diffs, the complete supplied RPI artifact set, relevant project context,
  and the three governing UX standards. Inspected actual final browser JSON,
  original failed-run logs/scans and desktop, short-height and enlarged-text
  screenshots. Independently reran 35 focused tests and syntax/whitespace checks.
* Only this record is changed. No implementation, additional Review, agent,
  commit, push, cloud operation, database change or rubric edit was performed.

## Plan-to-Change Reconciliation

| Current plan scope | Changes summary | Current-state reconciliation | Assessment |
| --- | --- | --- | --- |
| P01-T01 | Shared controls and focus-safe map reads | Reconciled | Original filter/area group moves into dialog and back; ovState remains authoritative; button nodes are stable. |
| P01-T02 | Compact bounded layout and documentation | Reconciled | Dialog-only compact styles, hidden Completed summary, scroll cap, minimum workspace and documented native controls match current details. |
| P02-T01 | Source contracts and real-server browser regression | Reconciled with RV-001 | Required commands/results and retained failures are recorded; one claimed browser proof uses an ineffective oracle. |
| P01/P02 markers and handoff | Full implementation complete; one Review/local commit next | Reconciled | Markers describe executed implementation, not defect-free acceptance or publication. This record supplies the one Review result; parent owns continuation. |
| Follow-Up Items | None | Reconciled | No unresolved original follow-up was silently included in completion claims. |

## Completed Work Assessment

| Marker | Files | Assessment and evidence |
| --- | --- | --- |
| P01-T01 | src/api/src/zava_forward/api/web/app.js | Correct shared-node architecture. Same labelled select/handler and stable flag buttons prevent competing header/modal state. Non-returning read handlers bypass AsyncAction's control disable; draw retains region progress and request/error ownership. |
| P01-T02 | src/api/src/zava_forward/api/web/style.css; src/api/README.md | Compact count type and spacing consume existing Fluent-derived tokens. Bounded native scrolling preserves a 14rem workspace. Documentation accurately describes state, keyboard, Completed and Coordinator limits. |
| P02-T01 | src/api/tests/test_map_fullscreen.py; src/api/checks/map_fullscreen_browser_check.py | Two new unit methods, one top-level browser check helper with a nested route callback, and added enlarged-font assertions. No test method/helper removed; existing regressions retained. Budget respected. RV-001 concerns one browser assertion, not an observed application failure. |

### Correctness, pending reads and lifecycle

* Expansion inserts the same group before the workspace; collapse restores it
  to its original slot. Native dialog naming, modal containment, exit focus,
  first-Escape summary closure and second-Escape collapse remain intact.
  Disposal collapses before removal, invalidates the response sequence and
  prevents retained controls reopening the old modal.
* Stable buttons update aria-pressed and selection words only. Flag handlers
  suppress the already selected flag in production; area changes use the
  same ovState. No duplicate mapArea or independently synchronized filter
  model is introduced.
* A pending read keeps controls enabled and focused. Existing polite map
  progress and aria-busy distinguish pending selection from settled results.
  The held older successful flag read is released after a newer area response;
  final zero markers/status remain the newer selection. Existing request
  sequence checks also guard stale errors and stale fits.
* Failure clears markers, list and stale summary and presents an alert with
  recovery/manual paths. Selected-home removal and focus restoration remain
  exercised. Session-expiry evidence shows late responses do not fit/redraw a
  disposed map or issue further requests, including when route signals remain
  live. Pending-route navigation evidence shows modal/body-lock cleanup.
* Nonanimated pan:true resize and asymmetric fit padding affect the common
  map path, including Coordinator geometry. They do not change Coordinator
  authority, cohort queries, withheld fields or list selection. Existing
  Coordinator card-omission/list-focus regressions pass.

## Acceptance Criteria Assessment

The actual issue body was retrieved read-only with gh issue view 551.

| Criterion | Evidence assessed | Local assessment |
| --- | --- | --- |
| AC1: compact header filters at expanded map top | Computed smaller count type, group-before-workspace bounds, same six native controls, desktop and narrow screenshots | Supported. Completed is correctly excluded as a noninteractive summary. |
| AC2: marker and header state consistency | Six real-API flag populations (3/1/1/3/0/0), area changes, stable focus, original-node restoration, selected words/aria-pressed after collapse and header-to-modal changes, held stale-success case | Supported. Source confirms each returned item drives its marker; the new flag loop asserts counts, not an exhaustive per-flag marker-ID set. Existing summary/navigation checks verify concrete home IDs. |
| AC3: keyboard, non-colour state, narrow readability | Enter/Space activation, Tab traversal, pending native focus, selected words, focus styles, forced colours, 320/390/1280 widths, 390x568 and 640px with 32px default text | Supported within local Chromium engineering scope. Scrolling is intentional; not every filter is simultaneously visible at short height/enlarged text. Focus/scroll checks and manual paths retain access. |
| AC4: behavior covered automatically | Tracked real-loopback Playwright harness with actual filter/area result changes, plus source contracts; independently rerun 35 tests pass | Supported. Most browser checks assert actual behavior, not source strings. RV-001 limits the separate claimed proof of duplicate-request suppression. |

### Future PR linkage

All four literal issue criteria have bounded local evidence, so the issue-only
evidence supports eventual Closes #551 rather than requiring Refs #551 for an
unmet criterion. This does not make the RPI result defect-free: disclose and
route RV-001, preferably correct its oracle before asserting that every planned
validation obligation is proven. If a future candidate lacks the bounded
evidence above, use Refs instead. No PR is created, issue checkbox changed,
closure performed or publication authorized by this assessment.

## Implementation-Time Plan and Detail Update Assessment

| Affected scope | Update and trigger | Reconciliation and assessment |
| --- | --- | --- |
| P01-T01/P02-T01 | pan:false displaced the geographic centre during resize in run 1; changed to pan:true, animate:false | Current plan functional requirements, details, source contract and Changes all agree. Directly coupled nonanimated geometry correction, not new motion or authority. |
| P02-T01 | Run 2 measured clientHeight rather than the specified rectangle, missing two border pixels | Matching rectangle metric retained the threshold; not a relaxed pass condition. Original failure retained. |
| P02-T01 | Short-height helper left zoom inconsistent with pre-existing regression fixture in run 3 | Helper exit restores the original population/desktop fit. Existing assertions/scanner remain enabled. Appropriate isolation rather than suppression of a source failure. |
| P01-T01/P01-T02/P02-T01 | Run 4 found marker/attribution obstruction; raised workspace from 10rem to 14rem and bottom fit padding to 60px | Stronger threshold appears in current plan, details, CSS, browser checks and Changes. Actual final short-height and enlarged-text geometry meet it. |
| P02-T01 | Run 5 found obstruction after viewport change without a new population fit; layouts now execute a filter read/refit | Appropriate for proving filter behavior at each layout. Does not prove arbitrary resize/pan/zoom never produces marker overlap. Original adverse evidence and the list alternative remain explicit. |

These are immediately relevant implementation/fixture amendments within the
confirmed design. No significant divergent decision or new user approval
requirement was found; no second critique or Review is required or performed.

## Critique and Material Revision Assessment

* Original Revise verdict and PC-001/PC-002/PC-003 remain preserved.
* PC-001: plan correctly specifies non-control reads, region progress, pending
  focus and stale-response handling. Production and real held-response checks
  resolve the substantive disable/focus concern. Duplicate suppression exists
  in source, but the claimed behavioral negative proof needs RV-001.
* PC-002: current plan defines 45% bounded scrolling, 14rem height and measured
  short-height/enlarged-text behavior. Final JSON records 224px and 448px map
  heights respectively; screenshots show usable map/manual paths.
* PC-003: exact-signature extractor was updated, not bypassed. All original
  contract methods remain; independent focused module execution succeeds.
* Current plan/details record the compatible dispositions before the completed
  implementation handoff. No unresolved decision or evidence of premature
  dependent-work resumption was found.

## Plan Follow-Up Assessment

| Follow-up | Why outside immediate scope | Owner/next action | Assessment |
| --- | --- | --- | --- |
| None in the supplied plan/Changes | Not applicable | None | No existing follow-up is converted into an active task. |

## Findings

<!-- rpi:review id=RV-001 -->
### RV-001 [Low]: Duplicate-read browser assertion measures an invariant

* Related scope: P02-T01, PC-001 resolving evidence.
* Evidence: src/api/checks/map_fullscreen_browser_check.py:137-141 only
  appends the first request to held and continues every subsequent request.
  At line 154, after a second Space activation, len(held) == 1 is therefore
  true even if that activation emitted another request. The printed
  "selected flag suppresses duplicate reads" pass is not request-count proof.
* Impact: This individual browser oracle cannot detect the regression it
  names. The production guard at
  src/api/src/zava_forward/api/web/app.js:1965 is present and correct by
  inspection, and the source-contract test checks its presence. No duplicate
  application request or incorrect marker behavior is claimed as observed.
  Other genuine filter/area browser evidence still supports AC1-AC4.
* Destination: later rpi-implement; test implementation defect, not a new
  product decision, material research gap or broad accessibility audit.
* Smallest useful next action: within the existing helper, observe every
  page-originated map request around the repeated selected activation and
  assert no additional request after the activation has been processed.
  Keep the held/out-of-order case and existing test budget; demonstrate that
  the negative assertion would fail if duplicate requests were emitted.
  Do not implement this correction as part of this Review.

## Defects

* RV-001: one Low browser-test oracle defect. No application correctness
  defect identified in the bounded issue implementation.

## Routed Findings

| Finding | Destination | Owner/next action | Reason |
| --- | --- | --- | --- |
| RV-001 | rpi-implement | Parent's later implementation step, if authorized; correct actual-request observation and run focused evidence | Deterministic test correction within the accepted plan; no new research or design decision needed. |

Later implementation of this finding does not require another Review.

## Web Guideline Assessment

Fresh complete source fetched with web_fetch on 2026-10-29 from
https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md.
Reviewed both complete changed web files against all fetched rule groups,
with findings bounded to this issue and coupled behavior, not a repository audit.

| Rule group | Assessment of this issue boundary |
| --- | --- |
| Accessibility | Native named buttons/select, clickable label, group name, aria-pressed, live map status/error and retained semantic heading/manual paths. Native buttons supply keyboard activation; no redundant custom button key handler needed. |
| Focus states | Existing focus-visible replacement retained; stable nodes/pending focus, modal containment and focus-safe scrolling checked. |
| Forms | Area select now has name/autocomplete and associated label; no new text-entry, paste, submission or unsaved-state behavior. |
| Animation | No new animation; nonanimated resize/fitting preserves reduced motion. Existing token transitions retained. |
| Typography | Existing Fluent-derived type/rem tokens and plain ASCII punctuation retained. Generic curly-quote/ellipsis advice does not override the repository standard. Numeric comparisons/tables outside this slice unchanged. |
| Content handling | min-width:0, wrapping labels, bounded native scrolling, explicit zero/error/pending states; no new unconstrained user-text rendering. |
| Images | No image/media added or changed; no new dimensions, loading-priority or caption obligation introduced. |
| Performance | Six controls, in-place state updates and CSS flex/grid; no new large list, font fetch or render-time layout measurements. Geometry reads are browser assertions, not application rendering. |
| Navigation and state | Same page-session ovState deliberately retained; URL-state migration explicitly excluded by accepted plan. Native navigation links/manual paths retained; no destructive action added. |
| Touch and interaction | Compact buttons use touch-action:manipulation; scroll containment/native controls/manual map paths retained. No new gesture-only or autofocus behavior. |
| Safe areas and layout | Existing safe-area padding/dynamic viewport retained; scoped overflow and minimum workspace measured at required layouts. |
| Dark mode and theming | Existing light theme retained; expanded native select has explicit token foreground/background. No new dark theme or theme-color change. |
| Locale and i18n | Existing labels/count conventions retained; no new date/currency formatter or locale detection. This slice is not a locale-system migration. |
| Hydration safety | Vanilla DOM application; no server/client hydration or controlled framework input introduced. |
| Hover and interactive states | Existing hover border, pressed state and two-tone focus retained with visible state words. |
| Content and copy | Specific action labels, plain active wording and native selection words. Repository wording overrides generic title-case/ampersand advice. |
| Anti-patterns | No new disabled zoom, paste blocking, transition:all, focus removal, fake action elements, unlabelled input/icon or gesture-only interaction. |

### src/api/src/zava_forward/api/web/app.js

Pass for the bounded changed behavior, with the explicit existing page-session
state/URL guideline divergence above. No new web-guideline defect identified.

### src/api/src/zava_forward/api/web/style.css

Pass for the bounded changed behavior. Native token foundations, visible
non-colour selection and scroll-based reflow retained; no full Fluent adoption
or WCAG conformance inferred.

## Validation Evidence

External evidence root supplied by the caller:
/home/azureuser/.copilot/session-state/0bf3465f-5e57-4315-8cca-77967665eb60/files.
Exact original implementation commands remain in Changes, unchanged.

| Check | Status | Evidence and limits |
| --- | --- | --- |
| Independent focused unittest rerun | Passed | From src/api: PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src:tests:../core/src:../agents/src:../core/tests:../agents/tests python3 -m unittest test_map_fullscreen test_accessibility_baseline test_design_system test_content_standard test_loading_feedback test_workspace_scripts -q. 35 tests, 0.378s, OK. No shared editable checkout used. |
| Independent syntax/whitespace | Passed | node --check src/api/src/zava_forward/api/web/app.js; git diff --check, both from repository root. |
| Changed-Python Ruff/mypy | Reported passed; not rerun by reviewer | Changes records exact selectors and successful results for both changed Python files. |
| Final real-server browser run | Passed evidence inspected, with RV-001 oracle limitation | map-filters-browser-6.log contains 247 printed PASS checks, plus unprinted Playwright expect assertions in source. browser.json records Chromium 156.0.8078.4 and errors=[]. This Review did not rerun the full browser harness. |
| Final axe scans | 14 states, zero reported violations | Actual axe-results.json inspected: axe 4.10.3, WCAG tag selection retained, no unresolved ARIA references. Every state also contains color-contrast incomplete results, 5-13 nodes; not an all-rules/manual contrast pass. Examples include short marker text and scroll-obscured content. Existing token contrast tests pass but do not resolve every rendered incomplete node. |
| Geometry and visual evidence | Inspected | filters.json: no horizontal group/page overflow at 320/390/1280 and 390x568; map widths 156.61/195.11/912/195.11px; heights 359.61/359.61/617.61/224px. enlarged-font.json: root 32px, map content width 271px, rectangle height 448px, no measured horizontal overflow. Opened desktop, short-height and enlarged-text screenshots. |
| Original adverse evidence | Preserved and inspected | Runs 1-5 remain external: displaced viewport, border-metric failure, fixture zoom overlap, short-height attribution overlap and resize-without-refit overlap. No failed outcome overwritten or scanner disabled. |
| Supplementary isolated MCP geometry probe | Unavailable; no result claimed | Optional read-only probe failed before rendering because the MCP execution environment provided neither dynamic import nor require. No files written; browser closed. Existing actual-app geometry evidence above remains the review basis. |
| Full publication gate, hosted CI and human acceptance | Intentionally not run/not claimed | Full gate includes prohibited az; no publication requested. No screen-reader, voice-control, Firefox/Safari, 400% zoom, live-tile or live employee-site acceptance claimed. No installs, private data or cloud fallback used. |

## Residual Work

* No original plan follow-up item remains unresolved. RV-001 is routed once
  as a test defect, not duplicated as residual work.
* Existing full Fluent runtime adoption, whole-workflow accessibility/manual
  acceptance and publication gates remain with their established owners and
  scopes. This issue does not close or silently expand them.

## Blockers and Remaining Work

* Review blockers: none; credible bounded assessment completed.
* Remaining implementation follow-through: RV-001 actual-request oracle.
  The parent also owns the separately authorized local commit, outside this
  reviewer's single-file authority.
* Publication remains blocked by the explicit no-az/no-push boundary; focused
  checks do not waive the complete gate, human approval or hosted checks.

## Outcome

* Outcome: Defects found.
* Severity: 0 Critical, 0 High, 0 Medium, 1 Low (RV-001).
* Rationale: Correctness and all four literal issue criteria are supported
  within the bounded local evidence. One newly added browser assertion does
  not prove its claimed duplicate-request suppression property. This is a
  nonmaterial test defect, not an observed product failure or rejection of
  the selected architecture. Do not describe the result as defect-free.
* Accepted guideline differences are justified by the confirmed page-session
  scope and governing Fluent/native/plain-content standards, not by ignoring
  the freshly fetched source.
* Local engineering acceptance of the four criteria is distinct from human,
  accessibility-conformance, hosted CI, complete-gate and publication approval.

## Closeout Routing Record

| Finding class | Destination | Owner/next action |
| --- | --- | --- |
| Implementation/test defect | rpi-implement | Parent routes RV-001 to a later bounded test correction, with actual-request evidence. |
| Decision gap or invalid assumption | None | No new plan decision required. |
| Material research gap | None | No new research required for the deterministic oracle correction. |
| Non-blocking distinct residual work | None added | Existing broader acceptance/gate owners remain unchanged. |

* Execution status: Complete.
* Outcome: Defects found, one Low test-oracle finding.
* Continuation: return this one Review result to the active parent; do not
  launch a fix, another Review, publication or any peer stage here.

## Artifacts

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/research/2026-10-29/map-filters-551-research.md](.copilot-tracking/research/2026-10-29/map-filters-551-research.md) | Research and source boundary |
| [.copilot-tracking/plans/2026-10-29/map-filters-551-plan.md](.copilot-tracking/plans/2026-10-29/map-filters-551-plan.md) | Current plan and critique dispositions |
| [.copilot-tracking/details/2026-10-29/map-filters-551-phase-details.md](.copilot-tracking/details/2026-10-29/map-filters-551-phase-details.md) | Current implementation/validation details |
| [.copilot-tracking/reviews/plans/2026-10-29/map-filters-551-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-29/map-filters-551-plan-critique.md) | Preserved original Revise critique |
| [.copilot-tracking/changes/2026-10-29/map-filters-551-changes.md](.copilot-tracking/changes/2026-10-29/map-filters-551-changes.md) | Exact implementation commands and adverse evidence |
| [.copilot-tracking/reviews/logs/2026-10-29/map-filters-551-review.md](.copilot-tracking/reviews/logs/2026-10-29/map-filters-551-review.md) | This one original Review and RV-001 |

## Next Steps

The active parent receives execution Complete / outcome Defects found and owns
any later rpi-implement routing for RV-001 and local-only continuation. No user
response, second Review, source fix, push or cloud action is performed here.

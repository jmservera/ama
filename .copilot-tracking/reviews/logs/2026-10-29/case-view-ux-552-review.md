<!-- markdownlint-disable-file -->
# Review: Compact case view

## Scope and Evidence

* Task ID: 552
* Review date: 2026-10-29
* Review scope: single independent post-implementation Review of the local code slice.
* Plan: .copilot-tracking/plans/2026-10-29/case-view-ux-552-plan.md
* Phase details: .copilot-tracking/details/2026-10-29/case-view-ux-552-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-10-29/case-view-ux-552-plan-critique.md
* Changes: .copilot-tracking/changes/2026-10-29/case-view-ux-552-changes.md
* Research: .copilot-tracking/research/2026-10-29/case-view-ux-552-research.md

## Opening Review State

* Interpreted review goal: compare the six issue criteria to the complete uncommitted implementation, assets, regression coverage and supplied validation.
* Review scope: source, tests, browser check, README and the supplied dated RPI set; no publication acceptance.
* Evidence readiness: plan and changes record available; remaining artifacts, full diff, assets and check implementation require comparison.
* Acceptance basis: issue #552, current plan, PC-001/PC-002 dispositions, repository Fluent 2, accessibility and content baselines, and freshly fetched Web Interface Guidelines.
* First comparison boundary: reconcile the artifacts, then inspect changed source and test assertions against all six criteria.
* Active read-only boundaries: only this review record may be written; no fixes, agents, repeated critique/Review, commit, push, Azure or rubric changes.
* Initial blockers: direct inspection of externally stored browser JSON/screenshots under /tmp is prohibited by the review environment's file-operation restriction. Recorded browser evidence remains available in the changes record; distinguish reported results from directly inspected evidence.

## Execution Status

* Execution status: Partial.
* Review execution evidence: the complete tracked diff, every new browser-check line, both added unittest methods, all six PNGs, slide-four image relationships and bytes, README, all supplied RPI artifacts and current session state were inspected. The issue's six criteria were retrieved using gh. The review did not directly inspect the external baseline/final JSON or screenshots because file operations under their location are prohibited in this environment.
* This is the one independent post-implementation Review. No agents, further critique, second Review, source fixes, commits, pushes, Azure commands or rubric changes were performed.
* Outcome: Residual work. No implementation defect was identified in the inspected local slice; the mandatory independent rendered-evidence inspection remains incomplete. This is not a conformant acceptance or publication verdict.

## Plan-to-Change Reconciliation

| Current plan scope | Descriptive changes-record summary | Current-state reconciliation | Gap or rationale |
| --- | --- | --- | --- |
| P01-T01 | Baseline and Asset Provenance | Reconciled for assets; baseline reported | All six 256x256 PNGs are byte-identical to their named slide-four media. Baseline fixture and collection code inspected; external results not directly inspected. |
| P01-T02 | UI Implementation | Reconciled | Exact icons, compact token spacing, one-line summaries, full native disclosures and attached tabs are present. Backend/manual actions and state classification are unchanged. |
| P02-T01 | Validation | Reconciled as recorded execution | 54 tests, syntax, Ruff, mypy and final browser run are explicitly recorded. Earlier harness failures and corrections remain visible. RV-001 limits independent verification of rendered outcomes. |
| P02-T02 | Remaining Work and Limitations; Pre-Review Reconciliation | Correctly pending | This Review must return before the parent reconciles its outcome and makes the local commit. The unchecked phase/task is not stale evidence or a defect. |
| Follow-Up Items | Remaining Work and Limitations | Reconciled | Human/AT/cross-browser acceptance and full Fluent adoption remain outside this slice. Publication is neither performed nor waived. |

## Completed Work Assessment

| Related marker | Files | What changed and why | Completion evidence | Validation | Assessment |
| --- | --- | --- | --- | --- | --- |
| P01-T01 | src/api/src/zava_forward/api/web/journey-icons/{survey,assessment,funding,resident,contractor,quality}.png | Reuse exact presentation icons, not a substitute set | Direct visual inspection of all six files; direct ZIP relationship inspection and byte comparison against docs/capstone/deck/zava-forward-cowork-v2-draft.pptx | Passed direct read-only comparison; recorded hashes match | Supported |
| P01-T02 | src/api/src/zava_forward/api/web/case-workspace.js | Preserve all six visible labels and state words; separate native disclosure buttons from links; show complete reasons, owners and next actions with explicit missing-field recovery | Complete source inspection; safe text construction; unique summary/step IDs; native auto popover and focusable region | Node syntax passed freshly; shipped-JS unittest/browser passes reported | Source supported; rendered inspection limited by RV-001 |
| P01-T02 | src/api/src/zava_forward/api/web/style.css | Reduce padding/grid stretch, constrain only blocker summaries, bound scrollable disclosures, join wrapping tabs to panels | Complete changed-rule inspection against Fluent tokens and fetched guidelines | Recorded default-size, 200% root text, short-height, reduced-motion and narrow measurements | Source supported; visual outcome not independently observed |
| P01-T02 | src/api/src/zava_forward/api/web/app.js | Prepend tablist to workspace, enable panel-only scroll bounds, remove tab/layout state after enhancement failure | All four added lines and surrounding safety, mounted-panel and catch paths inspected | Node syntax passed freshly; both fallback browser scenarios reported | Supported without backend or governance changes |
| P02-T01 | src/api/tests/test_case_journey.py | Update intended concise status expectation; preserve complete blocker data; test exact icon bytes and safe full disclosure with separate controls | Complete test diff; two new methods, within three-method budget; no regression suppression or unrelated test edits | Parent reports 54 passing tests across five modules | Supported |
| P02-T01 | src/api/checks/case_view_ux_browser_check.py | Use the real synthetic loopback app to measure geometry and keyboard/touch/fallback behavior | All 399 lines inspected, plus reused fixture/server isolation and cleanup | Parent reports final Chromium 156.0.8078.4 / Playwright 1.64.0 run passed | Meaningful checks, not replacement-page or source-string geometry proxies; raw output inspection pending |
| P02-T01 | src/api/README.md | Describe behavior, asset provenance, commands and limitations | Complete documentation diff | Documentation/source comparison and git diff --check passed | Accurate local engineering boundary; no acceptance overclaim |

## Issue Criterion Disposition

| Issue #552 criterion | Code and measurable recorded evidence | Disposition |
| --- | --- | --- |
| 1. Presentation icon set with text labels | Six exact media mappings verified directly: survey/image11, assessment/image6, funding/image12, resident/image13, contractor/image14, quality/image15. Source retains Survey, Assessment, Funding, Resident agreement, Contractor, Quality and handover; decorative images have explicit 24x24 dimensions, empty alt and aria-hidden. Browser check asserts six loaded icons. | Source and provenance verified; rendered loading reported, not independently observed. |
| 2. Visibly thinner layout | Padding falls from sp-3 to sp-2; zero vertical link-grid gap and align-items:start prevent the tall blocked step stretching all desktop steps. Same-fixture baseline reports 1464.95px desktop; narrow blocked steps 690.11px/975.58px and ordinary steps 78.39px. Final reports 66.39-110.39px desktop, 66.39px ordinary and 110.39px blocked at both narrow widths. Reported ceilings <=132px/<=116px pass; ordinary narrow steps shrink 15.3%, blocked narrow steps 84.0%/88.7%. | Source supported and quantified results reported; direct before/after visual and raw measurement comparison incomplete, RV-001. |
| 3. One-line summary and keyboard/touch full reason | First sentence in a nowrap/ellipsis span; explicit Details text and native button. Every reason/owner/action remains in a viewport-bounded, focusable, scrollable auto popover. Tests exercise Enter, Space, Escape, returned focus, touch activation/swipes/light-dismissal and missing owner/action. Recorded 320x480 scrollTop1094, scrollHeight1548/clientHeight454; 200% text scrollTop7808, scrollHeight8238/clientHeight430, final next action reachable. | Source and meaningful assertions supported; interaction/reachability passes reported, direct JSON/screenshots incomplete, RV-001. |
| 4. Tabs attached, outside inner scroll; panel beneath scrolls | app.js prepends tablist as sibling before panels in one bordered workspace. Only direct child panels receive 70dvh overflow bounds; tabs wrap without a scrolling wrapper. Existing manual keyboard selection, URL/back, mounted panels and field retention remain. Browser check measures unchanged tablist box while panel scrollTop increases. | Source verified and browser outcome reported; direct attached-tabs screenshot inspection incomplete, RV-001. |
| 5. Fluent 2 and WCAG baselines preserved | Existing semantic tokens, native buttons/links, focus-visible rule, status words, forced-colors selection and reduced motion remain. No backend/action/authority changes; persistent open safety remains outside the workspace bounds. Reported regression modules cover journey, workspace scripts, design system, accessibility and content, 54 tests. Fresh guidelines source and all changed web code reviewed. | No material source regression identified; local engineering preservation supported, not full Fluent adoption or WCAG/AT acceptance. Rendered review limitation remains. |
| 6. Desktop/narrow browser evidence | Dedicated check captures 1280/390/320 CSS px, JSON and named journey/case screenshots, popovers and attached tabs. Changes record reports final complete run and no overflow or unexpected JS errors. | Evidence generation reported; required independent artifact inspection incomplete, RV-001. Do not mark the whole issue independently accepted on this Review alone. |

## Implementation-Time Plan and Detail Update Assessment

| Affected area or marker | What changed and why | Triggering evidence and user decision | Reconciliation performed | Planning and critique state | Assessment |
| --- | --- | --- | --- | --- | --- |
| P01-T01 | Use tracked capstone slide-four icons because docs/presentations is absent | Research C4 and direct matching deck media; confirmed intent is existing presentation icons, not a specific directory | Research, plan, details, changes and README agree | Already within final-candidate planning/critique | Compatible local choice, no divergent decision |
| P01-T02/P02-T01 | Bound and scroll long popovers; add final-content keyboard/touch and enlarged-text assertions | PC-001; implements existing accessibility/reachability intent | Current plan disposition, details and implementation agree | Original Revise preserved; no second critique | Direct compatible correction; source and assertions inspected, final runtime results reported |
| P01-T02/P02-T01 | Remove enhancement-only layout/tab state; test unavailable script and post-mutation exception | PC-002; preserves existing manual fallback | Current plan disposition, details, catch cleanup and both browser scenarios agree | Original Revise preserved; no second critique | Compatible correction, no material scope expansion |
| P02-T01 | Wait for native scroll completion; use dispatched touch swipes; use actual keyboard focus; accept the synthetic dirty-note dialog and wait for the new case | Earlier harness failures recorded in changes; no production workaround or changed product intent | Changes retain failures and final correction rationale; final assertions remain meaningful | No new owner decision or plan critique warranted | Supported harness corrections, not erased failures |

## Critique and Material Revision Assessment

* Latest critique dispositions: the single original critique remains Revise with PC-001 and PC-002, both Medium. The current plan explicitly directly resolves both; no original outcome was rewritten.
* PC-001: source constrains inline/block dimensions, allows overflow and word wrapping, provides focusable native scrolling and complete field recovery; the check verifies the final item's actual bounds after keyboard and real dispatched touch gestures, including 200% root text. The supplied final run is reported passing; direct external inspection remains RV-001.
* PC-002: fallback cleanup removes the inserted tablist and case-sections class and restores listed panels. The check independently exercises an unavailable script and a post-layout injected exception, checks all nine unbounded panels, ordinary input, absent tabs and persistent open safety above the workspace. The injected error is handled by the real catch and checked through its expected message, not waived as an arbitrary page error.
* Material revisions: none beyond the recorded compatible verification corrections. No new framework, dependency, source ownership or governance decision was introduced.
* Dependent-work pause assessment: current artifacts consistently state corrections were incorporated before implementation; no evidence of proceeding past an unresolved significant owner decision.
* Justification assessment: supported. Current plan, details, descriptive changes and handoff agree; no rpi-plan destination is needed.

## Plan Follow-Up Assessment

| Follow-up item | Why outside immediate scope | Owner or next action | Assessment and route |
| --- | --- | --- | --- |
| Cross-browser, assistive-technology and real-user acceptance | Existing wider baseline, not a new local Chromium criterion or permission to claim conformance | Project owner to schedule the separate browser/AT/user acceptance work described in docs/reference/research/ux/wcag-conformance-baseline.md | Open distinct follow-up; not an implementation defect or additional active plan task |
| Full Fluent library adoption | Existing #150 work; this task preserves native Fluent token foundations without selecting a replacement framework | #150 owner to integrate/validate actual Fluent implementation or obtain explicit acceptance of a native-only substitute | Open distinct follow-up; not closed or expanded by #552 |

## Fresh Changed-Web Guidelines Review

Source fetched successfully in this Review on 2026-10-29:
https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md.

All changed web code was compared against all fetched rule categories. No new forms, hydration, media, locale, font/CDN, large-list, destructive-action or animation behavior is introduced; unrelated pre-existing controls and copy are not new findings. Native buttons supply keyboard activation. New images are above-fold decorative icons with dimensions; explicit labels and state words retain meaning without images/color. URL-backed manual tabs, word wrapping, focusable bounded scrolling, native dismissal and touch manipulation are retained. The repository's sentence case/plain ASCII and owner-selected Fluent foundations take precedence over generic title-case/curly-quote/ellipsis preferences. Full rendered-state review is limited by RV-001.

### src/api/src/zava_forward/api/web/case-workspace.js

Pass: no new material source finding.

### src/api/src/zava_forward/api/web/app.js

Pass: no new material source finding.

### src/api/src/zava_forward/api/web/style.css

Pass: no new material source finding.

## Findings

### .copilot-tracking/changes/2026-10-29/case-view-ux-552-changes.md

.copilot-tracking/changes/2026-10-29/case-view-ux-552-changes.md:121 - RV-001 [Medium]: final and baseline rendered evidence is reported but cannot be directly inspected in this Review environment.

<!-- rpi:review id=RV-001 -->
### RV-001 [Medium]: Required independent rendered-evidence inspection remains incomplete

* Related scope: P02-T01/P02-T02; issue criteria 2, 3, 4 and 6, with a rendered-validation limitation on 1 and 5.
* Evidence: .copilot-tracking/changes/2026-10-29/case-view-ux-552-changes.md:121-130 reports the final JSON and desktop/narrow/popover/attached-tabs PNGs; its P01-T01 section reports the baseline. The requested final directory is /tmp/case-552-ui-complete-20261029 and baseline directory is /tmp/case-552-baseline-20261029. This reviewer cannot perform file operations in those locations. No raw JSON or application screenshots were inspected, copied, regenerated or represented as independently observed.
* Impact: code, exact assets and assertion quality can be assessed credibly, but the explicit visual comparison and raw recorded measurement inspection cannot be completed. Reported local results are not independent acceptance of all six criteria.
* Destination: rpi-research, bounded evidence reconciliation by the active parent; not rpi-implement and not a production defect.
* Smallest useful next action: the parent, in an environment authorized to read the existing external evidence, should inspect baseline/final results.json and desktop, 390/320px, keyboard/touch/enlarged-text popover and attached-tabs PNGs; reconcile the figures and visible states against this record. If permission requires relocating evidence, obtain appropriate authority and preserve originals. Do not rerun this Review, fabricate evidence, waive the restriction or change source as a substitute.
* Acceptance effect: leave independent rendered acceptance open until that distinct evidence action is completed; preserve this original Partial/Residual work outcome.

## Defects

* None identified in the inspected source/test/documentation slice. RV-001 is a review evidence-access gap, not an observed product failure.

## Routed Findings

| Finding | Destination | Owner or next action | Reason for route |
| --- | --- | --- | --- |
| RV-001, Medium | rpi-research | Active parent: bounded inspection/reconciliation of existing raw browser evidence under valid file-access authority | Missing independent evidence inspection, not implementation or decision drift |

Later implementation of any subsequently established defect does not require another Review. This task must not be put into a repeated Review loop.

## Residual Work

* RV-001: independent inspection of existing rendered browser evidence.
* Distinct existing project follow-ups: cross-browser/AT/user acceptance and #150 Fluent integration; neither is recast as a #552 source defect.
* Publication/full local gate and hosted/human approval are separate unperformed gates, not residual tasks silently added to this local plan. No push or az authorization exists.

## Blockers and Remaining Work

* Review blocker: direct access to the named external browser artifacts is unavailable under the active environment restriction. This limits execution to Partial without negating the completed source comparison.
* Remaining active work: parent must receive and reconcile this original Review outcome; P02-T02 Review/local commit necessarily remains unchecked here. The parent owns any later privacy-safe local commit and artifact-state reconciliation, not this reviewer.
* No material implementation blocker or significant unresolved product decision was found. Issue-wide independent acceptance remains incomplete because of RV-001.

## Validation Evidence

| Command or evidence | Scope | Status | Summary |
| --- | --- | --- | --- |
| gh issue view 552 --json body,title,state | Exact issue criteria | Passed, freshly executed | Six supplied criteria match the open issue; no issue mutation |
| Python read-only ZIP/XML/PNG inspection | All six icons and deck slide-four relationships | Passed, freshly executed | All six exact bytes, 256x256 PNG headers and recorded SHA-256 values match; all six images directly viewed |
| node --check src/api/src/zava_forward/api/web/app.js; node --check src/api/src/zava_forward/api/web/case-workspace.js | Changed JavaScript | Passed, freshly executed | Both syntactically valid |
| git diff --check | Complete tracked uncommitted diff | Passed, freshly executed | No whitespace errors |
| Fresh Web Interface Guidelines fetch and complete changed-web source comparison | Three changed web files | Passed for source review; rendered review incomplete | No new material source finding; repository standards retain precedence |
| Current-root PYTHONPATH with installed interpreter; unittest test_case_journey test_workspace_scripts test_design_system test_accessibility_baseline test_content_standard -q | Five directly related regression modules | Passed, reported by parent and changes record; not rerun | 54 tests; final reported 3.264s. Explicit current source roots avoid another worktree's editable installs |
| Ruff check and format --check for new browser check and changed journey tests | Python lint/format | Passed, reported; not rerun | Initial corrections and subsequent passes preserved |
| Focused mypy for checks/case_view_ux_browser_check.py | New browser check | Passed, reported; not rerun | Typed result corrections recorded |
| checks.case_view_ux_browser_check --baseline and final complete run | Real constructed-data loopback app, 1280/390/320px, long blockers, 320x480, 200% text, keyboard/touch, tabs/state and two fallbacks | Passed, reported; raw output unavailable to this reviewer | Harness directly inspected: sanitized server environment, explicit synthetic ZF_DATA, loopback readiness check, external browser traffic blocked, owned process/browser cleanup. No private/default dataset or cloud/model use |
| Requested raw baseline/final results.json and application screenshots | Direct visual/raw measurement comparison | Unavailable | Prohibited file-operation location; RV-001 |
| Additional browser reproduction or broad suite | Unchanged source doubts | Skipped | No concrete product defect needing the one allowed reproduction; no redundant large suite |
| Cross-browser, actual AT, human/user and full WCAG/Fluent acceptance | Wider project acceptance | Unperformed | Not established by local Chromium, source review or existing engineering tests |
| Full publication/local gate, hosted checks, push and Azure operations | Publication | Unperformed, not waived | Outside local authorization; no publication-ready or gate-passed claim |

## Outcome

* Outcome: Residual work.
* Outcome rationale: exact assets, complete local source behavior, test intent, critique dispositions and artifact coherence are supported; fresh read-only syntax/provenance/hygiene checks pass. No material local source defect was identified. The explicit direct screenshot/raw browser comparison was not performed, so this Review cannot certify the full local acceptance set. RV-001 routes that bounded evidence gap once without repeating Review or editing implementation.
* Severity summary: Critical 0; High 0; Medium 1 evidence gap; Low 0; implementation defects 0.
* No publication, legal/safety approval, complete Fluent adoption, full WCAG conformance, cross-browser or AT/user acceptance is inferred.

## Closeout Routing Record

| Finding class | Destination | Owner or next action |
| --- | --- | --- |
| Implementation defect | None | No source defect established |
| Decision gap or invalid assumption | None | No significant divergence or unresolved product decision |
| Material evidence gap | rpi-research | Parent reconciles existing rendered evidence under valid access authority, RV-001 |
| Non-blocking residual work | Distinct existing follow-ups | Project owner schedules browser/AT/user acceptance; #150 owner handles Fluent adoption |

* Execution status: Partial.
* Outcome: Residual work.
* Validation coverage: complete source/test/asset/artifact inspection; fresh provenance, syntax and diff checks; recorded five-module/lint/type/browser passes assessed but not relabeled as freshly executed.
* Blockers: direct inspection of externally located browser JSON/screenshots unavailable; no code defect established.

## Artifacts

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/research/2026-10-29/case-view-ux-552-research.md](.copilot-tracking/research/2026-10-29/case-view-ux-552-research.md) | Source evidence and selected direction |
| [.copilot-tracking/plans/2026-10-29/case-view-ux-552-plan.md](.copilot-tracking/plans/2026-10-29/case-view-ux-552-plan.md) | Current scope and pending P02-T02 |
| [.copilot-tracking/details/2026-10-29/case-view-ux-552-phase-details.md](.copilot-tracking/details/2026-10-29/case-view-ux-552-phase-details.md) | Task detail and PC corrections |
| [.copilot-tracking/reviews/plans/2026-10-29/case-view-ux-552-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-29/case-view-ux-552-plan-critique.md) | Preserved original Revise verdict |
| [.copilot-tracking/changes/2026-10-29/case-view-ux-552-changes.md](.copilot-tracking/changes/2026-10-29/case-view-ux-552-changes.md) | Implementation and reported validation |
| [.copilot-tracking/reviews/logs/2026-10-29/case-view-ux-552-review.md](.copilot-tracking/reviews/logs/2026-10-29/case-view-ux-552-review.md) | This single independent Review |
| [src/api/src/zava_forward/api/web/case-workspace.js](src/api/src/zava_forward/api/web/case-workspace.js) | Journey and native disclosure implementation |
| [src/api/src/zava_forward/api/web/app.js](src/api/src/zava_forward/api/web/app.js) | Workspace attachment and fallback cleanup |
| [src/api/src/zava_forward/api/web/style.css](src/api/src/zava_forward/api/web/style.css) | Compact layout, popover and attached-panel styling |
| [src/api/checks/case_view_ux_browser_check.py](src/api/checks/case_view_ux_browser_check.py) | Dedicated measurable real-app browser checks |
| [src/api/tests/test_case_journey.py](src/api/tests/test_case_journey.py) | Shipped-JS and exact-asset regressions |
| [src/api/README.md](src/api/README.md) | Behavior, commands and limitations |

## Next Steps

Return to the active parent. Preserve this original Review and its Partial/Residual work outcome; route RV-001 to bounded evidence reconciliation without another critique or Review. Reconcile P02-T02 and any local commit only in the parent's authorized continuation. No source fix, push, Azure operation, rubric edit or publication approval is authorized by this record.

---
title: "Review: chat-widget-550-copilot-fixes"
description: "Independent bounded post-implementation review for parent550-rebase."
ms.date: "2026-10-29"
---

## Opening Review State

* Interpreted review goal: independently assess the four requested local corrections on feat/chat-widget-550, PR 556, without publication or source edits.
* Review scope: task 550-copilot-fixes (parent550-rebase); six specified changed files and necessary adjacent app.js and CSS context.
* Evidence readiness: canonical research, plan, phase details, critique, changes and state paths supplied; external validation paths supplied, pending comparison.
* Acceptance basis: shared stacking above map 1000 and below account 1200; readable Close hover; pre-append bottom and outside-history follow guard; same-context installation guard; retained focus, no theft and reduced-motion behavior.
* First comparison boundary: reconcile current plan/detail/critique/change markers, then compare the bounded git diff and validation evidence.
* Active read-only boundaries: all source and task evidence read-only; only this review record may be written. No other workers, remote changes or publication gates.
* Initial blockers: none identified before evidence comparison.

## Scope and Evidence

* Task: 550-copilot-fixes; parent: 550-rebase (parent550-rebase).
* Review date: 2026-10-29. Exactly one independent post-implementation Review; no workers launched.
* Observed branch: feat/chat-widget-550. PR 556 is caller-supplied and corroborated by the intake artifacts; no new remote lifecycle query performed.
* Assessed source boundary: working-tree git diff against HEAD 1d7710b6975892cb5d23c2d82c939cccd4748734 of src/api/README.md, src/api/src/zava_forward/api/web/chat-widget.css, src/api/src/zava_forward/api/web/chat-widget.js, src/api/src/zava_forward/api/web/chat.js, src/api/tests/test_chat_widget_focus.py and src/api/checks/chat_widget_browser_check.py.
* Necessary adjacent evidence: app.js show/route lifecycle, employee style.css stacking/focus rules, resident demo.css hover/focus tokens, existing browser assertions and repository Fluent/WCAG/plain-content baselines.
* Canonical research, plan, phase details, critique, changes and session state were compared. State correctly identifies Review as active; its null review pointer and pending P03 markers are handoff state, not implementation defects.
* External evidence root supplied by the coordinator: /home/azureuser/.copilot/session-state/ad8b0385-46d2-4a6b-b6f4-8f9df1363f23/files/widget-fixes. Read static-final.log, chat-units.log, browser-attempt5.log, browser-attempt5/results.json, browser-attempt5/employee-stacking.json, negative-units.log and negative-css-browser.log. The changes record preserves and explains attempts 1-4; this Review does not relabel those attempts as passes.
* This is local correction acceptance, not a committed exact-head publication assessment, full-site audit, full WCAG conformance decision or approval to deploy.

## Execution Status

* Execution status: Complete.
* The supplied bounded implementation, artifact reconciliation, current guideline comparison and validation evidence assessment are complete.
* Independently executed: four focus-unit methods, three JavaScript syntax checks, source/test addition-budget comparison and bounded git diff whitespace check; all passed.
* Source, original critique and historical Review outcomes remain unchanged. Only this record was written.

## Plan-to-Change Reconciliation

| Current plan scope | Changes evidence | Reconciliation | Assessment |
| --- | --- | --- | --- |
| P01-T01 | P01 Implementation and per-finding matrix | Reconciled | Four surgical corrections; semantic unit/browser coverage, no source changes beyond the accepted boundary. |
| P01-T02 | Existing shared-chat README section | Reconciled | Documents conditional following, map/account order, Close hover and retained refresh toggle. |
| P02-T01 | P02 command record and final logs | Reconciled | Requested final static, 139-unit and two-site browser checks recorded passing; adverse attempts retained. |
| P02-T02 | Negative controls, matrix, limitations and readiness | Reconciled | Original JS/CSS rejection supports regression sensitivity; no human/live or publication claim. |
| P03-T01 | One independent Review | Reconciled at this handoff | This record supplies the planned Review; parent owns subsequent marker/state update. |
| P03-T02 | Local persistence pending | Correctly pending | Local commit follows Review by design. Not a source defect or reason to mark Review execution Partial. |
| Follow-Up Items | Publication gate, hosted CI and human/live acceptance | Reconciled | Explicitly outside local-only correction; routed once as RV-001. |

## Completed Work Assessment and Four-Finding Coverage

| Requested finding | Implementation and completion evidence | Executed regression evidence | Assessment |
| --- | --- | --- | --- |
| 1. Popup/launcher above map 1000, below account 1200 | chat-widget.css:1-2 sets both shared selectors to 1100. Adjacent style.css has map summary 1000 and account panel 1200; header introduces no intervening stacking context. | employee-stacking.json has eight true above/overlap results: popup and launcher against real map, zoom controls, summary card and account menu. All measured tiers 1100. Original CSS fails map hit tests. | Conformant. Account is the top hit target in its two overlap cases; map targets remain beneath chat in six cases. Native expanded-map top layer is unchanged. |
| 2. Readable Close hover on both sites | chat-widget.css:7 explicitly uses soft background and brand text, overriding each application's generic dark button hover without replacing Fluent tokens. | Final computed contrast: employee 6.54:1; resident 7.52:1; both >=4.5:1. Original employee CSS measures 1.45:1 and is rejected. | Conformant. Bounded hover correction, not a whole-theme contrast claim. |
| 3. Follow only at pre-append bottom, outside history focus | chat-widget.js:83-86 reads bottom distance and history containment before mutation; line 101 calls bottom only when eligible. One CSS-pixel tolerance handles rounding. No new focus or smooth-scroll call. | New unit covers older reading, subpixel eligible bottom and focused log/Sources both older and at bottom. Two-site reply_scroll covers delayed older reading, older Sources, Sources at bottom, log at bottom and positive following. Original JS fails the new unit. | Conformant. Non-follow positions stay within 1px; eligible follow within 2px in browser assertions. Actual focused element identity and hit visibility are checked, not a locator that can silently select a newly appended Sources control. |
| 4. Preserve employee toggle on same-context refresh | chat.js:38-41 assigns the initial opener and decorates only inside !widget; existing widget-owned toggle/ARIA remain untouched. | New unit repeats install from both states. employee_refresh submits the real coordinator filter form from pre-refresh open and closed states; requires same widget/icon/toggle, retained draft, correct ARIA, then working launcher open and close. Original JS fails the new unit. | Conformant. app.js:92 intentionally focuses the rendered workspace, hiding the nonmodal popup; tests correctly preserve that behavior rather than require continued visibility or steal focus back. |

Existing async current/stale operation, denial, consent, keyboard traversal, external-focus dismissal, focused-control hit testing, reflow, pinned composer, loading and reduced-motion assertions remain present. The diff removes no existing assertion. AST comparison independently confirms exactly two added unit methods, four added browser helpers, no removed functions; changed-file status confirms zero new test files.

## Implementation-Time Plan and Detail Update Assessment

| Affected scope | Update and triggering evidence | Reconciliation and decision assessment |
| --- | --- | --- |
| P01/P02 completion | Final static/unit/browser and negative-control evidence replaces planned-only status. | Plan checkboxes, details, changes and handoff align. Existing critique remains Complete / Pass, with no PC findings to resolve. |
| P01-T01 / reply_scroll | Attempt 1 exposed live-locator reselection of a new Sources disclosure; attempt 2 exposed delayed loading geometry changing after positioning. | ElementHandle retains the actual original element; loading is awaited before measuring/positioning. Identity, scroll and visibility assertions are retained, not weakened. No product behavior change or user decision required. |
| P01-T01 / employee_refresh | Attempt 3 inherited the synthetic 2030 clock; attempt 4 encountered existing show() outside-focus dismissal. | Explicit fixture-compatible cutoff 2026-01-01 isolates the intended route test. Current details/plan/changes explain intentional workspace focus and require identity/draft/ARIA/toggle plus open/close afterward. No workaround or new app-wide focus policy. |
| P03 and Follow-Up Items | One Review and local persistence remain ordered after validation; publication remains separate. | No material scope, architecture or confirmed-intent divergence; fresh planning/critique is unnecessary. Pending commit and future approvals are not retroactively called complete. |

## Critique and Material Revision Assessment

* Exactly one supplied plan critique: Complete / Pass; zero PC findings, no significant/divergent user decision outstanding.
* Implementation follows the accepted 1100 tier, soft/brand hover, pre-append guard and !widget ownership direction.
* Harness corrections are supported by concrete adverse evidence and adjacent source, within the accepted test budget. They do not remove acceptance assertions, resume work across an unresolved material planning gap or revise the user's intent.
* Research alternatives remain appropriately rejected: broader map isolation, scrollIntoView and duplicated toggle ownership would expand scope without addressing a missing requirement.

## Current Web Interface Guidelines Review

Fetched successfully immediately before this Review from https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md on 2026-10-29. Both installed skills were activated. All fetched rule categories were considered against the changed web files and necessary context, not silently reduced to an accessibility-only check.

| Guideline categories | Bounded assessment |
| --- | --- |
| Accessibility; focus states | Native controls, accessible names, decorative SVG hiding, polite updates and visible focus retained. No added async focus call; actual element identity and focus-not-obscured regressions support both adapters. No claim about human screen-reader acceptance. |
| Forms; content/copy | Names, labels and autocomplete retained; no paste blocking or changed submission/error behavior. Owner's no-focus-theft boundary overrides generic async error autofocus advice. Plain ASCII and repository sentence-style/plain content override generic curly quotes, ellipsis and Title Case advice. |
| Animation | No animation change or smooth scrolling. Existing transform-only spinner and reduced-motion suppression remain; final browser evidence checks both motion settings. |
| Typography; content handling | No new rendered copy or type system. Existing wrapping, bounded input, flexible/scrolling containers and empty-source fallback remain. No unrelated typography rewrite. |
| Images; performance | No new images/assets, font/CDN dependencies or large-list mapping. Existing decorative SVG dimensions and content-visibility strategy remain. Pre-append scroll geometry reads are grouped before DOM writes for the explicitly required imperative scroll decision, not a rendering-loop measurement. |
| Navigation/state; touch/interaction | Same-context query route tested through actual form/URL behavior. Ephemeral chat state is not promoted into a navigation/deep-link redesign. Native keyboard/tap controls, manipulation touch behavior and contained scrolling remain. |
| Safe areas/layout; hover/interactive states | Existing viewport/safe-area bounds preserved; 1100 tier and scoped readable hover verified. Existing reflow and short-window focus checks retained. |
| Dark mode/theming; locale/i18n; hydration | No new theme, native-select, date/number formatting, server hydration or language-detection behavior. Shared semantic tokens and existing explicit select colors retained. |
| Anti-patterns | No new zoom restriction, paste blocking, transition:all, outline removal, nonsemantic clickable control, unlabeled control, autofocus, gesture-only action or unsupported media behavior in the bounded diff. |

Per-file guideline output (pass is limited to this correction boundary and applicable rules):

### src/api/src/zava_forward/api/web/chat-widget.css

pass

### src/api/src/zava_forward/api/web/chat-widget.js

pass

### src/api/src/zava_forward/api/web/chat.js

pass

### src/api/README.md

pass (related behavior documentation; no runtime guideline change)

### src/api/tests/test_chat_widget_focus.py

pass (test-only change; semantic focus/scroll/toggle assertions)

### src/api/checks/chat_widget_browser_check.py

pass (test-only change; actual DOM, computed contrast and overlap assertions)

No actionable changed-code guideline finding requires a file:line defect entry. Existing unrelated regulatory-panel behavior in chat.js is not reclassified or expanded into this four-correction task.

## Plan Follow-Up Assessment

| Follow-up | Why outside immediate scope | Owner / next action | Assessment |
| --- | --- | --- | --- |
| Publication exact-head gate, hosted CI, human/live acceptance | Caller expressly authorizes local-only correction and no push, Azure action or rubric write. Local browser/axe evidence does not establish these approvals. | Coordinator: retain original evidence, commit locally after Review, then perform required current-base publication gates and obtain applicable hosted/human/live approvals before any future publication. | Open, non-blocking for this local verdict; RV-001, distinct follow-up, not a new active implementation task. |

## Findings

Complete finding set: Critical 0, High 0, Medium 0, Low 1 (non-blocking residual obligation only). Implementation defects, unaccepted decisions and material evidence gaps: none found within the assessed boundary.

<!-- rpi:review id=RV-001 -->
### RV-001 [Low]: Future publication and acceptance remain separately gated

* Class: non-blocking residual work, not a source defect.
* Related scope: plan Follow-Up Items; changes P03 Review and Persistence.
* Evidence: final results.json explicitly says live_model and human_assistive_technology not run; plan/details/changes exclude complete publication gate and hosted acceptance from this local-only correction. No fresh hosted or human/live approval evidence was supplied or generated.
* Impact: local passing regressions cannot authorize publication, claim full Fluent adoption/WCAG conformance or replace required human/live/hosted approvals.
* Destination: distinct coordinator-owned publication and acceptance follow-up; no rpi-implement, rpi-plan or rpi-research correction is required by this Review.
* Smallest useful next action: finish P03-T02 local persistence, preserving this original verdict; before any later publication, run and verify the complete required exact-head/current-base local gate and obtain applicable hosted/human/live approvals. No push is authorized now.

## Defects

None found in the six-file local correction boundary. No fix is requested.

## Routed Findings

| Finding | Destination | Owner / next action | Reason |
| --- | --- | --- | --- |
| RV-001 | Distinct publication/acceptance follow-up | Coordinator; retain unclaimed gates and approvals before later publication | Explicitly excluded residual work, not an implementation, planning or research defect. |

Later implementation of any routed finding does not require this Review to run again.

## Residual Work, Blockers and Remaining Work

* Review blockers: none.
* Remaining active work: parent records this Review outcome in its own artifacts and completes P03-T02 local commit. The commit necessarily follows this Review; no premature completion claim is made.
* Residual work: RV-001 only. Hosted CI, human assistive-technology, live-model validation, other browser engines and the complete local publication gate were not executed by this reviewer. No full API discovery or release approval is implied.
* Historical critique and Review outcomes are preserved, not replaced by this bounded verdict.

## Validation Evidence

| Check | Provenance / status | Evidence and limit |
| --- | --- | --- |
| API Ruff check/format, isolated browser-helper Ruff check/format, configured mypy | Coordinator-supplied final log: Passed; not rerun here | static-final.log: checks pass, 59 project files and one helper formatted, 112 mypy source files. |
| Named chat-focused unit groups with ZF_BROWSER_TESTS=1 | Coordinator-supplied log: Passed; not rerun as a suite here | chat-units.log: 139 tests in 61.769s, OK, no skips. Expected missing-law-store/fallback fixture diagnostics are not hidden failures. |
| Two-site browser checker | Coordinator-supplied attempt 5: Passed; not rerun here | browser-attempt5.log and results.json: Chromium 156.0.8078.4, owned synthetic loopback apps; employee/resident four-finding evidence, existing focus/denial/stale/consent/loading/axe/reflow checks retained. Eight stacking records all true. |
| Original-JS negative controls | Coordinator-supplied: expected failures, successful sensitivity check | Both new methods reject HEAD JS: older-history jump and replaced widget toggle. These failures are not candidate failures. |
| Original-CSS negative controls | Coordinator-supplied: expected failures, successful sensitivity check | Hover 1.45:1 and map hit-test failures reject original CSS. Candidate hover is 6.54:1 / 7.52:1. |
| Browser attempts 1-4 | Coordinator changes record: adverse attempts retained | Locator identity, loading geometry, fixture clock and intended show() dismissal issues explained and reconciled; not counted as complete passes. |
| Focus unit module | Independently executed: Passed | From src/api: PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src:tests:../core/src:../agents/src:../core/tests:../agents/tests /tmp/mv/bin/python -B -m unittest test_chat_widget_focus -v. Four methods, 0.211s, OK, no skips. Executing the supplied interpreter did not write files under /tmp. |
| JS syntax | Independently executed: Passed | From src/api: node --check src/zava_forward/api/web/chat-widget.js; node --check src/zava_forward/api/web/chat.js; node --check src/zava_forward/api/resident_demo/web/assistant.js. All exit 0. |
| Test budget / diff hygiene | Independently inspected/executed: Passed | AST old/new function sets: two unit methods, four browser helpers, none removed. Complete bounded diff has no removed assertions or new test files; git diff --check over all six files exits 0. |
| Publication / hosted / human / live gates | Not run, intentionally outside this local correction | Required later coordinator prerequisite, not waived or claimed; RV-001. |

## Outcome

* Outcome: Conformant.
* Rationale: all four requested corrections match confirmed intent and have positive semantic regressions plus original-code negative controls. Adjacent route/CSS evidence supports the chosen stacking and retained focus behavior. No implementation defect, material evidence gap or unaccepted divergence is found.
* Review execution is Complete; future local commit and publication/approval obligations remain pending separately. Conformant means only this assessed local correction, not whole-product acceptance.

## Closeout Routing Record

| Finding class | Destination | Owner / next action |
| --- | --- | --- |
| Implementation defect | None | No rpi-implement handoff. |
| Decision gap or invalid assumption | None | No rpi-plan handoff. |
| Material evidence gap | None | No rpi-research handoff. |
| Non-blocking residual work | RV-001 distinct publication/acceptance follow-up | Coordinator, before later publication. |

* Execution status: Complete.
* Outcome: Conformant.
* Substantive source findings: none. One Low residual obligation, not a correction request.
* Validation coverage: independently passed four focus methods, three syntax checks and diff/budget checks; broader supplied final static, 139-unit and two-site browser evidence assessed without claiming an independent rerun.
* Blockers: none for this Review/local correction. Future publication remains gated.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/research/2026-10-29/chat-widget-550-copilot-fixes-research.md](.copilot-tracking/research/2026-10-29/chat-widget-550-copilot-fixes-research.md) | Cause, alternatives and accepted direction |
| [.copilot-tracking/plans/2026-10-29/chat-widget-550-copilot-fixes-plan.md](.copilot-tracking/plans/2026-10-29/chat-widget-550-copilot-fixes-plan.md) | Current scope, markers and follow-up |
| [.copilot-tracking/details/2026-10-29/chat-widget-550-copilot-fixes-phase-details.md](.copilot-tracking/details/2026-10-29/chat-widget-550-copilot-fixes-phase-details.md) | Reconciled implementation details |
| [.copilot-tracking/reviews/plans/2026-10-29/chat-widget-550-copilot-fixes-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-29/chat-widget-550-copilot-fixes-plan-critique.md) | Preserved original Complete / Pass |
| [.copilot-tracking/changes/2026-10-29/chat-widget-550-copilot-fixes-changes.md](.copilot-tracking/changes/2026-10-29/chat-widget-550-copilot-fixes-changes.md) | Implementation, adverse attempts and validation provenance |
| [.copilot-tracking/rpi-sessions/2026-10-29/chat-widget-550-copilot-fixes-state.json](.copilot-tracking/rpi-sessions/2026-10-29/chat-widget-550-copilot-fixes-state.json) | Parent-owned Review handoff state |
| [.copilot-tracking/reviews/logs/2026-10-29/chat-widget-550-copilot-fixes-review.md](.copilot-tracking/reviews/logs/2026-10-29/chat-widget-550-copilot-fixes-review.md) | This single independent Review |

## Next Steps

Return Complete / Conformant to the active parent. Parent records the outcome and completes the already-planned P03-T02 local commit; no user action or new RPI correction command is required. Retain RV-001 for future publication/acceptance work. Do not push, invoke Azure, write rubric state or repeat this Review.

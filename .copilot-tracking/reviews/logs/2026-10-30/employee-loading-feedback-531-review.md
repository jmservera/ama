---
title: Employee loading feedback 531 original RPI Review
description: Independent post-implementation assessment of the bounded static-shell regression and documentation correction
ms.date: 2026-10-30
---

## Scope and Evidence

* Task ID: 531 / employee-loading-feedback-531.
* Base: 5634f9a077d175a931c15e3400114665d8c071ee.
* Branch: feat/employee-loading-feedback-531.
* Review scope: the one original post-implementation Review of the current task.
* Assessed boundary: complete current diff, limited outside dated RPI evidence to src/api/README.md and src/api/checks/loading_briefing_browser_check.py; inherited #538 behavior is acceptance context, not a production rewrite.
* Canonical artifacts: .copilot-tracking/plans/2026-10-30/employee-loading-feedback-531-plan.md; .copilot-tracking/details/2026-10-30/employee-loading-feedback-531-phase-details.md; .copilot-tracking/reviews/plans/2026-10-30/employee-loading-feedback-531-plan-critique.md; .copilot-tracking/changes/2026-10-30/employee-loading-feedback-531-changes.md; .copilot-tracking/research/2026-10-30/employee-loading-feedback-531-research.md.

## Opening Review State

* Interpreted review goal: independently compare the bounded implementation, issue AC1-7, owner direction, current plan and critique dispositions without implying whole-issue or live acceptance.
* Review scope: static JavaScript-disabled employee-shell browser coverage and README shared-lock correction, with inherited native Fluent/HAX and draft-only authority context.
* Evidence readiness: canonical artifact set located; branch and complete diff inventory inspected; substantive comparison pending.
* Acceptance basis: current research, plan, phase details, original critique and changes, supplied validation attribution and issue requirements.
* First comparison boundary: reconcile current plan markers and changes with the complete base-to-working-tree diff, then assess validation and residual acceptance separately.
* Active read-only boundaries: create or update only this review record; no source, plan, research, critique or changes edits, commits, push, cloud activity, secrets, nested agent or second Review.
* Initial blockers: none identified for bounded assessment. Full exact-HEAD gate is subsequent publication work, not an already passed check. Live employee verification is prohibited and remains outside this execution.

## Execution Status

* Execution status: Complete.
* Implementation execution: P01, P01-T01 and P01-T02 are complete at the bounded local implementation boundary.
* Review execution evidence: independently read all five canonical current research/planning/changes artifacts, the preserved original critique, workflow state and the complete tracked base-to-working-tree diff on 2026-10-30. Inspected the named browser runner, inherited shell, relevant native review/briefing rendering, helper timing test, README HAX mapping, design-system inventory and historical participation disclosure.
* Independently retrieved issue #531, including the owner extension and merge comment, and PR #538/#529 merge metadata using read-only gh commands. Verified both merge commits are ancestors of the supplied base. HEAD remains 5634f9a077d175a931c15e3400114665d8c071ee on the requested topic branch.
* No heavy gate was repeated. No source or other RPI artifact was modified, no additional agent or Review invoked, and no commit, push, live sign-in, cloud operation or secret access performed.

## Plan-to-Change Reconciliation

| Current plan scope | Descriptive changes-record summary | Current-state reconciliation | Gap or rationale |
| --- | --- | --- | --- |
| P01 / P01-T01 | Static shell evidence | Reconciled | Exactly one new static_shell_check scenario, invoked once before existing scenarios; two viewport iterations. README changes only the lock policy and explains the distinct evidence boundary. No runtime source change or test removal. |
| P01-T02 | Required API checks: fresh pass; Browser and axe result | Reconciled with attribution | Current plan/detail completion markers agree with the final reported API, lint, format, typing and browser results. Results are parent-reported, not independently rerun or read from external logs in this Review. |
| P01-T01 / P01-T02 | First-attempt evidence and local adjustment | Reconciled | Earlier lock waits and the failed noscript locator assertion remain recorded. Later headed result sections supersede the intermediate queued/pending descriptions; final handoff and completion sections are unambiguous. |
| Critique Disposition | PC-001 rejected; PC-002 applied | Reconciled | Confirmed caller lock/tool direction is distinguished from worker-local restrictions. Exact timing belongs to the Node-backed unit test. Original Complete / Revise critique remains intact. |
| Follow-Up Items | Remaining Work and Limits | Reconciled | Live verification, assistive-technology/usability and full Fluent acceptance stay outside P01 completion and issue closure. |
| Handoff | Review then commit then complete exact-head gate | Reconciled | This Review precedes commit/gate execution. No current receipt or full-gate pass is claimed. Workflow state remains active Review for parent continuation; updating it is outside this reviewer's write authority. |

## Completed Work Assessment

| Related marker | Files | What changed and why | Completion evidence | Validation | Assessment |
| --- | --- | --- | --- | --- | --- |
| P01-T01 | src/api/checks/loading_briefing_browser_check.py | Add static_shell_check to the existing runner, not a second harness or runtime implementation. | Complete diff adds 32 lines: one scenario and one call. Disabled page JavaScript, same-origin routing, exact startup text, role=status, aria-live=polite, empty app, initially hidden retry, shell-before-script DOM ordering, 320/1280 viewport checks, no document overflow, screenshots, no script requests and finally-based context cleanup. | Syntax and diff hygiene independently passed; successful browser execution is parent-reported. | Conformant to locked target/addition ceiling. Automation-side DOM evaluation does not enable page-authored scripts. Existing index.html contains scripts after the shell, so the ordering assertion has a real supplied markup boundary. |
| P01-T01 | src/api/README.md | Replace nonblocking/concurrent fallback advice with wait-600 serialization and explain the new no-script coverage. | Complete diff adds six lines and removes two. Lock timeout blocks the check; no unlocked heavy fallback is suggested. Static, held-script and script-enabled axe scenarios are distinguished. | Independent diff/content review. | Conformant; no unrelated guide edits or new acceptance claims. |
| P01-T02 | Existing API tests and browser scenarios; no additional source changes | Freshly exercise inherited behavior rather than duplicate merged #538. | Canonical changes record reports full API discovery, Ruff check/format, mypy and real constructed-loopback browser execution under the shared lock. Runner inspection confirms synthetic fixture, sanitized server environment, health readiness and owned-process termination. | Parent-reported local passes; inherited assertions independently inspected. | Adequate bounded evidence, with limitations below. No new runtime defect requiring implementation was identified. |

## Acceptance and Owner-Comment Assessment

Issue checkboxes and the merge comment are historical dispositions, not fresh execution proof. The following judgements combine independent source/diff inspection with explicitly attributed parent execution reports.

| Criterion | Evidence and assessment | Acceptance boundary |
| --- | --- | --- |
| AC1: static/panel loading, live/slow/retry | New disabled-script scenario verifies static status semantics/order and geometry. Existing shell_check holds app.js, checks immediate/4s/15s messages and retry; inherited service/helper/companion/action checks exercise bounded recovery and explicit terminal failures. | Supported locally; no claim that HTML appears before the host returns it, or that a static live region has been heard by a human screen-reader user. |
| AC2: simulated cold start without blank page | Held-script scenario checks visible startup text with an empty app; the added fully disabled-page-script context is distinct and verifies 320/1280 layout. Parent reports both pass. | Browser simulation after HTML arrival, not infrastructure scale-from-zero or deployed employee-site verification. |
| AC3: AI/rules/source distinction and HAX design note | src/api/README.md records G1/G2 labels/limits, G7 mode, G8 reversible local hide, G9 correction, G11 rationale/time/references and G15 feedback. app.js aiBox/aiNotes and browser assertions support the mapping. Native Fluent-derived patterns are retained. | Engineering/design-intent support, not specialist-authored approval, staff usability or full Fluent implementation adoption. |
| AC4: clear outcome wording and unchanged boundaries | Native choices are Use this draft, Edit this draft and Do not use this draft. Conditional editor/reason, required reason for edit/reject, cancel/focus, real review payload and pending/uncertain-history barriers are inspected in inherited source/tests. | Draft feedback only. No works approval, resident consent, safety decision, case change or resident contact is granted by recording a review. The issue's example Approve wording is not an instruction to misstate authority. |
| AC5: sources, time and unverified output | aiBox renders actual generated_at, per-statement references and declared case links; aiNotes labels unverified sources. Browser assertions cover source/time/type labels, unmatched references and disabled use/edit for stale/unverified material. | References and explanations are not proof of truth; inherited API regression execution is parent-reported. |
| AC6: automated browser/axe, no AT claim | Parent reports successful Chromium run and pinned axe 4.10.3, zero violations in briefing-320, briefing-390, briefing-1280 and ai-unverified-sources. Runner verifies pinned SHA256 and retains reports. | Only those four script-enabled scopes; no axe injection into the no-script scenario and no whole-app WCAG, screen-reader or voice-control acceptance. |
| AC7: separate live employee check | Issue remains open; owner merge comment expressly requires a live employee-site check after redeploy. No live check was authorized or attempted here. | Unmet. Distinct owner/coordinator follow-up; only Refs #531 is supported, not whole-issue completion. |
| Owner extension: immediate async feedback and icon after 200ms | src/api/tests/test_loading_feedback.py::test_actual_helper_timing_duplicates_errors_and_state_ownership executes the actual helper in Node with a controlled clock, immediate text/polite status/disabled and duplicate state, no icon at 199ms and icon at 200ms. Browser runner separately checks real pending controls/spinners, non-blocking editable search, duplicate prevention, errors and reduced motion. | Exact 199/200ms is unit-test evidence, not a browser timing measurement. Fresh execution is parent-reported. No universal live timing claim. |
| Owner extension: mode clarity and conditional larger fields | Existing labelled mode selector says Use rules and templates, without AI and explains scope/manual continuity. Review choices expose the large editor only for editing and reason for edit/rejection. | Source and browser assertions support unchanged delivered behavior; no new rewrite needed. |
| Owner extension: Fluent reference and UX participation | README cites Fluent UI React Storybook as a pattern reference; design-system inventory explicitly distinguishes native tokens from full runtime adoption. Current and historical research disclose that the UX agent returned intake questions, not a design artifact. | The agent was invoked, but the inherited note remains parent-written. No specialist contribution, approval, interview or human validation is inferred. |

## Implementation-Time Plan and Detail Update Assessment

| Affected area or marker | What changed and why | Triggering evidence and user decision | Reconciliation performed | Planning and critique state | Assessment |
| --- | --- | --- | --- | --- | --- |
| P01-T01 | Remove an unsupported noscript locator-text assertion after the first browser failure; retain actual static startup checks and screenshots. | Parent records empty locator text and later visible screenshot help text. No parser inference or production defect is asserted. | Current diff, plan, phase details and changes describe static startup semantics/order/geometry, not a promised noscript text assertion. | Local test correction within the one-scenario ceiling; original failure preserved. | Justified, non-material implementation adjustment; no new user decision or plan/critique cycle required. Screenshots were not independently viewed by this reviewer. |
| P01-T02 / Non-Functional Requirements | Correct exact-timing attribution. | PC-002 and actual-helper test inspection. | Plan, details and changes consistently attribute 199/200ms to the Node-backed unit test; browser owns real-control/reduced-motion/axe coverage. | Original critique preserved; direct correction applied. | Resolved. |
| Execution preconditions / Critique Disposition | Preserve caller-required shared lock/tool/output direction rather than impose the critique worker's local path restriction on the parent. | Explicit caller direction and current plan disposition. | Plan/details distinguish parent execution authority from worker-local restrictions; parent reports successful serialized runs after lock waits. | Original PC-001 High / Revise text retained and explicitly rejected with rationale. | Supported disposition, not an unresolved parent decision gap. This reviewer does not access the prohibited external paths. |
| P01 completion and Handoff | Reconcile final successful local validation after earlier failed/waiting attempts. | Parent reports third API acquisition/run and second browser pass. | Final markers, completion evidence and handoff agree; intermediate adverse evidence remains chronological. | Ready for this one original Review; commit and exact-head gate follow. | Consistent; no material scope expansion or premature publication acceptance. |

## Critique and Material Revision Assessment

* Latest critique is the supplied original Complete / Revise record, not a newly substituted approval.
* PC-001: rejected by parent with confirmed caller-direction rationale. A worker-local temporary-path prohibition is not promoted into a parent instruction. This Review neither reopens the resolved direction nor performs prohibited external file operations.
* PC-002: applied; independently inspected test confirms precise evidence ownership.
* Reusing merged #538 and merged dependency #529 is supported by issue comments, PR metadata and verified ancestry, not an assumption that closed work must be reimplemented.
* No significant divergent decision or expanded implementation was found after critique. The failed locator assertion correction did not remove the required static startup signal or expand scope.
* Dependent-work pause assessment: current artifacts record disposition before proceeding; inspected changes preserve the accepted narrow boundary. No unresolved decision requiring a new planning pause was identified.
* The unavailable UX-authored note is disclosed consistently in current research, plan, historical research and acceptance reporting. Retaining the existing evidence-backed parent note does not create specialist acceptance.

## Plan Follow-Up Assessment

| Follow-up item | Why outside immediate scope | Owner or next action | Assessment and route |
| --- | --- | --- | --- |
| Live employee-site verification, AC7 | Deployment/live sign-in are prohibited here; synthetic loopback does not establish deployed cold start. | Owner/coordinator: obtain separate authorization, then record live employee verification after redeploy. | Open, distinct live follow-up; not a defect or active P01 task, and not whole-issue completion. |
| Screen-reader, voice-control and staff usability acceptance | Automated DOM/browser/axe evidence is not human acceptance. | Owner/coordinator: arrange separately authorized direct AT and staff checks. | Open acceptance follow-up, not manufactured local conformance. |
| Full Fluent adoption / UX specialist contribution | Existing native token patterns and parent-written HAX mapping do not establish actual Fluent runtime adoption or specialist validation. | Owner/design-system workstream: retain the existing adoption decision boundary and seek specialist/human acceptance only in separately scoped work. | No framework change or repeated UX delegation is authorized by this task. |

Unresolved follow-ups remain outside active P01/P01-T01/P01-T02 completion and acceptance claims.

## Findings

No substantive implementation defect, unaccepted decision gap or material research gap was identified within the assessed boundary. No RV-xxx finding is raised. Severity summary: 0 Critical, 0 High, 0 Medium, 0 Low.

Unavailable reviewer access to the supplied external logs is an evidence-attribution limitation, not a claim that the parent did not run validation. Expected later publication steps and prohibited live acceptance are routed below without inventing defects.

## Defects

* None identified within the bounded two-file implementation.

## Routed Findings

| Finding | Destination | Owner or next action | Reason for route |
| --- | --- | --- | --- |
| None | No rpi-implement, rpi-plan or rpi-research handoff | Parent continues the already planned post-Review sequence. | No actionable defect, decision gap or material research gap in assessed scope. |

Later implementation, if separately authorized, does not require this original Review to run again.

## Residual Work

* Live acceptance: AC7 remains unmet and #531 remains open; separately authorized owner/coordinator live verification only.
* Human/design acceptance: retain explicit AT, voice-control, staff usability, specialist-contribution and full Fluent-adoption limitations. Local engineering evidence cannot close them.
* Publication: parent must commit implementation and dated original RPI evidence before running the complete local gate against the reviewed base, retain the final receipt externally, and verify exact-head/current-base validity before any separately authorized publication or independent exact-head assessment. Any later candidate/base/tool/image/input change invalidates that gate. No gate pass exists yet.
* Missing SQL/browser/scanner prerequisites, if encountered by the parent, block publication without cloud fallback, skipped controls or fabricated status. No push is authorized in this task.

## Blockers and Remaining Work

* Review blockers: none for the bounded implementation assessment.
* Remaining active implementation work: none in P01.
* Whole-issue acceptance: AC7 and separate live/human acceptance are not established.
* Publication readiness: not established; complete exact-head gate is deliberately subsequent to this Review and local commit. Its present unexecuted state does not retroactively block this bounded assessment.

## Validation Evidence

External log and JSON files were not opened: this reviewer's active file-operation restriction prevents access to the supplied external temporary directory. The caller and canonical changes record provide the following reported results. No results below are presented as independently rerun heavy checks.

| Command or evidence | Scope | Status | Summary and attribution |
| --- | --- | --- | --- |
| git diff against supplied base, status and branch inspection | Complete current tracked diff and untracked RPI inventory | Passed | Independently inspected. Exactly src/api/README.md and src/api/checks/loading_briefing_browser_check.py changed outside RPI evidence. Existing dirty inputs were left intact. |
| git diff --check against supplied base | Tracked candidate | Passed | Independently executed; no whitespace errors. |
| Python ast.parse of changed runner | src/api/checks/loading_briefing_browser_check.py | Passed | Independently executed without imports, dependency installation or bytecode generation. Not a substitute for browser execution. |
| gh issue/pr reads and git merge-base --is-ancestor | Issue #531, owner extension, #538/#529 inheritance | Passed | Independently retrieved; both PRs merged into main and inherited by base. Issue remains OPEN with AC7 unchecked. |
| python3 -m unittest discover -s tests -q, from src/api with recorded source/test paths | API discovery | Passed, parent-reported | Ran 1370 tests in 490.412 seconds; OK, skipped=318. The 318 opt-in skips are included in the run count, not additional passing tests. Supplied unittest.log not independently read. Exact helper timing belongs to test_loading_feedback, not browser measurements. |
| ruff check . | API | Passed, parent-reported | Supplied ruff-check.log; exit 0. |
| ruff format --check . | API | Passed, parent-reported | Supplied ruff-format.log; 60 files already formatted, exit 0. |
| mypy | API configured typing scope | Passed, parent-reported | Supplied mypy.log; 116 source files, exit 0. |
| checks.loading_briefing_browser_check | Real constructed loopback app and inherited/new scenarios | Passed, parent-reported | Supplied browser-2.log; Chromium 156.0.8078.4. New no-page-script scenario passes at 320/1280; inherited delayed/retry, real-action, review, provenance and reduced-motion checks pass. No heavy repetition in Review. |
| Pinned axe 4.10.3 reports | Four named script-enabled briefing scopes | Passed, parent-reported | Supplied axe-results.json reports zero violations in all four scopes. Source inspection confirms pinned SHA256 enforcement and scope selection. JSON not independently opened; not a new whole-runtime accessibility audit. |
| Earlier browser.log and lock attempts | Adverse execution history | Failed / blocked attempts, parent-reported | First browser attempt failed the removed noscript locator assertion. Two lock waits expired without API execution. Later passes do not erase these original attempts. |
| static-shell screenshots | 320/1280 evidence assets | Unavailable to reviewer | Parent reports retained screenshots and inspection of the 320px image. This Review makes no independent screenshot/readability inspection claim beyond inspected assertions and source layout. |
| Full exact-HEAD local gate | Publication candidate after commit | Not run | Required later; no receipt or publication pass claimed. |
| Live employee site, human AT/voice/usability, actual AI inference | Live/human acceptance | Not run | Outside authorization; no live deployment/sign-in, model, private dataset or cloud verification performed. |

Reported heavy execution used the caller-required shared lock with wait-600; the parent did not substitute a different lock or infer a pass from timeout. System-Python dependency limitations and reuse of existing installed tools are recorded in the changes artifact, not independently exercised here.

The parent reports a fresh web-guidelines retrieval. No runtime web file changed, and this Review does not claim a fresh full runtime web-guidelines audit, HAX source refresh, WCAG conformance or new specialist sign-off.

## Outcome

* Outcome: Conformant with justified divergence.
* Outcome rationale: the bounded static-shell regression and README correction match the current reconciled plan and preserve inherited behavior. Reuse of merged #538 instead of duplicate production work is evidence-backed; outcome-based draft wording correctly avoids implied operational approval. The narrowly removed unsupported noscript assertion and disclosed unavailable specialist-authored note do not justify rewriting delivered production behavior or manufacturing acceptance.
* This outcome applies to the bounded implementation, not whole issue #531, live employee behavior, full Fluent adoption, human accessibility/usability acceptance or publication readiness. AC7 remains unmet.

## Closeout Routing Record

| Finding class | Destination | Owner or next action |
| --- | --- | --- |
| Implementation defect | None | No later rpi-implement correction identified. |
| Decision gap or invalid assumption | None | No new rpi-plan decision required. |
| Material evidence gap | None within assessed boundary | No new rpi-research cycle required; supplied execution attribution stays explicit. |
| Non-blocking residual live/human acceptance | Distinct acceptance follow-up | Owner/coordinator obtains authorization and records live/AT/usability results separately; retain design-system limitations. |
| Subsequent publication work | Existing post-Review parent sequence | Parent commits original evidence and attempts complete exact-head local gate; no push authorized. |

* Execution status: Complete.
* Outcome: Conformant with justified divergence.
* Validation coverage: independent complete diff/source/artifact/issue/ancestry review and lightweight syntax/hygiene checks; API/browser/axe execution results explicitly parent-reported.
* Severity summary: no RV findings.
* Blockers: none for this bounded Review; live acceptance and exact-head publication prerequisites remain open separately.

## Artifacts

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/research/2026-10-30/employee-loading-feedback-531-research.md](.copilot-tracking/research/2026-10-30/employee-loading-feedback-531-research.md) | Current research, inherited behavior and participation limits. |
| [.copilot-tracking/plans/2026-10-30/employee-loading-feedback-531-plan.md](.copilot-tracking/plans/2026-10-30/employee-loading-feedback-531-plan.md) | Reconciled P01 plan, critique dispositions and follow-up. |
| [.copilot-tracking/details/2026-10-30/employee-loading-feedback-531-phase-details.md](.copilot-tracking/details/2026-10-30/employee-loading-feedback-531-phase-details.md) | Current scoped implementation and validation details. |
| [.copilot-tracking/reviews/plans/2026-10-30/employee-loading-feedback-531-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-30/employee-loading-feedback-531-plan-critique.md) | Preserved original Complete / Revise critique. |
| [.copilot-tracking/changes/2026-10-30/employee-loading-feedback-531-changes.md](.copilot-tracking/changes/2026-10-30/employee-loading-feedback-531-changes.md) | Implementation history and parent-reported execution evidence. |
| [.copilot-tracking/rpi-sessions/2026-10-30/employee-loading-feedback-531-state.json](.copilot-tracking/rpi-sessions/2026-10-30/employee-loading-feedback-531-state.json) | Parent-owned active Review handoff state; unchanged. |
| [src/api/README.md](src/api/README.md) | Complete changed guide and inherited HAX/Fluent/authority mapping. |
| [src/api/checks/loading_briefing_browser_check.py](src/api/checks/loading_briefing_browser_check.py) | Complete changed browser runner and retained scenarios. |
| [src/api/checks/design_system_browser_check.py](src/api/checks/design_system_browser_check.py) | Inherited synthetic server ownership/readiness boundary. |
| [src/api/tests/test_loading_feedback.py](src/api/tests/test_loading_feedback.py) | Actual-helper Node-backed exact timing evidence owner. |
| [src/api/src/zava_forward/api/web/index.html](src/api/src/zava_forward/api/web/index.html) | Inherited static shell semantics and script ordering. |
| [src/api/src/zava_forward/api/web/app.js](src/api/src/zava_forward/api/web/app.js) | Relevant inherited aiNotes/aiBox authority and interaction context. |
| [src/api/src/zava_forward/api/web/style.css](src/api/src/zava_forward/api/web/style.css) | Relevant inherited startup and reduced-motion styling. |
| [docs/reference/research/ux/design-system.md](docs/reference/research/ux/design-system.md) | Native Fluent-derived patterns and unresolved adoption boundary. |
| [.copilot-tracking/research/2026-10-28/loading-briefing-hax-531-research.md](.copilot-tracking/research/2026-10-28/loading-briefing-hax-531-research.md) | Historical parent-written design note and UX intake-only result. |
| [.copilot-tracking/reviews/logs/2026-10-30/employee-loading-feedback-531-review.md](.copilot-tracking/reviews/logs/2026-10-30/employee-loading-feedback-531-review.md) | This one original post-implementation Review. |

## Next Steps

Return this record to the active parent for its planned local commit and subsequent complete exact-HEAD local gate. Do not invoke another Review, push, mark the issue complete or perform prohibited live verification. Owner/coordinator retains separate live and human/design acceptance follow-up.

Parent editorial normalization: issue-reference wording uses Refs #531 only.
The original independent assessment, findings, outcome and routes are unchanged.

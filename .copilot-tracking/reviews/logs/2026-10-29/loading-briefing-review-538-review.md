---
title: PR 538 correction implementation review
description: Single independent RPI Review of task 538-review-corrections-2026-10-29
ms.date: 2026-10-29
---

## Opening Review State

* Goal: assess the three requested citation, abbreviation and startup corrections once, without implementation or a second Review.
* Scope: P01-P02; committed source candidate 0e910aa1e36c616c0b433b48e392e3ba94b97d2e against baseline 204507d6, plus current canonical research, plan, details, critique, changes and rpi-sessions state.
* Evidence readiness: matching artifact set exists; current dirty changes are confined to plan, details, changes and session-state reconciliation. Source is unchanged from the candidate.
* Acceptance basis: FR1-FR5, AC1-AC6, exact supplied reproductions, PC-001/PC-002 dispositions and explicit busy-lock targeted fallback.
* First comparison boundary: candidate parser/bootstrap changes and tests against the current requirements; then evidence and marker reconciliation.
* Read-only boundaries: all source, tests, documentation and other artifacts. This record alone may be written. No subagents, installs, full/browser suites, lock retry, Azure, commits or publication.
* Initial validation limitation: full units, fresh shared editable setup and actual browser/axe runs are unperformed. This does not block bounded review, but cannot establish browser acceptance.
* Web review source: freshly retrieved https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md on 2026-10-29; apply only to changed app.js code, with repository Fluent/plain-language conventions taking precedence.

## Scope and Evidence

* Task ID: 538-review-corrections-2026-10-29.
* Review date: 2026-10-29.
* Review scope: the complete supplied P01-P02 correction boundary; exactly one independent post-implementation Review, performed directly without subagents.
* Source boundary: HEAD is exactly 0e910aa1e36c616c0b433b48e392e3ba94b97d2e; comparison baseline is 204507d6. All six changed implementation/test/documentation files were inspected, including their relevant existing parser, loader, route, startup, HTML, shell and helper context.
* Current-artifact boundary: the working copies of plan, details, changes and rpi-sessions state have only evidence/state reconciliation changes since HEAD. These acknowledge the candidate commit, complete P02-T02 and transition to Review. Research and original critique remain unchanged. This assessment covers those working copies, not a fictional clean, committed, exact-head publication receipt.
* Canonical research: .copilot-tracking/research/2026-10-29/loading-briefing-review-538-research.md.
* Canonical plan: .copilot-tracking/plans/2026-10-29/loading-briefing-review-538-plan.md.
* Canonical details: .copilot-tracking/details/2026-10-29/loading-briefing-review-538-phase-details.md.
* Original critique: .copilot-tracking/reviews/plans/2026-10-29/loading-briefing-review-538-plan-critique.md.
* Changes evidence: .copilot-tracking/changes/2026-10-29/loading-briefing-review-538-changes.md.
* Session state: .copilot-tracking/rpi-sessions/2026-10-29/loading-briefing-review-538-state.json.
* Context: original case study, addendum, reference index, owner memory, housing-association primer and src/README.md local-gate guidance. No new legal, deployed, human-accessibility or whole-project acceptance claim is made.

## Execution Status

* Review execution status: Complete.
* Implementation execution assessment: P01/P02 completion markers are consistent with the explicitly authorized targeted fallback, not with execution of the full validation lane.
* Evidence: committed diff, all current canonical artifacts, focused source context, freshly fetched web rules, independent execution of the 83 focused tests, syntax/whitespace checks and two discriminating probes.
* Validation coverage remains bounded. No full discovery, browser, axe, editable installation, heavy-lock retry/poll, Azure, remote write or commit was performed. No second Review or correction round is requested.

## Plan-to-Change Reconciliation

| Current plan scope | Changes evidence | Current-state reconciliation | Assessment |
| --- | --- | --- | --- |
| P01-T01; FR1/FR2; AC1/AC2 | Parser normalization and three parameterized test methods | Complete source/test changes; LF/CRLF, groups, titles, explicit newlines and St./etc. negatives agree with details | Positive fixtures pass; suffix citation isolation still fails, RV-001. Exact original-example identity is not preserved in the plan, RV-003. |
| P01-T02; FR3-FR5; AC3/AC4 | Helper readiness, bootstrap, Node scenarios and browser scenarios | Helper-only null selection and listener/start ordering are implemented; cached attempts and route guards retained | Node contracts pass; malformed defined-helper terminal rendering fails, RV-002. Actual browser acceptance remains unestablished, RV-004. |
| P01-T03 | API README and unchanged manifest pins | Scoped behavior documentation; no pinned scenario input changed | README reflects intended bounded behavior, not proof against the defects below. Existing needs-inventory checks pass. |
| P02-T01; AC5 | 83 focused tests, strict checks and busy admission record | User-authorized fallback explicitly recorded; full/browser/editable work deferred | Reconciled. A checked task does not mean browsers passed. |
| P02-T02; AC6 | Candidate commit plus current evidence reconciliation | HEAD contains original evidence and code; current handoff/state names that commit and Review phase | Reconciled within the supplied mixed committed/current boundary. This Review was pending at intake; state is parent-owned and was not edited here. |
| Follow-Up Items | FU-001 in plan, changes and state | Deferred heavy validation remains outside active task acceptance | Distinct follow-up, RV-004; no automatic continuation. |

## Completed Work Assessment

| Marker | Files | Completion evidence | Validation and assessment |
| --- | --- | --- | --- |
| P01-T01 | src/core/src/zava_forward/core/ai_tasks.py; src/core/tests/test_ai_statement_sources.py | Scoped citation shielding/whitespace normalization and contextual abbreviation protection; full text/citation/unresolved assertions | Supplied focused suite passes. Independent Sr./Jr. probes reveal citation bleed not covered by the negative fixtures. |
| P01-T02 | src/api/src/zava_forward/api/web/app.js; src/api/tests/test_workspace_scripts.py; src/api/checks/loading_briefing_browser_check.py | Bootstrap awaits helper readiness before listeners/start; null session excludes role files; browser recovery/terminal scenarios authored | Actual loader/bootstrap Node scenarios pass. Browser scenarios are unexecuted. Terminal renderer is not covered by those Node assertions and fails for a defined object without handler. |
| P01-T03 | src/api/README.md | Directly related recovery and conservative parser documentation | No dependency expansion, redesign, weakened approval boundary or unrelated source change observed. |
| P02 | Matching plan/details/changes/state | Candidate and original evidence persisted; adverse attempts retained; fallback and residuals explicit | Reported static passes distinguished from independently rerun checks below. No full-gate or publication result inferred. |

## Implementation-Time Plan and Detail Update Assessment

| Area | What changed and why | Trigger and decision | Reconciliation and assessment |
| --- | --- | --- | --- |
| FR2/P01-T01 | Bounded contextual abbreviation rules and named supported forms | PC-001; direct correction within confirmed intent, no new user decision required | Plan/details/tests agree for St. and etc.; treating Sr./Jr. as unconditional titles still violates the higher-level no-bleed requirement, RV-001. |
| FR3-FR5/P01-T02 | Helper-only pre-session selection, unchanged-null readiness check and terminal reload | PC-002; direct correction within confirmed intent | Plan/details/source agree on selection and ordering. Terminal UI has an additional unhandled readiness case, RV-002. |
| P02-T01/FU-001 | Full lane replaced by explicitly authorized targeted fallback for this execution | Recorded nonblocking admission exit 75; owner PID 661156 | Rationale is supported by supplied execution evidence. Full/browser/editable work is consistently unperformed, not silently waived or claimed passed. No lock retry performed by Review. |
| P02-T02/handoff/state | Record commit identity, complete persistence and transition Implement to Review | Candidate 0e910aa1 exists locally | Current dirty edits reconcile the source commit without changing source. No significant divergent scope decision or early dependent-work resumption observed. |

## Critique and Material Revision Assessment

* Preserve original critique outcome: Complete execution, Revise verdict, PC-001 High and PC-002 Medium. This Review does not replace or rewrite it.
* PC-001 disposition was applied: explicit St. context, medial/terminal etc. and exact text/citation/unresolved assertions are present. Its broader citation-isolation concern is not fully solved because newly supported Sr./Jr. terminal suffixes merge independent claims. This is new implementation evidence, not a second plan critique.
* PC-002 disposition was applied: missingWorkspaceScripts excludes all role-specific dependencies while me is null, including screens. requireWorkspaceScripts captures session identity and rechecks unchanged-null readiness. bootstrapWorkspace awaits it before account handlers and start. Authenticated route performs its existing abort/session checks after the await. Node coverage retains those contracts.
* Retry policy remains two cached injections after the initial HTML download; only explicit network errors permit the second injection. Timeout or load without readiness does not restart the budget. The browser test source distinguishes three total failed requests from two requests when the injected script loads without the global.
* Readiness and selection clarification did not require a divergent user choice. No further critique was run. The original critique already noted that complete original reproductions were absent from the artifacts; current plan still does not make them explicit, RV-003.
* No material implementation expansion beyond the accepted correction direction was observed. Three parser methods, one Node scenario block and one parameterized browser function stay within the declared change budget.

## Plan Follow-Up Assessment

| Item | Why outside immediate scope | Owner or next action | Assessment and route |
| --- | --- | --- | --- |
| FU-001 | User permits targeted fallback when heavy admission is busy | Parent coordinates a later explicit free-lock validation event | Open; RV-004 routes to this distinct future validation work, not new active P02 work. |
| Human accessibility, deployed cold start, hosted/publication gates | Outside this local correction; targeted units do not establish them | Respective human/deployment/release owners when those gates are separately authorized | Remain outside acceptance and are not converted into implementation defects. |

## Findings

<!-- rpi:review id=RV-001 -->
### RV-001 [High]: Newly protected terminal name suffixes transfer citations to an uncited sentence

* Related scope: P01-T01, G1/G2, FR2, AC2 and the intent of PC-001.
* Evidence: src/core/src/zava_forward/core/ai_tasks.py:158-170 protects every supported abbreviation except the contextual St./approx./etc. cases. Sr. and Jr. are also ordinary name suffixes that can end a sentence. src/core/tests/test_ai_statement_sources.py:48-78 tests them only as prefixes in "Contact Jr. Jones ..." and "Contact Sr. Jones ..."; terminal negatives cover only St. and etc.
* Independently executed input: `Contact John Smith Jr. Repairs are due. [[Second source]]`, sources `{"ZF-1": ["Second source"]}`.
* Actual output: one statement, text `Contact John Smith Jr. Repairs are due.`, citations `["Second source"]`, unresolved `[]`. The same failure occurs with Sr.
* Required isolation: first statement `Contact John Smith Jr.` with citations `[]`; second statement `Repairs are due.` with citations `["Second source"]`; both unresolved `[]`.
* Impact: a separately uncited claim is displayed as owning another claim's declared evidence. This is newly introduced by abbreviation shielding and contradicts the correction's central citation-isolation acceptance, despite the passing focused tests.
* Destination: later rpi-implement, within the accepted no-invented-evidence direction.
* Smallest useful next action: distinguish or conservatively retain terminal suffix boundaries; add same-token positive/negative Sr./Jr. fixtures with full outputs, preserving legitimate title and newline behavior. Reconcile the bounded rule description during that future implementation, without rewriting this Review.

<!-- rpi:review id=RV-002 -->
### RV-002 [Medium]: The terminal reload renderer still depends on the helper whose readiness failed

* Related scope: P01-T02, FR3/FR5, AC4.
* Changed-code location: src/api/src/zava_forward/api/web/app.js:1542 - terminal reload construction calls h(), whose event wrapper invokes an unready AsyncAction.handler.
* Evidence: app.js:226 intentionally classifies a defined AsyncAction object without a callable handler as missing readiness. app.js:19-21 checks only whether AsyncAction is defined when wrapping onclick. Consequently startupFailed's new reload button is not independent of that failed readiness contract.
* Independent lightweight probe executed the shipped h() and startupFailed() in Node VM with `AsyncAction = {}` and an error carrying `reloadWorkspace: true`. Actual result: `TypeError: AsyncAction.handler is not a function`; zero rendered nodes and zero workspace-ready events. The status text is assigned, but show() never runs, so the announced alert and native reload button are absent. An independent shell watchdog remains available; this is not a claim that every possible recovery disappears.
* Impact: an evaluated but incompatible/incomplete helper cannot reach the promised terminal recovery UI. The ordinary wholly absent-helper case remains safe because h() falls back to the native handler; this defect concerns a defined object failing the newly explicit handler readiness check.
* Regression gap: the Node harness stubs h() and tests rejection, not startupFailed rendering. Browser missing-global mode returns a comment, not a defined helper without handler, and is unexecuted.
* Destination: later rpi-implement.
* Smallest useful next action: make terminal recovery independent of an unready helper and cover actual terminal rendering with an incomplete defined helper as well as an absent helper. Retain the bounded loader and native keyboard action.

<!-- rpi:review id=RV-003 -->
### RV-003 [Low]: The plan still does not persist all three exact supplied reproductions

* Related scope: user requirement for all three exact examples and acceptance in the plan; AC1-AC4; original critique's stated evidence limitation.
* Evidence: .copilot-tracking/plans/2026-10-29/loading-briefing-review-538-plan.md:74 refers to "both exact parser examples" without their strings, source maps or expected complete outputs. FR1/FR2 describe categories; AC3 describes helper abort behavior without an exact reproduction procedure tied to the third finding. Details include critique discriminators but likewise do not identify the complete original supplied pair. Research says they were reproduced exactly without recording the inputs.
* Impact: tests contain useful concrete LF/title cases, but this canonical artifact set cannot establish that they are the unchanged original reproductions rather than analogous fixtures. Implementation claims of exactness exceed the persisted traceability. This finding does not assert that the original supplied strings were different.
* Destination: later rpi-plan documentation reconciliation, not another critique or Review.
* Smallest useful next action: parent preserves the three original examples verbatim with expected outputs/startup observations and maps them to AC1-AC4 and specific fixtures. Do not invent missing originals or rewrite original outcomes.

<!-- rpi:review id=RV-004 -->
### RV-004 [Medium]: Actual-browser recovery acceptance remains unestablished

* Related scope: AC3/AC4, P02-T01 and existing FU-001.
* Evidence: changes, details and state consistently record busy admission exit 75 and unperformed loading/briefing Chromium/axe, workspace-script browser runs, full core/API discovery and fresh shared editable setup. Review independently reran only the permitted focused lane; no lock was retried or polled.
* Impact: passing Node stand-ins and syntax/type checks do not prove shipped lexical-helper injection, complete document startup, keyboard-native terminal recovery, page-error absence or axe results. Browser scenarios are authored, not observed passes. This is an explicit validation limitation, not an unauthorized fallback or evidence of browser failure.
* Destination: distinct follow-up FU-001, owned by parent-coordinated later validation. Non-blocking to execution of this user-authorized bounded round; not a conformant browser outcome.
* Smallest useful next action: at a separately coordinated free-lock event, perform the already specified editable/full/browser checks and retain actual results. No retry, verification/closure cycle or additional Review is authorized this round.

## Scoped Web Interface Guidelines Assessment

### src/api/src/zava_forward/api/web/app.js

src/api/src/zava_forward/api/web/app.js:1542 - RV-002 [Medium]: terminal reload UI construction invokes the helper that failed readiness; error recovery must retain a native usable action.

* Changed code otherwise retains semantic buttons, native click/keyboard behavior, an alert and the existing polite live status, explicit recovery labels, no new motion, and existing focus handling. Rules concerning new forms, images, media, virtualized lists, dates and layout are not newly implicated by this diff.
* No unrelated UI audit or redesign was performed. Fresh guideline retrieval succeeded in full; source review does not establish accessibility conformance or replace missing browser/axe and human evidence.

## Defects

* RV-001: newly introduced abbreviation/citation isolation defect; later rpi-implement.
* RV-002: terminal rendering defect in the newly added readiness failure path; later rpi-implement.

## Routed Findings

| Finding | Destination | Owner or next action | Reason |
| --- | --- | --- | --- |
| RV-001 High | Later rpi-implement | Future correction owner: suffix segmentation and discriminating fixtures | Behavior violates accepted citation-isolation direction. |
| RV-002 Medium | Later rpi-implement | Future correction owner: helper-independent terminal rendering and coverage | Recovery contract fails for a defined unready helper. |
| RV-003 Low | Later rpi-plan | Parent: preserve exact original examples and acceptance mapping | Explicit planning traceability requirement remains unmet; no divergent product decision needed. |
| RV-004 Medium | Distinct FU-001 | Parent: separately coordinate full/editable/browser validation | Explicit residual validation, not an implementation defect or a reason to run unapproved heavy work now. |

No material external research gap requires rpi-research. Later work must preserve this original finding set; it does not require another Review. No destination is invoked here.

## Residual Work

* FU-001 remains open with the scope above. Do not promote its deferred checks to passed, hide the browser limitation behind task markers or add it back into active scope in this round.
* Human accessibility, deployment cold-start and hosted/publication gates remain separately owned and outside this local correction.

## Blockers and Remaining Work

* Review blocker: none; a credible verdict is supported by direct evidence.
* Validation blocker: recorded heavy-lock contention prevented full/editable/browser execution. Owner PID 661156 is the implementation-time observation, not a fresh lock-status claim.
* Remaining work in this round: parent records the original Review outcome and future routes, then stops as instructed. No source fixes, lock retry, closure testing, second Review, push or cloud work.
* Future implementation acceptance is prevented by RV-001/RV-002. Local focused validation does not authorize publication; the repository's complete exact-head publication gate and human/hosted approvals were not executed.

## Validation Evidence

| Command or boundary | Status | Evidence |
| --- | --- | --- |
| `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src/api/src:src/core/src:src/agents/src:src/api/tests:src/core/tests:src/agents/tests /tmp/mv/bin/python -m unittest test_ai_statement_sources test_workspace_scripts test_loading_feedback test_ai_tasks test_needs_inventory -q` | Passed independently | Exit 0; 83 tests in 13.888 seconds, no skips. Source-first imports; no install or shared venv mutation. |
| `node --check src/api/src/zava_forward/api/web/app.js` | Passed independently | Exit 0. |
| `git diff --check` | Passed independently | Exit 0 for current tracked changes. |
| Inline Python Sr./Jr., Dr. and St. discriminators | Defect reproduced | Sr./Jr. merge the uncited/cited statements; Dr. positive and St. terminal control retain their expected behavior. See RV-001. |
| Inline Node VM using actual h() and startupFailed() | Defect reproduced | Incomplete defined helper throws before render/ready event. See RV-002. This is a lightweight source probe, not a browser run. |
| Core/API mypy, Ruff check and Ruff format check | Reported passed; not independently rerun | Changes records core mypy 157 files, API 101, Ruff exit 0 for both. External supplemental logs were not opened; these are implementation evidence, not this Review's independent executions. |
| Original red/green attempts | Reported; preserved | Changes retains initial failing regressions, normalization, formatting and harness-scope failures, followed by final green results. No earlier failure was silently rewritten into a pass. |
| Full discovery, fresh shared editable setup, loading/briefing Chromium/axe and workspace-script browser runs | Unperformed | Busy admission exit 75; owner explicitly permits targeted fallback. No lock retry/poll, full/browser execution or install by Review. |
| Current Web Interface Guidelines | Retrieved and applied to scoped changed code | Complete source fetched 2026-10-29; finding above uses file:line format. |
| Complete local publication gate; human/hosted approval | Not performed | Outside authorization; no gate receipt or accessibility/deployment acceptance asserted. |

## Outcome

* Outcome: Not accepted.
* Rationale: two independently reproduced source defects remain, including High-severity citation misownership. The exact-example planning traceability gap and honest residual browser/full-lane limitation are separately routed. Implementation task markers are reconciled, but cannot override unmet behavior acceptance.
* Severity summary: 0 Critical, 1 High, 2 Medium, 1 Low. One Medium is residual validation, not an implementation defect.
* Review execution is Complete; this is not a claim that all planned heavy checks or product acceptance completed.

## Closeout Routing Record

| Finding class | Destination | Owner or next action |
| --- | --- | --- |
| Implementation defects | Later rpi-implement: RV-001/RV-002 | Future correction owner; no fixes or closure this round. |
| Planning traceability gap | Later rpi-plan: RV-003 | Parent preserves original examples and acceptance mapping. |
| Material research gap | None | Existing source and tests suffice to identify the defects; do not create a research cycle to rerun tests. |
| Non-blocking residual work | Distinct FU-001: RV-004 | Parent coordinates a later explicit heavy-validation event. |

* Execution status: Complete.
* Outcome: Not accepted.
* Validation coverage: independent 83-test focused lane, syntax, whitespace and two discriminating probes; implementation-reported static checks; unperformed full/browser/editable lane retained explicitly.
* Review blockers: none. Future validation blocker: recorded lock contention, not retried.

## Artifacts

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/research/2026-10-29/loading-briefing-review-538-research.md](.copilot-tracking/research/2026-10-29/loading-briefing-review-538-research.md) | Bounded research and evidence claims assessed. |
| [.copilot-tracking/plans/2026-10-29/loading-briefing-review-538-plan.md](.copilot-tracking/plans/2026-10-29/loading-briefing-review-538-plan.md) | Current requirements, completion markers and FU-001 assessed. |
| [.copilot-tracking/details/2026-10-29/loading-briefing-review-538-phase-details.md](.copilot-tracking/details/2026-10-29/loading-briefing-review-538-phase-details.md) | Current task details and critique dispositions assessed. |
| [.copilot-tracking/reviews/plans/2026-10-29/loading-briefing-review-538-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-29/loading-briefing-review-538-plan-critique.md) | Original Revise outcome preserved unchanged. |
| [.copilot-tracking/changes/2026-10-29/loading-briefing-review-538-changes.md](.copilot-tracking/changes/2026-10-29/loading-briefing-review-538-changes.md) | Current implementation, validation, adverse attempts and residuals assessed. |
| [.copilot-tracking/rpi-sessions/2026-10-29/loading-briefing-review-538-state.json](.copilot-tracking/rpi-sessions/2026-10-29/loading-briefing-review-538-state.json) | Current parent-owned Review phase and future-validation state assessed. |
| [.copilot-tracking/reviews/logs/2026-10-29/loading-briefing-review-538-review.md](.copilot-tracking/reviews/logs/2026-10-29/loading-briefing-review-538-review.md) | This single independent Review and complete finding set. |

## Next Steps

Active parent: preserve this original outcome and route RV-001/RV-002 to distinct future implementation work, RV-003 to future plan reconciliation and RV-004 to existing FU-001. Stop this round without fixes, verification/closure, a repeated Review or heavy-lock retry. No user response is required for this handoff.

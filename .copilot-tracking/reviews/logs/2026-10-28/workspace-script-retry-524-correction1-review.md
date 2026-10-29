---
title: Workspace script retry correction independent RPI Review
description: Single post-implementation review of task 524-correction1
ms.date: 2026-10-28
---

## Opening Review State

* Interpreted review goal: independently assess the complete correction against AC1-AC6, current implementation evidence and direct PC-001/PC-002 dispositions; preserve the original adverse Review.
* Review scope: task 524-correction1, all current correction artifacts and four source/documentation files changed from HEAD.
* Evidence readiness: supplied research, plan, phase details, changes, critique and original Review exist; detailed comparison and direct evidence inspection pending.
* Acceptance basis: current correction requirements and AC1-AC6; correction conformance is distinct from publication and live approval.
* First comparison boundary: reconcile current artifact markers and dispositions with the HEAD diff, then inspect regression/browser observability and parent-produced validation evidence.
* Active read-only boundaries: only this review record may be written. No delegation, repeated Review, source/artifact edits, heavy tests, locks, Azure, secrets, environment files or private data access.
* Initial blockers: none identified before evidence comparison. Final exact-head publication gates remain future work.

## Scope and Evidence

* Task ID: 524-correction1; Review date: 2026-10-28.
* Branch: fix/workspace-script-retry-524; inspected HEAD: 2666a4020234ba3dae3c559c51a4c7abab1e622a.
* Assessed boundary: all correction requirements, AC1-AC6, P01/P02 and task markers, implementation-time fixture updates, PC-001/PC-002 direct dispositions, validation, follow-up, and publication limitations.
* Plan: .copilot-tracking/plans/2026-10-28/workspace-script-retry-524-correction1-plan.md.
* Phase details: .copilot-tracking/details/2026-10-28/workspace-script-retry-524-correction1-phase-details.md.
* Research: .copilot-tracking/research/2026-10-28/workspace-script-retry-524-correction1-research.md.
* Changes: .copilot-tracking/changes/2026-10-28/workspace-script-retry-524-correction1-changes.md.
* Critique: .copilot-tracking/reviews/plans/2026-10-28/workspace-script-retry-524-correction1-plan-critique.md.
* Immutable original Review: .copilot-tracking/reviews/logs/2026-10-28/workspace-script-retry-524-review.md.
* Entire four-file correction diff and relevant unchanged context inspected: src/api/src/zava_forward/api/web/app.js, src/api/tests/test_workspace_scripts.py, src/api/checks/workspace_scripts_browser_check.py, src/api/README.md. Related context: index.html status/main semantics, role-screens.js actual function entry, synthetic browser-server lifecycle and src/README.md publication contract.
* Project context: original case study, addendum opening, reference index and owner memory. No private data inspected.
* Parent-produced external logs read directly: full API discovery/browser attempt 1 and browser attempts 2, 3 and 4 at the supplied paths. Final lightweight results are parent-reported in the supplied changes record and instruction, not independently rerun.

## Execution Status

* Review execution status: Complete. This is the single independent correction Review; no delegation or repeated Review.
* Implementation execution: Complete as source delivery, validation execution and pre-Review handoff. Completion does not imply every assertion establishes its intended negative property.
* Publication execution: Not performed; explicitly future work.
* Review-owned execution: read-only source/artifact/log inspection, fresh web-guideline retrieval, standards inspection and git diff --check. No unit/browser/heavy tests, shared-lock access, dependency changes, commit, push, Azure or live inspection.
* Outcome: Not accepted for the complete correction proof boundary because RV-001 is a substantive browser-observability defect. No current production session-guard defect was identified.

## Plan-to-Change Reconciliation

| Current plan scope | Changes-record summary | Current-state reconciliation | Gap or rationale |
| --- | --- | --- | --- |
| P01-T01 | Actual session identity captured and checked; null/replacement regressions | Reconciled | Entry, post-await success and catch guards match accepted direction. |
| P01-T02 | Initial failure/readiness/retry proof, deterministic real-script settlement, exact independent status, real 401 and native reload | Reconciled delivery; incomplete invocation observability | RV-001: zero wrapper calls does not directly establish zero original view calls before wrapper installation. |
| P02-T01 | Full API discovery, final Chromium, focused/static checks | Reconciled execution evidence | Parent logs retain all three failed browser attempts and final pass. Existing discovery skips remain qualified. |
| P02-T02 | Reconciliation and one independent Review handoff | Reconciled for explicitly stated pre-Review boundary | Checked marker is not a claim that commit/full gate/push happened; details and changes explicitly defer those actions. |
| Follow-Up Items | Owner live diagnosis and post-deploy verification | Reconciled | Outside current local correction, not an unchecked implementation task. |

Research's opening Status: In progress and Q1-Q3 Open labels are historical/stale summaries. Later Findings Mapped to Questions and Planning Readiness explicitly answer the questions and record Complete / Ready. This does not obscure the accepted implementation boundary or create a material research gap.

## Completed Work Assessment

| Criterion or marker | Files and evidence | Assessment |
| --- | --- | --- |
| AC1 / P01-T01 | app.js:203-205,229-233,249-250; test_workspace_scripts.py session loop | Source conforms: actual object identity, not role/ID/truthiness, gates restoration/dispatch and stale catch rendering. Null entry returns before route mutations. Node matrix covers null and distinct replacement across overview/screens and ready/error/timeout/load without artificial abort. |
| AC2 / P01-T02 | Browser check actual api('/api/correction-session') 401, real login/alert, me null and unaborted controller; attempt 4 pass | Same-document login, empty status, unchanged hash and one document are actually asserted. Direct zero original-view invocation measurement is incomplete, RV-001. This is not a demonstrated authorization bypass or current app.js defect. |
| AC3 / P01-T02 | recovery() initial requestfailed, absent global, held successful retry, HTTP 200, actual global and visible map/specialist screen | Covered by source and final Chromium output: Leaflet after one and two failures, actual lexical companion after one; exact request bounds and one document. Source bytes are not substituted for successful recovery. |
| AC4 / P01-T02 | Direct node load/error listeners, bounded event wait, CDP top-level coverage; exact pre/post hash/status/view before revisit | Deterministic settlement replaces the old 300ms assumption. Final navigation, terminal-timeout late delivery and 401 cases each report load/ready with one actual top-level evaluation. The original-function invocation observer has RV-001. |
| AC4 cancellation alternative | Zero evaluation requires observed error, no readiness, unchanged independent state and cached terminal failure/no new request on revisit | Explicit safe branch exists; cancellation was not observed in the supplied Chromium run. No claim that removing a tag cancels execution. |
| AC5 / P02-T01 | Heavy log: 1149 tests in 427.344s, OK (skipped=314); attempt 4 complete Chromium pass and admission timestamps | Required local package/browser execution evidence is now available. 314 existing opt-in/integration skips are not integration acceptance. Original adverse Review remains unchanged. |
| AC6 / P02-T02 | One preserved Revise critique, direct dispositions, this single independent Review; future gate contract in details | Critique/Review requirements executed once. Committed exact-head full gate, external receipt/fresh-main verification and independent exact-head identity assessment are not yet executed and are not accepted as complete; RV-002. |
| Preserved retry policy | app.js loader/predicates unchanged by correction; existing Node cases retained | Two shared error-only retry insertions, 250/500ms delay, five-second attempt timeout, terminal timeout/load-without-global, cached budget, route predicates/messages and healthy dependencies unchanged. |
| Preserved semantics | index.html status role/polite live region/main; terminal native button; browser expect_failure and keyboard action | No new controls, styling, dependency, custom interaction or plain-language change. Final native Tab focus/solid outline/Enter reload checks pass in both exhaustion variants. Not whole-app or assistive-technology acceptance. |
| Scope/docs | Exactly four source/doc files changed; zero executable additions/removals | README accurately distinguishes local recovery, session isolation and pending live transport/deployment evidence. Invocation-measurement claim must be read with RV-001. |

## Implementation-Time Plan and Detail Update Assessment

| Affected marker | What changed and why | Triggering evidence and user decision | Reconciliation | Assessment |
| --- | --- | --- | --- | --- |
| P01-T02 / P02-T01 | Establish keyboard modality by focusing main then Tab to native reload | Attempt 1 programmatic focus did not produce :focus-visible outline; existing user intent requires native keyboard evidence | Changes and details retain failure and successful final run; no CSS/source relaxation | Justified fixture correction, not a material product divergence. |
| P01-T02 / P02-T01 | Correct expected synthetic role to Resident Liaison Officer | Attempt 2 observed fixture's actual role; no new user decision needed | Changes preserve incorrect expectation/failure and direct correction | Supported, not weakened product requirements. |
| P01-T02 / P02-T01 | Wait for completed independent perspective/scope/count announcement before taking baseline | Attempt 3 captured route's intermediate status before list's own async completion | Final source waits for final role/count prefix, captures full inner_text, compares exact full text after settlement before revisit | Justified deterministic baseline; exact final comparison remains intact. |
| P02-T02 / AC6 | Concrete admission and independent exact-head handoff added | PC-001/PC-002; compatible with settled owner authorization | Current plan dispositions and details agree; no runner changes or repeated critique | Both direct planning dispositions complete; execution remains future. |

No material undocumented scope change, unsupported dependent-work resumption or unresolved product decision was found. The fixture fixes preserve approved intent; the new RV-001 concerns the final measurement mechanism, not the justification for those fixes.

## Critique and Material Revision Assessment

* Original correction critique remains Complete / Revise, with its two Medium findings preserved. This Review does not retrospectively change it to Pass.
* PC-001 directly applied: details P02-T02 specifies runner --lock-timeout 0, no outer held duplicate lock, 60-second retries only for verified contention, up to 40 minutes, unique external output per attempt and no retry of admitted/preflight failures as contention. Later execution must retain actual attempts and exits.
* PC-002 directly applied: commit precedes full gate; fresh-main verification precedes independent read-only exact-head/receipt/source-boundary assessment and push; external attestation avoids invalidating the candidate. This is not another substantive RPI Review.
* Actual final browser admission in attempt 4 is consistent with the separate authorized policy: busy 17:32:31Z; acquired 17:33:31Z. No lock was touched by this reviewer.
* Critique's additional warning to measure actual view invocation, rather than only unchanged login DOM, remains relevant: the installed wrapper can miss pre-installation invocation, RV-001.
* Original task Review remains Complete / Not accepted. Original RV-001's source defect is corrected; original RV-002's elapsed-time/top-level/status gaps are substantially corrected; original RV-003 now has new package/browser execution evidence. Historical findings are not rewritten as passed. Original RV-004 remains distinct owner work.

## Plan Follow-Up Assessment

| Follow-up | Why outside immediate scope | Owner or next action | Assessment and route |
| --- | --- | --- | --- |
| Historical live response/cold-start/auth correlation and post-deploy verification | Local synthetic loopback traffic cannot diagnose historical authenticated failure or certify deployment | Owner arranges separately authorized response/telemetry capture and post-deploy verification | Open, legitimate distinct follow-up; RV-003. Do not add to active P01/P02 or claim live issue closure. |

## Web Interface Guidelines

Fresh source retrieved successfully on 2026-10-28 before changed app.js inspection:
https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md.
All fetched rule groups were considered against the complete five-line app.js correction and directly relevant unchanged context. The correction changes session/state guards only. Forms, media, animation, typography, layout, images, hydration, locale and styling are unchanged; no unrelated whole-file UI audit was introduced. Repository-preserved native semantics/plain-language copy take precedence over generic copy preferences.

### src/api/src/zava_forward/api/web/app.js

src/api/src/zava_forward/api/web/app.js:204 - pass: no-session route entry is harmless.

src/api/src/zava_forward/api/web/app.js:231 - pass: changed session cannot restore obsolete status or invoke recovered view.

src/api/src/zava_forward/api/web/app.js:250 - pass: stale-session errors cannot replace current login/replacement UI.

No new changed-app.js guideline finding. This is bounded source review plus supplied Chromium evidence, not fresh reviewer-run browser, WCAG, screen-reader or whole-application conformance.

## Findings

Finding IDs below are local to this correction Review, not edits to original RV findings.

<!-- rpi:review id=RV-001 -->
### RV-001 [Medium]: Load-event wrapper misses the earliest recovered view invocation

* Class: Regression-check defect; no current production session-guard defect demonstrated.
* Related scope: P01-T02, AC2/AC4, actual same-document 401 negative-dispatch proof.
* Evidence: src/api/checks/workspace_scripts_browser_check.py:174-188 attaches a load listener from MutationObserver and installs the roleScreensView wrapper only inside that listener. app.js:159 registers the loader's onload handler before appending the tag; app.js:152-156 resolves recovery from that earlier handler. Browser callback cleanup can run the promise microtask chain before the later listener, so route() can reach the original function before window.workspaceViewCalls starts measuring it. The assertion at browser check:291 only counts calls after wrapper installation. The timeout case has already settled its loader, but the normal late-navigation and especially unaborted 401 path must not depend on that timeout disposition.
* Semantic evidence: WHATWG HTML, clean-up-after-running-script, retrieved 2026-10-28: an empty JavaScript execution stack triggers a microtask checkpoint. Earlier onload completion therefore does not guarantee a later load listener runs before await continuations. This finding is source/event-order analysis, not a reviewer-run browser reproduction.
* Impact: An original recovered view invocation that throws before rendering can escape the zero-call assertion. Exact status/login checks remain valuable and would catch the original combined stale-status regression, and Node stubs directly verify the current guard. They do not make this counter a direct measurement of the actual function's earliest invocation, as expressly required by details and critique. A passing attempt-4 log cannot establish that stronger negative property from this observer.
* Destination: rpi-implement, later bounded correction of the existing browser owner only.
* Owner: Active implementation parent.
* Smallest useful next action: Use the existing CDP precise coverage to assert the actual original roleScreensView function-entry count is zero before revisit and one after a legitimate revisit, or install an observer provably before the loader resolves. Keep successful real script bytes, top-level evaluation count, exact status/hash/login checks, request bounds and all terminal-policy assertions. Preserve this Review and the original evidence; no repeat Review is required.

<!-- rpi:review id=RV-002 -->
### RV-002 [Low]: Exact-head publication evidence is intentionally future work

* Class: Publication prerequisite, not an implementation defect or current failed test.
* Related scope: AC6, P02-T02 publication continuation, PC-001/PC-002 execution.
* Evidence: Current candidate is uncommitted; details Completion Evidence explicitly limits P02-T02 completion to pre-Review handoff. Changes Remaining Work and src/README.md require committed full gate, authoritative external receipt, fresh-main verification and independent exact-head assessment. No final receipt exists in the supplied Review boundary.
* Impact: Current local successes and this Review cannot authorize a publication-readiness claim or stand in for hosted/human gates.
* Destination: Distinct parent-owned publication continuation, after RV-001 disposition; not a new active implementation task.
* Owner: Active parent and independent exact-head assessor.
* Smallest useful next action: Preserve evidence and resolve the routed check defect, validate the resulting candidate, commit with authenticated noreply identity and required trailer, fetch main, execute full gate using the applied admission contract, verify authoritative external receipt against fresh main immediately before independent exact-head assessment and nonforce push/gh pr create. Any source/base/commit/input change invalidates prior receipt. Use Refs #524; do not imply closure or merge approval.

<!-- rpi:review id=RV-003 -->
### RV-003 [Low]: Live diagnosis and post-deployment checks remain owner-pending

* Class: Non-blocking residual live work, inherited from original RV-004.
* Related scope: Plan Follow-Up Items; README live limitations.
* Evidence: Plan, changes and src/api/README.md explicitly retain missing authenticated status/size/headers/cold-start/auth correlation and owner-approved post-deploy verification.
* Impact: Local synthetic recovery proof does not identify historical deployed transport cause or establish live acceptance.
* Destination: Distinct owner live-verification follow-up, outside active P01/P02.
* Owner: Project owner.
* Smallest useful next action: Arrange authorized live capture and separately approved post-deploy verification; preserve pending wording and original adverse evidence.

## Defects

* RV-001: Medium browser-check observability defect, routed to later rpi-implement. Source session identity correction itself conforms to the accepted direction.
* No Critical/High finding, unresolved significant decision gap or new material missing-execution evidence gap identified.

## Routed Findings

| Finding | Severity | Destination | Owner and next action |
| --- | --- | --- | --- |
| RV-001 | Medium | rpi-implement | Parent corrects actual-function invocation measurement in existing browser check, preserves assertions and validates correction. |
| RV-002 | Low | Distinct publication continuation | Parent obtains committed full exact-head gate/verified external receipt and independent identity assessment before publication. |
| RV-003 | Low | Distinct live follow-up | Owner arranges authorized live diagnosis/post-deploy evidence. |

Later implementation of RV-001 does not require this Review to run again.

## Residual Work

* Publication sequence remains future and conditional, RV-002; neither an implementation failure nor an implemented acceptance claim.
* Live owner follow-up remains outside authorized local scope, RV-003.
* Preservation-backed generated-cache cleanup, if needed, remains the parent's retention-policy responsibility, not review cleanup authority.

## Blockers and Remaining Work

* No blocker prevented completing this Review.
* RV-001 prevents accepting the entire promised browser proof boundary; route only the bounded measurement correction, not an auth/loader redesign.
* No other active implementation task is missing delivery. Checked P02-T02 means pre-Review handoff only, as its explicit completion paragraph states.
* Publication remains blocked until corrected-candidate validation and required exact-head evidence/approvals exist. Owner authorization to commit/push/create PR does not waive these gates.

## Validation Evidence

| Check or evidence | Status | Summary and provenance |
| --- | --- | --- |
| Full API unittest discovery | Passed, parent-run log inspected | /tmp/ama-524-correction1-heavy-20261028.log: 1149 tests in 427.344s, OK (skipped=314). Existing opt-in/integration skips are not complete integration acceptance. |
| Chromium attempt 1 | Failed, retained | Same heavy log: initial real recoveries passed; native focus-outline assertion failed under programmatic/mouse modality. Not erased by later success. |
| Chromium attempt 2 | Failed, retained | /tmp/ama-524-correction1-browser-attempt2-20261028.log: native reload variants passed; expected role disagreed with real Resident Liaison Officer fixture. |
| Chromium attempt 3 | Failed, retained | /tmp/ama-524-correction1-browser-attempt3-20261028.log: intermediate list status captured before final perspective announcement; exact comparison caught fixture timing error. |
| Chromium attempt 4 | Passed assertions, parent-run log inspected | /tmp/ama-524-correction1-browser-attempt4-20261028.log: all scenarios and HTTP assertions pass. Three late companion paths load/ready, one top-level evaluation each; zero wrapper-call assertion subject to RV-001. |
| Shared admission | Observed in parent logs, not acquired by reviewer | Heavy acquisition 17:24:11Z; final browser busy 17:32:31Z then acquired exactly 60 seconds later at 17:33:31Z. |
| Final 32 focused units | Passed, parent-reported | Changes record/instruction: 0.212s; includes Node VM route/session regressions and related UI contracts. No independent rerun. |
| Package Ruff/check format | Passed, parent-reported | 47-file format boundary; no independent rerun. |
| Package mypy | Passed, parent-reported | 92 source files; no independent rerun. |
| Node syntax and changed Python <=100 characters | Passed, parent-reported | Both changed Python owners within limit; no independent rerun. |
| git diff --check | Passed, reviewer-executed | Read-only whitespace check; no source writes. |
| Fresh web guidelines / changed app.js comparison | Completed by reviewer | Fresh source retrieved before code comparison; no changed-app.js finding. |
| Browser event-order semantics | Source/standards inspection completed | Actual handler registration and late wrapper analyzed; no browser test/mutation rerun, RV-001. |
| Full committed exact-head gate/receipt verification/independent identity assessment | Not performed; future prerequisites | Not inferred from package/browser checks or substantive Review, RV-002. |
| Live authentication/deployment/assistive technology | Not performed | Owner-pending live boundary; no private data, secrets, environment files or Azure accessed. |

## Outcome

* Review execution status: Complete.
* Outcome: Not accepted for complete correction proof boundary.
* Rationale: Session identity source guards, realistic Node coverage, deterministic actual-script settlement, top-level count, exact independent status and parent-run local checks substantially resolve the original findings. However, the actual-function invocation counter is installed after the earlier loader handler can resume route continuations, leaving a required direct negative assertion unsound. RV-001 requires a bounded check correction, not a demonstrated production fix.
* Severity summary: 0 Critical, 0 High, 1 Medium regression-check defect, 2 Low distinct publication/live items.
* Fixture corrections are justified in-scope adjustments, not material divergences. Both planning critique dispositions are complete as contracts. Publication/live gates remain explicitly unexecuted; they are not the reason for the regression-check defect verdict.
* Original Review and critique outcomes remain immutable. No subsequent substantive Review is requested.

## Closeout Routing Record

| Finding class | Destination | Owner or next action |
| --- | --- | --- |
| Implementation/check defect | rpi-implement | RV-001; parent corrects direct original-function measurement and validates within current accepted scope. |
| Decision gap or invalid assumption | None | No new product choice or material plan revision required. |
| Material missing execution evidence | None newly identified | Full API/browser evidence now exists; do not confuse unsound assertion with unexecuted tests. |
| Publication prerequisite | Distinct parent continuation | RV-002; complete exact-head gates after corrected validation. |
| Non-blocking residual live work | Distinct owner follow-up | RV-003; live diagnosis/post-deploy verification remains pending. |

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/research/2026-10-28/workspace-script-retry-524-correction1-research.md](.copilot-tracking/research/2026-10-28/workspace-script-retry-524-correction1-research.md) | Correction evidence and decisions |
| [.copilot-tracking/plans/2026-10-28/workspace-script-retry-524-correction1-plan.md](.copilot-tracking/plans/2026-10-28/workspace-script-retry-524-correction1-plan.md) | Requirements, AC1-AC6 and dispositions |
| [.copilot-tracking/details/2026-10-28/workspace-script-retry-524-correction1-phase-details.md](.copilot-tracking/details/2026-10-28/workspace-script-retry-524-correction1-phase-details.md) | Task contracts and publication ordering |
| [.copilot-tracking/changes/2026-10-28/workspace-script-retry-524-correction1-changes.md](.copilot-tracking/changes/2026-10-28/workspace-script-retry-524-correction1-changes.md) | Implementation and preserved failed/final validation evidence |
| [.copilot-tracking/reviews/plans/2026-10-28/workspace-script-retry-524-correction1-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-28/workspace-script-retry-524-correction1-plan-critique.md) | Immutable single Revise critique |
| [.copilot-tracking/reviews/logs/2026-10-28/workspace-script-retry-524-review.md](.copilot-tracking/reviews/logs/2026-10-28/workspace-script-retry-524-review.md) | Immutable original adverse Review |
| [src/api/src/zava_forward/api/web/app.js](src/api/src/zava_forward/api/web/app.js) | Corrected session identity guards |
| [src/api/tests/test_workspace_scripts.py](src/api/tests/test_workspace_scripts.py) | Null/replacement and preserved loader contracts |
| [src/api/checks/workspace_scripts_browser_check.py](src/api/checks/workspace_scripts_browser_check.py) | Actual Chromium assertions and RV-001 measurement gap |
| [src/api/README.md](src/api/README.md) | Recovery/session guarantees and live limits |
| [.copilot-tracking/reviews/logs/2026-10-28/workspace-script-retry-524-correction1-review.md](.copilot-tracking/reviews/logs/2026-10-28/workspace-script-retry-524-correction1-review.md) | This single independent correction Review |

## Next Steps

Return Complete / Not accepted to the active parent. Parent routes RV-001 to later rpi-implement for the bounded measurement correction, preserves this Review, validates the resulting candidate and continues RV-002 only when required gates permit. Owner retains RV-003. No user response, repeated Review, or review-owned source/publication action is required.

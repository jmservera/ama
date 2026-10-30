<!-- markdownlint-disable-file -->
# Review: employee-chat-closes-on-send

## Scope and Evidence

* Task ID: employee-chat-closes-on-send-2026-10-30
* Date: 2026-10-30
* Full task boundary: implementation worktree against 29eab2e50dd7f958ea2f8d385411562e5573e8e9; no remote publication.
* Plan, details, critique, changes and research: matching employee-chat-closes-on-send dated 2026-10-30.

## Opening Review State

* Goal: independently assess source correction, regression, requirements and evidence once.
* Readiness: P01 implemented, red/green browser evidence available, final integrated browser/static/targeted-unit results pass.
* Acceptance basis: plan FR1-FR4, AC1-AC5, PC-001/PC-002 direct dispositions, owner no-push/no-deploy/Refs-only.
* First boundary: correlate actual source changes and executable browser assertions with reported root causes; then auth/access/focus boundaries and full evidence.
* Read-only: only this review record may be written by reviewer; no source or phase-artifact mutation.
* Initial blocker: required full API unit discovery not started because shared heavy lock was busy twice. No conformant/publication result may be inferred.

## Execution Status

* Execution status: Complete.
* Exactly one independent post-implementation Review was performed on 2026-10-30. All supplied artifacts, the complete tracked diff against HEAD 29eab2e50dd7f958ea2f8d385411562e5573e8e9 and untracked src/api/checks/chat_submit_browser_check.py were inspected.
* This describes review execution, not implementation-plan completion. The assessed plan remains Partial: P02-T01 lacks mandatory full-unit evidence and P02-T02 local commit is pending by design.
* No source, plan, details, research, original critique, changes or state artifact was modified. No nested agent, second Review, full-suite attempt, lock bypass, remote write, Azure operation or deployment was performed.

## Compared Artifacts and Evidence

* Plan: .copilot-tracking/plans/2026-10-30/employee-chat-closes-on-send-plan.md.
* Phase details: .copilot-tracking/details/2026-10-30/employee-chat-closes-on-send-phase-details.md.
* Original critique: .copilot-tracking/reviews/plans/2026-10-30/employee-chat-closes-on-send-plan-critique.md, Complete / Revise, PC-001 High and PC-002 Medium.
* Changes: .copilot-tracking/changes/2026-10-30/employee-chat-closes-on-send-changes.md.
* Research: .copilot-tracking/research/2026-10-30/employee-chat-closes-on-send-research.md.
* Runtime delta: only show() and start() in src/api/src/zava_forward/api/web/app.js. Shared chat-widget.js, employee chat.js and resident_demo/web/assistant.js were examined as unchanged lifecycle dependencies.
* Check/documentation delta: src/api/checks/chat_widget_browser_check.py, new src/api/checks/chat_submit_browser_check.py and src/api/README.md.
* External read-only evidence root: /home/azureuser/.copilot/session-state/231d6783-58ff-4002-bb8d-79e269bd38c0/files. Read submit-red.log, submit-green-2.log, shared-green-final.log, shared-green-final/results.json, submit-green-2/results.json and baseline-reproduction.json.
* Required project context: original case study, addendum, reference index and owner memory read. No private dataset was read.
* Web Interface Guidelines skill activated and current command.md retrieved successfully from https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md before changed-web assessment. All fetched categories were considered for the changed blocks; unrelated existing UI, styling and content were not audited.

## Plan-to-Change Reconciliation

| Current plan scope | Changes/evidence | Current-state reconciliation | Gap or rationale |
| --- | --- | --- | --- |
| P01-T01; FR1; AC1 | Actual Enter/mouse Send, case/no-case, none/route/session refresh; original red and final integrated green | Reconciled for submitted answer visibility | Baseline records 4 ordinary successes, 4 hidden route answers and 4 hidden/missing session answers. Executable red stops at the first route failure; it is not an independently failing assertion of both causes. Original baseline separately demonstrates the session failure. |
| P01-T02; FR1/FR2 | show() preserves the currently focused visible chat descendant | Partial | Internal textarea/log/Sources focus passes. Deliberate dismissal before delayed rendering is tested against app focus, contrary to PC-002's explicit outside-focus preservation; RV-001. |
| P01-T02; FR3; AC2 | start() retains me only for equal complete user/account, resets changed snapshots and guards obsolete success | Reconciled | Real-start setup/thread/ask variants and stale-auth race support the intended identity boundary. |
| FR4; AC3 | Resident runtime unchanged; focused actual rules replies and existing consent/session coverage | Reconciled | Both activation methods pass without changing resident consent or invalidation semantics. |
| P02-T01; AC4 | Targeted units/static/integrated browser pass; full discovery not started | Partial, accurately unchecked | Two busy nonblocking lock attempts are recorded; no full-unit result exists. RV-002. |
| P02-T02; AC5 | Original critique preserved; this one independent Review completed; local commit follows assessment | Expected sequencing | Pending local commit is not a source defect. Parent owns privacy-safe local identity/commit and Refs-only delivery, without publication. |
| Follow-Up Items | Later separately authorized deployed-site verification | Reconciled | Remains distinct follow-up, not local acceptance or active deployment scope. |

The plan's Handoff still names a noncanonical review path and says "critique, then Implement"; research Q1-Q3 retain "Open" table cells despite the later answered synthesis. These are stale descriptive pointers, not ambiguity about this supplied artifact set: stable markers, dispositions, current phase details and Changes explicitly identify the current implementation/validation state. They do not authorize a repeated critique or Review and are not separate substantive findings.

## Completed Work Assessment

| Marker / criterion | Files | Assessment and completion evidence |
| --- | --- | --- |
| P01-T01 / AC1 | src/api/checks/chat_submit_browser_check.py | Real browser actions, held answer request, exact post-busy activeElement, draft/skill, expanded state, visible answer and completed busy asserted in 12 combinations. Final integrated owner invokes the new employee check. Timing replies are constructed; not actual model evidence. |
| P01-T02 / FR1 | src/api/src/zava_forward/api/web/app.js:92-96 | Root-cause correction is narrow: app replacement no longer focuses away from a visible chat-owned element. No timers, reopening, suppression flags or event-trust heuristic introduced. |
| P01-T02 / FR2, AC1 | src/api/checks/chat_submit_browser_check.py:117-146 | Hidden state is preserved after Escape/external dismissal, but delayed render explicitly moves focus to app. Captured renderFocus is not compared after completion in this branch; RV-001. |
| P01-T02 / FR3, AC2 | src/api/src/zava_forward/api/web/app.js:137-159 | Complete user/account JSON comparison is conservative; non-identity fields update in place. Real changed user/capability/account disposes chat and aborts its controller before replacement; guard rejects successful re-check after me changes. No demonstrated auth weakening found in this boundary. |
| P01-T02 / FR4, AC3 | Unchanged shared widget and resident host; focused resident check | Native nonmodal dialog, labels, live regions, busy focus-before-disable, Escape, external focus dismissal, consent generation and session clear remain intact. Actual rules replies are verified for both send methods. |
| P02-T01 / AC4 | Existing and new checks; Changes validation record | Broad browser evidence is credible for asserted conditions, not sufficient for the unrun full-unit requirement or the contradicted focus assertion. |
| P01-T02 / documentation | src/api/README.md | Accurately describes same-context visibility/equal-session behavior, focused command and local-engineering limitations; no live/WCAG acceptance asserted. |

## Implementation-Time Plan and Detail Update Assessment

| Affected scope | Change and trigger | Reconciliation / decision | Assessment |
| --- | --- | --- | --- |
| AC2 / P01-T01 / P01-T02 | PC-001 added actual start(), mutable non-identity, changed user/account/capability and obsolete-auth cases | Direct disposition in plan and details; retains approved intent, no significant new decision | Implemented and exercised. |
| AC1 / FR2 / P01 | PC-002 added precise post-send focus, history/Sources and delayed-dismissal assertions | Direct disposition recorded; no new user decision | Partial: internal-focus and non-reopening assertions implemented; deliberate external/launcher focus retention silently replaced by the opposite expectation. No recorded approval supports that divergence; RV-001. |
| P02-T01 | Busy shared lock prevents full discovery | Details, Changes, unchecked marker and pre-review handoff agree | Honest blocked validation; no fabricated pass, waiting, bypass or cloud fallback. RV-002 remains material. |
| P02-T02 | Review precedes local commit | Details and supplied parent instructions agree | Normal delivery sequencing, not a decision gap or independent defect. |

No material architectural revision, new runtime dependency, resident redesign or changed server auth contract was introduced. The unsupported focus expectation is a correction within the accepted direction, not a reason to broaden scope or seek a new design.

## Critique and Material Revision Assessment

* PC-001: independently resolved for the supplied acceptance boundary. All 3 pending stages x 4 auth variants invoke actual start(). Equal user/account with changed counts/navigation retains reference, focus and unaborted consumer; changed user, rule_roles or account email disposes and aborts. Completing obsolete setup/thread/ask cannot alter replacement markup, focus or ask count. A held /api/me success after session invalidation cannot restore me, nav or widget. Final supplied logs report these checks passed.
* PC-002: partially resolved, not fully disposed. Internal textarea/history/Sources focus and the mouse-send capture after busy are correctly asserted. Escape/external dismissal remains hidden, but src/api/checks/chat_submit_browser_check.py:145-146 deliberately requires app focus rather than preserved renderFocus. That contradicts the original critique's required "do not redirect outside focus" and phase-details P01-T01. RV-001 records the one coupled implementation/test gap.
* Original Revise verdict is preserved. Compatible planning edits were applied before implementation; no unresolved significant owner decision required pausing dependent work. The passing suite cannot justify changing an accepted focus assertion without disposition.

## Auth, Focus and Stale-Result Boundary Assessment

* Successful equal re-check: retaining me reference keeps unchanged chat.js current() valid; actual chat request AbortSignal is separate from routeController, so same-route rendering does not cancel the pending chat.
* Changed identity/account/capability: reset(true) aborts and disposes before accepting refreshed me; no old consumer can satisfy both widget identity and session identity. Tests cover old success completion at setup/thread/ask; existing obsolete rejection coverage separately covers route/session invalidation.
* Expired/failed auth: unchanged api() still handles 401 with me=null and login/reset; start() does not swallow failures or restore a captured session. Existing access-loss/current/obsolete browser checks remain. No new claim is made about every possible overlapping server-auth race or live identity-provider behavior.
* Route/case changes: unchanged route() resets chat on destination-path changes; unchanged widget/session/signal guards still reject old results. Same-context refresh retains draft/skill and open toggle.
* Focus: internal focus preserved; current answers/errors do not asynchronously focus the widget; explicit outside focus hides it and Escape returns to launcher immediately. The later delayed render then steals those deliberately selected targets, an observed acceptance failure rather than a speculative issue; RV-001.
* Resident: no source modification, no weakening of signedIn/generation/consent checks. Prior resident withdrawal/re-consent/session coverage and new actual rules replies remain distinct evidence.
* No source defect was established in the inspected auth/access/stale-result paths. This is bounded source/browser assessment, not a general security audit.

## Plan Follow-Up Assessment

| Follow-up | Why outside immediate scope | Owner / next action | Assessment and route |
| --- | --- | --- | --- |
| Deployed employee-site verification | No deployment authorized; loopback synthetic checks cannot establish owner's deployed triggers | Owner/coordinator, after separately authorized redeployment | Open distinct residual follow-up. Do not silently add deployment, live model or human accessibility acceptance to this local task. |

## Findings

<!-- rpi:review id=RV-001 -->
### RV-001 [Medium]: Delayed render redirects deliberate outside/Escape focus; new check accepts the opposite contract

* Related scope: FR2, AC1, P01-T01/P01-T02, PC-002.
* Evidence: src/api/src/zava_forward/api/web/app.js:95 - show() focuses app whenever focus no longer belongs to a visible chat, including a retained nav control or Escape-return launcher chosen while rendering was pending.
* Evidence: src/api/checks/chat_submit_browser_check.py:135-146 - captures the chosen activeElement, releases the delayed case render, then requires app to be focused rather than comparing renderFocus. The passing supplied browser run therefore positively demonstrates the redirect. Original PC-002 explicitly requires no redirect of deliberately chosen outside focus; phase details P01-T01 repeats that obligation.
* Independent narrow confirmation: evaluating the exact source show() block with a minimal document/app model retains internal-chat focus but changes external-nav and escape-launcher to app. This is a source-level confirmation, not a new browser run.
* Impact: a keyboard user who has deliberately dismissed chat loses the navigation or launcher position on completion of unrelated delayed rendering. Immediate Escape behavior and hidden state pass, but the accepted delayed-dismissal focus boundary does not.
* Destination: later rpi-implement.
* Smallest useful next action: preserve the deliberately selected still-connected focus target through this delayed refresh while retaining ordinary workspace focus when appropriate; change the regression to assert exact retained external/launcher focus after completion, with no reopening. Do not remove intentional external dismissal, automatically reopen chat or broadly suppress navigation focus.
* This behavior existed in the old unconditional app focus, but is expressly in the accepted PC-002 correction boundary; it is not unrelated UI cleanup.

<!-- rpi:review id=RV-002 -->
### RV-002 [Medium]: Required full API unit evidence is unavailable

* Related scope: AC4, P02-T01.
* Evidence: phase details P02-T01 and Changes validation/pre-review sections explicitly record two nonblocking shared-heavy-lock attempts, neither starting full unittest discovery. P02-T01 correctly remains unchecked. Supplied browser JSON/logs do not supply a unit-suite result.
* Impact: requested package-level regression validation is unestablished. Passing 68 targeted tests and browser/static checks cannot establish complete task conformance or publication acceptance. No source defect or failing full-suite result is inferred.
* Destination: rpi-research, bounded validation-evidence collection by the active parent/coordinator when the shared lock becomes available.
* Smallest useful next action: run the existing documented full API unittest discovery with the specified caller PYTHONPATH and normal shared-lock admission; record actual pass/failure/skip output. Do not bypass, queue behind a busy lock, fabricate a status or substitute cloud validation. Preserve this original Review outcome.

## Defects

* RV-001 is the only demonstrated implementation/acceptance defect. No Critical or High source finding.
* RV-002 is a material validation-evidence gap, not an implementation defect.
* Severity total: 0 Critical, 0 High, 2 Medium, 0 Low.

## Routed Findings

| Finding | Destination | Owner / next action | Reason |
| --- | --- | --- | --- |
| RV-001 | rpi-implement | Active parent: bounded source/focus-regression correction | Fits accepted PC-002 intent; no new architectural decision required. |
| RV-002 | rpi-research | Active parent/coordinator: collect mandatory full-unit evidence when admitted | Missing validation evidence, not an observed full-suite failure. |

Later implementation or evidence collection does not require this Review to run again.

## Residual Work

* Distinct owner/coordinator follow-up: deployed-site verification only after separate authorization. Not a source defect, an active deployment task, or evidence that local controls passed live.
* Human screen-reader/voice-control, live-model and whole-app WCAG acceptance remain unestablished; local axe does not substitute for them.

## Blockers and Remaining Work

* P02-T01: full API unit discovery blocked by reported shared lock contention; reviewer neither retried nor bypassed it.
* RV-001: accepted delayed-dismissal focus behavior is not met; route to later implementation rather than modifying source during Review.
* P02-T02: local commit remains the parent's expected next delivery step after assessment. Preserve this review and original critique, resolve privacy-safe author/committer identity through gh api user, use required trailer and Refs-only references. No push, PR creation, issue closure, Azure or deploy authorized.
* No publication acceptance: local full gate, exact-head verification, hosted checks and human approvals are not established or waived by this assessment or a local commit.

## Validation Evidence

| Command / evidence | Scope | Status | Summary / provenance |
| --- | --- | --- | --- |
| baseline-reproduction.json | Actual loopback app / 12 combinations before fix | Passed reproduction | Four ordinary sends visible/answered; route four hidden/answered; session four hidden/unanswered. Reviewed external evidence, not rerun. |
| python -m checks.chat_submit_browser_check; submit-red.log | Failing-before regression | Failed as intended | False/Enter/route dismissed submitted chat. Cleanup cancellation trace follows primary assertion; not a separate runtime defect. |
| Focused browser; submit-green-2.log and results.json | 12 employee matrix, 12 real-start variants + stale-auth race; resident actual rules | Passed as asserted | Chromium 156.0.8078.4. Focus assertion limitation is RV-001, not a fabricated browser failure. |
| Integrated shared browser with pinned axe 4.10.3; shared-green-final.log/results.json | Existing + integrated new employee check; resident/access/consent/layout | Passed as asserted | Includes prior 48 focus/denial and 12 obsolete success/rejection combinations, script recovery, axe/reflow/following. Actual resident Enter/Send rules evidence is from the separate focused run. |
| Targeted unittest selectors | test_chat_widget_focus, test_chat_panel, test_resident_chat_api | Passed, one skip | Changes reports 68 tests, OK, one opt-in SQL skip; raw unit log not among supplied external read boundary. Not independently rerun. |
| Ruff check/format, mypy, node --check, compileall, git diff --check | API/static selectors | Passed, reported | Changes reports 59 formatted files / 114 mypy source files and final post-integration pass. No full-suite implication. |
| node --check app.js; ast.parse both changed checks; git diff --check | Independent bounded review checks | Passed | Executed during this Review without file generation or dependency changes. |
| Exact show() source block in Node minimal DOM model | Internal vs external/launcher focus | Completed; mismatch confirmed | Internal retained; external-nav and escape-launcher each redirected to app. Does not claim actual browser execution. |
| Full API unittest discover | Required package-level regression suite | Unavailable / not started | Two reported busy nonblocking lock attempts; no queue/bypass and no reviewer full-suite run. RV-002. |
| Deployed site / live model / human assistive technology | Operational acceptance | Not run | Outside authorization/local evidence, retained as distinct follow-up or acceptance limitation. |

## Changed-Web Guidelines Assessment

### src/api/src/zava_forward/api/web/app.js

src/api/src/zava_forward/api/web/app.js:95 - delayed refresh redirects deliberate external/launcher focus; RV-001, accepted PC-002 focus boundary unmet.

No other changed-line guideline finding. Native actions/labels, live updates and shared keyboard handlers are unchanged. No new styling, animation, image, layout, locale rendering, content or navigation element was introduced; those guideline categories introduce no changed-line finding. This is not a whole-app conformance statement.

## Outcome

* Outcome: Not accepted.
* Review execution is Complete; assessed task execution remains Partial.
* The central Enter/Send visibility and equal-session pending-answer corrections are supported by actual browser evidence, with no demonstrated new auth/access/stale-result defect.
* Acceptance remains unmet because PC-002's delayed-dismissal focus requirement is contradicted by source and regression, and AC4's full API unit validation is unavailable. Neither passing integrated browser evidence nor expected pending local commit changes that conclusion.
* No source fix, plan revision or acceptance waiver was made in this Review.

## Closeout Routing Record

| Finding class | Destination | Owner / next action |
| --- | --- | --- |
| Implementation defect | rpi-implement, RV-001 | Active parent corrects accepted delayed-dismissal focus behavior and regression in later work. |
| Decision gap or invalid assumption | None | No significant new owner decision or broadened design needed. |
| Material evidence gap | rpi-research, RV-002 | Active parent/coordinator obtains actual full API unit evidence under normal lock admission. |
| Non-blocking residual work | Distinct live-site follow-up | Owner/coordinator after separately authorized deployment. |

* Execution status: Complete.
* Outcome: Not accepted.
* Validation coverage: actual Chromium/axe, focused browser and reported targeted/static passes; narrow independent source/syntax checks completed; full API units unavailable.
* Blockers: RV-001 accepted-focus failure and RV-002 required validation gap. Local commit pending is sequencing, not a source defect.

| [.copilot-tracking/research/2026-10-30/employee-chat-closes-on-send-research.md](.copilot-tracking/research/2026-10-30/employee-chat-closes-on-send-research.md) | Dated reproduction and source findings |
| [.copilot-tracking/plans/2026-10-30/employee-chat-closes-on-send-plan.md](.copilot-tracking/plans/2026-10-30/employee-chat-closes-on-send-plan.md) | Requirements, criteria, task markers and dispositions |
| [.copilot-tracking/details/2026-10-30/employee-chat-closes-on-send-phase-details.md](.copilot-tracking/details/2026-10-30/employee-chat-closes-on-send-phase-details.md) | Execution detail and blocked validation state |
| [.copilot-tracking/reviews/plans/2026-10-30/employee-chat-closes-on-send-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-30/employee-chat-closes-on-send-plan-critique.md) | Original Complete / Revise, preserved |
| [.copilot-tracking/changes/2026-10-30/employee-chat-closes-on-send-changes.md](.copilot-tracking/changes/2026-10-30/employee-chat-closes-on-send-changes.md) | Implemented boundary and validation provenance |
| [src/api/src/zava_forward/api/web/app.js](src/api/src/zava_forward/api/web/app.js) | Reviewed runtime changes |
| [src/api/checks/chat_submit_browser_check.py](src/api/checks/chat_submit_browser_check.py) | New focused actual-browser check |
| [src/api/checks/chat_widget_browser_check.py](src/api/checks/chat_widget_browser_check.py) | Existing integrated browser/axe owner |
| [src/api/README.md](src/api/README.md) | Updated contract and validation commands |
| [.copilot-tracking/reviews/logs/2026-10-30/employee-chat-closes-on-send-review.md](.copilot-tracking/reviews/logs/2026-10-30/employee-chat-closes-on-send-review.md) | This single independent Review |

## Next Steps

Return this one Review to the active parent. Route RV-001 to later rpi-implement and RV-002 to bounded rpi-research evidence collection when normal lock admission succeeds; preserve the original outcome without another Review. Parent owns the requested local-only evidence/implementation commit with Refs-only references and the outstanding delivery state. Keep deployed verification as distinct follow-up. No publication, push, issue closure, Azure operation or deployment is accepted or authorized.

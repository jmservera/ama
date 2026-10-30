---
title: Capacity delayed sibling 401 original post-implementation Review
description: Independent bounded RPI Review for task 523-delayed-401 and PR 528
ms.date: 2026-10-28
---

## Opening Review State

* Interpreted review goal: independently assess the delayed sibling 401 correction and its synchronized two-endpoint regression once.
* Review scope: task 523-delayed-401 / capacity-page-523-delayed-401, issue #523, PR #528; working diff from HEAD 2d207b6284930d926324cdfea9282d3e78ce6203 in ops.js, capacity_browser_check.py and API README, plus the six dated task artifacts.
* Evidence readiness: research, plan, phase details, original critique, changes and state located; detailed comparison and external log inspection pending.
* Acceptance basis: supplied task requirements, current plan markers, original critique dispositions, consumed-body and retry-finally synchronization, existing lifecycle behavior and freshly retrieved web guidelines.
* First comparison boundary: reconcile the six task siblings, then inspect the bounded implementation diff against app.js lifecycle context and supplied external validation.
* Active read-only boundaries: only this review record may be written; no implementation, artifact mutation, git writes, nested agents, browser/heavy tests, az, full gate, secret/.env/private-data reads or second Review.
* Initial blockers: full gate is user-forbidden and live owner acceptance remains pending; neither may be reported passed. Existing dirty implementation and artifacts belong to the parent and remain untouched.

## Scope and Evidence

* Task ID: 523-delayed-401 / capacity-page-523-delayed-401.
* Review date: 2026-10-28 UTC.
* Branch: fix/capacity-page-523; issue #523, existing PR #528.
* Assessed source boundary: working diff against HEAD 2d207b6284930d926324cdfea9282d3e78ce6203 in src/api/src/zava_forward/api/web/ops.js, src/api/checks/capacity_browser_check.py and src/api/README.md. Diff: 109 insertions, one import-line deletion/reordering across three files; exactly two production guard lines.
* All six supplied 2026-10-28 delayed-401 siblings were read in full: research, plan, phase details, original critique, changes and JSON state. Earlier task Reviews were consulted only for the already named historical follow-ups, not reassessed or modified.
* Necessary lifecycle context: app.js api, login, show and route; ops.js capacityView, go, load and synchronous rendering/draft restoration.
* Repository context: original case study, relevant addendum, reference index, owner memory and sector primer. No new customer, regulatory or authority conclusion is made.
* External evidence root, workspace-relative: ../../../.copilot/session-state/30941a6a-b0c2-4550-8386-a144af07efac/files/. Named logs and launcher below are under that root; they are external evidence, not committed acceptance receipts.
* No source, plan, critique, changes or state file was edited. This is the task's one independent original post-implementation Review. No second critique, nested agent or repeat Review was invoked.

## Execution Status

* Review execution status: Complete.
* Planned task execution: Partial. P01-T01 and P01-T02 are evidenced complete; this record supplies P02-T01's assessment. P02-T02 has not run and correctly remains dependent on Review and scoped passing validation.
* Review execution evidence: direct artifact/diff/context inspection; supplied external red/green/unit logs; fresh web-rule retrieval; lightweight Node syntax and whitespace checks only.
* Full gate: Blocked, explicitly prohibited; not run and not passed. Live owner acceptance: pending, not passed. Neither blocks forming a credible verdict on this bounded source correction.

## Plan-to-Change Reconciliation

| Current plan scope | Changes/evidence | Current-state reconciliation | Assessment |
| --- | --- | --- | --- |
| Research C1-C4; functional requirements | Missing aggregate success-boundary check; old 401 does not abort current signal | Reconciled | Exact requested guard, no global authentication change. |
| P01-T01 | One two-endpoint regression, typed capture callback, two genuine red logs | Reconciled | Both endpoint permutations fail after the continuation barrier, not merely on fixture setup. |
| P01-T02 | Two-line guard, README, complete SQL/browser green, 82 units and static results | Reconciled with minor prose residue | Source and primary evidence agree; stale remaining-work prose is RV-001. |
| P02-T01 | State active_phase Review; plan unchecked when assessment began | Reconciled | In-flight status is appropriate; parent owns completion bookkeeping after this handoff. |
| P02-T02 | Commit/push/exact-thread reply and resolution pending | Reconciled | No premature completion, pushed SHA or resolved-thread claim. |
| Follow-Up Items | Full gate, live owner verification and historical RV-004/005/006 | Reconciled | Separate limitations/owners, not additions to the repair or acceptance claims. |

## Completed Work Assessment

| Marker | Files | Change and reason | Completion evidence | Assessment |
| --- | --- | --- | --- | --- |
| P01-T01 | src/api/checks/capacity_browser_check.py:559-657 | Controlled failed refresh, older sibling 401 and held successful retry responses; both endpoints | Both genuine red logs reach line 630's settled message then fail line 631 with Capacity and work orders rather than Sign in | Regression detects the actual missing guard. |
| P01-T02 | src/api/src/zava_forward/api/web/ops.js:177-178 | Recheck captured abort state and current session before building content | Green log passes both new permutations and all previous scenarios | Scoped production behavior Conformant. |
| P01-T02 | src/api/README.md:18-19,42-44 | Describe post-read guard and completed-continuation assertion | Matches source and observed ordering | Accurate; no whole-product/live acceptance claim. |
| P01-T02 | Existing focused tests and static checks | Preserve authorization, procurement and UI-support behavior | 82 tests OK; supplied final static passes, Node/whitespace also checked here | No backend source delta requiring a different suite. |

### Lifecycle and synchronization proof

1. app.js:28-37 awaits fetch and response-body JSON before resolving api. Its 401 branch clears me and renders login, but does not abort the shared route controller. Thus a successful api response alone cannot establish that the session remains present.
2. The first capacity Promise.all rejects when the selected refresh endpoint returns 503. Its older sibling remains outstanding. Promise.all's installed rejection handlers also account for the eventual sibling rejection; it does not become an unhandled page error.
3. The regression retains the original sibling Route before clearing held. Its typed callback appends each held route before incrementing window.capacityHeldReads. Function-form waits at harness lines 591 and 613 require both callback captures to have occurred, followed by len(held) == 2 checks. Request events alone are not mistaken for completed route capture; there is no fixed sleep.
4. The exact clicked retry button ElementHandle is retained at lines 603-605. With both retry GETs held, line 615 checks disabled and aria-busy=true. The older sibling is then fulfilled with 401; heading, session alert and app focus establish that login has already replaced the capacity subtree before either retry response is released.
5. Both retry Routes receive actual successful JSON payloads at lines 624-625. The detached original retry button, not a new locator matching a replacement button, is observed until disabled=false and aria-busy is absent at lines 626-629.
6. ops.js:149-164 makes that transition only in go's finally, after its awaited capacityView returns or throws. In this interleaving both retry responses are successful, the route is not aborted, and api awaits both response bodies. Consequently the retry Promise.all has fulfilled with both parsed bodies before the new !me return and the retained-button finally transition. The final Sign in assertions cannot pass merely because response headers arrived or because login was briefly visible while retry bodies were still pending.
7. Without the guard, capacityView synchronously renders stale capacity before go finally runs. Both genuine red logs therefore report the settled message and then the wrong capacity heading. With the guard, signal.throwIfAborted protects abandoned routes and !me protects the distinct non-aborting 401 path.
8. No await occurs between the new guard and content construction, show and draft restoration at ops.js:179-266. No asynchronous session transition can interleave within that synchronous section.
9. After the barrier, the regression checks heading/email/alert/focus, no capacity heading or Try again, one successful POST and exactly one additional persisted appointment configuration. Existing page/HTTP/transport/console collectors remain active. Reauthentication separates permutations, and route handlers are removed after each.

## Implementation-Time Plan and Detail Update Assessment

| Affected scope | Update and trigger | Reconciliation | Assessment |
| --- | --- | --- | --- |
| P01-T01 / PC-001 | Retain exact detached retry button and wait for its busy-to-settled finally transition | Plan locked boundary, details and changes describe the observable | Applied; meaningful continuation barrier, not a production test hook. |
| P01-T01 / PC-003 | Mandatory separate red runs; workorders-first selected through external in-memory loop reversal | Plan/details require both; launcher changes only endpoint iteration | Applied; committed green remains strict. |
| P01-T01 / capture callback | First fixture attempt failed because request events preceded complete route capture | Changes names original failed log; plan explicitly allows one typed callback | Immediately relevant deterministic fixture refinement, not a divergent product decision. |
| P01-T01 / CSP wait | Expression-string predicate failed under existing CSP | Changes preserves failed log; current predicates are function expressions | No unsafe-eval/CSP bypass or runtime-policy alteration. |
| P01-T02 / PC-002 | Parent rejected worker-specific path prohibition; owner explicitly required existing shared lock | Plan, details, changes and state preserve rejected disposition | Supported by supplied parent authority; no replacement lock, bypass or new product scope. |
| P02 | Review and publication remain pending at input boundary | State names active Review; plan keeps publication dependency | Correct; do not infer publication from completed P01. |

## Critique and Material Revision Assessment

* Original critique remains Complete / Revise, with its original two High and one Medium findings. This Review does not rewrite it to Ready or passed.
* PC-001 and PC-003 are resolved by implementation and actual evidence as above.
* PC-002 is rejected, not applied. The supplied parent/user authority establishes that the worker-local temporary-path prohibition was not a parent constraint and that the exact shared lock was explicitly required. This reviewer does not project its own filesystem restrictions onto the parent's historical execution. No operations on that temporary lock, interpreter or fixture were performed by this Review.
* External launcher inspection confirms 60-second retries, a 40-minute admission deadline, and retry selection by the harness's specific busy diagnostic. Actual test failures exit instead of being silently retried by that loop; the different fixture/red invocations are separately named evidence.
* Harness lines 763-780 acquire the exact shared lock with LOCK_EX | LOCK_NB before generated seed, owned SQL and browser work. The busy log contains the explicit no-browser/no-SQL message. No exclusion bypass or replacement admission path is present.
* The callback and CSP corrections do not alter confirmed intent, authority or architecture. No significant divergent decision or fresh critique is warranted. Original failed fixture logs are preserved and excluded from genuine regression-red counts.
* No dependent publication was resumed early. No additional user decision is necessary for the already authorized scoped continuation.

## Plan Follow-Up Assessment

| Follow-up | Why outside immediate scope | Owner / next action | Assessment |
| --- | --- | --- | --- |
| Complete local gate | Explicit user prohibition; scoped validation is not a substitute | Parent records Blocked; owner controls any future authorization | Remains unpassed; no az or full-gate recommendation for this run. |
| Live verification | No deployment/live acceptance evidence is supplied or authorized here | Owner performs separately authorized live verification | Pending, not a code defect or a passing criterion here. |
| Historical RV-004 | Existing eager work-order DOM strategy; browser completion is not performance measurement | UI/performance owner measures scale and considers draft-safe bounded rendering | Distinct inherited follow-up, unchanged. |
| Historical RV-005 | Unchanged form metadata omissions | UI/forms owner scopes metadata work | Distinct inherited follow-up, unchanged. |
| Historical RV-006 | Unchanged withdrawal confirmation/undo behavior | Work-order UX owner scopes confirmation/undo | Distinct inherited follow-up, unchanged. |

## Findings

<!-- rpi:review id=RV-001 -->
### RV-001 [Low]: Remaining-work prose still lists completed P01 validation as pending

* Related scope: evidence/handoff reconciliation, not production behavior.
* Evidence: .copilot-tracking/changes/2026-10-28/capacity-page-523-delayed-401-changes.md:137-139 says P01 validation remains pending. The same file's Complete green and final static results and Pre-Review Reconciliation sections, current plan P01 checkboxes, external green log and focused-unit log establish completion. Earlier pending statements at lines 21 and 85 are understandable historical progression but lack an explicit superseded label.
* Impact: a reader consulting the final blockers/remaining-work section can mistake completed scoped validation for outstanding work. The evidence is nevertheless sufficient for a credible scoped verdict; no test rerun or source change is needed.
* Destination: distinct nonblocking publication-evidence reconciliation follow-up, owned by the active parent.
* Smallest useful next action: when recording this Review's completion for P02 handoff, add an unambiguous current-state summary distinguishing completed P01 from remaining P02-T02, blocked full gate and pending live acceptance. Preserve historical failed logs and the original critique verdict. Do not rewrite original failures or invoke another Review.

Severity summary: zero Critical, High or Medium new findings; one Low nonblocking evidence-summary finding. No new implementation defect, material evidence gap or unaccepted decision was identified.

## Defects

* No production or regression implementation defect found within the supplied boundary.
* RV-001 is nonblocking handoff housekeeping, not evidence that the scoped behavior failed or that another research/implementation/review cycle is necessary.

## Routed Findings

| Finding | Destination | Owner / next action | Reason |
| --- | --- | --- | --- |
| RV-001 | Distinct publication-evidence reconciliation follow-up | Active parent clarifies current status during handoff bookkeeping | Authoritative results exist; residual prose ambiguity only. |

Later implementation or evidence reconciliation does not require another Review.

## Web Guidelines Assessment

Fresh source retrieved successfully on 2026-10-28:
https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md.
All fetched rule categories were considered against the changed web lines; only lifecycle/state preservation applies directly to the two new JavaScript statements. They add no controls, styles, animation, images, hydration, locale formatting or navigation affordances. Existing login alert/focus and retry semantics are preserved. Repository ASCII and owner-selected Fluent/plain-language conventions are not overridden by generic typography preferences.

### src/api/src/zava_forward/api/web/ops.js

* src/api/src/zava_forward/api/web/ops.js:177-178 - pass; post-read abort/session guard prevents stale async content and focus replacement.

Pre-existing, out-of-scope UI debt, retained under original finding IDs rather than invented new defects:

* src/api/src/zava_forward/api/web/ops.js:235 - eager work-order control rendering without bounded DOM strategy; historical RV-004, distinct UI/performance follow-up.
* src/api/src/zava_forward/api/web/ops.js:28 - free-text defect input lacks name/autocomplete; historical RV-005.
* src/api/src/zava_forward/api/web/ops.js:29 - free-text owner input lacks name/autocomplete; historical RV-005.
* src/api/src/zava_forward/api/web/ops.js:240 - free-text bindings input lacks name/autocomplete; historical RV-005.
* src/api/src/zava_forward/api/web/ops.js:248 - withdrawal has no confirmation/undo interaction; historical RV-006.

These are context observations, not a whole-application audit, fresh full accessibility assessment, Fluent acceptance or measured performance failure.

## Residual Work

* RV-001: nonblocking current-state summary clarification by the parent.
* P02-T02: authorized operational publication remains unperformed, not defective or prematurely complete.
* Full-gate, live-owner and historical UI follow-ups retain their separate boundaries above.

## Blockers and Remaining Work

* Review credibility: not blocked; authoritative source and evidence are sufficient despite RV-001.
* Full gate: Blocked by explicit prohibition. No valid current-candidate receipt or full-gate pass is claimed.
* Live owner acceptance: pending. No deployed result, hosted approval, issue closure or merge authorization follows from scoped checks.
* Parent continuation: consume this one original Review; record P02-T01 completion and correct current-state summary; then perform only the already authorized scoped P02-T02 publication, including honest PR gate qualification and exact-thread verification. Git writes were outside this Review and were not performed.

## Validation Evidence

| Check / evidence | Status | Assessment |
| --- | --- | --- |
| red-packages-csp-safe-attempt-1.log | Failed as expected, exit 1 supplied by caller | Real SQL/Chromium run; packages refresh fails first; old workorders 401; retry continuation settled, then stale capacity heading at final Sign in assertion. |
| red-workorders-attempt-1.log | Failed as expected, exit 1 supplied by caller | Opposite ordering independently reaches the same decisive post-finally stale-heading failure. |
| green-attempt-1.log | Passed, exit 0 supplied by caller | Owned SQL/Chromium; 980 generated cases, 443 open, 10 fictional staff; one package, 601 order identities; all 11 manager destinations, both new permutations and prior seeded/empty, failed-read/retry, transport/403, draft, cancellation and expiry scenarios. |
| focused-units.log | Passed | Log ends with Ran 82 tests in 41.996s / OK for test_procurement_api, test_auth and test_ui_support. Expected denial/law-store fixture diagnostics retained. |
| red-packages-attempt-16.log | Failed fixture, preserved | Capture timing failure, not production-red evidence. |
| red-packages-capture-barrier-attempt-28.log | Failed fixture, preserved | CSP rejects expression-string wait, not production-red evidence. Current function predicates resolve this without CSP bypass. |
| red-packages-attempt-1.log; capacity_401_validation.py; harness main | Assessed by inspection | Exact busy diagnostic; bounded 60-second retries; nonblocking shared lock before heavy work. No launcher/browser execution during Review. |
| node --check src/api/src/zava_forward/api/web/ops.js and app.js | Passed | Re-executed lightweight syntax checks during this Review. |
| git diff --check | Passed | Re-executed during this Review; no git writes. |
| API Ruff; strict isolated harness Ruff E/F/I/B/UP at 100 and format; API mypy | Passed in supplied implementation record and caller statement | Final API mypy covered 91 source files. No separate static-output log was supplied; not independently rerun or misrepresented as this reviewer's execution. |
| Current web guidelines | Passed retrieval / scoped assessment | Fresh complete rules source and changed-line assessment above; not live accessibility acceptance. |
| Browser/heavy tests during Review | Not run | Explicitly forbidden; actual earlier external evidence inspected instead. |
| az / complete local gate | Blocked / not run | Explicit prohibition; historical receipts cannot cover this changed candidate. |
| Publication and live acceptance | Pending / not run | P02-T02 and owner live verification are distinct future actions. |

Expected server BrokenPipe diagnostics in the browser logs are consistent with deliberate request cancellation. They are not hidden, and the harness's browser error collectors remain enabled and asserted empty. Exit codes above are corroborated by the supplied caller execution statement; individual redirected logs do not themselves contain process exit receipts.

## Outcome

* Review execution: Complete.
* Scoped source/regression outcome: Conformant.
* Full task outcome: Residual work.
* Rationale: deterministic red/green evidence and lifecycle inspection support the precise two-line correction and preserved prior behavior. RV-001 is a Low, nonblocking summary inconsistency. Publication is still pending; full-gate and live acceptance are not passed. None is silently promoted into source completion, approval or issue closure.

## Closeout Routing Record

| Finding class | Destination | Owner / next action |
| --- | --- | --- |
| Implementation defect | None | No rpi-implement source repair requested. |
| Decision gap or invalid assumption | None | No rpi-plan revision requested; PC-002 rejection justified at parent boundary. |
| Material evidence gap | None | No rpi-research continuation needed for the scoped verdict. |
| Nonblocking residual work | RV-001 distinct publication-evidence reconciliation; inherited UI/live follow-ups | Parent clarifies summary; existing specialist/owner routes remain unchanged. |

## Artifacts

| Path | Description |
| --- | --- |
| [.copilot-tracking/research/2026-10-28/capacity-page-523-delayed-401-research.md](.copilot-tracking/research/2026-10-28/capacity-page-523-delayed-401-research.md) | C1-C4 and research boundary |
| [.copilot-tracking/plans/2026-10-28/capacity-page-523-delayed-401-plan.md](.copilot-tracking/plans/2026-10-28/capacity-page-523-delayed-401-plan.md) | Current scope, markers and dependencies |
| [.copilot-tracking/details/2026-10-28/capacity-page-523-delayed-401-phase-details.md](.copilot-tracking/details/2026-10-28/capacity-page-523-delayed-401-phase-details.md) | Deterministic sequence and publication boundary |
| [.copilot-tracking/reviews/plans/2026-10-28/capacity-page-523-delayed-401-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-28/capacity-page-523-delayed-401-plan-critique.md) | Preserved original Revise |
| [.copilot-tracking/changes/2026-10-28/capacity-page-523-delayed-401-changes.md](.copilot-tracking/changes/2026-10-28/capacity-page-523-delayed-401-changes.md) | Implementation evidence and RV-001 location |
| [.copilot-tracking/rpi-sessions/2026-10-28/capacity-page-523-delayed-401-state.json](.copilot-tracking/rpi-sessions/2026-10-28/capacity-page-523-delayed-401-state.json) | Active-parent state at Review entry |
| [.copilot-tracking/reviews/logs/2026-10-28/capacity-page-523-delayed-401-review.md](.copilot-tracking/reviews/logs/2026-10-28/capacity-page-523-delayed-401-review.md) | This single original Review |
| [src/api/src/zava_forward/api/web/ops.js](src/api/src/zava_forward/api/web/ops.js) | Two-line production guard |
| [src/api/src/zava_forward/api/web/app.js](src/api/src/zava_forward/api/web/app.js) | Read-only lifecycle context |
| [src/api/checks/capacity_browser_check.py](src/api/checks/capacity_browser_check.py) | Regression, barriers and admission |
| [src/api/README.md](src/api/README.md) | Direct behavior and evidence limits |

## Next Steps

Active parent consumes this Review, clarifies RV-001 during evidence handoff, records P02-T01 completion and continues already authorized scoped P02-T02 when ready. Keep full gate Blocked, live owner acceptance pending and original failures/verdict intact. No second Review, new critique, source repair or user decision is requested.

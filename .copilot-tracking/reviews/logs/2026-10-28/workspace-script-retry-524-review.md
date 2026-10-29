<!-- markdownlint-disable-file -->
---
title: Workspace script retry implementation review
description: Original independent Review for issue 524
ms.date: 2026-10-28
---

# Review: workspace-script-retry-524

## Opening Review State

Task 524; date 2026-10-28. Assess the full task's stable candidate, preserving
explicitly incomplete P02-T01 validation. Compare research, plan, phase details,
original critique/dispositions, changes, app.js, unit/browser coverage and API
README. Read-only source boundary; write only this record. Initial blocker:
required API discovery and real-browser checks never started because the
mandated shared lock was occupied. Lightweight 32-test suite, package Ruff,
92-file mypy and 100-character new-Python line check passed. No live verification,
deployment, Azure, secrets, .env or private data. Do not equate missing evidence
with a passing criterion or rewrite original adverse evidence.

Acceptance basis: task requirements, AC1-AC5, additional safety requirements,
phase markers and direct PC-001-PC-003 dispositions. First compare the canonical
artifact set to the current source diff and persisted unit/browser checks.
Fresh web-design-guidelines source retrieved successfully on 2026-10-28 from
https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md
before inspecting changed web code. No delegation, heavy checks or lock access.

## Execution Status

* Review execution: Complete. One original independent source/evidence comparison
  completed on 2026-10-28; no implementation, delegation or second Review.
* Implementation execution: Partial, as recorded by the parent. P02-T01 remains
  incomplete. Complete comparison does not imply complete runtime validation.
* Outcome: Not accepted. RV-001 is a confirmed session-state defect; RV-002 is
  a regression-check defect; RV-003 is missing mandatory execution evidence.

## Scope and Evidence

Full issue #524 boundary: requirements, AC1-AC5, additional safety requirements,
P01/P02 markers, original critique and direct dispositions, implementation-time
decisions, validation, blockers, follow-up and publication limitations.

Compared canonical artifacts:

* .copilot-tracking/research/2026-10-28/workspace-script-retry-524-research.md
* .copilot-tracking/plans/2026-10-28/workspace-script-retry-524-plan.md
* .copilot-tracking/details/2026-10-28/workspace-script-retry-524-phase-details.md
* .copilot-tracking/reviews/plans/2026-10-28/workspace-script-retry-524-plan-critique.md
* .copilot-tracking/changes/2026-10-28/workspace-script-retry-524-changes.md
* Current diff: src/api/src/zava_forward/api/web/app.js and src/api/README.md
* New src/api/tests/test_workspace_scripts.py
* New src/api/checks/workspace_scripts_browser_check.py

Read directly relevant unchanged index.html, companion initialization, session
handling and synthetic browser-server lifecycle to assess the changed boundary.
Project context read: original case study, addendum context, reference index,
memory and housing-association primer. No claim to have reread every unrelated
section of the large addendum/index. Issue acceptance wording is supplied by the
canonical task artifacts and user; no fresh authenticated GitHub/live probe.
Observed branch: fix/workspace-script-retry-524. Existing implementation/evidence
changes were left in place. Only this opening Review record was modified.

## Plan-to-Change Reconciliation

| Current plan scope | Changes summary | Current-state reconciliation | Assessment |
| --- | --- | --- | --- |
| P01-T01 | Shared error-only retries and awaited readiness | Reconciled source intent | Session restoration defect RV-001 remains. |
| P01-T02 | Two regression files and API README | Files present; no extra executable targets | Late-delivery proof incomplete, RV-002. |
| P01 | Source/tests/documentation marked complete | Matches source-delivery interpretation | Not runtime acceptance; details' browser completion evidence is still unavailable. |
| P02-T01 / P02 | Unchecked; API discovery and Chromium blocked | Consistent across plan/details/changes/handoff | RV-003; do not mark complete. |
| P02-T02 | Reconciled once-only Review handoff | Complete for handoff | Publication instructions remain future gates, not completed work. |
| Follow-Up Items | Live response/cold-start/auth and post-deploy verification | Mirrored in changes and README | Distinct owner follow-up RV-004; not a new active phase. |

No material undocumented implementation-time scope change was identified.
Research question table Q1-Q3 still says Open, but its later stable headings
explicitly answer Q1/Q3 and qualify Q2 as unresolved live cause. This stale
summary does not prevent identifying the evidence boundary or establish live
resolution. Source completion and validation completion are explicitly distinct.

## Completed Work Assessment

| Requirement | Source/evidence comparison | Assessment |
| --- | --- | --- |
| AC1 | Research C1/C3 records synchronous script order, whole-file reads, MIME, length and no-store source; uncertainty and authenticated/cold-start/auth omissions remain explicit. | Met as an unresolved-cause record, not a live diagnosis. Browser HTTP assertions have not run. |
| AC2 | app.js:145-169,188-199 await retry promises, then recheck expected globals before dispatch. Browser recovery scenarios use real bytes, a map/specialist screen and one document request. | Credible source mechanism; actual browser recovery unproven, RV-003. |
| AC3 | app.js:196-199,246-252 retain exact original error text, alert and native Reload workspace button. Cached errors allow at most two retry insertions. | Source preserved; actual exhaustion, keyboard action and focus assertion unexecuted. |
| AC4 | Both regression files persist. Parent reports lightweight tests passed. Browser check source exists but Chromium never executed. | Not met in full, RV-003. Check-quality limitation RV-002 also applies. |
| AC5 | Plan Follow-Up Items, changes and README explicitly defer live post-deploy checks to owner. | Met as explicit pending-owner disposition, not deployment acceptance. |
| Predicates and order | Extracted missingWorkspaceScripts preserves all seven original role/route conditions and their missing-path/error-message order. Tests cover staff case, capacity, finance, assistants, time, screens, overview/coordinator, contractor and independent route. | Source comparison passes. Query behavior is unchanged, including exact equality for capacity/finance/time/overview. |
| Script evaluation order | Initial HTML synchronous order is unchanged. Missing paths retry concurrently through Promise.all, rather than recreating HTML execution order. | Current companion top-level constants do not eagerly depend on each other; cross-script calls occur in functions after aggregate readiness. No demonstrated order defect in this source set. Not a general dependency-order guarantee. |
| Shared budget | One page-lifetime Map entry per fixed same-origin path retains pending and settled promises; route revisits do not reset it. | Source/Node coverage supports two retries beyond initial HTML request, shared concurrently across routes. |
| Readiness/error-only retries | Only onerror continues the loop. Load, including load without sentinel, stops; final predicates decide readiness. | Matches final safe policy. A 200 response is not accepted as readiness. Unused budget after load-without-global is intentional. |
| Terminal timeout | Five-second timer; 250/500ms delays; settlement clears timer/handlers and removes tag. Timeout never starts a second attempt for that path. | Prevents overlapping timeout reinjection. Does not claim tag removal cancels execution. Late execution itself remains browser-unverified. |
| Healthy dependencies | Only currently missing paths enter retry recovery. | No unconditional reload; Node regression explicitly covers healthy Leaflet. |
| Stale route | New route aborts old signal; post-await throwIfAborted precedes status restoration/view dispatch; catch suppresses aborted-route errors. | Navigation isolation supported by source and Node assertions. |
| Stale session | requireWorkspaceScripts returns normally when me becomes null; route checks only its signal, not session readiness. | RV-001: restoring stale status and invoking screens view is possible without an abort. |
| Status restoration | Recovery writes polite loading text; current successful route restores captured role/scope; terminal failure writes actionable status. | Correct for current authenticated route; incomplete for session invalidation, RV-001. |
| Native controls/content | No HTML/CSS redesign, new custom controls, colour-only signal, changed terminal wording or new dependency. | Source passes preserved semantics; full accessibility/browser acceptance not established. |
| Change budget/docs | app.js, API README and exactly two approved new executable files; no removals. README accurately describes bounds and live uncertainty. | Within scope. Its unconditional obsolete-screen assurance needs the session limitation fixed through RV-001. |

## Implementation-Time Plan and Detail Update Assessment

| Area | Decision and triggering evidence | Current-state reconciliation | Assessment |
| --- | --- | --- | --- |
| P01-T01 / PC-001 | Classic scripts with lexical bindings can execute after tag removal; timeout becomes terminal. | Plan, details, source, unit check and browser scenario agree. | Supported safety correction within confirmed intent; execution evidence still missing. |
| P01-T01 / PC-002 | A loaded but incomplete script may install lexical bindings; reject advice to reinject after load without sentinel. | Final plan/details explicitly retain post-load global check and terminal cached outcome; tests use this policy. | Justified direct disposition, not an unexplained implementation deviation. |
| P02 / PC-003 | Parent/user authorize their task venv and required shared lock under /tmp. | Plan rejects critique worker's context-specific prohibition as inapplicable. | Accepted rejection; no unresolved parent policy conflict and no alternate lock required. |
| P02 handoff | Nonblocking lock acquisition failed before heavy commands started. | Unchecked markers and Partial implementation status preserved throughout. | Correct incomplete-evidence handoff; not a waiver of required validation. |

## Critique and Material Revision Assessment

The original critique remains Complete / Revise, with its original 1 High and
2 Medium findings intact. This Review neither changes that verdict nor claims
it was retrospectively passed.

* PC-001: Applied directly. Terminal timeout removes the overlap mechanism
  challenged by the original critique. Browser scenario now withholds a lexical
  companion past timeout. Its runtime proof remains unavailable and its
  deterministic late-settlement assertions need RV-002.
* PC-002: Partially applied; unsafe retry advice explicitly rejected. Global
  readiness is still checked, but loaded-without-global is terminal. Conservative
  failure is justified by lexical redeclaration risk; not a recovery-success claim.
* PC-003: Rejected as inapplicable to the parent's authorized execution context.
  The prohibition cited by that worker is not an unresolved parent constraint.
  Actual lock contention is a separate observed resource blocker, RV-003.
* These are recorded final planning dispositions before the stable implementation,
  not unreviewed significant product changes. No unsupported dependent-work
  resumption or new unresolved owner design choice was identified. No second
  critique is requested.

## Plan Follow-Up Assessment

| Follow-up | Why outside immediate implementation | Owner/next action | Route |
| --- | --- | --- | --- |
| Historical authenticated response, cold-start/auth correlation and post-deploy verification | Historical/live evidence cannot be inferred from local source or synthetic traffic; deployment/authenticated inspection are outside this task's authorization. | Owner arranges authorized capture and separately approved deployment verification. | RV-004, distinct live follow-up; preserve pending status and Refs #524. |

## Web Interface Guidelines

Fresh source successfully retrieved before changed web-code inspection:
https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md
(2026-10-28). Reviewed the entire app.js diff against the fetched rules, with
unchanged semantic/focus context where needed. Repository requirements to preserve
existing plain-language copy/native controls take precedence over generic copy
styling suggestions. New forms, media, animation, styling, hydration, locale
formatting and responsive-layout changes are absent, so those rule groups add
no changed-code finding.

### src/api/src/zava_forward/api/web/app.js

src/api/src/zava_forward/api/web/app.js:229 - stale role/scope status can overwrite
the cleared sign-in status after session invalidation; RV-001.

src/api/src/zava_forward/api/web/app.js:191 - pass: asynchronous recovery uses the
existing polite status region, with a specific non-colour loading message.

src/api/src/zava_forward/api/web/app.js:246-252 - pass: terminal error preserves
heading, alert, actionable copy and a native keyboard-operable button.

These are source findings, not fresh Chromium, assistive-technology, WCAG or
whole-application conformance evidence. Existing unrelated UI patterns were not
silently brought into scope.

## Findings

<!-- rpi:review id=RV-001 -->
### RV-001 [Medium]: Session invalidation does not guard post-recovery status or view dispatch

* Class: Implementation defect.
* Scope: P01-T01; stale-session and status-restoration requirements.
* Evidence: src/api/src/zava_forward/api/web/app.js:193 returns normally if me is
  null. app.js:227-230 then checks only signal.aborted, restores routeStatus and
  can call roleScreensView. The actual 401/login path at app.js:35,52-53 clears me
  and status but does not abort routeController. Sign-out also does not perform
  the abort assumed by the new Node test.
* Reproduction: Two read-only inline Node VM probes extracted the actual loader
  and route source. While a retry completed, each probe set me=null and cleared
  workspaceStatus without aborting the route, modelling that session transition.
  Overview output was {"me":null,"statusAfterSessionEnded":"Retrofit Programme
  Manager. Case workspace."}. A screens probe installed a spy as the recovered
  expected global and returned viewsAfterSessionEnd=1 with the same stale status.
  The spy demonstrates dispatch, not successful rendering of an authenticated
  real view or an authorization bypass.
* Impact: A signed-out/session-ended document can announce stale authenticated
  context and attempt view dispatch. Real roleScreensView dereferences me;
  suppression by the catch does not satisfy the requirement to avoid invocation
  and does not undo the already restored status.
* Test gap: src/api/tests/test_workspace_scripts.py:151-156 manually aborts the
  controller, unlike the actual session-invalidating path. Browser sign-out
  navigates away before releasing/aborting the pending request, so it does not
  exercise this same-document session-ended transition.
* Destination: rpi-implement.
* Smallest useful next action: Guard current session as well as current route
  before any post-await status/view update. Add a regression that clears the
  session without an artificial abort and verifies no status restoration or view
  call; cover actual 401/login behavior using constructed fixtures.

<!-- rpi:review id=RV-002 -->
### RV-002 [Medium]: Late-delivery browser proof relies on elapsed time and omits its promised evaluation/status assertions

* Class: Regression-check defect, not an observed browser runtime failure.
* Scope: P01-T02, PC-001 direct disposition and delayed lexical delivery.
* Evidence: src/api/checks/workspace_scripts_browser_check.py:169-185 continues
  the timed-out request and sleeps 300ms. It never waits for a response/evaluation
  sentinel or counts actual companion evaluations. The pre-revisit status
  assertion excludes only "unavailable", allowing stale loading or role text.
  Revisiting screens then overwrites status, hiding such stale updates.
  Details P01-T02 explicitly promises one evaluation and no stale view/error/
  progress after releasing the late response.
* Impact: A slow but valid late response can make the check revisit before
  readiness and fail for timing rather than the contract. Conversely, an
  incorrect late progress update is not detected. Request count and absence of
  pageerror are useful but do not alone prove all promised late-settlement facts.
* Destination: rpi-implement.
* Smallest useful next action: Observe a deterministic real-script evaluation/
  settlement event with a bounded wait, measure evaluations without replacing
  the real companion source, and compare the current independent route/status
  before and after settlement. Explicitly prove the safe disposition if the
  browser cancels execution instead of assuming removal guarantees cancellation.
  Keep the existing request-budget and actual-view assertions.

<!-- rpi:review id=RV-003 -->
### RV-003 [High]: Mandatory API discovery and real-browser acceptance evidence is unavailable

* Class: Material evidence gap; not a failing test or an inferred source defect.
* Scope: P02-T01, AC2-AC4 and publication readiness.
* Evidence: Plan P02/P02-T01 remain unchecked; changes Validation Record and phase
  details say nonblocking flock failed because another process held the shared
  resource. Full API discovery and Chromium never started. No browser output
  exists to establish actual script execution, map recovery, native keyboard
  reload, local HTTP assertions or late-delivery behavior.
* Impact: Passing lightweight checks cannot establish the required browser
  recovery acceptance or full API regression boundary. A Conformant verdict and
  publication-readiness claim are unsupported.
* Destination: rpi-research, bounded missing execution-evidence collection.
* Smallest useful next action: Parent schedules the required API discovery and
  real Chromium fault-injection check only when its authorized nonblocking
  shared-lock acquisition succeeds. Preserve original non-execution evidence,
  record actual outputs, and reconcile P02 honestly. Do not bypass, substitute
  locks, wait in this Review, or relabel contention as a test pass. Later source
  corrections must be covered by subsequent validation evidence.

<!-- rpi:review id=RV-004 -->
### RV-004 [Low]: Historical live diagnosis and post-deployment verification remain owner-pending

* Class: Non-blocking residual live work, not an implementation defect.
* Scope: Existing plan Follow-Up Items, AC1 and AC5.
* Evidence: Research Open Questions and C1/C3, plan Follow-Up Items, changes
  Follow-Up Items and src/api/README.md all distinguish inspected source from
  missing authenticated live response/cold-start/auth evidence and deployment.
* Impact: The local retry change cannot identify the original transport cause
  or certify behavior on the deployed authenticated path.
* Destination: Distinct owner live-verification follow-up, not active P01/P02.
* Smallest useful next action: Owner obtains authorized failed response
  status/size/headers and telemetry correlation, then verifies after separately
  approved deployment. Retain owner-pending wording and use Refs #524 rather
  than implying all live criteria are closed.

## Defects and Routed Findings

| Finding | Severity | Destination | Action owner |
| --- | --- | --- | --- |
| RV-001 | Medium | rpi-implement | Parent schedules session-guard fix and realistic regression. |
| RV-002 | Medium | rpi-implement | Parent schedules deterministic late-delivery proof within existing browser file. |
| RV-003 | High | rpi-research | Parent collects missing mandatory execution evidence when shared resource is available. |
| RV-004 | Low | Distinct live follow-up | Owner arranges authorized capture and post-deploy verification. |

No unresolved significant decision gap requires rpi-plan. These routes do not
authorize fixes during this Review or create another Review requirement.

## Validation Evidence

| Check | Status | Evidence boundary |
| --- | --- | --- |
| node --check src/api/src/zava_forward/api/web/app.js | Passed, parent-reported | Syntax only; not rerun by reviewer. |
| test_workspace_scripts, test_role_screens, test_workbench, test_design_system, test_content_standard, test_accessibility_baseline | Passed, parent-reported | 32 unittest tests in 0.265s; not full API discovery. |
| Package-wide Ruff | Passed, parent-reported | Existing package configuration; no waiver. |
| Package-wide mypy | Passed, parent-reported | 92 source files; changes preserves earlier listener correction. |
| Explicit new-Python line limit | Passed, parent-reported | Both new files <=100 characters per line. |
| Full API unittest discovery | Unavailable; never executed | Shared nonblocking lock acquisition failed before command start. |
| Real Chromium workspace fault injection | Unavailable; never executed | Same contention; source inspection is not execution evidence. |
| Browser local HTTP status/bytes/headers | Unavailable | Assertions exist but never ran; source serving inspection only. |
| Fresh web-design-guidelines retrieval and changed-web source comparison | Completed by reviewer | Retrieval succeeded; findings/pass entries above. |
| Two inline Node session-invalidating probes | Executed by reviewer; defect reproduced | Actual extracted source, constructed VM fixtures; stale status and screens dispatch without session. Not a full browser/session reproduction. |
| Complete local exact-head gate and receipt verification | Unexecuted future prerequisite | No gate receipt or publication readiness inferred. |
| Authenticated live diagnosis/post-deploy verification | Owner-pending | No Azure, credentials, .env, private data or deployment used. |

The supplied passing checks are retained as actual parent evidence, not claimed
as reviewer reruns. Reviewer performed no heavy command and never accessed the
shared lock. The initial corrected mypy issue remains historical evidence;
it is not a current unresolved defect.

## Blockers, Residual Work and Outcome

* Review execution: Complete for the supplied stable source/evidence boundary.
* Implementation execution: Partial; mandatory P02-T01 validation remains blocked
  by shared resource contention.
* Outcome: Not accepted. Two Medium implementation/check defects and a High
  mandatory evidence gap prevent acceptance. Severity summary: 0 Critical,
  1 High, 2 Medium, 1 Low residual item.
* Live owner work is explicitly residual and does not invalidate AC1/AC5's
  permitted unresolved/pending record. It is not recast as a source defect.
* Remaining publication prerequisites: corrected candidate validation where
  authorized, committed dated original evidence, complete exact-head gate and
  external receipt verification, independent exact-head assessment and hosted/
  human gates as applicable. No commit, push or PR action occurred here.
* This is exactly one original Review. Preserve this outcome and original
  critique; later work must not rewrite them as passed or create a correction
  Review loop.

## Closeout Routing Record

| Finding class | Destination | Next action |
| --- | --- | --- |
| Implementation/check defects | rpi-implement | RV-001/RV-002, only in a later authorized invocation. |
| Significant decision gaps | None | Direct critique dispositions preserve confirmed intent. |
| Material evidence gap | rpi-research | RV-003, collect actual required execution evidence when available. |
| Non-blocking residual work | Owner live follow-up | RV-004, preserve pending live boundary. |

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/research/2026-10-28/workspace-script-retry-524-research.md](.copilot-tracking/research/2026-10-28/workspace-script-retry-524-research.md) | Research and live uncertainty |
| [.copilot-tracking/plans/2026-10-28/workspace-script-retry-524-plan.md](.copilot-tracking/plans/2026-10-28/workspace-script-retry-524-plan.md) | Requirements, AC and direct dispositions |
| [.copilot-tracking/details/2026-10-28/workspace-script-retry-524-phase-details.md](.copilot-tracking/details/2026-10-28/workspace-script-retry-524-phase-details.md) | Phase contracts and validation ownership |
| [.copilot-tracking/reviews/plans/2026-10-28/workspace-script-retry-524-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-28/workspace-script-retry-524-plan-critique.md) | Preserved original Revise critique |
| [.copilot-tracking/changes/2026-10-28/workspace-script-retry-524-changes.md](.copilot-tracking/changes/2026-10-28/workspace-script-retry-524-changes.md) | Partial implementation and validation record |
| [src/api/src/zava_forward/api/web/app.js](src/api/src/zava_forward/api/web/app.js) | Changed recovery and route logic |
| [src/api/tests/test_workspace_scripts.py](src/api/tests/test_workspace_scripts.py) | Persisted Node VM regression |
| [src/api/checks/workspace_scripts_browser_check.py](src/api/checks/workspace_scripts_browser_check.py) | Unexecuted browser fault-injection source |
| [src/api/README.md](src/api/README.md) | Recovery bounds and live limitations |
| [.copilot-tracking/reviews/logs/2026-10-28/workspace-script-retry-524-review.md](.copilot-tracking/reviews/logs/2026-10-28/workspace-script-retry-524-review.md) | This one original Review |

## Next Steps

Return this Complete / Not accepted Review to the active parent. Parent owns
later rpi-implement routing for RV-001/RV-002, bounded rpi-research execution
evidence collection for RV-003, and the distinct owner follow-up RV-004.
No fixes, heavy validation, lock access, second Review or publication are
authorized by this assessment. Preserve the current original outcome.

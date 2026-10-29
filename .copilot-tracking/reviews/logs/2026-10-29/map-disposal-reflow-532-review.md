---
title: Map disposal and large-font reflow independent RPI Review
description: One bounded post-implementation review for issue 532 and PR 539
ms.date: 2026-10-29
---

## Scope and Evidence

* Task ID: issue-532-pr-539-map-disposal-reflow.
* Scope: the five supplied changed files and the matching dated research, plan, details, critique and changes artifacts.
* Acceptance basis: reject pending successful map fits after 401 disposal, preserve forced-collapse drawing, and preserve useful expanded map geometry at 640px with the real Blink 32px default font.

## Opening Review State

* Interpreted goal: independently compare the implementation and regression helper with approved intent without repairing or repeating Review.
* Evidence readiness: matching artifact paths supplied; five-file working-tree diff available on feat/map-fullscreen-532. Detailed comparison pending.
* First comparison boundary: reconcile plan markers, critique dispositions and recorded validation, then inspect the complete five-file diff and directly relevant map code.
* Active read-only boundaries: only this review record may be written; no source, plan, details, research, critique or changes edits; no nested agents.
* Initial blockers: heavy nonblocking lock admission returned 75 with holder PID 661156; no retry, polling, browser or full-suite execution permitted. Targeted results are supplied evidence, not fresh reviewer runs. Full map browser execution and pre-fix negative controls are unperformed.
* Web review source: freshly retrieved https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md on 2026-10-29; apply only to changed map web boundary.

## Execution Status

* Execution status: Partial.
* One independent Review completed against the available diff and matching artifacts. The implementation and validation plan remains partially executed: P01 is complete, P02 browser execution and negative controls are unperformed.
* No nested agent, browser, full suite, lock admission retry, lock polling, remote operation, source repair or second Review was performed.

## Plan-to-Change Reconciliation

| Current plan scope | Changes-record summary | Current-state reconciliation | Gap or rationale |
| --- | --- | --- | --- |
| P01 / P01-T01 | Disposal and sizing corrections | Reconciled | Exact requested source corrections and disposal-local source contracts are present. |
| P02-T01 | Browser coverage, validation pending | Partial | Exactly two helpers and README changes are present; runtime and negative controls are not established. RV-001. |
| P02-T02 | Validation record and pre-review reconciliation | Partial | Supplied strict checks and 43 focused tests passed; browser/full discovery unavailable; this one Review is now recorded; local commit belongs to parent continuation. |
| Follow-Up Items | Later coordinated validation | Reconciled, open | Explicit heavy-lock coordination is required. Preserve unchecked P02 markers and do not infer acceptance from the fallback. |

The changes record's opening Execution Status still describes the initial
pending-check state. Its later Validation Record, Pre-Review Reconciliation,
plan markers and details clearly identify the current partial state; the
opening is not evidence that the later recorded checks failed to execute.
No completion claim is inferred from that opening or from this Review.

## Completed Work Assessment

| Related marker | Files | What changed and why | Completion evidence | Validation | Assessment |
| --- | --- | --- | --- | --- | --- |
| P01-T01 | src/api/src/zava_forward/api/web/app.js | Increment seq after collapse(false), before dialog/map removal and nulling | Actual diff and surrounding success/catch guards | Source contracts reported passing | Correct static placement; catches draws started synchronously by collapse resize, without changing route-abort or login behavior. |
| P01-T01 | src/api/src/zava_forward/api/web/style.css | Desktop sidebar becomes min(19rem,45%) | Actual diff; existing min-width:0, minmax map track and narrow breakpoint retained | Source contract reported passing | Matches approved fix; preserves the 19rem ceiling and existing 600px rule. Runtime geometry not established. |
| P01-T01 | src/api/tests/test_map_fullscreen.py | Existing methods assert the capped track and disposal-local ordered operations | Extracted dispose closure and increasing operation positions | Included in supplied 33 focused API tests | Rejects missing or pre-collapse increment without adding unit methods. Not browser evidence. |
| P02-T01 | src/api/checks/map_fullscreen_browser_check.py | Controlled stale responses and isolated enlarged-font helper | Actual diff; exactly two added helpers | Strict checks reported passing; helper runtime unavailable | Credible bounded instrumentation; runtime sensitivity remains unverified, RV-001. |
| P02-T01 | src/api/README.md | Describe intended race and font regression coverage | Actual diff | Manual consistency review | Describes what the check is intended to exercise, not a dated execution receipt. Changes record correctly discloses that execution is unperformed. |

### Disposal helper assessment

* Real Overview area change handlers issue the two fit requests. DOM dispatch is appropriate for the inert background in expanded mode; no production test hook is introduced.
* Sequential request expectations, route-handler count handshakes and the no-bbox assertion establish two pending externally invoked fit draws before disposal. The second route fetches the real constructed API response and asserts successful status and nonempty bounds, rather than fabricating a boundless success.
* The earlier 401 takes the real api/login path. Captured signals are the actual signal arguments forwarded by api to fetch; the post-disposal live-signal check distinguishes sequence invalidation from route abortion. Capturing at the api boundary is adequate here because the inspected api forwards that signal unchanged.
* Returned panel.draw Promises are genuinely observed for fulfillment and rejection. This is stronger than requestfinished, but does not directly observe internal draw(false) calls. For those calls, captured api settlement plus the two-frame drain is credible in the inspected implementation: after the single awaited api call, draw's response processing is synchronous. Any unhandled internal rejection is additionally subject to the enclosing pageerror listener and final assertion. Do not equate state.draws with every internal draw Promise.
* Expanded mode forces a real Leaflet moveend during collapse, retaining its additional request and releasing it after login. Fit/clear counters detect late map mutations. The third request is inferred to be viewport draw(false) from inspected code; the helper does not explicitly assert its bbox.
* The initialization wait does not directly await an initial internal viewport network request. However, the two controlled fit calls synchronously advance seq, making any older viewport response stale; the internal draw(false) response cannot fit or recursively schedule another draw. This is not sufficient evidence of a helper defect. Actual scheduling and negative-control sensitivity still need RV-001's runtime follow-up.
* Route interception is removed in finally; results are persisted there. Held-route failures ultimately terminate with the enclosing browser.close. Prototype/global instrumentation belongs to a document replaced by the next page.goto, so it does not leak between the two modes or to the separate font browser.

### Enlarged-font helper assessment

* Launches its own Chromium with --blink-settings=defaultFontSize=32 before context creation, checks an unstyled document, and checks the real root font before navigation into the map. This does not substitute author CSS for a browser preference.
* Supplied evidence confirms only the tiny unstyled-font probe. It does not confirm the real application root, marker interaction or expanded geometry.
* At a 640 CSS-pixel viewport, code measures document, dialog, workspace, sidebar and map; checks scroll/client widths, sidebar <=45% plus rounding tolerance, and map width >80px. It exercises selected summary close/focus restoration and expanded exit/focus restoration.
* Separate browser finally cleanup isolates the preference. Loopback-only routing, integrity-pinned existing axe and screenshots are retained. The scan occurs after closing the selected summary, so it must not be presented as an axe scan of the open enlarged-font summary.
* No runtime geometry, screenshot, axe result, existing normal-font regression pass or pre-fix CSS failure is available for this candidate.

## Implementation-Time Plan and Detail Update Assessment

| Affected area | What changed and why | Triggering evidence and user decision | Reconciliation | Planning and critique state | Assessment |
| --- | --- | --- | --- | --- | --- |
| P02-T01 | Specify Promise capture, request identity, forced collapse draw and Blink font setup | PC-001 / PC-002; approved exact source fixes unchanged | Plan disposition and detailed protocol updated | One original Revise critique preserved | No divergent product decision; explicit fit Promise settlement plus internal-api/frame drain is statically credible, execution remains RV-001. |
| P02-T02 | Use targeted fallback and leave browser/full gates open | Nonblocking admission returned 75, holder PID 661156; user explicitly permits fallback | Plan, details and changes describe partial validation | No fresh critique required for the authorized fallback | Supported; no retry or false pass is warranted. |
| P02-T02 / PC-003 | Reject the critique worker's environment restriction as a parent blocker | Parent supplies successful authorized package install and font probe under its lock | Original critique preserved; rejection recorded | Worker-specific restriction is not inherited evidence about parent tools | Rejection is justified for the parent context; this reviewer does not access or modify that external environment. |

The requested source solution, five-file scope and two-helper ceiling did not
diverge materially. No additional product choice, dependency, auth redesign or
manifest-pin change is introduced. Later helper handshake changes fit the
approved protocol; typed checks do not prove that protocol runs correctly.

## Critique and Material Revision Assessment

* PC-001: applied to request identity, real fit Promise observation, inert-background dispatch and disposal-local source ordering. Internal initialization/collapse draws are not included in the returned-property Promise observer; their current synchronous post-api continuation is covered indirectly by the api/frame drain and outer pageerror assertion. Static mechanism is credible; executed proof remains unavailable under RV-001.
* PC-002: mechanism and cleanup are specified and implemented. The supplied unstyled 32px probe supports mechanism feasibility; real-app geometry and original-CSS failure remain unperformed under RV-001.
* PC-003: preserve the original High finding and Revise outcome. Its restriction described the critique worker's execution context. The supplied successful parent package install and font probe are concrete contrary evidence to treating that restriction as a parent-wide prohibition. Rejecting that premise does not waive lock admission or missing validation.
* Dependent-work pause: supplied artifacts record direct dispositions before implementation. Nothing in the diff indicates a divergent choice resumed without user approval.
* Material revision readiness: source intent remains approved and static assessment is credible. Browser acceptance is not ready; no conformant verdict follows from planning readiness.

## Plan Follow-Up Assessment

| Follow-up item | Why outside immediate continuation | Owner or next action | Assessment and route |
| --- | --- | --- | --- |
| Full API/core units, map browser and separate pre-fix asset controls | Heavy-lock denial; user permits targeted fallback and prohibits another admission attempt now | Parent records a distinct validation follow-up; authorized executor coordinates a later admission event | Open, RV-001. Not a new source defect, not a second Review and not authority to mark P02 complete. |

## Scoped Web Guidelines Review

Fresh source retrieved successfully for this Review. All fetched categories were
considered against the two changed map web lines and directly relevant context;
unaffected forms, navigation, copy and general application behavior were not
audited. Existing native dialog/button/link semantics, keyboard/manual paths,
focus behavior, non-colour symbols, no-animation settings, safe-area padding,
min-width constraints and contained sidebar scrolling remain intact.

### src/api/src/zava_forward/api/web/app.js

* Pass: changed disposal sequence introduces no scoped guideline violation.

### src/api/src/zava_forward/api/web/style.css

* Pass: changed desktop track addresses overflow at its source using CSS grid; no scoped static guideline violation found.

These are static changed-boundary passes, not a fresh browser, accessibility
conformance or whole-app acceptance claim. Actual overflow/focus geometry remains
unverified under RV-001.

## Findings

<!-- rpi:review id=RV-001 -->
### RV-001 [Medium]: Browser acceptance and defect-specific controls remain unperformed

* Related scope: P02-T01, P02-T02, PC-001 / PC-002 and the existing plan follow-up.
* Evidence: plan leaves P02, P02-T01 and P02-T02 unchecked; details Current Completion and Review Boundary and changes Validation Record identify admission exit 75 with holder PID 661156. The supplied task explicitly confirms no full map browser/new-helper execution or pre-fix asset negative control ran. Only the tiny unstyled font probe ran.
* Impact: real draw ordering, actual app 32px inheritance/geometry, preserved existing browser journeys and defect-specific red/green attribution are unestablished. Static/unit checks cannot establish these browser acceptance criteria. In particular, indirect completion of internal viewport draws and the actual collapse-request ordering have not been demonstrated by helper execution. This is missing execution evidence under an authorized fallback, not an observed production or helper failure.
* Destination: distinct follow-up item, coordinated local validation owned by the parent and an authorized executor. No second Review and no immediate lock retry.
* Smallest useful next action: preserve all original evidence and unchecked P02 markers; at a later explicit lock-coordination event run full API/core units, corrected map browser, original-JS/corrected-CSS disposal control and corrected-JS/original-CSS reflow control. Record actual defect-specific failures or unexpected failures honestly, plus corrected results. Local commits, hosted/human approval and publication remain separate.

## Defects

* No independently established defect in the two production corrections or new helper implementation. Runtime sensitivity remains unverified rather than presumed correct or defective.

## Routed Findings

| Finding | Destination | Owner or next action | Reason |
| --- | --- | --- | --- |
| RV-001 | Distinct coordinated-validation follow-up | Parent / authorized local executor | Missing runtime and negative-control evidence; no rerun of Review. |

Later implementation of a routed finding does not require another Review.

## Residual Work

* Keep full-suite/browser/negative-control follow-up separate from this completed one-pass assessment. Neither fallback success nor a local commit completes it.
* Parent owns remaining local-only commit work. No push, az, force-push, issue-closing instruction or publication gate is authorized by this record.

## Blockers and Remaining Work

* Browser and full discovery are unavailable after the disclosed lock denial. Do not retry, poll or inspect another holder's outputs.
* P02-T01 remains implemented but not fully verified, with RV-001 open. P02-T02 remains partial, including parent-owned local commit and distinct validation follow-up.
* No unresolved divergent product decision or additional research question was established. No route to rpi-plan or rpi-research is needed.

## Validation Evidence

| Command or evidence | Scope | Status | Summary |
| --- | --- | --- | --- |
| API mypy; ruff check .; ruff format --check . | API source/checks | Passed, supplied implementation record | 101 mypy source files; 53 format files. Not independently rerun. |
| Core mypy; ruff check .; ruff format --check . | Core | Passed, supplied implementation record | 156 mypy source files; 103 format files. Not independently rerun. |
| Focused API unittest modules named in changes | API contracts and adjacent UI | Passed, supplied implementation record | 33 tests, no skips; existing synthetic law-store warnings disclosed. |
| Focused core test_dependency_rule and test_scenario_manifest | Core and pins | Passed, supplied implementation record | 10 tests, no skips; no planned input requires pin refresh. |
| node --check src/api/src/zava_forward/api/web/app.js | JavaScript syntax | Passed, supplied implementation record | Syntax only, not map runtime. |
| Package-origin probe | API/core/agents imports | Passed, supplied task evidence | Current worktree origins, not another checkout. |
| Required editable package install under acquired lock | Parent environment | Passed, supplied task evidence | Supports parent rejection of PC-003; no reviewer environment mutation. |
| Isolated unstyled Chromium default-font probe | Blink 32px setting | Passed, supplied task evidence | Tiny probe only; not either new helper or app layout. |
| Heavy nonblocking admission | Full validation | Unavailable | Exit 75, actual holder PID 661156; chained browser/full checks did not execute. |
| Full API/core unit discovery | Packages | Skipped | Lock contention; targeted fallback explicitly authorized. |
| New helpers and existing map browser journeys | Real constructed app | Skipped | No browser execution permitted in this Review. |
| Separate pre-fix JS and CSS asset negative controls | Defect-specific sensitivity | Skipped | Never executed; no red/green result inferred. |
| Fresh Web Interface Guidelines retrieval and scoped static comparison | Changed map web boundary | Passed | Retrieved and assessed during this Review; no browser/conformance claim. |
| git diff --check | Existing five-file diff and review file as applicable | Passed, reviewer command | Whitespace check only; untracked review content separately inspected. |

The reviewer did not access the supplied external logs or shared environment.
Implementation command results above are attributed to the supplied artifacts
and task evidence, not fresh reviewer execution. No failure output, timeout or
empty log is represented as a passing browser control.

## Outcome

* Outcome: Residual work.
* Rationale: the exact requested production corrections and bounded regression instrumentation are statically credible, with no confirmed implementation defect. RV-001 leaves required browser acceptance unestablished. Partial execution under the user-authorized fallback is honest progress, not conformant acceptance.
* Severity summary: 0 Critical, 0 High, 1 Medium, 0 Low. One distinct runtime-evidence follow-up; no confirmed production or helper defect.

## Closeout Routing Record

| Finding class | Destination | Owner or next action |
| --- | --- | --- |
| Implementation defect | None | No source repair recommended on current evidence. |
| Decision gap or invalid assumption | None | No divergent product choice found; parent PC-003 rejection supported. |
| Material research gap | None | Runtime evidence is assigned to the existing distinct validation follow-up, not a new research cycle. |
| Runtime evidence / residual work | Coordinated validation follow-up, RV-001 | Parent / authorized executor after explicit lock coordination. |

* Execution status: Partial.
* Outcome: Residual work.
* Validation coverage: supplied strict checks and 43 focused tests passed; one tiny font probe passed; new helpers, full browser, full units and negative controls unperformed.
* Blockers: heavy-lock denial; unchecked P02 acceptance remains open.
* This is the single original post-implementation Review for this artifact set.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/research/2026-10-29/map-disposal-reflow-532-research.md](.copilot-tracking/research/2026-10-29/map-disposal-reflow-532-research.md) | Research |
| [.copilot-tracking/plans/2026-10-29/map-disposal-reflow-532-plan.md](.copilot-tracking/plans/2026-10-29/map-disposal-reflow-532-plan.md) | Current plan |
| [.copilot-tracking/details/2026-10-29/map-disposal-reflow-532-phase-details.md](.copilot-tracking/details/2026-10-29/map-disposal-reflow-532-phase-details.md) | Phase details |
| [.copilot-tracking/reviews/plans/2026-10-29/map-disposal-reflow-532-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-29/map-disposal-reflow-532-plan-critique.md) | Preserved original critique |
| [.copilot-tracking/changes/2026-10-29/map-disposal-reflow-532-changes.md](.copilot-tracking/changes/2026-10-29/map-disposal-reflow-532-changes.md) | Implementation and supplied validation |
| [.copilot-tracking/reviews/logs/2026-10-29/map-disposal-reflow-532-review.md](.copilot-tracking/reviews/logs/2026-10-29/map-disposal-reflow-532-review.md) | Single independent Review |
| [src/api/src/zava_forward/api/web/app.js](src/api/src/zava_forward/api/web/app.js) | Disposal correction and draw lifecycle |
| [src/api/src/zava_forward/api/web/style.css](src/api/src/zava_forward/api/web/style.css) | Expanded grid correction |
| [src/api/checks/map_fullscreen_browser_check.py](src/api/checks/map_fullscreen_browser_check.py) | Browser helper implementation |
| [src/api/tests/test_map_fullscreen.py](src/api/tests/test_map_fullscreen.py) | Source contracts |
| [src/api/README.md](src/api/README.md) | Browser coverage documentation |

## Next Steps

Return this one Review to the active parent. Preserve the findings and unchecked
P02 markers, make only the already authorized local evidence/commit continuation,
and stop without production repair or remote writes. Retain RV-001 as the distinct
later coordinated validation follow-up. Do not retry the lock, run browser/full
suites or request a second Review in this round.

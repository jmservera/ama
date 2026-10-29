<!-- markdownlint-disable-file -->
# Review: Map navigation disposal correction

## Scope and Evidence

* Task ID: issue-532-pr-539-map-navigation-disposal
* Review date: 2026-10-29
* Review scope: full bounded correction round, not whole PR/product acceptance.
* Assessed boundary: two supplied findings, pending-facets regression,
  isolated expiry iterations, strict/unit/browser validation and RPI evidence.
* Plan: .copilot-tracking/plans/2026-10-29/map-navigation-disposal-532-plan.md
* Details: .copilot-tracking/details/2026-10-29/map-navigation-disposal-532-phase-details.md
* Critique: .copilot-tracking/reviews/plans/2026-10-29/map-navigation-disposal-532-plan-critique.md
* Changes: .copilot-tracking/changes/2026-10-29/map-navigation-disposal-532-changes.md
* Research: .copilot-tracking/research/2026-10-29/map-navigation-disposal-532-research.md

## Opening Review State

* Goal: independently assess the completed correction and its evidence once.
* Evidence readiness: plan/details/changes reconciled; all P01/P02 markers
  complete; critique Complete / Pass without findings; full requested local
  validation reported passed with original failed attempts retained.
* Acceptance basis: current user requirements and plan criteria, preserving
  src-only/local-only/no-az/no-push and unchanged pinned fixtures.
* First comparison boundary: final four-file working-tree diff against
  starting HEAD 310889fa, then plan/evidence reconciliation.
* Active read-only boundary: source and all prior artifacts read-only;
  reviewer may write only this record. No implementation or second Review.
* Initial blockers: none reported; independent assessment pending.
* Independent review opening: artifact set resolved and read; comparison of
  starting HEAD 310889fa to the supplied working tree is now underway.
  Current Web Interface Guidelines retrieved successfully on 2026-10-29.

## Execution Status

* Execution status: Complete.
* Review execution evidence: one independent post-implementation Review on
  2026-10-29 of the supplied complete correction boundary. Compared the four
  actual changed files against 310889fa355c3b5821c3e1e0d03daa658a2abd63;
  current HEAD remains that starting commit on feat/map-fullscreen-532.
* All five supplied planning/implementation artifacts were read, along with
  surrounding route/auth/map lifecycle, browser instrumentation, the negative
  runner and existing runtime evidence. No tests, heavy commands, commits,
  subagents or source edits were performed by Review.
* The earlier opening statement that assessment was pending is preserved above
  as opening state, not the current verdict.

## Plan-to-Change Reconciliation

| Current plan scope | Descriptive changes-record summary | Current-state reconciliation | Gap or rationale |
| --- | --- | --- | --- |
| P01/P01-T01 | End obsolete map UI lifetime at disposal | Reconciled | Actual diff sets inert/disabled before collapse, preserves collapse before seq++, removes slot before Leaflet removal and guards expand. Existing contract and README updated. |
| P01/P01-T02 | Pending navigation regression and independent expiry iterations | Reconciled | One helper holds real facets and checks pointer, retained event and destination; reload precedes Coordinator navigation and fresh instrumentation in both expiry iterations. |
| P02/P02-T01 | Complete local correction verification | Reconciled | Existing API/core unit logs, final browser/negative-control evidence and caller-verified strict results support completion. Historical failures remain failures. |
| Acceptance, blockers and handoff | Pre-Review Reconciliation and Return-to-Caller State | Reconciled | All task/phase markers are complete; details and changes agree. Review and parent local commits are lifecycle actions, not unfinished source implementation. |
| Follow-Up Items | None | Reconciled | No distinct residual item appears in plan, details or changes. Excluded publication/SQL/hosted/human approval is not correction scope. |

## Completed Work Assessment

| Related marker | Files | What changed and why | Completion evidence | Validation | Assessment |
| --- | --- | --- | --- | --- | --- |
| P01-T01 | src/api/src/zava_forward/api/web/app.js | End disposed UI lifetime immediately, including live-signal disposal | expand guard at 1541; inert/disabled at 1565-1566; collapse, seq++, dialog/slot removal, Leaflet cleanup at 1567-1574 | Final pending navigation and both expiry modes pass | Conformant |
| P01-T01 | src/api/tests/test_map_fullscreen.py; src/api/README.md | Extend existing cleanup-order contract and explain immediate disposal/reset coverage | No added test method; ordered assertions include inert, disabled and slot removal plus guarded expand; documentation matches implementation | Full API units passed; source/diff read | Conformant |
| P01-T02 | src/api/checks/map_fullscreen_browser_check.py | Probe actual asynchronous navigation window, then isolate expiry iterations | check_pending_navigation added once and called by full runner; page.reload is first action of each expiry iteration | Final positive and original-JS negative control corroborate sensitivity | Conformant |
| P02-T01 | Supplied local validation and external logs | Verify strict tooling, full components and real browser without publication | API 1214 tests; core 1454 tests; full browser reaches 32px-font result; admitted nonblocking lock records | Passed with existing skips and stated limits | Conformant |

### Acceptance and Lifecycle Assessment

* Route disposal occurs synchronously at routeController.abort before
  listView awaits /api/facets. The fix removes the obsolete slot during that
  interval rather than relying on eventual show/render replacement.
* inert and disabled are assigned before collapse. For an expanded panel,
  collapse moves the box back into the inert slot, clears the body lock and
  calls resize while Leaflet still exists. seq++ follows that resize, so a
  collapse-triggered asynchronous draw cannot later pass its sequence guard.
  The existing success/catch guards and abort/disposer cleanup remain intact.
* Removing the slot alone would leave the retained event listener callable.
  The slot.inert guard rejects that listener's expand branch even when
  login/session disposal leaves the route signal live. The retained test uses
  both disabled-element click and dispatchEvent, the latter exercising the
  listener despite native disabled activation suppression.
* The new regression captures the original slot, toggle, scroll and pointer
  coordinates before navigation. A held real facets request, aborted old
  signal, live destination signal, #/all URL and still-visible Overview heading
  establish the pending boundary. Pointer activation occurs before release.
  Assertions require no map slot/dialog/body lock, disconnected/inert slot,
  disconnected/disabled toggle and clean retained activation and destination.
* The final old-source control uses the same helper and exact expected
  assertion, not a surrogate source-string check. Its served original-app.js
  bytes were independently compared with git show of starting HEAD and match.
  It records both dialogOpen and scrollLocked true while pending and verifies
  the leak over rendered All open cases. The positive capture records both
  false. This establishes that the pointer probe can detect the reported race.
* Each expiry loop reloads before fragment navigation and before wrappers are
  installed. The new document reconstructs ovState, me, mapPanel/api and Leaflet
  prototypes; start initializes authentication through the real valid cookie.
  Coordinator heading/clusters provide readiness before fresh instrumentation.
  Both modes then reach the unchanged overlapping-response assertions.
* Expanded expiry still causes a real collapse-resize request: four held
  requests versus two embedded, live route signals, empty draw errors and
  unchanged fits/clears after late successful responses. No sequence assertion,
  error collection, ordinary keyboard/manual path or enlarged-font check was
  removed or weakened.
* Test budget is respected: one browser helper, extension of one existing
  source-contract method, four approved source/documentation files, no new
  dependencies, fixture or production authentication changes.

## Implementation-Time Plan and Detail Update Assessment

| Affected area or marker | What changed and why | Triggering evidence and user decision | Reconciliation performed | Planning and critique state | Assessment |
| --- | --- | --- | --- | --- | --- |
| P01-T02/P02-T01 | Attached-pane readiness instead of visible-pane readiness | Original timeout; Leaflet's absolute pane has no own visible box | Current helper, phase details and changes describe attached readiness | Ordinary implementation refinement within accepted runtime coverage; no new user decision required | Reconciled; no assertion weakening |
| P02-T01 | Component-first test PYTHONPATH | API test_buildings shadowed core discovery | Details and changes preserve first failure and corrected core run | Command-binding correction, not product or scope divergence | Reconciled |
| P01-T02/P02-T01 | Function-valued wait predicates, including four existing expiry waits | Real strict-CSP EvalError in intermediate browser run | Source, details and changes agree; predicates retain original conditions | Tightly coupled execution refinement; no unsafe-eval, bypass or new requirement | Reconciled |
| P01-T02/P02-T01 | Release held facets before unroute in failure finally | Negative control reproduced defect but exposed cancellation, then double-handled route cleanup | Final helper and changes preserve failed attempts and final ordering | Test cleanup refinement within existing plan; no material revision | Reconciled |
| P01/P02 completion and handoff | Record observed results after final admitted checks | Final positive and exact negative control plus unit/strict results | Plan markers, details completion and changes agree on remaining work and limitations | Original Complete/Pass critique retained; one Review only | Reconciled |

## Critique and Material Revision Assessment

* Latest critique: Complete / Pass, zero PC findings. No unresolved disposition,
  accepted exception or significant/divergent decision is concealed.
* Implementation follows the critiqued disposal order and reset design.
  Readiness, import precedence, CSP predicates and cleanup refinements preserve
  confirmed intent and acceptance assertions. No material direction change
  required renewed planning, critique or a user decision.
* Dependent-work pause assessment: no evidence of work resuming before required
  critique disposition or of a material revision bypassing a decision.
* Original failed attempts and earlier outcomes were not rewritten by this
  Review. Final clean runtime evidence supports this correction only.

## Plan Follow-Up Assessment

| Follow-up item | Why outside immediate scope | Owner or next action | Assessment and route |
| --- | --- | --- | --- |
| None | No residual work was identified within this correction | None | No follow-up route |

## Findings

No actionable RV-xxx findings. Severity counts: Critical 0, High 0, Medium 0,
Low 0. No optional follow-up is invented.

## Defects

* None in the supplied correction boundary.

## Routed Findings

| Finding | Destination | Owner or next action | Reason for route |
| --- | --- | --- | --- |
| None | None | Parent receives this single Review result | No implementation, decision, research or residual-work gap identified |

## Residual Work

* None in the active correction. Local parent commits remain authorized
  lifecycle closeout, not a Review defect or a request for another Review.

## Blockers and Remaining Work

* Blockers: none for the supplied local correction acceptance.
* Remaining active implementation: none.
* SQL-backed integration, a complete publication receipt, hosted checks and
  human accessibility/operational approval remain explicitly outside this
  correction. They are neither passed here nor routed as correction defects.
  No push, az, merge or other remote lifecycle action is authorized by Review.

## Validation Evidence

Review inspected existing evidence only; no validation command was rerun.
External paths below are expressed relative to this worktree.

| Command or evidence | Scope | Status | Summary |
| --- | --- | --- | --- |
| API mypy; ruff check .; ruff format --check . | API strict tools | Passed, caller-verified | 101 mypy files; Ruff clean; 53 formatted files. Supplied parent verification and changes record, not independently rerun. |
| Core mypy; ruff check .; ruff format --check . | Core strict tools | Passed, caller-verified | 156 mypy files; Ruff clean; 103 formatted files. Supplied parent verification and changes record, not independently rerun. |
| python -m unittest discover -s tests -q, API | Full API suite | Passed | Read final summary in ../../../../../tmp/ama-532-navigation-20261029-U2JSTW/api-units.log: 1214 tests, 479.352s, 316 existing skips. |
| python -m unittest discover -s tests -q, core | Full core suite | Passed | Read final summary in ../../../../../tmp/ama-532-navigation-recheck-20261029-lTmkGK/core-units.log: 1454 tests, 299.607s, 190 existing skips. |
| python -m checks.map_fullscreen_browser_check | Complete constructed-app browser | Passed | ../../../../../tmp/ama-532-navigation-final-20261029-l51h74/browser.log and browser/*.json: pending pointer/retained/destination checks, both expiry modes and enlarged-font scenario complete. |
| Original-JS negative runner | Regression sensitivity | Passed, expected failure detected | ../../../../../tmp/ama-532-navigation-final-20261029-l51h74/negative-control.log and negative-control/pending-navigation.json: exact race assertion rejected old JS; modal/body lock observed pending and over destination; no final cleanup warning. Runner source read at ../../../.copilot/session-state/7ea8a749-09ea-4588-9bb5-768af3a41c5a/files/map_navigation_negative_control.py. |
| Chromium runtime | Browser error coverage | Passed | browser/browser.json reports Chromium 156.0.8078.4 and errors []; enlarged-font run also reports no errors. |
| 640px viewport and actual defaultFontSize=32 browser | Font/reflow coverage | Passed | Root font 32px; document 640px; dialog client/scroll 590/590; workspace 540/540; sidebar 243/243; map 271px. |
| Integrity-pinned axe 4.10.3 | Ten bounded map scans | Passed within automated boundary | Summarized existing axe-results.json: zero violations and no unresolved ARIA references. Each scan retains one color-contrast incomplete item; this is not full accessibility or contrast acceptance. No styling changes are made here. |
| flock -n admission | Heavy-check discipline | Passed, existing evidence | Initial and final lock.txt read as ACQUIRED nonblocking heavy lock; caller/changes report each heavy batch admitted and lock released. Review did not acquire or run a heavy batch. |
| Scenario-manifest SHA-256 comparison | Four pinned source inputs | Passed, read-only verified | All four current source bytes match manifest hashes; scoped diff does not edit pinned inputs, so no pin update is needed. |
| node --check; git diff --check | Syntax and whitespace | Passed, caller-verified | Final results supplied by caller/changes; Review inspected actual source diff without rerunning tests or checks. |
| Historical attempts | Failure preservation | Failed originally, retained | Existing logs retain visible-pane timeout, component-shadowed core invocation, strict-CSP predicate error, negative-control cancellation and double-route cleanup failures. Final evidence supersedes readiness, not those historical outcomes. |
| Review validation execution | Tests, browser and heavy checks | Skipped as instructed | Independent Review is source/evidence read-only; relies on inspected existing runtime logs and caller-verified strict results. |

### Scoped Web Interface Guidelines Review

Fresh source retrieved successfully on 2026-10-29:
https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md.
Reviewed the changed app.js lines with their lifecycle context against all
fetched rule categories. Accessibility, focus, interruptible interaction and
navigation/state rules are applicable: native controls/dialog/manual links
remain, disposal cannot restore focus to an obsolete toggle, and stale
activation is blocked. No markup, forms, typography, images, animation, theme,
locale, hydration, layout or styling change introduces a rule violation;
unchanged unrelated surfaces are outside this review.

src/api/src/zava_forward/api/web/app.js:1541 - pass
src/api/src/zava_forward/api/web/app.js:1565 - pass

This scoped guidelines pass and bounded automated scans are not whole-product
WCAG, human assistive-technology or staff usability acceptance.

## Outcome

* Outcome: Conformant.
* Rationale: actual source implements the accepted cleanup/reset design and
  preserves teardown ordering and prior behavior. The real held-facets test
  passes fixed JS and rejects exact starting JS at the reported race. Both
  isolated expiry modes, real collapse-resize late-response checks and
  enlarged-font coverage finish. Requested local strict/full-unit evidence is
  accounted for with existing skips and explicit provenance. Plan, details,
  critique, changes and research reconcile without material divergence.
* Acceptance limit: the bounded local correction only, not whole issue/PR,
  deployment, publication, SQL integration or human/hosted approval.

## Closeout Routing Record

| Finding class | Destination | Owner or next action |
| --- | --- | --- |
| Implementation defect | None | No RV finding |
| Decision gap or invalid assumption | None | No RV finding |
| Material evidence gap | None | No RV finding |
| Non-blocking residual work | None | No distinct follow-up |

* Execution status: Complete.
* Outcome: Conformant.
* Validation coverage: actual diff/lifecycle, all acceptance criteria, current
  RPI artifacts, existing full-unit/positive-browser/negative-control evidence,
  caller-verified strict checks, fresh scoped web guidelines and pin integrity.
* Blockers: none within the stated correction.
* Handoff: return this one complete findings/outcome set to the active parent.
  No later implementation invocation or repeated Review is requested.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-29/map-navigation-disposal-532-plan.md](.copilot-tracking/plans/2026-10-29/map-navigation-disposal-532-plan.md) | Accepted correction plan |
| [.copilot-tracking/details/2026-10-29/map-navigation-disposal-532-phase-details.md](.copilot-tracking/details/2026-10-29/map-navigation-disposal-532-phase-details.md) | Completed task details |
| [.copilot-tracking/reviews/plans/2026-10-29/map-navigation-disposal-532-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-29/map-navigation-disposal-532-plan-critique.md) | Original Complete / Pass critique |
| [.copilot-tracking/changes/2026-10-29/map-navigation-disposal-532-changes.md](.copilot-tracking/changes/2026-10-29/map-navigation-disposal-532-changes.md) | Implementation and retained validation history |
| [.copilot-tracking/research/2026-10-29/map-navigation-disposal-532-research.md](.copilot-tracking/research/2026-10-29/map-navigation-disposal-532-research.md) | Lifecycle/reset rationale and evidence |
| [.copilot-tracking/reviews/logs/2026-10-29/map-navigation-disposal-532-review.md](.copilot-tracking/reviews/logs/2026-10-29/map-navigation-disposal-532-review.md) | This single independent Review |

## Next Steps

No user action is required. The active parent may update closeout state and
make the authorized local conventional/coauthored commits. Stop without push
or another Review; no correction finding requires a subsequent RPI stage.

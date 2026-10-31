---
title: Browser asset matcher correction Review
ms.date: 2026-10-30
---
<!-- markdownlint-disable-file -->

## Scope and Evidence

Task ID: pr-594-browser-asset-matchers-568. Review date: 2026-10-30.
Full local correction for PR #594, Refs #568. Source/test/docs correction only; no release/live acceptance.
Plan: `.copilot-tracking/plans/2026-10-30/browser-asset-matchers-568-plan.md`.
Details: `.copilot-tracking/details/2026-10-30/browser-asset-matchers-568-phase-details.md`.
Critique: `.copilot-tracking/reviews/plans/2026-10-30/browser-asset-matchers-568-plan-critique.md`.
Changes: `.copilot-tracking/changes/2026-10-30/browser-asset-matchers-568-changes.md`.
Research: `.copilot-tracking/research/2026-10-30/browser-asset-matchers-568-research.md`.

## Opening Review State

* Goal: independently assess whether all asset routes/waits/DOM/coverage handle release versions without hiding real browser behavior.
* Scope: full task AC1-AC5 and P01/P02, source changes, five new regressions, guide, original critique and implementation updates.
* Evidence readiness: all markers checked; exact CI failure and after-pass logs, seven browser modules, 73 units, Ruff and mypy recorded with external identities.
* First comparison: staged correction versus original HEAD and current requirements/evidence.
* Boundary: read source/evidence only, write this one Review record only. No new source changes, approval, Azure, secrets, remote write or repeated Review.
* Initial blockers: none.

## Execution Status

* Review execution status: Complete.
* Exactly one independent post-implementation Review performed; no nested agents, source edits, repeated Review, staging, commit, remote or cloud operations.
* Assessed HEAD: b5ef6a1229b7d634868507db3ad8dca77678c890.
* Assessed staged source boundary: git diff --cached -- src/api, SHA-256 5acf67c09ae38e53b633d61be8c489ad403553aaec7bdbcc9f7033e6ac968a36, independently verified before and after inspection. No unstaged src/api changes.
* Implementation records mark P01/P02 Complete and accurately record the executed checks. Acceptance is not equivalent to those execution markers: one required context guard is missing (RV-001), and AC5's local commit remains the parent's administrative action.
* Original opening state above is retained, including its initial readiness interpretation. The completed comparison below qualifies that interpretation rather than rewriting its history.

## Plan-to-Change Reconciliation

| Current plan scope | Changes and current evidence | Assessment |
| --- | --- | --- |
| P01-T01 shared helper and seven harnesses | One new helper; every discovered asset route/unroute, wait, script observation and coverage classifier migrated; deliberate bare HTTP requests unchanged | Matcher correction reconciled; external-traffic requirement incomplete in chat recovery, RV-001 |
| P01-T01 behavioral preservation | Actual lexical CDP counts, retry budgets, readiness, navigation/session guards, MIME/length and cache turnover retained | Supported; employee count correction follows actual retry implementation |
| P01-T02 tests and guide | One new file, five methods, standard-library helper, no dependencies or test removals; guide specifies query versus synthetic-directory limits | Reconciled within six-method budget |
| P02-T01 CI and affected browsers | Original sequence and all seven affected modules passed across original fixed/remaining logs | Execution supported; passing scenarios do not establish a missing deny guard |
| P02-T02 units/lint/types | 73 tests; configured API Ruff check/format; strict new-code checks; mypy 122 files | Supported within configured scope, with legacy exclusions disclosed |
| AC5 and handoff | Ordered original artifacts present; local commit explicitly follows Review | Partial acceptance, not a false commit claim |
| Follow-Up Items | Hosted/publication/human/live gates and optional legacy lint cleanup remain outside active markers | Correctly segregated |

The P01-T02 changes subsection's historical "Validation pending" is superseded explicitly by the completed Validation Record, Pre-Review Reconciliation and Return-to-Caller State. It does not prevent a credible current-state comparison. The missing chat guard is substantive, not a prose-only discrepancy.

## Completed Work Assessment

| Marker | Files and behavior assessed | Evidence and result |
| --- | --- | --- |
| P01-T01 | src/api/checks/asset_urls.py | Anchored HTTP(S)/root-relative classifier; escaped exact origin when supplied; prefix segments exclude query/fragment delimiters; complete escaped canonical suffix; optional query/fragment. Lookalike filenames, trailing paths, query spoofing and incomplete vendor paths cannot match. Broad directory prefixes are intentional compatibility, not a serving promise. |
| P01-T01 | src/api/checks/workspace_scripts_browser_check.py | Routes, equivalent unrouting, response/failure selection, DOM wait and observer use shared origin-bound pattern. CDP still rejects duplicate executions and requires the original roleScreensView, not a wrapper. Real late-load checks retain zero inappropriate view calls and one legitimate revisit call. Leaflet body length 147552, MIME and ETag/revalidation assertions match StaticAssets.headers. |
| P01-T01 | src/api/checks/loading_briefing_browser_check.py | All app/watchdog/companion/law/helper routes and related observations migrated, including dynamic paths. Shell guard added; other contexts already guarded. Existing API matchers untouched. |
| P01-T01 | src/api/checks/employee_workspace_browser_check.py | Origin-bound ops/specialist injection and counts; path classification preserves script ordering. Exactly three ops attempts before reload, then one additional attempt; actual app.js retryWorkspaceScript makes two retries after the initial HTML request. No arbitrary timeout or retry expansion. |
| P01-T01 | src/api/checks/chat_widget_browser_check.py | Asset callback is origin-bound and original transient/exhaustion assertions preserved. employee and resident contexts have guards, but recovery_case creates a distinct unguarded context: RV-001. |
| P01-T01 | src/api/checks/case_journey_browser_check.py; src/api/checks/case_view_ux_browser_check.py | Enhancement fault injection now matches versioned assets; context guards inspected, stacked-panel/safety and controlled-enhancement-exception assertions retained. |
| P01-T01 | src/api/checks/asset_cache_browser_check.py | Server-side widget classification and DOM URL identification migrated. Exact failed/retried release URL, two requests, warm-cache reuse, executed release B, computed CSS, shared/vendor code and 304 validators retained. No Playwright routing added. |
| P01-T02 | src/api/tests/test_browser_asset_urls.py | Five methods cover positive/negative classification, native Chromium request/response waits and interception, equivalent unroute, DOM event observation, actual CDP (1,1), off-origin abort, mocked count filtering, duplicate versions and missing original view. |
| P01-T02 | src/api/README.md | Documents suffix/origin behavior, original ordered CI commands, pip prerequisites, external output and synthetic-only acceptance boundaries. No application or UI change. |

The survey included all src/api/checks Python files, not only changed lines or caller-named filenames. Seven modules contain relevant asset instrumentation. Remaining asset references are error wording, local source paths, deliberate bare byte-contract GETs, legacy priming or version-identity assertions, not missed version-sensitive routes. Existing API fault-injection matchers are unchanged and outside this correction.

### Test semantics and limits

* Classification exercises bare, query and leading-directory variants for main/shared/vendor JS and CSS, root-relative and absolute forms, query plus fragment, origin lookalikes, filename extensions, trailing paths and query-only asset names.
* Native test fulfills synthetic HTML and the script locally, starts precise coverage before navigation, appends the script, observes exactly one load event with readiness, invokes roleScreensView, then verifies actual CDP evaluation/view counts (1,1). It does not infer execution from a string or substitute a wrapper.
* Re-created equivalent matcher removes the actual page route; a later fetch reaches the context abort guard. Off-origin canonical-looking fetch likewise reaches that guard without entering the local companion callback. This proves the tested guarded context, not every production harness constructor.
* Mocked CDP tests separately establish same-origin filtering, original counts (1,2), absent local scripts (0,0), duplicate-script rejection and missing-view rejection. They are not represented as real V8 execution.
* Application StaticAssets.url emits query versions only. Synthetic directory versions prove instrumentation compatibility, not HTTP serving, app directory-version recovery or deployment acceptance.

## Implementation-Time Plan and Detail Update Assessment

| Affected scope | Change, trigger and rationale | Reconciliation and assessment |
| --- | --- | --- |
| PC-001 / P02 prerequisites | Parent explicitly rejected critique-worker-specific file-location constraint; caller mandates shared host lock and repository external generated outputs | Plan/details/changes preserve original Revise and explain execution context. Accepted as reasoned parent disposition; this reviewer did not open the lock, create external files or execute heavy commands. Reviewer-specific restrictions are not retroactive parent restrictions. |
| PC-002 / P01-T01 cache exception | Playwright routing disables HTTP cache; adding a cache-fixture guard would invalidate warm-cache proof | Exception recorded consistently in plan/details/changes and supported by actual fixture design and observed cache reuse. No page route exists in that fixture to bypass a lower-priority guard; constructed local fixture bytes are retained. Accepted justified divergence. |
| P01-T01 / P02-T01 employee counts | fixed-validation.log preserved old total-two assertion failure after real versioned interception | Source retry loop has two bounded retries, hence three initial attempts and one after document reload. Plan/details/changes reconcile the update and remaining-validation.log passes the stronger exact assertions. No product decision or new critique needed. |
| PC-002 / external traffic | Plan says exact-origin page matchers fall through to context deny guards | Applied to shell and other guarded contexts, but recovery_case lacks the assumed context guard. Native helper test does not resolve that implementation gap; RV-001. |

## Critique and Material Revision Assessment

* Original critique remains Complete / Revise, with PC-001 High and PC-002 Medium; neither finding was silently erased or relabeled as an original approval.
* PC-001 rejection is explicit and justified for parent execution, as directed by the caller. Available baseline/fixed/remaining artifacts corroborate actual runtime evidence. No imaginary parent restriction is used as a Review blocker.
* PC-002 exact-origin binding resolves page asset callback precedence where a context guard exists. Shell guard is present. Cache omission is deliberate and justified. Chat recovery omission is neither the documented cache exception nor covered by the guards in other, independent contexts.
* Descriptive updates preserve approved matcher, cache and retry intent and are reflected in current plan/details/changes. No unaccepted product redesign or significant decision gap was found; no route to rpi-plan or rpi-research is needed.
* Ordered research, one critique with explicit dispositions, implementation/evidence and this one Review are documented. Artifact contents support this sequence; this assessment does not claim a separately recorded immutable timestamp for each historical step.

## Acceptance Criteria

| Criterion | Assessment | Proven boundary |
| --- | --- | --- |
| AC1 | Supported | Hash-verified baseline log shows initial design-system and regulatory success followed by exact case-journey fallback timeout at original :1489. Workflow source confirms original command order. No baseline rerun performed in Review. |
| AC2 | Supported for matcher/test semantics | Five native/unit methods cover required positive/negative matrix, real routing/waits/unroute, DOM and actual/mocked coverage. Harness-wide traffic control still has RV-001 under functional/non-functional requirements. |
| AC3 | Supported for execution | Corrected original three-command sequence and seven affected modules passed. fixed-validation.log includes the intermediate employee assertion failure; remaining-validation.log proves the repaired employee and remaining modules. This is not blanket traffic-boundary acceptance. |
| AC4 | Supported within configured checks | 73 selected tests, API Ruff lint/format, strict new helper/test lint/format and mypy 122 files recorded. Baseline whole-case-view isolated lint discrepancy is optional and pre-existing, not failed required CI. |
| AC5 | Partial | Original Research/Plan/Critique/Implement evidence exists and this Review persists. No push or closing keyword introduced. Local commit is not yet created and remains parent-owned; no full AC5 completion claim. |

## Plan Follow-Up Assessment

| Follow-up | Why outside current correction | Owner / next action |
| --- | --- | --- |
| Hosted rerun and complete local publication gate | Local commit only; no publication authorized; focused checks cannot substitute for exact-head full receipt or hosted gates | Parent/owner, only upon later publication authorization; preserve original evidence and perform required current-base gates |
| Human/live-site and accessibility acceptance | Constructed local browser evidence is not deployment, assistive-technology or WCAG acceptance | Owner and appropriate human acceptance reviewers in distinct later work |
| Optional legacy case-view lint cleanup | Existing API exemptions and workflow do not require whole-file isolated strict lint; ten original B023/E501 diagnostics independently recorded | API maintainer may open a separate cleanup task; do not absorb into matcher correction |

These follow-ups remain outside active implementation and acceptance claims. AC5's local commit is a pending current administrative action, not an optional future follow-up.

## Findings

<!-- rpi:review id=RV-001 -->
### RV-001 [Medium]: Chat recovery has no context deny guard for off-origin requests

* Related scope: P01-T01; PC-002; functional exact-origin/fallthrough requirement and non-functional external-application-traffic boundary.
* Evidence: src/api/checks/chat_widget_browser_check.py:908-920 creates a fresh context in recovery_case and registers only the origin-bound chat-widget page route. There is no context.route guard before navigation or later in that function. employee (:749-756) and resident (:810-817) guards belong to separate contexts and do not carry over; main invokes recovery as a separate scenario. src/api/tests/test_browser_asset_urls.py installs its own local_fixture context guard, so its successful off-origin test cannot establish the missing recovery guard.
* Impact: an off-origin canonical-looking asset correctly fails the page matcher but falls through to normal networking, not the promised deny guard. Other unexpected application requests are likewise not blocked in this recovery context. Existing passing synthetic scenarios and correct matcher origin precision do not establish the required control. No actual off-origin transmission is alleged.
* Destination: rpi-implement, current accepted direction; not a product redesign, research gap or optional follow-up.
* Smallest useful next action: add the existing local-only context guard to recovery_case while preserving origin-bound page routing, transient/exhaustion/revisit assertions and the deliberately unrouted cache fixture. Validate off-origin denial in this actual recovery context and run the relevant focused check under the parent's shared heavy lock; retain original Review and adverse evidence.
* Acceptance evidence needed: actual recovery context aborts an off-origin canonical-looking request without reaching the asset callback/network, while both existing recovery scenarios still pass. No second Review is required.

This is the complete substantive finding set for the supplied frozen boundary: 0 Critical, 0 High, 1 Medium, 0 Low. No additional matcher, assertion-preservation, test-budget, dependency or type/lint defect identified.

## Defects and Routed Findings

| Finding | Destination | Owner / action |
| --- | --- | --- |
| RV-001 | rpi-implement | Active parent performs surgical chat recovery guard correction and focused locked validation |

## Residual Work and Blockers

* Review blockers: none; evidence was sufficient for a complete single assessment.
* Acceptance blocker: RV-001's unmet explicit traffic-control requirement.
* Remaining active work: implement/validate RV-001, then parent preserves original artifacts and creates the authorized local commit. AC5 is pending until then.
* Distinct residual follow-ups: hosted/publication/human/live acceptance and optional legacy lint cleanup, as routed above. None is falsely claimed passed.

## Validation Evidence

External logs were read at the supplied session files location, not copied or modified. All four supplied SHA-256 identities were independently matched:

| External evidence basename | SHA-256 |
| --- | --- |
| baseline-ci.log | b61a9587e4ed95b8a2b78a3f9839d158b50efa299fd7a9c2c9d6aaa4c8bd0545 |
| fixed-validation.log | 493fe2f9bf3a1905a39db805e4d5f971d0b56f633e7cb50f6f2f3690ba7abe98 |
| remaining-validation.log | d13ba1d567e2dd9b39102586465b571ac4e6f06a5b9a8141f0b2983af855c4bc |
| axe-4.10.3.min.js | 880970c081707360e64f34cea25ff91892f5bc95675b0776925b9709dd8a68bb |

The canonical external location and concrete locked commands are retained in the supplied changes artifact. Logs contain runtime output; the surrounding command/env/lock provenance is recorded in that artifact, not independently reconstructed by rerunning commands.

| Validation scope | Status | Evidence / limit |
| --- | --- | --- |
| Baseline original ordered CI commands | Failed as expected | Original fallback timeout, baseline-ci.log; design-system/regulatory preceding results inspected |
| Corrected original ordered CI commands | Passed, recorded | fixed-validation.log includes genuine stacked-section fallback and actual Chromium 200% zoom |
| Workspace scripts/loading briefing | Passed, recorded | fixed-validation.log; real lexical evaluation count 1, late/session guards, helper/law failure paths and Leaflet ETag |
| Initial corrected employee check | Failed, historical | fixed-validation.log preserves obsolete total-two assertion failure, not hidden |
| Repaired employee/chat widget/case-view/cache | Passed, recorded | remaining-validation.log; exact three/one ops assertions, original chat recovery, both case fallbacks, actual warm-cache turnover |
| Eight selected unit modules including five new matcher methods | Passed, recorded | 73 tests in 5.980s, remaining-validation.log; native method code inspected |
| Configured API Ruff check and format | Passed, recorded | All checks passed; 64 files already formatted. Existing checks/*.py exemptions/exclusions remain unchanged. |
| Strict new helper/test lint/format | Passed, changes-record evidence | Explicit isolated src=["src","tests"] command; no new suppression or manifest modification |
| mypy | Passed, recorded | Success in 122 source files; existing configured overrides unchanged, not universal strict typing acceptance |
| Optional whole-case-view strict lint | Failed, pre-existing | baseline-strict-case-view.log has ten original B023/E501 diagnostics; changed lines only add import/matcher substitution |
| git diff --check and git diff --cached --check | Passed in Review | Read-only whitespace/index consistency checks; no heavy execution |
| Heavy browser/test reruns in Review | Skipped deliberately | Caller requires evidence audit, not duplicated expensive checks. Static constructor evidence is conclusive for RV-001; no new runtime claim. |
| Hosted/full-publication/live/human acceptance | Unperformed | Outside authorized local correction; no exact-head receipt, deployment or approval claim |
| Local commit | Unperformed | Parent's final administrative action; this reviewer has no commit/stage authority |

## Outcome

* Outcome: Not accepted.
* Rationale: matcher implementation and local behavioral evidence are credible, with justified cache/environment dispositions, but the explicit chat recovery external-traffic control remains unmet. Passing recorded checks do not erase RV-001. AC5's local commit is also pending, rather than misrepresented as complete.
* Review execution remains Complete; this outcome does not mean the recorded browser/test commands were blocked or unrun.
* Preserve this original Review unchanged after handoff. A later correction and its evidence belong to parent-owned implementation records, without repeated Review.

## Closeout Routing Record

| Finding class | Destination | Owner / next action |
| --- | --- | --- |
| Implementation defect | rpi-implement | Parent resolves RV-001 and validates actual recovery-context denial |
| Decision gap / invalid assumption | None beyond implementation finding | Cache exception and parent environment disposition are justified |
| Material evidence gap | None requiring rpi-research | Missing guard is directly visible in source, not uncertain root-cause research |
| Non-blocking residual work | Distinct publication/acceptance and lint follow-ups | Owner/API maintainer, only upon separate authorization |
| Current administrative completion | Parent local commit | Preserve original Review and correction evidence; no push |

* Execution: Complete.
* Outcome: Not accepted.
* Severity: one Medium, RV-001.
* Validation: audited existing original CI before/after, seven modules, 73 tests, Ruff and mypy; no expensive reruns.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/research/2026-10-30/browser-asset-matchers-568-research.md](.copilot-tracking/research/2026-10-30/browser-asset-matchers-568-research.md) | Complete research, baseline and C1-C7 |
| [.copilot-tracking/plans/2026-10-30/browser-asset-matchers-568-plan.md](.copilot-tracking/plans/2026-10-30/browser-asset-matchers-568-plan.md) | Current requirements, markers and follow-ups |
| [.copilot-tracking/details/2026-10-30/browser-asset-matchers-568-phase-details.md](.copilot-tracking/details/2026-10-30/browser-asset-matchers-568-phase-details.md) | Complete implementation details and updates |
| [.copilot-tracking/reviews/plans/2026-10-30/browser-asset-matchers-568-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-30/browser-asset-matchers-568-plan-critique.md) | Original Complete / Revise retained |
| [.copilot-tracking/changes/2026-10-30/browser-asset-matchers-568-changes.md](.copilot-tracking/changes/2026-10-30/browser-asset-matchers-568-changes.md) | Commands, hashes, intermediate failure and final results |
| [.copilot-tracking/reviews/logs/2026-10-30/browser-asset-matchers-568-review.md](.copilot-tracking/reviews/logs/2026-10-30/browser-asset-matchers-568-review.md) | This single original Review |

## Next Steps

Active parent continues to rpi-implement for RV-001, preserves this original Review, performs focused locked validation and records the correction, then creates the authorized local commit. No second Review, push, cloud operation or user action is requested by this reviewer.

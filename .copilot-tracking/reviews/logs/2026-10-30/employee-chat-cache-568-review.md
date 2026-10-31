---
title: Employee chat and release cache implementation Review
ms.date: 2026-10-30
---

## Scope and Evidence

Task ID 568, employee-chat-cache-568. Review date 2026-10-30.
Full requested task, working-tree candidate against supplied base d986c4c4;
not a committed exact-head publication assessment.
Plan/details/research/changes and original plan critique use this date/slug.
Acceptance basis: plan AC1-AC5 and caller local-only/no-push boundaries.

## Opening Review State

* Goal: independently compare implemented cache/chat delivery and regression
  evidence with the reconciled plan and caller requirements.
* Scope: all changed/new API serving, web loader, tests, browser checks and guide.
* Evidence readiness: P01 complete; final full API discovery 1,384 tests OK,
  320 skips; Ruff/format/mypy and both browser checks passed.
* First comparison boundary: implementation correctness and AC1-AC5, original
  critique dispositions and honest local/nonlocal acceptance separation.
* Read-only boundaries: no source/plan changes; write only this Review record.
* Initial blockers: none for local engineering assessment. Full publication,
  hosted/human/live acceptance is not established by this candidate.

## Execution Status

* Execution status: Complete.
* One independent post-implementation Review performed on 2026-10-30.
* Compared the complete tracked diff against d986c4c4 and all untracked
  implementation, test, check and task-evidence files listed by git.
* No nested agent, source change, heavy-check rerun, commit, credential access,
  live sign-in, cloud operation, deployment or push was performed.
* Only this canonical Review record was changed by Review.

## Compared Artifacts and Boundary

The reconciled plan, phase details, original critique, research and changes
record were read in the requested order after the preserved opening above.
The RPI session state confirms that Review is the parent's active phase.

* Plan: .copilot-tracking/plans/2026-10-30/employee-chat-cache-568-plan.md
* Details: .copilot-tracking/details/2026-10-30/employee-chat-cache-568-phase-details.md
* Original critique: .copilot-tracking/reviews/plans/2026-10-30/employee-chat-cache-568-plan-critique.md
* Research: .copilot-tracking/research/2026-10-30/employee-chat-cache-568-research.md
* Changes: .copilot-tracking/changes/2026-10-30/employee-chat-cache-568-changes.md
* Parent state: .copilot-tracking/rpi-sessions/2026-10-30/employee-chat-cache-568-state.json

Implementation boundary: src/api/src/zava_forward/api/static_assets.py,
src/api/src/zava_forward/api/server.py,
src/api/src/zava_forward/api/resident_demo/app.py,
src/api/src/zava_forward/api/resident_preview/app.py and
src/api/src/zava_forward/api/web/app.js.

Regression boundary: src/api/tests/test_static_assets.py,
src/api/tests/test_workspace_scripts.py, src/api/tests/test_ui_support.py,
src/api/tests/test_auth.py, src/api/tests/test_resident_preview_api.py,
src/api/tests/test_resident_demo_api.py, src/api/tests/test_mvp.py,
src/api/checks/asset_cache_browser_check.py and
src/api/checks/chat_submit_browser_check.py. Documentation boundary:
src/api/README.md. No tracked file removal or unrelated source change appears
in the candidate.

Repository problem/reference context and the Fluent 2 design-system,
WCAG-baseline and plain-content documents were consulted. This is a delivery
and interaction regression assessment, not a whole-app visual or accessibility
audit.

## Plan-to-Change Reconciliation

| Current plan scope | Changes and actual implementation | Reconciliation | Gap or rationale |
| --- | --- | --- | --- |
| P01, FR1-FR5 | All three tasks checked complete; changes and detail completion summaries agree | Reconciled | Scope remains shared delivery and existing chat, not a replacement widget |
| P01-T01 | Shared typed snapshot helper; all three static handlers; versioned HTML, ETags and conditional responses | Reconciled | Existing employee admission and resident host/expiry/allowlist boundaries precede conditional handling |
| P01-T02 | Four-line loader adjustment; version-preserving Node regression; ordinary employee real-endpoint browser path | Reconciled | Existing shared widget/focus implementation and controlled race matrix retained |
| P01-T03 | One new test module, one new browser harness, intentional expectation changes and API guide | Reconciled | Addition budget honored; original failures retained; final checks separately recorded |
| AC1-AC5 | Acceptance table below and actual external results | Reconciled | Skips and nonlocal acceptance are not converted into passes |
| Follow-Up Items | Plan says none; changes records no remaining implementation task | Reconciled | Commit and publication gates remain subsequent parent actions, not hidden implementation acceptance |

## Completed Work and Acceptance Assessment

| Criterion / task | Evidence assessed | Assessment |
| --- | --- | --- |
| AC1 / P01-T02 | Both handlers serve shared widget bytes; socket tests compare those bytes to the packaged shared source. Ordinary employee launcher performs real local Enter and mouse Send asks before any reset/install or ask interception. Successful reply content, message count, visible panel, expanded launcher, emptied composer and focus are asserted, followed by actual route refresh. Resident exercises actual rules replies, consent, both activations and expanded/focus state. | Conformant for local engineering scope |
| AC1 / retained regressions | Existing 12-case case/no-case x Enter/Send x none/route/equivalent-session matrix remains, with controlled delayed replies. Separate deliberate dismissal, workspace focus, changed identity/capability/account and stale-session races remain intact. | Conformant; controlled responses are not misrepresented as the new real-endpoint happy path |
| AC2 / P01-T01 | SHA-256 release identity includes sorted asset URL names and body digests, including shared and vendored files; order is deterministic. Handler creation captures bytes; known HTML src/href values receive that release query. All employee HTML entry aliases and both resident applications are covered. Names, shared JS, Leaflet JS and CSS changes have identity assertions. | Conformant; no runtime identity, user content, secret or git dependency enters the digest |
| AC3 / P01-T01 | Actual socket contract tests cover each entry point, byte-derived quoted ETags, weak/list/star conditions, changed validators, bare/old-version URLs, empty responses, MIME and policy. GET and HEAD share dispatch; HEAD suppresses bodies while retaining representation length, and 304 suppresses bodies and omits Content-Length. | Conformant; conditional HEAD follows the same inspected conditional path |
| AC3 / auth separation | Employee trusted-proxy checks remain before asset lookup/304; resident host/expiry checks and preview host/method/allowlists remain before serving. HTML never receives conditional 304 or an ETag, including provider-substituted employee HTML. APIs, unknown paths and denials retain no-store. Existing auth expectations change only static policy. | Conformant; cache handling does not authorize requests |
| AC4 / P01-T02 | Loader selects the original script attribute by pathname and reuses the full versioned value. Actual loader execution tests cover widget, adapter, async helper and Leaflet, two error attempts, deduplication and fallback compatibility. Existing timeout/load stopping and session/route guards are unchanged. Browser server records the identical widget query for initial failure and subsequent success. | Conformant |
| AC5 / P01-T03 | Final discovery log, original failure log, browser JSON and reviewed harness assertions support the recorded local results; lint/type outcomes are explicitly reported evidence rather than new Review executions. | Conformant within the disclosed validation boundary |

The static helper permits current bytes at bare or obsolete query URLs but
requires revalidation; it does not promise immutable historical representations.
HTML remains no-store so a normal new page load obtains current release URLs.
The change does not promise hot reload for an already open page, nor prove what
an earlier deployment actually served.

## Implementation-Time Plan and Detail Update Assessment

| Affected scope | Update and trigger | Reconciliation / decision | Assessment |
| --- | --- | --- | --- |
| P01-T03 / PC-002 | Critique required demonstrated legacy cache reuse, unchanged origin/context, snapshot turnover and observable execution/style | Details specify these assertions; new harness implements them and records request evidence | Compatible clarification, not a new product or architecture decision |
| P01-T02 / PC-003 | Critique separated an ordinary launcher real-reply path from controlled races | Details require real thread/ask behavior; new path runs before existing reset/interception helpers | Compatible clarification; no duplicate chat or live model authority |
| P01-T01/T03 | Initial full run exposed two old static-policy expectations | Logo assertion now requires a release query; resident static headers now expect revalidation while other security/API/error expectations stay intact | Intentional expectation maintenance, not weakened acceptance |
| P01-T03 | First cache browser polling failed under CSP | Harness now supplies function predicates; application CSP is unchanged | Test correction supported by the actual source and preserved failed-run history |
| P01-T03 | Typing/format validation required fixture and factory boundary annotations | New helper and factory signatures are typed; existing fixture annotations are narrow | No broad suppression, dependency addition or unrelated behavior change |
| P01 completion / handoff | Final discovery completed after the chronological running-run paragraph | Final changes readiness, plan checklist, details completion and parent next action all say Review | Reconciled; earlier running/failure statements remain historical evidence |

No material divergent implementation decision requiring replanning was found.
Preserving the shared focus fix already in d986c4c4, rather than duplicating
chat, is the researched and explicitly planned direction.

## Critique and Material Revision Assessment

* Original critique execution Complete and verdict Revise are preserved.
* PC-002 is applied: the cache harness uses one server port and browser context
  per site, primes legacy unversioned assets with a fresh lifetime, proves
  their second navigation causes no additional server asset requests, creates
  a new B handler snapshot, and asserts B execution and computed CSS. Shared
  widget B and employee Leaflet B are observed. No page/context routing
  disables caching in this harness.
* PC-003 is applied: the new employee path uses the normal launcher and actual
  local replies for both activations without employeeChat.reset/install or
  fulfilled ask responses. Controlled race tests remain separate.
* PC-001 is explicitly rejected by the parent on the stated distinction
  between its host/caller permissions and the critique worker's restriction.
  That disposition is recorded, not silently deleted or converted to an
  original Pass. Review does not independently reconstruct the parent's
  execution permissions or lock admission from browser JSON. It performed
  no prohibited-path operations or heavy checks itself and grants no path
  permission to a subsequent worker.
* Plan/details record these dispositions as preceding implementation; no
  contrary evidence of dependent work resuming before the compatible
  corrections was found. No second critique or Review was performed.

## Browser Proof and Test Reliability

External evidence supplied by the parent and inspected during Review:
/home/azureuser/.copilot/session-state/50f32963-b5c2-4665-b044-30dc1dde1c9c/files/employee-chat-cache-568/.

* chat-submit/results.json reports passed on Chromium 156.0.8078.4 and
  explicitly excludes live site/model/human accessibility.
* chat-submit/employee-real-replies.json records Enter and Send HTTP 200,
  visible replies and normal-launcher use. Harness assertions establish
  actual returned content and focus, rather than trusting summary booleans.
* chat-submit/employee-matrix.json contains all 12 intended combinations.
  The source retains additional dismissal and session-race assertions.
* asset-cache-v2/results.json records employee origin
  http://127.0.0.1:38757 and resident origin http://127.0.0.1:37939; each
  remains unchanged within its own exercise. Legacy script/style/widget
  requests appear once despite two prime navigations; employee also primes
  Leaflet. This is evidence of genuinely warm legacy caching, not merely
  a changed query string on a cold browser.
* Both cache runs observe release B script execution, computed CSS B and shared
  widget B; employee also observes vendor B. Each first versioned widget
  request receives server-injected 503 and its identical query subsequently
  receives 200, with two total requests before the final reload. Employee
  uses recovery; resident uses its existing visible manual-help/reload path,
  not an invented automatic retry.
* The final unchanged-release reload records 18 employee and 9 resident
  validator-bearing 304 responses. Server-side failure injection and actual
  handler recreation avoid Playwright routing's cache-disabling confound.
* Assertions are behavior/byte/socket based. Summary JSON is written only
  after assertions succeed, with fixture/context cleanup in finally blocks.
  There is no new package dependency, in-package test or removed coverage.
* Cross-browser repetition and timing-stress measurement were not requested
  or performed. Screenshots exist in the supplied evidence; Review assessed
  the assertions/results and does not claim a fresh visual acceptance run.

## Scoped Web Interface Guidelines Review

The complete current rules were freshly retrieved on 2026-10-30 from
https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md.
Retrieval succeeded without truncation. All fetched categories were considered
against the changed loader and its surrounding retry contract.

### src/api/src/zava_forward/api/web/app.js

Pass: src/api/src/zava_forward/api/web/app.js:238-241.

The change only retains the existing script URL for dependency recovery.
It adds no rendered control, copy, navigation, focus operation, layout,
animation, media, locale output, theme or hydration behavior. It performs
bounded script-element lookup, not a layout read or per-keystroke operation.
Existing retry failure/manual-reload and session boundaries remain. Fluent 2,
native semantics, reduced motion and plain-content rules are not displaced.
No introduced finding under the fetched rules is supported. Unchanged
whole-file UI patterns are not newly audited or attributed to these four
lines; this is not a WCAG or assistive-technology conformance claim.

## Plan Follow-Up Assessment

| Follow-up item | Outside immediate scope / next owner | Assessment |
| --- | --- | --- |
| None in plan | No distinct product follow-up to route | No unresolved plan follow-up was imported into active P01 |
| Subsequent commit and publication assessment | Parent owns the requested local commit with Refs #568 and coauthor, then applicable committed-candidate gates | Not completed by this Review and not counted as implementation acceptance |
| Historical/live/human/hosted acceptance | Separate authorized evidence and human/hosted processes | Explicit limitations, not invented defects or an authorization to sign in, deploy or push |

## Findings

No substantive actionable RV finding is supported by the reviewed boundary.
Severity summary: 0 Critical, 0 High, 0 Medium, 0 Low. No RV identifier is
fabricated for a passed criterion, a disclosed non-goal or a subsequent gate.

## Defects

* None found within AC1-AC5 and the supplied working-tree boundary.

## Routed Findings

| Finding | Destination | Next action |
| --- | --- | --- |
| None | None | Return the one completed Review to the active parent |

## Residual Work

* No newly discovered implementation residual or unaccepted decision.
* Full publication/exact-committed-head assessment and live/human/hosted
  acceptance remain outside this Review; passing local component checks
  does not replace them.

## Blockers and Remaining Work

* Review blockers: none.
* Remaining P01 implementation tasks: none supported by this assessment.
* Parent continuation: preserve the original evidence and this Review,
  perform only the authorized local commit, and keep later gate outcomes
  separate. No push, merge, deployment or issue-closing directive is authorized.

## Validation Evidence

| Check / evidence | Status | Coverage and qualification |
| --- | --- | --- |
| Focused unittest command in changes record | Passed, reported | Original 78 tests; subsequent 10 focused checks. No independent rerun in Review |
| Full API unittest discovery / api-tests.log | Failed, inspected | Original 1,384-test run: two static expectation failures, 320 skips; retained unchanged |
| Full API unittest discovery / api-tests-final.log | Passed, inspected | 1,384 tests in 487.490s, OK, 320 skips; skips are not executions |
| Ruff check and Ruff format --check | Passed, reported | Parent/changes report 63 files; raw standalone lint logs were not supplied in the evidence directory |
| Mypy | Passed, reported | Parent/changes report 120 source files; not independently rerun |
| checks.chat_submit_browser_check | Passed, inspected | Chromium 156.0.8078.4, real local replies plus controlled race/lifecycle assertions |
| checks.asset_cache_browser_check / asset-cache-v2/results.json | Passed, inspected | Both sites, warm legacy cache, fixed origin/context, B execution/style/shared/vendor, versioned recovery and actual 304s |
| Original cache-browser failure | Failed, reported | CSP polling problem retained in original asset-cache evidence; corrected predicates do not relax CSP |
| Fresh Web Interface Guidelines retrieval and scoped changed-loader review | Passed, performed in Review | All rule categories considered; no introduced finding |
| git diff --check d986c4c4 | Passed, performed in Review | No tracked diff whitespace errors |
| Complete publication gate / exact committed receipt | Not run in Review | Candidate is uncommitted; subsequent parent/gate boundary |
| Live sign-in/model/deployment, additional browsers and human accessibility | Not run | Outside authorization/scope; no acceptance claimed |

Original lock-wait timeouts described in changes are non-executions, not
passed checks. Review did not rerun heavy checks or infer a publication receipt
from the final API log.

## Outcome

* Outcome: Conformant.
* Rationale: the implemented delivery architecture, retained shared interaction,
  new regressions and inspected local results satisfy AC1-AC5 within the
  explicitly local working-tree assessment. No supported material defect,
  divergent decision or missing evidence prevents that bounded verdict.
* This verdict does not identify a committed publication head, establish a
  full local-gate receipt, close issue #568, or claim live/human acceptance.

## Closeout Routing Record

| Finding class | Destination | Owner or next action |
| --- | --- | --- |
| Implementation defect | None | No rpi-implement finding |
| Decision gap or invalid assumption | None | No rpi-plan finding |
| Material evidence gap | None for this boundary | No rpi-research finding |
| Non-blocking residual work | None discovered | Subsequent acceptance gates remain separate |

* Execution status: Complete.
* Outcome: Conformant.
* Validation coverage: inspected full API results and both browser outcomes;
  reported lint/type results distinguished from independently performed checks.
* Blockers: none for the completed local Review.
* One Review only; no repeat Review is requested.

## Next Steps

The active parent should record this one Review result and continue its
authorized local-only closeout, including the requested local commit and
separately recorded applicable gates. No user action or new RPI stage is
required by a finding. Do not push or claim publication/live/human acceptance.

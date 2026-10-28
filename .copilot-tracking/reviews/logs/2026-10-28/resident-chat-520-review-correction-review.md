---
title: Resident chat review correction original Review
ms.date: 2026-10-28
---

## Opening Review State

* Task: 520-review-correction. Review date: 2026-10-28.
* Interpreted goal: independently assess the five requested corrections and their
  coupled session/logout/direct-probe behavior, without assuming implementation correctness.
* Scope: current working correction against HEAD 685547ed on feat/resident-chat-520,
  continuing PR #525, not the earlier PR implementation.
* Evidence readiness: same-slug dated research, plan, phase details, original
  critique, changes and state are available; source comparison is beginning.
* Acceptance basis: five user criteria, PC-001/002 adopted, PC-003 rejected with
  its original rationale preserved, strict headers and asynchronous fences.
* First comparison boundary: reconcile current artifacts, then inspect the complete
  correction diff and necessary unchanged calling context.
* Active read-only boundaries: only this canonical Review may be updated; no other
  artifacts, source, agents, heavy checks, private data, secrets or Azure operations.
* Initial blockers: browser/axe not verified. First admitted run failed held-route
  setup; corrected times=1 rerun could not acquire the heavy lock in 40 minutes.
  Full exact-head gate not run. No publication or thread-resolution claim.
* Fresh Web Interface Guidelines source retrieved successfully on 2026-10-28 before
  reviewing changed JS.

## Execution Status

* Review execution: Complete. One original independent assessment performed.
* Implementation execution: Partial. P01 and P02-T01/T02 are implemented;
  P02-T03 lacks successful browser/axe execution, and publication tasks are pending.
* Method: read all seven same-slug evidence/state records, inspect the complete
  11-file correction diff and necessary unchanged server/controller/codec/probe
  context. No test suite, browser, heavy gate or other agent was launched.
* HEAD confirmed as 685547ed548464ebe58222e21ea3557fb53be963. Source corrections
  are working-tree changes; this is not an assessment of an earlier PR diff or
  a committed final publication candidate.

## Scope and Evidence

* Task ID: 520-review-correction; continuing parent 520 / PR #525.
* Research: .copilot-tracking/research/2026-10-28/resident-chat-520-review-correction-research.md
* Plan: .copilot-tracking/plans/2026-10-28/resident-chat-520-review-correction-plan.md
* Phase details: .copilot-tracking/details/2026-10-28/resident-chat-520-review-correction-phase-details.md
* Original critique: .copilot-tracking/reviews/plans/2026-10-28/resident-chat-520-review-correction-critique.md
* Changes: .copilot-tracking/changes/2026-10-28/resident-chat-520-review-correction-changes.md
* State: .copilot-tracking/rpi-sessions/2026-10-28/resident-chat-520-review-correction-state.json
* Implementation boundary: src/api/README.md; app.py, chat.py, web/demo.js and
  web/assistant.js under src/api/src/zava_forward/api/resident_demo/;
  src/api/tests/test_resident_chat_api.py and test_resident_demo_api.py;
  src/api/checks/resident_assistant_browser_check.py,
  resident_demo_browser_check.py, resident_sensors_browser_check.py and
  resident_demo_image_check.py.
* Context read: original case study, addendum, reference index/memory, sector
  primer, src/README.md local gate, existing SessionCodec and directly coupled
  browser/controller context. No regulatory-currentness or whole-product audit.
* Fresh source: https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md
  successfully retrieved in full on 2026-10-28, before inspecting changed JS.
  All fetched rule categories were considered for this behavior-only delta.
  Owner-selected Fluent/plain-language/ASCII conventions take precedence over
  conflicting generic typography or capitalization preferences.
* Evidence attribution: supplied passing counts and browser failure/admission
  history agree with the changes record and state. External logs, environments
  and datasets were not opened; reported results are not fresh reviewer runs.

## Plan-to-Change Reconciliation

| Current plan scope | Changes-record summary | Current-state reconciliation | Gap or rationale |
| --- | --- | --- | --- |
| P01-T01 | Verified sid, strict headers, cross-tab clearing, epochs and shared tokens | Partial | Binding and JS continuations are implemented; delayed logout cookie effects remain unfenced, RV-002. |
| P01-T02 | Visible manual target, untrimmed draft comparison, open-panel guard | Reconciled in source | Actual browser/focus/axe outcomes remain unverified, RV-001. |
| P02-T01 | Three new HTTP methods, Client sid and repeated-header support | Reconciled | Within eight-method maximum; no removals. Reported owning suite and final focused rerun passed. |
| P02-T02 | Existing browser/axe harness extended; README and coupled probes adapted | Implemented, unverified | times=1 corrects premature unroute intent but has not been successfully executed. No fresh pass inferred. |
| P02-T03 | Units, Ruff100, mypy, JS and browser validation | Partial, accurately unchecked | Static/unit results reported passed; first browser setup failed, corrected admission exhausted. |
| P03-T01 | One original independent Review | Completed by this record | Original adverse critique and earlier records preserved. Parent owns later state reconciliation. |
| P03-T02/T03 | Committed candidate, full receipt, exact-head assessment, push/resolutions | Pending, accurately unchecked | Not run or authorized by this read-only Review; RV-001 remains a publication blocker. |
| Follow-Up Items | Human/content, AT/native zoom and real-model acceptance | Reconciled as separate work | Remain outside active correction and engineering acceptance claims. |

The changes record still says "Implement active" and lists independent Review as
pending; the state already selects Review. This is the expected handoff snapshot,
not evidence that browser validation or publication completed. Only the Review
is updated here. Parent must record this outcome without marking unmet tasks done.

## Completed Work Assessment

| Criterion / marker | Exact source and regression evidence | Assessment |
| --- | --- | --- |
| Cross-tab per-login sid and permission; P01-T01 | app.py:228-247 validates one lowercase 16-hex header after cookie verification; /session and /login return verified sid. demo.js:28-49 clears page/account/controllers/transcript/permissions and revalidates hints without adopting their identity. demo.js:314-369,385-402 and assistant.js:322,349,366-379 fence JSON continuations and controller generations. test_resident_chat_api.py:182-264 covers cookie replacement, same-resident fresh sid, absent authentication and malformed/duplicate headers. | Server read/mutation binding is supported by source and reported HTTP results; actual shared-browser state is unverified. Logout response-cookie race remains, RV-002. |
| Punctuated morning/afternoon; P01-T01 | chat.py:36-43 shares regex word tokens with app.py:447-455. test_resident_chat_api.py:154-180 checks six punctuation searches and matching offered-slot hours with no bookings. Browser harness:367-381 checks period/proposals/focus plus axe. | Source and reported HTTP evidence support period selection; browser result not established. No new routing authority or reservation is introduced. |
| Visible manual retry/loading focus; P01-T02 | assistant.js:296-301 chooses a rendered callback title, email or retry, otherwise launcher. Existing tabindex/native controls retained. Browser harness:482-496 asserts error retry and loading launcher focus. | Correct for the named visible states by source inspection; actual layout/focus/axe unverified. |
| Typed-ahead draft; P01-T02 | assistant.js:317-319 captures the untrimmed value; :339 clears only an unchanged value; failure paths do not erase it. Browser harness:287-300 holds success and checks changed versus unchanged fields. | Implements selected exact-value comparison without trimming away draft identity. Actual delayed browser outcome unverified. |
| Dismissed delayed appointments; P01-T02 | assistant.js:322 checks controller generation/session and :340-342 requires an open panel before search/focus handoff. Escape/outside dismissal hide the panel at :289-294. Browser harness:302-322 checks unchanged focus, zero extra agenda requests and continued manual route, with axe. | Named remain-dismissed scenarios are guarded in source, not a verified browser pass. |
| Strict malformed/duplicate header denial; PC-002 | app.py:233-237 checks multiplicity and full ASCII hex shape before compare_digest. test_resident_chat_api.py:229-264 sends actual repeated HTTP headers, comma joins, empty/missing, short/long, nonhex and non-ASCII values across view/chat/agenda/logout. | No malformed non-ASCII compare_digest path found. Invalid cookie yields 401; valid-cookie binding denial yields 409 before personal reads. Header is not an identity selector. |
| Coupled direct probes; P02-T01/T02 | resident_demo_browser_check.py:264-279,359-373; resident_sensors_browser_check.py:139-146; resident_demo_image_check.py:208-216 add sid only to authenticated view probes. Existing forged-cookie, cross-handle and revoked-cookie denial probes remain. | Necessary caller adaptations, not scope expansion or weakened isolation. SQL/browser/image execution remains unverified here and cannot be inferred from unit/static counts. |

Server inspection also confirms existing same-origin/CSRF checks, strict request
fields, use_record is True, explicit book/cancel confirmation, case allowlisting
and reauthorization remain. Invalid-binding agenda book/cancel requests cannot
reach agenda operations. Withdrawal clears UI permissions but does not cancel
already accepted callbacks. No new private/model transport, works consent or
booking authority was added. This is bounded source review, not a security,
accessibility or resident-acceptance certification.

## Implementation-Time Plan and Detail Update Assessment

| Affected scope | Change / trigger | Reconciliation and assessment |
| --- | --- | --- |
| P01-T01/P02-T02, PC-001 | One transition epoch and fresh fenced /session comparison address reordered hints and stale continuations. | Plan, details and changes describe the same accepted direction. Source covers session/login/view/error/logout JS continuations; cookie side effects expose a remaining implementation defect, RV-002, not a new identity-provider decision. |
| P01-T01/P02-T01, PC-002 | Strict header shape/multiplicity avoids ambiguous values and non-ASCII comparison errors. | Applied consistently to view/chat/agenda/logout; parameterized owning HTTP coverage within fixed budget. No divergent decision. |
| P02-T02 | First browser setup failed after premature unroute; one-shot session/view routes now use times=1. | Source change matches recorded synchronization rationale, retains assertions and does not erase the first failure. Successful execution is missing, RV-001. |
| P02 and Scope | New view requirement necessitates sid in existing SQL/sensor/image direct probes. | Current plan, details and changes explicitly include those callers; no separate harness or new methods. Ordinary coupled compatibility work, not a material scope/authority revision. |
| P02-T03/P03 | Corrected browser admission exhausted the caller's full bounded retry window. | Unchecked markers and state blocker match actual reported execution; no skip, fallback, lock bypass or success is inferred. |

## Critique and Material Revision Assessment

* Original critique remains Complete / Revise, with PC-001 High and PC-002/003
  Medium. Its verdict is not rewritten or converted into approval.
* PC-001 and PC-002 were adopted directly in the current plan/details and
  implemented in the bounded source changes. The remaining logout defect is
  recorded independently below rather than declaring the contract satisfied.
* PC-003 rejection is preserved exactly as the parent's disposition: the worker
  invented a temp-path prohibition absent from that parent's instructions.
  That rejected premise does not create an unresolved owner decision or justify
  fixture redesign. This Review performs no operations on those external paths.
* No significant user-intent divergence, new authority, dependency change,
  schema change or unsupported material planning decision was found. Source,
  detail and scope updates are current enough for a credible verdict.
* Dependent-work readiness: PC-001/002 dispositions are recorded before this
  handoff; no publication is evidenced. P02-T03 and the gate remain incomplete.

## Plan Follow-Up Assessment

| Follow-up | Why outside immediate scope | Owner / next action | Assessment and route |
| --- | --- | --- | --- |
| Human resident/content acceptance | Not established by automated behavior checks | Product/resident engagement owner: arrange named acceptance separately | Open distinct follow-up, not a new P01/P02 task or a current defect. |
| AT/screen-reader and native browser zoom | Axe and root-font/reflow checks do not replace actual AT/native zoom | Accessibility acceptance owner: conduct the inherited human protocol | Open distinct follow-up; no conformance or acceptance claim. |
| Real-model acceptance | Synthetic bounded workflow does not establish real-model readiness | Resident-assistant/model acceptance owner: separately authorized evaluation | Open distinct follow-up; no Azure or paid model activity authorized here. |

## Findings

<!-- rpi:review id=RV-001 -->
### RV-001 [High]: Required browser/axe and publication evidence is incomplete

* Related scope: P02-T03, P03-T02/T03; all five acceptance criteria.
* Evidence: .copilot-tracking/changes/2026-10-28/resident-chat-520-review-correction-changes.md:38-43,48-69,79-84
  and the state blocker browser-heavy-admission. First actual browser admission
  followed 35 occupied-lock retries and failed setup with "Route is already
  handled" before application assertions. Source now uses times=1 for held
  session/view routes; its corrected rerun exhausted 40 minutes of nonblocking
  admission attempts every 60 seconds and exited 1 without Chromium execution.
  The caller identifies external log
  /tmp/ama-520-review-correction-browser-20261028-2.log; it was not opened here.
  No successful corrected report, full gate receipt or exact-head assessment
  is available. The source remains an uncommitted candidate at this boundary.
* Impact: Passed HTTP/static/type checks cannot prove shared-browser permission
  clearing, actual focus, delayed UI behavior, axe outcomes or coupled runtime
  compatibility. Publication, five remote thread resolutions and whole-task
  acceptance remain materially blocked; no partial receipt or historical pass
  can substitute.
* Owner: Validation/evidence owner (parent), then publication owner for P03.
* Destination: rpi-research, material evidence gap. Existing P03 publication
  tasks remain pending; this is not a request for a second Review.
* Smallest useful next action: after resolving RV-002 and obtaining coordinated
  shared-lock availability, execute the corrected existing Chromium/pinned-axe
  harness with all five scenarios and retained original failure evidence.
  Capture exact candidate/tool identities and actual results. Then commit the
  stable candidate and original dated RPI records, fetch current main, run the
  required complete gate under its existing admission contract, verify its
  current-base exact-head external receipt immediately before independent
  exact-head assessment and normal push. Preserve hosted/human approval gates.
  Any changed source, commit or base invalidates earlier candidate evidence.

<!-- rpi:review id=RV-002 -->
### RV-002 [Medium]: A delayed valid logout response can erase a replacement login

* Related scope: P01-T01, PC-001/002; cross-tab session/logout asynchronous fences.
* Exact evidence: src/api/src/zava_forward/api/resident_demo/web/demo.js:405-422
  fences only the JavaScript continuation of fetch. In
  src/api/src/zava_forward/api/resident_demo/app.py:556-562, successful logout
  validates the request's old cookie/sid, revokes that old token, then sends
  unconditional Max-Age=0 headers for both shared cookie names.
  test_resident_chat_api.py:182-205 only exercises an already-stale sid with a
  replacement cookie at request admission. The browser additions do not hold
  a successful logout response across another tab's new login.
* Reproduction from source: tab A submits valid logout for login A; the server
  accepts it, but its response headers are delayed before reaching the browser.
  Pre-opened tab B signs in successfully and installs login B's shared cookies.
  A's older logout response then arrives and deletes those same cookie names.
  Cookie processing occurs independently of, and before protection by, the
  transition comparison in demo.js:414. A also has an empty tab-local sid after
  clearPersonal, so it ignores B's change hint while logout is pending.
* Impact: A valid replacement login loses authentication and CSRF cookies,
  clears its new page/permissions on revalidation or fails its next request.
  This does not revoke B's server token or prove cross-case disclosure, but it
  violates the selected promise that stale logout work cannot sign out a
  replacement login. The new request-binding check only fixes stale admission,
  not this accepted-request/delayed-cookie-response ordering.
* Owner: Resident demo session implementation owner.
* Destination: rpi-implement, within the accepted session-lifecycle correction.
* Smallest useful next action: make logout cookie effects safe against a newer
  login, not merely its JSON continuation. Preserve old-token revocation,
  confirmed sign-out behavior, HttpOnly cookie authentication and strict binding;
  do not weaken denial or rely only on BroadcastChannel. Extend the existing
  shared-context browser scenario with an old logout held before browser cookie
  application, complete B login (including same-resident re-login), then release
  logout and assert B's cookies, protected view and new permission state survive.
  Retain ordinary logout and stale-at-admission denial coverage.

## Changed-Web Guideline Findings

## src/api/src/zava_forward/api/resident_demo/web/demo.js

src/api/src/zava_forward/api/resident_demo/web/demo.js:414 - stale-response fence does not fence shared logout Set-Cookie deletion; replacement login can be discarded (RV-002).

## src/api/src/zava_forward/api/resident_demo/web/assistant.js

No additional substantive guideline defect found in the changed lines for the
named five scenarios. Visible native focus targets, existing accessible names,
status/log announcements and generation guards remain. No stylesheet, motion,
image, locale, framework or layout change is introduced. Browser/axe, actual
focus visibility and human/AT conformance remain NOT VERIFIED.

## Defects

* RV-002: delayed logout cookie deletion escapes JS epoch fencing; route to
  rpi-implement. Source-grounded finding, not a claimed browser reproduction.
* No additional confirmed implementation defect is asserted. Unrun scenarios
  remain an evidence gap, not an invented test success or additional defect.

## Routed Findings

| Finding | Severity | Destination | Owner / next action | Route rationale |
| --- | --- | --- | --- | --- |
| RV-001 | High | rpi-research | Parent validation owner: acquire coordinated admission and establish actual browser/axe and final exact-head gate evidence | Material evidence gap; publication stays blocked. |
| RV-002 | Medium | rpi-implement | Session implementation owner: fence logout cookie effects and cover delayed logout/new-login ordering in existing harness | Concrete defect within accepted behavior, not a significant design-choice request. |

Later implementation of routed findings does not require this Review to run again.

## Residual Work

* Human/content, AT/native zoom and real-model acceptance remain the distinct
  inherited follow-ups above. They are not added to active correction scope.
* No new non-blocking residual item or unresolved significant planning decision.

## Blockers and Remaining Work

* RV-001 blocks publication even if source defects are corrected.
* RV-002 requires implementation before treating the session-lifecycle correction
  as complete. Do not mark the original Review accepted after a later correction.
* P02-T03 remains incomplete; P03 commit, complete gate, receipt verification,
  independent exact-head assessment, normal push and five thread resolutions
  remain pending. No remote thread or PR state was mutated by this Review.
* No heavy checks, retries, source/artifact corrections, new agents, environment
  inspection, private datasets, Azure operations or secret access were performed.

## Validation Evidence

| Command / check | Scope | Status | Evidence / qualification |
| --- | --- | --- | --- |
| Owning HTTP/agenda suite | Resident HTTP, agenda and owning checks | Passed, supplied | 71 tests, no skips; changes:38-39. Not rerun by reviewer. |
| Final ChatApiTests rerun | Final shared-cookie and stale book/cancel binding tests | Passed, supplied | 12 tests; changes:67-69. |
| Ruff check and format, line length 100 | Eight changed Python files | Passed, supplied | Final eight-file result; earlier import-order failure preserved and corrected. |
| API mypy | API typing | Passed, supplied | 94 files; earlier six test typing errors corrected without diagnostic suppression. |
| JS syntax | demo.js and assistant.js | Passed, supplied | Syntax only, not behavior. |
| git diff --check 685547ed | Correction including this Review | Passed, reviewer executed | No whitespace diagnostics; HEAD exactly matches requested baseline. |
| Actual Chromium/pinned axe, initial admission | Existing extended harness | Failed setup, supplied | Acquired after 35 busy retries; "Route is already handled", no application-assertion pass. |
| Corrected Chromium/pinned axe | Existing harness with times=1 | Blocked / not executed, supplied | Full 40-minute nonblocking admission window exhausted at 60-second retries; exit 1. Browser/axe NOT VERIFIED. |
| Coupled SQL/browser/image probes | Existing adapted protected-view callers | Not verified here | Source reviewed; no actual runtime pass supplied for those changed probes. Required gate must establish coverage. |
| Complete local gate and receipt verification | Clean committed final candidate / current origin/main | Not run | Required after stable original Review/implementation and commit. No final receipt exists here. |
| Fresh Web Interface Guidelines | Changed demo.js and assistant.js plus necessary context | Completed source review | Full current source fetched first; substantive finding reported file:line. Not accessibility conformance. |
| Human resident/content, AT/native zoom, real model, hosted approval | Distinct acceptance boundaries | Not performed / not claimed | Engineering results cannot establish these gates. |

## Outcome

* Outcome: Not accepted.
* Severity summary: 0 Critical, 1 High, 1 Medium, 0 Low.
* Rationale: review execution is complete, but planned implementation/validation
  is partial. Four named behavioral corrections and the main sid/header
  mechanism have credible source support and reported HTTP/static evidence;
  required real-browser/axe and publication evidence remains unavailable, and
  the logout response-cookie race is a concrete remaining defect. No conformance,
  human approval, release readiness or remote-thread resolution is inferred.

## Closeout Routing Record

| Finding class | Destination | Owner / next action |
| --- | --- | --- |
| Implementation defect | rpi-implement | Resident session owner: RV-002 logout cookie race, retain strict admission and existing assertions. |
| Decision gap or invalid assumption | None | No significant unresolved decision; original PC-003 rejection preserved. |
| Material evidence gap | rpi-research | Validation owner: RV-001 actual corrected browser/axe, then existing final publication gate sequence. |
| Non-blocking residual work | Distinct inherited follow-ups | Human/content, accessibility and model acceptance owners; not active correction defects. |

* Review execution: Complete.
* Implementation execution: Partial.
* Outcome: Not accepted.
* Validation coverage: supplied 71 owning tests, final 12 ChatApiTests,
  Ruff/format100 eight files, mypy 94 files and JS syntax passed; reviewer diff
  check passed. Browser/axe not verified; full gate not run.
* Parent continuation: preserve this original outcome and route each finding
  once. Do not repeat this Review, bypass the lock, resolve threads, or publish
  without the required corrected-source and exact-head evidence.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/research/2026-10-28/resident-chat-520-review-correction-research.md](.copilot-tracking/research/2026-10-28/resident-chat-520-review-correction-research.md) | Research evidence and accepted boundaries |
| [.copilot-tracking/plans/2026-10-28/resident-chat-520-review-correction-plan.md](.copilot-tracking/plans/2026-10-28/resident-chat-520-review-correction-plan.md) | Current requirements, markers and follow-ups |
| [.copilot-tracking/details/2026-10-28/resident-chat-520-review-correction-phase-details.md](.copilot-tracking/details/2026-10-28/resident-chat-520-review-correction-phase-details.md) | Strict-header, transition and regression contracts |
| [.copilot-tracking/reviews/plans/2026-10-28/resident-chat-520-review-correction-critique.md](.copilot-tracking/reviews/plans/2026-10-28/resident-chat-520-review-correction-critique.md) | Preserved original Complete / Revise critique |
| [.copilot-tracking/changes/2026-10-28/resident-chat-520-review-correction-changes.md](.copilot-tracking/changes/2026-10-28/resident-chat-520-review-correction-changes.md) | Implementation, reported checks and adverse browser history |
| [.copilot-tracking/rpi-sessions/2026-10-28/resident-chat-520-review-correction-state.json](.copilot-tracking/rpi-sessions/2026-10-28/resident-chat-520-review-correction-state.json) | Parent handoff and active admission blocker |
| [.copilot-tracking/reviews/logs/2026-10-28/resident-chat-520-review-correction-review.md](.copilot-tracking/reviews/logs/2026-10-28/resident-chat-520-review-correction-review.md) | This one original independent Review |

## Next Steps

Parent: route RV-002 to rpi-implement and RV-001 to rpi-research for evidence
completion, preserving the original Review and critique outcomes. Continue
existing publication tasks only after corrected-source validation, a clean
committed current-base complete gate, verified exact-head receipt and independent
exact-head assessment. No second Review or publication action is performed here.

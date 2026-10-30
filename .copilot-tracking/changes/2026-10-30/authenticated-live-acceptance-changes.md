<!-- markdownlint-disable-file -->
# RPI Changes: Authenticated live acceptance

## Metadata

* Task ID: authenticated-live-acceptance-2026-10-30
* Related plan: .copilot-tracking/plans/2026-10-30/authenticated-live-acceptance-plan.md
* Details: .copilot-tracking/details/2026-10-30/authenticated-live-acceptance-phase-details.md
* Implementation date: 2026-10-30

## Execution Status

Full RPI loop and bounded evidence persistence complete. Actual authenticated
feature execution remains Partial/Blocked; independent Review execution
Complete, outcome Not accepted. P01/P02 markers complete as evidence work,
not product acceptance. No product or private-data changes.

## Execution Summary

Independent Review execution Complete; outcome Not accepted; task execution
Partial. Original RV-001..005 retained. Do not reuse the current runner before
separately addressing RV-003: public capture shares the resident context and
does not fail closed after a future successful login. This run's observed 401
and independently viewed public crops did not disclose private records.
No Review finding is fixed or re-reviewed in this task.

Actual Chromium 156.0.8078.4 exercised both deployed sites on 2026-10-30.
Employee sign-in selected a passkey prompt after the username; normal Back and
Sign-in options exposed passkey/GitHub, not a password option. The definitive
run did not submit the password to Microsoft and did not reach an employee
session. This does not prove a Conditional Access/MFA misconfiguration.
Resident sign-in submitted the supplied credentials and received HTTP 401 with
a visible alert. Its cause is not established by the safe evidence.

No authorized /api/me response was obtained, so roster binding is UNKNOWN,
not absent. No private roster was read or edited. The documented initializer
would mutate SQL and restart services, so it was not used. No account, role,
Azure resource, configuration, policy or private dataset was changed.

Nineteen criterion decisions are recorded below: one proven for source browser
coverage only, eighteen unmet/blocked for live acceptance. No issue is accepted
as a whole. Unmet here includes missing evidence, not necessarily a UI defect.
Only the resident public chat shell could be exercised, not authenticated chat.

## Completed Work

### P01-T01: Actual sign-in and access boundary

* One task-owned automation: .copilot-tracking/changes/2026-10-30/authenticated-live-acceptance/acceptance.py.
* E1: .copilot-tracking/changes/2026-10-30/authenticated-live-acceptance/final-095616-evidence.json,
  09:55:23-09:56:16 UTC, definitive normal UI access classification.
* Employee: username value confirmed, Next route observed, unexpected passkey
  prompt, normal keyboard Back, normal Sign-in options; no password choice.
* Resident: actual /demo/login response 401, visible alert, sign-in form remains.
* Browser and owned scratch closed/removed; no traces/HAR/video/storage exports.

### P01-T02: Reachable public resident shell

* E2: E1's resident_public_chat section and the three
  resident-public-chat-1280.png, resident-public-chat-390.png and
  resident-public-chat-320.png crops in the same evidence directory.
* Launcher: right/bottom gaps both 16 CSS px; keyboard Enter opens role=dialog;
  Escape closes and focus returns to Chat.
* Popup widths at 1280/390/320: 448/358/288 CSS px, contained in viewport,
  no document horizontal overflow.
* Reduced-motion preference actually emulated: --motion 150ms becomes 0s;
  popup transition 0s and animation none in both cases.
* Fresh unauthenticated observer attached before navigation saw zero
  /demo/assistant requests. Shell says sign in to ask about own record.
* No authenticated composer, agent selection, consent, answers, map or case
  surface was reachable. No fabricated response, fault injection, paid model
  call, resident callback, works consent or record write was attempted.

### Evidence provenance and intermediate probe correction

* E3: inspect-evidence.json records the two public entry forms; auth-methods
  JSONs preserve investigation of the provider's username/passkey/options flow.
* E4: accept-evidence.json and employee-only JSONs retain original coarse
  probes, timeouts and classifications. The early employee password_submitted
  flags mean the script filled an autofill password field and activated a
  button; later inspection proved that button was Next, not a password
  submission. Those flags are NOT proof of password authentication.
* Early labels decline_stay_signed_in and stay_signed_in_navigation_timeout
  were also misclassifications: idBtn_Back was the passkey Back control, not
  a KMSI No action. Final normal keyboard navigation corrected this without
  policy changes. Original adverse evidence is preserved, not silently fixed.
* E1 is authoritative for the final outcome. It records
  password_submitted=false for employee. No successful callback, role or roster
  conclusion can be derived from E4.
* The first direct file invocation failed to import Playwright; invoking the
  existing interpreter through runpy resolved it without installation.
  MCP's code sandbox could not load filesystem modules; it never read the secret.
* The final screenshots contain only public widget chrome/help, no sign-in
  input, username, private record or credential. Their visible content was
  reviewed at 1280 and 320 px; the 390 crop is also checked in reconciliation.

## Criterion Acceptance Matrix

Proven requires every stated subpart. Unmet includes blocked/not observed;
partial successes are retained explicitly. Source coverage is not live proof.

| ID | Exact criterion | Decision | Evidence and missing proof |
| --- | --- | --- | --- |
| 550-01 | Both sites use one shared component with a bottom-right icon launcher that opens a popup chat | Unmet | E1/E2 prove only resident public launcher/popup and 16px gaps. Employee popup and applicable served shared-component use provenance unavailable. Appearance/asset presence is not substituted. |
| 550-02 | The conversation persists as a scrolling thread (newest at the bottom, input pinned), and the window stays open after sending | Unmet | E1: neither authenticated composer reachable. No multi-turn send, scrolling, pinning or post-send observation. |
| 550-03 | Enter sends, Shift+Enter adds a line, and a send button is present | Unmet | E2: Enter opens launcher only; this is not Enter-send proof. Both authenticated composers, newline and Send untested. |
| 550-04 | A compact selector in the input area changes the agent or skill (employee) and shows the active one | Unmet | E1 employee auth blocked; no actual selector, skill change or active indication observed. |
| 550-05 | Attach files and voice input controls are present, or are disabled with a stated reason where not yet supported | Unmet | E2 pre-sign-in shell has no composer. Authenticated Attach/Voice controls and reasons unobserved on both sites. |
| 550-06 | AI-generated content carries a thin label and a collapsed sources list (HAX and Teams AI content label patterns) | Unmet | E1 no actual response or AI content. Neither rules labels nor source code can substitute for live AI label/source-state evidence. |
| 550-07 | The resident consent step remains before any data is used | Unmet | E2 pre-navigation observer saw zero assistant requests in unauthenticated shell. Signed-in record-use consent/order and backend-only data use unobservable; portal session/view reads are not assistant consent proof. |
| 550-08 | A free-text question like the rat example gets a relevant answer or an honest 'I cannot answer that, here is who to contact', not the home summary | Unmet | E1 resident 401; "My home smells like a dead rat" was not sent without authentication/record-use consent. No answer/fallback observed. |
| 550-09 | Loading state appears after 200 ms, errors are shown, keyboard and screen-reader semantics are kept, reduced motion respected | Unmet | E2 proves shell role=dialog, Enter-open, Escape-close/focus return and motion token change; E1 proves a sign-in alert, NOT a chat error. Actual 199/200ms timing, chat error, sending keyboard/log semantics and assistive announcements untested. No native screen reader or injected success/error response. |
| 551-01 | The expanded map shows a compact version of the header filters along its top edge | Unmet | E1 employee session not reached; map/filter geometry unobserved. |
| 551-02 | Changing a filter updates map markers and the header filter state consistently | Unmet | E1; no authorized map, live marker changes, filter counts or restored header state. |
| 551-03 | Keyboard operable, non-colour state indication, readable at narrow widths | Unmet | E1; map keyboard/focus, aria-pressed plus visible Selected and 390/320 readability not observed. Resident shell width checks do not prove map behavior. |
| 551-04 | Behaviour covered by a browser or unit test | Proven (source coverage only) | C9: src/api/checks/map_fullscreen_browser_check.py:100-140 at ffd8f35e63b24905b9aeb937dbf2a7fe9968747f enumerates six filters, Enter/Space, aria-pressed, Selected, marker count against actual local API and focus assertions. This establishes existing browser-test coverage, not a run in this task, deployed parity or live acceptance of #551. |
| 552-01 | Workflow steps use the presentation icon set with text labels | Unmet | E1; no authorized case. Live icon rendering, labels, served icon-byte/presentation provenance unobserved. |
| 552-02 | Layout is visibly thinner, with less vertical space per step | Unmet | E1; no step geometry or comparative deployed before baseline. Local source density is not live comparative evidence. |
| 552-03 | The blocker shows a one-line summary and the full reason in a tooltip or popover that works by keyboard and touch | Unmet | E1; no case/blocker. Summary truncation, complete detail, keyboard and genuine touch interactions untested. |
| 552-04 | Tabs are visually attached to their panel, outside any inner scroll box, with the panel scrolling beneath | Unmet | E1; no case tablist/panel, ancestry, visual attachment or actual panel scrolling observed. |
| 552-05 | Fluent 2 and WCAG baselines in docs/reference/research/ux are preserved | Unmet | E1; affected authenticated case surface unavailable. Contrast, native semantics, focus, non-colour states, zoom/text resize, 320/390 reflow, touch, reduced motion and AT checks incomplete. E2 shell checks do not cover this surface; baseline itself disclaims completed Fluent adoption/full WCAG conformance. |
| 552-06 | Browser check evidence for desktop and narrow widths | Unmet | E1; no case-view captures at 1280/390/320. E2 resident public-shell captures do not satisfy single-case-view evidence. |

## Implementation-Time Plan and Detail Updates

P01/P02-T01 complete as bounded acceptance investigation, not successful product
acceptance. Auth blockers activate the preplanned stop for affected features;
no access repair or expanded authorization inferred. The final employee login
uses actual Next versus password-step semantics and normal sign-in options;
earlier heuristic flags are explicitly invalidated as proof, not rewritten.
Original critique Revise retained; no second critique.

## Validation Record

| Check | Result | Boundary |
| --- | --- | --- |
| Actual two-site Playwright | Executed, access blocked | E1, browser 156.0.8078.4 |
| Public resident desktop/narrow shell | Passed scoped observations | E2, 1280/390/320; not authenticated chat/case |
| Secret exclusion | Passed automation booleans | E1 credential_not_in_evidence and existing_evidence_credential_free; password never returned |
| Browser/scratch cleanup | Passed | E1 browser_closed and owned_scratch_removed |
| Python AST and 14 generated JSON parses | Passed initial reconciliation | No bytecode created |
| All 19 criteria and final evidence links | Passed | Ordered 9/4/6 IDs; definitive JSON and all three PNGs exist |
| Script Ruff and formatting | Passed after direct lint fixes | Removed unused import, explicit expected exception types, repository formatting |
| Original-evidence local commit | Passed | 2e07c2ad; Refs #550, Refs #551, Refs #552; no push |
| Full local RPI gate | Blocked before checks | Ignored Ruff cache corrected; then advanced main and non-descendant base; no receipt or publication |

## Pre-Review Reconciliation

Original handoff reconciled P01/P02-T01 and left P02-T02 for independent Review
and persistence. That one Review is now complete and its original artifact is
unchanged. Post-Review administrative work committed original evidence and
attempted the full gate. No finding remediation or second Review occurred.

## Blockers

* B1: Employee sign-in offered a passkey route, no password option in normal
  alternatives. Owner/identity operator must validate the intended supported
  password flow without assuming this run diagnosed policy. No changes made.
* B2: Resident /demo/login 401 for supplied test credentials. Owner/resident
  showcase operator must confirm intended account/enrolment. No alternate user
  or private account record was inspected or modified.
* B3: Employee roster binding unknown because authenticated /api/me unavailable.
  Only after access is available can an authorized account probe establish it.
  No absent-binding claim or initializer mutation.
* B4: Full local gate blocked: latest fetched main
  63422cdf9fd477dd8892a27ac8b11487bc3a2429 is not an ancestor of this topic
  candidate. No automatic rebase, merge, history rewrite, skip or cloud fallback.
  Any later integration/publication requires a separately authorized lineage
  decision and a fresh exact-head full gate/independent assessment.

## Remaining Work

No remaining active-plan evidence/persistence task. Product criteria and routed
Review findings remain open, not accepted or fixed.
Current script has post-execution dead-code removal, timestamped future
screenshot naming, explicit exception types and formatting. E1 was generated
before those maintenance edits; no exact script hash was captured for E1.
These limitations are retained for independent assessment rather than claiming
an exact-head receipt for the live run.

Independent Review is complete. Its original assessed boundary does not include
the later local commits/gate. The containing closeout commit persists only
administrative state after original-evidence commit 2e07c2ad; this is a direct
recordkeeping refinement, not a second Review or product change. Full loop
finished with an unaccepted/blocked outcome, not a conformant result.

### Post-Review local gate attempts

* Original source/evidence candidate: 2e07c2ad, clean after commit.
* First command: python3 tools/rpi-checks.py --all --jobs 1 --base
  80a7606bf0f8131df39f93b54ed5ac1fd479f467 --out
  /tmp/ama-auth-acceptance-20261030-2e07c2ad-gate.
  Blocked by task-created ignored .ruff_cache files. Removed only its three
  known cache files and their empty owned directories, not historical evidence.
* Second new output path ended -gate-attempt2; same reviewed base. Blocked
  because origin/main advanced. No checks, receipt or output tree produced.
* Fetched/reconciled main: 63422cdf9fd477dd8892a27ac8b11487bc3a2429.
  Delta since 80a7606b includes merged rubric/cutover evidence and an unrelated
  synthetic orchestrator rebuild module/tests, not employee/resident web code.
  No deployed parity or additional Review is inferred from this read-only delta.
* Third command used that current base and output path ending -gate-attempt3.
  Blocked: "Candidate does not descend from the reviewed main base".
  No rebase/merge was authorized or performed; no checks ran and no receipt
  exists to verify. This is a gate/lineage blocker, not a live UI test failure.
* Final containing commit invalidates earlier gate attempts as current-head
  evidence. A final same-policy attempt is kept external; the lineage blocker
  is not repaired by metadata. No push or final-head acceptance is claimed.
* The git-commit skill's referenced commit-message instruction file was
  unavailable at both resolved plugin paths. Repository Conventional Commit,
  Refs-only, noreply identity and required Copilot trailer rules were followed.

## Follow-Up Items

1. RV-003: isolate and fail-close public capture before runner reuse; later
   tracking-runner implementation. This is outside the evidence-only task and
   no actual disclosure was observed in the supplied public crops.
2. Establish supported employee test-user sign-in, then inspect binding through
   authorized /api/me; highest leverage because it blocks both map/case and
   employee chat. Owner/identity operator, E1. No role/policy edits authorized.
3. Confirm resident showcase test-user enrolment/credentials; resident operator,
   E1 HTTP 401. Distinct from employee Entra/roster.
4. RV-001/002: collect blocked authenticated criteria after access is ready,
   with exact executed-script/runtime and uniquely hashed per-run outputs;
   preserve originals rather than retroactively edit their provenance.
   Include actual
   AI labels, 200ms loading, rat fallback and map/case desktop/narrow behavior.
   Acceptance executor; matrix missing-proof cells. No source fixes inferred.

## 2026-10-30 11:55Z: Employee attempt 3 continuation

New dated evidence extends, and does not replace, the original run above.
See .copilot-tracking/changes/2026-10-30/employee-acceptance-attempt-3-changes.md
and its exact two-source/two-evidence manifest. Exactly TWO counted sign-in
attempts were used after the owner reported removing the passkey requirement.
The first failed on initial /app navigation before username/secret actions.
The final allowed attempt used the existing normal /.auth/login/aad entry,
reached the real password step, submitted once, reached Stay signed in and
subsequently had the app origin. No passkey challenge was seen in this run.

A browser/API transition failed before verified /api/me employee admission;
binding is UNKNOWN, not absent. Chat/map/case were not executed. Earlier
no-route evidence remains preserved, but no-password-route is no longer the
current blocker. No TAP submission or offered TAP option was observed; no
claim is made about file line-2 presence. The attempt cap now stops live work.
One source-only criterion (551-04) remains proven; eighteen remain unmet.
No whole-issue, Fluent/WCAG, human or deployed-parity acceptance is implied.
No screenshots, secret capture, video/HAR/trace, resident execution,
Azure/resource/role/policy change or push. Refs #550, Refs #551, Refs #552 only.

---
title: Resident chat 520 logout follow-up independent RPI Review
description: Original independent Review of child task 520-logout-followup
ms.date: 2026-10-28
---

## Opening Review State

* Interpreted review goal: Assess the distinct child 520-logout-followup once, not reopen or replace the parent Review.
* Review scope: Complete child requirements, current RPI artifacts, four-file working-tree diff against 618777a26bf62566a0d920c7127d3a8313b85e65, necessary unchanged session/browser source, and supplied validation evidence.
* Evidence readiness: Child research, plan, details, critique, changes and state exist; raw evidence verification and reconciliation are pending.
* Acceptance basis: User constraints, child acceptance criteria, original critique and direct dispositions, and mandatory repository publication gate.
* First comparison boundary: Child plan and critique against implementation, then actual recorded validation and publication readiness.
* Active read-only boundaries: Only this Review record may be written. Parent Not accepted artifacts, child planning artifacts, runtime, tests, remote state and external evidence remain unchanged. No new checks, installs, agents or Azure commands.
* Initial blockers: Canonical full local gate/receipt reportedly unavailable under the explicit no-Azure constraint; local commit, publication and verified thread resolutions remain pending.

## Execution Status

* Review execution status: Complete.
* Implementation execution status: Partial. P01/P02 are evidenced complete within the permitted boundary; P03 commit, exact-head publication prerequisites, push and five verified replies/resolutions remain unfinished.
* Review execution evidence: One original independent assessment on 2026-10-28 of the entire supplied child boundary. The canonical opening state above was persisted before comparison. Required review.md and review-log.md template were read.
* Method: Read the complete child research, plan, phase details, original critique, changes and session state; complete four-file diff against 618777a26bf62566a0d920c7127d3a8313b85e65; necessary unchanged demo.js, assistant.js, codec, HTTP tests, scanner and runner; and preserved parent Review. Read actual task-owned external JSON/logs, verified their hashes and current source fingerprints. No tests, browser, heavy checks, dependency installs, nested agents or remote operations were launched.
* Write boundary: Only this Review record was created/updated. No parent adverse artifact, planning artifact, source, external evidence, receipt or remote thread was changed.

## Scope and Evidence

* Task ID: 520-logout-followup; slug resident-chat-520-logout-followup; review date 2026-10-28.
* Relationship: Distinct child of 520-review-correction, on existing feat/resident-chat-520 / supplied open PR #525. This is not a repeated or closure Review of the parent.
* Assessed boundary: Delayed accepted logout cookie application across replacement login; ordinary sign-out, strict cookie/session binding, CSRF, revocation and expiry; all five original browser scenarios; existing-method/dependency budget; permitted validation; local commit and publication requirements.
* Plan: .copilot-tracking/plans/2026-10-28/resident-chat-520-logout-followup-plan.md.
* Phase details: .copilot-tracking/details/2026-10-28/resident-chat-520-logout-followup-phase-details.md.
* Original critique: .copilot-tracking/reviews/plans/2026-10-28/resident-chat-520-logout-followup-critique.md. This actual filename, not a hypothetical -plan-critique.md file, is authoritative.
* Changes: .copilot-tracking/changes/2026-10-28/resident-chat-520-logout-followup-changes.md.
* Research: .copilot-tracking/research/2026-10-28/resident-chat-520-logout-followup-research.md.
* State: .copilot-tracking/rpi-sessions/2026-10-28/resident-chat-520-logout-followup-state.json.
* Parent evidence: .copilot-tracking/reviews/logs/2026-10-28/resident-chat-520-review-correction-review.md remains Complete / Not accepted, unchanged.
* Source boundary: src/api/README.md; src/api/src/zava_forward/api/resident_demo/app.py; src/api/tests/test_resident_demo_api.py; src/api/checks/resident_assistant_browser_check.py. The complete tracked diff contains exactly those four existing files. Existing functions/methods were neither added nor removed, confirmed by comparing AST function-name multisets with HEAD. No dependency manifest changed.
* Unchanged context: src/api/src/zava_forward/api/resident_demo/web/demo.js and web/assistant.js; src/core/src/zava_forward/core/resident_showcase.py; src/api/checks/regulatory_ux_check.py; tools/rpi-checks.py; src/README.md. Case-study original/addendum, reference index/memory and housing-association primer were read for orientation; no whole-product or regulatory-currentness audit.
* Candidate identity: HEAD 618777a26bf62566a0d920c7127d3a8313b85e65 with uncommitted child changes. Local origin/feat/resident-chat-520 is 685547ed548464ebe58222e21ea3557fb53be963; local origin/main is 413ccaf253fce4566e855bae9d0a924b2a82b506. Earlier fetch/no-new-bot observations are parent-supplied; this Review did not fetch or establish current remote identity.
* Evidence attribution: Passing results below are actual retained implementation-run evidence inspected by the reviewer, not fresh reviewer executions. External paths are evidence locators, not workspace delivery artifacts. Raw partial command evidence is not a canonical receipt or exact-head publication assessment.

## Plan-to-Change Reconciliation

| Current plan scope | Descriptive changes-record summary | Current-state reconciliation | Gap or rationale |
| --- | --- | --- | --- |
| P01-T01 | Logout removes response cookie writes; existing HTTP owner and README updated | Reconciled | Admission and revocation remain unchanged; retained cookie is unusable, not an authenticated session. |
| P01-T02 | Existing shared-session harness covers both replacement identities with isolated upstream acceptance | Reconciled | Real browser cookie application is demonstrated by the inert marker, not assumed from route.fetch. |
| P02-T01 | First scan failure retained; selector corrected; final-byte Chromium/pinned-axe run passed | Reconciled | All five original scenarios plus both delayed logout identities ran. Six contrast incompletes remain disclosed. |
| P02-T02 | All project checks and permitted non-az matrix/infrastructure evidence completed | Reconciled within permitted scope | Canonical preflight and four az-dependent infrastructure modules were not executed. This is not full-gate completion. |
| P03-T01 | Evidence reconciled; original child Review ready | Completed by this record | Parent owns subsequent state/marker reconciliation; their pre-Review snapshots are not falsely marked accepted here. |
| P03-T02 | Privacy-safe commit, bot ancestry reconciliation and eligible exact-head evidence | Pending | Local commit remains authorized but unperformed. No final committed candidate or receipt exists. |
| P03-T03 | Current-main receipt verification, independent exact-head assessment, normal push, five verified replies/resolutions | Blocked / pending | RV-001. No partial evidence authorizes publication or remote thread resolution. |
| Follow-Up Items | Human/content, actual AT/native zoom and real-model acceptance; full-gate limitation | Reconciled | Human/model items remain distinct follow-ups. The full-gate limitation remains an active P03 prerequisite, not optional residual acceptance. |

The changes record retains chronological "in progress" and "no complete browser pass yet" paragraphs, then explicitly records the final successes and unchanged publication blocker. Its final handoff, plan markers, details and state agree. The state intentionally remains manual / session stopped / active Review with full-receipt-no-az. These snapshots need parent closeout after this record; they do not justify stopping this credible assessment or accepting unfinished publication.

## Completed Work Assessment

| Related marker | Files | What changed and why | Completion evidence | Validation | Assessment |
| --- | --- | --- | --- | --- | --- |
| P01-T01 | src/api/src/zava_forward/api/resident_demo/app.py:548-560 | Remove only logout's Set-Cookie tuple to eliminate shared-cookie deletion after a later login | _same_origin, _csrf_ok, _session_bound and codec.revoke precede the same signed-out JSON response | Existing HTTP owner fails against original handler and passes corrected handler | Required runtime correction supported; no new session scheme or authority. |
| P01-T01 | src/api/tests/test_resident_demo_api.py:403-420; src/api/README.md:158-163 | Assert absent response cookies, retained opaque token, verify denial, protected 401 and signed-out session; explain lifecycle | Existing thirty-minute expiry, cookie-security, CSRF and replay tests retained | Owning suite and red/green log inspected | Retaining bytes does not extend expiry or restore authentication. |
| P01-T02 | src/api/checks/resident_assistant_browser_check.py:44-66,184-268 | Forward intercepted bound request through stdlib urllib without a cookie jar; retain accepted status/body/headers; release after replacement login | Before replacement, browser cookies equal original and old-token protected read is 401; fresh sid and renewed permissions precede release | Actual different/same-resident browser states present in final report | PC-001 contract implemented without new methods/dependencies. |
| P01-T02 | Same existing shared_session_checks | Add nonauthentication __Host-logout-probe only on fulfillment, absent before and present after release | Full replacement auth-cookie dictionary including expiry is equal; CSRF equality excludes only permitted /session expiry refresh; own view/transcript/chat/callback permission preserved | Both identity cases pass; replacement protected API view also checked | Actual Chromium cookie application boundary is established, not just JavaScript ordering. |
| P02-T01 | Existing run method, src/api/checks/resident_assistant_browser_check.py:597 | Scan body during loading/manual fallback because target_sizes enumerates descendants, not selector roots | Old selector excluded the launcher root; body includes the visible target without weakening assertions | First failure retained; final report includes loading-manual-launcher-focus | Directly coupled harness fix, not an unrelated redesign. |
| P02 | Existing project suites and unchanged Runner methods | Establish permitted source/runtime compatibility | Five project suites, browser, SQL, images, migration/static and complementary infra evidence inspected | Detailed table below | Bounded engineering evidence is strong; whole-task acceptance still blocked by RV-001. |

### Necessary unchanged behavior and five original scenarios

* Session isolation: demo.js:28-49 clears stale personal state and rechecks the verified current sid rather than adopting message identity; :314-369 and :385-422 retain transition fences and ordinary logout recovery. assistant.js:322,349,366-379 retains generation/session guards and clears transcript/permission on session changes. The existing browser shared-session checks still cover cross-tab replacement, same-resident fresh sid, stale view failure and unnotified cookie replacement.
* Punctuated periods: Existing run checks morning? and afternoon? proposals, selected period, offered/excluded hours and callback focus. Corresponding final report states are present with no violations.
* Manual retry/loading focus: assistant.js:296-301 chooses a rendered callback title/email/retry, else launcher. Existing browser assertions verify retry in the error state and launcher during loading; the body scan preserves target checks.
* Typed-ahead draft: assistant.js:317-319 captures the untrimmed draft; :339 clears only the unchanged value. Existing held-response assertions preserve a different next draft and clear the unchanged one.
* Dismissed delayed appointments: assistant.js:340-342 requires the panel still be open before automatic callback search/focus. Existing Escape and outside-dismissal tests verify focus preservation, no extra agenda request, and the continued manual route.
* Ordinary sign-out: Existing run signs out while advice is pending, verifies visible sign-in and focused confirmation, then signs in another resident and verifies the late answer cannot restore transcript or permission. The added different-resident iteration also performs ordinary sign-out before resetting the same-resident case.
* Admission/security preservation: app.py:228-247 still requires a valid unrevoked cookie and exactly one lowercase 16-hex matching sid; logout retains same-origin and CSRF checks. SessionCodec.verify/revoke at src/core/src/zava_forward/core/resident_showcase.py:423-455 rejects retained/replayed sid through the token's remaining lifetime; expiry and restart constraints are unchanged. No claim of comprehensive security certification is made.

## Implementation-Time Plan and Detail Update Assessment

| Affected area | What changed and why | Triggering evidence and user decision | Reconciliation performed | Planning and critique state | Assessment |
| --- | --- | --- | --- | --- | --- |
| P01-T02 / PC-001 | Isolated urllib transport, browser cookie snapshots, fulfillment-only inert marker; auth expiry exact, CSRF expiry exception | Critique identified unsupported route.fetch cookie-isolation assumption | Plan disposition, details and implementation agree | Original critique remains Complete / Revise; direct correction adopted before source implementation per changes/state | Compatible correction; no new user decision or material divergence. |
| P03-T02/T03 / PC-002 | Explicit current-base receipt verification and independent exact-head assessment before push | Critique identified publication ordered ahead of assessment | Plan, dependencies and details now agree | Original Revise verdict preserved; direct correction adopted | No evidence of premature push/resolution; blocker remains active. |
| P02-T01 | Change loading scan selector to body | Actual first Chromium run failed because launcher was a root, not descendant target | Changes explain failure and correction; final plan/details summarize successful actual run | Existing task/harness scope; no new runtime behavior | Justified local correction, not an unaccepted plan revision. |
| P02-T01/T02 | Typed dictionary comprehensions replace dynamic-key indexing; agents fixture path corrected | Mypy diagnostic and initial agents import-name collision | Final source and recorded reruns agree; adverse logs remain | No diagnostic suppression, method addition or dependency change | Compatible implementation/validation adjustments. |
| P02/P03 | Execute permitted non-az operations; distinguish detached HEAD plus patch from full exact-head receipt | Mandatory runner preflight and infra launch az, explicitly prohibited | Plan/details/changes/state consistently retain no-az/full-receipt blocker | No new decision required to stop; no gate downgrade | Permitted evidence is useful but cannot satisfy P03 acceptance. |

The standalone root Ruff import-group probe used different configuration; project-configured Ruff passes are the relevant results. Its failure is retained, not relabeled a project pass. The raw matrix also contains two expected absent-import probes and five SQL startup/readiness failures followed by successful readiness and SQL execution. The changes prose shorthand about missing-dependency probes does not enumerate those readiness attempts; this Review records their actual classification rather than claiming 77 zero exits. No unexpected failed suite or material stale-completion claim was found.

## Critique and Material Revision Assessment

* Latest critique remains exactly one original Complete / Revise, with PC-001 and PC-002 Medium. This Review neither changes that verdict nor requests another critique.
* PC-001 disposition is supported by current source and actual final browser evidence: urllib has no cookie jar; browser cookie state is checked after upstream acceptance and before fulfillment; the inert marker proves Chromium applies Set-Cookie at release; both replacement identities retain protected state and renewed permissions.
* PC-002 disposition is supported by the corrected conditional publication sequence in both plan and details. It is not yet executed and is not accepted as completed publication.
* The logout design preserves confirmed user intent without broadening scope: no JS edits, dynamic cookie names, new runtime/test methods, method removals, dependencies or weaker admission rules.
* Dependent-work pause: The record reports PC-001/002 adopted before implementation; current source reflects them. P03 publication remains paused. No unaccepted significant decision or material planning gap requiring rpi-plan was identified.
* Parent comparison: Its source-grounded delayed-cookie defect is addressed by this child, and its missing actual-browser evidence now has a successful final-byte child run. This does not revise the parent's original Not accepted outcome or satisfy its remaining publication/human boundaries retroactively.

## Plan Follow-Up Assessment

| Follow-up item | Why outside immediate scope | Owner or next action | Assessment and route |
| --- | --- | --- | --- |
| Human resident/content acceptance | Synthetic engineering checks do not establish user/content approval | Product/resident engagement owner: arrange named acceptance separately | Open inherited follow-up; not a new logout defect or active P01/P02 task. |
| Actual AT/screen reader and native browser zoom | Axe, viewport reflow and root-font resize are not actual AT/native zoom; six contrast states are incomplete | Accessibility acceptance owner: assess retained incomplete targets and execute inherited human protocol | Open inherited follow-up; no WCAG conformance/acceptance claimed. |
| Real-model acceptance | Local synthetic workflow and rules do not establish model readiness | Resident-assistant/model acceptance owner: separately authorized evaluation | Open inherited follow-up; no Azure/paid-model activity authorized here. |
| Mandatory full-gate limitation | Not outside scope: prerequisite to active P03 publication | Validation owner: retain full-receipt-no-az until a later authorized task can establish eligible evidence | RV-001, material evidence gap; cannot be reclassified as nonblocking residual work. |

Unresolved inherited follow-ups remain separate from this child's active implementation/completion/acceptance claims. Image-scan residual risk discovered in permitted validation is routed separately as RV-002 below; it does not silently expand P01/P02.

## Findings

<!-- rpi:review id=RV-001 -->
### RV-001 [High]: Mandatory committed exact-head publication evidence is unavailable

* Related scope: P03-T02/T03; complete child acceptance and publication.
* Evidence: Current HEAD remains 618777a26bf62566a0d920c7127d3a8313b85e65 with the four source/document edits and child artifacts uncommitted. The child state records full-receipt-no-az. tools/rpi-checks.py:1322-1334 unconditionally invokes az bicep version during canonical preflight; :1436-1452 invokes az infrastructure compilation/lint. Current user direction prohibits every az invocation. Actual nonaz-results.json explicitly labels its evidence as neither a full nor partial canonical receipt; complementary infra evidence excludes four az-dependent modules. No full receipt, current-main verification, independent committed exact-head assessment, pushed fixing commit or five verified thread replies/resolutions is evidenced.
* Impact: Strong source, browser, unit, SQL and permitted infrastructure results do not satisfy the mandatory publication gate. Whole-task conformance and publication remain unaccepted; no bypass, fabricated receipt or protection change is an eligible resolution.
* Destination: rpi-research, material evidence gap, owned by validation/evidence owner. Pending local commit/publication tasks remain with the implementation/publication parent rather than being duplicated as new defects.
* Smallest useful next action: Preserve this original Review and the blocker. Parent may complete the already authorized privacy-safe local commit of implementation and dated original evidence, after resolving gh api user and deriving repository-local noreply author/committer identity with the required Copilot trailer. A later expressly authorized validation task must establish a clean committed current-base full receipt under the unchanged runner contract. Under the present no-az direction, stop publication. If later prerequisites become available, fetch current remote/main, perform only an authorized necessary bot rebase, rerun invalidated evidence, verify the external full receipt against current origin/main immediately before independent exact-head assessment and normal push. Reply with the fixing commit and resolve only the five actually verified threads afterward. No force-push, closing keyword, merge or deployment.

<!-- rpi:review id=RV-002 -->
### RV-002 [Medium]: Passing image policy retains substantial unfixed vulnerability exposure

* Related scope: P02-T02 permitted image evidence; distinct nonblocking image-maintenance follow-up.
* Evidence: Actual api-all.json, agents-all.json, orchestrator-all.json and importer-all.json under the recorded non-az output each contain 59 HIGH and two CRITICAL vulnerability entries, all without FixedVersion. Each corresponding gate report is empty under the existing --ignore-unfixed policy and its command exited successfully. Full reports and SPDX are retained; the changes record accurately discloses the limitation.
* Impact: The fixable-vulnerability gate pass does not mean vulnerability-free images, exploitation assessment, runtime safety or deployment approval. These findings are not evidence that the logout change introduced vulnerabilities, and no new exploitable defect is asserted.
* Destination: Distinct follow-up item, image/base-dependency maintenance owner; not rpi-implement for this bounded logout task and not an additional publication-gate waiver.
* Smallest useful next action: Triage the retained full-report identifiers against upstream fixes and actual consumer exposure, record owner/disposition and schedule refresh when remediation becomes available. Preserve existing scan policy and separately authorized deployment gates. This residual risk is nonblocking for the narrow logout implementation; RV-001 independently blocks whole-task publication.

## Defects

* No additional confirmed implementation defect was found within the complete child delta and necessary unchanged context.
* The parent logout response-cookie defect is corrected in this assessed child candidate; the parent's original adverse Review is unchanged.
* RV-001 is a material evidence/publication gap, not an instruction to modify the runner or redesign logout. RV-002 is distinct residual maintenance work, not a newly introduced source defect.

## Routed Findings

| Finding | Severity | Destination | Owner or next action | Reason for route |
| --- | --- | --- | --- | --- |
| RV-001 | High | rpi-research | Validation/evidence owner: retain blocker; later authorized committed exact-head full-gate evidence, then existing P03 sequence | Material acceptance/publication evidence missing. |
| RV-002 | Medium | Distinct image-maintenance follow-up | Image/base-dependency owner: triage retained unfixed full-report findings and remediation availability | Nonblocking residual risk beyond this narrow change; no policy violation or introduced defect inferred. |

Later implementation or evidence completion does not require this original Review to run again. A required later publication exact-head assessment is a distinct repository gate, not a repeat or closure RPI Review.

## Residual Work

* Inherited human/content, AT/native zoom and real-model acceptance remain with their separate owners above.
* Six color-contrast incomplete states require accessibility-owner assessment; zero automated violations is not conformance or zero unresolved findings.
* RV-002 retains image-maintenance follow-up. No unrelated source fix, framework swap or expanded runtime/test scope is authorized.

## Blockers and Remaining Work

* Active blocker: full-receipt-no-az / RV-001. Canonical full preflight and required infrastructure cannot run under the current no-az instruction. Standalone Bicep equivalence does not remove that requirement.
* P03-T01: This one Review is complete. Parent must record its result without changing original critique or parent Review outcomes.
* P03-T02: Local commit remains pending, including privacy-safe authenticated account-derived noreply identity, Conventional Commit and Copilot trailer. No commit was made by this Review. Parent reports two prior fetches with no new bot commit; no new remote fetch or rebase was performed here.
* P03-T03: Full receipt, final current-main verification, independent exact-head assessment, normal push and all five verified replies/resolutions remain pending/ineligible. This Review does not verify thread IDs/current remote state or authorize their mutation.
* No Azure, secrets, .env, private dataset, merge, deployment, force-push, runner/protection changes or PR-body closing keyword was used by this Review.

## Validation Evidence

| Command or evidence | Scope | Status | Summary |
| --- | --- | --- | --- |
| Existing owning logout/binding HTTP regressions | P01 server correction | Passed, retained evidence | Three focused tests reported; inspected owning regression source and actual negative/positive log. No reviewer rerun. |
| Existing SessionTests.test_logout_revokes_and_replay_fails against original/corrected handler | Regression specificity | Failed as expected / Passed | logout-red-green.log shows original destructive Set-Cookie fails the new assertion; corrected handler passes. Original HEAD diff corroborates the deleted tuple; no new test method. |
| Existing resident_assistant_browser_check --axe | All five original scenarios plus both delayed logout identities | Passed, actual retained evidence | Chromium 156.0.8078.4; hash-pinned axe 4.10.3; 31 states; zero violations; six color-contrast incomplete states; zero page errors/external requests. Final report hash verified below. |
| First actual child browser run | Complete original harness before scan correction | Failed, retained | Two 60-second busy admissions before acquisition at 19:21:01Z; no interactive descendants for #main, #chat-launcher. Final body scan fixes the selector without weakening scanner assertions. |
| Core unittest discover / configured Ruff100 / format100 / mypy | src/core | Passed | 1454 tests, 190 general-discovery skips; 103 formatted files; mypy 156 files. |
| Agents corrected unittest discover / configured Ruff100 / format100 / mypy | src/agents | Passed | 116 tests, zero skips; 20 formatted files; mypy 24 files. Initial import collision remains in agents.log; corrected core-only fixture path succeeds. |
| API unittest discover / configured Ruff100 / format100 / mypy | src/api | Passed | 1167 tests, 314 general-discovery skips; 50 formatted files; mypy 94 files. |
| Orchestrator unittest discover / configured Ruff100 / format100 / mypy | src/orchestrator | Passed | 46 tests, zero skips; nine formatted files; mypy 12 files. |
| Importer unittest discover / configured Ruff100 / format100 / mypy | src/importer | Passed | 39 tests, zero skips; 11 formatted files; mypy 10 files. |
| Five-project aggregate | Existing installed project suites | Passed with disclosed skips | 2822 tests including 504 general-discovery opt-in skips, not 2822 unskipped tests. General skips do not substitute for actual integration selectors. |
| Unchanged Runner namespace/static/migration/browser/mssql/image/logo methods | Permitted non-az matrix | Passed within boundary | 77 recorded commands; ten passed groups; all command log hashes verified. Two expected absent-import probe failures and five SQL readiness failures precede successful setup; failures list empty. No unexpected failed suite. |
| Real owned loopback SQL | Existing integration selectors | Passed with one enumerated nonapplicability | 263 tests; only test_mssqlstore.MssqlHazardReferral.test_json_postsave_audit_failure_reports_persisted_uncertainty skipped for JSON-only separate-file audit ordering. Cleanup log removes the exact owned container. |
| Four image contracts/scans and logo0600 | Existing consumer contracts | Passed policy, limited | Fixable HIGH/CRITICAL gates pass. Full reports each retain 59 HIGH/two CRITICAL unfixed entries; RV-002. |
| Complementary standalone Bicep / runner infra Ruff100, format/types / non-az tests | Permitted infrastructure | Passed within boundary | 26 builds plus 26 lints; 15 recorded static/type commands; all 67 command-log hashes verified; 379 tests, zero failures/errors/skips; no attempted az launches recorded. |
| Four az-dependent infrastructure modules and canonical preflight | Full-gate requirements | Unavailable / not run | test_bicep_policy, test_iothub_module, test_resident_assistant, test_resident_demo_deploy excluded explicitly; az forbidden. RV-001. |
| JS syntax and common browser/regulatory checks | Existing unchanged JS plus matrix checks | Passed, recorded | Matrix static/browser command logs match hashes. These are engineering checks, not whole-product acceptance. |
| Source/patch/runner provenance | Candidate versus retained evidence | Verified by reviewer | Four current source fingerprints equal final-browser summary; source.patch hash and complete four-file diff match exactly; detached checkout's four files match candidate; runner source is unchanged. |
| Canonical full receipt/current-main verification/independent exact-head publication assessment | Clean committed final candidate | Not available | Raw command output and detached HEAD plus patch are not receipt coverage. API venv editables target byte-identical working candidate source, not a hermetic exact-head publication claim. |
| Fresh Web Interface Guidelines | Bounded behavioral delta and necessary unchanged JS | Source fetched completely | Successfully retrieved https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md before guideline assessment. No JS/HTML/CSS changes in this child; no fresh whole-interface/accessibility conformance claim. |
| Human/content, AT/native zoom, real model, hosted acceptance | Separate acceptance | Not performed / not claimed | Engineering checks do not replace these inherited gates. |

### Evidence integrity and admission

The following actual evidence locators were read, not modified:

* /tmp/ama-520-logout-validation-20261028/browser-evidence-summary.json: SHA-256 bcda723882867fadf8b3fa27d35a283290586132e7652e6bd09f3a3b779ce479. Its four source hashes match the current candidate.
* /tmp/ama-520-logout-browser-20261028-3/report.json: SHA-256 de24204cef6e56d1da5e76029d51b548b0ef66570ae4896e95eac7a9f0a4aaf8. All 31 state rows were inspected. Both delayed identities, draft preservation, both dismissal modes, punctuated periods, retry and loading focus are present.
* Pinned axe bytes in the non-az output hash to 880970c081707360e64f34cea25ff91892f5bc95675b0776925b9709dd8a68bb, matching the browser summary and scanner's 4.10.3 contract.
* /tmp/ama-520-logout-validation-20261028/{core,agents,agents-corrected,api,orchestrator,importer,logout-red-green}.log: Actual results and retained initial agents failure inspected.
* /tmp/ama-520-logout-browser-20261028-1/command.log: Original loading-scan failure and 60-second busy admission evidence inspected.
* /tmp/ama-520-logout-nonaz-20261028-1/nonaz-results.json: SHA-256 79cfef8ab5546c30764a77d5d2ac4cd280d0634cd14301e08a7525e1bd7d5ccc; base 413ccaf253fce4566e855bae9d0a924b2a82b506; candidate HEAD 618777a26bf62566a0d920c7127d3a8313b85e65 plus exact source.patch SHA-256 1876193fe692ca2f18f9f4b8120aa8d6aed4cd2f0de26a68d9df582f0032bebe. All 77 referenced command logs exist and match their hashes.
* /tmp/ama-520-logout-nonaz-infra-20261028-1/nonaz-infra-results.json: SHA-256 dd36230bd922a118d9f6e5eaa0e0ce8e40ef723c9ec56a3a5708953865ffb143. All 67 referenced command logs exist and match their hashes; infra-tests.log agrees with 379 tests/zero skips.
* Matching matrix/infra aggregate logs show admitted runs, including final resident chat browser success in the matrix log. Initial browser lock acquisition follows two busy 60-second retries; complementary infrastructure acquisition follows three. The required contract is nonblocking shared lock with 60-second retries for at most 60 minutes; no timeout exhaustion or foreign interruption is evidenced for these successful child runs. Actual lock ownership throughout execution is parent-recorded, not independently reconstructed from a lock operation by this reviewer.

The six incomplete states are anonymous, document-facts, document-facts-320-text-200, signed-in-chat, typed-ahead-draft-preserved and page-error-help; every incomplete rule ID is color-contrast. They are six state-level incomplete results, not necessarily six DOM nodes. Current source is unchanged from the final-browser fingerprints. Historical failures, task-created external generated metadata and raw reports remain preserved; no generated input or evidence was cleaned up by this Review.

### Web Interface Guidelines findings

#### src/api/src/zava_forward/api/resident_demo/web/demo.js

No additional substantive guideline defect found within the necessary unchanged session/logout context and this child's behavior-only correction. The parent cookie-side-effect finding is removed at app.py:560, not by weakening the JavaScript fence.

#### src/api/src/zava_forward/api/resident_demo/web/assistant.js

No additional substantive guideline defect found within the five specified unchanged scenario guards. Native controls, focus routes, status/log semantics and generation checks remain. No typography, animation, image, layout, framework, locale or form-markup change is introduced. Six automated contrast incompletes and absent human/AT/native-zoom acceptance remain limitations, not a file:line defect invented without evidence.

## Outcome

* Outcome: Not accepted.
* Review execution: Complete; implementation execution: Partial.
* Severity summary: 0 Critical, 1 High, 1 Medium, 0 Low. RV-001 is the blocking material evidence gap; RV-002 is a nonblocking residual-maintenance finding.
* Rationale: The narrow logout correction and all-five/both-identity browser evidence are supported, with no additional confirmed source defect. Permitted unit/static/type/browser/SQL/image/infrastructure evidence is substantial and accurately bounded. However, mandatory committed current-base full-receipt publication evidence and publication steps are missing and blocked by explicit no-az direction. A conformant whole-task outcome, push or thread resolution cannot be inferred. The parent's original Not accepted Review and this child's original Revise critique remain unchanged.

## Closeout Routing Record

| Finding class | Destination | Owner or next action |
| --- | --- | --- |
| Implementation defect | None | No new confirmed child implementation defect. Parent owns existing pending local commit and P03 tasks. |
| Decision gap or invalid assumption | None | No unresolved significant decision requiring rpi-plan; preserve no-az and full-gate boundaries. |
| Material evidence gap | rpi-research | RV-001: validation owner retains blocker; later expressly authorized clean committed current-base full-receipt evidence, then existing exact-head publication sequence. |
| Nonblocking residual work | Distinct follow-up owners | RV-002 image maintenance; inherited product/resident, accessibility and model acceptance owners, outside active logout implementation. |

* Review execution status: Complete.
* Outcome: Not accepted.
* Validation coverage: Final-source actual Chromium/pinned axe, all five project suites/static/types, 77 non-az matrix commands, real SQL, images and 67 complementary infra commands were inspected; evidence hashes and four-file candidate fingerprints verified. No fresh tests or heavy checks were run by this reviewer.
* Blockers: full-receipt-no-az; uncommitted candidate; current-base exact-head publication evidence, push and five verified thread replies/resolutions pending.
* Parent continuation: This is the child's one original Review. Preserve adverse outcomes, reconcile state without marking blocked work accepted, complete only eligible local work, and do not relaunch Review or bypass the gate.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/research/2026-10-28/resident-chat-520-logout-followup-research.md](.copilot-tracking/research/2026-10-28/resident-chat-520-logout-followup-research.md) | Child evidence and bounded direction |
| [.copilot-tracking/plans/2026-10-28/resident-chat-520-logout-followup-plan.md](.copilot-tracking/plans/2026-10-28/resident-chat-520-logout-followup-plan.md) | Reconciled requirements, tasks and follow-ups |
| [.copilot-tracking/details/2026-10-28/resident-chat-520-logout-followup-phase-details.md](.copilot-tracking/details/2026-10-28/resident-chat-520-logout-followup-phase-details.md) | Execution contracts and validation limits |
| [.copilot-tracking/reviews/plans/2026-10-28/resident-chat-520-logout-followup-critique.md](.copilot-tracking/reviews/plans/2026-10-28/resident-chat-520-logout-followup-critique.md) | Preserved original Complete / Revise critique |
| [.copilot-tracking/changes/2026-10-28/resident-chat-520-logout-followup-changes.md](.copilot-tracking/changes/2026-10-28/resident-chat-520-logout-followup-changes.md) | Implementation, adverse history and actual validation |
| [.copilot-tracking/rpi-sessions/2026-10-28/resident-chat-520-logout-followup-state.json](.copilot-tracking/rpi-sessions/2026-10-28/resident-chat-520-logout-followup-state.json) | Manual Review handoff and full-receipt blocker |
| [.copilot-tracking/reviews/logs/2026-10-28/resident-chat-520-review-correction-review.md](.copilot-tracking/reviews/logs/2026-10-28/resident-chat-520-review-correction-review.md) | Unchanged original adverse parent Review |
| [.copilot-tracking/reviews/logs/2026-10-28/resident-chat-520-logout-followup-review.md](.copilot-tracking/reviews/logs/2026-10-28/resident-chat-520-logout-followup-review.md) | This single original child Review |

## Next Steps

Active parent: record Complete / Not accepted, preserve original critique/parent outcomes, and finish only the authorized privacy-safe local commit and state reconciliation. Route RV-001 to later authorized rpi-research evidence work and RV-002 to the distinct image-maintenance owner. Under current no-az direction, keep publication and all five replies/resolutions blocked; do not modify the runner, fabricate a receipt or repeat this Review. Inherited human/content, AT/native zoom and model acceptance remain separate.

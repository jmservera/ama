---
title: Case journey UX 526 correction original RPI Review
description: Independent bounded original Review for issue 526 and PR 529
ms.date: 2026-10-28
---

## Opening Review State

* Interpreted review goal: independently assess the seven correction requirements, implementation root causes, asynchronous ownership, tests and guide changes.
* Review scope: task 526-correction, parent issue #526, PR #529; eight supplied files against d3fbba5807d574136bc77307b4e95c2fec657654.
* Evidence readiness: supplied research, plan, phase details, critique and changes paths identified; substantive comparison pending. HEAD and eight-file diff SHA256 confirmed as supplied: bfac509bb360f234ada27986406f0b6fce060890918d64f00714650357b41b40.
* Acceptance basis: seven research thread requirements; current plan and critique dispositions; bounded web interface rules; recorded local validation, not human/live acceptance.
* First comparison boundary: reconcile plan markers, critique dispositions and implementation evidence, then inspect source/test/guide diff and relevant unchanged context.
* Active read-only boundaries: write only this record; no source, plan, details, changes, state or other artifact edits; no subagents, remote mutations, Azure, secrets, private data or heavy tests.
* Initial blockers: complete publication gate cannot run under the explicit no-az instruction; no push, thread resolution or end-to-end conformance claim is authorized.

## Execution Status

* Execution status: Complete
* Review execution evidence: one independent original Review on 2026-10-28; no subagents. All five supplied artifacts, eight-file diff, relevant unchanged call-site context, browser result summaries and upstream web rules compared. Two defects independently reproduced using shipped JavaScript helpers with bounded control stubs, not a claimed browser rerun.

## Scope and Evidence

* Task: 526-correction; parent issue #526; PR #529.
* Branch: feat/case-journey-ux-526. HEAD: d3fbba5807d574136bc77307b4e95c2fec657654.
* Assessed candidate: dirty implementation diff against that HEAD, restricted to src/api/src/zava_forward/api/web/app.js, src/api/src/zava_forward/api/web/assistants.js, src/api/src/zava_forward/api/web/ops.js, src/api/src/zava_forward/api/web/panels.js, src/api/checks/case_journey_browser_check.py, src/api/checks/assistants_browser_check.py, src/api/tests/test_case_journey.py and src/api/README.md.
* Eight-file diff SHA256 independently confirmed before and after checks: bfac509bb360f234ada27986406f0b6fce060890918d64f00714650357b41b40.
* Inputs: supplied correction research, plan, phase details, original plan critique and changes record, all dated 2026-10-28.
* Context: original case study, addendum, reference index and owner memory; relevant content standard and WCAG baseline. Memory is context, not acceptance evidence.
* External evidence inspected read-only: correction-validation/journey-09.log, journey-09/results.json, assistants-02.log, api-unit.log and focused-final.log under the supplied session files root. External paths are evidence references, not committed artifacts or new Review outputs.
* Boundary excludes unrelated legacy style, redesign, deployment and regulatory/legal acceptance. No remote lifecycle recheck or mutation was needed; PR association is supplied and corroborated by the original critique, not fresh remote-head attestation.

## Plan-to-Change Reconciliation

| Current plan scope | Changes summary | Current-state reconciliation | Gap or rationale |
| --- | --- | --- | --- |
| P01-T01 | Complete document output retained; successful Edit displays dispatch-time replacement | Reconciled | Review model and handlers remain in the session-owned output node; upload form is rebuilt. |
| P01-T02 | Session proposal cache and action-aware cleanup | Reconciled | Connected loader restores current session cache; detached loader cannot consume it. Verification does not clean unsent JSON. |
| P01-T03 | Immutable upload/handoff/resident snapshots and file handling | Reconciled | Pre-await values, later-change comparison, copyable vanished-form edits and file-object comparison address dispatch races. |
| P01-T04 | Checklist and funding identity isolation | Partial | Funding isolation is supported; initial checklist restoration is covered, but recovery ownership and submission cleanup remain defective, RV-001/RV-002. P01 complete overstates this acceptance boundary. |
| P02-T01 | Existing browser checks, units, static checks and guide | Reconciled with coverage limitation | Recorded checks passed; checklist scenarios omit the two transitions identified below. |
| P02-T02 | Original independent Review and local commit | Review now executed; parent continuation pending | Original adverse outcome must be preserved; Review completion is not acceptance. |
| P02-T03 | Complete gate, exact-head publication and thread resolution | Blocked as explicitly planned | Required gate invokes prohibited az. No receipt, push or thread-resolution completion is supported. |

## Completed Work Assessment

| Requirement/thread | Files and root-cause assessment | Evidence and assessment |
| --- | --- | --- |
| PRRT_kwDOUU8JX86xUr6L: full document review survives call/proposal refresh | app.js:562-580,1117-1156 | Session retains the output node, record identity, editable controls and handlers rather than just field strings. Browser regression compares node identity and retained text/reason after both refresh paths. Supported. |
| PRRT_kwDOUU8JX86xUr6p: submitted Edit wording displayed | app.js:322-337,1136-1146 | Text/reason captured before await; callback displays the submitted replacement, not a later live value. Browser asserts successful real review and read-only displayed replacement. Supported. |
| PRRT_kwDOUU8JX86xUr7A: overlapping proposal snapshots retained | app.js:758-764; assistants.js:85-148 | Cache persists across redraws; live clean controls remove only their keys, absent pending controls do not erase them. Loader current() excludes detached/wrong-route panels. Browser holds two loads and checks retained JSON/reason. Supported. |
| PRRT_kwDOUU8JX86xUr7q: later mutation edits preserved | app.js:581-593,903-910,942-986,1117-1132; panels.js:147-166 | Snapshot is taken before mutation/FileReader; handoff mutation runs inside refresh; resident passes immutable snapshots. File-object identity detects same-name replacements. Held-response tests cover request values versus later dirty text/files and vanished handoff recovery. Supported for the named mutation forms. |
| PRRT_kwDOUU8JX86xUr8F: async checklist restoration restricted to measure/version | ops.js:89-118; app.js:758-803 | Explicit measure/version/item keys prevent transplanting evidence; async construction restores the current measure. But later recovered-measure edits can be overwritten and unrelated recovery can be marked submitted. RV-001/RV-002 prevent acceptance. |
| PRRT_kwDOUU8JX86xUr8k: old funding edits not mapped onto new AI record | app.js:1160-1194 | Funding identity includes record_id/manual initial identity; old text becomes copyable recovery without stale review actions. Browser exercises two record identities, fresh wording, another refresh and explicit discard. Supported. |
| PRRT_kwDOUU8JX86xUr9C: own verification preserves unsent JSON | assistants.js:27-38 | Cleanup covers note plus action-specific submitted fields, not every proposal editor. Revision-keyed recovery retains unsent JSON after verification advances the revision. Browser checks recovery and another refresh. Supported. |
| Stepper and authority boundaries | case-workspace.js; existing browser assertions | Stepper file has no diff. No API/domain/schema/permission changes. Server source verification remains enforced; the document test obtains fresh evidence after a call rather than bypassing stale-source rejection. Supported within inspected scope. |

## Implementation-Time Plan and Detail Update Assessment

| Affected scope | Change and trigger | Reconciliation and assessment |
| --- | --- | --- |
| P01-T03 | Retain later selected file nodes and recover later edits after successful handoff removes its form | Details and changes explain this tightly coupled completion of the named preservation requirement. No new feature, authority or divergent user decision. File identity regression covers same-name replacement semantics. |
| P01-T04 | Separate other-measure/version and funding drafts into copyable recovery | Research, details and changes describe the identity-preserving design. Direction is compatible, but implementation introduces the two untested checklist defects below. |
| P02-T01 | Fixture/helper extraction, nullable browser request bodies and source-hash-sensitive document test adjusted after failed attempts | Changes preserves failed attempts and corrective rationale. Existing runner ownership, no removals and helper cap remain respected: one new journey helper, no new assistant helper or runner. No scope-changing revision requiring a new critique was identified. |
| P02-T03 | Explicit complete-gate conflict and exact-head fail-closed publication sequence | Current plan/details/changes agree. The local guide's smaller-tier discussion does not override the supplied repository-wide complete-gate requirement. No material unresolved planning decision justifies relaxing it. |

## Critique and Material Revision Assessment

* Original critique remains Complete / Revise, with 3 High findings; this Review does not rewrite it.
* PC-001 remains rejected under the parent's recorded disposition: its purported parent /tmp prohibition conflicts with the explicit owner lock instruction. Historical recorded browser admission is retained as supplied evidence; this reviewer neither opens that lock nor reruns browsers.
* PC-002 is accepted and reconciled: tools/rpi-checks.py preflight invokes az bicep version; infrastructure invokes az bicep build/lint. The no-az instruction blocks the complete gate, publication and thread resolution. No gate was launched.
* PC-003 is accepted and reconciled: unresolved in-scope Review defects block publication; local candidate/evidence commit precedes the required gate; clean exact HEAD/current-main receipt verification and independent exact-head assessment remain prerequisites.
* Permitted implementation/local validation could proceed without waiting for blocked publication. No evidence of premature push, thread resolution or claimed exact-head acceptance appears in the supplied correction record.
* New Review findings route to later implementation, not another original Review or silent rewriting of completed markers.

## Plan Follow-Up Assessment

| Follow-up | Why outside immediate scope | Owner or next action | Assessment |
| --- | --- | --- | --- |
| Screen-reader acceptance | Automated axe/keyboard checks cannot establish assistive-technology usability | Owner arranges representative human screen-reader assessment | Distinct follow-up; unchecked. |
| Staff usability | Synthetic regression does not establish real staff workflow acceptance | Owner arranges staff evaluation | Distinct follow-up; unchecked. |
| Postdeployment/live and hosted acceptance | No deployment or hosted approval is performed here | Owner/release parent obtains authorized environment and hosted evidence | Distinct follow-up; unchecked. |

These are not active implementation defects or additions to the correction's scope. Publication's required gate is separately blocking active P02-T03, not a deferrable human-acceptance item.

## Findings

<!-- rpi:review id=RV-001 -->
### RV-001 [High]: Returning to a recovered checklist measure loses later evidence edits

* Related scope: P01-T04; checklist measure/version isolation.
* Evidence: src/api/src/zava_forward/api/web/ops.js:89-107; src/api/src/zava_forward/api/web/app.js:758-764,783-803.
* Reproduction: enter evidence for measure A, switch to B, refresh the case so A becomes a read-only recovery entry, switch back to A, edit the restored live evidence, then refresh or switch measures again. Measure repaint replaces only the checks container, leaving A's recovery textarea in the form. Both controls now have the same preserved key. DOM-order capture stores the live input first and the stale recovery textarea last; the latter overwrites the newer text in pendingFields.
* Independent lightweight evidence: evaluated the shipped caseFieldEntries/captureCaseFields/rememberCaseFields helpers in Node with the two controls created by that flow. Live value "New depth typed after switching back" was captured as "Earlier depth".
* Impact: silently loses new inspection evidence during the same-measure/version recovery path this correction promises to preserve.
* Destination: later rpi-implement; blocks current-scope acceptance and publication.
* Smallest useful next action: reconcile/remove recovery controls when their semantic identity becomes live, enforce live-control precedence for duplicate keys, and extend the existing journey browser check with A -> B -> refresh -> A -> edit -> refresh. Keep measure/version isolation.

<!-- rpi:review id=RV-002 -->
### RV-002 [High]: Saving one measure clears unsent recovery evidence for other measures

* Related scope: P01-T04; preservation of different-measure/version drafts.
* Evidence: src/api/src/zava_forward/api/web/ops.js:107,117-118 appends recovery textareas inside form, sends only checks inputs, but passes every form input/textarea/select as submitted. src/api/src/zava_forward/api/web/app.js:583-588 marks each unchanged submitted control clean; app.js:758-764 then deletes its pending snapshot.
* Reproduction: enter measure A evidence, switch to B, refresh so A appears as copyable recovery, complete valid B evidence and save B successfully. The recovery textarea for A is included in submitted even though A is absent from the request body. Success marks A clean and the redraw deletes it from the pending cache, so it disappears without explicit discard.
* Independent lightweight evidence: evaluated the shipped snapshot/comparison/cache helpers using the exact payload/submitted selection mismatch. Payload contained only B; A's recovery lost its dirty marker and remaining pending snapshots were empty.
* Impact: silently discards unsubmitted inspection evidence for another measure/version when saving unrelated work.
* Destination: later rpi-implement; blocks current-scope acceptance and publication.
* Smallest useful next action: restrict successful cleanup to controls actually represented in the quality-submit payload, excluding all recovery controls. Extend the existing journey browser check to save B with recovered A present and assert A remains copyable and dirty across a further refresh; also cover older-version recovery.

## Defects

* RV-001 and RV-002: 2 High implementation defects, no Critical/Medium/Low code findings. Both fit the accepted identity-bound preservation direction.
* Existing passing checks do not refute these defects: measure switching is tested before a recovery block exists; changed-version recovery is tested without subsequently switching back/editing or successfully saving unrelated evidence.

## Fresh Web Interface Guidelines Review

* Successfully fetched the complete raw upstream https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md on 2026-10-28 using web_fetch immediately for this Review. No partial retrieval or unavailable skill.
* Inspected changed web surfaces and their relevant surrounding rendering/handler code against all applicable rules: accessibility/semantics and live updates; focus; forms and unsaved state; animation/reduced motion; typography; long/empty content; performance; navigation/state; touch; layout; theming; locale; hydration; hover/interactive states; copy and listed anti-patterns.
* Native labels, details/buttons, status/alert semantics, names/autocomplete on added controls, existing dirty navigation warnings and unchanged focus/style tokens are retained. Repository ASCII/plain-language and existing design-system rules take precedence over upstream smart punctuation/title-case aesthetic preferences.
* No new image/media/animation/theme/locale/hydration implementation is introduced; those rules have no new applicable change. No unrelated legacy style findings or redesign is included. No claim that unchanged whole-app legacy surfaces comply with every upstream preference.

### src/api/src/zava_forward/api/web/app.js

src/api/src/zava_forward/api/web/app.js:763 - stale recovery control overwrites newer live same-identity edits; RV-001.

### src/api/src/zava_forward/api/web/ops.js

src/api/src/zava_forward/api/web/ops.js:101 - measure repaint restores live input without reconciling its earlier recovery control; RV-001.

src/api/src/zava_forward/api/web/ops.js:107 - recovery textareas enter the form-wide submitted selection at line 118 although excluded from payload; unrelated unsent evidence is discarded; RV-002.

### src/api/src/zava_forward/api/web/assistants.js

No additional new in-scope web-rule finding.

### src/api/src/zava_forward/api/web/panels.js

No additional new in-scope web-rule finding.

The state-preservation findings above are the substantive changed-surface findings, not separate duplicate design tickets. Automated scans do not establish complete UI or accessibility conformance.

## Routed Findings

| Finding | Destination | Owner or next action | Reason |
| --- | --- | --- | --- |
| RV-001 | Later rpi-implement | Parent assigns checklist recovery/live-control reconciliation and existing-runner regression | Implementation ownership defect within accepted requirements |
| RV-002 | Later rpi-implement | Parent restricts cleanup to submitted evidence and adds successful unrelated-save regression | Implementation payload/cleanup mismatch |

Later implementation does not require another original Review. Preserve this complete original finding set and adverse outcome.

## Residual Work

* Distinct owner follow-ups: human screen-reader, staff usability and authorized postdeployment/live/hosted acceptance, as above.
* No additional rpi-plan decision gap or rpi-research evidence gap is needed to establish the two reproducible defects.

## Blockers and Remaining Work

* RV-001/RV-002 leave P01-T04 substantively incomplete despite its current checked marker. Parent must reconcile future implementation evidence without changing this original verdict.
* P02-T02 local commit is parent-owned and still pending at review time. It is not a push authorization or acceptance.
* P02-T03 remains blocked: mandatory complete --all gate invokes prohibited az. No compliant receipt exists for this dirty candidate/current base/exact final HEAD. Do not execute prohibited commands, substitute a focused gate, fabricate a receipt, alter protections, push or resolve threads.
* After defects and gate incompatibility are legitimately resolved, publication still requires clean committed candidate/evidence, fresh main fetch, required external full-gate receipt, current-base receipt verification and independent exact-head assessment. Every later candidate/base/tool/image/input change invalidates prior gate evidence.

## Validation Evidence

| Check | Status | Evidence and limitations |
| --- | --- | --- |
| Eight-file diff identity and stepper boundary | Passed, independently checked | SHA256 matches supplied identity before/after review checks; case-workspace.js unchanged. |
| git diff --check | Passed, independently run | No whitespace errors in current diff. |
| Focused test_case_journey | Passed, independently run | From src/api: PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=tests:../core/tests:../agents/tests ../../.venv/bin/python -B -m unittest test_case_journey -q; 9 tests, 1.590 seconds, no skips. |
| Node syntax | Passed, independently run | node --check on app.js, assistants.js, ops.js and panels.js. |
| Two checklist ownership reproductions | Defects reproduced, independently run | Node evaluates shipped caseFieldEntries, snapshotCaseFields, caseFieldUnchanged, captureCaseFields and rememberCaseFields with bounded control stubs; does not claim DOM/browser end-to-end execution. No scratch artifact written. |
| Full API discovery | Recorded pass, log verified | 1158 tests / 314 skips, 443.683 seconds, OK. Not rerun. |
| Final affected suites | Recorded pass, log verified | 212 tests / 51 skips, 52.199 seconds, OK. Not rerun. |
| Final semantics | Recorded pass | Supplied changes/user evidence: 24 tests, no skips. Not independently rerun as that exact selector. |
| API Ruff/format and mypy | Recorded pass | Changes records Ruff clean, 48 formatted files, mypy 94 source files; not independently rerun. |
| Journey Chromium/axe | Recorded pass, results/log inspected | 141 PASS assertions; Chromium 156.0.8078.4; axe 4.10.3; 38 scans, zero detected violations, page_errors empty; real chrome.tabs.setZoom=2. Not rerun. |
| Axe manual/incomplete results | Unresolved human checks, not a scan failure | color-contrast incomplete entries occur in 37 scans; inspected example is non-text decorative step glyphs. Zero violations does not mean all contrast checks completed or human acceptance passed. |
| Assistant browser | Recorded pass, log inspected | 30 checks; synthetic provider; no page errors. Log also retains server BrokenPipeError during unavailable/timed-out requests; not concealed or treated as a browser-check failure. |
| Heavy admission | Recorded, not rerun here | Parent changes records flock -n shared lock, 15-second retries/2400-second bound, immediate release. Review does not create/open the lock. |
| Complete publication gate | Blocked/not run | Explicit no-az conflicts with required preflight/build/lint. No alternative tier or cloud fallback used. |
| Human/live/hosted acceptance | Not performed/unchecked | No screen-reader/staff/live deployment or hosted approval claim. |

## Outcome

* Outcome: Not accepted.
* Execution: Complete. The original independent Review finished; implementation acceptance did not.
* Severity summary: 0 Critical, 2 High, 0 Medium, 0 Low substantive implementation findings.
* Rationale: six named correction requirements have credible local source/test support; checklist identity isolation is initially implemented but still loses unsent evidence through two reproducible ownership/cleanup paths. Passing recorded local tests leave those transitions uncovered. Publication is separately blocked by the required full-gate/no-az conflict.
* This is neither end-to-end conformance nor a fresh clean committed/exact-head publication assessment. The uncommitted eight-file diff is the reviewed boundary.

## Closeout Routing Record

| Finding class | Destination | Owner or next action |
| --- | --- | --- |
| Implementation defects | Later rpi-implement | Parent addresses RV-001/RV-002 and adds existing-runner regressions; preserve this outcome. |
| Decision gap or invalid assumption | None newly identified | Existing fail-closed publication plan remains valid. |
| Material research evidence gap | None newly identified | Do not relabel missing gate authority as a research pass. |
| Non-blocking residual work | Distinct owner acceptance follow-ups | Human screen-reader/staff and authorized postdeployment/live/hosted evaluation. |

* Review execution status: Complete.
* Outcome: Not accepted.
* Validation coverage: independent bounded source/artifact review, 9 focused tests, 4 syntax checks, diff identity/hygiene and 2 reproductions; supplied broader local logs assessed with skips/manual limitations retained.
* Blockers: RV-001/RV-002 plus mandatory complete gate unavailable under no-az; no push/thread-resolution authority inferred.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/research/2026-10-28/case-journey-ux-526-correction-research.md](.copilot-tracking/research/2026-10-28/case-journey-ux-526-correction-research.md) | Seven-thread evidence and requirements |
| [.copilot-tracking/plans/2026-10-28/case-journey-ux-526-correction-plan.md](.copilot-tracking/plans/2026-10-28/case-journey-ux-526-correction-plan.md) | Assessed plan and dispositions |
| [.copilot-tracking/details/2026-10-28/case-journey-ux-526-correction-phase-details.md](.copilot-tracking/details/2026-10-28/case-journey-ux-526-correction-phase-details.md) | Assessed task details |
| [.copilot-tracking/reviews/plans/2026-10-28/case-journey-ux-526-correction-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-28/case-journey-ux-526-correction-plan-critique.md) | Preserved original Revise |
| [.copilot-tracking/changes/2026-10-28/case-journey-ux-526-correction-changes.md](.copilot-tracking/changes/2026-10-28/case-journey-ux-526-correction-changes.md) | Implementation and recorded validation |
| [.copilot-tracking/reviews/logs/2026-10-28/case-journey-ux-526-correction-review.md](.copilot-tracking/reviews/logs/2026-10-28/case-journey-ux-526-correction-review.md) | This single independent original Review |

## Next Steps

Return to the active parent for later rpi-implement work on RV-001/RV-002 and evidence reconciliation. A safe local commit may preserve the candidate and this adverse Review, but no push or thread resolution is eligible without resolved in-scope defects and compliant complete-gate/current-base/exact-head evidence. Keep human/live acceptance unchecked. No second original Review or nested delegation is requested.

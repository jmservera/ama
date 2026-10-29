---
title: Case journey 526 round 6 independent RPI Review
description: Sole bounded post-implementation review for PR 529
ms.date: 2026-10-28
---

## Scope and Evidence

* Task: 526-pr529-round6-20261028; PR #529; Refs #526.
* Intake date: 2026-10-28. Actual execution: 2026-10-29 UTC, after midnight.
* Boundary: final uncommitted API changes against HEAD 91caef1c413764aacea2da492368a72bb4366c6f on feat/case-journey-ux-526, plus the requested PR-changed sibling web audit.
* Initial API diff SHA256 verified: 142e451dc07f5602412e88ee3aa025d27d0bfef53c9f40bba02e6dcd84bf64f4.

## Opening Review State

* Goal: independently compare the supplied implementation, accepted intent, canonical artifacts and actual validation evidence once.
* Scope: editor-only malformed-JSON errors; pending submission reconciliation; sibling form error, recovery, isolation and mutation/reload behavior.
* Evidence readiness: state resolves one research/plan/details/critique/changes set; supplied evidence locations and diff fingerprint available. Detailed comparison pending.
* Acceptance basis: supplied requirements, current plan markers and critique dispositions; freshly retrieved Web Interface Guidelines.
* First comparison boundary: canonical artifact reconciliation, then complete supplied API diff and sibling audit matrix.
* Read-only boundaries: write only this record; no source fixes, other agents, Azure, secrets/private datasets, GitHub mutation, publication or heavy gate execution.
* Initial blockers: none to bounded review; full publication gate expressly outside authority.

## Execution Status

* Execution status: Complete.
* Execution window: 2026-10-29, approximately 00:15-00:20 UTC; the intake date and canonical artifact directory remain 2026-10-28.
* Outcome: Not accepted. One Medium scoped sibling defect remains; the two primary corrections have supporting implementation and passing regression evidence.
* Exactly one Review was executed. No fixes, second Review, delegation, Azure operation, GitHub operation, commit or push was performed. Prior critique and implementation failure outcomes were not changed.

## Assessed Boundary and Context

* Eight modified API files: README.md; checks/assistants_browser_check.py; checks/case_journey_browser_check.py; tests/test_case_journey.py; src/zava_forward/api/web/app.js, assistants.js, ops.js and panels.js, all under src/api.
* Additional PR-changed web audit: chat.js, case-workspace.js, index.html and style.css under src/api/src/zava_forward/api/web. The locally available origin/main comparison confirms these eight web files; it is not a fresh remote-base assessment.
* Read the canonical state-resolved research, plan, phase details, original sole critique and changes record. Project context included docs/case_study_48_original.md, relevant addendum framing, docs/reference/README.md, owner memory, housing-association primer, src/README.md local gate, src/api/README.md, component tooling configuration and the design-system/WCAG/content/workspace-design references.
* Preserved owner-selected Fluent 2 direction, native semantics, ASCII/plain-language preference, non-colour signals and reduced motion. No new legal, customer, approval or conformance claim is inferred.
* Refreshed Web Interface Guidelines from https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md during this Review. Applied all fetched rule categories to the supplied behavioral boundary, rather than silently expanding into a whole-site redesign. Images/media, hydration, drag gestures and theme implementation are not introduced by this correction; existing unrelated baseline presentation is not certified. Repository ASCII content policy takes precedence over generic curly-punctuation/ellipsis guidance.
* The supplied source fingerprint was verified at opening and again after investigation. No tools file changed. Exact-head/current-base publication checks were not run.

## Plan-to-Change Reconciliation

| Scope | Implementation and evidence | Assessment |
| --- | --- | --- |
| P01-T01 | app.js:788-920 adds semantic-key/session snapshots, independent original/current/recovery/cache retirement, file identity, recovered checkbox semantics and cache-authoritative restore. | Reconciled. Raw later values remain distinct; cached recovery cannot be recreated from a stale loader-local array. |
| P01-T02 | assistants.js:21-70 separates local Reason/JSON errors from request status and tracks proposal ID/revision independently of case sessions. app.js:613-644 and ops.js:124-148 separate pending/retry/check-history states. panels.js adds manual-form reentry exclusion and challenge correction clearing. | Primary flows reconciled. Recorded document-upload uncertainty is not covered by the shared wrapper: RV-001. |
| P01-T03 | Exactly four new unit methods, one helper in each existing browser check, related README clarification; no dependency, generated-source or tools changes. | Declared test ownership and addition budgets respected. Units execute shipped JS rather than a replacement algorithm. |
| P02-T01 | Original final unit/lint/type logs, both final browser receipts, hashes, preserved adverse attempts and sibling matrix inspected. | Execution evidence substantiates the recorded passing suites. The matrix's blanket recorded-change safeguard conclusion is not substantiated for upload transport uncertainty. |
| P02-T02 | This sole independent Review is now retained. Local commit and parent reconciliation were still unchecked at intake. | Review complete; implementation/local retention task is not automatically complete. Parent owns later disposition and privacy-safe local commit. |
| Follow-Up Items | Current-base/exact-head publication, thread handling and human/hosted acceptance explicitly separate. | Remain distinct follow-ups, not new active implementation tasks or implied passes. |

## Acceptance Checklist

* [x] AC1: nonempty Reason plus malformed JSON focuses, invalidates and describes only the editor; no request is dispatched. Correction/retry clears associations; API failures do not falsely invalidate Reason/JSON. Shipped assistants.js:21-70, executable unit matrix and both case/queue browser rows support this.
* [x] AC2: pending quality submission consumes equal original/recovered/cache evidence across measure switches, preserves later whitespace/other-measure drafts and corresponding unload warnings, and prevents consumed-cache resurrection. Six browser scenarios and semantic unit cases support this.
* [x] AC3: case proposal refresh covers live, recovery and cache-only submission cleanup; later Reason/JSON and checkbox changes remain distinct. Verification does not submit edited JSON. Sessionless queue pending exclusion is covered without claiming a new queue-wide draft-recovery feature.
* [x] AC4: original final requested/related units and both real-Chromium/pinned-axe suites passed within their recorded boundaries. This is an evidence audit, not a fresh heavy rerun.
* [ ] AC5 whole-task completion: sibling audit and this one Review exist, but RV-001 remains unresolved and the source/original-evidence local commit is the parent's remaining action.
* [ ] Human screen-reader and real-staff usability acceptance.
* [ ] Manual assessment of axe color-contrast incomplete results.
* [ ] Full current-base/exact-head publication receipt, independent publication assessment and hosted acceptance.

## Completed Work and Sibling Audit

| File and location | Error/invalidity assessment | Pending/recovery and outcome assessment |
| --- | --- | --- |
| src/api/src/zava_forward/api/web/app.js:310-377 | aiNotes missing Reason is local and correction clears its association; request failure is status feedback rather than a false Reason error. | Equal dispatched values are reconciled; completed reviews retain later read-only edits. Generic refresh protects keyed pending submissions and distinguishes rejection, uncertainty and recorded mutation with reload failure. Upload bypass remains RV-001. |
| src/api/src/zava_forward/api/web/app.js:788-920 | No synthetic field invalidity in the shared lifecycle. | Independent equal-value comparison, all matching counterparts, recovered checkbox state, File object identity, same-session protection, form markers and authoritative cache restore inspected. The unit matrix checks later values through another remember/restore cycle and isolates another session. |
| src/api/src/zava_forward/api/web/assistants.js:12-133 | Separate Reason/JSON error association and first-error focus; status-only request/reload failures. | Shared ID/revision pending/recorded states cover case and queue rebuilds; editors stay editable. Definitive refusal releases readiness, uncertainty requires authoritative reconstruction, recorded old revision remains unavailable. Backend source confirms verification increments revision, so the recorded old revision does not block the new verified revision. |
| src/api/src/zava_forward/api/web/ops.js:21-151 | Empty remediation evidence validates before dispatch, associates/focuses the note, clears on correction, and async failure does not infer invalidity from later text. | Save evidence excludes duplicates while permitting measure navigation and later edits; checklist keys bind measure/version/label. Check-history state remains unavailable until authoritative case redraw. Record-action wrapper and stale-session guard inspected. |
| src/api/src/zava_forward/api/web/ops.js:184-442 | Package/appointment local error association and correction handlers retained. | Separate capacity/appointment draft/context and explicit read-retry paths inspected for interaction with the changed shared helpers; no new shared-lifecycle regression found. This is not a new whole-capacity acceptance claim. |
| src/api/src/zava_forward/api/web/panels.js:7-29 | Manual finance/grant/technical errors remain status-owned through refresh. | Busy/reentry exclusion handles true/false/check-history outcomes without disabling editor fields. |
| src/api/src/zava_forward/api/web/panels.js:145-186, 316-399 | Resident/challenge feedback remains local/status-owned; challenge stale invalidity clears on correction. | Native resident submit reentry is excluded; resident/challenge committed and uncertain raw-fetch outcomes retain disabled actions. Challenge draft capture remains separately owned and revision/context intact. |
| src/api/src/zava_forward/api/web/chat.js:12-16, 51-69, 234-250 | Question, source-admission, doubt and inbox errors use their own status channels. | Raw snapshot equality, successful-only cleanup, pending guards, mounted chat identity and later/failed text retained; source admission still disables unavailable lookup. |
| src/api/src/zava_forward/api/web/case-workspace.js:64-155 | Atomic/polite count changes are deduplicated; native tabs, links and heading focus retained. | Mounted panels preserve drafts; tab-only route changes are exempt from discard. Query-preserving links and observer disposal have no submission/cache ownership. |
| src/api/src/zava_forward/api/web/index.html:11-42 | Skip link, main, visible workspace live status and script ordering retained. | No lifecycle state owner or new field-error handler. |
| src/api/src/zava_forward/api/web/style.css:121-155, 224-264 | Focus-visible, field-error/non-colour states, long-content containment and forced-colour states retained. | No new motion, disabled-zoom or layout-measurement anti-pattern introduced. Existing reduced-motion tokens and responsive/tab overflow remain. No CSS submission-state owner. |

### Web Interface Guidelines Findings

#### src/api/src/zava_forward/api/web/app.js

src/api/src/zava_forward/api/web/app.js:1025-1031 - RV-001: uncertain dispatched upload re-enables unchanged submit; require history checking before retry.

No additional substantive in-boundary finding in assistants.js, ops.js, panels.js,
chat.js, case-workspace.js, index.html or style.css. This is bounded source
assessment with automated browser evidence, not full Guidelines/WCAG conformance.

## Implementation-Time Plan and Detail Update Assessment

| Affected scope | Update, reason and evidence | Assessment |
| --- | --- | --- |
| P01-T01/T02/T03 | Accepted PC-002 adds sessionless ID/revision ownership and queue regression rows; accepted PC-003 adds rejection/uncertainty/recorded-reload distinctions. | Current plan, details and implementation reflect these compatible refinements; no significant/divergent user decision was introduced. |
| P01/P02 | Additional file alias/form-marker reconciliation, detached status routing and checklist navigation separation arose from implementation regression investigation. | Within approved exact-value, identity and unsaved-warning intent; described in changes and reflected in current details. No material revision requiring a new critique was identified. |
| P02-T01 | Browser-only locator/loading/hidden-editor synchronization corrections followed the frozen production/unit source. | Final assistants source was exercised by attempt 07; earlier journey/unit/type evidence is not silently assigned to changed production bytes. Original failed attempts remain available. |
| P02-T02 | Intake state says Review active; changes says Review next; plan leaves Review/local commit unchecked. | Consistent starting state, not an already completed Review claim. This report does not mutate those parent-owned artifacts. |

## Critique and Material Revision Assessment

* Original sole critique remains Complete / Revise, with PC-001 High and PC-002/PC-003 Medium as originally recorded. Its outcome is not rewritten into a pass.
* PC-001's unsupported lock prohibition was already rejected by the parent; that disposition is preserved, not re-adjudicated or silently applied as a plan change. This Review required no heavy rerun and did not open any temporary-directory lock or create scratch files.
* PC-002 and PC-003 were accepted directly and incorporated before implementation; unit/browser evidence covers the case and sessionless callers and confirmed-success/reload failures.
* No evidence of dependent work resuming before the compatible dispositions. No additional significant or divergent planning decision found. RV-001 is an implementation/sibling gap, not a reason to reopen the completed critique.

## Plan Follow-Up Assessment

| Follow-up | Why outside this Review | Owner and route |
| --- | --- | --- |
| FU-01: current-base/exact-head gate, original evidence commit, publication, replies/resolutions | Review is read-only except this record; full gate invokes expressly forbidden az and no final committed candidate exists yet. | Parent/coordinator: persist disposition and local commit; after any later implementation, obtain fresh applicable gate evidence and independent exact-head publication assessment before publication. No push or thread mutation here. |
| FU-02: manual contrast, screen-reader/staff and hosted acceptance | Automated axe and source inspection cannot establish speech, comprehension, operational usability or hosted approval. | Owner/accessibility and staff evaluators plus hosted reviewers. Keep checkboxes unchecked until actual evidence exists. |

These are preserved distinct follow-ups, not additional defects or newly active P01/P02 scope.

## Findings

<!-- rpi:review id=RV-001 -->
### RV-001 [Medium]: Recorded document uploads allow immediate retry after an uncertain mutation

* Related scope: P01-T02/P02-T01 sibling pending and mutation-versus-reload audit.
* Evidence: src/api/src/zava_forward/api/web/app.js:1025-1031 reports any thrown upload error and unconditionally enables the submit button. src/api/src/zava_forward/api/web/app.js:1247 dispatches the upload before entering the shared refresh wrapper at :1248. Thus the new keyed pending/check-history state in :613-644 cannot protect an upload whose response is lost. Supporting trace: src/api/src/zava_forward/api/server.py:983-988 routes uploads to add_document; src/core/src/zava_forward/core/store.py:627-640 assigns a new document ID and appends the document, rather than deduplicating the repeated payload.
* Independent lightweight reproduction: executed the shipped recordedChangeForm and documentsPanel functions with the repository's existing synthetic Node DOM, a constructed FileReader and an API transport failure after dispatch. First submission: requests=1, disabled=false, refreshes=0. Immediate unchanged resubmission: requests=2, original File retained. No source or fixture file was written.
* Impact: a potentially committed upload can be repeated before checking authoritative document history. This is an existing scoped sibling gap, not claimed to have been introduced by the new line. The changes artifact's recorded-change safeguard assurance is too broad; its successful-upload browser coverage does not exercise this uncertainty path.
* Destination: later rpi-implement.
* Smallest useful next action: distinguish pre-dispatch read/validation errors and definitive refusal from dispatched uncertainty; keep the upload unavailable until authoritative refresh/history checking after uncertainty. Propagate confirmed-mutation/reload outcomes to the form without falsely invalidating metadata or clearing later text/File selections. Add a shipped-handler regression for the actual upload call before refresh.

## Defects and Routed Findings

* Severity summary: Critical 0; High 0; Medium 1; Low 0.
* RV-001 is the sole substantive defect identified. No source fix was made.

| Finding | Destination | Owner/next action | Reason |
| --- | --- | --- | --- |
| RV-001 | Later rpi-implement | Parent schedules the bounded document-upload outcome safeguard and regression. | Existing requested sibling remains unsafe under dispatched uncertainty; compatible with the accepted direction. |
| None | rpi-plan | No handoff. | No unaccepted significant/divergent decision identified. |
| None | rpi-research | No handoff. | Available source and original validation evidence support a credible verdict. |
| FU-01/FU-02 | Distinct coordinator/owner follow-up | Complete publication and human/hosted gates under their own authority. | Not implementation defects and not claims of current acceptance. |

Later implementation of RV-001 does not require this Review to run again.
Preserve this original Complete / Not accepted result and append later
implementation/validation evidence in the owning stage.

## Validation Evidence Audit

External evidence root supplied by the coordinator:
/home/azureuser/.copilot/session-state/ec604a8f-07fa-4225-8a37-eb9e234f5e87/files.
Paths below are relative to that external root, not worktree outputs.

| Check/scope | Status | Independently inspected evidence and limitation |
| --- | --- | --- |
| Requested test_case_journey/test_workspace_scripts | Passed, original run | round6-final-checks/focused.log: 21 tests, OK. Read new/extended shipped-code oracles; no fresh full unit rerun. |
| Related accessibility/design/content tests | Passed, original run | round6-final-checks/related.log: 22 tests, OK. |
| Owning Ruff at line length 100 | Passed, recorded | round6-final-checks/ruff.log says all checks passed; final src/tests plus two changed checks pass is recorded in changes/intake. No fresh Ruff rerun. |
| Owning format | Passed, recorded, count qualified | round6-final-checks/format.log contains 52 selected files, not a standalone final 51-file receipt. Changes/intake explicitly correct final owning src/tests scope to 51 files. checks/*.py are excluded by component format configuration; their exploratory whole-file formatting failure is not claimed as a pass. No broad reformat or rerun. |
| Owning mypy | Passed, original run | round6-final-checks/mypy.log: no issues in 99 source files. This is the existing configured scope, including its pre-existing overrides, not a stronger type-safety claim. |
| Journey Chromium/axe | Passed, original run | round6-validation-04/journey.log contains 231 PASS assertions; results.json has 38 scans, zero violations/page errors, Chromium 156.0.8078.4, axe 4.10.3, actual chrome.tabs.setZoom=2 and innerWidth<=640. Six added quality rows include duplicate, dirty/unload, later/other-measure/cache/refusal/reload assertions. |
| Assistants Chromium/axe | Passed, original run | round6-assistants-07/assistants.log ends 141 checks passed; results.json has 141 check names, 32 scans, zero violations/page errors, Chromium 155.0.8059.39 and pinned axe. Case and queue JSON/pending/settlement rows inspected. Fixture BrokenPipe traces accompany aborted requests, not browser page-error failures. |
| Manual axe incomplete assessment | Not performed | Both final receipts retain color-contrast incomplete results; no full accessibility conformance follows from zero violations. |
| Four modified JS files | Passed, fresh lightweight check | node --check on app.js, assistants.js, ops.js and panels.js exited 0 in this Review. |
| Whitespace/diff integrity | Passed, fresh lightweight check | git diff --check exited 0; API diff SHA256 and intake HEAD remained unchanged. |
| RV-001 reproduction | Confirmed, fresh lightweight check | Two in-memory Node probes, including actual shipped documentsPanel/recordedChangeForm, reproduced immediate resubmission after uncertain dispatch. No test/source/scratch file added. |
| Full local publication gate/receipt | Not run, prohibited in this scope | Includes az; no final full-gate receipt exists. Browser/scanner/SQL/image/current-base/exact-head publication requirements are not bypassed by these focused passes. |
| Human/hosted/live acceptance | Unperformed/pending | No screen-reader/staff session, deployment check, remote thread update, hosted approval or user acceptance performed. |

Verified SHA256 identities:

* round6-validation-04/journey/results.json: 79be0afa1f705756f0ede4b8ed97d4e0cf7b7a52a4cea6cae2564abb003cfac1.
* round6-assistants-07/assistants/results.json: c29a4206f85d8b75fc606c9fcf2128c315e3208ee1543e51bb2573071caf243e.
* round6-assistants-07/assistants.log: f9b9cb904c60ba396560f81d0a403e68f6270ffa0e98b641cb620e562b8bfb5f.
* axe-4.10.3.min.js: 880970c081707360e64f34cea25ff91892f5bc95675b0776925b9709dd8a68bb.
* Final API diff: 142e451dc07f5602412e88ee3aa025d27d0bfef53c9f40bba02e6dcd84bf64f4.

Preserved adverse evidence was inspected, not overwritten: round6-units-01
fixture failure; round6-validation-02 pending accessible-name locator failure;
round6-validation-03 duplicate-status strict locator failure;
round6-validation-04 assistants replacement wait failure; and
round6-assistants-05/06 hidden-editor/exact-heading failures. Earlier passing
units/types remain attributed to their original runs. Final production/unit
source froze before 00:03:59Z; final browser-only synchronization fixes are
covered by assistants attempt 07 at/after 00:14:11Z.

No heavy rerun was necessary: evidence hashes, actual logs, receipts, shipped
oracles and lightweight reproduction were sufficient. No heavy lock was
acquired or bypassed and no cloud fallback was used.

## Blockers, Residual Work and Outcome

* Review blockers: none; the bounded Review executed completely.
* Acceptance blocker: RV-001 remains unresolved. The primary quality/proposal corrections are supported, but a requested sibling cannot safely distinguish upload uncertainty from retryable failure.
* Remaining parent work: record this original result, retain original phase evidence and commit locally under the configured privacy-safe identity/trailer rules; do not mark the entire P02-T02 complete merely because this report exists.
* Publication remains blocked in this no-az task and outside reviewer authority. Any later correction/commit/base/tool/input change requires new applicable gate evidence; no final receipt is claimed here.
* Outcome: Not accepted for the complete supplied implementation-and-sibling boundary. This is not a rejection of the passing focused evidence and not a whole-PR, release, WCAG, legal or operational conformance verdict.

## Closeout Routing Record

| Finding class | Destination | Owner/next action |
| --- | --- | --- |
| Implementation defect | Later rpi-implement, RV-001 | Parent routes actual upload uncertainty safeguard plus regression; no fix/re-review in this task. |
| Decision gap or invalid assumption | None | Accepted direction remains valid. |
| Material evidence gap | None | Evidence supports this bounded verdict. |
| Non-blocking residual work | FU-01 and FU-02 | Coordinator publication/exact-head gates; owner manual and hosted acceptance. |

* Execution status: Complete.
* Outcome: Not accepted.
* Findings: one Medium, RV-001.
* Validation coverage: 43 original focused/related units, both final browser/axe suites and owning lint/type evidence audited; fresh JS/diff checks and upload reproduction completed.
* Human checkboxes remain unchecked. Source, plans, critique, changes and state were not edited.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/research/2026-10-28/case-journey-526-round6-research.md](.copilot-tracking/research/2026-10-28/case-journey-526-round6-research.md) | Canonical requirements and root-cause evidence. |
| [.copilot-tracking/plans/2026-10-28/case-journey-526-round6-plan.md](.copilot-tracking/plans/2026-10-28/case-journey-526-round6-plan.md) | Current scope, markers, critique dispositions and follow-ups. |
| [.copilot-tracking/details/2026-10-28/case-journey-526-round6-phase-details.md](.copilot-tracking/details/2026-10-28/case-journey-526-round6-phase-details.md) | Current task details and validation ownership. |
| [.copilot-tracking/reviews/plans/2026-10-28/case-journey-526-round6-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-28/case-journey-526-round6-plan-critique.md) | Original Complete / Revise critique, preserved. |
| [.copilot-tracking/changes/2026-10-28/case-journey-526-round6-changes.md](.copilot-tracking/changes/2026-10-28/case-journey-526-round6-changes.md) | Original implementation, adverse attempts and final validation claims. |
| [.copilot-tracking/rpi-sessions/2026-10-28/case-journey-526-round6-state.json](.copilot-tracking/rpi-sessions/2026-10-28/case-journey-526-round6-state.json) | Intake artifact pointers and parent-owned execution state. |
| [.copilot-tracking/reviews/logs/2026-10-28/case-journey-526-round6-review.md](.copilot-tracking/reviews/logs/2026-10-28/case-journey-526-round6-review.md) | This sole Complete / Not accepted implementation Review. |

## Next Steps

Active parent: preserve this original result and route RV-001 to a later
rpi-implement invocation, without repeating this Review. Keep coordinator
publication/thread follow-up and human/hosted acceptance separate and unchecked.
No reviewer source changes or publication actions are authorized.

---
title: Independent Review - resident-survey-check-571-correction1
description: One bounded post-implementation Review for child task 571-correction1
ms.date: 2026-10-31
---

## Opening Review State

* Interpreted review goal: Independently assess the owner-authorized retained source, current-main reconciliation, correction artifacts and supplied validation, without implying publication or live acceptance.
* Review scope: Distinct child task 571-correction1 / resident-survey-check-571-correction1, one Review.
* Evidence readiness: Six correction artifacts discovered as untracked inputs; original changes and Review available for provenance. HEAD e2e815e22432441887597e5ab7e97bcb4282ca0f and origin/main a75bbdffa51ae34b1fcf779250f1f553d566ee93 match the supplied boundary. Contents and issue criteria remain to be compared.
* Acceptance basis: Correction plan/details/research/state/critique/changes, original findings, actual issue #571 criteria and complete origin/main...HEAD diff.
* First comparison boundary: Reconcile phase markers, critique dispositions, implementation evidence and publication remaining work, then compare retained source against issue criteria.
* Active read-only boundaries: Write only this record; no tests, source/other artifact edits, git mutation, private/cloud data, nested agents or repeat Review. External task-owned /tmp evidence will not be accessed because the active filesystem restriction prohibits /tmp file operations; distinguish supplied provenance from independent validation.
* Initial blockers: None established for bounded Review. Full committed-head gate, verified receipt and independent exact-head publication assessment are explicitly pending.

## Scope and Evidence

* Task ID: 571-correction1; parent 571. Review date: 2026-10-31.
* Assessment count: Exactly one independent post-implementation Review for this distinct child.
* Assessed boundary: G1-G3, FR1-FR3, NFR1-NFR4, AC1-AC5, P01-T01/P01-T02/P02-T01/P02-T02, coverage lock, implementation-time reconciliation, PC-001, original Review findings and plan Follow-Up Items.
* Read completely: correction plan, phase details, research, changes, state and single critique; original changes and Review; complete 1114-line origin/main...HEAD diff, including all eight original tracking artifacts and the two source/guide files. Original artifacts were compared for provenance, not re-reviewed as another task or rewritten.
* Supporting context: src/api/checks/resident_assistant_browser_check.py fresh-reply helper and positive/refusal/reflow sequence; src/api/tests/test_resident_chat_api.py document/form/refusal contracts; src/api/src/zava_forward/api/resident_demo/chat.py finite full-message grammar; src/api/README.md acceptance caveats; src/README.md local gate and tools/rpi-checks.py lock/hash contracts.
* Project context: docs/case_study_48_original.md, resident proposal and exercise acceptance sections of docs/case_study_48_addendum.md, docs/reference/README.md and docs/reference/memory.md. Memory is context, not evidence.
* Actual issue #571 retrieved read-only with gh issue view on 2026-10-31: OPEN, three unchecked criteria. No matching open branch PR returned by gh pr list. No issue or PR was changed.
* All execution outputs outside the workspace are supplied provenance. The three caller-permitted task-owned /tmp outputs were not opened or rehashed because the active filesystem restriction prohibits those operations. This limitation is explicit, not a retroactive execution failure.
* No tests, dependency installation, browser execution, cloud/private-data access, git mutation, nested agents or source/other-artifact changes occurred.

## Execution Status

* Review execution status: Complete.
* Evidence: One comparison of the full supplied boundary, independent local ancestry/diff/source-hash inspection, actual read-only issue retrieval, reconciliation and complete finding set persisted here.
* Task delivery status, separately: Partial. P01 complete on supplied execution evidence; P02-T01 is fulfilled by this record; P02-T02 remains planned and uncompleted.
* Parent owns reconciliation of its checkboxes/state after handoff. Their Review-active/pending state accurately describes entry, not a material stale-state defect.

## Candidate, Merge and Evidence Identities

* Branch: fix/resident-survey-check-571.
* Inspected HEAD: e2e815e22432441887597e5ab7e97bcb4282ca0f.
* Inspected origin/main: a75bbdffa51ae34b1fcf779250f1f553d566ee93.
* Merge parents: eebef7820b96a5ed6f17c29f81b039600cc62009 and a75bbdffa51ae34b1fcf779250f1f553d566ee93. Main is an ancestor of HEAD; owner-approved reconciliation preserves both histories.
* Complete main...HEAD diff: only eight original task artifacts, src/api/README.md and src/api/checks/resident_assistant_browser_check.py. Source/guide delta is exactly 7/5 additions and zero deletions.
* No main...HEAD workflow, tools/rpi-checks.py, knowledge-log or rubric delta. Thus protected main inputs and runner workflow hashes are retained; no workflow edit justifies a hash update. Knowledge log equals main while the original branch history remains reachable.
* Scoped first-parent merge comparison reports no change to original resident-survey-check-571 tracking artifacts. Their original Complete / Residual work Review and failed ancestry gate remain historical.
* Local history independently confirms a0670b58a171255284b005ad281b26fd50ea89c7, merged #573 stale-prompt correction, is already an ancestor of main.
* Correction artifacts and this Review are untracked inputs at this assessment boundary. This is not a clean committed final publication candidate or full-gate identity.
* No fetch occurred; the supplied/current local main boundary was verified. Parent must fetch immediately before the final gate and receipt verification.

| Input | Independently computed SHA-256 |
| --- | --- |
| src/api/checks/resident_assistant_browser_check.py | d122c04850e6bdabe031f2c6e07a464be31d3ac3ac62f8887e55ee306ee071ad |
| src/api/README.md | 0494f6248310d6ded347e60d6afef22c60927a7aaff2b713bb8708814349e755 |

Both hashes match correction changes and original source evidence. No external
execution identity was independently certified:

| Supplied output or asset | Recorded SHA-256, not independently rehashed |
| --- | --- |
| Correction API log | 90ba854c735e3e59006533fd9849b960027c8ef1bbc264bd4490955d90f9850b |
| Correction browser report | db71cd47cc17644630eecbeaf7909e66908d7e3d72fb3a75d49d62814ce4b79b |
| Correction browser log | fd9450c71c5bf40f56ad64463e1c2232a4914e2e6bc5988fee958c5a282b002a |
| Pinned axe 4.10.3 asset | 880970c081707360e64f34cea25ff91892f5bc95675b0776925b9709dd8a68bb |

## Plan-to-Change Reconciliation

| Current plan scope | Changes-record summary | Current-state reconciliation | Gap or rationale |
| --- | --- | --- | --- |
| G1; FR1; AC1; P01-T01 | Authorized merge, protected inputs and retained source | Reconciled independently | Main ancestry and complete diff support owner direction; no workflow/hash changes. |
| G2; FR2; AC2; P01-T01 | Fresh API/Ruff/browser execution | Reconciled on supplied provenance | Requested checks reported passing; 320 skips and 42 incompletes disclosed. Raw external evidence unavailable to reviewer. |
| P01-T02; NFR1-NFR3 | Exact commands, hashes, limitations and current state | Reconciled | Plan/details/changes/state agree P01 complete, Review active and publication pending. No correction dependency recovery or source edit reported. |
| AC3; P02-T01 | One critique, direct PC-001 disposition, one Review | Reconciled | Original verdicts preserved; this record completes the sole child Review. |
| FR3; AC4; P02-T02 | Commit/full gate/verify/exact-head assessment/push/PR remaining | Correctly incomplete | Planned publication is not an introduced defect or claimed pass. |
| AC5 | Conditional issue wording | Reconciled by actual criterion comparison below | All three bounded issue criteria supported; closing language remains conditional on eligible publication. |
| Follow-Up Items | Original human/AT/live limits and hosted/owner gates | Reconciled | Separate owners/routes, outside immediate source/evidence scope. |

Changes' earlier chronological wording groups the original skips/incompletes
with historical limits; its later Fresh Execution Evidence table and current
details explicitly record the same counts for the correction run. Read together,
no current skip or incomplete is erased or relabelled pass.

## Completed Work Assessment

| Marker | Files or evidence | What changed and why | Completion evidence | Assessment |
| --- | --- | --- | --- | --- |
| P01-T01 merge | Main and branch histories | Owner-directed ancestry reconciliation, not a new product decision | Actual merge parents, ancestry and complete diff | Bounded merge conformant; original RV-001 permission resolved prospectively. |
| Retained parent P01-T01 | src/api/checks/resident_assistant_browser_check.py | Two obsolete inputs checked after successful documents | Existing ask_chat counts new articles and returns nth(previous); seven additive lines | Earlier Survey facts cannot satisfy fresh refusals. All existing positives and later checks remain. |
| Retained parent P01-T01 guide | src/api/README.md | Distinguish #573 correction from new negative regression | Five additive lines and adjacent limits | Accurate; no runtime/grammar/UI/authority or approval change. |
| Correction P01-T01/P01-T02 | Correction changes and state | Fresh validation and canonical handoff | Matching commands, counts, input hashes and phase markers | Supported on supplied execution provenance, not independent rerun. |

Recognized questions still assert Survey: Missing, request/document IDs, warnings,
sources, secure-upload instructions, rules labels, own-case isolation and
no-submit/decision limits. Obsolete documents help/forms help assert refusal,
housing-officer help and rules metadata, with no Survey: Missing/R-SURVEY/D-EPC/
AI suggestion in each new reply. Existing HTTP tests encode both outcomes and
finite full-message routing explains their difference. No assertion was removed,
relaxed or substituted; no later reply dependence introduced by the added loop
was found. Source hashes are unchanged by correction and merge.

## Implementation-Time Plan and Detail Update Assessment

| Affected area | Change and reason | Triggering evidence and decision | Reconciliation | Assessment |
| --- | --- | --- | --- | --- |
| G1; P01; original RV-001 | Replace unresolved base permission with authorized merge | Explicit owner continuation; actual merge | Correction research/plan/details/changes/state | Preserves intent and both histories; original verdict not rewritten. |
| P01-T01; NFR2 | Standalone browser literal flock -w 1800; native runner lock for full gate | Owner scheduling direction; runner opens the same global lock itself | Plan/details/research/changes agree | No nested self-lock, lock bypass or workflow edit. First browser admission succeeded; retry unused. |
| AC4; P02-T02 | Fail closed on material Review findings and non-approving exact-head assessment | Single critique PC-001 | Explicit plan AC4, executive readiness and details publication guard | Compatible direct planning correction, no significant user decision or source expansion. |
| P01-T02 handoff | Mark completed checks, retain limits and pending publication | Fresh supplied results | All six current correction artifacts agree | Ready for this bounded Review, not full publication acceptance. |

## Critique and Material Revision Assessment

* Exactly one correction critique executed: Complete / Revise, one Medium PC-001. Preserve that outcome; do not convert it to Pass.
* PC-001 is directly resolved for planning readiness: current plan AC4 and details P02-T02 expressly block unresolved material Review findings and a non-approving independent exact-head assessment. The same details require committed evidence, full passing receipt, fresh-main verification and unchanged inputs before assessment/push.
* Missing or stale assessment cannot satisfy that bound sequence. Subsequent changes invalidate the full gate under the retained local contract. Passing checks alone cannot override adverse independent evidence.
* Execution of those safeguards remains future P02-T02 work; this Review does not invent their receipt or approval.
* Owner-selected merge is not reopened. No significant unaccepted decision, coverage-lock divergence, premature push or dependent-work resumption is evidenced.
* Original RV-001 is settled prospectively by authorization plus verified ancestry, not by editing its original finding. Original RV-002 remains open as a separate acceptance limit.

## Actual Issue #571 Acceptance and PR Wording

| Actual criterion, retrieved 2026-10-31 | Reviewed proof | Determination |
| --- | --- | --- |
| Mismatch root cause identified | Original research/red-probe provenance, inherited #573 commit, current full-message grammar and HTTP refusal contract | Proven for the reported mismatch: obsolete documents help/forms help intentionally refuse; recognized questions return Survey facts. Not a new missing-data/runtime defect. |
| Check and prompt agree, with the check passing locally | Retained supported-question positive assertions and fresh obsolete-input refusal assertions; fresh complete local browser PASS in correction changes and caller attestation; source hashes independently match | Proven on reviewed supplied local execution evidence. Raw report/log hashing and rerun are not independently certified. |
| Resident acceptance evidence not weakened | Complete additive-only source diff, retained positives/authority/isolation/reflow/manual paths and explicit API/guide limitations | Proven as preservation of the existing acceptance evidence, not new attainment of all resident approvals. |

All three issue-specific criteria are supported within this bounded engineering
evidence assessment. A future eligible PR may therefore use Closes #571 once
P02-T02 publication gates succeed and exact-head assessment approves the same
retained scope/evidence. There is no unproven #571 criterion to invent solely
because broader human/live acceptance remains open. Refs #571 is also permissible
as conservative wording; if later exact-head evidence no longer supports a
criterion, use Refs and explicitly name it, never a closing keyword.

No issue checkbox, closure or PR has been performed or authorized by this record.
The criterion says evidence not weakened; it does not say every human, AT, live,
model, native-zoom or WCAG approval is newly achieved. Those approvals remain
unestablished and must remain disclosed even in a future closing PR.

## Plan Follow-Up Assessment

| Follow-up | Why outside immediate scope | Owner or next action | Assessment and route |
| --- | --- | --- | --- |
| Original RV-002 human/AT/live/model/native-zoom/WCAG limits | Synthetic regression and artifact-only correction cannot establish direct acceptance | Corresponding authorized resident/content/accessibility/model/live owners | Open; correction RV-001 below routes once to the existing distinct acceptance follow-up. |
| Hosted checks and owner merge | Occur after eligible PR; not local Review or receipt approval | Delivery parent preserves hosted gates; owner decides merge | Open distinct post-PR follow-up; no bypass or automatic merge. |

Follow-ups remain outside active P01 completion and issue-specific preservation
claims. P02-T02 is already planned active remaining work, not a new follow-up or
an implementation defect created by this Review.

## Findings

<!-- rpi:review id=RV-001 -->
### RV-001 [Low]: Direct resident and operational acceptance remains unestablished

* Related scope: NFR3 and correction plan Follow-Up Items; continuation of original RV-002, not original RV-001.
* Evidence: src/api/README.md limits, correction details Current Completion and Review Handoff, correction changes Fresh Execution Evidence, and preserved original Review RV-002.
* Impact: 320 discovery skips and 42 incomplete-rule occurrences across 31 states cannot become executed integration or accessibility passes. Local synthetic PASS does not establish resident/content approval, screen-reader/AT usability, native browser zoom, actual-model/live service or full WCAG conformance.
* Classification: Non-blocking existing residual acceptance work, not an introduced source defect, reopened merge decision or unmet issue-specific evidence-preservation criterion.
* Destination: Distinct existing human/content/AT/model/live acceptance follow-up, owned by the corresponding authorized acceptance owners.
* Smallest useful next action: Preserve explicit unrun/incomplete boundaries in the future PR and obtain separately authorized direct evidence and named approval before corresponding use or claims. No such execution is authorized here.

## Defects

* No material implementation defect, unaccepted decision gap or material research gap established in the bounded correction.
* Severity summary: Critical 0; High 0; Medium 0; Low 1 non-blocking residual finding.
* No route to rpi-implement, rpi-plan or rpi-research is required by this finding set. Planned P02-T02 remains parent-owned.
* External evidence-access limits qualify the verdict; they do not fabricate a test failure or retroactively invalidate supplied execution.

## Routed Findings

| Finding | Destination | Owner or next action | Reason |
| --- | --- | --- | --- |
| Correction RV-001 | Distinct existing acceptance follow-up | Authorized resident/content/accessibility/model/live owners | Residual direct acceptance outside bounded engineering preservation. |
| Hosted/owner plan follow-up | Distinct post-PR approval work | Delivery parent and owner | Not an implementation defect or local-gate substitute. |

Later publication continuation or routed work does not require another Review of
this child. Preserve this one record and the original Review.

## Blockers and Remaining Work

* Review blockers: None for bounded source/merge/evidence acceptance.
* Publication is not yet eligible: P02-T02 must commit task-owned original correction evidence, obtain a full passing clean committed-head gate, verify its external receipt against freshly fetched main, obtain an explicit approving independent exact-head assessment, then non-force push and create the main PR.
* Untracked correction/Review inputs are expected before that commit and are incompatible with claiming a currently sealed final candidate. Any later input/base/head/tool/image drift requires fresh gate evidence.
* An adverse required check, missing prerequisite, unresolved material finding, failed/stale receipt verification or non-approving/missing/stale exact-head assessment blocks publication. Stop and route later work; do not expand source scope, repeat this Review, use cloud fallback or weaken protections.
* Hosted checks and owner merge remain separate after PR; no merge or private/live approval is inferred.

## Validation Evidence

| Command or evidence | Status | Scope and important result |
| --- | --- | --- |
| git status/branch/rev-parse; merge-base --is-ancestor; merge parents and full origin/main...HEAD diff | Passed, independently observed | Supplied branch/head/main match; main incorporated; source 7 and guide 5 additions only; protected inputs unchanged; correction inputs untracked. |
| sha256sum of resident browser source and API guide | Passed, independently observed | Both exact hashes match correction changes and original source evidence. |
| gh issue view 571; gh pr list --head fix/resident-survey-check-571 | Completed, independently observed read-only retrieval | Three actual unchecked criteria; issue OPEN; no matching open branch PR returned. No remote mutation. |
| API: PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=tests:../core/tests:../agents/tests task-owned python -m unittest discover -s tests -q | Passed, supplied provenance only | From src/api: 1430 tests in 758.350s, OK (skipped=320), exit 0. Skips are not executed SQL/browser/live success. |
| Ruff: check --no-cache .; format --check . | Passed, supplied provenance only | All checks passed; 65 files already formatted; no dependency recovery or source change reported. |
| Resident browser: literal flock -w 1800 -E 75 on the shared lock, task-owned python -m checks.resident_assistant_browser_check with pinned axe | Passed, supplied provenance only | First admission, no retry; Chromium 156.0.8078.4; axe executed 32 scans, zero violations, 42 incomplete-rule occurrences across 31 states, no page errors/external requests. |
| External correction API/browser logs, report and axe asset hashing | Unavailable to independent reviewer | Filesystem prohibition prevented access to task-owned /tmp evidence. Hashes above are supplied, not independently verified. No rerun permitted. |
| Original adverse attempts and ancestry gate | Preserved historical provenance | Original admission timeout, missing-dependency execution failure/recovery and full-gate ancestry rejection remain adverse historical records, not current correction successes. |
| Complete --all gate, receipt verification and independent exact-head assessment | Not run at this planned ordering boundary | Remaining P02-T02 after evidence commit; no full receipt or exact-head approval exists in the assessed correction evidence. |
| Hosted checks/owner merge; direct resident/content/AT/native zoom/model/live/WCAG acceptance | Not run or unestablished | Separate authorized gates/follow-ups; root-font 200% and 320px equivalent reflow are not native zoom or full conformance. |

Exact task-owned external command paths and outputs are recorded in the correction
changes artifact; no reviewer re-execution or external filesystem certification
is claimed. No fresh whole-site web-guideline or accessibility audit is claimed:
there is no changed UI source, only retained Python regression and guide.

## Outcome

* Outcome: Residual work.
* Bounded decision: Approve retained source, authorized merge and reconciled evidence for parent continuation, with supplied-execution provenance limitations explicitly retained.
* Rationale: No material correction defect or unresolved decision found; PC-001 directly reconciled; all three #571 engineering criteria supported. Planned publication and separate direct/hosted acceptance remain unfinished.
* This Complete Review is not complete task delivery, a full-gate receipt, an exact-committed-head publication approval, PR closure, hosted approval or full resident acceptance.

## Closeout Routing Record

| Finding class | Destination | Owner or next action |
| --- | --- | --- |
| Implementation defect | None | No implementation correction required by this Review. |
| Decision gap or invalid assumption | None | Owner merge permission and PC-001 planning guard resolved prospectively. |
| Material research evidence gap | None | Credible bounded verdict from inspected source and qualified supplied execution; raw external hashes not independently certified. |
| Non-blocking residual work | Distinct existing acceptance follow-up, correction RV-001; distinct hosted/owner follow-up | Authorized acceptance owners and delivery parent/owner. |

* Review execution: Complete; task delivery: Partial.
* Outcome: Residual work; bounded source/merge/evidence approved.
* Validation coverage: Independent issue/ancestry/full-diff/source-hash inspection; API/Ruff/browser outcomes supplied, not rerun/rehashed externally.
* Material blockers: None for bounded continuation; P02-T02 publication gates not yet satisfied.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-31/resident-survey-check-571-correction1-plan.md](.copilot-tracking/plans/2026-10-31/resident-survey-check-571-correction1-plan.md) | Current child requirements, criteria and remaining tasks |
| [.copilot-tracking/details/2026-10-31/resident-survey-check-571-correction1-phase-details.md](.copilot-tracking/details/2026-10-31/resident-survey-check-571-correction1-phase-details.md) | Current execution and publication sequence |
| [.copilot-tracking/research/2026-10-31/resident-survey-check-571-correction1-research.md](.copilot-tracking/research/2026-10-31/resident-survey-check-571-correction1-research.md) | Current merge, lock and acceptance rationale |
| [.copilot-tracking/changes/2026-10-31/resident-survey-check-571-correction1-changes.md](.copilot-tracking/changes/2026-10-31/resident-survey-check-571-correction1-changes.md) | Supplied fresh commands/results/hashes and PC disposition |
| [.copilot-tracking/rpi-sessions/2026-10-31/resident-survey-check-571-correction1-state.json](.copilot-tracking/rpi-sessions/2026-10-31/resident-survey-check-571-correction1-state.json) | Parent-owned Review-active state |
| [.copilot-tracking/reviews/plans/2026-10-31/resident-survey-check-571-correction1-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-31/resident-survey-check-571-correction1-plan-critique.md) | Preserved Complete / Revise critique and PC-001 |
| [.copilot-tracking/changes/2026-10-31/resident-survey-check-571-changes.md](.copilot-tracking/changes/2026-10-31/resident-survey-check-571-changes.md) | Immutable original execution and ancestry rejection |
| [.copilot-tracking/reviews/logs/2026-10-31/resident-survey-check-571-review.md](.copilot-tracking/reviews/logs/2026-10-31/resident-survey-check-571-review.md) | Immutable original Review and residual limits |
| [.copilot-tracking/changes/2026-10-31/resident-survey-check-571-evidence.json](.copilot-tracking/changes/2026-10-31/resident-survey-check-571-evidence.json) | Original canonical evidence and input hashes |
| [.copilot-tracking/plans/2026-10-31/resident-survey-check-571-plan.md](.copilot-tracking/plans/2026-10-31/resident-survey-check-571-plan.md) | Original planned boundary and follow-ups in full diff |
| [.copilot-tracking/details/2026-10-31/resident-survey-check-571-phase-details.md](.copilot-tracking/details/2026-10-31/resident-survey-check-571-phase-details.md) | Original execution details in full diff |
| [.copilot-tracking/research/2026-10-31/resident-survey-check-571-research.md](.copilot-tracking/research/2026-10-31/resident-survey-check-571-research.md) | Historical mismatch diagnosis in full diff |
| [.copilot-tracking/reviews/plans/2026-10-31/resident-survey-check-571-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-31/resident-survey-check-571-plan-critique.md) | Preserved original critique in full diff |
| [.copilot-tracking/rpi-sessions/2026-10-31/resident-survey-check-571-state.json](.copilot-tracking/rpi-sessions/2026-10-31/resident-survey-check-571-state.json) | Original historical blocker state in full diff |
| [src/api/checks/resident_assistant_browser_check.py](src/api/checks/resident_assistant_browser_check.py) | Retained positive and fresh-refusal browser evidence |
| [src/api/tests/test_resident_chat_api.py](src/api/tests/test_resident_chat_api.py) | Existing recognized-question and host-refusal contracts |
| [src/api/src/zava_forward/api/resident_demo/chat.py](src/api/src/zava_forward/api/resident_demo/chat.py) | Finite full-message routing |
| [src/api/README.md](src/api/README.md) | Retained guide and direct acceptance limits |
| [src/README.md](src/README.md) | Local full-gate and receipt contract |
| [tools/rpi-checks.py](tools/rpi-checks.py) | Native same-path locking and workflow hash contract |
| [.copilot-tracking/reviews/logs/2026-10-31/resident-survey-check-571-correction1-review.md](.copilot-tracking/reviews/logs/2026-10-31/resident-survey-check-571-correction1-review.md) | This sole independent child Review |

## Next Steps

Return this Complete / Residual work Review to the active parent. Parent records
the bounded approval and single Low residual disposition, then continues existing
P02-T02 only through committed evidence, full current-main gate, fresh receipt
verification and explicit approving independent exact-head assessment before
non-force push/main PR. Conditional Closes #571 is supported for the three
reviewed criteria, without implying new human/live acceptance. Preserve both
Reviews and all adverse provenance; do not repeat this Review. No user action
is required for the parent continuation.

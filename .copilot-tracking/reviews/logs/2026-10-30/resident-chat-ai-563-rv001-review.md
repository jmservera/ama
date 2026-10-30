---
title: Resident chat RV-001 follow-up Review
description: Independent review of the bounded issue 563 repair-admission correction
ms.date: 2026-10-30
---

## Scope and Evidence

* Task: issue-563-rv001 / resident-chat-ai-563-rv001.
* Review date: 2026-10-30.
* Boundary: working diff against HEAD 66924f3aa908ee9bac386a260f805555e47becdb in src/api/README.md (repair-admission paragraph only), src/api/src/zava_forward/api/resident_demo/chat.py and src/api/tests/test_resident_chat_api.py.
* Canonical plan, phase details, changes and state use resident-chat-ai-563-rv001 under their dated .copilot-tracking directories.
* Reused original critique and original resident-chat-ai-563-review.md are immutable. This is one Review of new work, not a rerun or revision of the original adverse Review.

## Opening Review State

* Interpreted review goal: independently assess whether bounded conservative repair admission fixes original RV-001 without diverting unrelated or action messages from deterministic host routes, while retaining enabled generation for genuine household repairs including the dead-rat observation.
* Review scope: P01/P02 implementation and validation plus reconciliation of P03's intentionally pending Review, local commit and post-commit gate.
* Evidence readiness: supplied plan exists, branch and HEAD match the requested boundary, and only the three supplied tracked files are modified. Other untracked files are child RPI evidence. Detailed evidence, full affected routing/tests and necessary dispatch/accounting context remain to be inspected.
* Acceptance basis: user-selected original RV-001, approved child plan and preserved original critique; conservative unknown/single-clause refusal is permitted, general NLP and parent RV-002/RV-003 are excluded.
* First comparison boundary: reconcile plan/details/changes/state and original finding, then inspect the complete three-file diff and affected routing/tests with bounded context.
* Active read-only boundaries: only this review record may be written; no source, other evidence, commits, push, agents, Azure, live model, cloud or private-data access. Existing external logs may be read. No UI review applies.
* Initial blockers: none established; full publication gate is explicitly pending, not presumed passed.

## Execution Status

* Execution status: Complete.
* One independent Review assessed the complete supplied three-file diff, full chat.py and test_resident_chat_api.py, necessary app._assistant and AzureAdvisor dispatch/accounting context, child artifacts and original RV-001/critique. No delegation or implementation occurred.
* Plan execution: P01/P02 are checked with local validation evidence; P03 remains pending because it combines this Review, parent-owned local persistence and the subsequent full gate.
* Outcome: Not accepted. A material admission defect remains in the new follow-up; this does not alter the original Review.
* Severity summary: Critical 0; High 0; Medium 1; Low 0. Existing parent operational follow-ups are preserved separately, not counted as new defects.

## Plan-to-Change Reconciliation

| Current plan scope | Changes-record summary | Current-state reconciliation | Gap or rationale |
| --- | --- | --- | --- |
| P01-T01 household repair admission | Positive household/predicate matching and action/instruction guards | Partially conformant | Original named false positives now have refusals and positive repairs remain supported, but matching a prefix still admits combined instructions/actions, RV-001 |
| P01-T01 external regressions | Two new methods, 30 host examples, ten generated positives | Reconciled within tested examples | Exact host answers and zero advisor/accounting/token/transport assertions are meaningful; comma/then continuation coverage is missing |
| P01-T01 README | Single-clause admission; combined requests remain deterministic | Not fully supported | Source does not establish that claim for comma/then continuations, RV-001 |
| P02-T01 resident and API validation | 149 resident tests, Ruff lint/format and mypy | Reconciled | Raw final logs substantiate the reported results and existing skips; passing examples do not establish completeness of admission |
| P03-T01 Review/persistence | Review next, commit/full gate pending | Reconciled as intentionally pending | Parent must preserve this verdict; this Review neither commits nor claims a gate receipt |
| Follow-Up Items | Parent RV-002/RV-003 and publication gates | Reconciled | Remain outside local acceptance and active implementation completion |
| State/handoff | Review active, review path null before invocation, P01/P02 complete | Reconciled at entry | Parent owns adding this result after handoff; Review does not edit lifecycle state |

## Completed Work Assessment

| Marker | Files | What changed and why | Completion evidence | Validation | Assessment |
| --- | --- | --- | --- | --- | --- |
| P01-T01 | src/api/src/zava_forward/api/resident_demo/chat.py | Replaced bare repair keywords with household/predicate checks and broader refusal guards | Complete source/diff inspected; six bounded route probes | Original refusal and dead-rat probes conform; four mixed-message probes fail intended host boundary | RV-001 |
| P01-T01 | src/api/tests/test_resident_chat_api.py | Added 30 protected/off-topic/action examples and ten generated positives | Two methods added outside installed package, none removed | Final chat log: 22 passed | Sound assertions for enumerated inputs, but not sufficient to catch RV-001 |
| P01-T01 | src/api/README.md | Documents conservative lexical routing and informational reporting exception | Only seven-line admission paragraph changed | Markdown/diff inspection | Claim that combined requests remain refused exceeds source behavior |
| P02-T01 | Child artifacts and external logs | Preserve pre-fix failure, intermediate failure and final successful checks | Raw named logs inspected | Resident 149 run, seven skips; tooling passes | Honest local proof, not actual-model or whole-issue acceptance |

Safety still precedes every other route. Documents, legal, appointment, consent, home, status and forms retain their relative source ordering after refusal guards. Existing hazard/ordinary-topic tests, dead-rat enabled/disabled tests, consent-first, own-case exclusion and late-revocation assertions remain intact. app._assistant sends every typed repair classification to answer_question when configured. AzureAdvisor retains precommitted reservation before credentials/transport, completion accounting and expiry/output limits. No changed accounting, consent, authority, model or UI code was found.

## Implementation-Time Plan and Detail Update Assessment

| Affected area | Update and reason | Triggering evidence and decision | Reconciliation | Planning/critique state | Assessment |
| --- | --- | --- | --- | --- | --- |
| P01-T01 | Household modifiers include broken so informational contact question remains eligible | rv001-chat.log records two intermediate failures, including nine rather than ten generated calls; final log passes | Plan/details/changes report corrected bounded grammar | No new product decision; compatible with accepted RV-001 | Justified local correction |
| P01/P02 | Narrow single-clause/unknown policy and completed local checks | User-approved child plan permits conservative refusal rather than general NLP | Current markers, details, changes and state agree | Reused original Complete / Pass critique; no repeat critique required | Intent is reconciled, but implementation is incomplete, RV-001 |
| P03/Follow-Up Items | Ancestry blocker is historical; current complete gate remains unrun | Local merge-base check confirms f7482602ee8dd8e7eb36dc05426732a56aa982f7 is an ancestor of HEAD | All child handoff sections preserve pending commit/gate | No history rewrite or publication assumed | Reconciled |

## Critique and Material Revision Assessment

* Original .copilot-tracking/reviews/plans/2026-10-30/resident-chat-ai-563-plan-critique.md is Complete / Pass, with no PC findings. It explicitly requires deterministic unrelated/action handling; its verdict does not preapprove this implementation.
* Original .copilot-tracking/reviews/logs/2026-10-30/resident-chat-ai-563-review.md remains Complete / Not accepted. Its RV-001 is the accepted problem statement, not an outcome to soften.
* The child plan's conservative refusal and informational guidance exception preserve confirmed user intent; no significant divergent product decision or invalid planning assumption was identified.
* No dependent-work pause violation is evidenced. The new finding is incomplete implementation of the accepted boundary, so routes to rpi-implement, not rpi-plan or a repeated critique.

## Plan Follow-Up Assessment

| Follow-up | Why outside immediate scope | Owner or next action | Assessment and route |
| --- | --- | --- | --- |
| Parent RV-002 actual-model/live activation | User excludes cloud, actual inference and deployment from this local correction | Owner separately authorizes activation, authority/budget/tariff and actual-model/live evaluation | Open distinct operational follow-up; not a new local defect |
| Parent RV-003 human/content/AT approval | Scripted responses and engineering assertions cannot establish human approval | Resident/content and accessibility owners arrange representative checks | Open distinct human-acceptance follow-up |
| Complete publication gate and hosted/human approval | Full gate is planned only after local implementation/evidence commit; publication is not authorized here | Parent attempts local gate externally after commit and retains blockers; owner retains later approval | Pending, no receipt or publication readiness claimed |

These items remain distinct from RV-001 and are not added to current implementation acceptance scope.

## Findings

<!-- rpi:review id=RV-001 -->
### RV-001 [Medium]: Repair prefixes still admit appended off-topic instructions and contact actions

* Related scope: P01-T01 deterministic action/off-topic routing and conservative single-clause admission; P02-T01 negative coverage.
* Evidence: src/api/src/zava_forward/api/resident_demo/chat.py:230-242 uses re.match for a household/query prefix, then accepts the rest of the text with a punctuation-only fullmatch that permits commas. The report/contact exception at lines 193-195 similarly allows any non-sentence-delimiter tail, including additional guarded action verbs. The few denied tokens at line 243 do not establish that the rest is one informational clause.
* Direct no-inference reproduction against the current source:
  * "My home smells like a rat, sing a song" -> repair.
  * "My home smells like a rat, make a shopping list" -> repair.
  * "How can I report a leak in my home, then email my housing officer?" -> repair.
  * "Who should I contact about my broken boiler, then call my housing officer?" -> repair.
* These are explicit combined instruction/action messages, not unrecognised genuine repairs that the plan permits refusing. In particular email/call are already recognised action tokens, but the informational prefix exempts the entire message from their refusal.
* Impact: with valid consent and enabled AI, app.py:424-435 forwards the entire combined question plus projected own-case grounding to answer_question. aoai.py:_request reserves before token/transport. This violates the promised host-owned refusal and can consume an otherwise unnecessary model reservation. No actual model execution or external contact was performed or inferred.
* Positive/control evidence: the same bounded probe returns repair for "My home smells like a dead rat" and unknown for "Write a poem about a rat". The original examples are improved, but that does not resolve the general accepted deterministic boundary.
* Coverage gap: src/api/tests/test_resident_chat_api.py:REPAIR_HOST_ROUTES covers semicolon, "and", "you" and selected command words, but no comma/then continuation escaping the prefix exception. Its exact host/no-inference assertion pattern can directly cover these cases.
* Destination: later rpi-implement within the existing accepted direction.
* Smallest useful next action: constrain admission to the complete recognised observation/informational request, keeping ambiguous or appended requests refused rather than growing a command-word blacklist. Add the reproduced mixed messages to exact-host/no-advisor/accounting/token/transport regression coverage, retain genuine repair positives and reconcile README/evidence. No model-based classification or general NLP is required.

## Defects

* RV-001 is the sole identified implementation defect in this Review's supplied boundary. No Critical/High finding, material decision gap or research blocker was found.

## Routed Findings

| Finding | Destination | Owner or next action | Reason |
| --- | --- | --- | --- |
| RV-001, Medium | Later rpi-implement | Parent preserves this result and routes complete-request admission plus negative regressions | Existing accepted deterministic boundary remains incomplete |

Later implementation of this finding does not require this Review to run again. Stop after this one Review; do not overwrite the parent's or this Review's original adverse evidence.

## Residual Work

* Preserve parent RV-002 actual-model/live and RV-003 human/content/AT follow-ups under their existing owners.
* Parent P03 owns local persistence with authenticated noreply identity, Copilot trailer and Refs #563 only, followed by the external complete local gate attempt. No push or Azure is authorized. This Review provides no issue-closure or publication approval.

## Blockers and Remaining Work

* Review blockers: none. Evidence suffices for a credible verdict.
* Implementation acceptance blocker: RV-001.
* Remaining active work: parent P03 reconciliation/persistence and subsequent gate. P03 must not be checked as fully completed solely because this Review record exists.
* Current main ancestry is not a blocker: local ancestry check passed for the supplied fresh main SHA. No remote fetch or cloud operation occurred in Review.

## Validation Evidence

External supplied raw-log root: /home/azureuser/.copilot/session-state/1f24faca-4dc1-4e9a-9431-c81211ada179/files/. These paths identify evidence read, not files written by Review.

| Command/evidence | Scope | Status | Summary |
| --- | --- | --- | --- |
| rv001-before.log | New regression methods before fix | Failed, historical expected reproduction | 17 assertions fail, preserving pre-fix defect evidence |
| rv001-chat.log | Intermediate chat suite | Failed, historical | Two failures from missing broken modifier and resulting nine/ten generation count; not represented as final passing evidence |
| rv001-chat-final-bounded.log | Final chat tests | Passed, supplied raw log inspected | 22 tests in 16.374s, OK |
| README resident discovery; rv001-resident-suite.log | test_resident*.py | Passed within stated coverage | 149 in 66.767s, OK skipped=7; six AccountingSqlTests require opt-in isolated local SQL, one ResidentApi test requires opt-in local browser |
| Ruff check, format --check, configured mypy; rv001-api-tooling.log | API | Passed, supplied raw log inspected | All checks passed; 59 formatted files; 113 mypy source files |
| git diff --check | Current candidate | Passed, directly observed | No whitespace errors |
| git merge-base --is-ancestor f7482602ee8dd8e7eb36dc05426732a56aa982f7 HEAD | Supplied fetched main ancestry | Passed, directly observed | Parent's original ancestry failure is historical |
| Six route() probes using supplied installed Python, PYTHONDONTWRITEBYTECODE=1 and prescribed source/test paths | Current chat.py only; no HTTP/model/credentials | Failed intended boundary, directly reproduced | Two controls conform; four combined messages classify as repair, RV-001; output recorded above |
| Second full resident/tooling run | Review | Not run | Supplied raw final evidence is sufficient; bounded probes isolate the newly found logic defect |
| Browser/Web Interface Guidelines review | Backend-only correction | Not applicable/not rerun | No UI file changes; existing local browser skip is explicitly retained |
| Complete post-commit RPI gate | Current candidate | Not run | No implementation commit yet; parent owns attempt and blocker retention |
| Actual model, Azure/live, private data, human/content/AT | Operational acceptance | Not run | Explicit scope exclusions; no acceptance claim |

Review probes imported current source without bytecode writes and printed to tool output; no scratch files, source/test changes or external output files were created.

## Outcome

* Outcome: Not accepted.
* Rationale: the follow-up fixes the enumerated original examples and preserves genuine repair generation, but household/query prefix matching still admits explicit combined off-topic instructions and contact actions. This contradicts the child's approved conservative full-message boundary and README claim. Local tests/tooling pass only for their demonstrated coverage.
* This outcome belongs solely to issue-563-rv001. Original parent Review Not accepted and original critique Complete / Pass remain unchanged.

## Closeout Routing Record

| Finding class | Destination | Owner or next action |
| --- | --- | --- |
| Implementation defect | rpi-implement | Parent routes RV-001 complete-request admission and regressions, preserving this original finding |
| Decision gap or invalid assumption | None | No new product decision required |
| Material evidence gap | None | Sufficient local evidence; no research handoff |
| Non-blocking residual work | Existing distinct operational/human follow-ups | Owners retain parent RV-002/RV-003; parent retains commit/gate work |

* Execution status: Complete.
* Outcome: Not accepted.
* Validation coverage: supplied 22 chat / 149 resident tests with seven disclosed skips; API Ruff/format/mypy raw logs inspected; direct diff/ancestry checks and six no-inference probes.
* Blockers: RV-001 prevents accepting this bounded implementation; no Review-execution blocker.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-30/resident-chat-ai-563-rv001-plan.md](.copilot-tracking/plans/2026-10-30/resident-chat-ai-563-rv001-plan.md) | Accepted bounded correction and pending P03 |
| [.copilot-tracking/details/2026-10-30/resident-chat-ai-563-rv001-phase-details.md](.copilot-tracking/details/2026-10-30/resident-chat-ai-563-rv001-phase-details.md) | Phase evidence and persistence boundary |
| [.copilot-tracking/changes/2026-10-30/resident-chat-ai-563-rv001-changes.md](.copilot-tracking/changes/2026-10-30/resident-chat-ai-563-rv001-changes.md) | Implementation history and raw-log pointers |
| [.copilot-tracking/rpi-sessions/2026-10-30/resident-chat-ai-563-rv001-state.json](.copilot-tracking/rpi-sessions/2026-10-30/resident-chat-ai-563-rv001-state.json) | Entry lifecycle state; parent owns continuation |
| [.copilot-tracking/reviews/plans/2026-10-30/resident-chat-ai-563-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-30/resident-chat-ai-563-plan-critique.md) | Immutable reused Complete / Pass critique |
| [.copilot-tracking/reviews/logs/2026-10-30/resident-chat-ai-563-review.md](.copilot-tracking/reviews/logs/2026-10-30/resident-chat-ai-563-review.md) | Immutable original adverse Review/problem evidence |
| [src/api/src/zava_forward/api/resident_demo/chat.py](src/api/src/zava_forward/api/resident_demo/chat.py) | Reviewed routing and host answers |
| [src/api/tests/test_resident_chat_api.py](src/api/tests/test_resident_chat_api.py) | Reviewed full affected regression suite |
| [src/api/README.md](src/api/README.md) | Reviewed admission paragraph and bounded validation instructions |
| [src/api/src/zava_forward/api/resident_demo/app.py](src/api/src/zava_forward/api/resident_demo/app.py) | Context-only dispatch/consent boundary |
| [src/api/src/zava_forward/api/resident_demo/aoai.py](src/api/src/zava_forward/api/resident_demo/aoai.py) | Context-only generation/accounting boundary |
| [.copilot-tracking/reviews/logs/2026-10-30/resident-chat-ai-563-rv001-review.md](.copilot-tracking/reviews/logs/2026-10-30/resident-chat-ai-563-rv001-review.md) | This one independent follow-up Review |

## Next Steps

Return Complete / Not accepted to the active parent. Parent preserves this result and routes RV-001 to later rpi-implement within the existing accepted direction, without another Review or a same-invocation correction loop. Parent owns lifecycle reconciliation and authorized local persistence/gate work; this invocation stops with no commits, push or cloud actions.

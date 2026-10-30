---
title: Resident browser check 571 independent RPI Review
description: One post-implementation review of the local synthetic browser-check correction
ms.date: 2026-10-30
---

## Opening Review State

* Interpreted goal: independently assess task #571 execution and acceptance without implementing or publishing.
* Scope: current worktree changes against HEAD 3d9d523df35e3a974e1586e23f3f6aa2d0447dbd, limited to src/api/README.md, src/api/checks/resident_assistant_browser_check.py, src/api/tests/test_resident_chat_api.py and the supplied dated task artifacts.
* Evidence readiness: named artifacts and durable evidence bundle supplied; content comparison pending.
* Acceptance basis: ordered RPI, real local baseline and positive browser evidence, fresh current-reply assertions, preserved plain language and AI/rules authority semantics, focused/static/full-unit evidence and explicit acceptance exclusions.
* First comparison boundary: plan/details/critique against actual diff and captured original output.
* Active read-only boundaries: only this review record may be written; no implementation, other artifact edits, commits, remote writes, Azure, deployment, sign-in or credentials.
* Initial blockers: none established; publication and named-human/live acceptance are not authorized review actions.

## Execution Status

* Execution status: Complete.
* Review executed on 2026-10-30 after the supplied P01 implementation/validation handoff, activating rpi-review once. No further reviewer or subagent was invoked.
* Outcome: Conformant for the bounded synthetic-check correction. This is not whole-issue closure, completed local delivery, human acceptance or publication readiness.
* Reviewer actions: read-only git status/branch/HEAD/diff inspection; source and artifact comparison; in-memory verification of captured complete-output hashes and lengths; Python AST parsing; captured axe-summary consistency checks; git diff --check HEAD.
* Browser, unit, Ruff and mypy results below are parent-executed evidence, not independent reruns. No heavy suite or browser was rerun. No external scratch file was accessed by this reviewer.

## Scope and Evidence

* Task: #571, resident-browser-check-571.
* Branch: fix/resident-browser-check-571.
* Assessed baseline: HEAD 3d9d523df35e3a974e1586e23f3f6aa2d0447dbd.
* Assessed executable/documentation boundary: the complete unstaged diff of src/api/README.md, src/api/checks/resident_assistant_browser_check.py and src/api/tests/test_resident_chat_api.py against that HEAD. Diff statistics: 82 insertions, 37 deletions. The assessment is of these worktree bytes, not a future commit or exact-head publication candidate.
* Assessed dated artifacts: research, plan, phase details, original single critique, changes, durable evidence JSON and RPI session state listed below. No other untracked task set was substituted.
* Context read: docs/case_study_48_original.md; relevant opening scope in docs/case_study_48_addendum.md; docs/reference/README.md; docs/reference/memory.md; housing-association primer; content-standard scope and AI/rules wording; finite-grammar routing in src/api/src/zava_forward/api/resident_demo/chat.py; original RV-003 in .copilot-tracking/reviews/logs/2026-10-30/employee-chat-dismissal-correction-review.md.
* Product routing, rendered copy, templates, identity, model enablement, data and deployment are unchanged. No general repository, live-site, UI-conformance or legal-currentness audit is implied.
* Read-only git inspection found precisely the three expected tracked modifications and the dated #571 artifacts. The only reviewer write is this record. Existing modified/untracked inputs were not moved, staged or committed.

### Frozen review boundary

SHA-256 identities computed directly by the reviewer:

| Input | SHA-256 |
| --- | --- |
| Scoped git diff HEAD, three changed files | bb7572a0272c3f41db1fef08ec6bdf558363f6ab1a8ffa81c3d9bccb15e6f30a |
| src/api/README.md | 1c83ef42106d2cadb69066233d264be6b755eecc2a7bb4a56307ccd07a4a10c7 |
| src/api/checks/resident_assistant_browser_check.py | a4ee2cc65faa81e36bc048da289f9ddf525146afb1de84af7657368848051bfb |
| src/api/tests/test_resident_chat_api.py | 1ddc58763c6c52e741b0ea9a2bdbbce27b06769f6af4331dd161f7821a9265d8 |
| .copilot-tracking/plans/2026-10-30/resident-browser-check-571-plan.md | dde3fe3efe10e6431327093f12f531daa10d4c0e7291a7efa9493e10eb74edb8 |
| .copilot-tracking/details/2026-10-30/resident-browser-check-571-phase-details.md | d133660206df0f412c3abadfefdd19ed1c3487c4417cd5b1da55a22956d4ecf2 |
| .copilot-tracking/research/2026-10-30/resident-browser-check-571-research.md | 6f32b2b76b47d7c0fb4b64dc95d4353d9eca0cc49df96c3b6cad29c41327b56d |
| .copilot-tracking/changes/2026-10-30/resident-browser-check-571-changes.md | a6b054f9d296c2f11b8f9d341b07a2db4cb86e0f3c2eb1c3ead472752422e102 |
| .copilot-tracking/changes/2026-10-30/resident-browser-check-571-evidence.json | 4642bcdfb43cac647cfc0ffd43fa44a75a7607fad58c59d2127dcc096158520a |
| .copilot-tracking/reviews/2026-10-30/resident-browser-check-571-critique.md | 0b074bb6e2d53fc9b563a79a73f1d52537cc00e285278719fb3ef699c9ba626d |
| .copilot-tracking/rpi-sessions/2026-10-30/resident-browser-check-571-state.json | febb9dd9d7bcea5364daad545437d2cc336f4c421a6b7c766ef008a1cda258b9 |

These identify reviewed inputs; they are not a signed execution attestation or publication receipt. Later source changes are outside this assessment.

## Plan-to-Change Reconciliation

| Plan scope | Changes/evidence | Current-state reconciliation | Assessment |
| --- | --- | --- | --- |
| Research, AC1 | Research C1-C8, complete captured baseline failure, finite-grammar source | Reconciled | Real Chromium baseline rejects documents help; supported questions retain the intended answer. Research identifies two additional stale inputs and the whole-history risk. |
| P01-T01, FR1-FR3, AC2-AC3 | Browser helper and supported questions | Reconciled | New reply count and HTTP success precede per-reply facts/labels; no product routing change. |
| P01-T02, FR4 | Strengthened document HTTP test and two new methods | Reconciled | Exact supported document/form routes and disabled-AI labels; obsolete prompts remain no-model refusals. |
| P01-T03, AC2-AC4 | Guide, positive/negative browser, units/static captured evidence | Reconciled | Required local engineering evidence supplied; full API run records the exact required lock. Skips remain explicit. |
| P02-T01, AC5 | Plan/details/changes await one independent Review | Completed by this record | Parent owns recording this handoff in its artifacts; reviewer does not edit them. |
| P02-T02, AC5 | Local Refs-only commit unchecked | Pending, accurately represented | Reviewer cannot commit. Parent must complete authorized local delivery, without closing syntax or remote publication. |
| Follow-Up Items | No new out-of-scope work; existing human/live gates retained | Reconciled | Existing exclusions are not inserted into P01 completion or acceptance. |

The changes record's early P01 paragraph says "Validation pending"; its later dedicated Validation section, P01-T03 details and handoff explicitly supersede that implementation-time state with completed results. This does not leave a material ambiguity about the current evidence.

## Completed Work Assessment

| Marker | Files | Assessment and evidence |
| --- | --- | --- |
| P01-T01 | src/api/checks/resident_assistant_browser_check.py | One small typed ask_chat helper waits for /demo/assistant HTTP 200 and exactly one additional assistant article, then returns nth(previous). Topic assertions and all three supported document-question assertion sets bind to that new article. Document source geometry and the second resident's absent-document checks also bind to their own reply. |
| P01-T01 | Same | Existing Survey: Missing, secure upload link, unreadable page, address mismatch, unfinished file check, R-SURVEY, D-EPC, not-a-decision, cannot-upload/send and cross-case exclusions are retained. The metadata itself must say Summary by rules. Protected consent, regulations and safety questions retain the same expected meanings using complete everyday questions. |
| P01-T02 | src/api/tests/test_resident_chat_api.py | Existing document test retains every factual, source, authority and isolation assertion and gains subtests, exact route and exact Summary by rules - AI is not enabled label checks. Two added methods cover the exact form question and all three obsolete inputs. The existing assert_host_routes helper checks full expected answer/sources/label and no advisor, provider selection, accounting reservation/completion, token or transport access; human help remains in the host-owned refusal. |
| P01-T03 | src/api/README.md | Directly related explanation correctly names the supported/refused grammar and fresh-reply acceptance. It explicitly disclaims general language understanding and does not change resident copy or claim human/live acceptance. |

No test method, acceptance fact or protected-route check was removed. No runtime source, finite grammar, model authority, consent behavior, manual route, session fencing, callback or accessibility assertion was weakened in the supplied diff. The permitted addition cap is met: one helper, two test methods. Existing unrelated whole-history assertions elsewhere are outside this bounded correction and were not opportunistically refactored.

### Freshness and mutation proof

The original browser failure shows documents help rendering the task-limit refusal instead of Survey: Missing. Positive evidence now reaches the complete check's terminal PASS, including unchanged downstream session/consent/callback/error/reflow assertions.

The documented in-memory routing probe first permits the supported document response and forces only its second occurrence to unknown. Its captured failure targets #assistant-result > article.chat-widget-assistant nth(6), contains the current refusal and fails specifically on Survey: Missing. The probe verifies two document calls and the expected assertion before reporting expected failure. Earlier successful document facts therefore cannot satisfy the revised current-reply assertion. This is real-browser parent-executed mutation evidence, not merely a route mock unit test or a product-source edit.

Each supported document question in the detailed browser loop independently checks all preserved facts, sources, rules metadata and authority limits; the HTTP document subtests independently check the same contract. The initial topic loop additionally exercises its current document response, rather than borrowing a later or historical answer.

## Implementation-Time Plan and Detail Update Assessment

| Affected area | Update and trigger | Reconciliation / decision | Assessment |
| --- | --- | --- | --- |
| Research to P01-T01 | Baseline refusal plus complete-message grammar history identified stale prompts; accumulated chat history exposed false-positive risk | Plan FR1-FR3, coverage lock and phase details select supported questions and fresh replies | Preserves approved intent; right-side harness fix, not a product expansion. |
| P01-T02 | Exact form wording and obsolete inputs need regression protection | Existing document test extended; two focused additions; no new framework or shared prompt registry | Compatible implementation detail, no divergent product decision. |
| P01-T03 | Positive and adversarial outputs became available | Details, validation section, JSON and P01 completed markers agree | No source change after the supplied final validation is reported; reviewer fingerprints current bytes but cannot independently attest execution chronology. |
| Critique disposition | Worker-local path restriction conflicted with parent authority and exact lock requirement | Explicit rejection recorded before implementation handoff; compatible provenance advice retained | Justified environment-specific disposition, not an acceptance waiver or unresolved product assumption. |
| P02 | Review and local commit separated from P01 | Checkboxes remain pending until their respective owner actions | Accurate review-entry state, not unfinished P01 implementation. |

The supplied ordered research, planning/critique, implementation and Review narrative is consistent across the artifacts and session state. This Review executes after implementation. No significant implementation-time product divergence requires renewed planning or another critique; no second review loop is proposed.

## Critique and Material Revision Assessment

* Original critique remains Complete / Revise, with PC-001 High. Its record was read and not modified or relabelled Pass.
* PC-001's premise is the critique worker's local inability to operate in temporary paths. Parent disposition explicitly states that constraint is not the parent's execution restriction, repository scratch policy prefers external evidence, and the user specifically requires the exact /tmp lock for full units.
* Current evidence includes captured complete baseline/negative outputs and hashes, positive output, static output and durable unit tails, satisfying the useful provenance concern without this reviewer accessing forbidden external paths. The current reviewer also obeyed its own local filesystem restrictions; those do not retroactively invalidate parent-authorized execution.
* Rejecting PC-001 on this basis is justified, not a silent bypass. There is no need to change the parent's prescribed lock, pretend the full suite was Not run, or repeat the critique. The original verdict is historical and remains Revise.
* Original RV-003 in the employee-chat-dismissal-correction review remains unchanged. This task supplies separately scoped resolving evidence for its standalone resident failure; it does not rewrite that earlier assessment, approve its broader AC4 or establish whole issue closure.

## Plan Follow-Up Assessment

| Item | Why outside immediate scope | Owner / earliest next action | Assessment |
| --- | --- | --- | --- |
| Existing named-human resident copy, direct assistive-technology, real-model and live-site acceptance | Synthetic fixture/check correction cannot supply these approvals or evidence | Existing resident/content, accessibility and model/live-service acceptance owners; separately authorized acceptance before the relevant claims/use | Open existing gates; RV-001, not a new P01 defect. |
| Complete publication gate and hosted/human release approvals | Local-only delivery is authorized; push/deployment prohibited | Parent/release owner, only when publication is separately authorized | RV-002; no publication readiness inferred. |

No new evidence-grounded out-of-scope implementation task was discovered. Existing exclusions remain separate from active P01 completion.

## Findings

The complete current set contains no introduced implementation defect, material decision gap or material research-evidence gap. The following two Low entries record existing non-blocking residual acceptance boundaries, not reasons to withhold acceptance of this synthetic correction. RV IDs here are local to this review and do not replace the historical RV-003.

<!-- rpi:review id=RV-001 -->
### RV-001 [Low, residual]: Human and live acceptance remains unestablished

* Related scope: AC5 exclusions and existing plan Follow-Up Items.
* Evidence: src/api/README.md acceptance caveat immediately before the new explanation; phase-details non-goals; changes limitations; evidence JSON browser.human_and_assistive_technology and limitations.
* Impact: automated local browser/axe, HTTP and mock-model evidence cannot approve resident wording, prove actual assistive-technology usability or establish real-model/live-site behavior. This is not a regression or a blocker to the bounded correction/local evidence commit.
* Destination: distinct existing acceptance follow-up, not rpi-implement, rpi-plan or rpi-research for this task.
* Owner: existing named-human resident/content and accessibility acceptance owners, plus model/live-service owner; no new appointment or approval is inferred.
* Earliest useful follow-up: before making the relevant human, accessibility, actual-model, live-service or whole-issue acceptance claim, obtain separately authorized named-human/direct evidence and record its actual result. No such activity is authorized here.

<!-- rpi:review id=RV-002 -->
### RV-002 [Low, residual]: Publication readiness is intentionally unassessed

* Related scope: P02 local-only delivery and publication exclusion.
* Evidence: plan Handoff, changes Review and Remaining Work, evidence JSON limitations; worktree still uncommitted at the assessed HEAD.
* Impact: this Review and the targeted validation are not the complete local publication gate, a receipt, exact-committed-head independent assessment or hosted/human release approval. This does not block the specifically requested local Refs-only commit, but remains a prerequisite boundary for later publication.
* Destination: distinct future publication/release follow-up, not a current implementation defect or a request to run prohibited publication actions.
* Owner: parent/release owner under repository publication policy.
* Earliest useful follow-up: only after separate publication authorization, commit/reconcile the intended candidate and original evidence, then satisfy the complete local gate and fresh exact-head/base receipt/review requirements before any push; retain hosted and human approval requirements. Do not reuse this worktree Review as an exact-head gate.

## Defects

* None established in the assessed source/check/test/documentation diff.
* Severity totals: 0 Critical, 0 High, 0 Medium defects; 2 Low residual boundary findings.
* No corrective rpi-implement, rpi-plan or rpi-research handoff is required by this Review.

## Routed Findings

| Finding | Destination | Owner / next action | Reason |
| --- | --- | --- | --- |
| RV-001 | Distinct existing acceptance follow-up | Relevant human/content/AT/model/live-service owners, separately authorized evidence before corresponding acceptance | Out-of-scope existing acceptance, not a defect. |
| RV-002 | Distinct future publication follow-up | Parent/release owner, complete fresh publication gates only upon later authorization | Current delivery is local-only, not publication-ready. |

Later work does not require this Review to run again.

## Blockers and Remaining Work

* Review blockers: none. Captured project-relative evidence is sufficient for a credible bounded verdict.
* P01 implementation blockers or remaining active implementation: none established.
* P02-T01: this one independent Review is executed; parent must record the handoff without altering original critique or historical review outcomes.
* P02-T02: authorized local-only commit remains pending and is parent-owned. Use Refs #571 only, privacy-safe identity and required trailer; no closing keyword, push or remote mutation. This reviewer neither performed nor claims the commit.
* Broader acceptance blockers: RV-001 remains open for its respective human/live claims. Future publication prerequisites in RV-002 remain unperformed. Neither expands the current correction scope or creates whole-issue closure.

## Validation Evidence

Unless identified as reviewer-executed, entries are assessed parent-executed evidence captured in .copilot-tracking/changes/2026-10-30/resident-browser-check-571-evidence.json, with exact commands/probe in the changes record and environment in the phase details.

| Command / check | Status | Evidence and limits |
| --- | --- | --- |
| Unmodified python -m checks.resident_assistant_browser_check with digest-checked axe | Failed as required baseline | Complete captured Chromium traceback: documents help refused, Survey: Missing absent. Reviewer recomputed its 5726-byte output hash e7351ecbdcb7f6f757dbf2192aa47d333ac3eaea011759fe53df86794292196e. |
| Revised standalone check with axe | Passed, parent execution | Complete positive PASS output; actual loopback Chromium 156.0.8078.4. Captured 32 axe states have empty violation lists; console errors and external requests empty. Full external report hash is recorded, not independently recomputed from that external file. |
| Actual browser later-document-refusal probe | Failed at intended assertion, probe succeeded | Complete captured negative output: fresh nth(6) article is refusal despite earlier successful document facts. Hash/byte length verified from captured complete text. |
| python -m unittest test_resident_chat_api -q | Passed, parent execution | Complete captured output: 27 tests, no failures. Hash/byte length verified. |
| python -m unittest discover -s tests -p test_resident*.py -q | Passed with skips, parent execution | Tail records 154 tests run, 7 skipped. Six opt-in resident SQL and one opt-in rendered-browser skip are disclosed; not 154 independent successful integrations. |
| flock -w 600 /tmp/ama-rpi-heavy.lock, task-owned Python, -m unittest discover -s tests -q | Passed with skips, parent execution | Exact required lock invocation recorded. Tail: 1363 tests run in 482.777s, 318 skipped. Reviewer did not rerun or independently observe lock acquisition. |
| ruff check .; ruff format --check .; mypy | Passed, parent execution | Complete captured output: all checks passed; 59 files already formatted; no issues in 114 typed source files. Hash/byte length verified. |
| In-memory captured-evidence integrity checks | Passed, reviewer execution | All five complete-output entries match recorded lengths and SHA-256 values; 32 empty-violation states agree with count, external-request summary empty. Resident/full-unit tails are explicitly partial captures; their full external-file hashes were not independently verified. |
| ast.parse of both changed Python files; git diff --check HEAD | Passed, reviewer execution | No filesystem compilation output; both files parse and tracked diff has no whitespace errors. Not a substitute for unit/static runs. |
| Named-human resident copy, direct screen-reader/voice/AT, real-model, live-site acceptance | Not run | Outside correction and review authority; RV-001. Axe/reflow assertions are engineering evidence, not WCAG conformance or native browser zoom acceptance. |
| Complete local publication gate, committed-head receipt verification, hosted checks, release approvals | Not run | Intentionally deferred for local-only delivery; RV-002. No publication readiness claimed. |

The full suite's 318 skips are not hidden passes: the changes record distinguishes 317 declared SQL/browser skips from one dynamic JSON/SQL COMMIT acknowledgement-boundary exclusion. The standalone requested browser check ran separately. Neither skipped SQL nor other optional browser journeys are claimed covered by it.

The complete baseline, positive, negative, chat and static captures are hash-consistent with the original-log metadata. Hash consistency verifies capture integrity, not independent re-execution. The reviewer did not access external original files, credentials, Azure, deployment or any live resident service. The producer's scoped guideline review is documented in changes; this Review does not assert a fresh independent whole-UI guideline/accessibility audit, and no production web surface changed.

## Outcome

* Review execution: Complete.
* Outcome: Conformant for the supplied correction boundary.
* Rationale: stale check inputs were corrected against the existing deliberate finite grammar; plain-language question meaning, truthful rules labeling, document facts/sources and resident authority/isolation remain intact. Fresh-reply assertions have positive and adversarial real-browser evidence, supported/refused HTTP coverage and passing resident/static evidence. No coverage removal, product weakening, unresolved divergent decision or material missing evidence was established.
* Acceptance limit: P01 engineering evidence is acceptable; AC5/local delivery is not complete until the parent performs the authorized local commit. The whole issue, historic broad AC4, named-human/live acceptance and publication readiness are not approved.

## Closeout Routing Record

| Finding class | Destination | Owner / next action |
| --- | --- | --- |
| Implementation defect | None | No rpi-implement correction needed. |
| Decision gap or invalid assumption | None | No rpi-plan handoff needed; PC-001 rejection is justified and original Revise preserved. |
| Material evidence gap | None within boundary | No rpi-research handoff needed; captured-output and rerun limits disclosed. |
| Non-blocking residual acceptance | RV-001, distinct existing follow-up | Relevant acceptance owners, only under separate authority. |
| Non-blocking publication boundary | RV-002, distinct future follow-up | Parent/release owner, only upon publication authorization. |

* Execution status: Complete.
* Outcome: Conformant within the frozen worktree boundary.
* Validation coverage: parent browser baseline/positive/mutation, 27 focused chat tests, 154 resident tests with 7 skips, locked 1363 API tests with 318 skips, Ruff and mypy; reviewer capture/hash/AST/diff checks.
* Current correction blockers: none. Local commit remains parent-owned; broader acceptance and future publication gates remain open.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/research/2026-10-30/resident-browser-check-571-research.md](.copilot-tracking/research/2026-10-30/resident-browser-check-571-research.md) | Baseline investigation and grammar decision |
| [.copilot-tracking/plans/2026-10-30/resident-browser-check-571-plan.md](.copilot-tracking/plans/2026-10-30/resident-browser-check-571-plan.md) | Acceptance, coverage lock and critique disposition |
| [.copilot-tracking/details/2026-10-30/resident-browser-check-571-phase-details.md](.copilot-tracking/details/2026-10-30/resident-browser-check-571-phase-details.md) | Phase tasks, commands and boundaries |
| [.copilot-tracking/reviews/2026-10-30/resident-browser-check-571-critique.md](.copilot-tracking/reviews/2026-10-30/resident-browser-check-571-critique.md) | Preserved original Complete / Revise critique |
| [.copilot-tracking/changes/2026-10-30/resident-browser-check-571-changes.md](.copilot-tracking/changes/2026-10-30/resident-browser-check-571-changes.md) | Implementation, commands, mutation probe and skips |
| [.copilot-tracking/changes/2026-10-30/resident-browser-check-571-evidence.json](.copilot-tracking/changes/2026-10-30/resident-browser-check-571-evidence.json) | Durable original-output captures and hashes |
| [.copilot-tracking/rpi-sessions/2026-10-30/resident-browser-check-571-state.json](.copilot-tracking/rpi-sessions/2026-10-30/resident-browser-check-571-state.json) | Parent lifecycle and decisions at review entry |
| [src/api/README.md](src/api/README.md) | Scoped check rationale and acceptance exclusions |
| [src/api/checks/resident_assistant_browser_check.py](src/api/checks/resident_assistant_browser_check.py) | Reviewed standalone check |
| [src/api/tests/test_resident_chat_api.py](src/api/tests/test_resident_chat_api.py) | Reviewed HTTP regression coverage |
| [.copilot-tracking/reviews/logs/2026-10-30/employee-chat-dismissal-correction-review.md](.copilot-tracking/reviews/logs/2026-10-30/employee-chat-dismissal-correction-review.md) | Preserved historical RV-003 |
| [.copilot-tracking/reviews/logs/2026-10-30/resident-browser-check-571-review.md](.copilot-tracking/reviews/logs/2026-10-30/resident-browser-check-571-review.md) | This single independent Review |

## Next Steps

Return this result to the active parent for P02 handoff reconciliation and the already authorized local Refs #571 commit only. No corrective RPI stage, second reviewer or Review loop is required. Do not push, close the issue, claim human/live acceptance or claim publication readiness. Keep RV-001/RV-002 with their distinct existing/future owners.

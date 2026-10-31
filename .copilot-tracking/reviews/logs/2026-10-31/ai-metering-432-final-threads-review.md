---
title: AI metering final threads independent implementation Review
ms.date: 2026-10-31
---
<!-- markdownlint-disable-file -->

## Scope and Evidence

* Task ID: issue-432-pr-602-final-threads / PR #602 Refs #432.
* Review date: 2026-10-31.
* Review scope: one independent post-implementation assessment of the full current working-tree correction, including relevant unchanged contracts; publication P02-T03 is pending and excluded from source acceptance.
* Candidate baseline HEAD: 3d4a8d324b5324c2cabd1e037bde3dcbf6ba7f6f on feat/ai-metering-432.
* Plan: .copilot-tracking/plans/2026-10-31/ai-metering-432-final-threads-plan.md.
* Phase details: .copilot-tracking/details/2026-10-31/ai-metering-432-final-threads-phase-details.md.
* Plan critique: .copilot-tracking/reviews/plans/2026-10-31/ai-metering-432-final-threads-plan-critique.md.
* Changes: .copilot-tracking/changes/2026-10-31/ai-metering-432-final-threads-changes.md.
* Research: .copilot-tracking/research/2026-10-31/ai-metering-432-final-threads-research.md.
* Additional evidence: full unstaged diff of all 14 changed source/test/documentation files; no staged diff; .copilot-tracking/rpi-sessions/2026-10-31/ai-metering-432-final-threads-state.json; original case study, addendum, knowledge-base index and memory; relevant unchanged worker, financial ledger, SQL/JSON storage, continuity, registry and review contracts.
* Reviewed tracked diff SHA-256 (`git diff --binary | sha256sum`): 2d7d4829817035bedccf8302696d38b601509e86503b36c15cf3b12d27491cb2. HEAD and tracked change boundary remained unchanged through assessment.
* GitHub inspection: PR #602 is open, main-based, head branch feat/ai-metering-432. Its remotely reported head was 007149d7af79da6706844b83e665a3a53fe26395. This Review assesses the supplied local candidate, not that remote head or its hosted checks; the parent must bind publication to the eventual pushed head.

## Opening Review State

* Interpreted review goal: assess bounded mismatch quarantine, held report availability, and financially unresolved persistent manual publication at actual capacity without weakening immutable joins.
* Evidence readiness: all five supplied artifacts available; current source/test/documentation diff and relevant unchanged contracts available; supplied static/unit evidence is to be assessed, not assumed independently rerun.
* Acceptance basis: FR1-FR4 and AC1-AC4, original PC-001 through PC-004 dispositions; AC5 publication portion remains pending. The explicitly selected CI gate overrides the complete local publication gate.
* First comparison boundary: current complete git diff against HEAD, followed by provider-worker-completion, report input/read handling, strict financial output and backend-specific actual-message persistence.
* Active read-only boundaries: only this canonical Review record may be written; no source/plan/critique changes, nested agents, repeated Review, private data or paid inference.
* Initial blockers: none for source Review; hosted CI and publication remain subsequent parent-owned work.

## Execution Status

* Review execution status: Complete.
* Review execution evidence: one independent assessment completed against the supplied local candidate on 2026-10-31. All five requested artifacts, the complete current tracked diff and relevant unchanged contracts were compared. Nine composed test methods and both packages' requested static checks were independently run successfully.
* Plan execution status: Partial only because publication P02-T03 remains pending. P01 and P02-T01 are complete; P02-T02's checks and this Review are now evidenced. This is not a claim that AC5 or publication has completed.
* Independence: no nested agents, source edits, amended/repeated Review, commits, push, thread changes or PR merge. This invocation writes only its one canonical original Review artifact.

## Plan-to-Change Reconciliation

| Current plan scope | Changes evidence | Current-state reconciliation | Gap or rationale |
| --- | --- | --- | --- |
| P01-T01, FR1, AC1 | Specific ModelMismatch, model-specific shaping, mismatch completion branch | Reconciled | Closed outcome survives the real worker and JSON result roundtrip; invalid model values are null, not arbitrary objects or truncations. |
| P01-T02, FR2, AC2 | Parameter validation separated from consumption read hold handling | Reconciled | Valid held reads retain complete HTTP 200 reports; malformed parameters remain 400 before ledger access. |
| P01-T03, FR3-FR4, AC3 | Publication-only helper, saved legacy/priority fallback, backend-specific chat finalization | Reconciled | Original output immutability and financial admission/settlement remain intact. No predicted chat join or provider replay. |
| P02-T01 | External fixture controls, three added test methods and one extended existing HTTP method; five guide/knowledge updates | Reconciled | No removed tests, package-local new test files, schema changes or generated runtime targets; below four-method maximum. Knowledge log change is append-only. |
| P02-T02, AC4 | API/core checks and 326-test related regression command; focused rerun after typing guard | Reconciled | Checklist is intentionally unchecked while Review is pending. Handoff and changes distinguish completed checks from pending Review. The parent can now reconcile this completed Review without altering its original result. |
| P02-T03, publication portion of AC5 | Ordinary commit/push, exact-head CI, then precise thread replies/resolution | Accurately pending | Neither source evidence nor this Review proves those actions. Remains outside this source-acceptance verdict. |
| Follow-Up Items | Existing #432 price/billing/approval gaps retained in guides and evidence | Reconciled | Not folded into active correction tasks or whole-issue closure. |

## Completed Work Assessment

| Related marker | Files | What changed and why | Completion evidence and validation | Assessment |
| --- | --- | --- | --- | --- |
| P01-T01 | src/core/src/zava_forward/core/ai.py; src/core/src/zava_forward/core/ai_consumption.py; src/core/src/zava_forward/core/assistants.py | Preserve safe returned-model mismatch separately from retryable provider failure | ModelMismatch normalizes strings to at most 512 characters. evidence() retains outcome/model/settled usage but no provider text. shape_result() allowlists model with the same bound while retaining other metadata bounds. Independently passed mismatch worker-roundtrip test covers short, 121-, 512-, 513-character and object values. | Conformant |
| P01-T01 | src/core/src/zava_forward/core/assistants.py; unchanged src/agents/src/zava_forward/agents/dispatch.py | Quarantine mismatch independently of another completion denial and suspend the selected released record | Complete rejects unverified output, marks serving_attestation mismatch, suspends release, persists quarantined state and actual usage, closes active attempt, and makes its output join ineligible. Both claim and execute refuse retry. Existing provider-failure/revocation/fence and pending-rejection tests independently pass. | Conformant; returned-model comparison is not authoritative serving attestation |
| P01-T02 | src/api/src/zava_forward/api/server.py; src/api/tests/test_ai_consumption_api.py | Do not confuse a valid report's backend financial hold with invalid request parameters | Parameter names/cardinality and report_period validate first. Only report DispatchHeld becomes safe unavailable/Unknown consumption. Actual local HTTP test independently passes capacity and invalid-schema holds with all evaluation/live/registry sections and 400 invalid inputs, including unavailable backends. | Conformant; unrelated non-hold errors are not converted into successful held reports |
| P01-T03 | src/core/src/zava_forward/core/ai_consumption.py; src/core/src/zava_forward/core/ai_tasks.py; src/core/src/zava_forward/core/store.py | Keep strict output() and add narrow publication-only DispatchHeld handling after domain save | publish_output() catches only DispatchHeld, logs its safe code and returns unresolved/Unknown metadata. Legacy retains AI comparison but switches shown/returned text, model, source, citations, verification, envelope and mode to manual. Priority preserves AI comparison, switches shown/returned items/source/model/mode and recomputes overlap. Six independently passing capacity subtests verify SQL/JSON disk state and one provider request. | Conformant |
| P01-T03, PC-001 | src/core/src/zava_forward/core/chat_panel.py; src/core/src/zava_forward/core/chatthreads.py; unchanged SqlRepo/MemoryRepo | Bind financial output to the actual persisted message, not a predicted occupant | SQL allocates actual seq, validates owner/status/version, updates thread, runs private callback with self.db, inserts message, then commits the surrounding message transaction. Strict output receives that same db and cannot independently commit. Callback changes the not-yet-inserted message to FALLBACK/no evidence/workflow-only on hold. JSON first saves the real message, then joins its actual seq; on hold, only that seq's just-saved content/evidence/model are replaced under Store.lock and saved again. | Conformant; no schema or public message-edit API |
| P01-T03, FR4, AC3-AC4 | src/api/tests/test_ai_consumption_api.py; unchanged financial report and review contracts | Preserve immutable joins, truthful incompleteness and exception propagation | Actual ledger is filled to 9,999 closed-schema events; reservation/completion reach 10,001 without altered admission limits. No output join is created on held publication. Read-only test recovery retains all events, finds one unjoined root and incomplete/Unknown report. Subsequent production-bound dispatch remains held with no second HTTP call. SQL link RuntimeError and insertion failure roll back; JSON link RuntimeError and initial save failure propagate before a phantom join. Other SQL writer advances sequence and actual assistant seq 3 is joined ineligible. Existing legacy/priority repair and successful chat tests independently pass. | Conformant |
| P02-T01 | src/core/README.md; src/api/README.md; docs/reference/resources/ai-tokenomics.md; docs/reference/README.md; docs/reference/log.md | Document source-only controls and retained live gaps | Full documentation diff inspected, relative links retained, log additions only, git diff --check passes. No legal snapshot, initial case study, memory, price/budget authority or live approval is changed. | Conformant; synthetic source results are not business/live acceptance |

## Implementation-Time Plan and Detail Update Assessment

| Affected marker | What changed and why | Triggering evidence and user decision | Reconciliation and critique state | Assessment |
| --- | --- | --- | --- | --- |
| P01-T03 / PC-001 | Replace research's predicted-sequence pre-linking with actual SQL transactional finalization and JSON save-first replacement | Original critique identified phantom immutable joins after conflict/save failure. Existing owner direction already requires consistent delivery and original immutable attribution. | Current plan disposition and details explicitly select backend-safe actual sequence; changes record and fault/interleaving tests implement it. Research remains historical and its superseded C6 design is not treated as current authority. Original Revise critique preserved, direct disposition Ready. | Justified compatible correction, not unapproved scope expansion |
| P01-T01 / PC-002 | Define existing model field's consistent 512-character bound through worker shaping | Original shaping truncated all metadata to 120; critique required faithful bounded evidence through the allowlist/serialization | Current details, bounded_model(), shape_result(), exception/receipt and five model subtests agree. No broader metadata or permission contract changed. | Reconciled |
| P02-T03 / PC-003 | Require successful applicable CI on exact pushed head before thread resolution | Explicit user CI-publication decision; original critique identified premature resolution risk | Current plan/details retain ordinary push followed by exact-head CI and then resolution. Still pending, not represented as passed. Full local gate is not reintroduced. | Reconciled publication design; execution pending |
| P02-T02-P02-T03 / PC-004 | Preserve one original Review while forbidding false closure of unresolved scoped findings | Original critique distinguished out-of-scope follow-up from acceptance-disproving defects | Current plan/details require no unresolved scoped finding to permit success or thread resolution. This Review found no such defect. If later evidence exposes one, parent must record a separate evidenced disposition/correction, not rewrite this Review or manufacture a passing outcome. | Reconciled; no unconditional scoped-defect deferral accepted |
| P02-T01-P02-T02 | Fix fixture admission/latency and typing issues before Review, including final test-only typing guard | Changes record discloses initial failing attempts, missing SDK dependency restoration in existing isolated venv, then final pass | No manifest edits or typing exemption for new defects. Independently rerun package static checks and exact-capacity test pass on current source. | Compatible implementation refinement, no material plan revision needed |

## Critique and Material Revision Assessment

* Original critique execution Complete and outcome Revise are retained verbatim. This Review neither replaces nor relabels them.
* PC-001 resolving source and test evidence is present: actual SQL sequence and shared message/join transaction, rollback after join-before-insert failure, actual other-writer sequence, JSON save-first and targeted replacement. Successful existing joins remain ineligible chat joins to the actual assistant message.
* PC-002 resolving evidence is present across provider, worker, JSON serialization, task/attestation, settled financial usage and no retry. Invalid model values do not enter durable model fields.
* PC-003 is resolved as a planning disposition, not as performed publication: applicable exact-head successful CI and thread actions remain pending.
* PC-004's no-false-closure rule is retained. No material scoped defect was found; passing source tests still do not authorize premature thread resolution, altered historical Review findings or #432 closure.
* Significant implementation decisions agree with the owner's accepted boundaries. Plan/details/changes reconcile the compatible critique corrections before the asserted implementation. No evidence of dependent work proceeding against unresolved divergent authority was found.
* AC1-AC4 have conformant source evidence. AC5 is only partly evidenced: one independent critique and this one Review exist; commit/push/CI/thread publication work does not yet.

## Plan Follow-Up Assessment

| Follow-up item | Why outside immediate scope | Owner or next action | Assessment and route |
| --- | --- | --- | --- |
| Existing #432 live price, billing and approval gaps | Three source review-thread corrections do not supply applicable actual prices, Azure billing reconciliation, OD-51, complete resident/historical joins or an authorized held-out batch | Existing #432 workstream owner, with named Finance/Digital and approval authorities, to obtain and review missing live evidence under separate authorization | Open distinct follow-up; correctly retained in plan, changes and guides. No new active correction task or whole-issue closing claim. |

Unresolved follow-up work is not a source defect and is not added to P01 or P02 acceptance by this Review.

## Findings

No substantive actionable finding or material source issue was found within the assessed boundary. Severity summary: 0 Critical, 0 High, 0 Medium, 0 Low. No RV-xxx entry is fabricated for conformant behavior, already acknowledged publication work or out-of-scope live gaps.

## Defects

* None found. No implementation, planning or material research-gap handoff is required by this Review.

## Routed Findings

| Finding | Destination | Owner or next action | Reason for route |
| --- | --- | --- | --- |
| None | None | None | No substantive actionable review finding |

Later correction of any separately evidenced issue does not authorize repeating or relabelling this original Review.

## Residual Work

* Existing #432 live price/billing/approval and resident/historical evidence remains distinct follow-up work, not accepted source closure.
* P02-T03 is planned remaining publication work, not an unacknowledged defect or additional source acceptance criterion.

## Blockers and Remaining Work

* Source-review blockers: none.
* P02-T02: parent may record completion now that requested checks and this one Review are evidenced.
* P02-T03: authenticated privacy-safe author/committer setup, original implementation/evidence commit with required trailer, ordinary push, successful applicable exact-head CI verification, then three precise thread replies/resolutions. Until proven, these remain pending. Do not close #432.
* Remote PR head differs from this local baseline; no exact-head hosted acceptance is inferred. Parent owns final publication binding and CI.
* No live Azure SQL, paid provider, private dataset, deployment, human approval or operational serving attestation was exercised.

## Validation Evidence

Independent validation used the supplied external isolated venv's python/ruff/mypy, with no installation or manifest change. Unit fixtures construct local data and loopback providers; no private working-data path or paid inference was used.

| Command | Scope | Status | Summary |
| --- | --- | --- | --- |
| From src/api: ruff check .; ruff format --check .; mypy --cache-dir=/dev/null, with requested PYTHONPATH for typing | API static checks | Passed independently | All checks passed; 66 files formatted; 124 source files type checked. |
| From src/core: ruff check .; ruff format --check .; mypy --cache-dir=/dev/null | Core static checks | Passed independently | All checks passed; 117 files formatted; 170 source files type checked. |
| From src/api: python -m unittest test_ai_consumption_api.ConsumptionApi.test_model_mismatch_survives_worker_roundtrip_and_suspends_release test_ai_consumption_api.ConsumptionApi.test_exact_capacity_publication_returns_persisted_manual_routes test_ai_consumption_api.ConsumptionApi.test_chat_finalization_has_no_phantom_join_on_fault_or_other_writer test_ai_consumption_api.ConsumptionApi.test_manager_report_local_http_and_bad_period -q | All three added methods plus changed HTTP method | Passed independently | 4 tests, 27.223s, OK, no skips; bounded worker mismatch, six real-capacity SQL/JSON routes, faults/other writer and actual HTTP holds/invalid parameters. Includes exact-capacity current typing-guard candidate. |
| From src/api: python -m unittest test_ai_consumption_api.ConsumptionApi.test_legacy_and_priority_reviews_recover_only_committed_matching_links test_ai_consumption_api.ConsumptionApi.test_actual_worker_thread_settlement_survives_failure_revocation_and_fence test_ai_consumption_api.ConsumptionApi.test_actual_chat_adapter_preserves_metering_without_proposal_eligibility test_ai_consumption_api.ConsumptionApi.test_document_calls_preserve_shared_call_and_depth_limits test_ai_consumption_api.ConsumptionApi.test_failed_metered_provider_pending_task_can_be_rejected_without_redispatch -q | Adjacent immutable review/repair joins, ordinary errors, worker settlement/fencing, successful chat, document call limits and retryable failure | Passed independently | 5 tests, 20.544s, OK, no skips. Non-hold output errors propagate and original matching-link repairs remain intact. |
| From src/api with PYTHONPATH=.:src:tests:../core/src:../agents/src:../core/tests:../agents/tests: python -m unittest test_ai_consumption_api test_ai_consumption test_ai_tasks test_assistants test_assistants_dispatch test_assistant_release test_chat_panel test_chatthreads -q | Full relevant API consumption/core consumption/drafts/assistants/dispatch/release/chat/chatthreads suites | Passed, supplied implementation evidence | Changes record and caller report 326 tests, OK, 51 existing skips. Not independently rerun wholesale; independently selected nine composed methods above cover the corrections and tightly coupled unchanged contracts. |
| git diff --check; complete source/test/documentation diff inspection | Entire tracked correction | Passed independently | No whitespace errors, no staged changes, append-only log, no unrelated tracked change introduced by Review. |
| Complete tools/rpi-checks.py local publication gate | Publication | Not run, explicitly overridden | User selected CI rather than complete local gate. Not counted as a missing source-acceptance requirement. |
| Applicable hosted CI on eventual pushed exact head | Publication P02-T03 | Pending/not assessed | Cannot infer successful hosted checks from local tests or this Review; must precede final thread resolution. |
| Browser/full SQL/platform, live serving/billing and human approval | Outside focused source validation | Not performed | Existing optional skips do not establish conformance or live acceptance. No cloud fallback or paid call. |

## Outcome

* Outcome: Conformant for the completed source-implementation boundary.
* Rationale: all three thread contracts are implemented with bounded mismatch quarantine, complete held HTTP reports, and actual-capacity persistent manual publication. SQL joins use actual message sequence and the same committing transaction; JSON joins use actual saved message and replacement only on hold. Strict immutable output semantics, narrow error handling, settled usage, unrepaired incomplete economics and subsequent dispatch refusal remain intact. Independent composed tests and package static checks pass.
* This outcome does not assert whole-plan execution, publication AC5, live authority, hosted/human approval or issue closure. P02-T03 remains accurately pending.

## Closeout Routing Record

| Finding class | Destination | Owner or next action |
| --- | --- | --- |
| Implementation defect | None | No defect found |
| Decision gap or invalid assumption | None | Current compatible dispositions supported |
| Material evidence gap | None within source boundary | No rpi-research handoff required |
| Non-blocking residual work | Existing #432 follow-up | Existing workstream owner obtains authorized live/billing/approval and resident/historical evidence |
| Planned publication, not a finding | P02-T03 | Active parent records original Review, commits/pushes and verifies exact-head CI before thread resolution |

* Review execution status: Complete.
* Outcome: Conformant for source scope.
* Validation coverage: both packages' static checks and nine composed methods independently pass; supplied related regression evidence is 326 tests, OK, 51 existing skips.
* Blockers: none for source Review; publication and live acceptance remain unproven.
* Stop: this is the one original substantive Review. No second Review or source correction was performed.

| [.copilot-tracking/plans/2026-10-31/ai-metering-432-final-threads-plan.md](.copilot-tracking/plans/2026-10-31/ai-metering-432-final-threads-plan.md) | Current plan and pending publication |
| [.copilot-tracking/details/2026-10-31/ai-metering-432-final-threads-phase-details.md](.copilot-tracking/details/2026-10-31/ai-metering-432-final-threads-phase-details.md) | Backend-safe correction and publication contracts |
| [.copilot-tracking/reviews/plans/2026-10-31/ai-metering-432-final-threads-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-31/ai-metering-432-final-threads-plan-critique.md) | Preserved original Revise and PC-001 through PC-004 |
| [.copilot-tracking/changes/2026-10-31/ai-metering-432-final-threads-changes.md](.copilot-tracking/changes/2026-10-31/ai-metering-432-final-threads-changes.md) | Implementation and supplied validation evidence |
| [.copilot-tracking/research/2026-10-31/ai-metering-432-final-threads-research.md](.copilot-tracking/research/2026-10-31/ai-metering-432-final-threads-research.md) | Original trace and three thread references |
| [.copilot-tracking/rpi-sessions/2026-10-31/ai-metering-432-final-threads-state.json](.copilot-tracking/rpi-sessions/2026-10-31/ai-metering-432-final-threads-state.json) | Automatic parent continuation and accepted CI gate |
| [.copilot-tracking/reviews/logs/2026-10-31/ai-metering-432-final-threads-review.md](.copilot-tracking/reviews/logs/2026-10-31/ai-metering-432-final-threads-review.md) | One original independent Review result |

## Next Steps

The active parent records this original Review as Complete/Conformant for source
scope, reconciles P02-T02 completion, and continues authorized P02-T03 without a
new Review. Commit original evidence and implementation with privacy-safe
identity and required trailer, ordinary-push the candidate, verify successful
applicable CI on its exact PR head, then reply to and resolve only the three
evidenced threads. Leave publication pending until proven and retain Refs #432.
No user action or new RPI stage is required by a source finding.

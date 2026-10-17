<!-- markdownlint-disable-file -->
# Review: Consultation record controls #92

## Opening Review State

* Interpreted review goal: Independently assess the complete issue #92 implementation and RPI reconciliation once, retaining the original verdict.
* Review scope: Baseline 2b244568 through current tracked and task-owned untracked changes on feat/consultation-record-controls-92, including new core tests and dated research, plan, details, critique, changes and state.
* Evidence readiness: Branch and complete changed-file inventory identified; artifact contents and validation evidence await comparison.
* Acceptance basis: Approved isolated fail-closed synthetic mechanic; both exact issue criteria remain partial. Missing genuine Legal authority and let/renew seam are acknowledged residual work, not defects. Preserve #90 and #84/#94/#95 boundaries.
* First comparison boundary: Requirements and research against plan, critique and changes, then every changed source/test/documentation file and relevant unchanged control paths.
* Active read-only boundaries: Only this canonical review record may be written. No corrections, other artifact changes, agents, second review, private datasets, other worktrees, credentials or database mutation.
* Initial blockers: None identified.

## Scope and Evidence

* Task ID: 92; task slug: consultation-record-controls-92.
* Review date: 2026-10-17.
* Worktree: /home/azureuser/source/ama-wt/issue-92.
* Branch: feat/consultation-record-controls-92; baseline: 2b244568.
* Review scope: Full approved P01/P02 implementation, not operational legal sufficiency or full issue closure.
* Plan: .copilot-tracking/plans/2026-10-17/consultation-record-controls-92-plan.md.
* Phase details: .copilot-tracking/details/2026-10-17/consultation-record-controls-92-phase-details.md.
* Original critique: .copilot-tracking/reviews/plans/2026-10-17/consultation-record-controls-92-plan-critique.md.
* Changes: .copilot-tracking/changes/2026-10-17/consultation-record-controls-92-changes.md.
* Research: .copilot-tracking/research/2026-10-17/consultation-record-controls-92-research.md.
* State: .copilot-tracking/rpi-sessions/2026-10-17/consultation-record-controls-92-state.json.
* Requirements: Read-only `gh issue view 92 --json number,title,body,state` confirmed the open issue and its two unchecked criteria. The old "Not evidenced in mvp/" note is historical, not an accurate description of migrated procurement.
* Supporting evidence: Original case study, bounded addendum, KB index and memory, housing-association primer, regulatory register, BRD RULE-023/CON-004/AC-073, PRD FR-007/CON-002 and ADR 0005 exercise-owner scope.
* Complete implementation boundary: All 13 tracked changed files were read against baseline, plus the new untracked src/core/tests/test_consultation_controls.py and all seven task-owned research/planning/changes/state/review artifacts. Tracked scope is procurement.py, server.py, six existing test files, two component READMEs and three KB files.
* Source inspection also covered unchanged procurement authority/source/recovery paths, Store.advance, SQL writer validation/recovery, registered actor resolution, shared text/bulk checks and the existing MSSQL adapters.
* No other worktree, private dataset, secret file, SQL credentials, operational database or cloud resource was read. No agents, source corrections or second Review were used.

## Execution Status

* Execution status: Complete.
* Review execution evidence: One independent comparison of the entire supplied boundary; direct bounded JSON/SQLite/HTTP validation; complete final findings and routing recorded here.
* Implementation execution: P01/P01-T01/P02/P02-T01/P02-T02 are complete for the approved partial-engineering scope. This is separate from exact issue acceptance.
* Original independent outcome: Conformant with justified divergence. Preserve this verdict as historical evidence; do not replace it with a later correction or acceptance result.
* Severity summary: Implementation defects 0; decision gaps 0; material evidence gaps 0; accepted residual findings 2 Medium. Residual severity concerns eventual exact acceptance, not a request to fabricate missing authority or workflows.

## Plan-to-Change Reconciliation

| Current plan scope | Descriptive changes-record summary | Current-state reconciliation | Gap or rationale |
| --- | --- | --- | --- |
| P01 / P01-T01 | Record-only consultation, authenticated route and unknown gate | Reconciled | Existing provider package reused; manager recorder is not Legal; no release path introduced. |
| P02 / P02-T01 | Ten canonical core methods, three canonical HTTP methods and historical downstream states | Reconciled | Counts remain below 18 core / 4 API maxima; no existing test removal. Separate classes and cleanup isolate legacy-only patches. |
| P02 / P02-T02 | Component checks, actual local SQL parity, mutation evidence, migration and documentation | Reconciled | Parent results are distinguished from this Review's independently repeated checks below. |
| PC-001 / PC-002 | Direct planning dispositions applied before implementation | Reconciled | Historical unmocked seam tests and backend-selectable MSSQL suite are present; original Revise critique remains unchanged. |
| Follow-Up Items | Missing named Legal consultation authority and genuine let/renew integration | Reconciled, open | Both remain outside checked implementation markers and full acceptance claims; routed separately as RV-001/RV-002. |
| Handoff / state | Independent Review is active and next | Reconciled | State's active Review and null review pointer describe entry to this stage. Parent owns later state/PR continuation; this Review cannot edit state. |

Research's opening "Status: In progress" is historical metadata alongside an explicit executed disposition, final synthesis and Ready planning section. It does not create an unresolved research blocker. Current plan, details, changes and code consistently describe completed bounded engineering and partial exact criteria.

## Completed Work Assessment

| Related marker | Files | What changed and why | Completion evidence | Validation | Assessment |
| --- | --- | --- | --- | --- | --- |
| P01-T01 | src/core/src/zava_forward/core/procurement.py | New/legacy effective unknown; append supplied decisions with current recorder, source hash/version and package versions; hold consequential work | record_consultation at lines 282-313; five gate calls at 358, 406, 426, 460, 554; list projection at 543-546 | New unpatched JSON/SQLite tests passed here; parent reports actual SQL parity | Conformant to approved record-only scope |
| P01-T01 | src/api/src/zava_forward/api/server.py | One existing procurement dispatch route to record_consultation | Lines 695-696; existing authentication, POST checks, bulk refusal and error mapping retained | Six JSON/SQLite consultation HTTP executions passed here | No new approval role or API invented |
| P02-T01 | src/core/tests/test_consultation_controls.py | Ten semantic methods inherited by JSON, SQLite and opt-in MSSQL | Explicit historical order helper; exact consultation errors and state/audit invariance; source, identity, stale version and failure tests | Direct JSON/SQLite execution; SQL-specific JSON skip explicit | No consultation guard patch, including setup |
| P02-T01 | src/api/tests/test_procurement_api.py | Shared fixture with unpatched default, legacy-only opted-in patch and three new HTTP methods | Fixture lines 22-38; legacy class 122-123; separate ConsultationApi at 209 | New HTTP methods run after both legacy classes, followed by an unpatched core downstream test | No observed patch leakage |
| P02-T01 | src/core/tests/test_quality_procurement.py; src/core/tests/test_buildings.py; src/core/tests/test_hazard_referral.py; src/core/tests/test_resident_decisions.py; src/api/tests/test_role_matrix.py | Explicit test-local isolation of only the new hold | Setup/method patches each register addCleanup(stop); no other production control patched by this delta | Parent coupled regression evidence; legacy API classes repeated here | Independent-domain successes are not #92 release acceptance |
| P02-T02 | src/core/README.md; src/api/README.md; docs/reference/README.md; docs/reference/log.md; docs/reference/research/ux/zava-forward-prototype-profile-review.md | Document actual payload/controls, test isolation and exact acceptance limitations | Full diff read; KB index route and append-only log entry present | Diff whitespace check passed; related relative link targets/headings reviewed | Honest partial criteria and no legal-currentness/UI claim |

### Functional provenance and effective clearance

* record_consultation accepts exactly seven fields; enum, nonnegative integer expected_version, bounded strings and nonempty cleaned text are checked before mutation. Caller recorder/time/authority additions are rejected.
* The existing registered actor lookup is reused, not a request role claim. _proc_operation authenticates a current manager and skips contract-action delegation only for capacity and consultation; capacity still performs its original named delegation check explicitly. Existing issue/reissue/rescope/appointment/complete/correct/withdraw delegation paths retain their checks.
* The supplied decided_by string is unverified history, not an independently authenticated Legal adviser. recorded_by is copied from the current registry actor, separately from that claim; server recorded_at is UTC. No authority is derived from either the user's manager role or rule_owner.
* Source lookup reuses _capacity_source: exact case/document/version, clean scan, non-generated source and matching original byte hash. Record version is monotonic history length plus one; contract reference/version, scope version and content hash are captured with each entry.
* "Stale" evidence here means stale expected record version, a changed/missing source version or hash, or changed writer dependencies/current recorder. There is no invented legal review-expiry rule. Historic supplied entries are not reclassified as current Legal clearance when source, contract or scope changes.
* Both persisted consultation_status and package projection stay unknown. The guard always refuses, independently of saved positive status or mutated authority flags. Forged positive history therefore has no release effect. History remains application-level history, not a legally signed or externally immutable ledger.

### Guard coverage and preserved controls

| Consequential seam | Exact source evidence | Reachability evidence |
| --- | --- | --- |
| Issue | procurement.py:354-358 | New core binding_seams issues a separate eligible case after test-local history setup; HTTP tests also request a real issue after each status. |
| Reissue | procurement.py:399-406 | Historical Issued order, explicit reason and resident bindings. |
| Correction/reopening | procurement.py:453-460 | Historical Completed order, explicit correction and resident bindings. |
| Positive Booked appointment | procurement.py:418-426 | Historical Issued order and a valid future appointment date. |
| Final ordering | procurement.py:549-554 and unchanged store.py:502-514 | Historical Appointed order, latest Booked appointment and actual advance call, not a direct helper-only assertion. |

The core seam test at src/core/tests/test_consultation_controls.py:229-267 requires the consultation-specific refusal and unchanged procurement/audit for each path. Parent reports all five individually removed seam-call mutants killed by this same reachable test; this Review did not rerun those mutations. Direct execution reached all five seams without patching the guard.

Package drafting/rescope and capacity recording remain under their existing checks, with no new consultation prerequisite. Negative appointments, withdrawal and historical factual completion remain reachable and were exercised unmocked at test_consultation_controls.py:285-295. Nothing in the delta changes #90 quotas, original-source validation or named contract-action authority. Safety, resident and building checks remain in their production paths; the intentional new hold can precede them without granting clearance.

No stock/document provenance, financial matching, grant approval, Store/SQL validation hook, generated dataset or scenario hash was changed. This preserves the production boundaries of #84/#94/#95 by source comparison; their broader regression validation is parent-reported, not independently rerun in this Review.

### Transactions and recovery

* The new operation remains under the existing procurement lock/context. For SQL, _capacity_source registers the source case rowversion; validate_sql rechecks current actor, original procurement snapshot and source rowversion inside the writer transaction before record/audit commit.
* SQL save calls the existing change, bulk, stock, finance and procurement validation hooks unchanged. Consultation recording does not replace or disable any hook.
* Stale expected versions fail before append. On failed operations, the existing procurement exception path restores JSON procurement or invokes SQL _discard; the latter quarantines pending failed audit before recovery reads. No Store/SQL recovery rewrite was introduced.
* test_consultation_controls.py:190-200 exercises same-store and reopened-store stale versions. Lines 297-307 inject pre-save failure and compare persisted/reopened record and audit. Lines 309-350 inject source-rowversion, procurement-snapshot and current-recorder changes between validation and save, requiring refusal and unchanged procurement/audit.
* The injected dependency changes are controlled writer-boundary tests, not a claim of exhaustive thread/interprocess scheduling coverage. JSON persistence/audit retain their existing separate-file mechanism; this change does not establish a new cross-file transactional guarantee.

## Implementation-Time Plan and Detail Update Assessment

| Affected area or marker | What changed and why | Triggering evidence and user decision | Reconciliation performed | Planning and critique state | Assessment |
| --- | --- | --- | --- | --- | --- |
| P02-T01 / ownership lock | Explicit historical snapshots, unpatched new API class and per-seam mutation | PC-001; user prohibits invented approval | Plan lock, details, changes and actual tests agree | Direct compatible critique disposition recorded; original verdict retained | Applied, no unaccepted divergence |
| P02-T02 / ownership lock | New module exposes MssqlConsultation using existing local wipe/factory | PC-002; actual new-feature SQL evidence required | Plan selector, details and changes identify new core SQL suite | Direct compatible correction, shared MSSQL harness unchanged | Applied, actual SQL execution supplied |
| P02-T01 legacy targets | Role-matrix method additionally isolates consultation only | Expanded run hit historical issuance setup; user permits legacy-only isolation | Current scope and changes disclose test target; cleanup present | Immediately relevant test setup update, not a material runtime decision | Justified, no fresh plan/critique needed |
| P01 acceptance boundary | No positive release; no Legal mapping; no let/renew API | Research C3-C8 and explicit user-approved fail-closed partial scope | Requirements, code, docs, follow-ups and handoff agree | Approved direction, not an implementation-time authority expansion | Justified divergence from full issue completion |

## Critique and Material Revision Assessment

* Original independent critique outcome remains Revise, with two Medium findings; it was not replaced or reassessed as a second critique.
* PC-001 is directly addressed: exact historical states are seeded without guard patches; separate API inheritance prevents legacy setup patch adoption; consultation-specific refusals and before/after snapshots cover all five actual seams; parent supplies individual mutation-kill evidence.
* PC-002 is directly addressed: MssqlConsultation inherits the ten new core methods, makes the existing MSSQL factory through a lazy import, and opts in explicitly. Parent reports all ten actually passed against the owned SQL Server, rather than substituting only legacy adapters.
* Plan and phase details contain the final test recipes and completed markers; changes record records dispositions before implementation. No evidence of premature continuation against an unresolved critique decision or an unaccepted material revision was found.
* Source and tests implement the accepted isolated mechanic. A future genuine Legal authority contract or workflow integration would be distinct work, not an unrecorded change to this implementation's approval semantics.

## Plan Follow-Up Assessment

| Follow-up item | Why outside immediate scope | Owner or next action | Assessment and route |
| --- | --- | --- | --- |
| Named owner approves exact Legal consultation authority contract | Neither current registry nor ADR 0005 confers contract-consultation approval authority | Named accountable Legal/Procurement authority owners establish the contract and scope before integration | Open accepted residual, RV-001; distinct follow-up, not active implementation |
| Genuine letting/renewal integration | Current package is a draft/reference and work-order gates are not a contract let/renew command | Procurement workflow owner identifies the authoritative letting/renewal system and consequential seam | Open accepted residual, RV-002; distinct follow-up, not an invented API request |

Both are mirrored in changes Remaining Work and Acceptance Boundary and the READMEs/KB. Neither is included in active completion claims or treated as permission for an automatic approval.

## Findings

<!-- rpi:review id=RV-001 -->
### RV-001 [Medium]: Exact Legal-record acceptance remains an explicit human-authority follow-up

* Classification: Accepted residual work, not an implementation defect or missing approval to be manufactured.
* Related scope: Exact issue criterion 1; plan Follow-Up Items; BRD RULE-023/AC-073.
* Evidence: Issue #92 asks for a Legal consultation status on a contract record. src/core/src/zava_forward/core/procurement.py:299-317 records a current manager's supplied human decision but labels authority Unverified and leaves effective status unknown. docs/adrs/0005-regulatory-compliance-assistant.md:57-74 restricts the named exercise Legal capacity to fictional rule cards/source proposals and identifies real company authority as unknown. Plan lines 69-74 and 134 explicitly retain this partial criterion.
* Impact: Source-backed history can be reviewed, but no entry is evidence that an authorized Legal adviser made or approved the contract-consultation decision. Even supplied complete/not_applicable cannot release work. Full criterion 1 or operational release must not be claimed.
* Destination: Distinct follow-up for the named Legal and Procurement authority owners; no rpi-implement correction in this accepted task.
* Smallest useful next action: Obtain a human-approved, exact contract-consultation authority/delegation contract before separately planning its integration. Do not reuse rule_owner, promote the recorder or autogrant approval.

<!-- rpi:review id=RV-002 -->
### RV-002 [Medium]: Exact letting/renewal acceptance awaits a genuine authoritative workflow seam

* Classification: Accepted residual work, not a missing invented endpoint.
* Related scope: Exact issue criterion 2; plan Follow-Up Items; BRD RULE-023/CON-004.
* Evidence: Issue #92 requires unknown to block letting or renewal. Current procurement.py:260-280 creates a draft/reference; actual holds at 358/406/426/460/554 protect work-order confirmation and final ordering, not contract award/renewal. Plan lines 73-74 and 135 and docs/reference/research/ux/zava-forward-prototype-profile-review.md, Consultation record engineering continuation, explicitly distinguish the absent genuine seam.
* Impact: All five implemented consequential order paths fail closed, but their tests cannot establish enforcement in an absent contract/framework/call-off letting or renewal workflow. Criterion 2 remains partial and issue #92 should remain open.
* Destination: Distinct follow-up for the Procurement workflow/integration owner; no active source correction or API invention.
* Smallest useful next action: Identify the real authoritative let/renew operation and its responsible owner, then separately scope consultation enforcement at that actual transition while preserving #90 and independent human decisions.

## Defects

* None identified in the approved implementation boundary. No correction is requested or executed.
* Missing Legal authority and the nonexistent let/renew seam are not implementation bugs. Their limitations are retained as the two distinct residual findings above.

## Routed Findings

| Finding | Destination | Owner or next action | Reason for route |
| --- | --- | --- | --- |
| RV-001 | Distinct human-authority follow-up | Named Legal/Procurement owners approve the future exact authority contract | Current engineering deliberately cannot certify the supplied decision |
| RV-002 | Distinct workflow-integration follow-up | Procurement owner identifies the genuine authoritative let/renew seam | No such transition exists in the supplied implementation |

No rpi-implement, rpi-plan or rpi-research correction is required for this approved scope. Future separately authorized integration can use appropriate RPI stages, but is not added to P01/P02. Later implementation does not require another Review of this task.

## Residual Work

* RV-001 and RV-002 remain open before full issue acceptance or operational reliance.
* Preserve both unchecked exact issue criteria. Use Refs #92 rather than closing syntax in the eventual PR.
* Existing Legal-currentness, operational authority, real processing, browser/UI and cloud acceptance remain unclaimed, not failed backend implementation checks.

## Blockers and Remaining Work

* Review blockers: None.
* Remaining active P01/P02 implementation work: None identified.
* Exact issue acceptance prerequisites: Named human authority and genuine letting/renewal workflow, owned by the distinct follow-ups above.
* Parent continuation: Persist this one Review's result in parent-owned state and continue the authorized normal PR workflow. This Review does not alter state, commit, push, merge or close the issue.

## Validation Evidence

| Command or evidence | Scope | Status | Summary |
| --- | --- | --- | --- |
| Read-only `gh issue view 92 --json number,title,body,state` | Exact issue and state | Passed, independently executed | Open issue, two unchecked criteria; historic mvp note confirmed |
| `git diff --check 2b244568` | Tracked supplied diff | Passed, independently executed | No whitespace errors |
| Local unittest runner described below | New JSON/SQLite core and HTTP semantics, both legacy API classes, then unpatched downstream core test | Passed, independently executed | 35 executions, 34 passes, 1 explicit JSON-only SQL-writer skip; 14.513 seconds |
| Changes Validation Record and caller's supplied execution evidence | Procurement/building/hazard/resident/stock/finance/grant/role/core/API coupled run | Passed, parent-reported | 321 executions, 274 passes, 47 explicit opt-in/browser/JSON-writer skips; expected missing-law-store warnings mean unknown |
| Actual owned loopback SQL Server replay | New core10, unpatched HTTP3 and legacy procurement/API/stock/finance | Passed, parent-reported | 70 passes, no skips; not rerun here, no credentials read and no database altered |
| Five individually removed seam calls, in memory | Reachability and mutation sensitivity | Passed, parent-reported | Five of five mutants killed; source never mutated for this Review |
| Configured full core/API Ruff and mypy; targeted format | Component static checks | Passed, parent-reported | mypy 113/54 files; no separate static rerun here |
| Migration and scenario manifest suites | Rename/source-layout and unchanged public scenario contract | Passed, parent-reported | 25 migration and 8 manifest tests; not independently rerun |
| Related Markdown/link and diff review | Changed READMEs, KB route, synthesis and appended log | Passed, independently inspected | Correct related destinations and honest partial-acceptance prose; no repository-wide Markdown build exists |
| Browser/UI/accessibility, official legal-currentness, cloud and paid AI | Outside backend synthetic mechanic | Not run, intentionally excluded | No conformance, legal interpretation, deployment or operational acceptance claim |

Independent test reproduction: use installed .venv Python with PYTHONDONTWRITEBYTECODE=1 and PYTHONPATH=src/core/tests:src/api/tests:src/agents/tests; unset ZF_TEST_MSSQL; set Python tempfile.tempdir to the existing worktree-local .venv directory so all fictional scratch data remains inside this worktree and is cleaned by fixtures. Run unittest.TestLoader.loadTestsFromName in this order:

1. test_consultation_controls.JsonConsultation
2. test_consultation_controls.SqlConsultation
3. test_procurement_api.ProcurementApi
4. test_procurement_api.JsonProcurementApi
5. test_procurement_api.ConsultationApi
6. test_procurement_api.JsonConsultationApi
7. test_consultation_controls.SqlConsultation.test_every_binding_seam_has_a_reachable_consultation_hold

This order explicitly exercises legacy patch cleanup before new unpatched HTTP and downstream core controls. No fixture data or persistent source artifact changed during validation.

## Outcome

* Original outcome: Conformant with justified divergence.
* Rationale: Completed approved record-only engineering accurately captures unverified supplied-human history and fails closed at all five actual confirmation seams without conferring Legal authority. Provenance, expected versions, source dependencies, recovery, test ownership/isolation and documentation match the reconciled plan. The intentional divergence from full issue acceptance is explicitly authorized and documented, not concealed or filled by invented approvals/APIs.
* Findings: RV-001 and RV-002 are Medium non-blocking residuals for eventual exact acceptance; no implementation defect, material evidence gap or unaccepted decision gap identified.
* Preservation: This is the one original independent Review result. No correction, re-review or amended verdict was performed.

## Closeout Routing Record

| Finding class | Destination | Owner or next action |
| --- | --- | --- |
| Implementation defect | None | No correction requested |
| Decision gap or invalid assumption | None | Approved fail-closed scope preserved |
| Material evidence gap | None within assessed scope | SQL/mutation/static broad results explicitly attributed to parent evidence |
| Non-blocking residual work | RV-001 distinct authority follow-up | Named Legal/Procurement owners establish the exact approval contract |
| Non-blocking residual work | RV-002 distinct integration follow-up | Procurement owner identifies the genuine let/renew transition |

* Execution status: Complete.
* Original outcome: Conformant with justified divergence.
* Validation coverage: Direct 35 executions/34 passes/1 explicit skip plus independent complete diff/criteria review; parent-reported 321 coupled executions, 70 actual SQL passes, five killed seam mutations, static checks, migration25 and manifest8.
* Blockers: None to this bounded delivery; both exact issue criteria remain partial.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/research/2026-10-17/consultation-record-controls-92-research.md](.copilot-tracking/research/2026-10-17/consultation-record-controls-92-research.md) | Authority and workflow research assessed |
| [.copilot-tracking/plans/2026-10-17/consultation-record-controls-92-plan.md](.copilot-tracking/plans/2026-10-17/consultation-record-controls-92-plan.md) | Completed bounded plan and distinct follow-ups |
| [.copilot-tracking/details/2026-10-17/consultation-record-controls-92-phase-details.md](.copilot-tracking/details/2026-10-17/consultation-record-controls-92-phase-details.md) | Reconciled implementation and validation details |
| [.copilot-tracking/reviews/plans/2026-10-17/consultation-record-controls-92-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-17/consultation-record-controls-92-plan-critique.md) | Original Revise critique preserved |
| [.copilot-tracking/changes/2026-10-17/consultation-record-controls-92-changes.md](.copilot-tracking/changes/2026-10-17/consultation-record-controls-92-changes.md) | Implementation and parent validation evidence |
| [.copilot-tracking/rpi-sessions/2026-10-17/consultation-record-controls-92-state.json](.copilot-tracking/rpi-sessions/2026-10-17/consultation-record-controls-92-state.json) | Parent-owned active Review state, read only |
| [.copilot-tracking/reviews/logs/2026-10-17/consultation-record-controls-92-review.md](.copilot-tracking/reviews/logs/2026-10-17/consultation-record-controls-92-review.md) | One original independent Review and complete finding set |

## Next Steps

The active parent should retain this original verdict, record the Review handoff in its own state, and continue the authorized normal PR workflow with Refs #92 and both exact criteria explicitly partial. No defect correction or second Review is requested. Keep RV-001 and RV-002 as distinct human/workflow follow-ups. No user response is required for the accepted bounded delivery.

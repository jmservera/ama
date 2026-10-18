<!-- markdownlint-disable-file -->
# RPI Plan Critique: consultation-record-controls-92

## Metadata

* Task ID: 92
* Critique date: 2026-10-17
* Plan: .copilot-tracking/plans/2026-10-17/consultation-record-controls-92-plan.md
* Phase details: .copilot-tracking/details/2026-10-17/consultation-record-controls-92-phase-details.md
* Critique execution status: Complete
* Critique count: One independent final-candidate assessment. No subsequent critique performed.

## Inputs and Criterion Boundary

* Caller direction: execute exactly one critique, write only this artifact, and perform no implementation. The wider delivery requires actual ordered Research, Plan/critique, Implement and independent Review phases, src rather than mvp, preservation of #90, no invented Legal role, mappings, grants or approval decisions, and honest partial issue acceptance.
* Candidate inputs: the plan, phase details and research at the paths above and .copilot-tracking/research/2026-10-17/consultation-record-controls-92-research.md.
* Requirements evidence: read-only GitHub issue #92 title, body and both acceptance criteria; docs/brds/agentic-retrofit-programme-brd.md RULE-023, CON-004 and AC-073; original case study and bounded addendum, knowledge-base index, owner memory and regulatory source register.
* Bounded source evidence: src/core/src/zava_forward/core/procurement.py, src/api/src/zava_forward/api/server.py procurement dispatch, src/core/tests/test_quality_procurement.py test inventory, src/api/tests/test_procurement_api.py, src/api/tests/test_mssqlstore.py adapters, component README validation guidance and component pyproject.toml configurations. ADR 0005 exercise-owner scope was read directly.
* Decisions assessed: manager-recorded supplied human decision, four supplied statuses, permanently unknown effective clearance, unverified Legal authority, actual binding order holds, preservation of nonbinding operations, no invented let/renew seam, no full issue closure.
* Dependencies assessed: the research reports #90 merged through #384, #89 as hierarchy and #290 as historical skeleton. Current procurement source corroborates the existing authority/capacity/source controls; historical merge provenance was not independently re-investigated.
* Worktree inspection: feat/consultation-record-controls-92 at 2b244568; supplied planning/research/state files were already untracked. No open PR was returned for this head. Existing inputs were left untouched.
* Boundary: assess implementation-plan credibility against the supplied requirements and bounded source, not legal sufficiency, operational authority, executed test outcomes or full issue acceptance. Research's PRD pointers were considered as supplied evidence, not independently re-audited.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| Caller: ordered full RPI and one critique | Covered | Research records wider/deeper/contrarian waves; plan has P01/P02 implementation tasks and requires independent Review after reconciliation. Execution of later stages is not claimed. |
| Caller: src, not mvp | Covered | Runtime targets are existing src/core procurement and src/api server paths. |
| Issue #92 criterion 1 / C1, C7, C8 | Partial, explicitly accepted boundary | Supplied statuses are recordable, but a manager's recording is not a verified named Legal consultation decision. The plan explicitly preserves this gap. |
| Issue #92 criterion 2 / C3-C5 | Partial, explicitly accepted boundary | Real order confirmation paths are identified for holds; no dedicated contract/framework/call-off letting or renewal path exists in the supplied evidence. |
| No manufactured authority / ADR 0005 | Covered | Rule-owner/card-review authority is not consultation authority. Every supplied status remains unverified and effective unknown. No extra role, mapping or grant is proposed. |
| #90 authority, capacity and source controls / C3-C6, C9 | Covered in design; validation qualification needed | Existing checks remain; only the new consultation guard may be isolated in unrelated regressions. PC-001 and PC-002 specify the missing evidence wiring. |
| P01-T01 decision provenance and recording | Covered | Registered recorder, supplied named decision maker, source/version/hash, contract/scope binding, expected record version, server time and retained history are specified. |
| P01-T01 binding guard placement | Covered in design | Issue, reissue, correction/reopening, Booked appointments and require_booked_capacity are enumerated. PC-001 concerns proving each path, not adding another authority boundary. |
| P01-T01 preserved nonbinding operations | Covered in design | Drafts, capacity recording, negative appointments, withdrawal and factual completion retain their existing checks. |
| P02-T01 exact semantic tests and ownership lock | Partial | Counts and canonical modules are bounded; reachable downstream preconditions and patch lifecycle need an explicit recipe, PC-001. |
| P02-T02 JSON/SQLite/local SQL Server parity | Partial | Real local SQL validation is required, but the new core module is not wired into the existing MSSQL adapters, PC-002. |
| P02-T02 docs, checks, evidence and independent Review | Covered | Component checks, READMEs and existing KB synthesis/index/log updates are required; actual results and partial acceptance must be recorded. |
| Risks and external dependencies | Covered | Missing Legal authority and genuine let/renew integration remain external gaps, not implementation excuses or implicit approvals. |

## Verdict

* Original verdict: Revise.
* Severity summary: Critical 0; High 0; Medium 2; Low 0.
* Rationale: the selected record-only boundary respects the user's exact direction. Neither absent Legal authority nor absent let/renew workflow is a reason to invent a role, grant, decision or API. The remaining substantive gaps concern how the promised unmocked tests reach downstream seams and how the newly owned core tests execute against actual SQL Server. Both are direct planner corrections, not reasons to reopen the approved scope.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [Medium]: Specify reachable unmocked downstream tests and patch isolation

* Related IDs: P01-T01; P02-T01; Test Ownership Lock; acceptance criterion "All existing binding seams deny".
* Evidence: .copilot-tracking/plans/2026-10-17/consultation-record-controls-92-plan.md permits setup patches for existing success-flow tests while requiring all #92 tests to be unmocked. The phase details require denial at all consequential seams and preservation of nonbinding operations. In src/core/src/zava_forward/core/procurement.py:357-438, reissue, appointment, completion, correction and withdrawal require existing work orders with particular states. require_booked_capacity at :509 requires a single Appointed order and a latest Booked appointment. src/api/tests/test_procurement_api.py currently creates work orders through the ordinary issue route inside success-flow methods; its existing class is also the proposed location for new #92 HTTP tests.
* Concern: once issue is always held, normal public setup cannot reach downstream operations. The candidate does not specify how #92 tests obtain legitimate historical states without patching the guard, or how a permitted legacy setup patch is kept away from new tests in the same API class. A generic refusal can be caused by missing orders, wrong states or other existing checks rather than consultation. The same problem affects positive tests for historical completion, negative appointments and withdrawal.
* Impact: tests can report all paths blocked while a downstream consultation guard is missing, or unintentionally test a patched guard. Safe nonbinding paths can also become untested. This is an evidence gap in the candidate, not a claim that an implementation already contains these bugs.
* Smallest useful change: add a short test recipe to P02-T01 and the ownership lock. Use explicit, test-local historical order snapshots in the required Issued/Appointed/Completed states, with otherwise valid #90 and resident/safety prerequisites and no invented Legal approval. Persist the snapshots through the relevant backend and end fixture setup before the operation under test. Keep the consultation guard entirely unpatched for #92 tests, including setup; scope unrelated-domain patches to named legacy tests or an explicitly separate legacy class. Assert consultation-specific refusal and unchanged state/version/audit, not merely any error. Pair downstream holds with positive nonbinding-operation checks under the same unknown consultation boundary.
* Action owner: planning parent.
* Exact resolving evidence: revised plan/details identify the historical-state setup, patch boundaries and case-to-seam assertions for issue, reissue, correction/reopening, Booked appointment and actual case advancement through require_booked_capacity. They also identify positive negative-appointment, withdrawal and factual-completion cases. The implementation handoff requires those tests to detect removal of the corresponding guard, through a focused mutation or equivalent explicit guard-reachability assertion, without removing existing domain controls.
* Decision route: direct planner correction. No user decision or new authority is required.

<!-- rpi:critique id=PC-002 -->
### PC-002 [Medium]: Wire the new core consultation suite into actual SQL Server validation

* Related IDs: P02-T01; P02-T02; Non-Functional Requirements; Test Ownership Lock.
* Evidence: .copilot-tracking/plans/2026-10-17/consultation-record-controls-92-plan.md names src/core/tests/test_consultation_controls.py as the new canonical core target and promises real local SQL parity, but identifies no SQL Server adapter for it. src/api/tests/test_mssqlstore.py:155-173 shows MssqlProcurement inherits the old test_quality_procurement.SqlFlows and MssqlProcurementApi inherits test_procurement_api.ProcurementApi. Neither automatically discovers a new core module. src/api/README.md:129-134 recommends those existing adapters for #90. The phase details constrain shared changes to the API route and possible fixture helper, without declaring an MSSQL harness extension.
* Concern: running the existing procurement adapters can prove preserved #90 behavior and inherited HTTP tests, but cannot prove the new core consultation suite against SQL Server. The candidate leaves its parity requirement and declared test-write scope disconnected, especially for optimistic record conflicts, source rowversion changes at writer time, rollback and restart persistence.
* Impact: a nominally successful local SQL run could omit decision-record transaction semantics unique to #92 and be misreported as new-feature parity.
* Smallest useful change: identify one concrete reusable backend-test approach. Prefer a narrowly declared adapter in src/api/tests/test_mssqlstore.py that runs the new core consultation behavior against the existing task-owned MSSQL factory/reopen mechanism, or an equivalent backend-selectable harness within the new module. Declare any shared harness edit before implementation. Name the actual unittest selectors and opt-in configuration, and distinguish authored semantic methods from inherited backend executions under the existing test-count lock.
* Action owner: planning parent.
* Exact resolving evidence: revised P02-T01/P02-T02 and ownership lock name the new core test class, JSON/SQLite variants, actual MSSQL adapter or backend selector, precise local selectors and shared-file boundary. The mapped SQL cases include successful unverified recording/reload, competing expected-record versions, source-case rowversion and procurement snapshot conflicts at writer time, and failed-commit state/audit recovery. The changes evidence must record executed methods and skips, with no SQL-parity claim from legacy-only runs.
* Decision route: direct planner correction. No user decision, new runtime authority, Store schema change or broadened domain scope is required.

## Strengths and Residual Risk

* The plan correctly distinguishes the authenticated recorder from the supplied human decision maker and from verified Legal authority. This is safer and more accurate than promoting rule_owner or the ADR 0005 exercise owner.
* Complete and not_applicable supplied claims cannot release work. Applies is not completion. Unknown remains the effective value for new, legacy, invalid and stale records.
* The consequence of the accepted scope is intentional: no binding order issuance or positive confirmation can succeed in the unmodified application through these guarded seams, even after a positive supplied record. Legacy regression patches must never be described as an available application clearance path.
* Existing _proc_operation actor/snapshot dependencies and source-case rowversion validation are a credible reuse direction. A consultation-specific authentication exception must remain limited to recording and must not weaken existing contract-authority actions.
* The record is append-only by application, not a legally verified signature, an externally immutable ledger or a new authority registry. The plan does not claim otherwise.
* Full issue acceptance remains unavailable: neither an actual named Legal consultation capability nor an actual let/renew workflow is supplied. Current explicit user direction already settles the bounded partial-delivery choice; no further approval is needed to retain it.

## Questions or Blocking Evidence Gaps

* No user question is necessary for these planner-owned revisions.
* Verified Legal consultation authority and genuine letting/renewal remain external acceptance prerequisites, not blockers to this bounded record-only implementation and not critique findings requesting manufactured authority.

## Limitations

* This is a plan critique. No implementation, application tests, local SQL container, mutation run, lint, typing or operational legal check was executed.
* Source inspection was bounded to the supplied procurement path, relevant test harnesses and directly related documentation. Other domains were not independently audited.
* No current-law interpretation or activation decision was made. The regulatory register and ADR were used only to verify the human-approval boundary.
* Only this critique artifact was written; plan, details, research, state and implementation sources remain unchanged.

## Recommended Next Action

* Highest-impact finding: PC-001.
* Action owner: planning parent.
* Smallest next action: specify the unmocked historical-state test recipe and patch lifecycle, then wire the same behavior suite to actual SQL Server as PC-002 requires.
* User response required: No.
* Handoff: preserve this original Revise verdict, record each direct disposition in the existing planning artifacts, and finalize the plan without commissioning a second critique. Continue implementation and the separately required independent implementation Review only after those corrections.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-17/consultation-record-controls-92-plan.md](.copilot-tracking/plans/2026-10-17/consultation-record-controls-92-plan.md) | Final-candidate plan assessed |
| [.copilot-tracking/details/2026-10-17/consultation-record-controls-92-phase-details.md](.copilot-tracking/details/2026-10-17/consultation-record-controls-92-phase-details.md) | Implementation and validation details assessed |
| [.copilot-tracking/research/2026-10-17/consultation-record-controls-92-research.md](.copilot-tracking/research/2026-10-17/consultation-record-controls-92-research.md) | Supplied research and authority-gap evidence |
| [.copilot-tracking/reviews/plans/2026-10-17/consultation-record-controls-92-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-17/consultation-record-controls-92-plan-critique.md) | Original independent critique and complete actionable finding set |

## Next Steps

The active planning parent should resolve PC-001 and PC-002 directly, retain the record-only partial-acceptance boundary and finalize without another critique. No user response is required. This critique execution stops here; implementation is outside its write authority.

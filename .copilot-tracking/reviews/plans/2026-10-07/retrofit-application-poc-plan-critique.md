<!-- markdownlint-disable-file -->
# RPI Plan Critique: Proper Warm Architecture and PoC

## Metadata

* Task ID: 4aaf9ee3-da69-4ebb-812a-edccc5637af7
* Critique date: 2026-10-07
* Plan: .copilot-tracking/plans/2026-10-07/retrofit-application-poc-plan.md
* Phase details: .copilot-tracking/details/2026-10-07/retrofit-application-poc-phase-details.md
* Critique execution status: Complete
* Critique count: One final-candidate assessment. No second critique requested or required.

## Inputs and Criterion Boundary

* Caller requirements: architecture plus runnable PoC; document everything created; confirmed automatic local synthetic PoC first. Production unknowns are disclosed release blockers, not reasons to stop that PoC.
* Primary inputs: the plan and phase details above, including AC-P01 through AC-P07, locked targets, no removals, maximum additions, backend semantic-test ownership and parent integration-test ownership.
* Supplied research: .copilot-tracking/research/2026-10-07/retrofit-application-poc-research.md, C3-C10/W1-W3; .copilot-tracking/research/subagents/2026-10-07/retrofit-poc-contract-lane.md.
* Requirements evidence: docs/prds/proper-warm-retrofit-programme-demonstrator.md, draft v0.7.0, component contracts, FRs, constraints, lifecycle and ACs; docs/case_study_48_original.md; relevant opening/control sections of docs/case_study_48_addendum.md.
* Context: docs/reference/README.md, docs/reference/memory.md and the opening of docs/reference/research/sector/housing-association-primer.md. Memory is context, not evidence.
* Assessment standard: docs/reference/method/ama-capstone-assessment-guide.md, all twenty criteria and floor rules. This critique assesses a build plan, not panel performance or capstone approval.
* Decisions retained: dependency-free Node 24 modular monolith, one SQLite process, same-origin UI, local Docker volume, simulator-only assistant and proposed Azure-led hybrid architecture. No live model, Azure deployment, tenant write, full workbook import or full PRD MVP is required.
* Boundary: assess implementation readiness, synthetic authority/gates, idempotency/recovery, backend/frontend API viability, inventory and validation. No external research, implementation or research redesign was performed. The API findings concern the included local integration, not deferred external adapters.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| Architecture and runnable PoC; C3-C5/W1-W3; P02-T02 | Covered | Actual local runtime is separated from proposed Azure services, scale-out migration and production release blockers. |
| Local-first decision; locked target/removal/addition/test boundary | Covered | Findings fit existing targets and owners; no new service, dependency, architecture document or removal is necessary. |
| AC-P01/P02; PRD FR-008/013/016-019; P01-T01 | Partial | Named actions and stages exist, but authority and exact release/acceptance predicates remain implicit: PC-001. |
| Versioned evidence; PRD FR-009/010/014; P01-T01 | Partial | Mutable decisions/evidence have no affected-approval invalidation or return contract: PC-002. |
| Idempotency and concurrency; AC-P01/P03; P01-T01 | Partial | Atomic storage is selected, but lost-response retries, actor scope and replay ordering need an explicit oracle: PC-003. |
| Backend/frontend contract; P01-T01/P02-T01 | Partial | Routes are listed; action schemas, role propagation, handoff invariants and response handling are not stable enough for independent implementation: PC-004. |
| Fail-closed recovery; AC-P03; P01-T01/P03-T01 | Partial | Restart and rollback tests are named without a storage-failure/restart reconciliation scenario: PC-005. |
| Nine representations, narrower-than-MVP disclosure; AC-P07; C7-C10 | Partial | Broad exclusions are honest, but a scenario/requirement manifest must distinguish included controls from omitted paths: PC-006. |
| No-access rule; PRD FR-031/AC-033; P01-T01 | Partial | Boundary count is tested, but counted evidence, investigation-task creation and active-case semantics are not specified: PC-007. |
| Simulator/failure handling; AC-P05; P01-T01/P03-T01 | Partial | No real autonomy is claimed; source-validation oracles and durable owned fallback are unspecified: PC-008. |
| Created resources; AC-P06; P02-T02/P03-T01 | Partial | Ledger and scoped cleanup are sound in intent; collision/reuse and test-data boundaries need an executable rule: PC-009. |
| UI/metrics, performance and accessibility; AC-P04/P07; P02-T01/P03-T01 | Covered with bounded limitations | Derived cohort metrics, visible rejection, browser checks and measured localhost p95 are planned. These are engineering observations, not company SLO or accessibility conformance evidence. |
| Publication and one Review; P03-T02 | Covered | Dedicated PR tool, topic branch, no merge and one later Review are specified. This assessment does not approve publication of failing acceptance gates. |

## Verdict

* Verdict: Revise.
* Severity summary: 0 Critical, 2 High, 7 Medium, 0 Low.
* Rationale: the selected approach is credible and supplied evidence supports local implementation. Several contracts still permit incompatible implementations or false synthetic readiness. Resolve the nine bounded planning corrections below, then finalize and proceed without another critique. There is no decision-critical research blocker or unresolved user choice.
* Resolution convention: the exact evidence below means revised planning contracts and assigned acceptance oracles before implementation. The named runtime/test outcomes are subsequently required implementation evidence, not a demand to build during planning.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Release and acceptance gates are not executable contracts

* Related IDs: AC-P01, AC-P02; P01-T01; PRD FR-008, FR-013, FR-016-019; AC-011, AC-016, AC-019-022, AC-042.
* Evidence: .copilot-tracking/details/2026-10-07/retrofit-application-poc-phase-details.md, P01-T01, lists roles/actions and says `advance` checks stage-specific requirements; it does not map actions to roles or each stage edge to concrete prerequisites. The plan promises separate sign-offs, committed capacity, invoice match and all applicable gates.
* Concern: assessment submission could count as its own professional review; a capacity commitment could substitute for budget/contract/work-release evidence; installation could bypass resident/design scope checks. `handed_over` also lacks a separate handover-acceptance predicate, despite the PRD distinguishing stage from accepted outcome. Role names alone do not determine which actor can approve, submit or advance.
* Impact: a happy journey can appear controlled while omitting the very approvals the demonstration is meant to prove.
* Smallest useful change: add a synthetic action-to-role and stage-edge gate matrix in phase details. Define assessment submission versus review, design approval, measure decision, package/capacity/release evidence, provider submission versus independent quality acceptance, and handover acceptance. Identify applicable budget/funding/contract/invoice checks, including where a check is not applicable rather than treating unknown as pass. Keep recorded exercise authority explicitly distinct from live approval; define who may invoke `advance` without granting it approval powers.
* Action owner: planning parent; backend implementer owns the corresponding semantic/API tests.
* Exact resolving evidence: P01-T01 contains every included action's permitted role(s), every lifecycle edge's required fields/current evidence versions and stable rejection code/owner, and AC-P01/P02 require one happy edge plus missing, unauthorised and non-applicable gate tests. Include provider self-acceptance denial and `handed_over` versus accepted-handover metric assertions.
* Decision route: direct planner correction. Use a declared synthetic authority matrix; no company ratification or production authority decision is needed now.

<!-- rpi:critique id=PC-002 -->
### PC-002 [High]: Material changes can leave stale approvals and advanced state intact

* Related IDs: AC-P01/P02; P01-T01; PRD FR-005, FR-009/010, FR-013/014/017; AC-008, AC-012/013, AC-037.
* Evidence: .copilot-tracking/details/2026-10-07/retrofit-application-poc-phase-details.md includes repeat assessment/design/decision/quality actions and versioned case JSON, but only a forward lifecycle and `return_handoff`. The contract lane explicitly identifies affected-approval invalidation on return or reopen.
* Concern: case versioning is not approval validity. A new design/scope, replacement evidence or withdrawn resident decision may leave an old approval or advanced lifecycle appearing valid. Continuing checks on `advance` do not correct already-scheduled or installed state. A handoff return is not a technical/quality return.
* Impact: the PoC could show current consent and evidence alongside an acceptance derived from superseded inputs, and cannot demonstrate recovery of the quality exception.
* Smallest useful change: define which included commands replace material inputs and invalidate which dependent approvals. Add a bounded return/reassessment command, or explicitly reject material replacement after dependent approval until an authorised return. Preserve prior records, scope/version links, reason, receiving owner and next action; unrelated approvals remain intact. No full generic reopen engine is required.
* Action owner: planning parent; backend implementer.
* Exact resolving evidence: P01-T01 includes a dependency/invalidation table and allowed recovery path; planned tests cover design v2 versus decision/approval v1, withdrawal after scheduling, quality return/reinspection, and unaffected measure/history retention. API/UI acceptance requires visible pending-reassessment status rather than stale readiness.
* Decision route: direct planner correction within the existing controlled-lifecycle scope, not a full-MVP expansion.

<!-- rpi:critique id=PC-003 -->
### PC-003 [Medium]: Lost-response replay semantics remain ambiguous

* Related IDs: AC-P01/P03/P04; P01-T01, P02-T01, P03-T01; PRD component contracts and bounded-agent orchestration.
* Evidence: phase details define idempotency `(case/key, actor, request hash, stored response)` and optimistic versions, but not validation ordering, hash contents, actor/key collision behavior or UI retry behavior.
* Concern: a committed request retried after a lost response necessarily carries an old `expectedVersion`. Checking version first rejects the valid retry; ignoring actor or payload differences may replay another role's response. Generating a new key after an ambiguous timeout can duplicate a command. A saved replay snapshot may also be older than subsequent case changes.
* Impact: apparently successful idempotency tests could miss the real network-recovery path and return stale UI state.
* Smallest useful change: specify role authorization plus actor/intent-bound replay lookup before fresh-command version checks; canonical hash inputs and key uniqueness/conflict policy; retention across restart; and distinction between replayed original response and current case. Have the UI retain the exact request/key while outcome is uncertain, then refetch current detail before its next action.
* Action owner: planning parent; backend implementer owns semantic/API tests, frontend implementer owns client retry state, parent owns integration.
* Exact resolving evidence: revised details state the algorithm and statuses; AC-P01/P03/P04 include commit-then-response-loss retry, restart replay, role collision, changed payload/version conflict, and replay after a later successful command. Tests require one original event/version increment and no overwrite of later state.
* Decision route: direct planner correction.

<!-- rpi:critique id=PC-004 -->
### PC-004 [Medium]: The shared API contract does not yet constrain command or handoff interpretation

* Related IDs: P01-T01, P02-T01; AC-P01/P04; PRD FR-011, FR-033/034; AC-014, AC-035/036.
* Evidence: phase details name routes and envelope shapes, permit a JSON payload editor, and require role-sensitive `allowedActions`; concrete command payloads, role selection for GET/assistant/export, filter values and action errors are not defined.
* Concern: separately built UI and server can disagree on source/evidence structures, role propagation and action fields. A fixed role mapping does not by itself stop a valid role accepting a handoff addressed to a different destination, accepting before receipt, or overwriting chase/update ownership through payload fields.
* Impact: integration can fail late or mutate ownership incorrectly despite passing isolated role tests.
* Smallest useful change: freeze the included command payload/response schema and required/unknown-field policy before parallel build. State how the selected demo role reaches each relevant endpoint and which reads are deliberately unrestricted synthetic views. Define server-owned fields, filter/query semantics, handoff ID/state/destination guards, allowed-action meaning and stable error codes. Keep resident-update reassignment separate from operational handoff acceptance.
* Action owner: planning parent freezes the contract; backend and frontend implementers consume it without independently inventing alternatives.
* Exact resolving evidence: P01-T01/P02-T01 contain a shared action contract table and representative requests/responses; planned API checks deny cross-destination acceptance, premature acceptance and owner-field injection. Parent browser checks include one accepted command, one denied command, version conflict/recovery, and unchanged resident-update owner through a return/acceptance sequence.
* Decision route: direct planner correction. No real record/field authorization claim is required; explicit synthetic read limits remain acceptable.

<!-- rpi:critique id=PC-005 -->
### PC-005 [Medium]: Persistence validation does not prove fail-closed recovery after interrupted writes

* Related IDs: AC-P01/P03; P01-T01, P02-T02, P03-T01; PRD programme-store/orchestrator failure contracts.
* Evidence: phase details promise a transaction, rollback, file-backed restart and a health/store probe. P03-T01 verifies restart after a successful command, not interrupted commit or store failure; seed initialization/recovery semantics are unspecified.
* Concern: an orderly restart does not establish consistency among case JSON, event sequence and replay record when a write fails or the process is interrupted. A store-open error or partial seed must not be handled by silently creating/resetting cases. Recovery and health meaning are needed even in a single-process demonstration.
* Impact: recoverability could be claimed from persistence alone, while an exceptional write loses history, repeats an event or recreates the fixture state.
* Smallest useful change: specify atomic seed-on-empty initialization with a schema/seed marker, preserve-on-restart behavior, fail-closed store-error handling and an owned manual recovery route. Assign one injected failure between mutation/event/idempotency writes and one process-interruption or equivalent durable restart scenario. Separate liveness from writable-store readiness; record reset/restore as explicit destructive/manual actions.
* Action owner: planning parent; backend implementer owns store fault tests, parent owns container recovery and runbook evidence.
* Exact resolving evidence: details name fault points and expected unchanged-or-fully-committed state; AC-P01/P03 require reopening the file and reconciling case version, events and replay entry. The runbook plan says unreadable/incompatible storage fails visibly without reseeding; validation records the health/error/owner and subsequent safe retry.
* Decision route: direct planner correction. Production RPO/RTO and managed-store design remain deferred.

<!-- rpi:critique id=PC-006 -->
### PC-006 [Medium]: Scope disclosure lacks an exact scenario and requirement coverage oracle

* Related IDs: AC-P01/P02/P07; P02-T02/P03-T01; C7-C10; PRD FR-002, FR-019, FR-035; AC-002/003, AC-022, AC-043.
* Evidence: the plan honestly excludes full MVP surfaces, but its nine fixture names do not establish expected safe endpoints or shared-building checks. Phase details reduce the grant ledger to opportunity/awarded/claimed/received, whereas the PRD separates claimable, submitted and accepted/rejected states.
* Concern: "all nine workflows" can mean nine filters rather than nine tested behaviors. A common building ID cannot prove independent home gates. The grant reduction could be mistaken for delivered PRD semantics, especially if claimed and accepted amounts share a field.
* Impact: documentation may overstate coverage and tests may lack a reproducible oracle for omissions or independent home readiness.
* Smallest useful change: declare a versioned constructed-scenario/traceability manifest within existing application/docs targets. Map each represented workflow to fixture IDs, commands, blocked/success endpoints and tests; map relevant PRD checks to implemented/partial/deferred with reasons. Include two homes sharing a package with different decisions/holds. Either represent the PRD grant distinctions in the existing ledger or explicitly disclose unsupported stages and prevent "claimed" from implying accepted or received.
* Action owner: planning parent; backend implementer supplies fixture/test identifiers, frontend implementer supplies available/unavailable surfaces.
* Exact resolving evidence: P02-T02/P03-T01 require the manifest and its planned test linkage; all nine rows have executable or read-only safe-endpoint assertions, the paired-home test denies inherited approval, and the grant mapping identifies each represented/omitted state. Coverage does not mark deferred checks as full-MVP passes.
* Decision route: direct planner correction. The existing narrower PoC decision stands; do not add full analytics, eleven production workspaces, import or external integrations.

<!-- rpi:critique id=PC-007 -->
### PC-007 [Medium]: The sixth no-access event has no specified investigation or lifecycle effect

* Related IDs: P01-T01; AC-P01; PRD FR-031/AC-033; owner-directed rule in docs/case_study_48_addendum.md, Missed-Appointment Escalation Evidence.
* Evidence: plan/details preserve strict greater-than-five and excluded outcomes, but specify only `record_appointment` and boundary tests. They do not specify a configurable/versioned threshold, eligible-event evidence, owned investigation task or human-close/reset handling.
* Concern: counting six can satisfy the named test while creating no human review work, counting duplicate/unverified appointments, or clearing history through an implicit lifecycle change.
* Impact: the demonstrator can suggest escalation occurred when only a number changed, or mistake no-access for refusal.
* Smallest useful change: define confirmed/verified counted-event fields, appointment identity deduplication, rule version/default and the one owned investigation created when the active case first exceeds the threshold. Specify whether closure/reset is supported. If not, keep the case active and disclose reset as unavailable; never reset on restart, stage advance or UI filter reset.
* Action owner: planning parent; backend implementer.
* Exact resolving evidence: details require event IDs/rule version and task owner/reason; planned tests cover five versus six, a duplicate event under a different command key, unconfirmed/unverified events, excluded outcomes, repeated above-threshold events, unchanged consent and hazard referral, and the supported or explicitly deferred reset path.
* Decision route: direct planner correction using the already confirmed provisional exercise rule, not a new operational threshold decision.

<!-- rpi:critique id=PC-008 -->
### PC-008 [Medium]: Assistant failure ownership and evaluation are not observable enough

* Related IDs: AC-P05; P01-T01/P02-T01/P03-T01; PRD FR-025-028; AC-028-030.
* Evidence: phase details prescribe a cited simulator response and explicit error with manual owner; the plan promises an owned manual task. No task record/visibility, invocation history, source-version validation or defined evaluation oracle is specified.
* Concern: returning an owner string is not the promised persistent manual task. A citation can be nonempty but nonexistent or superseded. No model is required, but even simulator validity/prohibited-action assertions need known inputs and measurable expected results.
* Impact: failure may disappear on refresh and the evaluation can report success without demonstrating supported drafts or a usable workflow-only recovery path.
* Smallest useful change: define structured citation IDs/versions and a small fixed evaluation set with expected source support, draft status, unsupported-output handling and prohibited-action checks. Persist a bounded assistant attempt/failure/manual task or explicitly narrow the task claim to a visible manual route with recorded invocation evidence. Clarify that no controlled stage/evidence approval changes on either success or failure; any task creation uses the authoritative API/store boundary.
* Action owner: planning parent; backend implementer owns simulator evaluations, parent owns browser evidence.
* Exact resolving evidence: AC-P05 details name evaluation fixtures, per-check counts and pass criteria, including missing/stale citation, hostile source text, disabled/failure mode and unchanged controlled state. The planned UI/restart check verifies the fallback owner/next action and retained failure evidence. Reports remain labelled simulator-only.
* Decision route: direct planner correction. Real-model comparison, live AI integration and genuine autonomy remain disclosed future release work.

<!-- rpi:critique id=PC-009 -->
### PC-009 [Medium]: Resource creation and cleanup need a shared-environment ownership rule

* Related IDs: AC-P03/P06; P02-T02/P03-T01; locked generated targets.
* Evidence: phase details choose Compose project `proper-warm-poc`, a named volume and port 3410, with exact-name cleanup and isolated temporary test databases. They do not distinguish pre-existing resources from newly created ones or reserve a safe test-data location.
* Concern: an automatic run can encounter an existing project/volume/port and silently reuse or later delete someone else's data. Restart tests must not target an unrelated volume. Tests using operating-system temporary directories also conflict with the supplied no-temporary-directory constraint.
* Impact: inventory can falsely claim creation, persistence evidence can use stale data, and cleanup/reset can affect non-task resources.
* Smallest useful change: add a before-create collision check and task-owned Compose label/name policy; fail or use a documented distinct scoped name on conflict, never adopt/delete a foreign resource. Record created versus reused versus planned status, persistent objects and task-generated files. Put isolated test databases in a dedicated ignored workspace-relative scratch path, not OS temporary directories; close/remove only those test files. Verify the non-root app can write its actual named volume. Leave the requested demonstrator available and clean only owned bounded helpers.
* Action owner: planning parent, including resource ledger/runbook and runtime validation.
* Exact resolving evidence: P02-T02/P03-T01 prescribe pre/post inventory, collision behavior, task ownership, named-volume write/restart checks, scratch paths and project-scoped stop/reset commands. Ledger acceptance includes actual names, image digest, port, volume/network, generated file locations/status, creation or reuse basis and zero Azure/M365 creations; no credentials or account IDs.
* Decision route: direct planner correction. No additional cloud permission or user decision is required.

## Strengths and Residual Risk

* Architecture and runnable application are both first-class deliverables; the plan does not confuse the existing read-only HTML with a transactional system.
* One authoritative API, transactional SQLite writes, demo-role disclosure, persistent events and same-origin/local-only deployment are proportionate to the chosen synthetic scope.
* Hazard holds remain immutable in this application. Acknowledgement does not confer release authority or control the external hazard clock.
* Resident decisions are scoped, provider submission is separated from review, operational ownership transfers on acceptance and resident-update continuity is explicitly preserved.
* Portfolio metrics derive from the inspectable filtered cohort rather than unrelated illustrative totals.
* Azure/M365 creation is not required. Proposed target services, managed identity versus human authority, SQLite scale limits and future model evaluation are disclosed correctly.
* All twenty rubric criteria and floor limits are assigned for documentation. Simulator evidence cannot establish A6 real-model selection/evaluation or A7 genuine autonomy; live presentation, stakeholder validation and dissemination scores remain unproven.
* Full PRD MVP, real identity/permissions, operational legal/professional/Finance authority, data protection release and cloud resilience remain explicit future blockers. They are not findings requiring this local PoC to stop.

## Questions or Blocking Evidence Gaps

* None requiring a user answer or new research cycle. The planning parent can set declared synthetic contracts and acceptance oracles directly from the supplied evidence.
* If an implementer discovers that the locked boundary cannot satisfy an included acceptance criterion, record that actual contradiction and route it to the parent rather than silently broadening scope or making an operational claim.

## Limitations

* This is one assessment of the supplied final candidate, not a code review or runtime certification. No implementation, fault injection, browser run or resource creation was performed by this critique.
* Existing source documents, tracking research and owner memory were not changed. Only this requested critique artifact was written.
* External documentation was not refreshed: supplied research already establishes local Node/SQLite viability and Azure storage/identity constraints. Target deployment API/service availability is a future release check, not demonstrated here.
* Provisional requirements and synthetic role mappings do not establish actual company staffing, delegated powers, platform approval, safety compliance or benefits.

## Recommended Next Action

* Highest-impact finding: PC-001.
* Action owner: planning parent.
* Smallest next action: freeze the synthetic action/authority/stage-gate matrix, then resolve PC-002 through PC-009 in the existing plan/details and record all dispositions.
* User response required: No. All findings are direct planner corrections under the confirmed local-first automatic instruction.
* Handoff: finalize the amended plan and continue to Implement, preserving locked targets/test owners and the single later Review. Do not dispatch a second critique.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-07/retrofit-application-poc-plan.md](.copilot-tracking/plans/2026-10-07/retrofit-application-poc-plan.md) | Final-candidate plan assessed. |
| [.copilot-tracking/details/2026-10-07/retrofit-application-poc-phase-details.md](.copilot-tracking/details/2026-10-07/retrofit-application-poc-phase-details.md) | Contracts and acceptance oracles to revise. |
| [.copilot-tracking/research/2026-10-07/retrofit-application-poc-research.md](.copilot-tracking/research/2026-10-07/retrofit-application-poc-research.md) | Supplied research and local-first decision. |
| [.copilot-tracking/research/subagents/2026-10-07/retrofit-poc-contract-lane.md](.copilot-tracking/research/subagents/2026-10-07/retrofit-poc-contract-lane.md) | Requirements/contract evidence lane. |
| [.copilot-tracking/reviews/plans/2026-10-07/retrofit-application-poc-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-07/retrofit-application-poc-plan-critique.md) | Complete one-pass actionable finding set. |

## Next Steps

Active planning parent: disposition all PC-001 through PC-009, finalize the bounded plan and proceed automatically to implementation. No user action or second critique is required.

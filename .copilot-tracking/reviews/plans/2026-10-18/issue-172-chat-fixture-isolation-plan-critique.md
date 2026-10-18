<!-- markdownlint-disable-file -->
# RPI Plan Critique: issue-172-chat-fixture-isolation

## Metadata

* Task ID: jmservera/ama#172
* Critique date: 2026-10-18
* Plan: .copilot-tracking/plans/2026-10-18/issue-172-chat-fixture-isolation-plan.md
* Phase details: .copilot-tracking/details/2026-10-18/issue-172-chat-fixture-isolation-phase-details.md
* Critique execution status: Complete
* Assessment: One independent final-candidate critique; original verdict below.

## Inputs and Criterion Boundary

* Read the locked plan, phase details and supplied research at .copilot-tracking/research/2026-10-18/issue-172-chat-fixture-isolation-research.md.
* Assessed the caller's bounded fixture requirements against src/agents/tests/chat_fixture.py, src/agents/tests/test_chat_fixture.py, src/agents/tests/test_chat_provenance.py and src/api/tests/test_chat_fixture_roles.py.
* Checked component validation and existing exclusions against src/agents/README.md, src/agents/pyproject.toml and .github/workflows/src-ci.yml.
* Checked public documentation coupling against the chat fixture section of docs/reference/research/retrofit-synthetic-data/data-dictionary.md and SN-08 in docs/reference/research/retrofit-synthetic-data/needs-inventory.json.
* Read project framing and repository context in docs/case_study_48_original.md, docs/case_study_48_addendum.md, docs/reference/README.md and docs/reference/memory.md. Memory supplies preferences, not evidence.
* The decision boundary is implementation-plan credibility for the existing public synthetic helper/tests and directly related documentation. It does not establish implementation success, runtime authorization, approved retention, approved SN-08 scope/volume or whole-issue acceptance.
* Caller-supplied dependency facts govern: #158 is closed; ADR 0004 was accepted as written October 15 and merged in #279; OD-45 to OD-49 remain open; #167 establishes hierarchy only. No external dependency research was repeated.
* The existing untracked planning inputs on test/chat-fixture-isolation-172 were read without alteration. Only this critique artifact is written.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| Research C1-C3; disproved baseline failure | Covered | Research records 11 passing focused tests. Existing test_chat_fixture.py combines thread and memory owners when counting eleven perspectives. The candidate explicitly preserves this contrary evidence rather than claiming a failing baseline. |
| 22 personas, eleven perspectives, unchanged role/task mappings | Covered | The plan preserves personas and eligibility. P01-T01 derives thread-owner expectations from persona eligible_tasks, while separate memory/combined coverage retains eleven perspectives. Existing role-map regression remains selected. |
| Resource-specific eligible-owner coverage; P01-T01 | Covered | Details require equality of eligible user keys with thread owners and same-role thread probe owners, plus per-owner read/list/search, actor/owner roles, ownership and deny checks. This addresses resource mixing without incorrectly granting chat to ineligible staff or contractors. |
| Both-contractor explicit denial matrix; P01-T01/P01-T02 | Covered | Required contractor_access_denied kind covers each contractor and all three actions. Shared assertions check contractor identity, distinct actor/owner, eligible owner/task, actual resource ownership and active target. Incidental cross-role read coverage is correctly deemed insufficient. |
| Legitimate deterministic target; P01-T02 | Covered | Existing generated threads supply the target. Selection requires active state, non-contractor owner and task eligibility; deterministic traversal reuses the target without changing RNG, ownership or mappings. Missing legitimate target raises ValueError and has a direct test. |
| Mutation-sensitive coverage; P01-T01 | Covered | The same assertion must reject modified copies missing each required contractor action and copies with self-pairing or invalid/mismatched resource targets. Combined with the explicit both-actor matrix requirement, the deletion checks must cover each required actor/action entry, not merely global action presence. |
| Failing-first evidence; P01-T01 before P01-T02 | Covered | Tests precede generator changes and record the newly exposed denial gap. The candidate does not conflate this intentional new-test failure with the already passing 11-test baseline. |
| Lifecycle, null content, retained metadata and memory withdrawal | Covered | Existing lifecycle, expiry, ledger-null, opt-in/withdrawal and deletion expectations are retained. P01-T02 leaves content generators and lifecycle unchanged; P02 reruns existing tests. No new policy or runtime behavior is proposed. |
| Determinism and nine-payload privacy canaries; Research C4/P02-T01 | Covered | Acceptance requires identical manifest/all payload bytes for equal seeds and different data for another seed. Existing provenance test independently mutates labels and email patterns in every payload after rehashing, avoiding a hash-mismatch-only oracle. Candidate preserves and reruns it. |
| Source/output provenance; Research C5/P02-T01 | Covered | Plan requires fresh disposable generation and existing write() hashing, not tracked generated output or unrelated frozen snapshot refresh. Research supplies the no-chat-source-digest conclusion; no metadata change is proposed that would itself require another source hash. |
| Documentation and bounded claims; P02-T01 | Covered | Dictionary, component README, KB index and append-only log are named. Seven eligible thread perspectives remain distinct from eleven represented persona perspectives. SN-08 stays partial and scope/volume remains unapproved. |
| Validation scope and tooling; P02-T01 | Covered | Focused fixture/provenance/role tests, agents discovery, existing Ruff/format/mypy and relevant public provenance/scenario/inventory/evaluation tests are selected. Existing migration exclusions are disclosed, not presented as strict checking of the excluded helper/tests. Rename regression is conditional on actual path/metadata coupling. |
| Privacy and change boundaries | Covered | No private data, support reads, runtime/UI/mvp changes, live cloud/model/browser operations, new dependencies or payload families are authorized. Fixture declarations are explicitly not runtime enforcement evidence. |
| Dependencies and unresolved decisions | Covered | Candidate carries the supplied accepted ADR status, open OD-45 to OD-49 and hierarchy-only #167. It does not use unrelated approval gaps to block the bounded fixture correction or pretend those gaps are resolved. |
| Actual ordered execution and persistent evidence; P01-P03 | Covered | Ordered phases require actual checks, changes evidence, one original independent Review and dated artifacts committed with the change in the same PR on acceptance. These are future execution obligations, not claimed completed results. |
| Original adverse Review and publication gate; P03-T01 | Covered | Details preserve the original adverse verdict, block publication, commit frozen local evidence and route to the coordinator for at most two corrections. No self-certification or repeat Review is authorized. Accepted publication retains Refs #172 without issue closure or acceptance-criteria edits. |

## Verdict

* Verdict: Pass
* Rationale: The candidate is credible and proportionate for the bounded public fixture correction. It addresses the actual missing both-contractor read/list/search expectations and resource-specific eligible-owner coverage, preserves the disproved failure claim as contrary evidence, and specifies meaningful target validation and mutation-sensitive tests. Implementation, local verification and original independent Review remain mandatory; this planning verdict does not substitute for any of them.
* Severity counts: Critical 0; High 0; Medium 0; Low 0.

## Findings

No actionable PC-xxx findings were identified within the supplied criterion boundary. The complete actionable finding set is empty. No direct planner correction or significant/divergent user decision is required by this critique.

The shared assertion, per-contractor action-removal mutations, active eligible-owner target and all-payload byte determinism are explicit candidate obligations. They are not additional scope or findings; the original implementation Review must inspect their actual execution rather than treating plan language as evidence of completion.

## Strengths and Residual Risk

* The correction is grounded in what the helper actually generates: thread owners require eligible tasks, whereas memory probes can represent perspectives without thread eligibility.
* Both contractor actors receive deliberate coverage, rather than relying on one incidental read case. A real active target avoids a denial that could be explained solely by expired or deleted content.
* Negative controls share the production-fixture coverage assertion, so removal sensitivity is directly tested rather than claimed from passing happy-path assertions.
* Existing lifecycle and independently rehashed privacy canaries remain in scope without requiring new payloads or private snapshots.
* Accepted scope limitations remain explicit: these are declarative fixture expectations, not tested runtime enforcement; retention and SN-08 scope/volume are unapproved; open decisions are not silently closed.
* Existing format/type migration exclusions reduce the assurance supplied by green tool exits for the affected helper/tests. The candidate explicitly requires disclosure and relies on semantic tests plus independent Review, rather than claiming newly strict coverage.
* The no-valid-target branch deliberately fails explicitly. This is an appropriate diagnostic for the selected contract, not permission to fabricate an eligible owner or silently omit denials.

## Questions or Blocking Evidence Gaps

None for this bounded planning decision. Outstanding policy, scope/volume and runtime evidence remains outside this change and is already recorded as unresolved.

## Limitations

* No implementation exists in this candidate for the new denial kind or assertions; execution results must be recorded during Implement.
* The 11-test baseline and observed seven eligible thread perspectives are supplied research evidence, supported by reading the helper/tests; tests and generation were not rerun during this read-only critique. No scratch files, test outputs or caches were created.
* GitHub acceptance/dependency status and absence of a tracked chat source digest are assessed from caller-supplied facts and the supplied research, not a new remote or repository-wide audit.
* The initial conventional .github/workflows/ci.yml lookup was unavailable; the actual .github/workflows/src-ci.yml was located and read. Component validation assessment is therefore based on the real workflow and pyproject configuration, not the missing conventional path.
* No private dataset, private name source, support file, runtime serving data, live service, model or browser was accessed. No nested agent, second critique, commit or source change was made.

## Recommended Next Action

* Highest-impact finding: None.
* Action owner: Planning parent.
* Smallest next action: Record this original Pass disposition, finalize the locked plan and begin P01-T01 with the required failing-first evidence.
* User response required: No.
* Preserve this critique and the eventual original independent Review; route any later adverse Review through the coordinator's maximum-two correction process, not another critique or self-awarded acceptance.

## Artifacts

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-18/issue-172-chat-fixture-isolation-plan.md](.copilot-tracking/plans/2026-10-18/issue-172-chat-fixture-isolation-plan.md) | Locked plan assessed |
| [.copilot-tracking/details/2026-10-18/issue-172-chat-fixture-isolation-phase-details.md](.copilot-tracking/details/2026-10-18/issue-172-chat-fixture-isolation-phase-details.md) | Execution details assessed |
| [.copilot-tracking/research/2026-10-18/issue-172-chat-fixture-isolation-research.md](.copilot-tracking/research/2026-10-18/issue-172-chat-fixture-isolation-research.md) | Supplied baseline and bounded evidence |
| [.copilot-tracking/reviews/plans/2026-10-18/issue-172-chat-fixture-isolation-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-18/issue-172-chat-fixture-isolation-plan-critique.md) | Complete original critique |

## Next Steps

Return Complete / Pass to the active planning parent. The parent records disposition and advances to actual Implement and the single original independent Review under the existing gates. No user action or second critique is required.

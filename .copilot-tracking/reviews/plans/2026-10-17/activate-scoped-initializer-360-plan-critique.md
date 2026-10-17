<!-- markdownlint-disable-file -->
# RPI Plan Critique: Activate scoped initializer #360

## Metadata

* Task ID: 360
* Task slug: activate-scoped-initializer-360
* Critique date: 2026-10-17
* Plan: .copilot-tracking/plans/2026-10-17/activate-scoped-initializer-360-plan.md
* Phase details: .copilot-tracking/details/2026-10-17/activate-scoped-initializer-360-phase-details.md
* Research: .copilot-tracking/research/2026-10-17/activate-scoped-initializer-360-research.md
* Critique execution status: Complete
* Assessment count: Exactly one final-candidate critique.

## Inputs and Criterion Boundary

* Caller direction: FULL ordered RPI; boolean true approves only reviewed API read/restart and temporary staff-job lifecycle permissions in ama. Existing-job result-tag grants are not implicitly approved. No runtime restarts, job execution, Graph, SQL, vault-secret reads, browser acceptance, broader roles, network changes, spend or deletion.
* Candidate decision: preserve merged defaults and add includeResultRelay bool default true; condition both relay authorization resources; deploy only the API slice with false after tests and independent source review.
* Supplied evidence assessed: research C1-C4/W1-W4 and its explicit limitations; infra/staff-initializer-rbac.bicep; infra/modules/staff-initializer-guard.bicep; infra/tests/test_identity_rbac.py:94-121; existing compile_bicep, resources and evaluate helpers in infra/tests/test_bicep_policy.py; infra/README.md:1632-1705,1790-1845; .copilot-tracking/reviews/logs/2026-10-17/demo-setup-readiness-360-review.md:140-185.
* Repository context consulted: docs/case_study_48_original.md, relevant opening framing in docs/case_study_48_addendum.md, task-routing entries in docs/reference/README.md, docs/reference/memory.md and the opening sector primer. Memory was treated as context, not evidence.
* Dependencies assessed: research and critique disposition before P01; successful focused validation and fresh independent source review before P02; exact preview and unchanged source/inputs before apply; actual live outcome or concrete blocker before P03; one independent full-task RPI Review before publication handoff.
* Acceptance assessed: default four/subset two active authorization resources; exact actions/scopes/principal; no relay grant; demo API rather than old API; genuine sanitized results; ordered durable evidence and main PR; #360 d/e remain UNMET.
* Boundary: plan credibility and executable safety gates, not implementation correctness, current Azure state, effective identity permissions, live acceptance or approval of any excluded operation. No external research, live operations, tests or source mutations were performed.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| Owner approval; research C1/C2/W3/W4 | Covered | Separates management capability from consent and temporary operator lifecycle from existing-job tag permissions. API subset does not depend on relay approval. |
| Target identity/API; research W1/W2 | Covered | P02-T01 fixes demo API, existing initializer identity, expected principal and deterministic authorization IDs; no old-API assignment or runtime action. |
| P01-T01; default compatibility | Covered | Default true, both relay resources conditional, API resources unconditional, GUID/action/scope preservation and no new role design. |
| P01-T01; semantic and regression tests | Covered | Existing matrix and compiled helpers reused; true/false/default active-resource evaluation, exact properties and missing-condition mutation. Maximum three additions; no removals. |
| P01-T02; validation and source review | Covered | Required Bicep build/lint and focused tests; independent complete-diff source review is a hard prerequisite, separate from the later RPI Review. |
| P02-T01; preview authority | Covered | Incremental ama-only operation with false; exact two authorization resources, Creates or exact already-correct NoChange, only same-root Ignore rows and no Modify/Delete or unexplained payload. Metadata-only guard is explicitly bounded. |
| P02-T01; principal resolution and evidence | Covered | Unresolved principal must match reviewed expression, then resolve through identity metadata before apply and actual assignment readback afterward. Source/input identity is retained through preview/apply. |
| P02-T01; readback and failure handling | Covered | Definition/actions, assignment/principal/scope, relay absence and unchanged demo metadata; genuine error metadata only, partial creations retained, no broadened retry or deletion rollback. |
| P03-T01; durable publication evidence | Covered | Existing runbook/evidence pack/index and append-only log updated factually; historical receipts retained; approval limitation, ordered phase evidence and remaining blockers explicit. |
| P03-T02; ordered independent review and PR | Covered | One independent full-task RPI Review, parent dispositions, privacy-safe local identity/trailer, topic push/main PR Refs #360, remote-head verification, no closing syntax, merge or force push. |
| Research alternatives and residual dependencies | Covered | Rejects full-template activation, new broad roles, hand-edited compiled deployment and manufactured denials; retains no-deployment fallback, private-publisher and human acceptance blockers. |

## Verdict

* Verdict: Pass
* Rationale: The supplied final candidate is credible for bounded implementation. It resolves the material authorization mismatch without changing reviewed role semantics or treating existing operator capability as approval. Tests and independent predeployment review precede the exact API-only activation; later independent RPI Review and factual publication remain distinct required steps.
* Severity counts: Critical 0; High 0; Medium 0; Low 0.
* This verdict is not evidence that the amendment exists, tests passed, source review completed, Azure accepted a deployment or #360 acceptance criteria d/e were met.

## Findings

No actionable PC-xxx findings were identified within the supplied boundary. No planner correction or significant/divergent user decision is required. Findings were not withheld for a later critique.

## Strengths and Residual Risk

* Authorization interpretation is conservative and consistent with current owner direction. Existing-job tags/read and tags/write remain excluded, even though the historical runbook proposed all four Creates. P03 explicitly requires factual reconciliation rather than reusing that historical approval wording.
* Source selection is auditable: both relay definition and assignment are omitted together, default behavior remains compatible, and generated JSON is not hand-filtered.
* Semantic assertions cover both relay resources, API resource independence and default/subset behavior. A source-only string check cannot substitute for the planned compiled evaluation and mutation evidence.
* The existing nested guard has only an approvedScope parameter and checked output. The candidate permits only metadata-only guard behavior, not an extra workload or permission write.
* The predeployment reviewer has no authority to enlarge owner approval. A source-review defect blocks deployment even if the historical merged template was reviewed.
* Exact already-correct NoChange is an idempotency path, not permission to accept a modified role or assignment. Unexpected changes, target mismatches and unresolved nonprincipal properties stop the live step.
* Grant readback does not prove effective token propagation or worker execution. The candidate explicitly retains that distinction and prohibits runtime tests here.
* Partial deployment may leave one authorized resource created. The plan requires truthful receipts and prohibits deletion rollback; it does not promise transactional ARM behavior.
* API-only activation cannot supply the private worker image, authorize relay, unblock tenant setup or prove staff/browser/SQL/AI acceptance. These are explicit follow-ups, not hidden completion claims.

## Questions or Blocking Evidence Gaps

* None for the planning verdict. Current owner direction already resolves the API-only selection; no additional approval is needed merely to begin P01.
* Future implementation evidence is deliberately absent: the amended compiled output, focused test results, independent source-review artifact, fresh subset what-if and live readback must be produced at their gates. Missing future evidence must not be replaced by this critique or the historical four-Create preview.
* Source reviewer owns the independent review conclusion; implementation parent owns test receipts, exact preview/apply/readback checks and publication; owner retains any separate relay approval and merge decision.

## Limitations

* W1-W4 were assessed as dated research claims, not independently reexecuted ARM observations. Their raw live responses were not supplied as separate files. Fresh preview and identity readback remain mandatory.
* Current source was read to assess feasibility; it has not yet received includeResultRelay and this critique does not serve as the mandatory independent review of that future diff.
* No tests, CLI compilation, GitHub publication or live Azure operation were run. No runtime, legal, accessibility or whole-repository acceptance conclusion is made.
* Initial branch was chore/activate-scoped-initializer-360 at e065ecd2c5b09b0f4bc22bfbfdb343e41910189b. Existing untracked plan/details/research/state artifacts were left untouched. The only intended write is this critique artifact.

## Recommended Next Action

* Highest-impact finding: None; no PC-xxx issued.
* Action owner: Active planning parent, then implementation parent.
* Smallest next action: Record this single critique's Pass disposition and finalize the candidate without another critique. Begin P01-T01, then obtain the independent source review before any P02 live step.
* Resolving/continuation evidence: Parent disposition records this artifact and Pass; subsequent changes evidence identifies the final source hash, focused validation, independent source review and exact authorized live outcome or blocker in lifecycle order.
* Decision route: Direct parent continuation under existing direction.
* User response required: No.

## Artifacts

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-17/activate-scoped-initializer-360-plan.md](.copilot-tracking/plans/2026-10-17/activate-scoped-initializer-360-plan.md) | Final candidate assessed; unchanged. |
| [.copilot-tracking/details/2026-10-17/activate-scoped-initializer-360-phase-details.md](.copilot-tracking/details/2026-10-17/activate-scoped-initializer-360-phase-details.md) | Detailed execution gates assessed; unchanged. |
| [.copilot-tracking/research/2026-10-17/activate-scoped-initializer-360-research.md](.copilot-tracking/research/2026-10-17/activate-scoped-initializer-360-research.md) | Supplied research and evidence claims; unchanged. |
| [.copilot-tracking/reviews/plans/2026-10-17/activate-scoped-initializer-360-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-17/activate-scoped-initializer-360-plan-critique.md) | This single complete final-candidate critique. |

## Next Steps

No user action is required. Return Complete / Pass to the active planning parent for finalization and continuation through the existing gates. This critique stops here; it does not invoke implementation, another critique or live operations.

---
title: Employee AI Deployment Independent RPI Review
description: One independent post-implementation review of the employee AI deployment boundary
ms.date: 2026-10-28
---

## Scope and Evidence

* Task ID: employee-ai-deployment-2026-10-28
* Review date: 2026-10-28
* Review scope: Completed implementation and bounded deployment; P03 publication remains upcoming.
* Assessed HEAD: d783b63acb0e2e59ad52f1c8f999e093c149297b
* Assessed origin/main: 98b0bb98f2424dd23c00e386378f44892a7a79e0
* SHA256 of `git diff origin/main -- infra`: 589cb6072ca2cb33211843f9b140e2f61f6c2505634982a985122b7adb4ccd89
* Boundary includes uncommitted infra changes, not merely HEAD. Subsequent evidence-only commits must not be presented as independently assessed source without matching these infra diff bytes.

## Opening Review State

* Interpreted review goal: Compare the completed employee model source, bounded deployment evidence and handover against owner intent, the canonical plan, details, research, original critique and changes record once.
* Review scope: All infra changes against origin/main, relevant bounded runtime/test context and task state; no inference or live application acceptance.
* Evidence readiness: Canonical artifact paths exist; substantive comparison and validation-evidence assessment pending.
* Acceptance basis: Exactly one small employee deployment on the existing ama account, optional missing API OpenAI User assignment only, reproducible source forwarding/pins, bounded test additions and explicit operator/publication gates.
* First comparison boundary: Plan markers and critique dispositions against changes, then full infra diff and runtime consumers.
* Active read-only boundaries: Only this review record may be written; no source/artifact corrections, Azure operations, secret/private data reads, nested agents, repeat Review or closure verification.
* Initial blockers: None identified before evidence comparison. Publication and human approval are not presumed complete.

## Execution Status

* Execution status: Complete.
* Exactly one independent Review performed. All supplied canonical artifacts, state and the complete `git diff origin/main -- infra` were read. Bounded runtime consumers, source module context and compiled-policy helpers were examined directly; no nested agents, fixes or closure verification.
* Implementation execution: P01/P01-T01/P01-T02 and P02/P02-T01 complete on the recorded evidence. P03/P03-T01 and AC6 remain incomplete by design: this Review precedes evidence commit, scoped gate, push and PR.
* State correctly identifies active Review with no review pointer yet; Changes' pending-Review wording is its pre-Review snapshot. Neither is silently updated here.
* Current origin/main has advanced from implementation's initial d783b63a to 98b0bb98 (#514). Its infra content is identical to HEAD (`git diff origin/main..HEAD -- infra` is empty). The assessed infra patch and fingerprint therefore remain unambiguous. This does not certify publication ancestry, a deployed #514 image or completion of coordinator work.

## Scope and Evidence Inventory

* Plan: .copilot-tracking/plans/2026-10-28/employee-ai-deployment-plan.md
* Phase details: .copilot-tracking/details/2026-10-28/employee-ai-deployment-phase-details.md
* Research: .copilot-tracking/research/2026-10-28/employee-ai-deployment-research.md
* Original critique: .copilot-tracking/reviews/plans/2026-10-28/employee-ai-deployment-plan-critique.md
* Changes: .copilot-tracking/changes/2026-10-28/employee-ai-deployment-changes.md
* State: .copilot-tracking/rpi-sessions/2026-10-28/employee-ai-deployment-state.json
* Complete source boundary: infra/README.md, infra/main.bicep, infra/modules/containerapps.bicep, infra/modules/foundry.bicep, infra/tests/test_bicep_policy.py; 302 insertions and 17 deletions across five files.
* Bounded runtime evidence: src/core/src/zava_forward/core/ai.py and src/api/README.md. Required project context: docs/case_study_48_original.md, opening sections of docs/case_study_48_addendum.md and docs/reference/README.md, and docs/reference/memory.md.
* Azure results and complete historical validation are assessed as supplied command/result evidence in Changes and the current request, not independently repeated cloud observations or freshly opened external logs. No secrets, .env, private datasets or forbidden filesystem locations were read.

## Plan-to-Change Reconciliation

| Current plan scope | Changes-record summary | Current-state reconciliation | Gap or rationale |
| --- | --- | --- | --- |
| P01-T01, AC1/AC2 | Scalar defaults, nonempty array, derived outputs and conditional API env | Reconciled | Exact accepted nano default and override semantics agree across source, plan, details and handover. |
| P01-T02, AC5 | Four compiled semantic methods; full discovery/build/lint/type evidence | Reconciled | No tests removed; within six-method ceiling. Independent four-method execution also passed. |
| P02-T01, AC3/AC4 | Rejected original model; one successful fallback child and one missing account role; unchanged app | Reconciled | Commands/readbacks preserve child, capacity, role, identity, private/keyless and no-inference boundaries. |
| P03-T01, AC5/AC6 | Review-ready; commit/gate/push/PR upcoming | Reconciled, intentionally open | No completed publication claim; current Review satisfies only its own stage. |
| Follow-Up Items | Coordinator activation and owner lifecycle/quality/cost review | Reconciled | Distinct operator work; not silently part of source completion or present live acceptance. |

## Completed Work Assessment

| Related marker | Files | What changed and why | Completion evidence | Validation | Assessment |
| --- | --- | --- | --- | --- | --- |
| P01-T01 | infra/main.bicep; infra/modules/foundry.bicep | One standard nano default; scalar model/version/SKU/capacity; retained explicit array | Full diff and compiled model-loop assertions | Independently passed focused tests | Positive scalar capacity and nonempty arrays enforced; dated version, NoAutoUpgrade and Microsoft.DefaultV2 preserved. |
| P01-T01 | infra/modules/foundry.bicep; infra/main.bicep; infra/modules/containerapps.bicep | Separate OpenAI endpoint and positional tier names/version identities forwarded end-to-end | Account-advertised OpenAI property is distinct from unchanged generic endpoint | Compiled single/two-entry and scalar-override assertions passed | API receives exactly five AI_* settings only when enabled; selected AZURE_CLIENT_ID and other app behavior preserved. |
| P01-T01 | infra/README.md | Replace invalid empty bootstrap; disclose new nonzero model provisioning and explicit evaluated-array preservation | Command and adjacent warning agree with constraints | Diff/link-text review | Future stack deployment is intentionally broader than this child-only operation; not authorized here. |
| P01-T02 | infra/tests/test_bicep_policy.py | Four methods plus reusable assertion helper in existing owner/class | AST comparison confirms four additions, zero removals | Four methods passed independently, including mutations | Actual compiled values/resource loop/module bindings checked, not source-token-only assurance. |
| P02-T01 | Changes deployment/role/readback sections | Minimal provider-accepted model and exact missing invocation assignment | One standard Succeeded, nano/2025-04-14/GlobalStandard/1; exact UUID/principal/role/account | Supplied Azure readback; independent local UUID calculation | No second child, throughput increase, Foundry User assignment, full-stack operation, app update or inference evidenced. |

The runtime reads the same endpoint, names and response-model pins. Its chat API uses 2024-10-21 with max_tokens and temperature; a non-reasoning GPT-4.1 chat-family selection is structurally compatible with that request shape. The runtime compares the provider response `model` to the supplied full identity and falls back on mismatch/network failure. Both routes sharing `standard` also share the same identity, so the strong-route comparison remains consistent. This is structural compatibility, not observed provider-response identity, task quality, private reachability or release acceptance.

Future redeployment keeps the model's existing resource name, version and policies. Explicit multi-model arrays still flow into the real model loop and first/second bindings; a single entry backs both tiers. The live role UUID matches the exact Bicep account/principal/openai-user seed, avoiding a differently named duplicate assignment. Existing source can also create the pre-existing agent/API Foundry roles in a full stack; that is unchanged source behavior, not authority to add them during this task.

## Implementation-Time Plan and Detail Update Assessment

| Affected area | What changed and why | Triggering evidence and decision | Reconciliation | Planning and critique state | Assessment |
| --- | --- | --- | --- | --- | --- |
| P01/P02 default and handover | gpt-4o-mini replaced by gpt-4.1-nano/2025-04-14 | ServiceModelDeprecating rejected original PUT; list remained empty; existing authority permits compatible capacity-one fallback | Source default, compiled assertion, README, plan/details, Changes and exact settings match successful child | PC-004 disposition anticipated this branch; no new resource/capacity authority or significant unaccepted decision | Justified in-scope divergence; original research/rejection/critique preserved. |
| P01 bootstrap | Remove empty-array example and warn about model provisioning | Nonempty-array contract; PC-005 | Current command and nearby cost/override prose agree | Applied before implementation | No hidden zero-model compatibility claim. |
| P02 role identity | Add algorithm, known answer and name readback | PC-003; future ARM redeployment identity | Exact inputs and 207df5ea-ca56-5fb7-9ebb-f533d02dadb8 recorded | Bounded local check, not a new production helper | Independently reproduced UUID and RFC known answer. |
| P03 publication | Conditional partial receipt verification, fresh base, one attempt and invalidation disclosure | PC-002 and explicit owner gate exception | Plan/details/Changes retain unperformed state | No gate attempted by this reviewer | Parent-owned continuation, not a completed or full-tier gate. |

## Critique and Material Revision Assessment

* Original critique remains Complete / Revise, with 2 High and 3 Medium findings. Its original findings are not rewritten as a retrospective pass.
* PC-001 was explicitly rejected because the worker-local /tmp prohibition was not a parent restriction. The current request confirms that disposition. This reviewer does have its own filesystem restriction and neither opens that brief nor executes the gate; it does not transfer that constraint to the parent or reinstate the unsupported finding.
* PC-002, PC-003, PC-004 and PC-005 each have a direct recorded disposition and corresponding plan/detail/source/evidence changes as assessed above. No second critique is required or represented.
* The fallback is an expressly planned, bounded response to provider rejection, not an unaccepted architecture change. The original deprecated-model research remains historical evidence and is explicitly reconciled by the later current plan and Changes.
* Dependent-work pause: rejected PUT left no model and prevented the role write; only the compatible one-child fallback and authorized missing role proceeded. Final fallback reconciliation and validation preceded this Review. No source or live-operation decision gap requiring rpi-plan was identified.

## Plan Follow-Up Assessment

| Follow-up item | Why outside immediate scope | Owner or next action | Assessment and route |
| --- | --- | --- | --- |
| Employee app configuration/redeploy and source=ai acceptance | Live app writes and inference expressly excluded; image/release/private access require separate authorization/evidence | Coordinator, after confirming #514 integration and approved deployed candidate | Open; RV-001, distinct operator activation work. |
| Model retirement, quality and cost review | Short exercise resource creation is not permanent model selection, evaluated capable-tier quality or hard budget enforcement | Owner; reassess availability/quality and authorization before later deployment/use | Open; RV-002, distinct lifecycle/cost work. |

## Findings

No high-confidence implementation defect, unaccepted decision gap or material evidence gap within completed P01/P02 scope was found. The complete original finding set consists of these non-blocking residual items; they are not source defects.

<!-- rpi:review id=RV-001 -->
### RV-001 [Medium]: Resource prerequisites do not activate or accept employee AI

* Related scope: Plan Follow-Up Items; AC4; P02/P03 handover.
* Evidence: Changes' Exact Coordinator Settings and readbacks; infra/README.md small employee model section; src/core/src/zava_forward/core/ai.py. App remains revision 0000006 with no AI_* settings; no inference was performed.
* Impact: Resource existence and structurally correct bindings do not prove actual response-model identity, private access, registered release/evaluation, governed budget/incident behavior or an accepted employee source=ai result.
* Owner: Coordinator, with designated human approver for activation/acceptance.
* Destination: Distinct employee-app activation follow-up, not rpi-implement for this source task.
* Smallest useful next action: Confirm #514 integration and approved runtime candidate, then separately authorize/configure/redeploy with the exact settings while preserving auth/data/identity; verify private connectivity, registered release/model/evaluation and spending/incident controls, then obtain bounded human-witnessed source=ai acceptance. Keep manual and human/resident decisions intact.

<!-- rpi:review id=RV-002 -->
### RV-002 [Low]: Short exercise authorization is neither long-term model suitability nor a hard spend cap

* Related scope: Plan Follow-Up Items; capacity-one fallback; handover cost boundary.
* Evidence: Current plan and Changes record nano as Legacy, inference retirement 2027-04-14 and USD30 additional employee AI authorization through 2026-10-31. README explicitly distinguishes throughput from money/expiry and disclaims stronger-tier evaluation.
* Impact: A successful capacity-one allocation does not constrain dollars, automatically expire, establish later availability or demonstrate quality for both logical tiers.
* Owner: Owner/budget holder and model-evaluation operator.
* Destination: Distinct exercise cost/model lifecycle follow-up, not an implementation defect.
* Smallest useful next action: Before any authorized inference or continuation beyond October 31, confirm spending controls/authority and evaluated task-model bindings; recheck provider availability before later deployment and plan retirement/replacement before the recorded date.

## Defects

* None identified within the assessed completed implementation boundary.
* No fixes, source corrections, closure verification or repeat Review performed.

## Routed Findings

| Finding | Destination | Owner or next action | Reason |
| --- | --- | --- | --- |
| RV-001 Medium | Distinct employee-app activation follow-up | Coordinator and human approver | Explicitly deferred live deployment/release/private reachability/inference acceptance. |
| RV-002 Low | Distinct exercise cost/model lifecycle follow-up | Owner/budget holder and evaluation operator | Explicitly deferred cost authorization, availability and quality/lifecycle decisions. |

Later implementation of a routed finding does not require another Review of this task.

## Residual Work

* RV-001 and RV-002 retain the plan's distinct follow-up owners; neither is added to active implementation or current acceptance.
* Human approval remains unchecked. This record supplies independent review evidence, not owner approval, hosted approval, issue closure or operational acceptance.

## Blockers and Remaining Work

* Review blockers: None.
* P03-T01 remains open: parent records this original Review, commits implementation and original dated evidence, attempts at most one owner-authorized scoped `--changed` gate with native `--lock-timeout 0`, and publishes the requested Refs-only PR with actual evidence.
* Full `--all` is explicitly forbidden for this task. No complete repository-default gate or valid receipt is claimed here.
* Parent must freshly fetch main; conditionally verify a successful scoped receipt with `--required-scope partial` against that base immediately before push, and disclose skip/failure/missing prerequisite or later head/base invalidation without a second attempt.
* Later evidence-only commits must identify their publication head separately from this assessed source boundary. Any source change is outside this Review's fingerprint; no repeated assessment or acceptance is implied.
* Current origin/main already contains #514, unlike its earlier open-PR snapshot in implementation evidence. The coordinator must verify the actual intended runtime candidate and remaining live gates; merged source does not establish a deployed revision.

## Validation Evidence

| Command or evidence | Scope | Status | Summary |
| --- | --- | --- | --- |
| `PYTHONDONTWRITEBYTECODE=1 REQUIRE_AZ_BICEP=1 python3 -m unittest discover -s infra/tests -p test_bicep_policy.py -k employee -q` | Four new compiled-policy methods | Passed, independently executed | 4 tests / 6.334s / OK; no skips. Compiles main and guard and checks resource/env propagation plus mutations. |
| AST comparison against `git show origin/main:infra/tests/test_bicep_policy.py` | Locked test budget | Passed, independently executed | Exactly four added test methods, none removed; existing class retained. |
| Python uuid5 DNS known answer and ARM namespace/seed calculation | Role-name redeployment compatibility | Passed, independently executed | RFC expected UUID matches; exact account/principal/openai-user yields recorded assignment UUID. |
| `git diff --check origin/main -- infra` | Complete infra patch | Passed, independently executed | No whitespace errors. |
| HEAD/base/diff SHA256 and `git diff origin/main..HEAD -- infra` | Assessed source identity | Passed, independently executed | Repeated read-only fingerprint unchanged; base advancement has no infra delta. |
| `az bicep build`; all templates and three build-params | P01 source compilation | Passed, supplied implementation evidence | All compiled earlier; final main rebuilt after nano reconciliation. Not independently rerun as an all-target build. |
| `REQUIRE_AZ_BICEP=1 .../python -m unittest discover -s infra/tests -q` | Full infra discovery | Passed, supplied final implementation evidence | Final 466 tests / 111.776s / OK, no skips. Earlier 466 / 116.326s and initial failures remain separately preserved. External logs not opened by this reviewer. |
| Changed-file Ruff check/format and mypy | Python policy file | Passed, supplied implementation evidence | Final passes recorded after callback-context annotation fix; not independently rerun. |
| Exact model/role/app/account readbacks in Changes | Authorized live child and role boundary | Passed, supplied operational evidence | One Succeeded model, one exact role, unchanged revision/identity/AI absence, private/keyless account. No fresh cloud reads or writes by reviewer. |
| Live inference, private runtime reachability, governed release/evaluation and human acceptance | Operator activation | Not run, intentionally excluded | RV-001; resource creation is not application acceptance. |
| Scoped gate, receipt verification, push/PR and hosted checks | P03 publication | Not run, upcoming | Parent-owned; no full-tier or publication-success claim. |

## Outcome

* Outcome: Conformant with justified divergence.
* Rationale: Completed P01/P02 meet the bounded source/deployment criteria on inspected source, independently passed focused tests and supplied operational evidence. The explicitly planned capacity-one nano fallback is justified by provider rejection and reconciled across source, tests, current plan/details and handover. No high-confidence implementation defect was identified. P03 publication remains incomplete, and RV-001/RV-002 preserve distinct non-blocking operator work.
* Severity summary: 0 Critical, 0 High, 1 Medium residual, 1 Low residual; 0 implementation defects.
* Human approval: [ ] Not requested, granted or inferred by this Review.

## Closeout Routing Record

| Finding class | Destination | Owner or next action |
| --- | --- | --- |
| Implementation defect | None | No rpi-implement correction identified. |
| Decision gap or invalid assumption | None | No rpi-plan revision needed for the planned fallback or recorded critique dispositions. |
| Material evidence gap | None within completed scope | No rpi-research handoff; excluded live acceptance remains RV-001. |
| Non-blocking residual work | RV-001 activation; RV-002 lifecycle/cost | Coordinator/human approver; owner/budget holder/evaluation operator. |

* Execution status: Complete for this one independent Review; P03 publication remains open.
* Outcome: Conformant with justified divergence.
* Validation coverage: Independent four-test compiled-policy pass, AST/UUID/fingerprint/diff checks; supplied full infra/build/lint/type and bounded live-readback evidence, with limitations explicit.
* Blockers: None to close this Review; no publication, hosted or human acceptance granted.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-28/employee-ai-deployment-plan.md](.copilot-tracking/plans/2026-10-28/employee-ai-deployment-plan.md) | Canonical scope, markers and follow-ups. |
| [.copilot-tracking/details/2026-10-28/employee-ai-deployment-phase-details.md](.copilot-tracking/details/2026-10-28/employee-ai-deployment-phase-details.md) | Reconciled phase details. |
| [.copilot-tracking/research/2026-10-28/employee-ai-deployment-research.md](.copilot-tracking/research/2026-10-28/employee-ai-deployment-research.md) | Historical candidate and bounded evidence. |
| [.copilot-tracking/reviews/plans/2026-10-28/employee-ai-deployment-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-28/employee-ai-deployment-plan-critique.md) | Original Complete / Revise critique. |
| [.copilot-tracking/changes/2026-10-28/employee-ai-deployment-changes.md](.copilot-tracking/changes/2026-10-28/employee-ai-deployment-changes.md) | Original operations, failures, validation and handover. |
| [.copilot-tracking/rpi-sessions/2026-10-28/employee-ai-deployment-state.json](.copilot-tracking/rpi-sessions/2026-10-28/employee-ai-deployment-state.json) | Pre-Review parent state. |
| [.copilot-tracking/reviews/logs/2026-10-28/employee-ai-deployment-review.md](.copilot-tracking/reviews/logs/2026-10-28/employee-ai-deployment-review.md) | This single independent Review. |

## Next Steps

Active parent continues the existing P03 publication sequence with this original record and exact assessed-source fingerprint; disclose actual gate/publication state and retain unchecked human approval. Coordinator and owner retain RV-001/RV-002 as separate follow-up work. Do not repeat this Review. No user action is required for review closeout.

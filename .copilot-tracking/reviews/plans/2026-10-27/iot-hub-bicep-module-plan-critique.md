<!-- markdownlint-disable-file -->
# RPI Plan Critique: IoT Hub Bicep module

## Metadata

* Task ID: issue-140
* Task slug: iot-hub-bicep-module
* Critique date: 2026-10-27
* Plan: .copilot-tracking/plans/2026-10-27/iot-hub-bicep-module-plan.md
* Phase details: .copilot-tracking/details/2026-10-27/iot-hub-bicep-module-phase-details.md
* Critique execution status: Complete
* Assessment: Exactly one independent final-candidate critique; no implementation or repeated critique.

## Inputs and Criterion Boundary

* Caller requirements: Complete ordered RPI loop under the existing parent; author and locally validate only; B1/Free IoT envelope, uksouth, resource group ama, USD700 aggregate cap; never delete ama. No deployment, what-if, secrets, uv, full gate, source edits, commits or cloud operations during this critique. Later parent publication authorization does not authorize publication by this critic.
* Primary inputs: .copilot-tracking/plans/2026-10-27/iot-hub-bicep-module-plan.md; .copilot-tracking/details/2026-10-27/iot-hub-bicep-module-phase-details.md; .copilot-tracking/research/2026-10-27/iot-hub-bicep-module-research.md.
* Existing implementation evidence: infra/modules/iothub.bicep; infra/main.bicep; infra/modules/guard.bicep; infra/modules/privateEndpoint.bicep; infra/modules/monitoring.bicep; infra/role-assignments.json; infra/tests/test_iothub_module.py; infra/tests/test_identity_rbac.py; infra/tests/test_edge_module.py; relevant guard, network, endpoint and mutation assertions in infra/tests/test_bicep_policy.py; relevant infra/README.md sections.
* Context: docs/case_study_48_original.md; relevant docs/case_study_48_addendum.md and docs/reference/README.md sections; docs/reference/memory.md as context only; IoT provisions in docs/adrs/0003-journey-derived-capabilities-runtime-fit.md and OD-43 in docs/brds/agentic-retrofit-programme-brd.md.
* Decisions and dependencies: Accept the supplied research's W1 keyless-consumption correction, W2 system-identity sequencing and W9 private-network trusted-service support. Accept the planning parent's explicit bootstrap/activation flag selection and its requirement to preserve true after activation. SDK work, device enrolment, live quota/headroom, transport, what-if and human operational approvals remain outside this authoring slice.
* Acceptance boundary: Assess requirements, research, phases, tasks, dependencies, six local acceptance targets, ownership, test/removal budget, risks and handoff once. Determine whether the implementation instructions and local proof obligations are sufficiently precise. Do not establish Azure execution, current subscription prices, operational approval or whole-issue completion.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| Owner scope, branch and preservation requirements | Covered | Existing feat/iot-hub-bicep-module branch; original candidate artifacts retained. No source or cloud mutation in this assessment. |
| W1; API least-privilege acceptance; P01-T01 | Covered | Dedicated Standard namespace and telemetry hub replace the unsupported built-in endpoint receiver claim; API receiver is scoped to the telemetry event hub. |
| W2; bootstrap/activation; P01-T01, P02-T01 | Partial | Two-apply sequencing is appropriate, but endpoint-registration absence in bootstrap is not an explicit test obligation. PC-002. |
| W3, W6, W9; production network acceptance | Covered | Separate unconditional endpoints/DNS, namespace public Disabled, default Deny and trusted-service exception; supplied evidence supports authoring, not runtime acceptance. |
| B1/one unit/uksouth/ama; P01-T01, P02-T01 | Partial | B1/unit parameter constraints are clear. A permitted module-local scope guard does not establish fail-closed protection for the integrated main graph. PC-001. |
| W5; diagnostics and service/device authentication | Covered | Metrics-only exports, explicit disabled allLogs, local service auth disabled, module SAS disabled and per-device authentication retained. |
| Cost/retention acceptance; P02-T02 | Covered | B1 and TU/ingress inputs are sourced; endpoint/DNS/diagnostic allowances must remain estimates. USD60 allocation is conditional on the final calculation; actual aggregate headroom blocks provisioning. |
| Device provisioning/credential owner; OD-43 | Covered | Exercise owner selection is distinguished from operational appointment; no actual device/credential operations; privacy and real-monitoring approval gates retained. |
| P02-T01; test ownership/removals/budget | Covered with PC-001/PC-002 corrections | Existing unittest owner and compiler/evaluator reused; four weak tests replaced; no unrelated removals; at most 20 IoT-specific plus six coupled additions. Both corrections fit these existing targets and limits. |
| P02-T02; ADR/runbook/reference evidence | Covered | Dated correction rather than historical rewrite; stale consumer/logging/tier claims reconciled, with reference index and append-only log updates. |
| P03-T01; build/lint/what-if acceptance | Covered | Local compiler/linter and required infra suite are explicit; live what-if/full gate excluded; existing hosted wiring retained without claiming it ran. |
| P03 handoff and publication | Covered | One later independent implementation Review; Refs #140 rather than closure; no authorization inferred for deployment or repeated assessment. |

## Verdict

* Verdict: Revise
* Severity counts: 0 Critical, 1 High, 1 Medium, 0 Low.
* Rationale: The supported keyless architecture and scoped local validation approach are credible. Tighten the integrated scope-guard boundary and the bootstrap endpoint-registration test contract before implementation. These are compatible planner corrections, not reasons to reopen the selected architecture or request additional user authority.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: A module-local guard alone cannot protect the integrated main resource graph

* Related IDs: Owner ama/uksouth constraints; plan Non-Functional Requirements; P01-T01; P02-T01.
* Evidence: .copilot-tracking/details/2026-10-27/iot-hub-bicep-module-phase-details.md, P01-T01, permits a small named guard with dependencies before all module resources. infra/main.bicep has an existing top-level parameter-guard and independently scheduled identity, network, monitoring and other resources; infra/modules/guard.bicep currently checks recorded evidence and nonempty locations, not ama/uksouth equality. infra/tests/test_bicep_policy.py, test_every_deployed_resource_waits_for_the_guard, establishes the existing top-level dependency boundary.
* Concern: The plan permits satisfying the new restriction solely inside iothub.bicep. Failure of that nested guard would block its descendants, but would not prevent independent main resources from changing in another resource group or primary region. A compiled unit test that checks only the nested guard's values could therefore pass without proving the integrated fail-closed constraint.
* Impact: A later separately authorized main deployment could partially mutate resources outside the owner's allowed target before failing at the IoT boundary. No such deployment is requested or performed here.
* Smallest useful change: Specify that the ama and primary uksouth checks run in the existing main parameter-guard before every resource-writing main branch. Retain a narrowly scoped equivalent in the standalone IoT module if standalone use must also be protected. Restrict this correction to the selected IoT/primary location boundary; do not silently constrain existing independently configured SQL placement or global service locations.
* Action owner: Planning parent, updating P01-T01 and P02-T01.
* Exact resolving evidence: Revised plan/details explicitly identify the top-level guard and dependency boundary. Required implementation tests evaluate actual compiled resource-group context and primary location for ama/uksouth, wrong RG, wrong region and both wrong; inspect the full main dependency graph; and reject mutations removing either named check or bypassing the guard. Standalone module coverage must not substitute for main coverage. Extend the existing evaluator only as necessary to supply resourceGroup() fixture context.
* Decision route: Direct planner correction. The owner already selected the permitted RG and primary region; no new user decision or Azure verification is needed.

<!-- rpi:critique id=PC-002 -->
### PC-002 [Medium]: Bootstrap must omit endpoint registration, not merely disable its route

* Related IDs: Research W2 and bootstrap disposition; plan routing-ready requirement; P01-T01; P02-T01.
* Evidence: .copilot-tracking/research/2026-10-27/iot-hub-bicep-module-research.md states sender-role propagation must precede custom endpoint registration. .copilot-tracking/details/2026-10-27/iot-hub-bicep-module-phase-details.md says false yields no active custom route and true configures the identityBased endpoint. The plan's semantic coverage lists route activation and identity shape, but does not expressly require bootstrap to contain no custom endpoint registration.
* Concern: The intended two-stage design is sound, but testing only route inactivity would accept an always-present identityBased endpoint with an inactive route. Endpoint validation, not just active message routing, is the sequencing hazard identified by W2. The true-state wording suggests the intended omission but leaves the decisive false-state assertion implicit.
* Impact: A structurally tested first apply could still attempt endpoint validation before its newly created hub principal has an effective sender role, defeating the reason for the bootstrap flag.
* Smallest useful change: Make the false-state resource contract explicit: keep the system-assigned hub identity, namespace, telemetry entity, consumer group, sender/receiver roles and private endpoints, but register no custom Event Hubs routing endpoint, enable no custom route and keep fallback disabled. True registers the system-identity endpoint and the all-DeviceMessages route only after the separately recorded propagation prerequisite. Do not add a hub dependency on its own downstream sender assignment, a deployment loop or automatic activation.
* Action owner: Planning parent, clarifying P01-T01 and P02-T01 within the locked test budget.
* Exact resolving evidence: Revised phase details and semantic-test obligations distinguish endpoint registration from route enablement. Required compiled false/true evaluations assert endpoint absence/presence, route absence or inactivity/presence, disabled fallback in both states, and persistent system identity/sender assignment. A mutation registering the endpoint during bootstrap must fail the same assertion even with its route disabled. Dependency checks must reject a hub-to-own-sender cycle; no local test may claim role propagation was observed.
* Decision route: Direct planner correction. Preserve the already selected default-off flag and later explicit activation process; no user response is required.

## Strengths and Residual Risk

* The plan corrects the ineffective receiver assignment rather than reproducing historical acceptance claims. IoT Hub remains the device-identity boundary; the extra Event Hub is an Entra consumer adapter, not an unauthorized replacement for IoT Hub.
* Dedicated namespace sender and entity-scoped receiver roles are distinct; role-matrix parsing must identify the system principal rather than attributing its assignment to the API. Existing broad-role and unrelated scope checks remain intact.
* Supplied W9 resolves the proposed public Disabled/trusted-service combination for authoring. Actual trusted-service behavior, private DNS resolution and transport remain untested, correctly deferred evidence.
* The accepted flag can disable an active route if omitted on a later apply. The plan explicitly selects this behavior and requires preserving true; do not replace it with an unrequested bootstrap orchestration or describe offline checks as protecting deployed state.
* No amount of ARM dependency testing proves role propagation. The later activation owner must record effective authorization and the separate write approval before activation; this critique does not request that work.
* USD10 B1 plus USD21.90 for 730 TU-hours is a sourced USD31.90 fixed-service subtotal, not a complete transport total. Ingress volume, two endpoint hourly/data charges, DNS and diagnostic allowances still belong in the required final calculation. Do not publish USD60 as a verified reservation without that calculation, treat billing-currency budget values as USD without reconciliation, or infer aggregate headroom from a component estimate.
* Budget resources are alerts, not hard spending controls. Actual billing currency, prices, remaining aggregate USD700 headroom and owner authorization stay provisioning blockers. Their deliberate deferral is not an authoring blocker.
* Metrics-only changes do not erase already ingested logs or historical identifiers. No cleanup or retention-policy change is authorized by this source correction.
* Later incremental deployment would not itself remove historical resources or old role assignments merely because they disappear from source. Any live reconciliation needs separately scoped authority; no deletion or migration procedure is requested here.
* Local constraints, diagnostics, PE/DNS, roles, routes and mutation checks provide authored-contract evidence only. They do not establish device enrolment, SDK consumption, live what-if, OD-43 approval or closure of #140.

## Questions or Blocking Evidence Gaps

* No decision-critical user question. Both findings are resolvable by the planning parent within the selected design and source/test scope.
* Public pricing placeholders and live quota/network/propagation/headroom remain explicit deferred gates. No new external research or subscription inspection is required to resolve this critique.

## Limitations

* Official-document findings were assessed from the supplied dated research, not independently re-fetched. This respects the prohibition on research beyond supplied inputs.
* No Bicep compilation, test execution, Azure call, what-if, subscription read, credential access, source edit, commit or push was performed. The candidate is a plan, not an implemented result.
* The supplied research summarizes the six issue criteria; this critique does not claim independent retrieval of the issue or review of every historical tracking record.
* Existing untracked plan, details, research and session-state inputs were left in place. Only this caller-designated critique artifact was written.

## Recommended Next Action

* Highest-impact finding: PC-001.
* Action owner: Planning parent.
* Smallest next action: Clarify the integrated main guard and bootstrap endpoint-absence obligations in plan/details, record disposition of both findings, then continue the already authorized implementation loop.
* User response required: No.
* Do not commission another plan critique. Preserve this original Revise verdict and resolve the findings through explicit planner disposition and later implementation evidence.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-27/iot-hub-bicep-module-plan.md](.copilot-tracking/plans/2026-10-27/iot-hub-bicep-module-plan.md) | Reviewed final-candidate plan |
| [.copilot-tracking/details/2026-10-27/iot-hub-bicep-module-phase-details.md](.copilot-tracking/details/2026-10-27/iot-hub-bicep-module-phase-details.md) | Reviewed implementation and validation obligations |
| [.copilot-tracking/research/2026-10-27/iot-hub-bicep-module-research.md](.copilot-tracking/research/2026-10-27/iot-hub-bicep-module-research.md) | Supplied dated research and selected decisions |
| [.copilot-tracking/reviews/plans/2026-10-27/iot-hub-bicep-module-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-27/iot-hub-bicep-module-plan-critique.md) | Complete independent critique; Revise |

## Next Steps

The active planning parent should apply the two compatible planner corrections and finalize without another critique, then continue the authorized RPI loop. No user action is required. This critic stops here; it does not implement, publish or invoke another stage.

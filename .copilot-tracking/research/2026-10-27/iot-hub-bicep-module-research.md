<!-- markdownlint-disable-file -->

# Task Research: iot-hub-bicep-module

| Field | Value |
| --- | --- |
| Date | 2026-10-27 |
| Researcher / agent | RPI Agent / rpi-research |
| Status | Complete |
| Artifact path | .copilot-tracking/research/2026-10-27/iot-hub-bicep-module-research.md |

## Research Brief

* Research target: issue #140, ADR 0003 and BRD OD-43; verify the existing infrastructure before choosing precise corrections.
* Purpose / audience: author-reviewable IoT Hub infrastructure and honest acceptance evidence for the owner.
* Scope: infra module, integration, policy/tests, budget and directly related documentation.
* Non-goals: deployment, what-if against Azure, resource deletion, consumer implementation, real devices/data, secrets, uv, full local gate.
* Criteria: all six issue criteria mapped to local evidence or explicit remaining gates.
* Requested outputs: dated Research, Plan, Implement and independent Review evidence, commit, branch push and PR.
* Output mode: convergence.

## Research Parameters

| Field | Value |
| --- | --- |
| Questions | What already exists, which tier/network/identity constraints apply, and what can be proven offline? |
| Codebase scope | infra/, related ADR/requirements/budget/workflows and original tracking evidence |
| External scope | Official Microsoft Learn schema, IoT tier/identity/network documentation and public pricing only as needed |
| Initial internal candidate areas | infra/modules/iothub.bicep, infra/tests/test_iothub_module.py, infra/main.bicep, infra/README.md |
| Initial external candidate areas | Microsoft.Devices/IotHubs schema, IoT Hub pricing and feature comparison |
| Research posture / provenance | focused / bounded explicit caller scope |
| Limits | Author and validate only; RG ama only; USD700 cap; never delete ama; no full gate |
| Completion basis | Material task questions covered with evidence; external/live gaps stated |
| Edits allowed | Research evidence and workflow state only |
| Resolved evidence root | .copilot-tracking/ |

## Extension Registry and Provenance

| Kind | Candidate | Provenance / authority | Disposition |
| --- | --- | --- | --- |
| Instructions | Repository guidance supplied in conversation | All paths; infra conventions, branch/privacy and evidence | Selected; user's explicit local-only/no-full-gate exception controls this task |
| Skill | rpi-research | Installed RPI contract | Selected |
| Specialist | hve-core-all:rpi-researcher | Registered independent research lanes | Skipped: a tightly coupled existing-module trace is best handled inline |
| Skill | Web/design/security assessment skills | No web surface or vulnerability assessment requested | Not applicable |

## User Participation and Research Decisions

* Owner explicitly requested the complete ordered RPI loop, commit, push and PR on feat/iot-hub-bicep-module. This is automatic execution authorization, not authorization for deployment or any subsequent child task.
* Owner supplied 2026-10-27 ADR approval and Free/B1 envelope. Existing ADR records older Basic acceptance and unresolved infrastructure details; reconcile dated authority without erasing that history.
* No questions: non-interactive execution and sufficient scope.

## Direction Controls

| Control | Source | Effect |
| --- | --- | --- |
| Free/B1, uksouth, RG ama, USD700 cap | Owner request 2026-10-27 / issue #140 | Only author definitions inside this envelope |
| Never deploy/delete RG/read secrets/use uv | Owner request | No Azure resource or credential operations |
| Local az bicep build and existing infra tests | Owner request | No full gate; scoped --changed only if needed |
| Preserve original evidence | Repository retention / RPI conventions | New dated artifacts, no historical outcome rewriting |

## Research Questions

| ID | Question | Type | Status |
| --- | --- | --- | --- |
| Q1 | What is already implemented, and where does it fall short of #140? | depth | Open |
| Q2 | Which tier, identity, diagnostics and production network definition is valid? | depth | Open |
| Q3 | Which acceptance criteria can local build/tests prove without deployment/what-if? | straightforward | Open |

## Prior Knowledge Gate

* Read issue #140, ADR 0003 and BRD FR-048/OD-43 first.
* Branch is already feat/iot-hub-bicep-module, initially clean; no existing PR.
* Existing module and 2026-10-15 evidence are present despite the issue's stale "Not started" description. They must be verified, not recreated blindly.
* Read project original/addendum, reference index and owner memory; memory is context only.

## Research Cycle Log

### Cycle 1

#### Wave 1: Wider

* Inspected module, entrypoint, network, role matrix, compiled policy tests, static tests and existing build/what-if workflows.
* Reflection: the existing module grants Event Hubs Data Receiver on IoT Hub, logs connection/identity events, permits S1 and ten units, and uses an unverified currency-neutral 25 budget. Static tests do not establish the authentication contract.

#### Wave 2: Deeper

* Prioritized authentication, diagnostic privacy and the least-cost supported replacement.
* Microsoft explicitly says the built-in Event Hubs-compatible endpoint still requires shared access keys; Entra consumption requires routing to a custom Event Hub. The current role on IoT Hub cannot meet the keyless consumer criterion (W1).
* IoT Hub managed-identity routing supports Event Hubs Data Sender; private-resource trusted-service routing requires a system-assigned identity and role propagation before endpoint registration (W2).
* IoT Hub Private Link supports both device endpoint and built-in endpoint DNS; Event Hubs requires a separate namespace endpoint with the shared servicebus private DNS zone (W3).
* Reflection: keeping the old role would preserve a false acceptance claim. A custom Standard Event Hub is a necessary infrastructure dependency, not a replacement for IoT Hub or an SDK/consumer change.

#### Wave 3: Contrarian

* Challenged the old "no DeviceTelemetry means no device IDs" assertion: Connections/DeviceIdentityOperations can contain device identifiers. Select metrics-only diagnostics; do not enable resource logs.
* Challenged F1 as a zero-cost drop-in: free cannot be upgraded, and its limited allowance is not the selected Basic exercise definition. Select B1/one unit only within the owner's Free/B1 envelope; reject S1 and scale-out.
* Challenged immediate route creation with system identity: the role cannot exist before the hub is created. A phased enable flag is possible but makes a later default redeploy disable an active route. Prefer an explicit bootstrap/final-update composition using one shared hub-resource template, so the final definition always has routing and sender-role dependency. Plan critique must evaluate this sequencing.
* Challenged default-deny Event Hubs with no firewall rules: official docs warn an empty allowlist can still expose public access. Use public access Disabled plus trusted-services exception if supported; otherwise use selected networks with an actual VNet rule and system identity. Verify the exact supported combination before implementation.
* Reflection: no offline result proves actual role propagation, network behavior, quota, budget headroom or what-if. Use Refs #140 and preserve open live gates.

## Evidence Log

| ID | Claim | Location | Confidence |
| --- | --- | --- | --- |
| C1 | Issue lists six infrastructure criteria and dependencies | https://github.com/jmservera/ama/issues/140 (retrieved 2026-10-27) | High |
| C2 | Existing Basic exercise acceptance does not establish operational authority | docs/adrs/0003-journey-derived-capabilities-runtime-fit.md:12 | High |
| C3 | OD-43 blocks real operational monitoring, not simulator exercise | docs/brds/agentic-retrofit-programme-brd.md:2161 | High |
| C4 | Existing module uses an ineffective consumer role scope and device-bearing log categories | infra/modules/iothub.bicep:30 | High |
| C5 | Main passes only the API consumer principal and private-by-default switch | infra/main.bicep:302 | High |
| C6 | Build/lint, infra tests and owner-gated what-if already exist | .github/workflows/mvp-validation.yml:33; .github/workflows/infra-plan.yml:47 | High |
| C7 | Historical Review overclaims acceptance while admitting unrun what-if | .copilot-tracking/reviews/2026-10-15-iot-hub-bicep-review.md:3 | High; retained unchanged |

| ID | External source / finding | URL | Retrieved |
| --- | --- | --- | --- |
| W1 | Microsoft Entra access: built-in endpoint requires shared key; custom Event Hub supports Entra | https://learn.microsoft.com/en-us/azure/iot-hub/authenticate-authorize-azure-ad | 2026-10-27 |
| W2 | Managed identities, sender role and endpoint-registration ordering | https://learn.microsoft.com/en-us/azure/iot-hub/iot-hub-managed-identity | 2026-10-27 |
| W3 | Private Link and trusted-service egress | https://learn.microsoft.com/en-us/azure/iot-hub/virtual-network-support | 2026-10-27 |
| W4 | Free/Basic features, B1 400,000 messages/day, no F1 upgrade | https://learn.microsoft.com/en-us/azure/iot-hub/iot-hub-scaling | 2026-10-27 |
| W5 | Monitoring reference, metrics and resource log shapes | https://learn.microsoft.com/en-us/azure/iot-hub/monitor-iot-hub-reference | 2026-10-27 |
| W6 | Empty firewall rule warning and trusted IoT system identity | https://learn.microsoft.com/en-us/azure/event-hubs/event-hubs-ip-filtering | 2026-10-27 |
| W7 | Stable IoT Hub routing schema | https://learn.microsoft.com/en-us/azure/templates/microsoft.devices/2023-06-30/iothubs | 2026-10-27 |
| W8 | Event Hubs Standard UK South USD0.03/TU-hour, USD0.028/million ingress events | https://prices.azure.com/api/retail/prices | 2026-10-27 |

## Current Decisions

Keep the existing topic branch, preserve prior evidence, perform the full ordered loop, and publish only local evidence. No live what-if or deployment.

## Open Questions, Risks and Residual Uncertainty

W9 confirms public network Disabled plus trusted-services exception is supported. Public retail API returns B1 USD10/month and Event Hubs USD0.03/TU-hour plus USD0.028/million ingress events; generic Private Link pricing remains an explicitly labelled public-page estimate, not a subscription quote. No subscription reads, secret access, deployment or what-if performed.

## Parent Synthesis and Disposition

* Accepted: B1/one unit; two partitions; one-day transport retention; metrics-only diagnostics; individual per-device credentials owned by Juan Manuel Servera; API receiver role on a dedicated custom Event Hub.
* Accepted: private endpoints for hub and Standard Event Hubs namespace; namespace public access Disabled, trusted-services exception for the hub system identity, sender role at namespace scope per Microsoft guidance.
* Selected explicit bootstrap/activation parameter rather than implicit same-resource bootstrap/update deployments. Default bootstrap creates the private hub, Event Hub and roles with routing disabled. Future separately authorized activation requires waiting for role propagation, then preserving the activation parameter on every later deployment. No devices or messages are authorized during bootstrap. This avoids circular dependencies and hidden route churn on every normal deployment.
* Rejected: Event Hubs Data Receiver on IoT Hub (W1); S1/scale-out (owner envelope); shared service keys; resource logs with device identifiers (W5); unconditional route registration before its system identity role exists (W2).
* Deferred: live what-if, exact region/quota and role propagation checks, real transport, actual cost headroom and OD-43 operational approvals.
* Another complete cycle: not needed. Focused questions are answered sufficiently for authoring; live gaps cannot be resolved under the explicit no-Azure execution scope.

| ID | External source / finding | URL | Retrieved |
| --- | --- | --- | --- |
| W9 | Event Hubs private endpoint mode explicitly permits trusted-services exception | https://learn.microsoft.com/en-us/azure/event-hubs/private-link-service | 2026-10-27 |
| W10 | UK South B1 USD10/month, Free USD0/month; public list price, not actual subscription cost | https://prices.azure.com/api/retail/prices?$filter=armRegionName%20eq%20%27uksouth%27%20and%20contains(productName,%20%27IoT%20Hub%27)&currencyCode=USD | 2026-10-27 |

## Findings Mapped to Questions and Evidence

| Question | Finding | Evidence |
| --- | --- | --- |
| Q1 | Repair existing module and associated policy/matrix tests; do not recreate or claim not-started | C4-C7 |
| Q2 | B1 + custom Standard Event Hub is the supported keyless consumer definition; stage system-identity routing | W1-W4, W6-W10 |
| Q3 | Local compiler/linter and structural/mutation tests establish authored contracts, not actual Azure execution | C6-C7, W2-W3 |

## Alternatives and Decision State

The selected route adds Event Hubs as an authenticated consumer adapter, not an alternative device identity boundary. Shared-key built-in consumption is incompatible with the acceptance criterion. Implicit duplicate-resource bootstrap was considered but rejected for recurring route churn and complexity. A separate live activation remains visible and blocked.

## Self-check

All three waves completed inline in order. Evidence distinguishes code, official guidance, public estimates and owner direction. No worker implied, secrets read, source edits, provisioning or legal approval. Prior artifacts remain unchanged.

## Planning Readiness

Ready for scoped authoring. Research disposition: executed / Complete. Q1-Q3 answered.
Next action: Plan precise source/test/documentation changes, with one independent critique.

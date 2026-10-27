<!-- markdownlint-disable-file -->
# RPI Phase Details: IoT Hub Bicep module

## Metadata

* Task ID: issue-140
* Task slug: iot-hub-bicep-module
* Date: 2026-10-27
* Plan: .copilot-tracking/plans/2026-10-27/iot-hub-bicep-module-plan.md
* Research: .copilot-tracking/research/2026-10-27/iot-hub-bicep-module-research.md

## Phase Index

| Phase | Name | Status | Tasks |
| --- | --- | --- | --- |
| P01 | Infrastructure contract | Complete: module/main build and lint passed | P01-T01 |
| P02 | Tests and decisions | Complete: compiled/mutation tests, matrix, ADR/runbook/index/log reconciled | P02-T01, P02-T02 |
| P03 | Local validation | Complete: 459 tests, changed Bicep build/lint and scoped ruff passed | P03-T01 |

<!-- rpi:phase id=P01 -->
## P01: Correct the infrastructure contract

<!-- rpi:task id=P01-T01 -->
### P01-T01: Implement keyless transport, networking, diagnostics and constraints

Context: research W1 disproves the existing built-in receiver role. W2 requires system identity plus sender role before custom route registration; no source-only test can prove Azure role propagation.

Implement a dedicated Standard/one-TU Event Hubs namespace inside iothub.bicep, telemetry hub and consumer group. Namespace public access Disabled, local auth disabled, trusted-service bypass enabled, private namespace endpoint using the existing servicebus DNS zone. API Data Receiver scope is the event hub, not namespace or IoT Hub. Hub system identity Data Sender scope is the dedicated namespace as documented. Keep all resources at resource-group scope. Extend the existing main parameter-guard to require resourceGroup().name == 'ama' and primary location == 'uksouth' before the entire main graph; do not constrain independently configured SQL/global placements. Also protect standalone module use with a narrowly scoped equivalent and full dependency coverage (PC-001).

Expose a routing-ready parameter through main. False (default) registers no custom Event Hubs endpoint, has no active custom route and disables fallback, explicitly bootstrap-only (PC-002). It retains system identity, namespace, entity, group, sender/receiver roles and endpoints. True configures identityBased endpoint using system identity and all-device-message route. The operator must wait for actual sender role propagation before that separately approved second apply and preserve true in subsequent private parameter files. No device provisioning during bootstrap. No hidden deployment loop or automatic activation.

Select B1 only and one unit (reject S1 and scale-out), retain bounded 1-7 days and 2-32 partitions. Add nonsecret FQDN/entity/group outputs for #110. Do not write API SDK/runtime code.

Diagnostics must explicitly disable allLogs and export AllMetrics only on hub and namespace. This corrects the old Connections/DeviceIdentityOperations leak. Configure a positive <=700 budget for all owned transport resources, with emails; document alert-only semantics.

Completion: compiler-valid actual resource graph, no key functions/secrets and no source changes beyond these dependencies.

<!-- rpi:phase id=P02 -->
## P02: Lock local contract and document decisions

<!-- rpi:task id=P02-T01 -->
### P02-T01: Extend compiled, network and role-matrix tests

Reuse compile_bicep, evaluate, resources and resource helpers in test_bicep_policy.py rather than adding a second parser/evaluator. Replace four weak IoT source tests with compiled assertions. Existing policy/network coverage assumes one target per module; generalize only to cover the added namespace and its own endpoint, without weakening checks for the original hub.

Update role-matrix parser to recognize the hub system principal distinctly from the API principal; assert expected sender and receiver scopes and reject broad roles. Add focused mutation tests for critical route/network/auth/diagnostic contracts. Preserve every unrelated test. Bicep guard tests evaluate actual compiled resourceGroup() fixtures for ama/uksouth, wrong RG, wrong primary region and both wrong, inspect the full main dependency graph, and reject bypass mutations. False/true routing assertions distinguish endpoint absence/presence from active-route absence/presence, require disabled fallback and persistent identity/roles, reject endpoint registration during bootstrap even with route disabled, and prevent a hub-to-own-sender cycle. No local test claims actual role propagation.

Completion: targeted semantic/mutation tests pass and existing matrix/network controls retain their original scope.

<!-- rpi:task id=P02-T02 -->
### P02-T02: Reconcile ADR, runbook, budget and reference pointers

Add dated owner-authorized source-only delta to ADR 0003 and replace stale infra proposals with a truthful current decision table. Do not imply that approving the ADR settles OD-43 or that the owner approved a paid deployment. Record device credential owner Juan Manuel Servera as exercise selection, with no operational appointment inferred; individual registry identities/per-device symmetric keys or X.509, no DPS, issue/rotate/revoke under owner control via later #185 work, never actual keys.

Record public B1 USD10/month and Standard TU USD21.90/730h plus ingress. Private endpoint/DNS/diagnostic allowances must be labelled estimates when public page only yields placeholders. Reserve a bounded USD60 transport allocation inside the USD700 overall cap only if supported by the final calculation; actual aggregate headroom unknown and blocks provisioning. A budget resource is alert-only, not an enforced cap.

Update reference index and append new log entry. Preserve old ADR history and original tracking outcomes.

<!-- rpi:phase id=P03 -->
## P03: Validate and prepare independent Review

<!-- rpi:task id=P03-T01 -->
### P03-T01: Run local compilation, lint, targeted and existing infra tests

Commands: az bicep build/lint module and main, REQUIRE_AZ_BICEP=1 python3 -m unittest discover -s infra/tests -q, targeted scoped ruff and git diff --check. Start with the four directly coupled test modules. Expand to the full existing infra suite, not a full RPI gate. Missing dependencies may be restored with pip after the observed failure; never use uv or read private datasets/secrets.

Record actual results, failure/correction history, acceptance evidence and unrun live checks in the dated changes record. Reconcile plan markers and details before one independent Review. Review findings become later work; no repeated Review.

### Completion Evidence

All P01-P03 tasks completed within the locked change budget: twelve IoT test
methods replace the four old substring methods, and existing matrix/network/
policy tests are extended rather than unrelated tests removed. The shared
compiled evaluator gained explicit synthetic ARM context; dependency-ID
resolution now handles child resources for both main and standalone guards.
All 459 infra tests pass with REQUIRE_AZ_BICEP=1 and no skips. All changed
Bicep sources build/lint and scoped ruff check/format passes. No full RPI gate,
Azure what-if, deployment, secret access or operational approval occurred.

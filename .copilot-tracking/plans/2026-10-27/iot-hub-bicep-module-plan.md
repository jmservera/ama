<!-- markdownlint-disable-file -->
# RPI Plan: IoT Hub Bicep module

## Task Metadata

* Task ID: issue-140
* Task slug: iot-hub-bicep-module
* Plan date: 2026-10-27
* Planning status: Implemented and locally validated; single critique Complete / Revise, both compatible planner corrections applied
* Phase details: .copilot-tracking/details/2026-10-27/iot-hub-bicep-module-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-10-27/iot-hub-bicep-module-plan-critique.md

## Executive Summary

Correct the existing B1 definition to provide a supported keyless consumer path, private networking, privacy-preserving diagnostics and bounded cost documentation. Retain the IoT Hub device boundary and add a dedicated Standard Event Hub for Entra consumption. No Azure operations follow from this authoring task.

### What You May Not Know

Microsoft documents that the built-in IoT Hub endpoint requires a shared service key. Its current Event Hubs receiver role cannot work as claimed. System-identity routing also needs sender-role propagation before endpoint registration, so bootstrap and activation are explicit, not hidden deployment retries.

### Unresolved Decisions or Blockers

No local authoring blocker. Actual quota, pricing/headroom, what-if, role propagation, transport and OD-43 remain separate live/human gates. The PR will use Refs #140, not closure.

## User Decisions and Requirements

* Run research, plan, implement and review in order with dated artifacts.
* Owner approved ADR 0003 on 2026-10-27; Free/B1 envelope, ama RG only, USD700 cap; never delete ama and do not deploy.
* Author Bicep under infra/, with az bicep build and existing local infra tests; no mvp code, secrets, uv or full gate.
* Conventional Commit with Copilot trailer; push feat/iot-hub-bicep-module and open an evidence-qualified PR.

## Goals

* Make the authored identity/network/diagnostics contract correct rather than preserving false historical acceptance claims.
* Provide measurable local coverage and an honest six-criterion acceptance matrix.

## Scope and Non-Goals

* In scope: iothub module, its main integration/outputs, shared policy and role-matrix tests, infra README, dated ADR delta, reference index/log.
* Non-goals: SDK/consumer work (#110), device enrolment (#185), deploying or running what-if, subscription cost reads, operational monitoring/OD-43 approval, changing hosted workflows/protection.

## Functional Requirements

* B1 only, one unit, uksouth; two partitions; one-day transport retention by default (bounded at seven).
* Add Standard Event Hubs namespace (one TU, no auto-inflate), telemetry event hub and api-consumer group. Route all DeviceMessages using the IoT Hub system identity; disable built-in fallback. API gets only Data Receiver on the telemetry event hub; hub identity gets only Data Sender on its dedicated namespace.
* Explicit routing-ready flag defaults false for first provisioning. Bootstrap creates hub/roles but registers no custom endpoint, enables no route and disables fallback; devices must not be provisioned or send. Future owner-authorized activation waits for role propagation, records it, then sets/preserves the flag true. No activation/deployment is performed here.
* IoT Hub and Event Hubs namespace both disable local service authentication. Per-device SAS remains explicitly supported; module SAS disabled. No keys or connection strings in source/outputs.
* Both services have private endpoints. Namespace public access always Disabled with default Deny and trusted-service access for system-identity routing; IoT public switch remains development-only via main's existing profile gate.
* Metrics-only Log Analytics diagnostics, no device-bearing resource logs; explicit disabled allLogs prevents retaining the old diagnostic categories.
* Budget entry includes B1, Event Hubs TU/ingress, two endpoints, diagnostics/DNS contingency inside a USD700 overall cap; alerts are not hard spending limits.

## Non-Functional Requirements

* Existing strict Bicep rules pass; structural tests inspect compiled resources and activation variants, not only source substrings.
* Enforce B1/one-unit limits and positive bounded budget. Existing main parameter-guard must check resourceGroup().name == ama and primary location == uksouth before the whole main graph; do not constrain independent SQL/global placements. Standalone module has equivalent checks and dependencies.
* Do not broaden source/test scope beyond the module's actual dependencies. Preserve historical evidence and unchecked human gates.

## Acceptance Criteria

| Issue criterion | Local acceptance target | Not implied |
| --- | --- | --- |
| Tier/region/units/cost/retention | Recorded defaults, constraints and priced scenario before provisioning | Subscription quote/headroom |
| Module, group/routing, diagnostics | Compiled private keyless route/group and metrics destinations | Routed live messages |
| API least-privilege identity | Correct Event Hub receiver assignment/matrix; no service credentials | Actual token/SDK authentication |
| Production network | Private endpoints/DNS, public disabled and trusted exception | Azure network acceptance |
| Provisioning/owner | Individual identities; Juan Manuel Servera issues/rotates; DPS deferred | Device creation/credential access |
| Build/lint/what-if/budget gates | Local build/lint/tests and existing guarded what-if wiring | Unrun live what-if/full gate |

## Implementation Context Record

* Research: .copilot-tracking/research/2026-10-27/iot-hub-bicep-module-research.md (Complete / Ready).
* Plan/details/critique: paths in metadata; critique pending.
* Changes record: .copilot-tracking/changes/2026-10-27/iot-hub-bicep-module-changes.md, owned by Implement.
* Continuation: owner-authorized automatic parent advances after critique disposition.

## Sources

* Research C1-C7, W1-W10: current code, official identity/network/schema and public retail evidence.
* Issue #140, ADR 0003 decision 6 and BRD OD-43/FR-048.

## Phase Checklist

### Current bounded implementation: RV-001

The owner selected RV-001 for later implementation on PR #498 on 2026-10-27.
Only P04 is active in this invocation; P01-P03 and the original critique/Review
outcomes remain historical. Normalize the provider URI once for both the SDK
hostname and active sb URI; evaluate port-bearing and portless fixtures through
module outputs and main forwarding. No Azure operations or second Review.

<!-- rpi:phase id=P01 -->
### [x] P01: Correct the infrastructure contract

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Implement keyless transport, networking, diagnostics and constraints

* Targets: infra/modules/iothub.bicep, infra/main.bicep, narrowly scoped guard if needed.
* Detail: P01-T01 in phase details.

<!-- rpi:phase id=P02 -->
### [x] P02: Lock local contract and document decisions

* Depends on P01.

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Extend compiled, network and role-matrix tests

* Targets: infra/tests/test_iothub_module.py, test_identity_rbac.py, test_edge_module.py, test_bicep_policy.py and infra/role-assignments.json.

<!-- rpi:task id=P02-T02 -->
#### [x] P02-T02: Reconcile ADR, runbook, budget and reference pointers

* Targets: infra/README.md, ADR 0003, docs/reference/README.md and append-only log.md.

<!-- rpi:phase id=P03 -->
### [x] P03: Validate and prepare independent Review

* Depends on P02.

<!-- rpi:task id=P03-T01 -->
#### [x] P03-T01: Run local compilation, lint, targeted and existing infra tests

* No full gate or Azure what-if. Record commands/counts/outcomes and residuals.
* Handoff exactly once to independent rpi-review after all markers/evidence reconcile.

<!-- rpi:phase id=P04 -->
### [x] P04: Resolve RV-001 in later implementation

<!-- rpi:task id=P04-T01 -->
#### [x] P04-T01: Normalize namespace hostname and evaluate regression fixtures

* Targets: infra/modules/iothub.bicep and infra/tests/test_iothub_module.py.
* Cover HTTPS endpoints with/without port 443 and trailing slash; retain
  bootstrap omission and assert module output, main forwarding and active URI.
* Validate with REQUIRE_AZ_BICEP=1 in an external isolated pip venv, build/lint,
  scoped Ruff and diff checks. Record evidence in changes and a review addendum.
* Preserve original Review verdict, PR draft status and `Refs #140`.

## Test Ownership and Change Budget

* Canonical test owner: existing infra unittest suite; no new runner or dependency unless a real missing-dependency failure.
* Exact removals: replace the four weak substring tests in test_iothub_module.py with compiled semantic tests; no other test removal.
* Maximum additions: 20 IoT-specific tests plus up to six tightly coupled policy/matrix/network tests; no unrelated suite growth.
* Canonical targets: Bicep sources and existing tests. Generated ARM JSON remains temporary/external, not committed.
* Semantic coverage: SKU/capacity/retention, route activation and identity shape, correct roles/scopes, PE/DNS links, metrics-only destinations, budget filters/limits and scope guards.
* Regression/mutation coverage: broaden role, enable public access/log categories/fallback, register endpoint during bootstrap, lose endpoint/DNS or bypass scope checks must be rejected by the same semantic assertions. Evaluate ama/uksouth, wrong RG, wrong region and both wrong; inspect main and standalone dependency boundaries and prevent hub-to-sender circularity.
* Validation evidence: az bicep build/lint main + module; python3 -m unittest discover -s infra/tests -q with REQUIRE_AZ_BICEP=1; scoped ruff if installed/repository runner.

## Dependencies

* #110 consumer and #137 actual capability checks remain open, not prerequisites for source-only authoring.
* Route activation requires actual system identity/RBAC propagation, separately authorized later.

## Critique Disposition

Exactly one fresh independent critique executed. Original verdict **Revise** is preserved.

| Finding | Owner / disposition | Resolving planning evidence |
| --- | --- | --- |
| PC-001 High | Planner / directly corrected | Main named guard covers the entire graph, standalone equivalent is additional; P01-T01 and compiled scope/dependency tests clarified |
| PC-002 Medium | Planner / directly corrected | Bootstrap must omit endpoint registration, not just deactivate routes; P01-T01 and P02-T01 explicitly require false/true semantics plus bootstrap-endpoint mutation rejection |

No unresolved significant/divergent decision. Runtime propagation, redeploy flag preservation and alert-only budget remain explicit residual gates. No second critique.

## Follow-Up Items

* Actual live what-if/transport/role propagation and budget headroom require later owner-authorized work.
* OD-43 real inventory, lawful basis, DPIA, retention, calibration and operational review ownership remain with named human owners.

## Handoff

Implementation P01-P03 complete. All four changed Bicep sources build/lint;
459 existing infra tests pass without skips in the isolated pip environment.
Scoped ruff check/format and diff whitespace checks pass. Twelve IoT tests
include both critique obligations and mutations. Ready for one independent
Review; preserve the original critique verdict. No deployment, live what-if,
full gate, budget headroom or OD-43 acceptance is inferred.

### Later RV-001 implementation handoff (2026-10-27)

P04 alone is complete: one normalized hostname feeds both the SDK output and
sb routing URI. Four HTTPS fixture forms evaluate module outputs, main
forwarding and false/true routing; mutations reject port leakage and wrong
forwarding. All 461 infra tests pass with REQUIRE_AZ_BICEP=1 and zero skips in
the external pip venv; module/main build/lint, scoped Ruff and diff checks pass.
The separate review addendum records RV-001 resolved locally without rewriting
the original Complete / Not accepted Review or executing a second Review.
No live acceptance, hosted/human approval or full-gate success is implied.

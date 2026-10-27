<!-- markdownlint-disable-file -->
# RPI Changes: IoT Hub Bicep module

## Metadata

* Task ID: issue-140
* Task slug: iot-hub-bicep-module
* Implementation date: 2026-10-27
* Plan: .copilot-tracking/plans/2026-10-27/iot-hub-bicep-module-plan.md
* Details: .copilot-tracking/details/2026-10-27/iot-hub-bicep-module-phase-details.md
* Critique: .copilot-tracking/reviews/plans/2026-10-27/iot-hub-bicep-module-plan-critique.md, Complete / Revise, PC-001/002 planner-corrected.

## Execution Status

* Current later invocation: P04 / P04-T01, RV-001 correction, Complete.
* Owner-selected boundary: shared namespace normalization, compiled evaluated
  fixtures, current planning/state evidence and a separate review addendum.
* Required validation: external isolated pip venv, REQUIRE_AZ_BICEP=1 full infra
  discovery, changed Bicep build/lint, scoped Ruff and diff checks.
* Original P01-P03 implementation and Review below remain historical; original
  Review Complete / Not accepted is not rewritten or repeated.

* Original status: Complete (full scoped implementation plan); subsequent
  original Review Complete / Not accepted, preserved unchanged.
* Original declared scope: Full plan P01-P03; later invocation only P04.
* Completed: P01, P01-T01, P02, P02-T01, P02-T02, P03, P03-T01, P04, P04-T01.
* Remaining active-plan markers: None.
* Boundary: source/tests/docs and dated evidence only. No deployment, what-if, secrets, uv or full gate.

## Execution Summary

Implement the corrected B1/keyless custom-Event-Hub transport definition and explicit bootstrap/activation boundary. Enforce ama/uksouth before the whole main graph, preserve private defaults, and use metrics-only diagnostics.

## Completed Work

### Keyless transport and integrated scope guards

* Related task: P01-T01.
* Files: infra/modules/iothub.bicep, infra/modules/iothub-scope-guard.bicep, infra/modules/guard.bicep, infra/main.bicep.
* Defined B1/one-unit hub plus dedicated private Standard Event Hub, namespace sender and entity-scoped receiver, explicit bootstrap endpoint omission, metrics-only diagnostics, bounded budget and nonsecret outputs.
* Main and standalone named scope guards cover ama/uksouth; full compiled dependency assertions cover both graphs.
* Evidence: az bicep build/lint module and main passed; 12 compiled IoT tests including rejection mutations passed before the separate role suite hit a missing distribution.

### Compiled tests and role/network matrix

* Related task: P02-T01.
* Files: infra/tests/test_iothub_module.py, test_bicep_policy.py, test_identity_rbac.py, test_edge_module.py and infra/role-assignments.json.
* Twelve IoT tests replace four weak substring tests. Semantic checks cover endpoint absence/presence, route and identity/scopes, private endpoints/DNS, metrics-only destinations, cost/sizing/retention, actual main wiring and all-resource guards. Mutation subcases reject bootstrap registration, fallback/auth changes, a hub-to-sender dependency, public namespace/trust/DNS loss, device-bearing logs, wrong receiver scope/principal/role, missing/bypassed scope checks/constraints and unordered resources.
* Existing policy test dependency checks are shared and strengthened to resolve child-resource IDs; endpoint policy handles the namespace as a distinct target, while preserving hub coverage. The matrix recognizes IoT system identity separately from API.
* Evidence: 12 IoT + 50 compiled-policy targeted tests passed; complete existing infra discovery then passed all 459 tests without skips.

### Dated decisions and honest acceptance boundary

* Related task: P02-T02.
* Files: infra/README.md, docs/adrs/0003-journey-derived-capabilities-runtime-fit.md, docs/reference/README.md and append-only docs/reference/log.md.
* Recorded the owner-supplied 2026-10-27 source-only authorization, keyless adapter correction, named exercise credential owner, individual enrolment and six-criterion evidence matrix.
* Public B1/TU/ingress inputs plus explicitly unverified endpoint/variable allowances yield a modelled USD60/month transport allocation. It is not extra spend approval, actual headroom or an enforceable cap. Bootstrap/activation and preserving true on redeploy are explicit.
* Original ADR proposal/approval history and 2026-10-15 tracking outcomes remain intact. No memory, original case study or real OD-43 approval changed.

## Implementation-Time Plan and Detail Updates

### Compiler and fixture corrections

* Local implementation judgment, no new user decision or scope change. Bicep's environment suffix type has no serviceBus property; derive the nonsecret endpoint from the namespace's serviceBusEndpoint instead.
* Initial compiled test assumptions incorrectly expected extension-resource format() scope and single-segment child dependency IDs; corrected to actual resourceId scopes and shared dependency-ID resolution. Preserves the same assertions, rather than weakening them.
* Critique is not repeated; PC-001/002 requirements remain unchanged.

### Isolated dependency restoration

* The first coupled role-suite attempt failed importing zava_forward. The host also lacked ruff, and system pip correctly refused installation under PEP668.
* Created an external session-local pip venv; installed src/core, agents, api and orchestrator distributions with --no-deps, hash-pinned src/api requirements, PyYAML 6.0.3 and repository-version ruff 0.17.1.
* No PYTHONPATH=mvp workaround, uv, private dataset or secret access.

### Scope-fixture reconciliation

* The first full infra run found one additional demo-guard fixture using offline-region, now intentionally rejected by the new primary uksouth guard. Changed that synthetic primary fixture to uksouth while leaving independently chosen SQL fixtures unchanged.
* This is tightly coupled expected-behavior test maintenance, not an unrelated source fix or weakened guard. The original failed run was 459 tests / one failure; final identical discovery passes.

## Validation Record

| Check | Scope | Status | Evidence |
| --- | --- | --- | --- |
| Azure CLI/Bicep availability | Local compiler | Passed | az bicep version: 0.48.1 |
| Initial Bicep compile | Module | Failed, corrected | Unsupported environment().suffixes.serviceBus; derive serviceBusEndpoint from namespace instead |
| Initial compiled IoT tests | 12 tests | Two fixture failures, corrected | Actual ARM scopes use resourceId; child IDs have separate name arguments |
| Initial dependency availability | Host Python | Missing, restored externally | zava_forward and ruff missing; PEP668 respected with session-local venv |
| Initial complete infra suite | 459 tests | One fixture failure, corrected | Demo primary-region fixture reconciled to intentionally enforced uksouth |
| az bicep build and az bicep lint | infra/main.bicep, modules/iothub.bicep, modules/guard.bicep, modules/iothub-scope-guard.bicep | Passed | Each compiled to stdout/discarded locally; no warnings |
| Targeted compiled contracts | test_bicep_policy.py; test_iothub_module.py | Passed | 50 + 12 tests, including mutation rejection |
| REQUIRE_AZ_BICEP=1 python -m unittest discover -s infra/tests -q | Complete existing infra suite | Passed | 459 tests in 109.822 seconds; zero skips |
| ruff 0.17.1 check --isolated --select E,F,I,B,UP --target-version py312 --line-length 100 | test_iothub_module.py, test_bicep_policy.py | Passed | All checks passed |
| ruff format --isolated --line-length 100 --check | Same two compiled test files | Passed | Both already formatted |
| git diff --check | Entire current diff | Passed | No whitespace errors |
| Live what-if, deployment, real token/network/diagnostic flow, full RPI gate | Azure/publication execution | Not run | Explicit owner local-only/no-full-gate scope; no claim of hosted approval |

Console messages mentioning post-deployment checks were emitted by mocked
pipeline test fixtures, not actual Azure operations.

## Pre-Review Reconciliation

* Plan markers: all P01-P03 tasks checked with evidence above.
* Phase details: current completion and actual evidence recorded.
* Handoff prose: ready for one independent Review of source-only definitions.
* Blockers: no local authoring blocker; actual Azure/OD-43 gates remain deferred.
* Acceptance matrix: infra README explicitly maps all six criteria to authored evidence and remaining live proof.
* Test scope: within locked budget; no unrelated test removal or generated ARM snapshot.

## Blockers

No local authoring blocker. Actual Azure role propagation, budget headroom, what-if and OD-43 remain separate gates.

## Remaining Work

No remaining active implementation markers. Independent Review and authorized publication remain.

## Follow-Up Items

Canonical plan Follow-Up Items: later owner-authorized live what-if/transport/role propagation/headroom and OD-43 human operational approvals.

## Return-to-Caller State

Implementation complete, full plan. Automatic parent continues to one independent
Review, then records original outcome before authorized commit/push/PR.
No source deployment is authorized. Review findings route to later work, not
another implementation/Review loop in this task.

## Later Implementation: RV-001 (2026-10-27, PR #498)

* Related task: P04-T01, correcting P01-T01/P02-T01 under explicit owner direction.
* Classification: immediately relevant implementation/test correction; no new
  architecture, paid resource, deployment or human-approval decision.
* First boundary: add evaluated port-bearing/portless regression coverage, then
  normalize the provider endpoint once for SDK output and active routing.
* Initial validation in a newly created external pip venv failed (346 discovered
  tests, 10 errors) because zava_forward/PyYAML were absent. Dependencies will
  be restored using the documented pip prerequisites; no production manifest
  changes, uv or service/secret calls.
* Original critique and Review artifacts stay unchanged. Publication remains
  subject to applicable local/hosted/human gates; a source fix is not acceptance.

### Completed normalization and evaluated regression

* Files: infra/modules/iothub.bicep, infra/tests/test_iothub_module.py and the
  directly related namespace-output contract in infra/README.md.
* Extract the hostname from the provider's HTTPS authority, dropping any port
  and trailing slash, once. Export that hostname and construct the separate
  `sb://<hostname>/` routing URI from it instead of copying the HTTPS port.
* Four synthetic provider forms cover port 443 and trailing slash independently.
  Evaluate actual compiled module outputs and main forwarding expressions in
  both routing states, not output-name presence. Reuse the existing shared
  evaluator. Existing routing assertions now evaluate all four fixtures and
  still require empty bootstrap endpoints/routes.
* Two added test methods (14 IoT methods total, within the original budget):
  evaluated outputs and mutation rejection for hostname-port leakage,
  routing-port leakage and forwarding the wrong output. No unrelated tests,
  production dependencies or hosted workflow names changed.
* Before the fix, the two selected regressions failed with four failures,
  reproducing both the `:443` SDK hostname and active URI defects.
* First corrected full run: 461 tests, one failure because Bicep inlines the
  reference-bearing variable and the routing mutation was a no-op. Targeted
  the compiled URI format instead and assert the mutation actually changes it.
  Ruff also required explicit loop-variable binding; both fixture issues fixed.
* Restored the documented editable distributions, hash-pinned API requirements,
  PyYAML 6.0.3 and Ruff 0.17.1 with pip in the external session venv.

### Correction validation and residual gates

| Check | Result | Evidence |
| --- | --- | --- |
| REQUIRE_AZ_BICEP=1 external-venv/bin/python -m unittest discover -s infra/tests -q | Passed | 461 tests in 109.451s, zero skips |
| az bicep build --file <source> --stdout; az bicep lint --file <source> | Passed | iothub module and main, no diagnostics, Bicep 0.48.1 |
| Ruff 0.17.1 check --isolated --select E,F,I,B,UP --target-version py312 --line-length 100 | Passed | Changed test file |
| Ruff format --isolated --line-length 100 --check; git diff --check | Passed | Changed test already formatted; no whitespace errors |
| Original Review / fresh Review | Preserved / not repeated | Original Complete / Not accepted remains immutable; separate addendum records local RV-001 resolution |
| Full local publication gate | Pending exact-commit execution | Must not infer success from the scoped tests |
| Azure deployment, what-if, secrets, live transport and operational acceptance | Not performed | No authority implied by source-only correction |

Mocked pipeline messages in the suite are not Azure deployment evidence.
Current implementation has no remaining P04 work. Parent state removes the
resolved source defect from active blockers/follow-ups while preserving the
original Review decision; live acceptance and publication approvals stay open.

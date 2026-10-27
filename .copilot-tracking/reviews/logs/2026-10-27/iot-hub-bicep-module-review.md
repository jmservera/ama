<!-- markdownlint-disable-file -->
# Review: IoT Hub Bicep module

## Scope and Evidence

* Task ID: issue-140 / iot-hub-bicep-module.
* Review date: 2026-10-27.
* Review scope: One independent post-implementation Review of P01-P03 and the complete working diff, including the added standalone scope guard.
* Assessed boundary: Source-only infrastructure, tests, documentation and canonical dated RPI inputs. B1/one unit, uksouth, existing ama RG, USD700 aggregate envelope. No live acceptance or whole-issue closure.
* Plan: .copilot-tracking/plans/2026-10-27/iot-hub-bicep-module-plan.md
* Phase details: .copilot-tracking/details/2026-10-27/iot-hub-bicep-module-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-10-27/iot-hub-bicep-module-plan-critique.md
* Changes: .copilot-tracking/changes/2026-10-27/iot-hub-bicep-module-changes.md
* Research: .copilot-tracking/research/2026-10-27/iot-hub-bicep-module-research.md

## Opening Review State

* Interpreted review goal: Compare authored implementation, all six issue criteria, original critique obligations and recorded validation once; preserve all original outcomes and route later work without fixes.
* Review scope: Full scoped plan P01-P03, complete tracked diff and added infra/modules/iothub-scope-guard.bicep.
* Evidence readiness: All five supplied canonical artifacts available; plan tasks checked; changes record identifies passed local checks, corrected failures and deferred live gates. Source comparison pending.
* Acceptance basis: Owner's 2026-10-27 author/validate-only direction, current plan/details, original Complete / Revise critique with PC-001/002 planner dispositions, supplied W1-W10 evidence and six-criterion authoring matrix.
* First comparison boundary: Complete actual diff, then compiled infrastructure contract and test assertions against phase requirements; local structural evidence only.
* Active read-only boundaries: Only this review record may be written. No other artifact/source changes, fixes, commits, publication, Azure resource operations, live what-if, secrets, uv, full gate or nested delegation.
* Initial blockers: None to source review. Actual propagation, quota, pricing/headroom, transport, what-if, OD-43 and publication approvals are not established.

## Execution Status

* Execution status: Complete.
* Review execution evidence: All supplied canonical artifacts, complete tracked diff, added scope guard, relevant unchanged integration/helpers and workflows assessed once. Independent compilation/lint of all four changed Bicep sources and 40 bounded local tests passed. A separate read-only compiled-expression probe reproduced RV-001. No source fixes or second Review performed.

## Reviewed Boundary Reference

* HEAD: 65a514ed20e97816dbf47e9fb981ab4cfe40597d.
* SHA-256 of exact tracked non-tracking patch produced by `git diff --binary HEAD -- . ':!.copilot-tracking'`: bbf9e1382ca805a1a76bf9cab08272316caafa46acff33b75338762d3a8be3ea.
* SHA-256 of added infra/modules/iothub-scope-guard.bicep, not included in that tracked patch: 7500a345265ba37ea02121e5c21e7d78b8a9bb24ea41b89a61204593bdcca8a0.
* Tracked patch covers exactly docs/adrs/0003-journey-derived-capabilities-runtime-fit.md, docs/reference/README.md, docs/reference/log.md, infra/README.md, infra/main.bicep, infra/modules/guard.bicep, infra/modules/iothub.bicep, infra/role-assignments.json, infra/tests/test_bicep_policy.py, infra/tests/test_edge_module.py, infra/tests/test_identity_rbac.py and infra/tests/test_iothub_module.py.
* These references exclude this review record and parent-owned tracking/session state. Parent must compare the same patch digest and added-file hash before committing; a source correction is later work and does not change this original verdict.

## Plan-to-Change Reconciliation

| Current plan scope | Descriptive changes-record summary | Current-state reconciliation | Gap or rationale |
| --- | --- | --- | --- |
| P01 / P01-T01 | Keyless transport and integrated scope guards | Reconciled, with defect | B1/one unit, guards, routes, roles, endpoints and diagnostics implemented. Namespace endpoint derivation has RV-001 |
| P02 / P02-T01 | Compiled tests and role/network matrix | Reconciled, with coverage gap coupled to RV-001 | Twelve compiled IoT tests replace the four original substring tests; matrix and existing policy/endpoint assertions retained. Fixture omits the provider's possible HTTPS port; output assertion checks presence, not evaluated value |
| P02-T02 | Dated decisions and honest acceptance boundary | Reconciled | ADR delta, runbook, USD60 model, named exercise owner, index and append-only log distinguish source evidence from live gates |
| P03 / P03-T01 | Validation record and pre-review reconciliation | Reconciled | Full 459-test zero-skip result is implementation-reported, not independently rerun. Review reproduced bounded passing checks and a missing endpoint-shape case |
| Follow-Up Items | Later live work and OD-43 approvals | Reconciled; remain outside active scope | Distinct human/live follow-ups, not failed local tasks or implicitly approved work |

## Completed Work Assessment

| Related marker | Files | What changed and why | Completion evidence | Validation | Assessment |
| --- | --- | --- | --- | --- | --- |
| P01-T01 | infra/modules/iothub.bicep; infra/main.bicep | Dedicated Standard namespace and telemetry entity correct unsupported built-in keyless receipt; activation defaults off | Actual resource graph, receiver on entity, system sender on namespace, no service-secret retrieval | Independent build/lint and compiled IoT tests passed | Correct architecture and role scope; RV-001 affects nonsecret consumer contract and endpoint normalization |
| P01-T01 / PC-001 | infra/modules/guard.bicep; infra/modules/iothub-scope-guard.bicep | Guard ama and primary uksouth in main and standalone use | Compiled dependency assertions and four RG/region combinations; SQL/global locations remain independently configured | Independent guard and mutation tests passed | Critique obligation satisfied; no independently writable branch bypass observed |
| P01-T01 / PC-002 | infra/modules/iothub.bicep | Bootstrap omits endpoint registration and active routes, retains identity/RBAC/PEs, disables fallback | False/true evaluated routing; sender assignment follows hub; hub does not wait on own sender | Independent registration/fallback/auth/cycle mutations passed | Critique obligation satisfied; actual propagation remains a separate operator prerequisite |
| P01-T01 / P02-T01 | infra/modules/iothub.bicep; infra/tests/test_edge_module.py; infra/tests/test_bicep_policy.py | Two private endpoints, appropriate DNS and trusted-service exception; metrics-only diagnostics | Both namespace and rules public Disabled; Deny; no IP/VNet allowances; allLogs disabled; AllMetrics enabled at each service scope | Independent network, RBAC, diagnostics and mutation assertions passed | Source contract supported; no claim of private DNS, traffic acceptance, historical log erasure or effective Azure RBAC |
| P02-T01 | infra/tests/test_iothub_module.py; infra/tests/test_identity_rbac.py; infra/role-assignments.json | Compiled semantics and distinct principal matrix replace weak original checks | Exactly four original tests removed, twelve added; other edits extend existing tests | Independent 40-test bounded selection passed | Within test budget; passing fixture does not cover RV-001 |
| P02-T02 | infra/README.md; docs/adrs/0003-journey-derived-capabilities-runtime-fit.md; docs/reference/README.md; docs/reference/log.md | Dated source authorization and honest six-criterion/cost evidence | Original ADR restrictions retained as history; new authority is source-only; index and appended log point to canonical runbook | Direct complete diff/link review | No fabricated human, runtime or budget acceptance |
| P03-T01 | Canonical changes record | Actual failures/corrections and validation declared | Compiler suffix correction, ARM scope/dependency fixture corrections, dependency restoration and region fixture correction retained | Independent compiler checks agree; full suite reported 459 / zero skips | Local evidence is credible but cannot override the uncovered semantic defect |

## Implementation-Time Plan and Detail Update Assessment

| Affected area or marker | What changed and why | Triggering evidence and user decision | Reconciliation performed | Planning and critique state | Assessment |
| --- | --- | --- | --- | --- | --- |
| P01-T01 | Derive namespace endpoint from serviceBusEndpoint rather than nonexistent environment suffix | Recorded compiler failure; implementation judgment within accepted architecture | Changes record explains correction; current source uses runtime property | No new owner choice or architectural divergence | Direction preserved, but correction is incomplete for port-bearing responses: RV-001 |
| P02-T01 | Shared evaluator gains synthetic ARM context; dependency resolver handles child IDs | Compiled scopes and child-resource dependency expressions differed from fixture assumptions | Current compiled assertions inspect real guard/dependency graph; matrix distinguishes hub system identity | PC-001/002 requirements unchanged | Appropriate tightly coupled helper changes, not unrelated test removal |
| P03-T01 | Isolated pip environment and primary-region fixture reconciliation | Missing zava_forward/ruff, PEP668 refusal and one full-suite guard fixture failure | Changes record preserves failures and final commands/counts; independent SQL fixture stays unconstrained | Accepted local-only scope preserved | No uv, new production dependency or weakened owner guard inferred |
| Research synthesis / P01-T01 | Explicit default-off flag selected over speculative duplicate-resource bootstrap | Research parent synthesis selects flag and preserve-true procedure; plan/details and critique use that same choice | Final plan, details, runbook and implementation agree | Original critique remains Complete / Revise, compatible findings planner-corrected | Justified decision within source-only authorization; no unaccepted architecture change discovered |

## Critique and Material Revision Assessment

* PC-001 High: Planner correction implemented in main's existing parameter-guard plus standalone equivalent. Named ama/uksouth values, minLength constraints, every-resource dependency boundary, invalid-target combinations and bypass mutations are independently covered.
* PC-002 Medium: Bootstrap evaluates to no Event Hubs custom endpoint, no active custom route and disabled fallback; activation adds the system-identity endpoint and all-DeviceMessages route. Roles and identity are unconditional. Bootstrap-registration and hub-to-sender-cycle mutations are rejected.
* Original Complete / Revise verdict is preserved; resolving dispositions do not retroactively convert it to approval.
* No significant implementation-time revision requiring a new owner decision or fresh plan/critique was identified. The record supports corrected planning before implementation; this Review cannot independently establish wall-clock ordering from uncommitted artifacts alone.
* Current plan markers, details, handoff and changes evidence agree on completed authoring. Minor stale prose remains in the plan's Implementation Context Record ("critique pending") and research question table ("Open"), but their explicit terminal dispositions resolve state unambiguously; not a substantive finding.
* RV-001 is an implementation defect within the accepted direction, not a reason to reopen architecture selection or obtain new purchase authority.

## Six-Criterion Acceptance Assessment

The six issue criteria are assessed against the supplied research/plan and the runbook matrix; the issue was not independently retrieved. "Authored" below does not mean hosted, deployed, human-approved or whole-issue accepted.

| Issue criterion | Authoring evidence assessed | Remaining gate and disposition |
| --- | --- | --- |
| Tier/region/units/cost/retention | B1/one unit, uksouth, two partitions, bounded 1-7 days, Standard/one TU/no auto-inflate; positive budget <=700 | Public B1/TU/ingress inputs plus clearly labelled endpoint/variable assumptions model USD60/month. Actual subscription currency, prices, quota and aggregate USD700 headroom unverified; later owner-authorized provisioning gate |
| Hub/group/routing/diagnostics | Telemetry entity and api-consumer group, explicit bootstrap/activation, fallback off; metrics-only diagnostics on hub and namespace | RV-001 endpoint derivation defect; no actual message routing or Log Analytics arrival. Authoring not fully accepted while defect remains |
| API least-privilege/no keys | API receiver only at telemetry entity; hub sender only at dedicated namespace; service local auth off, per-device SAS separately explicit; no listKeys/secrets | RV-001 exported namespace host contract; actual #110 consumer/token acceptance and actual role propagation remain later work |
| Production networking | Unconditional endpoints, IoT/device and servicebus DNS mappings; namespace Disabled/Deny with trusted-service exception; existing main profile protects public hub opt-in | No live DNS, private traffic or public denial evidence; separately authorized network verification required |
| Individual provisioning/owner | Named Juan Manuel Servera exercise credential owner, individual registry identities, controlled issue/rotate/revoke expectations; DPS deferred | #185 implementation and actual credential handling not performed; no operational appointment inferred |
| Build/lint/what-if/budget entry | Existing workflow wiring inspected; all four changed Bicep sources independently build/lint; bounded local tests pass; explicit alert-only budget filters hub/namespace/two PE IDs | Live what-if and full gate deliberately not run; shared DNS/workspace charges stay aggregate. No hosted approval, hard cap enforcement or issue closure inferred |

## Plan Follow-Up Assessment

| Follow-up item | Why outside immediate scope | Owner or next action | Assessment and route |
| --- | --- | --- | --- |
| Actual what-if, propagation, transport and budget headroom | Owner expressly authorizes source authoring/local tests only | Later owner-authorized infrastructure operator: verify prices/currency/quota/headroom, guarded what-if, bootstrap, effective RBAC then explicit activation; preserve true thereafter | Open distinct live-infrastructure follow-up, not a source defect or active-plan task |
| OD-43 inventory, lawful basis/DPIA, retention, calibration and operational review | Real FR-048 use requires named human decisions absent from this exercise | Assets, Building Safety, DPO and data owners with Digital input, per BRD OD-43 | Open distinct governance follow-up; no operational approval fabricated |
| Consumer and device provisioning | #110 and #185 explicitly excluded | Respective work-item owners validate SDK transport and controlled individual enrolment separately | Open dependency/follow-up, not local acceptance evidence |

## Findings

<!-- rpi:review id=RV-001 -->
### RV-001 [Medium]: HTTPS management endpoint port leaks into the consumer hostname contract

* Related scope: P01-T01 nonsecret outputs and routing endpoint; P02-T01 compiled contracts; issue keyless API-consumer criterion.
* Evidence: infra/modules/iothub.bicep:256 strips `https://` and `/` from serviceBusEndpoint but does not remove an HTTPS port. infra/main.bicep:611 forwards that value as iotHubEventHubNamespaceFqdn. infra/tests/test_iothub_module.py:55 supplies only a portless serviceBusEndpoint; its main-output test checks existence rather than the evaluated host. The same property is converted to an sb URI at infra/modules/iothub.bicep:119.
* Independent reproduction: Evaluating the actual compiled output with synthetic `https://eh-fixture.servicebus.windows.net:443/` produces `eh-fixture.servicebus.windows.net:443`, not a fully qualified hostname. The active endpoint evaluates to `sb://eh-fixture.servicebus.windows.net:443/`, also inheriting the HTTPS management port.
* Official evidence checked 2026-10-27: Microsoft's REST reference for the exact Event Hubs namespace API version 2024-01-01, https://learn.microsoft.com/en-us/rest/api/eventhub/namespaces/get?view=rest-eventhub-2024-01-01, Sample response, documents serviceBusEndpoint with explicit `:443`. The Python EventHubConsumerClient constructor reference, https://learn.microsoft.com/en-us/python/api/azure-eventhub/azure.eventhub.eventhubconsumerclient?view=azure-python, defines fully_qualified_namespace as the host in `<yournamespace>.servicebus.windows.net` form. These are public-document reads, not Azure subscription/API execution.
* Impact: The documented future #110 consumer receives a host-and-port string instead of the promised SDK hostname when the provider includes its documented port. Local tests falsely accept only the simpler shape. Carrying the management HTTPS port into the sb endpoint is a related unverified transport assumption, not proof of actual Azure routing failure. No runtime failure or actual provider response was observed.
* Destination: rpi-implement, later work under the accepted architecture.
* Smallest useful next action: Normalize the provider URI to a hostname before exporting it; construct the routing endpoint from that normalized host with the intended protocol rather than copying the HTTPS port. Add compiled-expression regression assertions for documented port-bearing and portless forms, covering the module output, main forwarding and active endpoint while retaining false-state omission. Validate locally without deployment, then preserve this Review's original result; no second Review is required.

## Defects

* RV-001 Medium: Endpoint/hostname normalization and corresponding compiled-fixture gap; route to later rpi-implement. No fix applied in Review.

## Routed Findings

| Finding | Destination | Owner or next action | Reason for route |
| --- | --- | --- | --- |
| RV-001 Medium | rpi-implement | Later implementation owner normalizes hostname/routing URI and adds port-bearing regression coverage | Concrete source contract defect within already accepted architecture, not a new decision or deferred live acceptance requirement |

Later implementation of this finding does not require another Review. There is one complete finding set: 0 Critical, 0 High, 1 Medium, 0 Low.

## Residual Work

* Distinct live infrastructure and OD-43 governance follow-ups above remain open.
* Activated-hub parameter preservation and separately scoped historical-resource/role reconciliation remain operator responsibilities. Incremental deployment does not delete old assignments or erase historical diagnostics.
* Source-only local checks cannot prove effective propagation, consumer SDK transport, private networking, actual spend/headroom, device provisioning or operational acceptance.

## Blockers and Remaining Work

* Review blockers: None; credible complete source review performed.
* Source acceptance blocker: RV-001 affects the promised consumer connection contract.
* Remaining active implementation markers: None in supplied plan. Passing task markers denote execution, not defect-free outcome.
* Publication: User separately authorized parent commit/push/PR with Refs #140; this reviewer neither publishes nor interprets authorization as defect resolution, full-gate success or whole-issue closure. Parent must retain this result and disclose it in any permitted draft/publication, subject to applicable publication safeguards.

## Validation Evidence

| Command or evidence | Scope | Status | Summary |
| --- | --- | --- | --- |
| az bicep build --file <source> --stdout; az bicep lint --file <source> | infra/main.bicep; infra/modules/iothub.bicep; infra/modules/guard.bicep; infra/modules/iothub-scope-guard.bicep | Passed independently | Four builds/four lints, exit zero, no diagnostic output; compiled stdout discarded |
| REQUIRE_AZ_BICEP=1 <approved-venv-python> -m unittest discover -s infra/tests -p test_iothub_module.py -q | Twelve compiled IoT and mutation methods | Passed independently | 12 tests, 7.822 seconds, no skips |
| PYTHONDONTWRITEBYTECODE=1 REQUIRE_AZ_BICEP=1 PYTHONPATH=infra/tests <approved-venv-python> with explicit unittest selection | Nine relevant BicepPolicyTests plus complete test_identity_rbac and test_edge_module modules | Passed independently | 28 tests, 7.680 seconds, no skips; no lint-fixture tests creating temporary files selected |
| Explicit policy method selection | Guard graph; private endpoints; disconnected-endpoint mutations; named unsupported combinations; demo guard matrix; preserved private dependencies; no keys; production access; key-auth mutations | Passed independently | test_every_deployed_resource_waits_for_the_guard; test_each_data_service_has_a_private_endpoint; test_mutations_reject_missing_or_disconnected_private_endpoints; test_unsupported_parameter_combinations_are_rejected_with_a_named_check; test_demo_guard_matrix_including_environment_only_staging; test_demo_preserves_private_backing_services_names_and_identity_inputs; test_no_keys_or_sql_logins; test_production_profile_has_no_public_access; test_mutations_reject_key_auth_and_key_functions |
| Read-only compiled output/route evaluation with serviceBusEndpoint=https://eh-fixture.servicebus.windows.net:443/ | Real compiled expressions, synthetic namespace response | Defect reproduced | Output retains :443; route converts to sb while retaining :443; RV-001 |
| git diff --check | Complete current tracked diff | Passed independently | No whitespace errors |
| Complete infra discovery, REQUIRE_AZ_BICEP=1 | Existing full infra suite | Passed, implementation-reported | Changes record: 459 tests in 109.822 seconds, zero skips; not independently rerun because bounded checks cover this review |
| Scoped ruff check/format | test_iothub_module.py; test_bicep_policy.py | Passed, implementation-reported | Changes record preserves exact selectors/version; not independently rerun |
| Initial implementation failures | Compiler suffix, compiled fixtures, missing distributions/ruff, PEP668 and one primary-region fixture | Failed then corrected, implementation-reported | Preserved in original changes record; no failure history erased |
| Public Microsoft documentation retrieval | Namespace response shape, SDK constructor contract and existing managed-identity guidance | Retrieved independently | Bounded official-document reads only; no subscription, resource, token or credential access |
| Live what-if/deployment/propagation/transport/cost checks; full RPI gate | Azure/runtime/publication acceptance | Skipped by explicit scope | Not authorized; not converted into pass or approval. Mocked post-deployment messages in implementation's suite are fixture output only |

The approved interpreter was /home/azureuser/.copilot/session-state/d4520b64-77a4-482b-9cbf-b7786011af2e/files/iot-venv/bin/python. No dependency installation was performed by Review.

## Outcome

* Outcome: Not accepted.
* Outcome rationale: Review execution is complete, and most authored requirements plus both critique corrections are supported. RV-001 is a material defect in the central keyless-consumer hostname handoff, reproduced without live access. Passing local suites do not cover the documented provider response shape. Deferred live and human gates remain deliberate residual work, not additional defects and not approvals.

## Closeout Routing Record

| Finding class | Destination | Owner or next action |
| --- | --- | --- |
| Implementation defect | rpi-implement | Later implementation owner resolves RV-001 with hostname normalization and compiled regressions |
| Decision gap or invalid assumption | None | No new owner architecture choice needed |
| Material evidence gap | None requiring rpi-research | Documented source defect established; live evidence belongs to explicitly deferred authorized execution |
| Non-blocking residual work | Distinct live-infrastructure, #110/#185 and OD-43 follow-ups | Respective infrastructure/application/device owners and Assets/Building Safety/DPO/data owners |

* Execution status: Complete.
* Outcome: Not accepted.
* Validation coverage: 40 independent bounded tests, four independent builds/lints and whitespace checks passed; one additional compiled probe reproduced RV-001. Full 459-test suite and ruff are reported implementation evidence only.
* Blockers: RV-001 blocks defect-free source acceptance. Live/human/publication gates remain separate; no source or other canonical artifact was modified.

| Artifact | Description |
| --- | --- |
| .copilot-tracking/research/2026-10-27/iot-hub-bicep-module-research.md | Supplied dated research and selected bootstrap architecture |
| .copilot-tracking/plans/2026-10-27/iot-hub-bicep-module-plan.md | Current completed authoring plan and follow-ups |
| .copilot-tracking/details/2026-10-27/iot-hub-bicep-module-phase-details.md | Implementation and validation obligations |
| .copilot-tracking/reviews/plans/2026-10-27/iot-hub-bicep-module-plan-critique.md | Original Complete / Revise critique, preserved |
| .copilot-tracking/changes/2026-10-27/iot-hub-bicep-module-changes.md | Implementation evidence, failures/corrections and live limitations |
| .copilot-tracking/reviews/logs/2026-10-27/iot-hub-bicep-module-review.md | This single independent Review and complete finding set |

## Next Steps

Return this original Complete / Not accepted result to the active parent. Route RV-001 to later rpi-implement work; do not fix, rerun Review, silently approve the candidate or claim #140 closure. Parent owns any separately authorized continuation/publication and must check the recorded source boundary for drift. Live work still requires its own owner authorization; no user action is required by this reviewer.

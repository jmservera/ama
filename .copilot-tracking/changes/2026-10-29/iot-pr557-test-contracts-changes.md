---
title: PR 557 IoT test contracts implementation evidence
description: Test-only changes, validation and independent-review handoff
ms.date: 2026-10-29
---
<!-- markdownlint-disable-file -->

## Context and Scope

Task pr557-test-contracts-2026-10-29 / iot-pr557-test-contracts.
Full plan: .copilot-tracking/plans/2026-10-29/iot-pr557-test-contracts-plan.md.
Details: .copilot-tracking/details/2026-10-29/iot-pr557-test-contracts-phase-details.md.
Source edits limited to infra/tests/test_iothub_module.py. No Azure service calls,
pushes, scorecard edits or production changes.

## Planning and Critique

Research executed / Ready. Exactly one independent critique executed, original
verdict Revise, PC-001 Medium. Directly resolved in plan/details P02-T02: unresolved
acceptance-blocking Review findings prohibit successful delivery. No new critique.

## P01: Live Test Contracts

P01-T01 implemented: one build-params test asserts return code, parsed referenced
template equality against self.live and exact four-entry approved parameter map.
P01-T02 implemented: existing positive test calls a narrow full-name assertion,
evaluating to fixture/events/api-consumer. A single mutation test rejects a
wrong-hub expression retaining the approved suffix and a wrong-group expression
under the fixture hub. Change budget: two added methods and one helper, no removals.

## P02-T01: Validation

Compiler probe: local az bicep build-params succeeded and emitted both templateJson
and parametersJson. System Python lacks Ruff. pip --user installation was refused
by the externally-managed-environment protection; no override was used. Restored
Ruff 0.17.3 in an isolated session venv outside the repository. This is a local
validation-tool adjustment, not a plan divergence or dependency-manifest change.
Post-edit validation complete:

| Command | Working directory | Result |
| --- | --- | --- |
| python3 -m unittest discover -s tests -p 'test_iothub*' | infra | PASS, 22 tests, 12.688s, zero skips |
| PYTHONPATH=tests python3 -m unittest test_bicep_policy.BicepPolicyTests.test_parameter_examples_keep_api_scaled_to_zero test_bicep_policy.BicepPolicyTests.test_committed_environment_parameters_compile_and_match_the_contract | infra | PASS, 2 tests, 33.514s, zero skips |
| /home/azureuser/.copilot/session-state/c896dec6-ba50-4c06-bf6c-92fe304ac756/files/ruff-venv/bin/ruff check infra/tests/test_iothub_module.py | root | PASS, Ruff 0.17.3 |
| git diff --check | root | PASS |

Only test source changed: 49 additions, 2 replaced lines in the intended file.
No Bicep or parameter source modification. Two regression mutations ran as
subtests in the IoT suite, through the same assertion as the positive test.

## Amendments and Divergences

None. Semantic compiled-template comparison is an explicit planned choice.

## Review Handoff and Remaining Work

P01 and P02-T01 complete. Plan markers, phase details, changes evidence, handoff,
validation state and remaining work reconciled. Ready for one independent
post-implementation Review and local commit in P02-T02. No blockers or follow-up
work identified. Publication gate, hosted
checks and human approval are unperformed and unclaimed; push is prohibited.

## P02-T02: Independent Review Disposition

Exactly one Review executed, execution Complete, outcome Conformant, no RV
findings or acceptance blockers. Original Review is preserved at
.copilot-tracking/reviews/logs/2026-10-29/iot-pr557-test-contracts-review.md.
It independently reran 22 IoT tests (12.452s), 2 parameter tests (36.240s),
zero skips, touched-file Ruff and diff check, all passing.
No finding needs routing and no second Review is planned.

Reviewed test-file Git blob is 60ed4c4d30dfe1caf70a99186a1e4d03faa078bf.
Subsequent source identity check matches. The review noted stale historical
critique-pending prose in the plan's context paragraph; parent reconciled it
to the existing explicit disposition, with no source or acceptance change.
Local commit and verification remain; task is not yet reported complete.

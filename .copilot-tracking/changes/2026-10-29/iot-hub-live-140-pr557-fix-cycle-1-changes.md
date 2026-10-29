---
title: IoT Hub PR 557 fix cycle 1 changes
ms.date: 2026-10-29
---

## Metadata

* Task ID: 140-184-pr557-fix-cycle-1
* Task slug: iot-hub-live-140-pr557-fix-cycle-1
* Plan: .copilot-tracking/plans/2026-10-29/iot-hub-live-140-pr557-fix-cycle-1-plan.md
* Details: .copilot-tracking/details/2026-10-29/iot-hub-live-140-pr557-fix-cycle-1-phase-details.md
* Implementation date: 2026-10-29

## Execution Status

Active, full-plan invocation. P01/P01-T01/P01-T02/P02-T01 complete after executed research Ready and exactly one independent critique Complete / Pass. Remaining: P02/P02-T02 original Review and post-Review local lifecycle only.

## Approved Boundary

Only infra/tests/test_iothub_module.py and src/api/README.md source changes plus this cycle's dated artifacts. No Bicep/runtime changes, dependencies, Azure, secrets, scores or push. Use /tmp/mv and caller PYTHONPATH. Source edits precede coherent validation batch.

## Completed Work

### Compiled live scope coverage (P01-T01)

Added assert_live_scope_guards plus two test methods to infra/tests/test_iothub_module.py. Five group/requested/actual fixtures independently evaluate both outputs, check both minLength=1 schemas and guard dependencies. Thirteen deep-copy mutations cover each constant success, each input removal, each zero/missing constraint, either location clause, AND-to-OR and either child dependency. Helpers propagate assertions directly, following existing mutation-test conventions. Bicep is unchanged.

### Explicit bounded operator guidance (P01-T02)

Added required RunBudget max_messages=2/max_per_second=1.0/max_seconds=60.0 settings and required owner/cost/alert references beside DeviceActivation. Documentation rejects default100/larger limits for this exercise and assigns UTC cutoff/window checks to the operator, stopping before 2026-11-01T00:00:00Z. Manual comparison against RunBudget/Pacer confirms no date enforcement is claimed.

## Implementation-Time Plan and Detail Updates

None. Offline compiled inspection confirms both group/location expressions return a conditional createObject('value', ...), which existing evaluate handles. Mutations will preserve this compiled shape or replace the entire input with a constant value object, matching existing prior art.

## Validation Record

| Command | Outcome |
| --- | --- |
| REQUIRE_AZ_BICEP=1 PYTHONDONTWRITEBYTECODE=1 /tmp/mv/bin/python -m unittest discover -s infra/tests -p test_iothub_module.py -q | PASS,18 tests,9.738s; includes five fixture cases and13 rejected mutations |
| /tmp/mv/bin/ruff check --isolated --select E,F,I,B,UP --target-version py312 --line-length 100 infra/tests/test_iothub_module.py | PASS |
| /tmp/mv/bin/ruff format --isolated --line-length 100 --check infra/tests/test_iothub_module.py | Initial FAIL on one wrap; ran formatter, subsequent PASS,1 file formatted |
| REQUIRE_AZ_BICEP=1 PYTHONDONTWRITEBYTECODE=1 /tmp/mv/bin/python -m unittest discover -s infra/tests -q | PASS,470 tests,111.568s, no skips; offline compilation/fake cloud adapters only |
| cd src/api && /tmp/mv/bin/ruff check . && /tmp/mv/bin/ruff format --check . | PASS,59 files already formatted |
| From src/api: PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src:tests:../core/src:../agents/src:../core/tests:../agents/tests /tmp/mv/bin/python -m unittest test_iot_stream test_sensor_ingestion test_sensor_stream test_resident_sensors -q | PASS,94 tests,19.502s, no skips |
| git diff --check; score-path diff | PASS; .github/rubric/scores/latest.json unchanged |

No Azure command other than offline az bicep build invoked. No credential/private-data access. Existing fixture test stdout includes expected denial/invalid-argument messages; unittest result is OK.

## Pre-Review Reconciliation

Plan/source markers and details are current; P01 and P02-T01 complete with matching evidence. Ready for the one original independent Review of these two local findings. P02-T02 remains explicitly unchecked for that Review, local commit and full-gate attempt; no implementation work is presented as pending. Historical parent live/publication findings remain separate.

## Blockers

None for implementation. Parent live/publication blockers remain outside this cycle.

## Remaining Work

P02-T02 local commit and external gate attempt. Original independent Review is complete; no remaining source edit or required focused check.

## Follow-Up Items

Historical live and full-gate blockers remain owned by parent task; no new work inferred.

## Original Review and Local Lifecycle

Exactly one independent Review executed Complete / Residual work. Both source corrections are conformant, no source defects found. Independent reviewer reran18 compiled tests in9.264s and diff hygiene; supplied full470/unit94/Ruff evidence remained distinguished. RV-001 Low retains local lifecycle and RV-002 Low retains historical parent blockers; neither routes source changes or a repeated Review. Original verdict and artifact are preserved unchanged.

Fetched origin/main for the external gate: 356a3cfbaa2cd63a6fbf80e87e11a29cacaaf4c7. No shared lock holder appeared in lslocks at preflight. gh api user returned id8036360/login jmservera; local author/committer email is 8036360+jmservera@users.noreply.github.com. The next local commit includes implementation and all original RPI evidence with the required Copilot trailer; no push.

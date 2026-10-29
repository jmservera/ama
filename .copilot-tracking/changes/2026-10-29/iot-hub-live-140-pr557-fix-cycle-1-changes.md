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

Complete for the local-only full-plan invocation: all P01/P02 task markers executed. Both source findings addressed, required focused checks passed, one critique and one original Review preserved, implementation/evidence committed and complete local gate attempted. Publication is blocked by the adverse gate; Complete does not imply full-gate/issue/live acceptance.

## Approved Boundary

Only infra/tests/test_iothub_module.py and src/api/README.md source changes plus this cycle's dated artifacts. No Bicep/runtime changes, dependencies, Azure, secrets, scores or push. Use /tmp/mv and caller PYTHONPATH. Source edits precede coherent validation batch.

## Completed Work

### Compiled live scope coverage (P01-T01)

Added assert_live_scope_guards plus two test methods to infra/tests/test_iothub_module.py. Five group/requested/actual fixtures independently evaluate both outputs, check both minLength=1 schemas and guard dependencies. Thirteen deep-copy mutations cover each constant success, each input removal, each zero/missing constraint, either location clause, AND-to-OR and either child dependency. Helpers propagate assertions directly, following existing mutation-test conventions. Bicep is unchanged.

### Explicit bounded operator guidance (P01-T02)

Added required RunBudget max_messages=2/max_per_second=1.0/max_seconds=60.0 settings and required owner/cost/alert references beside DeviceActivation. Documentation rejects default100/larger limits for this exercise and assigns UTC cutoff/window checks to the operator, stopping before 2026-11-01T00:00:00Z. Manual comparison against RunBudget/Pacer confirms no date enforcement is claimed.

## Implementation-Time Plan and Detail Updates

No source-design amendment or material divergence. Offline compiled inspection confirmed both group/location expressions return a conditional createObject('value', ...), which existing evaluate handles. Mutations preserve this compiled shape or replace the entire input with a constant value object, matching existing prior art. Lifecycle status updated after consuming the original Review and gate result; original verdicts remain unchanged.

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

At Review intake, plan/source markers and details were current with P01/P02-T01 complete and P02-T02 honestly pending Review/local lifecycle. Original Review was then executed once. Post-Review parent reconciliation now marks P02-T02 complete for the required local commit and gate attempt, not gate success. No source change, closure Review or second critique occurred. Historical parent live/publication findings remain separate.

## Blockers

None for the two local source corrections. Publication blocked: current checkout has ignored cache/install inputs, and the clean exact-commit full gate fails API required-integration skip admission, blocking browser/MSSQL groups. Preserve both outcomes, no policy relaxation or cloud fallback. Parent registry/transport/SQL/resident-gauge approval and acceptance blockers remain outside this cycle.

## Remaining Work

No remaining active-plan source or local-lifecycle task. Future publication requires a separate gate-admission correction and fresh complete exact-head receipt; no publication is requested or performed.

## Follow-Up Items

Historical live and full-gate blockers remain owned by parent task; no new work inferred.

The current full-gate reproduction confirms the inherited API discovery/admission follow-up remains necessary. Owner: gate/tooling workstream, preserve required integration policy and original adverse receipts. Local evidence bookkeeping changes invalidate earlier receipt identities and cannot inherit their eligibility.

## Original Review and Local Lifecycle

Exactly one independent Review executed Complete / Residual work. Both source corrections are conformant, no source defects found. Independent reviewer reran18 compiled tests in9.264s and diff hygiene; supplied full470/unit94/Ruff evidence remained distinguished. RV-001 Low retains local lifecycle and RV-002 Low retains historical parent blockers; neither routes source changes or a repeated Review. Original verdict and artifact are preserved unchanged.

Fetched origin/main for the external gate: 356a3cfbaa2cd63a6fbf80e87e11a29cacaaf4c7. No shared lock holder appeared in lslocks at preflight. gh api user returned id8036360/login jmservera; local author/committer email is 8036360+jmservera@users.noreply.github.com. The next local commit includes implementation and all original RPI evidence with the required Copilot trailer; no push.

### Committed source and complete local gate (P02-T02)

Implementation and original RPI evidence committed as dd69200ba54e077bb5d1119977f63cff2e75e87f. Author/committer use the derived noreply identity, required Copilot trailer present. Committed two-file diff SHA256 is 3e5d39485e4414c188bb8235248a56eaadba1055ed2aee34bbc5af9c1e4d0d31, identical to the independent Review boundary; scores unchanged. No push.

First command from the working checkout:

```bash
PYTHONDONTWRITEBYTECODE=1 /tmp/mv/bin/python tools/rpi-checks.py --all --jobs 3 --lock-timeout 0 --base 356a3cfbaa2cd63a6fbf80e87e11a29cacaaf4c7 --out /home/azureuser/.copilot/session-state/f212780b-b61f-40a3-aaea-96edfdb33a23/files/iot-pr557-fix-cycle-1-dd69200b-gate
```

Exit1: candidate has ignored inputs; no receipt/output directory was produced. Filename-only inspection found Ruff/mypy/bytecode caches and editable-install metadata. Did not read private data or delete/move unknown inputs. Retried from a new detached worktree at the exact implementation commit, with separate new external output.

```bash
git worktree add --detach /home/azureuser/.copilot/session-state/f212780b-b61f-40a3-aaea-96edfdb33a23/files/iot-pr557-fix-cycle-1-clean-dd69200b dd69200ba54e077bb5d1119977f63cff2e75e87f
cd /home/azureuser/.copilot/session-state/f212780b-b61f-40a3-aaea-96edfdb33a23/files/iot-pr557-fix-cycle-1-clean-dd69200b
PYTHONDONTWRITEBYTECODE=1 /tmp/mv/bin/python tools/rpi-checks.py --all --jobs 3 --lock-timeout 0 --base 356a3cfbaa2cd63a6fbf80e87e11a29cacaaf4c7 --out /home/azureuser/.copilot/session-state/f212780b-b61f-40a3-aaea-96edfdb33a23/files/iot-pr557-fix-cycle-1-dd69200b-clean-gate
```

Full gate exit1, external receipt status failed, scope full. Shared lock acquired immediately; runner bounded actual workers to2. API discovery ran1338 tests in557.477s, exit0/skipped318, then failed admission of required SQL/browser integration skips. Browser and MSSQL groups were blocked by that prerequisite, not executed or accepted.

Successful groups: preflight, core, agents, orchestrator, importer, namespace, static, infra, migration, all four image/security/SBOM groups and logo-0600. These successes do not upgrade the failed overall receipt. No Azure resource operation or real model call.

Authoritative historical receipt:
/home/azureuser/.copilot/session-state/f212780b-b61f-40a3-aaea-96edfdb33a23/files/iot-pr557-fix-cycle-1-dd69200b-clean-gate/receipt.json.
External logs, environments, images and exact-commit wrapper worktree are retained for adverse-evidence inspection, not temporary cleanup targets.

Fetched main again, unchanged at356a3cfb. From the clean wrapper, ran:

```bash
PYTHONDONTWRITEBYTECODE=1 /tmp/mv/bin/python tools/rpi-checks.py --verify-receipt /home/azureuser/.copilot/session-state/f212780b-b61f-40a3-aaea-96edfdb33a23/files/iot-pr557-fix-cycle-1-dd69200b-clean-gate/receipt.json --base 356a3cfbaa2cd63a6fbf80e87e11a29cacaaf4c7
```

Exit1: receipt does not establish an eligible run. No bypass or repeated Review. Final local evidence reconciliation records the failure without changing reviewed source; its later commit invalidates the historical receipt's head binding. There is deliberately no final-head publication-pass claim. A new complete exact-head gate and independent exact-head assessment remain required before any future publication; no push is authorized.

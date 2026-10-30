---
title: IoT Hub PR 557 fix cycle 1 phase details
ms.date: 2026-10-29
---

## Metadata

Task ID: 140-184-pr557-fix-cycle-1. Task slug: iot-hub-live-140-pr557-fix-cycle-1.
Plan: .copilot-tracking/plans/2026-10-29/iot-hub-live-140-pr557-fix-cycle-1-plan.md.
Research: .copilot-tracking/research/2026-10-29/iot-hub-live-140-pr557-fix-cycle-1-research.md, C1-C8.

## Phase Index

| Phase | Status | Tasks |
| --- | --- | --- |
| P01 | Complete and validated | P01-T01, P01-T02 |
| P02 | Local tasks complete; publication gate failed | P02-T01, P02-T02 |

<!-- rpi:phase id=P01 -->
## P01: Address both bounded review findings

Context: live Bicep is already correct. Existing tests inspect SKU/units/dependencies but do not evaluate group or actual location. Changes are source-local, no Azure or secrets.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Add live-scope behavioral and mutation tests

Use module(template, "iot-live-scope-guard"), evaluate and unguarded_resources. Assert presence of both input and nested schema entries before access so removed-input mutations fail clearly. Assert minLength exactly1. Independent fixtures provide resourceGroup().name and reference(...).location; override requested location through existing values().

Require cases ama/uksouth/uksouth, other/uksouth/uksouth, ama/westus/westus, ama/uksouth/westus and ama/westus/uksouth. Verify each guard result against its independent predicate, not a single combined acceptance. Mutate compiled deep copies only: constant-ok group/location, requested-clause removal, actual-clause removal, AND-to-OR, removed inputs, zero/missing minLength on both constraints, and each child dependency. Reuse assertion and assertRaises(AssertionError). The mutations must actually change the compiled expression/object.

Completion: two new methods and one helper at most; targeted test suite passes and each enumerated mutation is rejected. No Bicep edit needed.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Document budget and cutoff

Place guidance directly after DeviceActivation paragraph. Name explicit RunBudget settings and required owner/cost/alert references. State defaults/larger supported limits are not exercise approval. Before each run operator verifies UTC cutoff and enough remaining time, stops before 2026-11-01T00:00:00Z (through 31 October UTC). RunBudget does not enforce that date. Preserve existing registry/routed receiver and credential approval warnings.

Completion: all four requested bounds visibly stated and manually checked against RunBudget/Pacer. No runtime policy change or claims of live authority.

<!-- rpi:phase id=P02 -->
## P02: Validate and preserve local handoff

<!-- rpi:task id=P02-T01 -->
### P02-T01: Run checks

First /tmp/mv/bin/python -m unittest discover -s infra/tests -p test_iothub_module.py -q with REQUIRE_AZ_BICEP=1, then full infra discover. Run /tmp/mv/bin/ruff check --isolated --select E,F,I,B,UP --target-version py312 --line-length 100 infra/tests/test_iothub_module.py and ruff format --isolated --line-length 100 --check on that file. From src/api, /tmp/mv/bin/ruff check . and ruff format --check .; PYTHONPATH=src:tests:../core/src:../agents/src:../core/tests:../agents/tests /tmp/mv/bin/python -m unittest test_iot_stream test_sensor_ingestion test_sensor_stream test_resident_sensors -q. Dependencies are not installed unless a command first fails from missing tools/packages.

Completion: exact commands/counts/outcomes recorded in changes; no accepted skipped guard compilation.

Observed: targeted IoT18 tests pass; full infra470 tests pass with REQUIRE_AZ_BICEP=1; API/core relevant94 tests pass. Infra/API Ruff check and format check pass. First infra format check identified one wrap; repository formatter corrected it before the complete infra run.

<!-- rpi:task id=P02-T02 -->
### P02-T02: Review and local lifecycle

Reconcile plan markers, details and changes before invoking Review once. Preserve all original review findings; route later work rather than repeat Review. Local commit includes implementation and dated original evidence, uses gh api user derived noreply identity and required trailer. Attempt complete local gate after commit with fetched main, new external output and --lock-timeout0; busy foreign lock/prerequisites block publication, not authority to terminate a foreign process or bypass checks. No push even on success.

Completion: local commit persistent; external gate evidence retained and accurately qualified. Human/hosted/live approval remain separate.

Observed: original independent Review Complete / Residual work, no source defects. Implementation and original evidence committed as dd69200b with noreply author/committer and required trailer. Initial full-gate admission refused existing ignored cache/install inputs; preserved them and used a clean detached exact-commit worktree rather than delete/move unknown files. Complete --all run executed, failed required SQL/browser skip admission in API discovery (1338 tests,318 skips); browser/MSSQL groups blocked. External receipt verification correctly refused eligibility. Final evidence commit is local-only bookkeeping and invalidates prior receipt identity; no valid exact-final-head publication gate or repeated Review is claimed.

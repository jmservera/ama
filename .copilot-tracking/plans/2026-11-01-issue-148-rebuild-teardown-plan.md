# Plan: issue 148 rebuild and teardown automation (2026-11-01)

Research: [research](../research/2026-11-01-issue-148-rebuild-teardown-research.md)

## Phases

* [ ] 1. `src/orchestrator/src/zava_forward/orchestrator/rebuild_azure.py`: `AzureConfig`, secret-argv guard, synthetic guard, `AzureBackend` (inventory, budgets, delete+wait, per-stage perform/verify), live runners `run_rebuild`/`run_teardown`, plan printer.
* [ ] 2. CLI in the module: `plan` (default, no I/O), `rebuild --apply`, `teardown --apply`; resource group fixed to `ama`; `--from-stage` resume; exit 2 on operator-gated stages.
* [ ] 3. `src/orchestrator/tests/test_rebuild_azure.py` with a recording fake runner (disposable environment): ordering, dry-run no calls, no secret argv, synthetic guard, budgets last, empty inventory verified, drift stops.
* [ ] 4. Update `infra/README.md` rebuild section and orchestrator README; knowledge log not required (no KB change).
* [ ] 5. Validate: unittest, ruff check, ruff format --check, mypy for orchestrator.

## Critique (single pass, compatible findings applied)

* Do not fake unscriptable probes (workload SQL, model checks): mark operator-gated and stop.
* Never delete the group, locks, or retained resources; reuse `canonical` fail-closed checks.
* Secrets only via environment of a child process, never argv; token read in memory.

## Acceptance mapping

AC1, AC2, AC3 proven by unit evidence; AC4 dry-run proven, disposable Azure test not run, so PR uses Refs.

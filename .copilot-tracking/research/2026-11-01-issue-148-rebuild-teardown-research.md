# Research: issue 148 rebuild and teardown automation (2026-11-01)

Disposition: executed. Planning Readiness: Ready.

## Evidence

* `infra/README.md` "From-empty rebuild observed on 2026-10-12": manual 7-step sequence and dependency-ordered deletion; budgets are listed separately via `Microsoft.Consumption/budgets`.
* `src/orchestrator/src/zava_forward/orchestrator/rebuild.py`: existing ordered `STAGES`, `ORDER`, `canonical`, `teardown`, `rebuild` and a `Backend` protocol, with only a synthetic SQLite backend and no Azure adapter (README states "no cloud adapter or `--apply`").
* Existing helpers to reuse (argv only): `infra/scripts/deploy.py` (what-if default, `--apply`, `--parameter`), `create-sql-users.py`, `setup-entra.py --check`, `initialize-workbench-staff.py --check/--apply --restart`, `src/core` `open_store` (first-start seeding), `az acr build -f src/api/Dockerfile src`.
* Dependency rule: orchestrator may import only `orchestrator` and `core`; stdlib subprocess/urllib are fine.
* Infra CI runs `python -m unittest discover -s infra/tests`; orchestrator tests run from `src/orchestrator/tests`.

## Gap against acceptance criteria

1. Scripted rebuild with checks and no secret on argv: missing (only simulation).
2. Teardown in dependency order incl. budgets with empty-inventory verification: logic exists; no Azure inventory/delete adapter.
3. Seeding and staff reconciliation with synthetic data only: stages named, no executor or synthetic guard.
4. Dry-run plus test in a disposable environment: dry-run exists only for contracts; no live-adapter tests.

## Decision

Add `rebuild_azure.py` in the orchestrator package: an injectable-runner Azure adapter implementing the existing `Backend` protocol, argv-only with a secret-argv guard, a synthetic-data guard for seed/roster, dry-run default, explicit `--apply`, and operator-gated stages that stop (exit 2) instead of being faked. Tests use a recording fake runner as the disposable environment. A real disposable Azure run is not authorised here, so AC4 is only partially proven.

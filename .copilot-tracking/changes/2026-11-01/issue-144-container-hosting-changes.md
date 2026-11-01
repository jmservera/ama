# Changes: issue 144 container hosting slice (2026-11-01)

Plan: [plan](../../plans/2026-11-01/issue-144-container-hosting-plan.md)

## Added

* `src/api/tests/scale_load.py`: in-process API load harness over a 60,000-home fictional SQL store; reports declared versus executed workload, cold and warm latency, NFR-002 observations and cost drivers per unit of load (cost Unknown).
* `src/api/tests/test_scale_load.py`, `src/api/tests/test_restart_audit.py`: harness report contract and single-replica restart audit persistence.
* `docs/architecture/scale-load-2026-11-01.json`: recorded 120 s run (not the declared 1,800 s; 53,821 of 600,000 events).

## Changed

* `infra/modules/containerapps.bicep`: API Startup probe.
* `infra/tests/test_bicep_policy.py`: probes, limits, Single revision, queue and job scale contract.
* `infra/README.md`, `docs/reference/log.md`: status table, rollback by digest, load run, log entry.

## Divergences and remaining work

* Agents queue transport, API post-back, real orchestrator job: not built (cross-project). Hosted hardening: platform-blocked. Azure restore proof: not run.
* Validation: scale and restart tests, ledger tests, `test_bicep_policy` and `test_container_contract` (61 tests) pass; ruff check, ruff format --check and mypy clean on the new files. `test_bicep_policy.py` was already not ruff-format clean at baseline.

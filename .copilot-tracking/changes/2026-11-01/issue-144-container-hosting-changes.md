# Changes: issue 144 container hosting slice (2026-11-01)

Plan: [plan](../../plans/2026-11-01/issue-144-container-hosting-plan.md)

## Added

* `src/api/tests/scale_load.py`: in-process API load harness over a 60,000-home fictional SQL store; reports declared versus executed workload, cold and warm latency, NFR-002 observations and cost drivers per unit of load (cost Unknown).
* `src/api/tests/test_scale_load.py`, `src/api/tests/test_restart_audit.py`: harness report contract and single-replica restart audit persistence.
* `docs/architecture/scale-load-2026-11-01.json`: recorded 120 s run, re-recorded after review (not the declared 1,800 s; 53,821 of 600,000 events).

## Changed

* `infra/modules/containerapps.bicep`: API Startup probe.
* `infra/tests/test_bicep_policy.py`: probes, limits, Single revision, queue and job scale contract.
* `infra/README.md`, `docs/reference/log.md`: status table, rollback, load run, log entry.

## Amendments after PR review (2026-11-01)

* `scale_load.py`: fixture homes carry `is_synthetic` and a deterministic lifecycle and the run fails unless dashboard coverage includes every requested home; the response body is read inside the timed call; list offsets work for 1 to 50 homes; transport failures count as errors and worker exceptions propagate. `test_scale_load.py` covers a 10-home fixture and a transport failure.
* Re-recorded the 60,000-home run: warm p95 7,076 ms list, 7,512 ms detail, 7,698 ms dashboard, all above the NFR-002 thresholds; 708 MiB resident. README states this without a pass claim.
* `infra/README.md`: the rollback text no longer implies redeploying a previous run digest; it documents revert PR, manual CI and `src-deploy.yml` dispatch, since `pipeline.py` only accepts current-run digests. Fixed an E501 in `test_bicep_policy.py` that failed the src-namespace check.
* Plan validation now requires the complete local RPI gate before publication.

## Amendments after second PR review (2026-11-01)

* `scale_load.py`: sessions stop dispatching at the deadline after sleeping, latency is measured from the scheduled arrival so backlog delay is reported, server, socket and database cleanup run through an `ExitStack` on failure, and `meets_declared_workload` also requires the requested duration and the unrounded achieved request rate. `test_scale_load.py` covers cleanup on login failure and deadline and backlog behaviour. The recorded 60,000-home run is unchanged and not re-run; its latencies were measured from dispatch, so treat them as lower bounds.

## Amendments after third PR review (2026-11-01)

* `scale_load.py`: all sessions share one start timestamp and a fixed observation window; `meets_declared_workload` uses the configured window and in-window throughput with a 5% tolerance; drain time and in-window counts are reported separately. `infra/README.md` no longer calls the stored latencies an upper bound; they are dispatch-based lower bounds for backlog and not hosted evidence.

## Divergences and remaining work

* Agents queue transport, API post-back, real orchestrator job: not built (cross-project). Hosted hardening: platform-blocked. Azure restore proof: not run.
* Validation: scale and restart tests, ledger tests, `test_bicep_policy` and `test_container_contract` (61 tests) pass; ruff check, ruff format --check and mypy clean on the new files. `test_bicep_policy.py` was already not ruff-format clean at baseline.

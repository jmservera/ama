# Changes: issue 144 guard fix (2026-11-20)

Tier: FULL (security control in src). The complete local gate, external receipt and independent review are run by the coordinator; none was run here. Refs #144, nothing ticked, no push, no Azure write.

## Files

* `src/core/src/zava_forward/core/container_hardening.py`: `_drop_inheritable_capabilities` (capget/capset v3), injectable `drop_inheritable_fn`, `prepare_private_scratch`; zero-mask and sticky-bit checks unchanged.
* Twelve entrypoints (server, resident_demo, agents worker, orchestrator document_rescan, source_monitor, token_store, `__main__`, digest_blob, ranking_publish, importer, live_receiver, live_simulator) call `prepare_private_scratch` before the guard.
* `src/core/tests/test_container_hardening.py` (new, 8 tests).
* `infra/README.md`, `docs/reference/log.md`, `docs/reference/README.md`, `docs/reference/research/issue-144-live-hardening-fix-2026-11-20.md`.
* `infra/tests/test_container_hosting_144.py` unchanged: mount paths and env in Bicep are unchanged (the repoint happens at runtime).

## Validation run

* New core tests 8 pass; `infra/tests/test_container_hosting_144.py` 19 pass; orchestrator 143, importer 125, api live-path tests 112 pass.
* `src/check-container.py` passes for api, agents, orchestrator and importer built from this tree.
* Local Container Apps simulation (real capset giving CapInh 0xa80425fb with empty permitted set, tmpfs mode 0777): unprepared refused on scratch; prepared passes, CapInh 0 afterwards.
* ruff check per project and ruff format check on changed core files pass; mypy passes in orchestrator and importer; core, api and agents mypy report only existing opentelemetry import errors (package absent on host).
* Full core suite: 4131 tests, 35 failures and 22 errors, all in `test_device_registry_azure` (54), `test_telemetry` (2) and `test_discovery_assistant_demo` (1), none touching hardening; agents suite: 13 failures/errors all in `test_paired_report_command` subprocess evals. Attributed to host dependencies (Azure SDK, opentelemetry in subprocesses); not compared against a clean-base run, so this attribution is unverified.
* Not run: `rpi-checks.py` (coordinator), hosted CI, a live Container Apps replica.

## Per-criterion table (#144 unticked criteria)

| Criterion | Status | Basis |
| --- | --- | --- |
| Worker and job images real, versioned, deployed through the pipeline | Unproven | Not addressed; needs an owner-authorised Azure deployment |
| Container hardening enforced in the deployed app | Unproven | Guard defects fixed and simulated locally; deployed demo has `ZF_CONTAINER_HARDENING=off` (read-only Azure check); live replica Running and Healthy under `enforced` not captured, needs an owner-authorised Azure write |

Evidence note: `docs/reference/research/issue-144-live-hardening-fix-2026-11-20.md`.

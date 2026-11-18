<!-- markdownlint-disable-file -->
# RPI Phase Details: Issue #144 Container Hosting Completeness

## Metadata

* Task ID: issue-144
* Task slug: infra-144-container-load
* Related plan: .copilot-tracking/plans/2026-11-15/infra-144-container-load-plan.md
* Evidence sources: .copilot-tracking/research/2026-11-15/infra-144-container-load-research.md

## Phase Index

| Phase ID | Name                                                                        | Status | Detail sections          |
|----------|-----------------------------------------------------------------------------|--------|--------------------------|
| P01      | Implement in-process container hardening runtime and entrypoint wiring      | Ready  | P01, P01-T01, P01-T02    |
| P02      | Harden deployed Bicep workload specifications and pipeline image consistency | Ready  | P02, P02-T01, P02-T02    |
| P03      | Execute and record declared-scale load and single-replica restart benchmarks | Ready  | P03, P03-T01             |
| P04      | Author `test_container_hosting_144.py`, update docs, and run validation     | Ready  | P04, P04-T01, P04-T02    |

## Test Ownership and Coverage Lock

* Canonical new test module: `infra/tests/test_container_hosting_144.py` (maximum new test files: `1`; test removals: `none`).
* Existing regression suites retained unchanged or additively verified: `infra/tests/test_container_contract.py`, `infra/tests/test_container_hosting_completeness.py`, `infra/tests/test_bicep_policy.py`, `infra/tests/test_pipeline.py`, `infra/tests/test_deploy.py`, `infra/tests/test_resident_demo_deploy.py`, `src/api/tests/test_scale_fixture_load_and_restart.py`, `src/api/tests/test_restart_audit.py`, and `src/agents/tests/test_worker.py`.
* Generated/recorded evidence targets: `docs/architecture/scale-load-2026-11-15.json` and `docs/architecture/scale-restart-2026-11-15.json`.
* Semantic vs regression coverage:
  * Semantic: Compiled ARM/Bicep evaluation of deployed workload hardening settings and `EmptyDir` scratch volumes; live execution of `zava_forward.core.container_hardening` positive and negative probes (root UID/GID rejection, capability bit rejection, `NoNewPrivs=0` rejection, writable `/app` or `/` rejection, missing writable scratch rejection, subprocess entrypoint exit-code checks across `api`, `agents`, `orchestrator`, `importer`); `pipeline.py` `rank-publish` image mismatch rejection; live bounded scale load + separate-process `SIGKILL` restart + `/api/audit-check` chain continuity + worker crash redelivery.
  * Regression: Preserve `USER 10001:10001` without `ENTRYPOINT` (`test_container_contract.py`), `resident_showcase.py` `FORBIDDEN_ENV_PREFIXES` (`test_resident_demo_deploy.py`), `main.bicep` `orchestratorImage` empty fallback (`test_bicep_policy.py`), and `infra/README.md` rollback/scale wording (`test_container_hosting_completeness.py`).

<!-- rpi:phase id=P01 -->
## P01: Implement in-process container hardening runtime and entrypoint wiring

### Context

Research (`C10`, `C14`) showed that Azure Container Apps `Microsoft.App/containerApps@2025-07-01` and `Microsoft.App/jobs@2025-07-01` reject Kubernetes `securityContext` properties (`BCP037`), and `infra/tests/test_container_contract.py` forbids Docker `ENTRYPOINT` wrappers because asserting `ST_RDONLY` on `/` or `CapBnd == 0` breaks ACA's hypervisor guest. However, in both hardened Docker (`--read-only --cap-drop=ALL --security-opt=no-new-privileges`) and ACA (`USER 10001:10001`), the container runs as UID/GID `10001:10001` with `CapEff == CapPrm == CapInh == CapAmb == 0`, Linux `prctl(PR_SET_NO_NEW_PRIVS, 1)` succeeds unprivileged to enforce `NoNewPrivs: 1`, and `/` plus `/app` reject writes (`EROFS` or `EACCES`).

### Intent

Create a pure-stdlib runtime hardening guard in `zava_forward.core` and wire it into every deployed container and job entrypoint so hardening is actively enforced in deployed workloads rather than only in CI `docker run` tests.

### Boundaries

* Included: `src/core/src/zava_forward/core/container_hardening.py` and startup calls in `api`, `agents`, `orchestrator`, and `importer` entrypoints.
* Excluded: Modifying any `Dockerfile` `CMD`/`ENTRYPOINT` or adding third-party dependencies.

### Likely Targets

* `src/core/src/zava_forward/core/container_hardening.py`: New stdlib runtime hardening enforcement module.
* `src/api/src/zava_forward/api/server.py`: Call `enforce_from_env()` at the start of `main()`.
* `src/api/src/zava_forward/api/resident_demo/__main__.py`, `live_receiver.py`, `live_simulator.py`: Call `enforce_from_env()` in `main()`.
* `src/agents/src/zava_forward/agents/worker.py`: Call `enforce_from_env()` at the start of `main()`.
* `src/orchestrator/src/zava_forward/orchestrator/__main__.py`, `token_store.py`, `digest_blob.py`, `ranking_publish.py`, `source_monitor.py`, `document_rescan.py`: Call `enforce_from_env()` at startup.
* `src/importer/src/zava_forward/importer/__main__.py`: Call `enforce_from_env()` at the start of `main()`.

### Dependencies

* None.

### Validation Expectations

* Unit and subprocess tests verify that when `ZF_CONTAINER_HARDENING` is unset, existing developer runs are unaffected, and when `ZF_CONTAINER_HARDENING=enforced`, any violation fails closed before work begins while compliant `10001:10001` state passes cleanly.

### Completion Evidence

* Clean execution of `container_hardening` unit/subprocess checks and existing `core`, `agents`, `orchestrator`, `importer`, and `api` tests.

### Unresolved Items

* None.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Add stdlib `zava_forward.core.container_hardening` guard module

#### Context

All four packages (`api`, `agents`, `orchestrator`, `importer`) already depend on `zava_forward.core` (`C5`-`C7`), and `agents` forbids SQL/Azure SDK imports (`C6`). Placing the helper in `zava_forward.core.container_hardening` using only `ctypes`, `errno`, `os`, ` pathlib`, `sys`, and `tempfile` satisfies all package boundaries.

#### Intent

Implement `ContainerHardeningError(RuntimeError)`, `HardeningReport` dataclass, `enforce_container_hardening(...)`, and `enforce_from_env(env=None)` in `src/core/src/zava_forward/core/container_hardening.py`.

#### Boundaries

* Included:
  * Check `ZF_CONTAINER_HARDENING` mode (`""` / `"off"` -> inactive no-op when unset; `"enforced"` -> strict fail-closed enforcement; unknown non-empty value -> `ContainerHardeningError` so typos like `"true"` or `"disabled"` cannot silently bypass hardening!).
  * Enforce `uid == euid == expected_uid` (`10001`) and `gid == egid == expected_gid` (`10001`), never `0`.
  * Accept injectable `umask_fn`, `prctl_fn`, `status_text`, `uid_getter`, `euid_getter`, `gid_getter`, `egid_getter`, `immutable_paths`, and `writable_paths` hooks so in-process unit tests do not mutate the test runner's process-global `umask` or irreversibly set `NoNewPrivs=1` on the runner process (`PC-003`). In real execution, set `os.umask(0o077)` and verify `sys.dont_write_bytecode` or `env.get("PYTHONDONTWRITEBYTECODE") == "1"`.
  * On Linux (`sys.platform.startswith("linux")`), invoke `libc.prctl(PR_SET_NO_NEW_PRIVS, 1, 0, 0, 0)` (`PR_SET_NO_NEW_PRIVS = 38`) when available, then parse `/proc/self/status` and require `CapInh == 0`, `CapPrm == 0`, `CapEff == 0`, `CapAmb == 0`, and `NoNewPrivs == 1`.
  * Probe immutable directories (`immutable_paths`, defaulting to `(Path("/"), Path("/app"))`): attempt creating an unguessable probe file; require `OSError` with `errno in (errno.EROFS, errno.EACCES, errno.EPERM)`; if creation unexpectedly succeeds, unlink immediately and raise `ContainerHardeningError`.
  * Probe writable ephemeral directories (`writable_paths`, defaulting to `(Path(env.get("TMPDIR") or "/tmp"),)` plus `(Path(env["ZF_STATE"]),)` when `ZF_STATE` is set in `env`): verify each exists as a directory, accepts creating and unlinking a short probe file, and is not world-writable without sticky bit unless `/tmp`.
  * Satisfy `mypy --strict` (`src/core/pyproject.toml`) and `ruff` (`E`, `F`, `I`, `B`, `UP`, line length 100) (`PC-001`).
* Excluded: Asserting `ST_RDONLY` on `statvfs("/")` or `CapBnd == 0`, which would break Azure Container Apps startup (`C10`, `C14`).

#### Likely Targets

* `src/core/src/zava_forward/core/container_hardening.py`: Create module.

#### Dependencies

* None.

#### Validation Expectations

* Direct unit tests in `infra/tests/test_container_hosting_144.py` exercising compliant state and every negative mutation (unknown mode string, UID/GID 0 or mismatch, capability bit non-zero, `NoNewPrivs != 1`, bytecode enabled, `/` or `/app` accepting writes, `/tmp` or `/state` unwritable).

#### Completion Evidence

* `zava_forward.core.container_hardening` passes all positive/negative tests, `ruff`, and `mypy`-clean typing annotations.

#### Unresolved Items

* None.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Wire `enforce_from_env()` into all deployed container and job entrypoints and add `orchestrator run`

#### Context

Deployed Container Apps and Jobs launch via `python -m zava_forward.api` (`server.main`), `python -m zava_forward.api.resident_demo`, `python -m zava_forward.api.live_receiver`, `python -m zava_forward.api.live_simulator`, `python -m zava_forward.agents serve` (`worker.main`), `python -m zava_forward.orchestrator` and its scheduled/manual job modules (`token_store`, `digest_blob`, `ranking_publish`, `source_monitor`, `document_rescan`), and `python -m zava_forward.importer` (`C1`, `C13`, `C15`). Note:
* `live_receiver.main(argv, env=None)`, `live_simulator.main(argv, env=None)`, `ranking_publish.main(..., env=None, ...)`, and `digest_blob.main(..., env=None, ...)` accept an optional `env` mapping for offline tests; passing `env` into `enforce_from_env(env)` preserves pure test isolation.
* Per `PC-001`, `token_store.py`, `resident_demo/__main__.py`, `live_receiver.py`, `digest_blob.py`, and `ranking_publish.py` contain broad `except (..., RuntimeError):` or `except Exception:` blocks, so `enforce_from_env(env)` MUST run at the very top of `main()` before `argparse` / `ZF_SIM_SEED` parsing and outside domain `try:` blocks, catching `ContainerHardeningError` explicitly to print a fixed sanitized refusal message to `sys.stderr` and return/exit `2`.
* Per `PC-001` and `PC-004`, `orchestrator/__main__.py` must define `main(argv=None, env=None) -> int` guarded by `if __name__ == "__main__":` that prints `zava-forward-orchestrator 0.1.0` when invoked with no arguments (satisfying `src/check-container.py:67-71`) and handles a bounded `run` subcommand (validating configuration and emitting a structured standby/diagnostic report with exit `0` when live dispatch is inactive, matching `agents` `serve` standby discipline); `importer/__main__.py` must also wrap `sys.exit(main(sys.argv[1:]))` under `if __name__ == "__main__":`.
* Per `PC-001` and `PC-002`, startup-time enforcement (including `publicSimulationRecipe`) intentionally supersedes any `/healthz` check so `server.py`'s `/healthz` handler remains untouched (`test_container_hosting_completeness.py:118`), and legacy files excluded from formatting in `pyproject.toml` (`server.py`, `digest_blob.py`, `token_store.py`) receive surgical edits only without whole-file `ruff format`.

#### Intent

Call `enforce_from_env(...)` at the entry of each workload entrypoint before opening stores, binding sockets, or polling queues, translating `ContainerHardeningError` into a clean non-zero return/exit without leaking environment values.

#### Boundaries

* Included: `server.py`, `resident_demo/__main__.py`, `live_receiver.py`, `live_simulator.py`, `agents/worker.py`, `orchestrator/__main__.py`, `token_store.py`, `digest_blob.py`, `ranking_publish.py`, `source_monitor.py`, `document_rescan.py`, and `importer/__main__.py`.
* Excluded: Changing CLI flags, default version output when `ZF_CONTAINER_HARDENING` is unset, or `/healthz` handler body inspected by `test_container_hosting_completeness.py:118`.

#### Likely Targets

* `src/api/src/zava_forward/api/server.py`
* `src/api/src/zava_forward/api/resident_demo/__main__.py`
* `src/api/src/zava_forward/api/live_receiver.py`
* `src/api/src/zava_forward/api/live_simulator.py`
* `src/agents/src/zava_forward/agents/worker.py`
* `src/orchestrator/src/zava_forward/orchestrator/__main__.py`
* `src/orchestrator/src/zava_forward/orchestrator/token_store.py`
* `src/orchestrator/src/zava_forward/orchestrator/digest_blob.py`
* `src/orchestrator/src/zava_forward/orchestrator/ranking_publish.py`
* `src/orchestrator/src/zava_forward/orchestrator/source_monitor.py`
* `src/orchestrator/src/zava_forward/orchestrator/document_rescan.py`
* `src/importer/src/zava_forward/importer/__main__.py`

#### Dependencies

* P01-T01.

#### Validation Expectations

* Subprocess invocation of `python -m zava_forward.<pkg>` with `ZF_CONTAINER_HARDENING=enforced` as non-10001 UID exits non-zero with a sanitized hardening message; unset `ZF_CONTAINER_HARDENING` preserves `zava-forward-<dist> 0.1.0` output (`C10`).

#### Completion Evidence

* Subprocess and unit tests across all four packages pass.

#### Unresolved Items

* None.

<!-- rpi:phase id=P02 -->
## P02: Harden deployed Bicep workload specifications and pipeline image consistency

### Context

Currently, `infra/modules/containerapps.bicep`, `infra/resident-demo.bicep`, `infra/live-receiver-job.bicep`, and `infra/live-simulator-job.bicep` omit `ZF_CONTAINER_HARDENING` and explicit `EmptyDir` ephemeral scratch mounts for `/tmp` and `/state` (`C1`, `C15`). In addition, `infra/scripts/pipeline.py` checks `auth-renewal` and `ledger-verify` for conflicting `orchestratorImage` during PR `what-if` planning, omitting `job-forward-{environment}-rank-publish` (`C4`).

### Intent

Declare explicit container hardening environment settings and `EmptyDir` scratch volumes on every deployed Container App and Job in `infra/` and enforce `orchestratorImage` consistency across all three scheduled maintenance jobs in `pipeline.py`.

### Boundaries

* Included: `infra/modules/containerapps.bicep`, `infra/resident-demo.bicep`, `infra/live-receiver-job.bicep`, `infra/live-simulator-job.bicep`, and `infra/scripts/pipeline.py`.
* Excluded: Adding unsupported `securityContext` properties (`C14`), adding `ZF_STATE` to `resident-demo.bicep` (`resident_showcase.py` `FORBIDDEN_ENV_PREFIXES`), or altering `main.bicep` `orchestratorImage` default parameter behavior (`C13`).

### Likely Targets

* `infra/modules/containerapps.bicep`: Add shared `scratchVolumes` / `scratchVolumeMounts` (`tmp` -> `/tmp`, `state` -> `/state` `EmptyDir`) and `ZF_CONTAINER_HARDENING: 'enforced'`, `PYTHONDONTWRITEBYTECODE: '1'`, `TMPDIR: '/tmp'`, `ZF_STATE: '/state'` across `commonEnv` AND `tokenRenewal`'s inline `env` array (`PC-002`, covering `api`, `agents`, `orchestrator`, `tokenRenewal`, `ledgerVerify`, `rankingPublish`, and `importJob`), prepend `from zava_forward.core.container_hardening import enforce_from_env; enforce_from_env()` at the start of `publicSimulationRecipe` without `test_bicep_policy.py` forbidden substrings (`os.environ`, `getenv`, `urandom`, `token_bytes`, `secrets`, `observe`, `request`) (`PC-002`), and set `args: ['run']` alongside `command: ['python', '-m', 'zava_forward.orchestrator']` on `orchestrator` (`PC-004`).
* `infra/resident-demo.bicep`: Add `tmp` `EmptyDir` volume mounted at `/tmp` and `ZF_CONTAINER_HARDENING: 'enforced'`, `PYTHONDONTWRITEBYTECODE: '1'`, `TMPDIR: '/tmp'` (omitting `ZF_STATE` and `/state`).
* `infra/live-receiver-job.bicep` and `infra/live-simulator-job.bicep`: Append `tmp` (`/tmp`) and `state` (`/state`) `EmptyDir` volumes alongside existing read-only `device-certs` (`mountOptions: 'ro'`) and add `ZF_CONTAINER_HARDENING: 'enforced'`, `PYTHONDONTWRITEBYTECODE: '1'`, `TMPDIR: '/tmp'`, `ZF_STATE: '/state'`.
* `infra/scripts/pipeline.py` and `infra/scripts/deploy.py`: Add `f"job-forward-{environment}-rank-publish"` to the `maintenance` job set in `pipeline.py` `deployment()` and add `"rank-publish"` to `targets` in `deploy.py` (`PC-004`).

### Dependencies

* P01.

### Validation Expectations

* `az bicep build` and `az bicep lint` pass with zero errors on `main.bicep`, `modules/containerapps.bicep`, `resident-demo.bicep`, `live-receiver-job.bicep`, and `live-simulator-job.bicep`; `test_bicep_policy.py`, `test_resident_demo_deploy.py`, and `test_pipeline.py` pass.

### Completion Evidence

* Compiled ARM JSON verification in `test_container_hosting_144.py` and passing existing `infra/tests`.

### Unresolved Items

* None.

<!-- rpi:task id=P02-T01 -->
### P02-T01: Add `ZF_CONTAINER_HARDENING=enforced` and `EmptyDir` scratch mounts to Bicep templates

#### Context

`az bicep build` (`Bicep CLI v0.48.1`) verified that `volumes: [{ name: 'tmp', storageType: 'EmptyDir' }, { name: 'state', storageType: 'EmptyDir' }]` and matching `volumeMounts` compile cleanly on both `Microsoft.App/containerApps@2025-07-01` and `Microsoft.App/jobs@2025-07-01` (`C15`), and `bicepconfig.json` treats unused variables as errors (`C14`).

#### Intent

Wire `ZF_CONTAINER_HARDENING: 'enforced'`, `PYTHONDONTWRITEBYTECODE: '1'`, `TMPDIR: '/tmp'` (plus `ZF_STATE: '/state'` everywhere except `resident-demo.bicep`) and explicit `EmptyDir` `volumes`/`volumeMounts` across all 10 declared Container Apps and Jobs in `infra/`.

#### Boundaries

* Included: `infra/modules/containerapps.bicep` (7 workloads), `infra/resident-demo.bicep` (1 workload), `infra/live-receiver-job.bicep` (1 workload), `infra/live-simulator-job.bicep` (1 workload).
* Excluded: Changing ingress, probes, scale rules, identity RBAC, or parameter contracts.

#### Likely Targets

* `infra/modules/containerapps.bicep`
* `infra/resident-demo.bicep`
* `infra/live-receiver-job.bicep`
* `infra/live-simulator-job.bicep`

#### Dependencies

* P01-T02.

#### Validation Expectations

* `az bicep lint` and `az bicep build` succeed on all four files plus `infra/main.bicep`, and `test_resident_demo_deploy.py` confirms no forbidden `ZF_*` prefix appears on `resident-demo`.

#### Completion Evidence

* Zero Bicep diagnostics and passing `test_bicep_policy.py` + `test_resident_demo_deploy.py`.

#### Unresolved Items

* None.

<!-- rpi:task id=P02-T02 -->
### P02-T02: Include `rank-publish` in `pipeline.py` maintenance-job digest check and `deploy.py` target discovery

#### Context

`infra/modules/containerapps.bicep` deploys three conditional scheduled maintenance jobs using `orchestratorImage`: `tokenRenewal` (`auth-renewal`), `ledgerVerify` (`ledger-verify`), and `rankingPublish` (`rank-publish`) (`C1`, `C13`). `infra/scripts/pipeline.py` checked only the first two when validating deployed maintenance images during PR `what-if` planning (`C4`), and `infra/scripts/deploy.py:37-39` listed only `("orchestrator", "auth-renewal", "ledger-verify")` (`PC-004`).

#### Intent

Add `f"job-forward-{environment}-rank-publish"` to `maintenance` in `infra/scripts/pipeline.py` and `"rank-publish"` to `targets` in `infra/scripts/deploy.py` so any deployed `rank-publish` job is discovered and checked fail-closed.

#### Boundaries

* Included: `infra/scripts/pipeline.py`, `infra/scripts/deploy.py`.
* Excluded: Changing `OVERRIDES`, `PROJECTS`, or GitHub workflow check names.

#### Likely Targets

* `infra/scripts/pipeline.py`
* `infra/scripts/deploy.py`

#### Dependencies

* None.

#### Validation Expectations

* `test_pipeline.py` passes and `test_container_hosting_144.py` proves that a mismatched `job-forward-dev-rank-publish` image raises `PipelineError("Existing maintenance jobs have conflicting orchestrator images")`.

#### Completion Evidence

* Passing unit tests on `pipeline.deployment(...)`.

#### Unresolved Items

* None.

<!-- rpi:phase id=P03 -->
## P03: Execute and record declared-scale load and single-replica restart benchmarks

### Context

Issue #144 requires a load test against the declared scale fixture to be run and recorded without claiming production scale, and single-replica + restart behaviour to be verified with audit persistence (`C16`, `C17`, `C18`). Running both harnesses (`scale_load.py` and `test_scale_fixture_load_and_restart.py`) at the declared 60,000-home fixture (`--homes 60000`) on `2026-11-15` produces fresh, reproducible JSON evidence reflecting the current branch head.

### Intent

Run `src/api/tests/scale_load.py` and `src/api/tests/test_scale_fixture_load_and_restart.py` against the 60,000-home SQLite `SqlStore` fixture and record `docs/architecture/scale-load-2026-11-15.json` and `docs/architecture/scale-restart-2026-11-15.json`.

### Boundaries

* Included: Executing both benchmark scripts at `--homes 60000` (`--sessions 20 --rate 5.0 --duration 60` and `--concurrency 20 --seconds 60`) and writing unedited JSON output to `docs/architecture/scale-load-2026-11-15.json` and `docs/architecture/scale-restart-2026-11-15.json`.
* Excluded: Deleting historical `2026-11-01` or `2026-11-13` benchmark files, or editing benchmark numbers by hand, or claiming `meets_declared_workload: true` or production scale.

### Likely Targets

* `docs/architecture/scale-load-2026-11-15.json`: Recorded 60,000-home load + cost-driver report.
* `docs/architecture/scale-restart-2026-11-15.json`: Recorded 60,000-home separate-process concurrent load + `SIGKILL` hard restart + `/api/audit-check` chain persistence report.

### Dependencies

* P01, P02.

### Validation Expectations

* Both CLI runs exit `0` with `0` HTTP errors across `list`, `detail`, and `dashboard` routes, `meets_declared_workload` is `false`, `scope` explicitly states `Not production scale`, and `restart.chain_intact_after_restart` and `restart.chain_intact_after_new_write` are both `true`.

### Completion Evidence

* Committed unedited `docs/architecture/scale-load-2026-11-15.json` and `docs/architecture/scale-restart-2026-11-15.json` verified by `infra/tests/test_container_hosting_144.py`.

### Unresolved Items

* None.

<!-- rpi:task id=P03-T01 -->
### P03-T01: Run 60,000-home `scale_load.py` and `test_scale_fixture_load_and_restart.py` and save dated JSON artifacts

#### Context

Prior runs completed in ~60-125 seconds on 4 vCPUs (`C18`). Running with `initial_wait: 300` captures full deterministic metrics cleanly.

#### Intent

Produce `docs/architecture/scale-load-2026-11-15.json` and `docs/architecture/scale-restart-2026-11-15.json` directly from the benchmark CLIs.

#### Boundaries

* Included: `docs/architecture/scale-load-2026-11-15.json`, `docs/architecture/scale-restart-2026-11-15.json`.
* Excluded: Manual post-editing of recorded metrics.

#### Likely Targets

* `docs/architecture/scale-load-2026-11-15.json`
* `docs/architecture/scale-restart-2026-11-15.json`

#### Dependencies

* P01, P02.

#### Validation Expectations

* Exit status `0` for both benchmark runs and schema/invariant checks in `test_container_hosting_144.py`.

#### Completion Evidence

* Both JSON files written and validated.

#### Unresolved Items

* None.

<!-- rpi:phase id=P04 -->
## P04: Author `infra/tests/test_container_hosting_144.py`, update evidence docs, and run Focused validation

### Context

The caller requested a dedicated test module `infra/tests/test_container_hosting_144.py` and evidence documentation proving all four unticked Issue #144 acceptance criteria, validated with the specified `PYTHONPATH=... unittest` and `ruff` commands.

### Intent

Implement `infra/tests/test_container_hosting_144.py`, update `infra/README.md` with accurate evidence and explicit local-vs-Azure boundaries, and pass Focused validation plus regression suites.

### Boundaries

* Included: `infra/tests/test_container_hosting_144.py` and `infra/README.md`.
* Excluded: Ticking checkboxes on GitHub Issue #144 prior to PR merge (per `.github/copilot-instructions.md`) or placing `.copilot-tracking/` paths in code comments, docstrings, or commit messages.

### Likely Targets

* `infra/tests/test_container_hosting_144.py`: Dedicated end-to-end contract, runtime-hardening, scale-fixture, and single-replica restart audit-persistence test module.
* `infra/README.md`: Updated Issue #144 hosting completeness table and dated `2026-11-15` deployed hardening + scale/restart evidence section.

### Dependencies

* P01, P02, P03.

### Validation Expectations

* `PYTHONPATH=src/core/src:src/agents/src:src/api/src:src/core/tests:src/agents/tests:src/api/tests:infra/tests python3 -m unittest infra/tests/test_container_hosting_144.py -q` passes.
* `python3 -m ruff check infra && python3 -m ruff format --isolated --line-length 100 --check infra/tests/test_container_hosting_144.py` passes (plus `ruff check` on touched `src/` files).
* Full `infra/tests` discovery and targeted `src/core`, `src/agents`, `src/orchestrator`, `src/importer`, and `src/api` restart/load tests pass.

### Completion Evidence

* Passing test and lint command outputs recorded in `.copilot-tracking/changes/2026-11-15/infra-144-container-load-changes.md`.

### Unresolved Items

* None.

<!-- rpi:task id=P04-T01 -->
### P04-T01: Create `infra/tests/test_container_hosting_144.py` covering all four Issue #144 criteria

#### Context

Notice the exact `PYTHONPATH` supplied by the user:
`PYTHONPATH=src/core/src:src/agents/src:src/api/src:src/core/tests:src/agents/tests:src/api/tests:infra/tests python3 -m unittest infra/tests/test_container_hosting_144.py -q`
Because `zava_forward` is a PEP 420 implicit namespace package and none of the five distributions are installed into site-packages, `test_container_hosting_144.py` MUST append `ROOT / "src/orchestrator/src"` and `ROOT / "src/importer/src"` to `sys.path` followed by `importlib.invalidate_caches()` at module top, AND include all five package `src` paths in child subprocess `PYTHONPATH` (`PC-003`).

#### Intent

Build four focused `unittest.TestCase` classes inside `infra/tests/test_container_hosting_144.py`:
1. `VersionedWorkerAndJobPipelineTests`: Verifies real non-root multi-stage Dockerfiles across `api`, `agents`, `orchestrator`, `importer`; `src-deploy.yml` build/check/Trivy/SBOM/publish/deploy stages; `pipeline.py` `release_tag`, `publish` `@sha256:` pinning, `release_images` AcrPull verification, PR-plan `deployment()` checks across all 7 workloads including `job-forward-{env}-rank-publish` conflict rejection, and `deploy.py` `rank-publish` discovery parity; `zava_forward.orchestrator` no-arg version + `run` standby job execution; and compiled `modules/containerapps.bicep` image bindings.
2. `DeployedContainerHardeningTests`: Compiles `modules/containerapps.bicep`, `resident-demo.bicep`, `live-receiver-job.bicep`, and `live-simulator-job.bicep` with `az bicep build` and asserts every container sets `ZF_CONTAINER_HARDENING=enforced`, `PYTHONDONTWRITEBYTECODE=1`, `TMPDIR=/tmp`, appropriate `ZF_STATE=/state` (absent on `resident-demo`), `publicSimulationRecipe` startup `enforce_from_env()`, and `EmptyDir` `volumes`/`volumeMounts` (plus `mountOptions: 'ro'` on cert volumes); exercises `zava_forward.core.container_hardening` positive compliance and negative mutations via side-effect-free injectable hooks (`PC-003`), verifies real kernel `prctl(PR_SET_NO_NEW_PRIVS, 1)` + `/proc/self/status` `NoNewPrivs == 1` + `os.umask(0o077)` inside an isolated child subprocess, and verifies subprocess entrypoint fail-closed refusal (exit code `2`) across `api`, `agents`, `orchestrator`, and `importer` when `ZF_CONTAINER_HARDENING=enforced` runs under a non-10001 host UID.
3. `DeclaredScaleFixtureLoadTests`: Executes a fast bounded `scale_load.run(...)` check verifying live route zero-error execution, cost-driver instrumentation, `meets_declared_workload is False`, and non-production scope framing, AND validates the committed 60,000-home `docs/architecture/scale-load-2026-11-15.json` and `docs/architecture/scale-restart-2026-11-15.json` artifacts against `scale_load.DECLARED` and `API_LIMITS`.
4. `SingleReplicaAndRestartAuditPersistenceTests`: Verifies compiled Bicep `activeRevisionsMode == "Single"`, simulation-lane and `resident-demo` single-replica `maxReplicas == 1`, job `parallelism == 1`, `agents` worker crash-before-post and crash-before-ack redelivery without message loss, and live separate-process API `SIGKILL` hard restart over SQLite `SqlStore` (with `ZF_CONTAINER_HARDENING` unset on the non-10001 host UID per `PC-003`) proving `/api/audit-check` SHA-256 chain persistence across process death and post-restart writes.

#### Boundaries

* Included: `infra/tests/test_container_hosting_144.py` formatted to line length <= 100 (`ruff format --isolated --line-length 100 --check`).
* Excluded: Network calls, Azure CLI live authentication, or Docker daemon dependency at unit-test runtime.

#### Likely Targets

* `infra/tests/test_container_hosting_144.py`

#### Dependencies

* P01, P02, P03.

#### Validation Expectations

* Runs in `< 15 s` with `0` errors under the exact user `PYTHONPATH` command and passes `ruff check infra` and `ruff format --isolated --line-length 100 --check infra/tests/test_container_hosting_144.py`.

#### Completion Evidence

* All tests in `infra/tests/test_container_hosting_144.py` pass and reject deliberate mutations.

#### Unresolved Items

* None.

<!-- rpi:task id=P04-T02 -->
### P04-T02: Update `infra/README.md` hosting completeness evidence and run Focused validation suite

#### Context

`infra/README.md` lines `1317-1404` contain `## Hardened source image rollout (#118)` immediately followed by `## Container hosting completeness (#144)` (`PC-005`), and `infra/tests/test_container_hosting_completeness.py` (`C9`) asserts specific phrases in the `Revision rollback:` paragraph and `"not at declared scale"` / `"makes no production"` wording.

#### Intent

Update `infra/README.md:1317-1404` to reconcile `#118` and `#144`:
* Reconcile the `#118` startup-guard paragraph so it accurately states that ACA `2025-07-01` still lacks ARM `securityContext` and Docker `ENTRYPOINT` wrappers remain omitted (avoiding ACA-incompatible `ST_RDONLY` / `CapBnd == 0` checks), while deployed Bicep templates now set `ZF_CONTAINER_HARDENING=enforced` + `EmptyDir` scratch volumes enforced fail-closed at Python process startup by `zava_forward.core.container_hardening`.
* Criterion 1 (`Worker and job images`): pipeline digest consistency across all 7 workloads including `rank-publish` in `pipeline.py` and `deploy.py`, plus `zava_forward.orchestrator run` scheduled-job standby execution, while noting honestly that direct `main.bicep` invocation outside `pipeline.py` retains bootstrap fallback defaults for `deploy.py` (`test_bicep_policy.py`) and live Azure rollout remains deployment-time scope.
* Criterion 2 (`Container hardening`): deployed Bicep `EmptyDir` scratch volumes + `ZF_CONTAINER_HARDENING=enforced` paired with `zava_forward.core.container_hardening` startup enforcement (`UID/GID 10001:10001`, `prctl(PR_SET_NO_NEW_PRIVS, 1)`, zero `CapEff`/`CapPrm`/`CapInh`/`CapAmb`, `/` and `/app` write rejection, writable `/tmp` and `/state` checks) alongside the ACA ARM `securityContext` schema constraint.
* Criteria 3 & 4 (`Declared-scale fixture load` and `Single-replica and restart audit persistence`): dated `2026-11-15` 60,000-home runs (`docs/architecture/scale-load-2026-11-15.json` and `docs/architecture/scale-restart-2026-11-15.json`) alongside preserved `2026-11-01`/`2026-11-13` records and `infra/tests/test_container_hosting_144.py` verification without claiming production scale or live Azure execution.

#### Boundaries

* Included: `infra/README.md` and full Focused validation run.
* Excluded: Removing or altering phrases pinned by `test_container_hosting_completeness.py`.

#### Likely Targets

* `infra/README.md`

#### Dependencies

* P04-T01.

#### Validation Expectations

* Markdown relative links resolve, `test_container_hosting_completeness.py` and `test_container_hosting_144.py` pass, full `infra/tests` suite passes, targeted `src/` suites pass, and `ruff` checks pass.

#### Completion Evidence

* Verified clean git diff and passing validation commands.

#### Unresolved Items

* None.

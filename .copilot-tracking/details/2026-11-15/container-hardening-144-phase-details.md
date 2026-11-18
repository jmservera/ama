<!-- markdownlint-disable-file -->
# RPI Phase Details: Issue #144 Container Hosting Completeness and Hardening Contracts

## Metadata

* Task ID: issue-144-container-hardening
* Task slug: container-hardening-144
* Related plan: .copilot-tracking/plans/2026-11-15/container-hardening-144-plan.md
* Evidence sources: .copilot-tracking/research/2026-11-15/container-hardening-144-research.md

## Phase Index

| Phase ID | Name                                                                               | Status | Detail sections          |
|----------|------------------------------------------------------------------------------------|--------|--------------------------|
| P01      | Harden Dockerfiles, Importer Bounded Job Entrypoint, and Dynamic Staff Job Spec    | Ready  | P01, P01-T01, P01-T02    |
| P02      | Complete Bicep Worker/Job Contracts and Pipeline Image Release Manifests           | Ready  | P02, P02-T01, P02-T02    |
| P03      | Expand Deterministic Hosting, Scaling, Revision, and Hardening Tests in `infra/`   | Ready  | P03, P03-T01, P03-T02    |
| P04      | Run Focused Validation Suite and Reconcile Implementation Evidence                 | Ready  | P04, P04-T01             |

<!-- rpi:phase id=P01 -->
## P01: Harden Dockerfiles, Importer Bounded Job Entrypoint, and Dynamic Staff Job Spec

### Context

Research evidence (`C1`-`C4`, `C7`, `C9`-`C11`, `C15`) established that `zava_forward.orchestrator` already supports both a no-argument version probe (`zava-forward-orchestrator 0.1.0`) for `src/check-container.py` and a bounded `run` subcommand invoked by Bicep, whereas `zava_forward.importer` only supports interactive/file subcommands (`preview`, `stage`, `exceptions`, `transfer`) plus no-argument version output. In addition, the six `src/` Dockerfiles omit `TMPDIR=/tmp` from `ENV`, and `infra/scripts/staff_azure.py` omits scratch volumes and hardening environment variables on dynamically created `job-staff-*` Container Apps Jobs.

### Intent

Give `zava_forward.importer` a deterministic, fail-closed `run` job subcommand, make `TMPDIR=/tmp` explicit across all `src/` Dockerfiles, and bring `staff_azure.py` dynamic job templates into hardening parity.

### Boundaries

* Included: `src/importer/src/zava_forward/importer/__main__.py`, `src/importer/tests/test_cli_run.py`, the six `src/` Dockerfiles, `infra/scripts/staff_azure.py`, and `infra/scripts/staff-azure-worker.py`.
* Excluded: Changing base image digests, changing `CMD` defaults (which `src/check-container.py` asserts print version strings), or enabling unapproved autonomous import writes.

### Likely Targets

* `src/importer/src/zava_forward/importer/__main__.py`: Add `run` subparser and `_run_job(active_env)` validator (requiring `SQL_SERVER` + `SQL_DATABASE` whenever `ZF_STORE` is `"mssql"` or unset, allowing omission only for explicit `"json"` or `"sqlite"`).
* `src/importer/tests/test_cli_run.py`: Focused unit tests for bare version output, hardened `run` standby JSON, missing/invalid env rejection (including unset vs `"mssql"` `ZF_STORE`), and `ContainerHardeningError` exit 2.
* `src/api/Dockerfile`, `src/agents/Dockerfile`, `src/orchestrator/Dockerfile`, `src/importer/Dockerfile`, `src/api/Dockerfile.resident-demo`, `src/api/live-simulator.Dockerfile`: Add `TMPDIR=/tmp` to `ENV`.
* `infra/scripts/staff_azure.py` and `infra/scripts/staff-azure-worker.py`: Add `ZF_CONTAINER_HARDENING="enforced"`, `PYTHONDONTWRITEBYTECODE=1`, `TMPDIR=/tmp`, `ZF_STATE=/state` env vars plus `tmp` (`/tmp`) and `state` (`/state`) `EmptyDir` volume mounts and volumes on `job-staff-*`, and call `enforce_from_env()` (`exit 2` on `ContainerHardeningError`) at startup in `staff-azure-worker.py`.

### Dependencies

* None.

### Validation Expectations

* `TMPDIR=/dev/shm PYTHONPATH=src/core/src:src/importer/src python3 -m unittest src/importer/tests/test_cli_run.py -q`
* `(cd src/importer && PYTHONPATH=../core/src python3 -m mypy)`

### Completion Evidence

* `zava_forward.importer run` exits 0 with deterministic standby JSON on valid job env and exits 2 on missing `IMPORT_QUEUE`, non-`https` `QUEUE_ENDPOINT`/`BLOB_ENDPOINT`, missing `SQL_SERVER`/`SQL_DATABASE` under `ZF_STORE=mssql`, or unsupported `ZF_IMPORT_DISPATCH`.
* All six `src/` Dockerfiles declare `TMPDIR=/tmp` and `staff_azure.py` mounts `EmptyDir` `/tmp` and `/state`.

### Unresolved Items

* None.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Add bounded `run` subcommand to `zava_forward.importer` and unit tests

#### Context

`infra/modules/containerapps.bicep` (`P02-T01`) configures `importJob` with `ZF_STORE='mssql'`, `SQL_SERVER`, `SQL_DATABASE`, `BLOB_ENDPOINT`, `QUEUE_ENDPOINT`, and `IMPORT_QUEUE='import-jobs'`. Mirroring `zava_forward.orchestrator.__main__` (`C9`), `zava_forward.importer.__main__` (`C10`) should accept an optional `env: Mapping[str, str] | None = None` parameter in `main(argv, env)` (defaulting `argv` to `sys.argv[1:]` when `None` while staying backwards-compatible with `main(sys.argv[1:])`), call `enforce_from_env(active_env)`, keep `not argv` returning `zava-forward-import {__version__}`, support `run` in `argparse` subparsers, and require non-empty `SQL_SERVER` and `SQL_DATABASE` whenever `ZF_STORE` is `"mssql"` or unset (`""`), allowing omission only when `ZF_STORE` is explicitly `"json"` or `"sqlite"` (`PC-001`).

#### Intent

Validate event-triggered `importJob` runtime configuration deterministically and fail closed without performing unreviewed autonomous database mutations.

#### Boundaries

* Included: `src/importer/src/zava_forward/importer/__main__.py` and `src/importer/tests/test_cli_run.py`.
* Excluded: Modifying existing `preview`, `stage`, `exceptions`, or `transfer` subcommand semantics.

#### Likely Targets

* `src/importer/src/zava_forward/importer/__main__.py`: Add `_valid_url`, `_run_job`, optional `env` parameter on `main`, and `sub.add_parser("run", ...)`.
* `src/importer/tests/test_cli_run.py`: New unit test file testing no-arg version check, valid `run` standby JSON (`{"importQueue": "import-jobs", "job": "importer", "mode": "standby", "status": "ok", "version": __version__}`), missing/invalid env cases, and `ZF_CONTAINER_HARDENING=enforced` fail-closed refusal when unhardened.

#### Dependencies

* None.

#### Validation Expectations

* `TMPDIR=/dev/shm PYTHONPATH=src/core/src:src/importer/src python3 -m unittest src/importer/tests/test_cli_run.py -q`
* `(cd src/importer && PYTHONPATH=../core/src python3 -m mypy)`

#### Completion Evidence

* Passing `test_cli_run.py` and zero `mypy` errors in `src/importer`.

#### Unresolved Items

* None.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Enforce `TMPDIR=/tmp` across `src/` Dockerfiles and full runtime hardening parity in `staff_azure.py` and `staff-azure-worker.py`

#### Context

All four primary service/worker/job Dockerfiles (`C1`-`C4`) and both auxiliary `src/api/` Dockerfiles (`C7`) run as `USER 10001:10001` with root-owned `/app` (`0:0`), but omit `TMPDIR=/tmp` in `ENV`. Meanwhile `infra/scripts/staff_azure.py:326-355` (`C15`, `PC-003`) builds an inline `Microsoft.App/jobs` body without `ZF_CONTAINER_HARDENING=enforced`, `PYTHONDONTWRITEBYTECODE=1`, `TMPDIR=/tmp`, `ZF_STATE=/state`, or `EmptyDir` `/tmp` + `/state` scratch mounts, and `infra/scripts/staff-azure-worker.py` omits `enforce_from_env()` startup verification.

#### Intent

Ensure read-only rootfs compatibility with writable `/tmp` and runtime kernel hardening enforcement are baked into every `src/` Dockerfile `ENV`, dynamic `staff_azure.py` job template, and `staff-azure-worker.py` startup path.

#### Boundaries

* Included: Six `src/` Dockerfiles, `infra/scripts/staff_azure.py`, and `infra/scripts/staff-azure-worker.py`.
* Excluded: Changing `infra/cutover-proof.Dockerfile` or `infra/resident-sensor-seed.Dockerfile` `ENTRYPOINT` contracts tested by `test_staff_azure.py`.

#### Likely Targets

* `src/api/Dockerfile`, `src/agents/Dockerfile`, `src/orchestrator/Dockerfile`, `src/importer/Dockerfile`, `src/api/Dockerfile.resident-demo`, `src/api/live-simulator.Dockerfile`: Add `TMPDIR=/tmp` to the runtime stage `ENV` directive.
* `infra/scripts/staff_azure.py`: Add `ZF_CONTAINER_HARDENING="enforced"`, `PYTHONDONTWRITEBYTECODE="1"`, `TMPDIR="/tmp"`, `ZF_STATE="/state"` to `env`, add `volumeMounts: [{"volumeName": "tmp", "mountPath": "/tmp"}, {"volumeName": "state", "mountPath": "/state"}]` to the `staff` container, and `volumes: [{"name": "tmp", "storageType": "EmptyDir"}, {"name": "state", "storageType": "EmptyDir"}]` to `template`.
* `infra/scripts/staff-azure-worker.py`: Call `enforce_from_env()` at startup in `main()`, catching `ContainerHardeningError` and returning `2` without logging private inputs.

#### Dependencies

* None.

#### Validation Expectations

* `TMPDIR=/dev/shm python3 -m unittest infra/tests/test_staff_azure.py infra/tests/test_container_contract.py -q`

#### Completion Evidence

* Passing `test_staff_azure.py` and `test_container_contract.py` with updated hardening assertions.

#### Unresolved Items

* None.

<!-- rpi:phase id=P02 -->
## P02: Complete Bicep Worker/Job Contracts and Pipeline Image Release Manifests

### Context

`infra/modules/containerapps.bicep` (`C6`) lacked `command` and `args` on `importJob` and lacked `@minLength(1)` on its four image parameters (`apiImage`, `agentImage`, `orchestratorImage`, `importImage`). `infra/scripts/pipeline.py` (`C12`) verified individual `{project}.json` files in `release_images()` without emitting/verifying an aggregated release manifest binding all 7 Container Apps/Jobs and their hardening contract, and PR `plan` mode checked only `"@sha256:" in image`. `infra/scripts/deploy.py` (`C13`) allowed placeholder or `:latest` explicit `--orchestrator-image` values even with `--apply`.

### Intent

Enforce complete non-empty/non-placeholder worker and job image and command contracts across `containerapps.bicep`, `pipeline.py`, and `deploy.py` while keeping `main.bicep` stage-1 dependency bootstrap parameter defaults compatible with `#136` and `test_bicep_policy.py`.

### Boundaries

* Included: `infra/modules/containerapps.bicep`, `infra/scripts/pipeline.py`, `infra/scripts/deploy.py`, and `infra/README.md`.
* Excluded: Removing stage-1 bootstrap parameter defaults from `infra/main.bicep` (`C16`, `C19`).

### Likely Targets

* `infra/modules/containerapps.bicep`: Add `@minLength(1)` on `apiImage`, `agentImage`, `orchestratorImage`, `importImage`; add `command: ['python', '-m', 'zava_forward.importer']` and `args: ['run']` on `importJob`.
* `infra/scripts/pipeline.py`: Add `IMMUTABLE_DIGEST_IMAGE_RE`, `HARDENING_CONTRACT`, `WORKLOAD_IMAGE_BINDINGS`, `build_release_manifest`, and `verify_release_manifest`; write/verify `release-manifest.json` inside `release_images`; tighten PR `plan` existing-image check in `deployment()` to require `IMMUTABLE_DIGEST_IMAGE_RE` and reject `quickstart`.
* `infra/scripts/deploy.py`: Reject `PLACEHOLDER`, `"quickstart"` substring, `:latest` tag, or whitespace in explicit `--orchestrator-image` when `--apply` is set (and reject whitespace/empty invalid image syntax in `--orchestrator-image` generally).
* `infra/README.md`: Clarify in the `#136` architecture and module matrix notes that `containerapps.bicep` defines explicit worker/job `command` and `args` overrides and hardening mounts, while `main.bicep` retains bootstrap-only quickstart defaults overridden by immutable `@sha256:` release manifests in `pipeline.py` (`#144` live rollout remains operator-gated).

### Dependencies

* P01 (`zava_forward.importer run` subcommand).

### Validation Expectations

* `python3 infra/scripts/bicep_inventory.py --check`
* `TMPDIR=/dev/shm python3 -m unittest infra/tests/test_bicep_architecture_inventory_136.py infra/tests/test_from_empty_reproducibility_136.py -q`

### Completion Evidence

* `az bicep build --file infra/main.bicep` succeeds, `scan_bicep_tree(ROOT)` shows `_resource_block_has_command(..., "importJob") == True`, and `bicep_inventory.py --check` exits 0.

### Unresolved Items

* None.

<!-- rpi:task id=P02-T01 -->
### P02-T01: Wire `importJob` explicit `run` command and `@minLength(1)` image constraints in `containerapps.bicep` and update `infra/README.md`

#### Context

In `infra/modules/containerapps.bicep`, `orchestrator` declares `command: ['python', '-m', 'zava_forward.orchestrator']` and `args: ['run']`, whereas `importJob` omitted both. Adding the matching `command` and `args` on `importJob` satisfies `_resource_block_has_command(..., "importJob")` in `bicep_inventory.py` (`C14`) while keeping `main.bicep` bootstrap defaults untouched so `bicep_tree.placeholder_workers` remains `True` (`main_has_placeholder == True`) as asserted by `test_bicep_architecture_inventory_136.py:199-203` (`C19`).

#### Intent

Guarantee `importJob` executes `python -m zava_forward.importer run` in both standard (`job-${prefix}-import`) and `demoDirectIngress` (`job-${prefix}-load`) modes and forbid empty image strings in `containerapps.bicep`.

#### Boundaries

* Included: `infra/modules/containerapps.bicep` and `infra/README.md`.
* Excluded: Changing `infra/main.bicep` parameter defaults or `#136` table column headers/status enums.

#### Likely Targets

* `infra/modules/containerapps.bicep`: `@minLength(1)` on `apiImage`, `agentImage`, `orchestratorImage`, `importImage`; `{ name: 'ZF_STORE', value: 'mssql' }`, `command`, and `args` on `importJob` (`PC-001`).
* `infra/README.md`: Update notes on `container-apps-hosting-and-jobs` and `infra/modules/containerapps.bicep` rows accurately while strictly preserving `Delivery status` `` `delivered-placeholder-workers` `` required by `bicep_inventory.py` / `test_bicep_architecture_inventory_136.py` (`PC-005`).

#### Dependencies

* P01-T01.

#### Validation Expectations

* `python3 infra/scripts/bicep_inventory.py --check`
* `TMPDIR=/dev/shm python3 -m unittest infra/tests/test_bicep_architecture_inventory_136.py -q`

#### Completion Evidence

* Compiled ARM JSON for `containerapps` module shows `minLength: 1` on all four image params and `command: ["python", "-m", "zava_forward.importer"]`, `args: ["run"]` on `importJob`.

#### Unresolved Items

* None.

<!-- rpi:task id=P02-T02 -->
### P02-T02: Enforce deterministic release manifest bundle and non-placeholder digest guards in `pipeline.py` and `deploy.py`

#### Context

Research (`C12`, `C17`) noted that `test_pipeline.py:667` uses `example.azurecr.io/{project}@sha256:{"b"*64}` in PR `plan` mode, whereas `publish()` and `release_images()` enforce `{server}/zava-forward-{project}@sha256:[0-9a-f]{64}` with exact `source_sha` and `release_tag()`.

#### Intent

Provide an explicit, versioned, tamper-checked `release-manifest.json` contract binding all 4 project images, all 7 Container Apps/Jobs, and their container hardening posture during release verification, while closing placeholder/digest loopholes in `pipeline.deployment()` PR `plan` mode and `deploy.py --apply`.

#### Boundaries

* Included: `infra/scripts/pipeline.py` and `infra/scripts/deploy.py`.
* Excluded: Altering `{project}.json` schema keys in `publish()` in any way that breaks existing `test_pipeline.py` assertions, or breaking `deploy.py` what-if fallback when no registry/tag exists yet.

#### Likely Targets

* `infra/scripts/pipeline.py`:
  * Keep eager Python 3.12 annotations (do NOT combine `from __future__ import annotations` with `@dataclass`, so `test_pipeline.py`'s `spec_from_file_location` import without `sys.modules["pipeline"]` and `mypy --strict infra/scripts/pipeline.py` both succeed; `PC-004`).
  * Add `RELEASE_MANIFEST_FILE = "release-manifest.json"`, `PLAN_IMMUTABLE_IMAGE_RE = re.compile(r"^[a-z0-9.-]+/[a-z0-9._/-]+@sha256:[0-9a-f]{64}$")`, `HARDENING_CONTRACT`, and `WORKLOAD_IMAGE_PARAMETERS` mapping all 7 workloads (`api`, `agents`, `orchestrator`, `auth-renewal`, `ledger-verify`, `rank-publish`, `import`) to their parameter keys.
  * Add `build_release_manifest(directory: Path, server: str) -> dict[str, Any]` and `verify_release_manifest(manifest: dict[str, Any], server: str) -> dict[str, str]` verifying `schema_version == 1`, `source_sha == source_sha()`, `tag == release_tag()` (using `release_tag()` equality rather than a rigid `-r<id>-a<attempt>` regex so `test_container_hosting_144.py:224`'s `release_tag` stub passes; `PC-004`), non-placeholder `{server}/zava-forward-{project}@sha256:[0-9a-f]{64}` digests for all 4 projects, exact 7-workload binding, and `HARDENING_CONTRACT` equality.
  * Update `release_images(directory, server)` to build, verify, write `directory / RELEASE_MANIFEST_FILE`, pull each immutable digest, and return the 4 Bicep image parameter values, and embed `summary["release_manifest"]` in `deployment()` when `images_directory is not None` (`PC-004`).
  * Update `deployment()` PR `plan` branch (`images_directory is None`) to require `isinstance(image, str) and PLAN_IMMUTABLE_IMAGE_RE.fullmatch(image) and "quickstart" not in image.lower()`.
* `infra/scripts/deploy.py`:
  * Reject internal whitespace/control chars in non-blank explicit `--orchestrator-image` (after outer `.strip()`), and when `--apply` is set, refuse `PLACEHOLDER`, `"quickstart"` in `image.lower()`, or `:latest` tags on non-blank `--orchestrator-image` as well as image `--parameter` overrides (`apiImage`, `agentImage`, `agentsImage`, `importImage`) without enforcing 64-hex CLI digest lengths so `test_deploy.py` synthetic fixtures (`@sha256:abc123` and blank `--orchestrator-image "  " --apply`) remain green (`PC-004`).

#### Dependencies

* None.

#### Validation Expectations

* `TMPDIR=/dev/shm python3 -m unittest infra/tests/test_pipeline.py infra/tests/test_deploy.py -q`

#### Completion Evidence

* `release_images()` emits verified `release-manifest.json` and rejects any mutated project digest, workload mapping, placeholder image, or hardening metadata; PR `plan` rejects `quickstart` and non-64-hex digests; `deploy.py --apply` rejects placeholder/`:latest` overrides.

#### Unresolved Items

* None.

<!-- rpi:phase id=P03 -->
## P03: Expand Deterministic Hosting, Scaling, Revision, and Hardening Tests in `infra/tests/`

### Context

Research (`C16`-`C18`) identified concrete test gaps across `test_container_hosting_144.py`, `test_container_hosting_completeness.py`, `test_bicep_policy.py`, `test_pipeline.py`, `test_deploy.py`, and `test_staff_azure.py`.

### Intent

Lock every `#144` worker/job image binding, revision mode, scaling rule, `demoDirectIngress` parity, release manifest, and container hardening invariant behind fast, deterministic offline tests.

### Boundaries

* Included: `infra/tests/test_container_hosting_144.py`, `infra/tests/test_container_hosting_completeness.py`, `infra/tests/test_bicep_policy.py`, `infra/tests/test_pipeline.py`, `infra/tests/test_deploy.py`, and `infra/tests/test_staff_azure.py`.
* Excluded: Live Docker daemon builds or live Azure network calls.

### Likely Targets

* `infra/tests/test_container_hosting_144.py`: Update `import` expected command/args to `(["python", "-m", "zava_forward.importer"], ["run"])` and assert `ZF_STORE == "mssql"` on compiled `importJob` (`PC-001`); add `("importer-run", [sys.executable, "-m", "zava_forward.importer", "run"])` to `test_all_deployed_entrypoints_fail_closed_under_enforced_hardening_violation` (`PC-005`); add tests for `importer` bare + bounded `run` mode, all six `src/` Dockerfiles (`TMPDIR=/tmp`, `USER 10001:10001`, root-owned `/app`, `chown 10001:10001 /state`), `containerapps.bicep` `@minLength(1)` image params + scaling rules (`api` HTTP `concurrentRequests: '50'`, `agents` `azure-queue` `agent-tasks` `queueLength: '5'` `0..5`, `importJob` `azure-queue` `import-jobs` `queueLength: '1'` `0..2`, cron schedules/timeouts/retries on `orchestrator`/`tokenRenewal`/`ledgerVerify`/`rankingPublish`) + `demoDirectIngress=true` compiled names (`ca-{prefix}-api`, `ca-{prefix}-agents`, `job-{prefix}-orch`, `job-{prefix}-auth`, `job-{prefix}-audit`, `job-{prefix}-rank`, `job-{prefix}-load` with `enableEntraTokenStore` and `rankingArchiveContainer` enabled; `PC-002`), securityContext/Linux capability/`NoNewPrivs` parity across `check-container.py` + `acr-cutover.yaml` + `container_hardening.py`, and `release-manifest.json` verification.
* `infra/tests/test_container_hosting_completeness.py`: Include `modules/containerapps.bicep:tokenRenewal`, `modules/containerapps.bicep:rankingPublish`, `live-receiver-job.bicep:job`, and `live-simulator-job.bicep:job` in `test_inventory_covers_api_worker_jobs_and_demo`.
* `infra/tests/test_bicep_policy.py`: Include `"ranking-publish"` alongside `"orchestrator"`, `"ledger-verify"`, `"auth-renewal"` in `assert_hosting_limits_and_rollout`.
* `infra/tests/test_pipeline.py`: Add tests for `release-manifest.json` binding/tamper rejection and PR `plan` placeholder/bad-digest rejection.
* `infra/tests/test_deploy.py`: Add test verifying `--apply` rejection of placeholder/`:latest` non-blank `--orchestrator-image` and image `--parameter` overrides while preserving blank/what-if bootstrap behavior (`PC-004`).
* `infra/tests/test_staff_azure.py`: Assert `job-staff-*` includes `ZF_CONTAINER_HARDENING=enforced`, `PYTHONDONTWRITEBYTECODE=1`, `TMPDIR=/tmp`, `ZF_STATE=/state`, and `EmptyDir` `/tmp` + `/state` mounts, and verify `staff-azure-worker.py` fails closed (`exit 2`) under `ZF_CONTAINER_HARDENING=enforced` when unhardened (`PC-003`).

### Dependencies

* P01, P02.

### Validation Expectations

* `TMPDIR=/dev/shm python3 -m unittest infra/tests/test_container_hosting_144.py infra/tests/test_container_hosting_completeness.py infra/tests/test_container_contract.py infra/tests/test_bicep_policy.py infra/tests/test_pipeline.py infra/tests/test_deploy.py infra/tests/test_staff_azure.py -q`

### Completion Evidence

* All targeted `infra/tests/` suites pass deterministically under `TMPDIR=/dev/shm`.

### Unresolved Items

* None.

<!-- rpi:task id=P03-T01 -->
### P03-T01: Extend `test_container_hosting_144.py`, `test_container_hosting_completeness.py`, and `test_bicep_policy.py`

#### Context

See P03 Context and Research `C16`, `C18`.

#### Intent

Verify worker/job Dockerfiles, Bicep scaling/revision/naming/command contracts, and securityContext/capability hardening invariants end to end.

#### Boundaries

* Included: `infra/tests/test_container_hosting_144.py`, `infra/tests/test_container_hosting_completeness.py`, `infra/tests/test_bicep_policy.py`.
* Excluded: Removing any existing test method.

#### Likely Targets

* `infra/tests/test_container_hosting_144.py`, `infra/tests/test_container_hosting_completeness.py`, `infra/tests/test_bicep_policy.py`.

#### Dependencies

* P01, P02.

#### Validation Expectations

* `TMPDIR=/dev/shm python3 -m unittest infra/tests/test_container_hosting_144.py infra/tests/test_container_hosting_completeness.py infra/tests/test_bicep_policy.py -q`

#### Completion Evidence

* Zero failures across all three Bicep and container hosting test modules.

#### Unresolved Items

* None.

<!-- rpi:task id=P03-T02 -->
### P03-T02: Extend `test_pipeline.py`, `test_deploy.py`, and `test_staff_azure.py` for release manifests, placeholder rejection, and job scratch mounts

#### Context

See P03 Context and Research `C12`, `C13`, `C15`, `C17`.

#### Intent

Verify release manifest generation/tamper rejection, PR `plan` and `deploy.py --apply` placeholder rejection, `rank-publish` image preservation, and `staff_azure.py` dynamic job hardening mounts.

#### Boundaries

* Included: `infra/tests/test_pipeline.py`, `infra/tests/test_deploy.py`, `infra/tests/test_staff_azure.py`.
* Excluded: Removing any existing test method.

#### Likely Targets

* `infra/tests/test_pipeline.py`, `infra/tests/test_deploy.py`, `infra/tests/test_staff_azure.py`.

#### Dependencies

* P01-T02, P02-T02.

#### Validation Expectations

* `TMPDIR=/dev/shm python3 -m unittest infra/tests/test_pipeline.py infra/tests/test_deploy.py infra/tests/test_staff_azure.py -q`

#### Completion Evidence

* Zero failures across `test_pipeline.py`, `test_deploy.py`, and `test_staff_azure.py`.

#### Unresolved Items

* None.

<!-- rpi:phase id=P04 -->
## P04: Run Focused Validation Suite and Reconcile Implementation Evidence

### Context

Repository instructions and caller rules require Focused-tier validation using `TMPDIR=/dev/shm`, `ruff check`, `ruff format --check`, `mypy` inside modified `src/<project>` directories, and `#136` regression checks, recorded in `.copilot-tracking/changes/2026-11-15/container-hardening-144-changes.md`.

### Intent

Confirm zero lint, format, type, or unit/Bicep regressions across all touched and coupled components before transitioning to `rpi-review`.

### Boundaries

* Included: Targeted `unittest` runs under `TMPDIR=/dev/shm`, `ruff check`, `ruff format --check`, `mypy` in `src/importer`, `bicep_inventory.py --check`, and `.copilot-tracking/` reconciliation.
* Excluded: Full 36-file `unittest discover -s infra/tests` or `tools/rpi-checks.py --all`.

### Likely Targets

* `.copilot-tracking/changes/2026-11-15/container-hardening-144-changes.md`, `.copilot-tracking/plans/2026-11-15/container-hardening-144-plan.md`, `.copilot-tracking/details/2026-11-15/container-hardening-144-phase-details.md`.

### Dependencies

* P01, P02, P03.

### Validation Expectations

* `python3 -m ruff check --isolated --select E,F,I,B,UP --target-version py312 --line-length 100 <touched files>`
* `python3 -m ruff format --isolated --line-length 100 --check <touched files>`
* `(cd src/importer && PYTHONPATH=../core/src python3 -m mypy)`
* `python3 -m mypy --strict infra/scripts/pipeline.py`
* `PYTHONPATH=src/core/src python3 -m mypy --follow-imports=silent --ignore-missing-imports infra/scripts/staff_azure.py infra/scripts/staff_blob.py infra/scripts/staff-azure-worker.py infra/scripts/credential_arm.py`
* `python3 infra/scripts/bicep_inventory.py --check`
* `TMPDIR=/dev/shm python3 -m unittest ... -q` across all touched/coupled test modules (`test_cli_run.py`, `test_container_hosting_144.py`, `test_container_hosting_completeness.py`, `test_container_contract.py`, `test_bicep_policy.py`, `test_pipeline.py`, `test_deploy.py`, `test_staff_azure.py`, `test_bicep_architecture_inventory_136.py`, `test_from_empty_reproducibility_136.py`).

### Completion Evidence

* Clean exit 0 from every static and targeted unit/Bicep check, recorded in `.copilot-tracking/changes/2026-11-15/container-hardening-144-changes.md`.

### Unresolved Items

* None.

<!-- rpi:task id=P04-T01 -->
### P04-T01: Execute RAM-backed targeted tests, `ruff`, `mypy`, and `#136` regression checks

#### Context

See P04 Context.

#### Intent

Run and record deterministic verification across all modified and coupled modules.

#### Boundaries

* Included: Static analysis, type checking, Bicep inventory check, and targeted unit suites under `TMPDIR=/dev/shm`.
* Excluded: Live Azure CLI commands or `tools/rpi-checks.py --all`.

#### Likely Targets

* `.copilot-tracking/changes/2026-11-15/container-hardening-144-changes.md`.

#### Dependencies

* P01, P02, P03.

#### Validation Expectations

* All commands exit 0.

#### Completion Evidence

* Recorded command outputs and reconciled `[x]` checklist items in plan, phase details, and changes artifacts.

#### Unresolved Items

* None.

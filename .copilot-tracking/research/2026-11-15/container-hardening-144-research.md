---
description: "Primary evidence artifact for Issue #144 local container hosting completeness and hardening contract"
---
<!-- markdownlint-disable-file -->

# Task Research: container-hardening-144

| Field              | Value                                                                    |
|--------------------|--------------------------------------------------------------------------|
| Date               | 2026-11-15                                                               |
| Researcher / agent | RPI Agent (`rpi-research`)                                               |
| Status             | Completed (`Planning Readiness: Ready`)                                  |
| Artifact path      | .copilot-tracking/research/2026-11-15/container-hardening-144-research.md |

## Research Brief

* What to research: Existing Issue #144 implementation across `src/*/Dockerfile`, `infra/modules/containerapps.bicep`, `infra/main.bicep`, `infra/scripts/`, `.github/workflows/`, and `infra/tests/` to identify any gaps in worker (`orchestrator`) and job (`importer`) image versioning, non-placeholder binding, container hardening (`USER` non-root, read-only root filesystem compatibility with explicit writable `/tmp` volume mounts, dropped Linux capabilities / security context contract), revision mode, scaling rules, and deterministic test coverage.
* Why it matters: Issue #144 requires deterministic local verification and contract completeness for worker/job images and container hardening in both Dockerfiles, Bicep definitions, and pipeline image release manifests while preserving live Azure deployment boundaries.
* Audience or intended use: `rpi-plan`, `rpi-plan-critique`, `rpi-implement`, and `rpi-review` on branch `feat/infra-144-container-hardening`.
* Scope: `src/api/Dockerfile`, `src/orchestrator/Dockerfile`, `src/importer/Dockerfile`, `src/agents/Dockerfile`, `infra/modules/containerapps.bicep`, `infra/main.bicep`, `infra/*.bicepparam`, `infra/scripts/pipeline.py`, `infra/scripts/deploy.py`, `.github/workflows/src-deploy.yml`, `.github/workflows/src-ci.yml`, `infra/README.md`, and `infra/tests/`.
* Non-goals: Live Azure deployments, pushing to remote or opening a PR, claiming live Azure runtime acceptance for #144, or running the full `tools/rpi-checks.py --all` gate (caller specified Focused tier).
* Criteria: Deterministic static/unit verification of worker and job image tag binding, non-placeholder image definitions, revision mode, scaling rules, non-root execution, read-only root filesystem with explicit `/tmp` `EmptyDir` volume mounts, and dropped Linux capabilities / security context contracts across Dockerfiles, Bicep templates, and pipeline release manifests.
* Requested outputs: Converged architectural and test gap synthesis with concrete file-and-line evidence ready for `rpi-plan`.
* Output mode: convergence

## Research Parameters

| Field                                | Value                                                                                                                                    |
|--------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------|
| Research question(s)                 | How do `src/*/Dockerfile`, `infra/modules/containerapps.bicep`, `infra/scripts/`, and `.github/workflows/` currently define and test worker/job image versioning, scaling, revisions, and container hardening, and what gaps remain? |
| Codebase scope                       | `src/`, `infra/`, `.github/workflows/`, `docs/adrs/0002-pilot-readiness-architecture.md`                                                 |
| External scope                       | none (local contract and Azure Container Apps Bicep schema already pinned in repo)                                                       |
| Initial internal candidate areas     | `src/api/Dockerfile`, `src/orchestrator/Dockerfile`, `src/importer/Dockerfile`, `infra/modules/containerapps.bicep`, `infra/scripts/pipeline.py`, `infra/tests/test_container_*.py` |
| Initial external candidate areas     | none                                                                                                                                     |
| Research posture                     | focused                                                                                                                                  |
| Posture provenance                   | caller-specified (bounded internal task with named source targets and Focused validation tier)                                           |
| Explicit limits / deadline           | Focused validation tier; no `git push` or `gh pr create`; prefix Python tests with `TMPDIR=/dev/shm`; run targeted tests only            |
| Posture-specific completion basis    | focused scope and materiality                                                                                                            |
| Edits allowed during research?       | no, research-only                                                                                                                        |
| Resolved evidence root               | `.copilot-tracking/`                                                                                                                     |
| Known constraints / excluded sources | Preserve live Azure deployment boundaries; do not claim live deployed acceptance for Issue #144                                          |

## Extension Registry and Provenance

* Precedence: platform and host safety; caller scope and criteria; matching repository instructions and enforced schemas; rpi-research contract; domain skills and specialists; examples and preferences.

| Kind                | Candidate                        | Match and provenance                              | Scoped authority or output contract          | Selected / skipped reason      |
|---------------------|----------------------------------|---------------------------------------------------|----------------------------------------------|--------------------------------|
| Instruction         | `.github/copilot-instructions.md` | `applyTo: "**"` repository guidance               | Validation tiers, infra ruff check+format, live vs local evidence boundaries | Selected: governs repository norms and Issue #144 truthfulness |
| Skill               | `owasp-infrastructure` / `secure-by-design` | Container hardening domain topic       | Advisory security context only               | Skipped: local Bicep/Dockerfile hardening criteria are explicitly enumerated by caller and existing repo tests |
| Research specialist | `hve-core-all:rpi-researcher`    | Host-registered subagent                          | Delegated research lane                      | Skipped (inline): tightly coupled 6-8 file codebase trace completes faster and cleaner inline without context fragmentation |

## User Participation and Research Decisions

| Checkpoint       | Questions or no-interaction rationale                       | Answers / unanswered      | Resulting decision or selected further research    |
|------------------|-------------------------------------------------------------|---------------------------|----------------------------------------------------|
| Intake           | Non-interactive session with complete caller scope, branch, target files, acceptance criteria, and validation rules | N/A (non-interactive) | Proceed directly with Cycle 1 inline focused research |
| Direction change | None                                                        | N/A                       | Maintain caller scope                              |
| Convergence      | Cycle 1 answered all questions with complete local evidence | N/A (non-interactive)     | Converged on concrete gap-closure recommendation; Planning Readiness `Ready` |

## Scope and Success Criteria

* Scope: Inspect `src/*/Dockerfile`, `infra/modules/containerapps.bicep`, `infra/main.bicep`, `infra/scripts/pipeline.py`, `infra/scripts/deploy.py`, `infra/scripts/bicep_inventory.py`, `.github/workflows/src-ci.yml`, `.github/workflows/src-deploy.yml`, `infra/README.md`, and `infra/tests/test_container*.py` + `test_pipeline.py` + `test_bicep_policy.py` + `test_bicep_architecture_inventory_136.py`.
* Assumptions verified:
  * Verified `infra/modules/containerapps.bicep` is the canonical module path (`infra/modules/container-apps.bicep` does not exist).
  * Verified Azure Container Apps ARM API `2025-07-01` does not expose `securityContext.readOnlyRootFilesystem` or `securityContext.capabilities.drop` in the ARM container resource schema; therefore Zava Forward enforces container hardening as a defense-in-depth contract across three layers: (a) image build/scan (`USER 10001:10001`, root-owned `0:0` `/app`, `PYTHONDONTWRITEBYTECODE=1`, `TMPDIR=/tmp`, `ZF_STATE=/state`, Docker `--read-only --cap-drop=ALL --security-opt=no-new-privileges` in `src/check-container.py` and `src/acr-cutover.yaml`), (b) Bicep hosting (`hardeningEnv` with `ZF_CONTAINER_HARDENING=enforced`, `PYTHONDONTWRITEBYTECODE=1`, `TMPDIR=/tmp`, `ZF_STATE=/state` plus explicit `EmptyDir` `/tmp` and `/state` volume mounts), and (c) startup fail-closed kernel verification (`zava_forward.core.container_hardening.enforce_from_env()` checking UID/GID `10001:10001`, `umask(0o077)`, `prctl(PR_SET_NO_NEW_PRIVS)` / `NoNewPrivs=1`, zero Linux capability masks `CapInh`/`CapPrm`/`CapEff`/`CapBnd`/`CapAmb`, write-rejected `/` and `/app`, and writable `/tmp` + `/state`).
* Success criteria:
  * Every research question is answered with exact `path:line` evidence (`C1`-`C19`).
  * Gaps in Dockerfiles, Bicep definitions, pipeline release manifests, and `infra/tests/` are concretely identified without regressing coupled `#136` or `test_bicep_policy.py` bootstrap invariants.
  * Self-check passes.

## Candidate Research Areas and Decomposed Questions

* Q1: Are worker (`orchestrator`, `agents`) and job (`importer`, `auth-renewal`, `ledger-verify`, `rank-publish`) Dockerfiles, Bicep definitions, and entrypoints real, versioned, non-placeholder, and explicitly invoked with bounded job commands?
* Q2: How is container hardening (`USER` non-root, read-only rootfs compatibility with writable `/tmp` + `/state` mounts, dropped Linux capabilities, `NoNewPrivs`) enforced across `src/*/Dockerfile`, `infra/*.bicep`, `infra/scripts/`, and workload startup entrypoints, and where are the remaining gaps?
* Q3: Do pipeline image release manifests (`infra/scripts/pipeline.py`, `infra/scripts/deploy.py`, `.github/workflows/src-deploy.yml`) deterministically bind versioned, immutable, non-placeholder `@sha256:` images across all apps and jobs, including PR `plan` mode and release promotion?
* Q4: What deterministic tests in `infra/tests/` currently cover `#144` worker/job image tag binding, revision mode, scaling rules, and hardening invariants, and what specific assertions are missing?

## Cycle 1 Execution (Wider -> Deeper -> Contrarian)

### Wave 1: Wider (Inline)

* Surveyed all 8 Dockerfiles (`src/api/Dockerfile`, `src/agents/Dockerfile`, `src/orchestrator/Dockerfile`, `src/importer/Dockerfile`, `src/api/Dockerfile.resident-demo`, `src/api/live-simulator.Dockerfile`, `infra/cutover-proof.Dockerfile`, `infra/resident-sensor-seed.Dockerfile`), all Bicep templates (`infra/main.bicep`, `infra/modules/containerapps.bicep`, `infra/modules/guard.bicep`, `infra/resident-demo.bicep`, `infra/live-receiver-job.bicep`, `infra/live-simulator-job.bicep`), CI/CD workflows (`.github/workflows/src-ci.yml`, `.github/workflows/src-deploy.yml`), pipeline/deploy/inventory scripts (`infra/scripts/pipeline.py`, `infra/scripts/deploy.py`, `infra/scripts/bicep_inventory.py`, `infra/scripts/reproducibility_check.py`, `infra/scripts/staff_azure.py`), and `infra/tests/test_container_*.py`.
* Baseline targeted test run (`TMPDIR=/dev/shm ... unittest discover -s infra/tests -p 'test_container_*.py' -q`) passed all 35 existing tests in 20.9s.

### Wave 2: Deeper (Inline)

* Traced `infra/modules/containerapps.bicep` (`C5`, `C6`):
  * `orchestrator` declares `command: ['python', '-m', 'zava_forward.orchestrator']` and `args: ['run']`, pairing with `src/orchestrator/src/zava_forward/orchestrator/__main__.py` (`C9`), which runs `enforce_from_env()`, validates `TASK_QUEUE`, `QUEUE_ENDPOINT`, `API_BASE_URL`, and `ZF_ORCHESTRATOR_DISPATCH`, and emits bounded standby JSON while keeping bare no-arg `CMD` as version output (`zava-forward-orchestrator 0.1.0`) for `src/check-container.py` (`C11`).
  * Gap G1 (`importJob` command + `importer` bounded `run` mode): `importJob` (`job-${prefix}-import` / `job-${prefix}-load`) in `infra/modules/containerapps.bicep:561-621` (`C6`) omits `command` and `args`, so queue-triggered runs fall back to no-arg `CMD ["python", "-m", "zava_forward.importer"]`, printing `zava-forward-import 0.1.0` and exiting 0 without validating `IMPORT_QUEUE`, `QUEUE_ENDPOINT`, `BLOB_ENDPOINT`, `SQL_SERVER`, or `SQL_DATABASE` (`C10`). Moreover, `infra/scripts/bicep_inventory.py:253-256` (`C14`) explicitly checks `_resource_block_has_command(..., "importJob")`!
  * Gap G2 (`containerapps.bicep` parameter contract): `apiImage`, `agentImage`, `orchestratorImage`, and `importImage` in `infra/modules/containerapps.bicep:55-61` lack `@minLength(1)` constraints.
* Traced Dockerfiles and runtime hardening (`C1`-`C4`, `C7`, `C8`, `C15`):
  * All four primary Dockerfiles (`src/api/Dockerfile`, `src/agents/Dockerfile`, `src/orchestrator/Dockerfile`, `src/importer/Dockerfile`) plus `src/api/Dockerfile.resident-demo` and `src/api/live-simulator.Dockerfile` share the pinned digest base `python@sha256:34386ef0cb081344d7ec1c103ba398e6e9f64e9ab3a1509accc92a4e24a07258`, install real hashed wheels, run as `USER 10001:10001`, and keep `/app` owned by `0:0` (`mkdir -p /app /data /state && chown 10001:10001 /state`) so `/app` rejects writes (`EACCES` on ACA, `EROFS` under Docker `--read-only`).
  * Gap G3 (Dockerfile `TMPDIR=/tmp` parity): None of the six `src/` Dockerfiles set `TMPDIR=/tmp` in `ENV` (`C1`-`C4`, `C7`), relying solely on Bicep `hardeningEnv` (`TMPDIR=/tmp`) at runtime. Declaring `TMPDIR=/tmp` in every `src/` Dockerfile `ENV` makes read-only rootfs scratch redirection intrinsic to the image contract itself.
  * Gap G4 (Dynamic `staff_azure.py` job hardening parity): `infra/scripts/staff_azure.py:326-355` (`C15`) constructs the manual `job-staff-*` Container Apps Job payload without `PYTHONDONTWRITEBYTECODE=1`, `TMPDIR=/tmp`, `ZF_STATE=/state`, or `EmptyDir` `/tmp` + `/state` scratch volume mounts.
* Traced `infra/scripts/pipeline.py` and `infra/scripts/deploy.py` (`C12`, `C13`):
  * `pipeline.publish()` writes `{project}.json` (`project`, `image`, `source_sha`, `tag`) and `pipeline.release_images()` verifies `{server}/zava-forward-{project}@sha256:[0-9a-f]{64}` for all 4 projects (`api`, `agents`, `orchestrator`, `importer`).
  * Gap G5 (Release manifest bundle & placeholder rejection in `pipeline.py` / `deploy.py`):
    1. `pipeline.py` lacks an explicit, deterministic aggregated release manifest contract (`build_release_manifest` / `verify_release_manifest` writing `release-manifest.json` during release verification) that binds all 4 versioned non-placeholder `@sha256:` images to all 7 hosted workloads (`api`, `agents`, `orchestrator`, `auth-renewal`, `ledger-verify`, `rank-publish`, `import`) alongside their verified container hardening contract (`user: "10001:10001"`, `read_only_root_compatible: True`, `writable_mounts: ["/tmp", "/state"]`, `dropped_capabilities: "ALL"`, `no_new_privileges: True`).
    2. In `pipeline.deployment()` PR `plan` mode (`infra/scripts/pipeline.py:555-565`, `C12`), existing cluster images are only checked with `"@sha256:" not in image`, which fails to reject malformed non-64-hex digests or `mcr.microsoft.com/k8se/quickstart@...` placeholder references.
    3. In `deploy.py` (`C13`), explicit `--orchestrator-image` CLI overrides do not reject `PLACEHOLDER` (`mcr.microsoft.com/k8se/quickstart:latest`), `:latest`, or whitespace-containing malformed image references when `--apply` or explicit override is used; and `test_deploy.py:163` (`C17`) omits `rank-publish` in `test_each_existing_job_preserves_its_image_without_querying_registry`.

### Wave 3: Contrarian (Inline)

* Tested the naive hypothesis: "Should we remove `'mcr.microsoft.com/k8se/quickstart:latest'` defaults from `infra/main.bicep` so `bicep_tree.placeholder_workers` flips to `False` and `infra/README.md` flips `containerapps.bicep` to `delivered`?"
* Counter-evidence (`C16`, `C18`, `C19`) decisively refuted removing bootstrap parameter defaults from `infra/main.bicep`:
  1. `infra/tests/test_bicep_policy.py:1044-1089` (`C16`) explicitly enforces `assert_orchestrator_image_contract`, asserting that `main.bicep` `orchestratorImage` defaults to `""` and forwards `'mcr.microsoft.com/k8se/quickstart:latest'` when empty so stage-1 bootstrap (`deployApplications=false` before ACR exists) and `.bicepparam` compilation succeed, and includes mutation tests that fail if `defaultValue` or forwarding changes!
  2. `infra/tests/test_from_empty_reproducibility_136.py` + `infra/scripts/reproducibility_check.py:124-135` assert that `main.bicep` defaultless parameters equal `("alertEmail", "sqlAdminGroupName", "sqlAdminGroupObjectId")`.
  3. `infra/tests/test_bicep_architecture_inventory_136.py:199-203` (`C19`) explicitly asserts `self.assertTrue(self.bicep_tree.placeholder_workers)` and `Delivery status == "delivered-placeholder-workers"` while `main.bicep` retains bootstrap-only parameter defaults.
  4. Also inspected `infra/tests/test_pipeline.py:667` (`C17`): PR `plan` fixture uses `example.azurecr.io/{project}@sha256:{"b"*64}` (e.g. `example.azurecr.io/api@sha256:...`), so `pipeline.deployment()` PR `plan` validation must require `<registry>/<repo>@sha256:[0-9a-f]{64}` while rejecting `quickstart` / placeholder repositories, without hardcoding `zava-forward-` prefix on pre-existing test fixtures in `plan` mode (`release_images` and `verify_release_manifest` continue to enforce exact `{server}/zava-forward-{project}@sha256:[0-9a-f]{64}`).
* Also found concrete missing coverage in existing `infra/tests/` (`C16`, `C17`, `C18`):
  * `infra/tests/test_container_hosting_completeness.py:34-43` (`C18`) omits `modules/containerapps.bicep:tokenRenewal`, `modules/containerapps.bicep:rankingPublish`, `live-receiver-job.bicep:job`, and `live-simulator-job.bicep:job` from its inventory assertion.
  * `infra/tests/test_bicep_policy.py:898` omits `ranking-publish` in `assert_hosting_limits_and_rollout` job container assertions.
  * `infra/tests/test_container_hosting_144.py:322-375` expects `"import": ("[parameters('importImage')]", None, None)` instead of explicit `["python", "-m", "zava_forward.importer"]` + `["run"]`, and lacks tests for `importer run` mode, `demoDirectIngress=true` shortened resource names/scaling parity (`ca-${prefix}-demo-api`, `ca-${prefix}-work`, `job-${prefix}-orch`, `job-${prefix}-auth`, `job-${prefix}-audit`, `job-${prefix}-rank-publish`, `job-${prefix}-load`), `TMPDIR=/tmp` + root-owned `/app` invariants across all Dockerfiles, and `release-manifest.json` generation/tamper rejection.

## Canonical Evidence Log

| ID  | Source (`path:line`)                                               | Finding summary                                                                                                   | State    |
|-----|--------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------|----------|
| C1  | `src/api/Dockerfile:1-34`                                          | Multi-stage digest-pinned `python@sha256:34386ef...`, `USER 10001:10001`, `/app` root-owned, `/state` `10001:10001`, lacks `TMPDIR=/tmp` in `ENV` | Verified |
| C2  | `src/agents/Dockerfile:1-26`                                       | Digest-pinned, no SQL/Blob extras, `USER 10001:10001`, `/state` `10001:10001`, lacks `TMPDIR=/tmp` in `ENV`        | Verified |
| C3  | `src/orchestrator/Dockerfile:1-29`                                 | Digest-pinned, real hashed wheels, `USER 10001:10001`, `/state` `10001:10001`, lacks `TMPDIR=/tmp` in `ENV`        | Verified |
| C4  | `src/importer/Dockerfile:1-28`                                     | Digest-pinned, real hashed wheels, `USER 10001:10001`, `/state` `10001:10001`, lacks `TMPDIR=/tmp` in `ENV`        | Verified |
| C5  | `infra/modules/containerapps.bicep:115-560`                        | `hardeningEnv`, `scratchVolumes` (`/tmp`, `/state` `EmptyDir`), `activeRevisionsMode: 'Single'`, HTTP/queue scale rules, and explicit `command`/`args` on `agents`, `orchestrator`, `tokenRenewal`, `ledgerVerify`, `rankingPublish` | Verified |
| C6  | `infra/modules/containerapps.bicep:55-61,561-621`                  | `importJob` lacks `command`/`args` override; image parameters lack `@minLength(1)`                                | Verified |
| C7  | `src/api/Dockerfile.resident-demo:1-34`, `src/api/live-simulator.Dockerfile:1-31` | Digest-pinned `USER 10001:10001` auxiliary images; lack `TMPDIR=/tmp` in `ENV`                        | Verified |
| C8  | `src/core/src/zava_forward/core/container_hardening.py:1-190`      | Fail-closed `enforce_container_hardening` / `enforce_from_env` verifying `10001:10001`, `umask 0o077`, `NoNewPrivs=1`, zero capability sets, immutable `/` + `/app`, writable `/tmp` + `/state` | Verified |
| C9  | `src/orchestrator/src/zava_forward/orchestrator/__main__.py:1-90`  | Calls `enforce_from_env()`, supports no-arg version check and bounded `run` mode validating `TASK_QUEUE`, `QUEUE_ENDPOINT`, `API_BASE_URL` | Verified |
| C10 | `src/importer/src/zava_forward/importer/__main__.py:181-235`       | Calls `enforce_from_env()`, supports `preview`/`stage`/`exceptions`/`transfer` and no-arg version output, but lacks bounded `run` job subcommand | Verified |
| C11 | `src/check-container.py:12-88`                                     | Verifies `--read-only --cap-drop=ALL --security-opt=no-new-privileges`, `10001:10001`, zero caps, `NoNewPrivs=1`, `/app` `EROFS`, `/state` write, and no-arg `CMD` version string | Verified |
| C12 | `infra/scripts/pipeline.py:363-404,540-605`                        | `publish` and `release_images` bind immutable `@sha256:` digests per project, but no aggregated release manifest contract exists and PR `plan` mode only checks `"@sha256:" in image` | Verified |
| C13 | `infra/scripts/deploy.py:55-122,190-225`                           | Resolves `orchestratorImage` across all 4 orchestrator jobs (`orchestrator`, `auth-renewal`, `ledger-verify`, `rank-publish`), warns on bootstrap placeholder | Verified |
| C14 | `infra/scripts/bicep_inventory.py:249-260`                         | Computes `apps_missing_worker_cmd` from `_resource_block_has_command(..., "orchestrator")` and `_resource_block_has_command(..., "importJob")` | Verified |
| C15 | `infra/scripts/staff_azure.py:319-356`                             | Dynamic `job-staff-*` ARM job spec omits `PYTHONDONTWRITEBYTECODE=1`, `TMPDIR=/tmp`, `ZF_STATE=/state`, and `/tmp` + `/state` `EmptyDir` scratch volumes | Verified |
| C16 | `infra/tests/test_bicep_policy.py:895-915,1044-1089`               | Enforces `main.bicep` `orchestratorImage` empty-to-quickstart bootstrap contract; omits `ranking-publish` in line 898 job list | Verified |
| C17 | `infra/tests/test_pipeline.py:580-715`, `infra/tests/test_deploy.py:162-170` | Tests `pipeline.py` release binding and PR `plan` (`example.azurecr.io/{project}@sha256:...`); `test_deploy.py` omits `rank-publish` in job loop | Verified |
| C18 | `infra/tests/test_container_hosting_completeness.py:34-105`, `infra/tests/test_container_hosting_144.py:1-520` | Existing `#144` tests; missing `importJob` `run` command, `demoDirectIngress` parity, full workload inventory, Dockerfile `TMPDIR=/tmp` + ownership checks, and release manifest bundle tests | Verified |
| C19 | `infra/tests/test_bicep_architecture_inventory_136.py:199-245`, `infra/README.md:3945` | Asserts `bicep_tree.placeholder_workers` remains `True` while `main.bicep` preserves stage-1 bootstrap parameter defaults | Verified |

## Alternatives Evaluated

1. **Selected Recommendation — Surgical contract closure across `importer`, `containerapps.bicep`, `src/` Dockerfiles, `staff_azure.py`, `pipeline.py` release manifests, and `infra/tests/` while preserving `main.bicep` stage-1 bootstrap defaults**:
   * Add bounded `run` subcommand to `zava_forward.importer.__main__` (preserving no-arg version output for `src/check-container.py`, validating `IMPORT_QUEUE`, `https` `QUEUE_ENDPOINT`/`BLOB_ENDPOINT`, `SQL_SERVER`/`SQL_DATABASE` under `ZF_STORE=mssql`, and gated `ZF_IMPORT_DISPATCH` standby) and wire `command: ['python', '-m', 'zava_forward.importer']`, `args: ['run']`, and `@minLength(1)` image params in `infra/modules/containerapps.bicep` (turning `apps_missing_worker_cmd` to `False` in `bicep_inventory.py` while keeping `main.bicep` bootstrap defaults compatible with `#136` and `test_bicep_policy.py`).
   * Add `TMPDIR=/tmp` to `ENV` across all 6 `src/` Dockerfiles (`api`, `agents`, `orchestrator`, `importer`, `Dockerfile.resident-demo`, `live-simulator.Dockerfile`) and add `PYTHONDONTWRITEBYTECODE=1`, `TMPDIR=/tmp`, `ZF_STATE=/state`, and `EmptyDir` `/tmp` + `/state` scratch mounts to dynamic `job-staff-*` jobs in `infra/scripts/staff_azure.py`.
   * Add deterministic release manifest assembly and verification (`build_release_manifest` / `verify_release_manifest` writing `release-manifest.json` in `release_images`) in `infra/scripts/pipeline.py`, tighten PR `plan` image validation in `pipeline.deployment()` to require valid 64-hex `@sha256:` digests and reject `quickstart`/placeholder images, and reject placeholder/mutable `:latest` explicit `--orchestrator-image` overrides when `--apply` is requested in `infra/scripts/deploy.py`.
   * Update `infra/README.md` notes honestly (preserving live Azure deployment boundaries and `#136` table invariants) and expand deterministic tests in `infra/tests/test_container_hosting_144.py`, `test_container_hosting_completeness.py`, `test_bicep_policy.py`, `test_pipeline.py`, `test_deploy.py`, and `test_staff_azure.py` (plus unit tests in `src/importer/tests/`).
2. **Rejected Alternative A — Remove `mcr.microsoft.com/k8se/quickstart:latest` defaults from `infra/main.bicep`**:
   * Rejected because `test_bicep_policy.py:1044-1089` (`C16`), `reproducibility_check.py:124-135`, and `test_bicep_architecture_inventory_136.py:199-203` (`C19`) explicitly enforce stage-1 dependency bootstrap parameter defaults in `main.bicep` before ACR exists, while `pipeline.py` injects immutable `@sha256:` release manifests for every workload deployment.
3. **Rejected Alternative B — Add unsupported `securityContext` properties to `Microsoft.App/containerApps@2025-07-01` Bicep**:
   * Rejected because ARM `Microsoft.App/containerApps@2025-07-01` and `Microsoft.App/jobs@2025-07-01` reject unknown `securityContext` container fields at `az bicep build` compile time; Zava Forward's 3-layer hardening contract (Dockerfile `USER 10001:10001` + root-owned `/app` + Docker `--read-only --cap-drop=ALL --security-opt=no-new-privileges` in CI + Bicep `ZF_CONTAINER_HARDENING=enforced` & `EmptyDir` `/tmp`+`/state` mounts + runtime `enforce_from_env()` kernel `/proc/self/status` & `PR_SET_NO_NEW_PRIVS` enforcement) compiles cleanly and fails closed at startup.

## Risks, Boundaries, and Potential Further Research

* Live Azure boundary: Local static/unit/compiled-Bicep verification proves repository contract completeness and fail-closed startup enforcement; live Azure rollout and deployed runtime verification remain gated on authorized operator execution (`Refs #144`).
* Test performance boundary: Full 36-file `unittest discover -s infra/tests` repeatedly shells out to `az bicep build`; during implementation and review, always prefix test commands with `TMPDIR=/dev/shm` and run targeted modified/coupled test modules plus `ruff` and `mypy`.
* Potential further research: None required; Cycle 1 achieved full source coverage with zero unresolved blockers.

## Readiness and Handoff

* Research disposition: `executed`
* Planning Readiness: `Ready`
* Self-check:
  * Cycle 1 completed Wider -> Deeper -> Contrarian waves in order: Yes.
  * Every codebase claim maps to `C1`-`C19` with `path:line`: Yes.
  * Research-only constraint honored (zero source files edited during Research): Yes.


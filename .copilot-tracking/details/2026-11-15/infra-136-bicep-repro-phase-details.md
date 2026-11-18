<!-- markdownlint-disable-file -->
# RPI Phase Details: Issue 136 From-Empty Bicep Deployment Reproducibility

## Metadata

* Task ID: infra-136-bicep-repro
* Task slug: infra-136-bicep-repro
* Related plan: .copilot-tracking/plans/2026-11-15/infra-136-bicep-repro-plan.md
* Evidence sources: .copilot-tracking/research/2026-11-15/infra-136-bicep-repro-research.md (`C1`-`C22`), `infra/scripts/pipeline.py`, `infra/main.bicep`, `infra/modules/guard.bicep`, `infra/main.bicepparam`, `infra/main.pilot.example.bicepparam`, `infra/scripts/bicep_inventory.py`, `src/orchestrator/src/zava_forward/orchestrator/rebuild.py`, `infra/README.md`

## Phase Index

| Phase ID | Name                                                                               | Status   | Detail sections        |
|----------|------------------------------------------------------------------------------------|----------|------------------------|
| P01      | Add Environment Parameter Templates (`infra/parameters/*.bicepparam`)              | Complete | P01, P01-T01           |
| P02      | Register Canonical Steps and Implement Deterministic Reproducibility Verifier      | Complete | P02, P02-T01, P02-T02  |
| P03      | Document Canonical From-Empty Step Registry in `infra/README.md`                   | Complete | P03, P03-T01           |
| P04      | Author Focused Unit & Mutation Tests, Validate, and Commit Cleanly                 | Complete | P04, P04-T01           |

<!-- rpi:phase id=P01 -->
## P01: Add Environment Parameter Templates (`infra/parameters/*.bicepparam`)

### Context

Research (`C7`-`C10`, `C14`-`C16`) showed that `infra/main.bicep` declares 61 parameters, of which exactly three have no default value (`alertEmail`, `sqlAdminGroupName`, `sqlAdminGroupObjectId`), while root parameter files sit at `infra/main.bicepparam` (`dev`), `infra/main.test.bicepparam` (`test`), and `infra/main.pilot.example.bicepparam` (`pilot` / `production` profile), and `infra/parameters/` does not yet exist. Criterion (b) explicitly checks `infra/parameters/dev.bicepparam` and `infra/parameters/prod.bicepparam` alongside `infra/scripts/pipeline.py` parameter injection.

### Intent

Provide canonical, compilable `infra/parameters/dev.bicepparam` and `infra/parameters/prod.bicepparam` files (`using '../main.bicep'`) that supply all defaultless parameters of `infra/main.bicep`, uphold every isolation and non-deployable placeholder rule in the repository, and coexist cleanly with `infra/main*.bicepparam`.

### Boundaries

* Included: Creating `infra/parameters/dev.bicepparam` and `infra/parameters/prod.bicepparam` and verifying offline compilation with `az bicep build-params`.
* Excluded: Altering `infra/main.bicep`, `infra/main.bicepparam`, `infra/main.test.bicepparam`, or `infra/main.pilot.example.bicepparam`, or creating `infra/main.pilot.bicepparam` (forbidden by `test_governance.py`).

### Likely Targets

* `infra/parameters/dev.bicepparam`: Canonical dev environment `.bicepparam` template (`using '../main.bicep'`).
* `infra/parameters/prod.bicepparam`: Canonical production-profile `.bicepparam` template (`using '../main.bicep'`).

### Dependencies

* None.

### Validation Expectations

* `az bicep build-params --file infra/parameters/dev.bicepparam --stdout` and `az bicep build-params --file infra/parameters/prod.bicepparam --stdout` both exit `0` and emit valid ARM `parametersJson`.
* Existing governance and credential-hygiene suites (`infra/tests/test_governance.py` and `src/api/tests/test_iot_credential_hygiene.py` rules) pass without issue.

### Completion Evidence

* Both files exist on disk, compile cleanly with `az bicep build-params`, contain `NON-DEPLOYABLE EXAMPLE` / `PLACEHOLDER` markers and zero secrets, keep `allowPublicNetworkAccess = false` and `apiMinReplicas = 0`, and supply `alertEmail`, `sqlAdminGroupName`, and `sqlAdminGroupObjectId`.

### Unresolved Items

* None.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Author `infra/parameters/dev.bicepparam` and `infra/parameters/prod.bicepparam`

#### Context

`infra/main.bicep` enforces `@allowed(['dev', 'test', 'pilot']) param environmentName` and `@allowed(['production', 'development']) param deploymentProfile`, while `infra/modules/guard.bicep` requires `deploymentProfile == 'production'` and `enableLocks == true` when `environmentName == 'pilot'` (`C7`, `C14`). In addition, `src/api/tests/test_iot_credential_hygiene.py` and `src/core/src/zava_forward/core/synthetic/cutover_audit.py` scan all `.bicepparam` files for secrets and retired identifiers (`C16`).

#### Intent

Create `infra/parameters/dev.bicepparam` and `infra/parameters/prod.bicepparam` matching the repository's dev (`main.bicepparam`) and production-profile (`main.pilot.example.bicepparam`) contracts.

#### Boundaries

* Included:
  * `infra/parameters/dev.bicepparam`: `using '../main.bicep'`, `NON-DEPLOYABLE EXAMPLE` + `PLACEHOLDER` header comments, `workload = 'forward'`, `environmentName = 'dev'`, `location = 'uksouth'`, `sqlLocation = 'uksouth'`, `regionCheckReference = '' // PLACEHOLDER`, `quotaCheckReference = '' // PLACEHOLDER`, `alertEmail = 'platform-alerts@example.invalid' // PLACEHOLDER`, `sqlAdminGroupName = 'sg-zava-forward-sql-admins' // PLACEHOLDER`, `sqlAdminGroupObjectId = '00000000-0000-0000-0000-000000000000' // PLACEHOLDER`, `entraClientId = '' // PLACEHOLDER`, `deploymentProfile = 'development'`, `allowPublicNetworkAccess = false`, `apiMinReplicas = 0`, `enableLocks = false`, `keyVaultPurgeProtection = false`, `registryQuarantineEnabled = false`, explicit quota/SQL/IoT/Foundry settings matching `infra/main.bicepparam` (zero `"chat"` substrings and zero retired `mvp/`/`prototype/`/`zavaforward_mvp` tokens per `PC-004`).
  * `infra/parameters/prod.bicepparam`: `using '../main.bicep'`, `NON-DEPLOYABLE EXAMPLE` + `PLACEHOLDER` header comments, `workload = 'forward'`, `environmentName = 'pilot'`, `location = '' // PLACEHOLDER`, `sqlLocation = '' // PLACEHOLDER`, `regionCheckReference = '' // PLACEHOLDER`, `quotaCheckReference = '' // PLACEHOLDER`, `alertEmail = 'platform-alerts@example.invalid' // PLACEHOLDER`, `sqlAdminGroupName = 'sg-zava-forward-sql-admins' // PLACEHOLDER`, `sqlAdminGroupObjectId = '00000000-0000-0000-0000-000000000000' // PLACEHOLDER`, `entraClientId = '' // PLACEHOLDER`, `deploymentProfile = 'production'`, `allowPublicNetworkAccess = false`, `apiMinReplicas = 0`, `enableLocks = true`, `keyVaultPurgeProtection = true`, `registryQuarantineEnabled = true`, `sqlTier = 'provisioned'`, explicit quota/SQL/IoT/Foundry settings matching `infra/main.pilot.example.bicepparam` (zero `"chat"` substrings, zero `"AutoPause"` substrings, and zero retired tokens per `PC-004`).
* Excluded: Modifying existing root `.bicepparam` files.

#### Likely Targets

* `infra/parameters/dev.bicepparam`
* `infra/parameters/prod.bicepparam`

#### Dependencies

* None.

#### Validation Expectations

* Both files compile cleanly via `az bicep build-params --file ... --stdout`.

#### Completion Evidence

* Compiled JSON contains all three defaultless `infra/main.bicep` parameters (`alertEmail`, `sqlAdminGroupName`, `sqlAdminGroupObjectId`).

#### Unresolved Items

* None.

<!-- rpi:phase id=P02 -->
## P02: Register Canonical Steps and Implement Deterministic Reproducibility Verifier & Dry-Run

### Context

Research (`C1`, `C2`, `C11`, `C12`, `C17`, `C18`) established two crucial compatibility constraints:
1. `bicep_inventory.load_pipeline_operations` AST-parses `parser.add_argument("operation", choices=...)` in `infra/scripts/pipeline.py`, and `test_bicep_architecture_inventory_136.py` asserts `self.pipeline_ops == ("plan", "deploy", "publish", "changed-images", "verify-environment")`.
2. `test_pipeline.py` and `test_environment_quota_parameters.py` load `infra/scripts/pipeline.py` via `importlib.util.spec_from_file_location` without `infra/scripts` on `sys.path`.

### Intent

Register the canonical 6-step from-empty deployment pipeline (`preflight`, `what-if`, `deploy`, `sql-init`, `seed`, `smoke`), `ENVIRONMENT_PARAMETER_FILES`, and `INJECTED_PARAMETERS` in `infra/scripts/pipeline.py`, and implement the pure-stdlib deterministic reproducibility verifier and offline 6-step dry-run executor in `infra/scripts/reproducibility_check.py` (with lazy `spec_from_file_location` re-export in `infra/scripts/pipeline.py`).

### Boundaries

* Included: Updating `infra/scripts/pipeline.py` and creating `infra/scripts/reproducibility_check.py` (without executable shebang on the non-chmodded file so user-level `EXE001` never triggers).
* Excluded: Changing existing positional `operation` choices or runtime CLI behavior of `pipeline.py` (`plan`, `deploy`, `publish`, `changed-images`, `verify-environment`).

### Likely Targets

* `infra/scripts/pipeline.py`: Canonical step registry, parameter injection constants, and lazy delegating `verify_from_empty_deployment_reproducibility` / `execute_from_empty_dry_run` entrypoints.
* `infra/scripts/reproducibility_check.py`: Full static verifier (steps, README, Bicep defaultless params, `.bicepparam` assignments, AST-checked `pipeline.py` injections), deterministic offline 6-step dry-run engine, and `--check` / `--dry-run` / `--json` CLI.

### Dependencies

* P01 (`infra/parameters/dev.bicepparam` and `infra/parameters/prod.bicepparam`).

### Validation Expectations

* `mypy --strict --no-incremental --cache-dir=/dev/null infra/scripts/pipeline.py infra/scripts/reproducibility_check.py` exits `0`.
* Bare `ruff check` and `--isolated` CI `ruff check` + `ruff format --check` exit `0` on both files.
* Existing `test_pipeline.py`, `test_environment_quota_parameters.py`, and `test_bicep_architecture_inventory_136.py` pass unchanged.

### Completion Evidence

* `verify_from_empty_deployment_reproducibility` and `execute_from_empty_dry_run` are importable and callable from both `infra/scripts/pipeline.py` and `infra/scripts/reproducibility_check.py`.

### Unresolved Items

* None.

<!-- rpi:task id=P02-T01 -->
### P02-T01: Register `FROM_EMPTY_STEPS`, `ENVIRONMENT_PARAMETER_FILES`, `INJECTED_PARAMETERS`, and verifier entrypoints in `infra/scripts/pipeline.py`

#### Context

`infra/scripts/pipeline.py` already owns `PARAMETER_FILES`, `OVERRIDES`, `IMAGE_PARAMETERS`, `parameters()`, `verify_environment()`, `summarize_plan()`, `deployment()`, `check_sql()`, and `smoke()`. Adding typed metadata constants and delegating entrypoints registers the complete from-empty pipeline sequence directly in `pipeline.py` without perturbing CLI `operation` choices (`C1`, `C2`, `C11`, `C12`).

#### Intent

Expose structured canonical step registration and reproducibility entrypoints in `infra/scripts/pipeline.py`.

#### Boundaries

* Included:
  * `@dataclass(frozen=True) class FromEmptyStep`: fields `step_id: str`, `pipeline_hook: str`, `rebuild_stages: tuple[str, ...]`, `artifacts: tuple[str, ...]`, `manual_prerequisite_owner: str | None`, `description: str`. Keep eager Python 3.12 type annotations in `infra/scripts/pipeline.py` — do NOT add `from __future__ import annotations`, so `test_pipeline.py`'s `spec_from_file_location` load without `"pipeline"` in `sys.modules` succeeds (`PC-001`).
  * `FROM_EMPTY_STEP_ORDER: tuple[str, ...] = ("preflight", "what-if", "deploy", "sql-init", "seed", "smoke")`.
  * `FROM_EMPTY_STEPS: tuple[FromEmptyStep, ...]` covering all 6 canonical steps in exact order and partitioning all 17 canonical `rebuild.py` stages:
    1. `preflight` (`pipeline_hook="verify-environment"`, `rebuild_stages=("parameters",)`, `artifacts=("infra/scripts/pipeline.py", "infra/scripts/tenant-readiness-preflight.py", "infra/entra/app-registration.json", "infra/secret-inventory.json", "infra/defender-decision.json")`, `manual_prerequisite_owner="Juan Manuel Servera (@jmservera)"`)
    2. `what-if` (`pipeline_hook="plan"`, `rebuild_stages=("dependencies",)`, `artifacts=("infra/main.bicep", "infra/governance.bicep", "infra/parameters/dev.bicepparam", "infra/parameters/prod.bicepparam", "infra/scripts/deploy.py", "infra/scripts/pipeline.py")`, `manual_prerequisite_owner=None`)
    3. `deploy` (`pipeline_hook="publish,deploy"`, `rebuild_stages=("discover", "images", "credential", "applications", "authentication")`, `artifacts=("infra/main.bicep", "infra/modules/containerapps.bicep", "src/api/Dockerfile", "src/agents/Dockerfile", "src/orchestrator/Dockerfile", "src/importer/Dockerfile", "infra/scripts/deploy.py", "infra/scripts/pipeline.py", "infra/scripts/setup-entra.py", "infra/scripts/credential_arm.py")`, `manual_prerequisite_owner=None`)
    4. `sql-init` (`pipeline_hook="check_sql"`, `rebuild_stages=("sql-users",)`, `artifacts=("infra/scripts/create-sql-users.py", "infra/scripts/create-sql-users.sql", "infra/sql/resident-showcase.sql", "infra/sql/resident-assistant.sql", "infra/staff-initializer-rbac.bicep")`, `manual_prerequisite_owner=None`)
    5. `seed` (`pipeline_hook="seed"`, `rebuild_stages=("seed", "staff")`, `artifacts=("src/importer/Dockerfile", "src/orchestrator/src/zava_forward/orchestrator/rebuild_azure.py", "infra/scripts/resident_sensor_seed.py", "infra/scripts/initialize-workbench-staff.py")`, `manual_prerequisite_owner=None`)
    6. `smoke` (`pipeline_hook="smoke"`, `rebuild_stages=("health", "api-denial", "browser-redirect", "workload-sql", "model-standard", "model-capable", "restart")`, `artifacts=("infra/scripts/pipeline.py", "infra/scripts/private-cutover-proof.py", "src/orchestrator/src/zava_forward/orchestrator/rebuild.py", "src/orchestrator/src/zava_forward/orchestrator/rebuild_azure.py")`, `manual_prerequisite_owner=None`)
  * `ENVIRONMENT_PARAMETER_FILES = {"dev": "parameters/dev.bicepparam", "prod": "parameters/prod.bicepparam"}`.
  * `INJECTED_PARAMETERS: frozenset[str] = frozenset(OVERRIDES | {"workload", "environmentName", "allowPublicNetworkAccess", "deployApplications"} | set(IMAGE_PARAMETERS.values()))`.
  * Lazy `_load_reproducibility_module()` helper using `importlib.util.spec_from_file_location` against `Path(__file__).resolve().with_name("reproducibility_check.py")` that sets `sys.modules[spec.name] = mod` BEFORE `spec.loader.exec_module(mod)` (`PC-001`), plus typed `verify_from_empty_deployment_reproducibility(repo_root: Path = ROOT) -> Any` and `execute_from_empty_dry_run(repo_root: Path = ROOT, environment: str = "dev") -> Any`.
* Excluded: Modifying `main()` positional `operation` choices or existing helper signatures.

#### Likely Targets

* `infra/scripts/pipeline.py`

#### Dependencies

* None.

#### Validation Expectations

* `mypy --strict infra/scripts/pipeline.py` and `infra/tests/test_pipeline.py` pass completely.

#### Completion Evidence

* `pipeline.FROM_EMPTY_STEPS`, `pipeline.INJECTED_PARAMETERS`, `pipeline.verify_from_empty_deployment_reproducibility`, and `pipeline.execute_from_empty_dry_run` are defined and typed.

#### Unresolved Items

* None.

<!-- rpi:task id=P02-T02 -->
### P02-T02: Implement `infra/scripts/reproducibility_check.py` static verifiers, deterministic offline dry-run executor, and CLI

#### Context

`reproducibility_check.py` implements the three sub-proofs required by Issue `#136`:
* (a) Step registration in `pipeline.py` + README documentation parity + zero undocumented manual steps;
* (b) Defaultless `infra/main.bicep` parameter coverage across `infra/parameters/dev.bicepparam` / `prod.bicepparam` or explicit injection in `infra/scripts/pipeline.py`;
* (c) Deterministic offline execution of the full 6-step sequence from repository files alone.

#### Intent

Build a fast, pure-stdlib, `--strict`-typed module and CLI with clean composable functions so unit and mutation tests can exercise both end-to-end repository verification and isolated synthetic mutations.

#### Boundaries

* Included:
  * **Bicep & `.bicepparam` Parsers**:
    * `parse_bicep_parameters(bicep_text: str) -> tuple[BicepParamDecl, ...]`: strips `//` line comments and `/* ... */` block comments (respecting `'...'` string literals), tracks `[]` / `{}` / `()` nesting depth across multi-line declarations (such as `param modelDeployments array = [...]`), and records `name`, `param_type`, `has_default`, and `is_secure` (`@secure()`).
    * `parse_bicepparam_file(param_path: Path, repo_root: Path) -> BicepparamSummary`: strips `//` and `/* ... */` comments outside single-quoted strings, parses `using '...'` target path, tracks `[]` / `{}` / `()` bracket depth across multi-line `param <name> = <expr>` assignments (parsing comma-free Bicep array/object blocks such as `modelDeployments` as well as string/bool/int literals purely in Python stdlib with zero `az` calls per `PC-004`), checks for forbidden raw secret patterns on `param` lines, and validates the resolved `using` target equals `infra/main.bicep`.
  * **Pipeline AST Verifier**:
    * `extract_pipeline_injected_parameters(pipeline_source: str) -> tuple[frozenset[str], list[str]]`: parses `infra/scripts/pipeline.py` with `ast` to extract keys in `OVERRIDES`, string keys in `IMAGE_PARAMETERS.values()`, and string keys written inside `parameters()` `values.update({...})`, verifying exact equality with `pipeline.INJECTED_PARAMETERS` so declared metadata cannot drift from executable injection logic. Custom `spec_from_file_location` module loading in `reproducibility_check.py` registers `sys.modules[spec.name] = mod` prior to `exec_module` (`PC-001`).
  * **Check (a) — Step Registration & Zero Undocumented Manual Steps (`verify_step_registration_and_docs`)**:
    * Verifies `[s.step_id for s in pipeline_steps] == ["preflight", "what-if", "deploy", "sql-init", "seed", "smoke"]`.
    * Parses `### Canonical from-empty pipeline step registry` from `infra/README.md` with expected columns `("Step", "Pipeline registration", "Rebuild stage(s)", "Repository template or script", "Manual prerequisites", "Verification check")`.
    * Verifies exact 6-row step order parity between `pipeline.FROM_EMPTY_STEPS` and the README table, verifies every artifact listed in `pipeline.FROM_EMPTY_STEPS` and in the README table exists as a regular file under `repo_root`, verifies per-step ordered `rebuild_stages` tuple equality between each README row and `pipeline.FROM_EMPTY_STEPS` (preserving relative `rebuild.py` order within each step) plus an exact disjoint 17-stage set partition across `rebuild.py` `STAGES` (`len(observed) == len(rebuild_stages)` with zero duplicates and `frozenset(observed) == frozenset(rebuild_stages)` per `PC-002`), and enforces **zero undocumented manual steps**:
      * Rejects empty/placeholder cells (`""`, `"tbd"`, `"todo"`, `"none"`, `"n/a"`, `"manual"`, `"undocumented"`, `"pending"`, `"unknown"`) in `Pipeline registration`, `Rebuild stage(s)`, `Repository template or script`, `Manual prerequisites`, and `Verification check` (except explicit `"none (automated from repository files)"` in `Manual prerequisites` for fully automated steps).
      * Requires any step with non-`none` `Manual prerequisites` (`preflight` only) to name a concrete human owner (`@jmservera` / `Servera`) in both `pipeline.FROM_EMPTY_STEPS` and `infra/README.md`; rejects any manual prerequisite on automated steps (`what-if`, `deploy`, `sql-init`, `seed`, `smoke`) unless paired with a repository script and explicit named owner, and scans section prose for forbidden undocumented-manual phrases (`"undocumented"`, `"manual workaround"`, `"ad-hoc step"`, `"run manually in portal"`).
  * **Check (b) — Defaultless Parameter Coverage (`verify_bicep_parameter_coverage`)**:
    * Dynamically identifies all `BicepParamDecl` entries in `infra/main.bicep` with `has_default == False`.
    * Verifies `infra/parameters/dev.bicepparam` and `infra/parameters/prod.bicepparam` (plus root `main.bicepparam`, `main.test.bicepparam`, `main.pilot.example.bicepparam` when verifying the live repo) exist, resolve `using` to `infra/main.bicep`, assign zero unknown parameters not declared in `infra/main.bicep`, and contain zero raw secret literals.
    * Enforces for every defaultless parameter `p` in `infra/main.bicep`: `(p in dev_params and p in prod_params) or (p in pipeline_injected_params)`, recording how each defaultless parameter is satisfied (`"bicepparam+pipeline"`, `"bicepparam"`, or `"pipeline"`). Fails closed with an explicit error naming `p` whenever `p` is missing from `dev.bicepparam` or `prod.bicepparam` AND absent from `pipeline_injected_params`.
  * **Check (c) — Deterministic Offline Full-Sequence Dry-Run (`execute_from_empty_dry_run`)**:
    * Accepts `repo_root: Path` and `environment: str = "dev"` (`"dev"` uses `infra/parameters/dev.bicepparam` with runtime environment `"dev"`; `"prod"` uses `infra/parameters/prod.bicepparam` with runtime environment `"pilot"` matching `environmentName = 'pilot'`).
    * Runs all 6 steps in strict order `("preflight", "what-if", "deploy", "sql-init", "seed", "smoke")` using **only** files under `repo_root` and isolated in-process `unittest.mock.patch` adapters around `pipeline.py`: patches `PARAMETER_FILES` on the loaded `pipeline` module to `{"dev": "parameters/dev.bicepparam", "pilot": "parameters/prod.bicepparam"}`, parses the exact `--file` path received by the in-memory `az("bicep", "build-params", "--file", path, "--stdout")` stub via `parse_bicepparam_file`, isolates `os.environ` via `patch.dict(os.environ, synthetic_env, clear=True)` (omitting `GITHUB_STEP_SUMMARY` and serializing `DEPLOY_PARAMETERS` with `sort_keys=True` per `PC-003`), and patches `subprocess.run` to raise `AssertionError("Offline dry-run must not spawn subprocesses")`:
      1. `preflight`: Reads `infra/entra/app-registration.json`, `infra/secret-inventory.json`, `infra/defender-decision.json`, and `infra/scripts/tenant-readiness-preflight.py`, verifies JSON contracts (`ZavaForward.*` app roles, named secret owners, `DoNotEnforce` / `enableDefenderPlans == false` governance baseline), and invokes `pipeline.verify_environment(f"{runtime_env}-release")` against a deterministic in-memory `gh api` fixture.
      2. `what-if`: Builds the offline ARM `parametersJson` payload from the parsed `.bicepparam` file, invokes `pipeline.parameters(infra_dir, runtime_env)` with deterministic synthetic `DEPLOY_PARAMETERS` and offline `az bicep build-params` adapter, and invokes `pipeline.summarize_plan(...)` over a deterministic ARM `what-if` change list derived from `infra/main.bicep`'s provisioned resource types inside `/subscriptions/00000000-0000-0000-0000-000000000001/resourceGroups/ama/providers/...` (verifying `Microsoft.Sql/servers` `publicNetworkAccess == "Disabled"`).
      3. `deploy`: Verifies all 4 workload Dockerfiles (`src/{api,agents,orchestrator,importer}/Dockerfile`) exist and declare wheel builds, materializes deterministic `sha256:` image digests hashed from those repository Dockerfiles + `infra/main.bicep` in a temporary workspace, invokes `pipeline.deployment(infra_dir, runtime_env, summary_out, images_dir)` against deterministic in-memory `az` / `run` / `smoke` adapters, and verifies `deployment_status == "Succeeded"` and deterministic `parameter_sha256`.
      4. `sql-init`: Reads `infra/scripts/create-sql-users.sql`, `infra/scripts/create-sql-users.py`, `infra/sql/resident-showcase.sql`, `infra/sql/resident-assistant.sql`, and `infra/staff-initializer-rbac.bicep`, verifies idempotent contained principal creation (`CREATE USER` + `db_datareader`/`db_datawriter`/`db_ddladmin`) and executes `pipeline.check_sql()` against the offline private SQL state (`publicNetworkAccess == "Disabled"`).
      5. `seed`: Reads `infra/scripts/resident_sensor_seed.py`, `infra/scripts/initialize-workbench-staff.py`, and `src/orchestrator/src/zava_forward/orchestrator/rebuild_azure.py`, verifying idempotent `IF OBJECT_ID` table guards, non-reseed invariants, and deterministic synthetic seed contract digest.
      6. `smoke`: Invokes `pipeline.smoke("https://ca-forward-dryrun-api.internal.uksouth.azurecontainerapps.io", attempts=1, delay=0, browser=True)` against an in-process deterministic `urllib.request.OpenerDirector` stub (suppressing stdout via `contextlib.redirect_stdout`), verifying all 5 probes (`/healthz` `200`, anonymous `/api/me` `401`, malformed bearer `/api/me` `401`, forged `X-MS-CLIENT-PRINCIPAL` `/api/me` `401`, `/sign-in` `302`) run in exact order.
    * Computes `sequence_digest` as `hashlib.sha256` over canonical `sort_keys=True` JSON of the 6 `StepExecutionRecord` objects (each containing `step_id`, `status`, `pipeline_hook`, `verified_artifacts`, `artifact_sha256`, and `checks_passed` — zero temp paths, timestamps, or random values).
    * `verify_from_empty_deployment_reproducibility(repo_root)` runs Check (a), Check (b), and Check (c) (executing `"dev"` twice and `"prod"` twice and asserting `run1 == run2` and `run1.sequence_digest == run2.sequence_digest`!) and returns a frozen `ReproducibilityReport`.
* Excluded: Network access, Azure authentication, or mutations to repository files.

#### Likely Targets

* `infra/scripts/reproducibility_check.py`

#### Dependencies

* P01-T01, P02-T01.

#### Validation Expectations

* `python3 infra/scripts/reproducibility_check.py --check --dry-run` exits `0`, `--json` prints valid deterministic JSON, and `mypy --strict` + `ruff` pass with `0` warnings.

#### Completion Evidence

* `ReproducibilityReport(ok=True, errors=(), ...)` returned from both `reproducibility_check.verify_from_empty_deployment_reproducibility()` and `pipeline.verify_from_empty_deployment_reproducibility()`.

#### Unresolved Items

* None.

<!-- rpi:phase id=P03 -->
## P03: Document Canonical From-Empty Step Registry in `infra/README.md`

### Context

`infra/README.md` currently lists `Layout` at lines `18-55` and `### Reproducible from-empty deployment sequence` (12 rows, 5 columns) at lines `3964-3987`. `bicep_inventory.py` stops parsing `### Reproducible from-empty deployment sequence` as soon as it sees the next `## ` or `### ` heading (`C13`, `C22`).

### Intent

Document `parameters/dev.bicepparam`, `parameters/prod.bicepparam`, and `scripts/reproducibility_check.py` in `## Layout`, and add `### Canonical from-empty pipeline step registry` right after `### Reproducible from-empty deployment sequence` so all 6 canonical steps (`preflight`, `what-if`, `deploy`, `sql-init`, `seed`, `smoke`) are documented cleanly in `infra/README.md` with zero undocumented manual steps and zero impact on `bicep_inventory.py`.

### Boundaries

* Included: Surgical additions to `## Layout` and `### Canonical from-empty pipeline step registry` (plus `ms.date` if frontmatter is present or keeping existing Markdown conventions: `*` unordered lists, plain ASCII punctuation, no em dashes, no bolded-prefix list items, zero `.copilot-tracking/` references).
* Excluded: Editing the 12-row `### Reproducible from-empty deployment sequence` table, `### Proposed architecture resource inventory`, `### Bicep module delivery matrix`, governance prose, or container-hosting prose.

### Likely Targets

* `infra/README.md`

### Dependencies

* P01, P02.

### Validation Expectations

* `python3 infra/scripts/bicep_inventory.py --check` exits `0`.
* `python3 infra/scripts/reproducibility_check.py --check --dry-run` exits `0`.
* `infra/tests/test_governance.py` and `infra/tests/test_container_hosting_completeness.py` pass.

### Completion Evidence

* Both `#136` verifiers pass against `infra/README.md` with zero errors.

### Unresolved Items

* None.

<!-- rpi:task id=P03-T01 -->
### P03-T01: Update `## Layout` and add `### Canonical from-empty pipeline step registry` in `infra/README.md`

#### Context

Markdown style rules in `.github/copilot-instructions.md` require `*` for unordered lists, plain ASCII punctuation, no em dashes, and no bolded-prefix list items.

#### Intent

Add the `parameters/` and `scripts/reproducibility_check.py` entries to `## Layout` and add the 6-row `### Canonical from-empty pipeline step registry` subsection immediately before `## Ledger digest immutability and scheduled verification wiring`.

#### Boundaries

* Included:
  * In `## Layout`: bullet entries for `parameters/dev.bicepparam` + `parameters/prod.bicepparam` and `scripts/reproducibility_check.py`.
  * Under `## Resource coverage register (issue 136)` immediately after the 12-row `### Reproducible from-empty deployment sequence` table: `### Canonical from-empty pipeline step registry` containing introductory prose explaining how `pipeline.FROM_EMPTY_STEPS` and `reproducibility_check.py` group the from-empty deployment into the 6 canonical pipeline steps (`preflight`, `what-if`, `deploy`, `sql-init`, `seed`, `smoke`) and verify deterministic offline execution, followed by the 6-row table (`Step`, `Pipeline registration`, `Rebuild stage(s)`, `Repository template or script`, `Manual prerequisites`, `Verification check`).
* Excluded: Modifying any existing table rows or historical sections in `infra/README.md`.

#### Likely Targets

* `infra/README.md`

#### Dependencies

* P01-T01, P02-T01, P02-T02.

#### Validation Expectations

* `bicep_inventory.py --check` and `reproducibility_check.py --check --dry-run` both exit `0`; `git diff infra/README.md` contains zero em dashes, zero bolded-prefix bullets, and zero `.copilot-tracking/` substrings.

#### Completion Evidence

* Reconciled `infra/README.md` diff verified by both CLI checkers.

#### Unresolved Items

* None.

<!-- rpi:phase id=P04 -->
## P04: Author Focused Unit & Mutation Tests, Validate, and Commit Cleanly

### Context

The caller requested `infra/tests/test_from_empty_reproducibility_136.py` proving criteria (a), (b), and (c) and Focused validation (`python3 -m unittest discover -s infra/tests -p 'test_*.py' -q`, `python3 -m ruff check`, `python3 -m ruff format --isolated --line-length 100 --check`).

### Intent

Deliver focused positive and fail-closed mutation tests in `infra/tests/test_from_empty_reproducibility_136.py`, run the full Focused validation suite with cacheless flags so zero scratch files remain, and prepare the clean repository state for `rpi-review` and local commit handoff.

### Boundaries

* Included:
  * Test ownership locked: `0` existing tests removed (`none`); `1` new test file (`infra/tests/test_from_empty_reproducibility_136.py`) with up to `14` focused test methods covering semantic acceptance criteria (a), (b), and (c) and fail-closed mutation regressions.
  * Running Focused validation (`unittest`, `ruff`, `mypy --strict`, `az bicep build-params`).
* Excluded: Running `tools/rpi-checks.py` or modifying unrelated test files.

### Likely Targets

* `infra/tests/test_from_empty_reproducibility_136.py`

### Dependencies

* P01, P02, P03.

### Validation Expectations

* `env -u PYTHONPATH PYTHONDONTWRITEBYTECODE=1 python3 -m unittest infra/tests/test_from_empty_reproducibility_136.py -v` passes.
* `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src/core/src:src/agents/src:src/api/src:src/orchestrator/src:src/importer/src python3 -m unittest discover -s infra/tests -p 'test_*.py' -q` passes (`0` failures, `0` errors).
* `python3 -m ruff check --no-cache infra/scripts/pipeline.py infra/scripts/reproducibility_check.py infra/tests/test_from_empty_reproducibility_136.py` passes (`0` issues).
* `python3 -m ruff check --no-cache --isolated --select E,F,I,B,UP --target-version py312 --line-length 100 infra/scripts/pipeline.py infra/scripts/reproducibility_check.py infra/tests/test_from_empty_reproducibility_136.py` passes (`0` issues).
* `python3 -m ruff format --no-cache --isolated --line-length 100 --check infra/scripts/pipeline.py infra/scripts/reproducibility_check.py infra/tests/test_from_empty_reproducibility_136.py` passes (`0` issues).
* `python3 -m mypy --strict --no-incremental --cache-dir=/dev/null infra/scripts/pipeline.py infra/scripts/reproducibility_check.py infra/tests/test_from_empty_reproducibility_136.py` passes (`0` issues).

### Completion Evidence

* Passing unit test output, clean lint/format/type checks, clean `git status --ignored --short`, and complete `.copilot-tracking/changes/2026-11-15/infra-136-bicep-repro-changes.md`.

### Unresolved Items

* None.

<!-- rpi:task id=P04-T01 -->
### P04-T01: Author `infra/tests/test_from_empty_reproducibility_136.py` and run Focused validation

#### Context

Tests must work both under hosted CI (`python -m unittest discover -s infra/tests -v` without `PYTHONPATH`) and under full local discovery (`PYTHONPATH=src/core/src:...`), and must test genuine behavioral invariants rather than restating constants.

#### Intent

Create `infra/tests/test_from_empty_reproducibility_136.py` covering positive repository verification, `az bicep build-params` compilation of `infra/parameters/{dev,prod}.bicepparam`, deterministic multi-run offline dry-run execution, and fail-closed negative mutations for criteria (a), (b), and (c).

#### Boundaries

* Included test cases (<= 14 focused tests):
  1. Live repository `verify_from_empty_deployment_reproducibility` passes via both `pipeline` and `reproducibility_check` (including loading `pipeline.py` via `spec_from_file_location` without `"pipeline"` registered in `sys.modules` and without `infra/scripts` on `sys.path` per `PC-001`), and `bicep_inventory.verify_all` remains `ok=True`.
  2. Criterion (a) positive + fail-closed mutations: rejects missing/reordered step in `pipeline.FROM_EMPTY_STEPS`, missing step row in `infra/README.md`, missing referenced artifact on disk, rebuild-stage partition/duplicate gap (`PC-002`), and undocumented manual steps (placeholder cell, unowned prerequisite, or `"run manually in portal"` prose).
  3. Criterion (b) positive + `az bicep build-params` parity + fail-closed mutations: compiles `infra/parameters/dev.bicepparam` and `infra/parameters/prod.bicepparam` via `az bicep build-params` and cross-checks equality against offline `parse_bicepparam_file` parsed values (confirming `allowPublicNetworkAccess == False`, `apiMinReplicas == 0`, `enableLocks == True` in `prod`, multi-line `modelDeployments` parsed identically, and defaultless params populated), proves a synthetic defaultless parameter in `main.bicep` passes when supplied in both `dev.bicepparam` & `prod.bicepparam`, passes when explicitly injected by `pipeline.py`, and fails closed when absent from `prod.bicepparam` (or `dev.bicepparam`) AND absent from `pipeline.py` injections, and rejects AST drift in `pipeline.INJECTED_PARAMETERS`, dynamically constructed secret tokens (`PC-004`), or unknown parameters in `.bicepparam`.
  4. Criterion (c) positive + determinism + CI env isolation + fail-closed mutations: executes `execute_from_empty_dry_run` across `"dev"` and `"prod"` with `subprocess.run` blocked and ambient `GITHUB_STEP_SUMMARY` / `RELEASE_SHA` / `DEPLOY_PARAMETERS` set, asserts the pre-existing `GITHUB_STEP_SUMMARY` file is untouched and `sequence_digest` is identical to a stripped `env={}` run (`PC-003`), verifies CLI `--check --dry-run --json` exits `0`, and proves dry-run fails closed when a required SQL/Dockerfile/JSON/parameter artifact is missing or malformed in a temporary fixture repo.
* Excluded: Live Azure network calls or modifications to unrelated test files.

#### Likely Targets

* `infra/tests/test_from_empty_reproducibility_136.py`

#### Dependencies

* P01-T01, P02-T01, P02-T02, P03-T01.

#### Validation Expectations

* All Focused validation commands pass and leave zero cache directories in the worktree.

#### Completion Evidence

* Recorded command outputs in `.copilot-tracking/changes/2026-11-15/infra-136-bicep-repro-changes.md`.

#### Unresolved Items

* None.

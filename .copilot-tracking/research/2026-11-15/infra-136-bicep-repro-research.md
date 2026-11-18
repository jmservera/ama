---
description: "Primary research artifact for Issue #136 from-empty deployment reproducibility verifier, Bicep parameter coverage, and deterministic offline pipeline dry-run"
---
<!-- markdownlint-disable-file -->

# Task Research: infra-136-bicep-repro

| Field              | Value                                                                    |
|--------------------|--------------------------------------------------------------------------|
| Date               | 2026-11-15                                                               |
| Researcher / agent | rpi-research (coordinated by RPI Agent)                                  |
| Status             | Complete                                                                 |
| Artifact path      | .copilot-tracking/research/2026-11-15/infra-136-bicep-repro-research.md  |

## Research Brief

* What to research: Inspect `infra/scripts/pipeline.py`, `infra/main.bicep`, `infra/parameters/*.bicepparam` (and existing `infra/*.bicepparam`), `infra/scripts/bicep_inventory.py`, `infra/README.md`, `src/orchestrator/src/zava_forward/orchestrator/rebuild.py`, and existing `infra/tests/test_*.py` suites to design a deterministic reproducibility verifier (`verify_from_empty_deployment_reproducibility`) and unit test suite (`infra/tests/test_from_empty_reproducibility_136.py`).
* Why it matters: Proves the Issue `#136` acceptance criterion *"A from-empty deployment is reproducible from the repository without undocumented steps"* across three concrete sub-proofs:
  1. Every step required for a from-empty deployment (`preflight`, `what-if`, `deploy`, `sql-init`, `seed`, `smoke`) is registered in `infra/scripts/pipeline.py` and documented in `infra/README.md` with zero undocumented manual steps;
  2. Every parameter in `infra/main.bicep` without a default is supplied in `infra/parameters/dev.bicepparam` / `prod.bicepparam` or explicitly injected by `infra/scripts/pipeline.py`;
  3. Dry-run / offline execution of the full from-empty pipeline sequence succeeds deterministically from repository files alone.
* Audience or intended use: `rpi-plan`, `rpi-implement`, and `rpi-review` phases in this confirmed automatic RPI loop, plus coordinator exact-head review.
* Scope: `infra/scripts/pipeline.py`, `infra/scripts/reproducibility_check.py`, `infra/parameters/dev.bicepparam`, `infra/parameters/prod.bicepparam`, `infra/main.bicep`, `infra/*.bicepparam`, `infra/README.md`, and `infra/tests/test_from_empty_reproducibility_136.py`.
* Non-goals: Live Azure resource provisioning or `az deployment` calls against a live subscription, running `tools/rpi-checks.py`, editing `.github/workflows/*.yml`, or pushing / opening a pull request.
* Criteria: Every claim backed by workspace-relative `path:line` evidence; zero regressions across all existing 631 `infra/tests` unit tests (including `test_bicep_architecture_inventory_136.py`, `test_pipeline.py`, `test_governance.py`, `test_bicep_policy.py`, `test_environment_quota_parameters.py`, and `test_container_hosting_completeness.py`); clean `ruff check`, `ruff format --isolated --line-length 100 --check`, and `mypy --strict`.
* Requested outputs: Converged design and exact verification/dry-run contract ready for `rpi-plan`.
* Output mode: convergence

## Research Parameters

| Field                            | Value                                                                   |
|----------------------------------|-------------------------------------------------------------------------|
| Research question(s)             | (Q1) How does `infra/scripts/pipeline.py` currently register operations, parameters, SQL checks, and smoke probes, and what AST/CLI invariants do existing tests enforce on it? (Q2) Which parameters in `infra/main.bicep` have no default value, how are `.bicepparam` files structured and tested today, and how should `infra/parameters/dev.bicepparam` and `infra/parameters/prod.bicepparam` coexist with `infra/main*.bicepparam`? (Q3) How does `infra/README.md` document the from-empty deployment sequence today, and how should the canonical 6-step registry (`preflight`, `what-if`, `deploy`, `sql-init`, `seed`, `smoke`) be documented without breaking `bicep_inventory.py`? (Q4) How can an offline dry-run execute the full 6-step pipeline sequence deterministically from repository files alone while exercising real `pipeline.py` logic? (Q5) What import-loading, `PYTHONPATH`, `ruff`, and `mypy --strict` constraints apply? |
| Codebase scope                   | `infra/`, `src/orchestrator/`, `tools/`, `.github/workflows/src-ci.yml` |
| External scope                   | none                                                                    |
| Initial internal candidate areas | `infra/scripts/pipeline.py`, `infra/main.bicep`, `infra/*.bicepparam`, `infra/scripts/bicep_inventory.py`, `infra/README.md`, `infra/tests/` |
| Initial external candidate areas | none                                                                    |
| Research posture                 | focused                                                                 |
| Posture provenance               | caller-specified (bounded internal task with named source targets, explicit acceptance sub-criteria, and Focused validation tier) |
| Explicit limits / deadline       | Focused validation tier (`infra/tests` + `ruff check` + `ruff format --isolated --line-length 100 --check`); do not run `tools/rpi-checks.py`; do not push |
| Posture-specific completion basis | All target scripts, Bicep templates, `.bicepparam` contracts, README tables, and existing test invariants verified with `path:line` evidence |
| Edits allowed during research?   | no, research-only                                                       |
| Resolved evidence root           | `.copilot-tracking/`                                                    |
| Known constraints / excluded sources | Do not embed `.copilot-tracking/` paths in production code, docstrings, comments, or commit message prose; commit `.copilot-tracking/` artifacts per caller handoff instructions |

## Extension Registry and Provenance

* Precedence: platform and host safety; caller scope and criteria; matching repository instructions and enforced schemas; rpi-research contract; domain skills and specialists; examples and preferences.

| Kind                | Candidate                        | Match and provenance                              | Scoped authority or output contract          | Selected / skipped reason      |
|---------------------|----------------------------------|---------------------------------------------------|----------------------------------------------|--------------------------------|
| Instruction         | `.github/copilot-instructions.md` (AMA Repository Instructions) | `applyTo: "**"` matches all workspace targets | Governs `infra/` Python formatting (`--line-length 100`), `mypy`, Focused validation tier, Markdown style (`*` bullets, no em dashes), and commit email/trailer hygiene | Selected: governs code style, documentation formatting, and validation |
| Skill               | `python-foundational`            | General Python guidance                           | General Python style                         | Skipped: existing `infra/scripts/pipeline.py` and `infra/scripts/bicep_inventory.py` define exact repository-local stdlib + `--strict` typing idioms |
| Research specialist | `hve-core-all:rpi-researcher`    | General delegated research lane worker            | Subagent lane artifact                       | Skipped (inline execution): tightly coupled AST/table/parameter invariants across 6 local files fit direct reads with zero coordination overhead |

## User Participation and Research Decisions

| Checkpoint       | Questions or no-interaction rationale                       | Answers / unanswered      | Resulting decision or selected further research    |
|------------------|-------------------------------------------------------------|---------------------------|----------------------------------------------------|
| Intake           | Non-interactive session; caller supplied exact branch, files, function name (`verify_from_empty_deployment_reproducibility`), test suite path (`infra/tests/test_from_empty_reproducibility_136.py`), criteria (a)-(c), and validation commands | No interaction available or needed | Execute focused inline Cycle 1 across all named targets |
| Direction change | None required; Cycle 1 uncovered all compatibility invariants with `bicep_inventory.py`, `test_pipeline.py`, and `test_governance.py` | N/A | Maintain focused scope |
| Convergence      | All five research questions answered with verified `path:line` evidence | Converged | Record `Research disposition: executed` and `Planning Readiness: Ready` |

## Scope and Success Criteria

* Scope: Inspect `infra/scripts/pipeline.py`, `infra/main.bicep`, `infra/*.bicepparam`, `infra/scripts/bicep_inventory.py`, `infra/README.md`, and `infra/tests/` to design the deterministic from-empty deployment reproducibility verifier, parameter files, README step registry, and unit/mutation tests.
* Assumptions: Commit `252125ad2` (`feat(infra): add Bicep architecture inventory and rebuild verifier (#136)`) is already in branch ancestry on `feat/infra-136-bicep-repro`, so the new verifier and tests must compose cleanly with `bicep_inventory.py` and `test_bicep_architecture_inventory_136.py`.
* Success criteria:
  * Exact compatibility invariants on `pipeline.py` CLI `operation` choices and `infra/README.md` tables are documented.
  * Every defaultless parameter in `infra/main.bicep` is identified and mapped to `.bicepparam` files and `pipeline.py` injections.
  * Every canonical from-empty step (`preflight`, `what-if`, `deploy`, `sql-init`, `seed`, `smoke`) is mapped to checked-in repository scripts/templates and deterministic offline dry-run probes.

## Task Research Requests

* Explicit requests:
  1. Inspect `infra/scripts/pipeline.py`, `infra/main.bicep`, `infra/parameters/*.bicepparam`, and `infra/README.md`.
  2. Design `verify_from_empty_deployment_reproducibility` (in `infra/scripts/pipeline.py` or `infra/scripts/reproducibility_check.py`) and `infra/tests/test_from_empty_reproducibility_136.py` proving criteria (a), (b), and (c).
* Inferred research questions:
  * Why does `infra/parameters/` not yet exist on disk, and do any existing tests forbid or constrain `infra/parameters/dev.bicepparam` and `infra/parameters/prod.bicepparam`?
  * How do `test_pipeline.py` and `test_environment_quota_parameters.py` load `infra/scripts/pipeline.py` (`spec_from_file_location`), and how does that affect cross-script imports?

## Direction Controls

| Control type (add / change / narrow / exclude / discard) | Direction or boundary | Source / checkpoint  | Effect on active brief, evidence, or revalidation |
|----------------------------------------------------------|-----------------------|----------------------|---------------------------------------------------|
| narrow |Focused validation tier (`infra/tests` + `ruff check` + `ruff format --isolated --line-length 100 --check`); do not run `tools/rpi-checks.py` | Caller prompt / Intake | Scopes validation to `infra/` unit tests, ruff, mypy, and Bicep parameter builds |
| exclude | Do not push or open a PR; leave clean frozen HEAD | Caller prompt / Intake | Restricts git operations to local commit on `feat/infra-136-bicep-repro` |

## Research Questions

|  # | Sub-question     | Type (depth / breadth / straightforward) | Priority  | Status                    |
|---:|------------------|------------------------------------------|-----------|---------------------------|
| Q1 | How does `infra/scripts/pipeline.py` define operations, parameter overrides, SQL checks, and smoke probes, and what AST invariants do existing tests assert? | depth | H | answered |
| Q2 | Which parameters in `infra/main.bicep` lack default values, and how should `infra/parameters/dev.bicepparam` and `infra/parameters/prod.bicepparam` be structured alongside `infra/main*.bicepparam`? | depth | H | answered |
| Q3 | How does `infra/README.md` currently document the from-empty sequence, and how can `preflight`, `what-if`, `deploy`, `sql-init`, `seed`, and `smoke` be documented and machine-checked with zero undocumented manual steps? | depth | H | answered |
| Q4 | How can offline dry-run execution run the full 6-step sequence deterministically from repository files alone while exercising `pipeline.py` code paths? | depth | H | answered |
| Q5 | What module-loading, `PYTHONPATH`, `ruff`, and `mypy --strict` traps exist in `infra/`? | straightforward | H | answered |

## Prior Knowledge Gate

* Existing artifacts reviewed: `docs/case_study_48_original.md`, `docs/case_study_48_addendum.md`, `docs/reference/README.md`, `docs/reference/memory.md`, `.copilot-tracking/research/2026-11-15/infra-136-bicep-inventory-research.md`, and `.copilot-tracking/reviews/logs/2026-11-15/infra-136-bicep-inventory-review.md`.
* Reused (verified) findings: Commit `252125ad2` established `infra/scripts/bicep_inventory.py` and the 3-table register in `infra/README.md:3900-3987`, including the 12-row `### Reproducible from-empty deployment sequence` mapped to the 17 `STAGES` in `src/orchestrator/src/zava_forward/orchestrator/rebuild.py`.
* New gap addressed by this task: `pipeline.py` did not yet expose a structured 6-step canonical from-empty pipeline registry (`preflight`, `what-if`, `deploy`, `sql-init`, `seed`, `smoke`) or `verify_from_empty_deployment_reproducibility`, `infra/parameters/dev.bicepparam` and `infra/parameters/prod.bicepparam` did not yet exist on disk, and there was no deterministic offline dry-run executor exercising the full 6-step pipeline sequence from repository files alone.

## Cycle 1 Execution

### Wave 1: Wider (Pipeline Surface, Bicep Parameters, Scripts, and README Coverage)

* Inspected `infra/scripts/pipeline.py`, `infra/main.bicep`, `infra/modules/guard.bicep`, `infra/*.bicepparam`, `infra/scripts/*`, and `infra/README.md`:
  * `infra/scripts/pipeline.py` (`C1`, `C2`) implements CI helpers `verify_environment` (preflight reviewer/branch policy check), `parameters` (compiles `.bicepparam` and injects `OVERRIDES` + fixed deployment keys), `summarize_plan` (`what-if` scope & private-SQL check), `publish` / `release_images` (digest-pinned workload images), `deployment` (lock/tag check + `what-if` + `create` + `check_sql` + `smoke`), `check_sql` (asserts SQL `publicNetworkAccess == "Disabled"`), and `smoke` (`/healthz` 200, 3 `/api/me` 401 auth-denial probes, optional `/sign-in` 302 probe).
  * Companion checked-in scripts cover the remaining from-empty steps (`C3`, `C4`, `C5`, `C6`):
    * `preflight`: `infra/scripts/tenant-readiness-preflight.py`, `infra/entra/app-registration.json`, `infra/secret-inventory.json`, `infra/defender-decision.json`, and `pipeline.verify_environment`.
    * `what-if`: `infra/main.bicep`, `infra/governance.bicep`, `.bicepparam` files, `infra/scripts/deploy.py` (default `what-if`), and `pipeline.parameters` + `pipeline.summarize_plan` (`plan`).
    * `deploy`: `infra/main.bicep`, `infra/modules/containerapps.bicep`, `src/{api,agents,orchestrator,importer}/Dockerfile`, `infra/scripts/deploy.py` (`--apply`), and `pipeline.publish` + `pipeline.deployment` (`deploy`).
    * `sql-init`: `infra/scripts/create-sql-users.py`, `infra/scripts/create-sql-users.sql`, `infra/sql/resident-showcase.sql`, `infra/sql/resident-assistant.sql`, `infra/staff-initializer-rbac.bicep`, and `pipeline.check_sql`.
    * `seed`: `src/importer/Dockerfile`, `src/orchestrator/src/zava_forward/orchestrator/rebuild_azure.py`, `infra/scripts/resident_sensor_seed.py`, and `infra/scripts/initialize-workbench-staff.py`.
    * `smoke`: `pipeline.smoke`, `infra/scripts/private-cutover-proof.py`, `src/orchestrator/src/zava_forward/orchestrator/rebuild.py`, and `src/orchestrator/src/zava_forward/orchestrator/rebuild_azure.py`.
  * `infra/main.bicep` (`C7`) declares 61 parameters in total; exactly **three** parameters have **no default value**:
    1. `param alertEmail string` (`infra/main.bicep:18`)
    2. `param sqlAdminGroupName string` (`infra/main.bicep:45`)
    3. `param sqlAdminGroupObjectId string` (`infra/main.bicep:46`)
  * All three defaultless parameters are present in `infra/main.bicepparam`, `infra/main.test.bicepparam`, and `infra/main.pilot.example.bicepparam` (`C8`, `C9`) AND are members of `pipeline.OVERRIDES` (`infra/scripts/pipeline.py:34-44`) injected into `compiled["parameters"]` by `pipeline.parameters()` (`infra/scripts/pipeline.py:120-182`).
  * `infra/parameters/` does not currently exist on disk (`C10`): root `.bicepparam` files sit directly under `infra/`.

### Wave 2: Deeper (AST Contracts, Parameter Compilation Rules, and Offline Dry-Run Mechanics)

* Audited every `bicepparam` and `pipeline.py` reference across `infra/`, `src/`, `tools/`, and `.github/` (`C11`-`C18`):
  1. **`bicep_inventory.py` AST invariant on `pipeline.py`**: `bicep_inventory.load_pipeline_operations` (`infra/scripts/bicep_inventory.py:578-604`) walks the AST of `infra/scripts/pipeline.py` looking for `add_argument("operation", choices=...)`, and `infra/tests/test_bicep_architecture_inventory_136.py:245` asserts `self.pipeline_ops == ("plan", "deploy", "publish", "changed-images", "verify-environment")` (`C11`, `C12`). Therefore `parser.add_argument("operation", choices=...)` in `pipeline.py` must remain unchanged while `FROM_EMPTY_STEPS` (`preflight`, `what-if`, `deploy`, `sql-init`, `seed`, `smoke`) and `verify_from_empty_deployment_reproducibility` are registered as structured module-level definitions/callables in `pipeline.py` (with standalone CLI execution in `infra/scripts/reproducibility_check.py`).
  2. **`bicep_inventory.py` Markdown table boundary in `infra/README.md`**: `parse_markdown_section_table` (`infra/scripts/bicep_inventory.py:272-319`) reads lines after `### Reproducible from-empty deployment sequence` and stops immediately at the next `## ` or `### ` heading (`if line.startswith(("## ", "### ")): break`) (`C13`). Adding a sibling subsection `### Canonical from-empty pipeline step registry` immediately after the 12-row `### Reproducible from-empty deployment sequence` table preserves all 12 rows and 17 `rebuild.py` stage tokens untouched while giving `preflight`, `what-if`, `deploy`, `sql-init`, `seed`, and `smoke` an unambiguous, machine-checked table in `infra/README.md`.
  3. **`infra/parameters/dev.bicepparam` and `infra/parameters/prod.bicepparam` compilation constraints**:
     * `infra/main.bicep:8` constrains `@allowed(['dev', 'test', 'pilot']) param environmentName string = 'dev'` and `@allowed(['production', 'development']) param deploymentProfile string = 'production'` (`C7`), while `infra/modules/guard.bicep:55-62` enforces `pilotRequiresProductionProfile` and `pilotRequiresLocks` (`C14`).
     * Creating `infra/parameters/dev.bicepparam` (`using '../main.bicep'`, `environmentName = 'dev'`, `deploymentProfile = 'development'`, `allowPublicNetworkAccess = false`, `apiMinReplicas = 0`, explicit `NON-DEPLOYABLE` / `PLACEHOLDER` header) and `infra/parameters/prod.bicepparam` (`using '../main.bicep'`, `environmentName = 'pilot'`, `deploymentProfile = 'production'`, `enableLocks = true`, `allowPublicNetworkAccess = false`, `keyVaultPurgeProtection = true`, `registryQuarantineEnabled = true`, `sqlTier = 'provisioned'`, `apiMinReplicas = 0`, explicit `NON-DEPLOYABLE EXAMPLE` header) compiles cleanly via `az bicep build-params` AND violates zero existing tests (`test_governance.py:48` checks `(INFRA / "main.pilot.bicepparam").exists() == False`; `test_iot_credential_hygiene.py` scans `.bicepparam` for IoT `SharedAccessKey=` secrets; `cutover_audit.py` scans `.bicepparam` for retired pre-cutover names) (`C15`, `C16`).
  4. **Dynamic parameter & injection verification**:
     * Static multi-line-aware Bicep parameter parsing extracts all `param <name> <type>` declarations from `infra/main.bicep` and partitions them into `with_default` vs `without_default` (`alertEmail`, `sqlAdminGroupName`, `sqlAdminGroupObjectId`).
     * Static `.bicepparam` parsing extracts `using '...'` target resolution and `param <name> = <expr>` assignments from `infra/parameters/dev.bicepparam` and `infra/parameters/prod.bicepparam` (as well as `infra/main.bicepparam`, `infra/main.test.bicepparam`, `infra/main.pilot.example.bicepparam`), rejecting unknown parameter names not declared in `infra/main.bicep`.
     * Python AST inspection of `infra/scripts/pipeline.py` extracts `OVERRIDES`, fixed keys in `parameters()` `values.update(...)`, and `IMAGE_PARAMETERS.values()` in `deployment()`, cross-checking them against `pipeline.INJECTED_PARAMETERS` so declared and actual AST-injected parameter sets cannot diverge.

### Wave 3: Contrarian (Import Loading, Determinism, and Lint/Cache Hazards)

* Tested potential failure modes against actual repository harnesses (`C17`-`C22`):
  1. **`importlib.util.spec_from_file_location` module-loading hazard**: Both `infra/tests/test_pipeline.py:23-26` and `infra/tests/test_environment_quota_parameters.py:39` execute `infra/scripts/pipeline.py` via `spec_from_file_location` without adding `infra/scripts` to `sys.path` (`C17`, `C18`). Contrarian resolution: `pipeline.py` must NOT use a bare `import reproducibility_check` at module import time; instead `pipeline.py` defines `FROM_EMPTY_STEP_ORDER`, `FROM_EMPTY_STEPS`, `ENVIRONMENT_PARAMETER_FILES`, and `INJECTED_PARAMETERS` natively with stdlib types and loads `reproducibility_check.py` via `importlib.util.spec_from_file_location` inside `verify_from_empty_deployment_reproducibility()` and `execute_from_empty_dry_run()`. Conversely, `reproducibility_check.py` loads `pipeline.py` via `spec_from_file_location` (reusing `sys.modules` when cached) so both scripts work standalone, under `unittest discover`, or under `spec_from_file_location`.
  2. **Subprocess `PYTHONPATH` in `test_pipeline.py`**: `SmokeTests.test_installed_local_api_denies_unauthenticated_requests` (`infra/tests/test_pipeline.py:888-920`) spawns `sys.executable -m zava_forward.api`, requiring `PYTHONPATH=src/core/src:src/agents/src:src/api/src:src/orchestrator/src:src/importer/src` when editable wheels are not pre-installed in the system interpreter (`C19`). Meanwhile, `test_from_empty_reproducibility_136.py` itself must use pure stdlib + `importlib` so it passes both WITH and WITHOUT `PYTHONPATH` (`env -u PYTHONPATH`).
  3. **True offline dry-run determinism**: If the dry-run called live `az bicep build-params` or `socket` servers, it would either be slow (~5s per call) or depend on host state, and any temp directory path or timestamp in the result would break determinism. Contrarian resolution: the offline dry-run parses `main.bicep`, `.bicepparam`, SQL, JSON, and Dockerfiles directly from `repo_root` on disk and drives `pipeline.verify_environment`, `pipeline.parameters`, `pipeline.summarize_plan`, `pipeline.deployment`, `pipeline.check_sql`, and `pipeline.smoke` through deterministic in-process mocks (`unittest.mock.patch.object` on the isolated module instance) with canonical fixed synthetic inputs derived solely from repository content hashes, producing an identical `sequence_digest` across repeated runs and across `env -i` clean environments.
  4. **Ruff 0.17.3 user-config vs CI `--isolated` config & cache hygiene**: `.github/workflows/src-ci.yml:253-263` runs `ruff check --isolated --select E,F,I,B,UP --target-version py312 --line-length 100`, `ruff format --isolated --line-length 100 --check`, and `mypy --strict infra/scripts/pipeline.py` (`C20`). Meanwhile, bare `python3 -m ruff check` on this host picks up user-level rules (`FURB`, `SIM`, `EXE001`) and flags 21 untouched legacy files in `infra/` under `ruff format --check` (`C21`). Contrarian resolution: keep untouched legacy `infra/` files untouched per surgical-change rules; ensure every file we create or modify (`infra/scripts/pipeline.py`, `infra/scripts/reproducibility_check.py`, `infra/tests/test_from_empty_reproducibility_136.py`) passes **both** bare `python3 -m ruff check` (0 warnings, omit `#!/usr/bin/env python3` on non-executable new `.py` files so `EXE001` cannot fire) **and** `--isolated` lint/format + `mypy --strict`; always pass `--no-cache` / `RUFF_CACHE_DIR=/tmp/ruff-cache` and `--no-incremental --cache-dir=/dev/null` so zero `.ruff_cache` or `.mypy_cache` directories remain in the worktree (`C22`).

## Evidence Log

| ID  | Source (`path:line`) | Summary of Verified Fact |
|-----|----------------------|--------------------------|
| C1  | `infra/scripts/pipeline.py:22-66,119-183` | Defines `PROJECTS`, `IMAGE_PARAMETERS`, `PARAMETER_FILES` (`dev`, `test`, `pilot`), `OVERRIDES` (9 keys including `alertEmail`, `sqlAdminGroupName`, `sqlAdminGroupObjectId`), and `parameters()` injecting overrides plus `workload`, `environmentName`, `allowPublicNetworkAccess`, `deployApplications`. |
| C2  | `infra/scripts/pipeline.py:240-480` | Defines `check_sql()`, `verify_environment()`, `summarize_plan()`, `smoke()`, `deployment()`, and CLI `operation` choices `("plan", "deploy", "publish", "changed-images", "verify-environment")`. |
| C3  | `infra/scripts/tenant-readiness-preflight.py:1-90` | Read-only Entra/Container Apps preflight script checking `infra/entra/app-registration.json` contract. |
| C4  | `infra/scripts/deploy.py:1-340` | Operator wrapper preserving orchestrator images, advisory auth locks, default `what-if` preview, and `--apply` deployment. |
| C5  | `infra/scripts/create-sql-users.py:1-58` & `infra/scripts/create-sql-users.sql:1-30` | Idempotent contained Entra SQL user creation (`IF NOT EXISTS ... CREATE USER ... TYPE = E`) and role grants (`db_datareader`, `db_datawriter`, `db_ddladmin` on `api`). |
| C6  | `infra/scripts/resident_sensor_seed.py:1-90` & `src/orchestrator/src/zava_forward/orchestrator/rebuild_azure.py:141-520` | Deterministic synthetic seed and 17-stage Azure rebuild executor (`rebuild.py:34-66`). |
| C7  | `infra/main.bicep:1-190` | Declares `@allowed(['dev', 'test', 'pilot']) param environmentName string = 'dev'`, `@allowed(['production', 'development']) param deploymentProfile string = 'production'`, and exactly 3 defaultless parameters: `alertEmail` (`:18`), `sqlAdminGroupName` (`:45`), `sqlAdminGroupObjectId` (`:46`). |
| C8  | `infra/main.bicepparam:1-41` | Dev parameter template (`using './main.bicep'`) supplying `alertEmail`, `sqlAdminGroupName`, `sqlAdminGroupObjectId`, `deploymentProfile = 'development'`, `allowPublicNetworkAccess = false`, `apiMinReplicas = 0`. |
| C9  | `infra/main.pilot.example.bicepparam:1-42` | Production-profile parameter template (`using './main.bicep'`, `NON-DEPLOYABLE EXAMPLE`) supplying `alertEmail`, `sqlAdminGroupName`, `sqlAdminGroupObjectId`, `environmentName = 'pilot'`, `deploymentProfile = 'production'`, `enableLocks = true`, `allowPublicNetworkAccess = false`. |
| C10 | `infra/` directory glob | `infra/parameters/` does not yet exist; only `infra/main.bicepparam`, `infra/main.test.bicepparam`, `infra/main.pilot.example.bicepparam`, and `infra/iot-hub-live.bicepparam` exist. |
| C11 | `infra/scripts/bicep_inventory.py:578-604` | `load_pipeline_operations()` AST-parses `add_argument("operation", choices=...)` from `infra/scripts/pipeline.py`. |
| C12 | `infra/tests/test_bicep_architecture_inventory_136.py:244-253` | Explicitly asserts `self.pipeline_ops == ("plan", "deploy", "publish", "changed-images", "verify-environment")`, `module_rows == 20`, and `sequence_steps == 12`. |
| C13 | `infra/scripts/bicep_inventory.py:272-319` | `parse_markdown_section_table()` stops reading a table section at the next `## ` or `### ` heading. |
| C14 | `infra/modules/guard.bicep:55-62` | Enforces `pilotRequiresProductionProfile` and `pilotRequiresLocks` at Bicep compile/validation time. |
| C15 | `infra/tests/test_governance.py:44-68` | Asserts `(INFRA / "main.pilot.bicepparam").exists()` is `False` and checks `main.bicepparam`, `main.test.bicepparam`, `main.pilot.example.bicepparam`. |
| C16 | `src/api/tests/test_iot_credential_hygiene.py:39,143` & `src/core/src/zava_forward/core/synthetic/cutover_audit.py:27` | Scans `.bicepparam` files for secret literals and retired pre-cutover identifiers. |
| C17 | `infra/tests/test_pipeline.py:23-26` | Loads `infra/scripts/pipeline.py` via `importlib.util.spec_from_file_location` without `infra/scripts` on `sys.path`. |
| C18 | `infra/tests/test_environment_quota_parameters.py:39` | Also loads `infra/scripts/pipeline.py` via `spec_from_file_location`. |
| C19 | `infra/tests/test_pipeline.py:888-920` | Spawns `sys.executable -m zava_forward.api`, passing in `0.45s` when `PYTHONPATH` includes `src/{core,agents,api,orchestrator,importer}/src`. |
| C20 | `.github/workflows/src-ci.yml:253-264` | Runs `ruff check --isolated --select E,F,I,B,UP --target-version py312 --line-length 100`, `ruff format --isolated --line-length 100 --check`, and `mypy --strict infra/scripts/pipeline.py`. |
| C21 | `.copilot-tracking/changes/2026-11-15/infra-144-container-load-changes.md:62` | Documents pre-existing user-level ruff warnings on 21 untouched legacy `infra/` files left untouched per repository surgical-change rules. |
| C22 | `infra/README.md:3964-3987` | Contains `### Reproducible from-empty deployment sequence` (12 rows, 17 `rebuild.py` stages) plus existing substring anchors asserted by `test_governance.py` and `test_container_hosting_completeness.py`. |

## Parent Synthesis and Recommendations

### Converged Design Decision (Accepted)

1. **Add `infra/parameters/dev.bicepparam` and `infra/parameters/prod.bicepparam`**:
   * Both files use `using '../main.bicep'`, carry explicit `NON-DEPLOYABLE EXAMPLE` / `PLACEHOLDER` safety headers with zero secrets, compile cleanly via `az bicep build-params`, and supply every defaultless parameter in `infra/main.bicep` (`alertEmail`, `sqlAdminGroupName`, `sqlAdminGroupObjectId`) alongside safe private-by-default isolation settings (`allowPublicNetworkAccess = false`, `apiMinReplicas = 0`; `dev.bicepparam` uses `environmentName = 'dev'`, `deploymentProfile = 'development'`; `prod.bicepparam` uses `environmentName = 'pilot'`, `deploymentProfile = 'production'`, `enableLocks = true`, `sqlTier = 'provisioned'`, `keyVaultPurgeProtection = true`, `registryQuarantineEnabled = true`).
2. **Register canonical from-empty steps and expose `verify_from_empty_deployment_reproducibility` in `infra/scripts/pipeline.py` + `infra/scripts/reproducibility_check.py`**:
   * In `infra/scripts/pipeline.py`:
     * Keep positional `operation` choices `("plan", "deploy", "publish", "changed-images", "verify-environment")` intact.
     * Define `FromEmptyStep` (`@dataclass(frozen=True)`), `FROM_EMPTY_STEP_ORDER = ("preflight", "what-if", "deploy", "sql-init", "seed", "smoke")`, `FROM_EMPTY_STEPS: tuple[FromEmptyStep, ...]`, `ENVIRONMENT_PARAMETER_FILES = {"dev": "parameters/dev.bicepparam", "prod": "parameters/prod.bicepparam"}`, and `INJECTED_PARAMETERS: frozenset[str]`.
     * Expose `verify_from_empty_deployment_reproducibility(repo_root: Path = ROOT)` and `execute_from_empty_dry_run(repo_root: Path = ROOT, environment: str = "dev")` delegating via `importlib.util.spec_from_file_location` to `infra/scripts/reproducibility_check.py` so `spec_from_file_location` loaders in `test_pipeline.py` and `test_environment_quota_parameters.py` never require `infra/scripts` on `sys.path`.
   * In `infra/scripts/reproducibility_check.py` (pure stdlib, `--strict` typed, CLI `--check`, `--dry-run`, `--json`):
     * **Check (a)**: Verifies `pipeline.FROM_EMPTY_STEPS` registers all 6 required steps (`preflight`, `what-if`, `deploy`, `sql-init`, `seed`, `smoke`) in exact canonical order, that every step appears in `infra/README.md` (`### Canonical from-empty pipeline step registry`) with matching checked-in repository artifacts that all exist on disk, that all 17 `rebuild.py` stages are partitioned across the 6 steps, and that **zero undocumented manual steps** exist (rejecting blank/placeholder actions, missing artifacts, unowned prerequisites, or undocumented manual prose).
     * **Check (b)**: Parses `infra/main.bicep` (multi-line & comment-safe) to find all parameters without defaults, parses `infra/parameters/dev.bicepparam` and `infra/parameters/prod.bicepparam` (plus `pipeline.PARAMETER_FILES`), AST-verifies `pipeline.py`'s actual parameter injections against `pipeline.INJECTED_PARAMETERS`, rejects unknown parameters in `.bicepparam`, and enforces that every defaultless parameter in `infra/main.bicep` is supplied in both `infra/parameters/dev.bicepparam` and `infra/parameters/prod.bicepparam` OR explicitly injected by `infra/scripts/pipeline.py`.
     * **Check (c)**: Runs `execute_from_empty_dry_run(repo_root, environment)` across `"dev"` and `"prod"`, executing all 6 steps (`preflight` -> `what-if` -> `deploy` -> `sql-init` -> `seed` -> `smoke`) completely offline from repository files alone — driving real `pipeline.verify_environment`, `pipeline.parameters`, `pipeline.summarize_plan`, `pipeline.deployment`, `pipeline.check_sql`, and `pipeline.smoke` via deterministic in-process adapters — and asserts bit-for-bit identical `DryRunResult` and `sequence_digest` across repeated executions.
3. **Update `infra/README.md`**:
   * Document `parameters/dev.bicepparam`, `parameters/prod.bicepparam`, and `scripts/reproducibility_check.py` under `## Layout`.
   * Add `### Canonical from-empty pipeline step registry` immediately following `### Reproducible from-empty deployment sequence` (preserving the 12-row sequence table and all existing governance/container-hosting test substrings intact).
4. **Create `infra/tests/test_from_empty_reproducibility_136.py`**:
   * Positive tests proving criteria (a), (b), and (c) via both `pipeline.verify_from_empty_deployment_reproducibility` and `reproducibility_check.verify_from_empty_deployment_reproducibility`, offline `az bicep build-params` compilation of `infra/parameters/dev.bicepparam` and `infra/parameters/prod.bicepparam`, CLI `--check --dry-run --json` execution, and clean-environment (`os.environ` stripped) multi-run digest determinism.
   * Focused negative/mutation tests proving fail-closed rejection when:
     * A required step (`preflight`, `what-if`, `deploy`, `sql-init`, `seed`, `smoke`) is unregistered from `pipeline.py` or missing/reordered in `infra/README.md`;
     * An undocumented manual step (placeholder/missing script or unowned manual instruction) is added to `infra/README.md`;
     * A parameter without a default is added to `infra/main.bicep` and neither supplied in `dev.bicepparam`/`prod.bicepparam` nor injected by `pipeline.py` (while also testing that supplying it in both `.bicepparam` files OR injecting it in `pipeline.py` satisfies the parameter contract);
     * Any repository artifact required by the offline dry-run is missing or violates private-SQL / auth-denial / digest-pinning invariants.

### Alternatives Considered and Rejected

* **Mutating `pipeline.py` positional `operation` `choices` to add `preflight`, `what-if`, `sql-init`, `seed`, `smoke`**: Rejected because `bicep_inventory.load_pipeline_operations` and `test_bicep_architecture_inventory_136.py:245` explicitly assert `operation` choices equal `("plan", "deploy", "publish", "changed-images", "verify-environment")`. Registering `FROM_EMPTY_STEPS` and `verify_from_empty_deployment_reproducibility` in `pipeline.py` while keeping CLI `operation` choices intact satisfies both `#136` verifiers cleanly.
* **Modifying the 12-row `### Reproducible from-empty deployment sequence` table in `infra/README.md`**: Rejected because `test_bicep_architecture_inventory_136.py:244` asserts `sequence_steps == 12` and exact 5-column headers. Adding sibling `### Canonical from-empty pipeline step registry` immediately after that table keeps `bicep_inventory.py` 100% green while cleanly documenting the 6 canonical pipeline steps.

### Risks, Open Items, and Further Research

* None unresolved; Cycle 1 answered Q1-Q5 with complete `path:line` evidence.

## Readiness and Handoff

* **Research disposition**: `executed`
* **Planning Readiness**: `Ready`
* **Blockers**: None
* **Canonical evidence IDs**: `C1`-`C22`
* **Next phase**: `rpi-plan` (automatic continuation owned by RPI Agent)

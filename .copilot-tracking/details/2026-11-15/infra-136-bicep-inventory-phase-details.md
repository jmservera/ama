<!-- markdownlint-disable-file -->
# RPI Phase Details: Issue 136 Bicep Architecture Inventory and Reproducibility Verifier

## Metadata

* Task ID: issue-136-bicep-inventory-2026-11-15
* Task slug: infra-136-bicep-inventory
* Related plan: .copilot-tracking/plans/2026-11-15/infra-136-bicep-inventory-plan.md
* Evidence sources: .copilot-tracking/research/2026-11-15/infra-136-bicep-inventory-research.md

## Phase Index

| Phase ID | Name                                                                               | Status | Detail sections        |
|----------|------------------------------------------------------------------------------------|--------|------------------------|
| P01      | Implement Architecture-to-Bicep and Reproducibility Verifier                       | Complete | P01, P01-T01           |
| P02      | Reconcile `infra/README.md` Layout, Coverage Register, Module Matrix, and Sequence | Complete | P02, P02-T01           |
| P03      | Add Unit and Mutation Tests and Run Focused Tier Validation                        | Complete | P03, P03-T01, P03-T02  |

<!-- rpi:phase id=P01 -->
## P01: Implement Architecture-to-Bicep and Reproducibility Verifier

### Context

Research (`C1`-`C20`) confirmed that `infra/` has 10 top-level `.bicep` entrypoints (`main.bicep`, `governance.bicep`, `public-edge-existing.bicep`, `iot-hub-live.bicep`, `staff-initializer-rbac.bicep`, `live-receiver-job.bicep`, `live-simulator-job.bicep`, `private-proof-publisher.bicep`, `resident-demo.bicep`, `resident-assistant.bicep`) and 20 `infra/modules/*.bicep` modules, paired with operator/CI wrappers (`infra/scripts/deploy.py`, `infra/scripts/pipeline.py`, companion scripts) and the 17-stage rebuild contract (`src/orchestrator/src/zava_forward/orchestrator/rebuild.py`). Currently no script verifies that ADR 0001-0003 resources, `infra/modules/*.bicep`, and the documented from-empty deployment sequence remain synchronized with `infra/README.md`.

### Intent

Provide a fast, offline, pure-stdlib Python module and CLI (`infra/scripts/bicep_inventory.py`) that parses repository Bicep files, ADR files, deployment scripts, and `infra/README.md` Markdown tables, returning structured diagnostics and non-zero exit status on any coverage, owner, module, or reproducibility drift.

### Boundaries

* Included: `infra/scripts/bicep_inventory.py` only.
* Excluded: Modifying `infra/scripts/deploy.py`, `infra/scripts/pipeline.py`, or any `.bicep` file; invoking `az` or network calls.

### Likely Targets

* infra/scripts/bicep_inventory.py: New architecture-to-Bicep inventory, module delivery matrix, and from-empty reproducibility verifier.

### Dependencies

* None (uses Python 3.12 standard library only).

### Validation Expectations

* `mypy --strict infra/scripts/bicep_inventory.py` passes with 0 issues.
* Both bare `ruff check` and `ruff check --isolated --select E,F,I,B,UP --target-version py312 --line-length 100` plus `ruff format --isolated --line-length 100 --check` pass on `infra/scripts/bicep_inventory.py`.

### Completion Evidence

* `infra/scripts/bicep_inventory.py` exists, exports deterministic parsing and verification APIs, and provides `--check` and `--json` CLI execution.

### Unresolved Items

* None.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Author `infra/scripts/bicep_inventory.py` parser, verifiers, and CLI

#### Context

`bicep_inventory.py` must avoid `EXE001` (do not place an unexecutable shebang on a mode-0644 module invoked via `python3 infra/scripts/bicep_inventory.py`), avoid nested `if`/`with` patterns flagged by `SIM102`/`SIM117`, and enforce fail-closed validation across three contracts corresponding directly to the three `#136` engineering acceptance criteria.

#### Intent

Implement typed dataclasses and pure verification functions in `infra/scripts/bicep_inventory.py`:

1. **Bicep AST-lite declaration scanner (`parse_bicep_file` / `scan_bicep_tree`)**:
   * Strips `//` line comments and `/* ... */` block comments outside single-quoted Bicep strings so commented-out resources or modules are never miscounted as delivered.
   * Extracts `targetScope` (defaulting to `'resourceGroup'` per Bicep spec), `module <symbolic> '<relpath>'` references (resolving to workspace-relative `infra/...` paths), `resource <symbolic> '<Provider/type>@<apiVersion>'` provisioned declarations (including nested child resources if any, though all current child resources in `infra/` use `parent:` top-level `resource` syntax with full `'Provider/parent/child@version'` type strings), and `resource ... existing` declarations separately.
2. **Markdown table parser (`parse_markdown_section_table`)**:
   * Locates exact H3 subheadings inside `infra/README.md`:
     * `### Proposed architecture resource inventory (ADRs 0001, 0002, 0003)`
     * `### Bicep module delivery matrix`
     * `### Reproducible from-empty deployment sequence`
   * Parses pipe-delimited header, separator, and data rows into `tuple[dict[str, str], ...]`, rejecting duplicate keys, malformed column counts, or missing headings.
3. **Verifier 1 — Architecture inventory (`verify_architecture_inventory`)**:
   * Defines `REQUIRED_ARCHITECTURE_COMPONENTS` (canonical component IDs, required ADR citations `ADR 0001` / `ADR 0002` / `ADR 0003`, and ADR anchor phrases verified to exist in `docs/adrs/0001-azure-architecture.md`, `docs/adrs/0002-pilot-readiness-architecture.md`, and `docs/adrs/0003-journey-derived-capabilities-runtime-fit.md`, preserving every non-stale capability from the prior `infra/README.md:3862-3887` register including Contractor Entra B2B guest policy, Microsoft 365/SharePoint permission grants via `infra/scripts/grant-sharepoint-access.sh`, GitHub protected environments/OIDC/branch protection, resource-group budget in `infra/main.bicep`, and `#1258` ranking-archive Blob wiring).
   * Verifies every component is present in Table 1 with a valid disposition (`bicep`, `bicep-conditional`, `manual`, `deferred`):
     * For `bicep` and `bicep-conditional`: parses backticked workspace-relative `.bicep` paths (`infra/...`) and case-insensitive ARM resource types (`microsoft.*`, normalized to lowercase, or `compile-time parameter guard`), confirming every `.bicep` file exists and declares every claimed provisioned ARM resource type (or zero-resource guard module for `guard.bicep`).
     * For `manual` and `deferred`: requires a concrete named owner (rejecting empty, `-`, `none`, `n/a`, `tbd`, `unassigned`, `unknown`) and non-empty operational rationale/artifact notes; when repository JSON/script records are cited (`infra/entra/app-registration.json`, `infra/secret-inventory.json`, `infra/defender-decision.json`, `infra/role-assignments.json`, `infra/scripts/grant-sharepoint-access.sh`), verifies those files exist on disk.
4. **Verifier 2 — Module delivery matrix (`verify_module_delivery_matrix`)**:
   * Discovers all actual `infra/modules/*.bicep` files on disk and requires exact set equality with Table 2's `Module path` column (20 modules).
   * Verifies `Wired in entrypoint(s)` lists actual `.bicep` callers across both `infra/*.bicep` and sibling `infra/modules/*.bicep` (`infra/main.bicep`, `infra/modules/containerapps.bicep`, `infra/modules/iothub.bicep`, `infra/public-edge-existing.bicep`, `infra/iot-hub-live.bicep`, `infra/staff-initializer-rbac.bicep`, `infra/live-receiver-job.bicep`, `infra/live-simulator-job.bicep`, `infra/private-proof-publisher.bicep`, `infra/resident-demo.bicep`, etc.) that contain a `module` reference resolving to that module.
   * Verifies `Provisioned ARM resource types` equals the exact case-normalized (`lowercase`) set of provisioned (non-`existing`) ARM resource types in that module (including lowercase `microsoft.insights/privatelinkscopes*` in `monitoring.bicep`, or explicit `none (compile-time guard)` when the module provisions zero ARM resources, and inversely fails if a module with resources claims `none`).
   * Verifies `Delivery status` is in `{"delivered", "delivered-conditional", "delivered-placeholder-workers", "delivered-guard"}`, and specifically requires `infra/modules/containerapps.bicep` to record `delivered-placeholder-workers` while `infra/main.bicep` still defaults worker image parameters to `mcr.microsoft.com/k8se/quickstart:latest` or `infra/modules/containerapps.bicep` omits explicit worker `command` overrides on `orchestrator` / `importJob` (`#144`).
5. **Verifier 3 — From-empty deployment sequence (`verify_from_empty_sequence`)**:
   * Verifies Table 3 steps are sequentially numbered `1..N` with zero gaps and non-empty `Action` and `Verification check` columns.
   * Requires every step to cite one or more existing workspace-relative repository templates/scripts/workflows (with Step 1 prerequisite explicitly citing `infra/governance.bicep` / `infra/main*.bicepparam` AND naming the explicit manual owner for Azure subscription / `ama` RG / Entra SQL admin group, leaving zero undocumented steps).
   * Parses `STAGES` order from `src/orchestrator/src/zava_forward/orchestrator/rebuild.py` (via `ast.parse`) and verifies all 17 stage names (`parameters` through `restart`) appear in Table 3's `Rebuild stage(s)` column in monotonic order.
   * Cross-checks via `ast.parse` / source inspection that `infra/scripts/deploy.py` (`--apply` and default `what-if`) and `infra/scripts/pipeline.py`'s actual CLI `operation` choices `("plan", "deploy", "publish", "changed-images", "verify-environment")` exist and match the CLI operations referenced by the sequence (explicitly noting that `rebuild.py`'s `"infra/scripts/pipeline.py release"` stage label corresponds to `pipeline.py publish` in CI and `az acr build` in operator rebuilds).
6. **CLI (`main`)**:
   * Supports `--repo-root <path>` (default repository root), `--check` (default behavior when no output mode specified; prints concise pass summary or error list and exits `0`/`1`), and `--json` (prints canonical JSON report and exits `0`/`1`).

#### Boundaries

* Included: `infra/scripts/bicep_inventory.py`.
* Excluded: Test files (P03) and `infra/README.md` edits (P02).

#### Likely Targets

* infra/scripts/bicep_inventory.py: Complete implementation.

#### Dependencies

* None.

#### Validation Expectations

* `mypy --strict` and `ruff check` / `ruff format --check` pass on `infra/scripts/bicep_inventory.py`.

#### Completion Evidence

* Clean module import and CLI `--help` execution.

#### Unresolved Items

* None.

<!-- rpi:phase id=P02 -->
## P02: Reconcile `infra/README.md` Layout, Coverage Register, Module Matrix, and Rebuild Sequence

### Context

`infra/README.md:18-39` (`## Layout`) omits 6 modules in `infra/modules/` and new `bicep_inventory.py`, while `infra/README.md:3852-3890` (`## Resource coverage register (issue 136, 2026-11-04)`) states it is not machine-checked, omits `authTokenStore.bicep` and guard modules, lacks explicit named owners across manual/deferred items, and mistakenly marks SQL Ledger digest upload and scheduled verification as `none | Not built`.

### Intent

Update `infra/README.md` in place so `## Layout` and `## Resource coverage register (issue 136)` become the single, current, machine-verified documentation source of truth for `#136` while preserving every existing operational section and existing test anchor.

### Boundaries

* Included: `infra/README.md` (`## Layout` around lines 18-39 and `## Resource coverage register (issue 136)` around lines 3852-3890).
* Excluded: All prose tested by `test_governance.py` (`"DoNotEnforce"`, `"until the owner accepts a cost"`) and `test_container_hosting_completeness.py` (`"Revision rollback:"`, `"Load run, from"`, `"not at declared scale"`, `"makes no production"`), and the `#115` section immediately following line 3891.

### Likely Targets

* infra/README.md: Reconciled layout listing and three-table machine-checked `#136` coverage, module delivery, and from-empty reproducibility register.

### Dependencies

* P01 (`infra/scripts/bicep_inventory.py` schema and CLI).

### Validation Expectations

* `python3 infra/scripts/bicep_inventory.py --check` exits `0`.
* `python3 -m unittest discover -s infra/tests -p "test_governance.py" -q` and `python3 -m unittest discover -s infra/tests -p "test_container_hosting_completeness.py" -q` pass.
* Markdown style adheres to repository conventions (`*` unordered lists, plain ASCII punctuation, no em dashes, no bolded-prefix list items, no `.copilot-tracking/` references).

### Completion Evidence

* `bicep_inventory.py --check` returns exit code `0` against `infra/README.md`, `infra/main.bicep`, `infra/modules/*.bicep`, `docs/adrs/0001-*.md`..`0003-*.md`, `infra/scripts/deploy.py`, `infra/scripts/pipeline.py`, and `src/orchestrator/src/zava_forward/orchestrator/rebuild.py`.

### Unresolved Items

* None.

<!-- rpi:task id=P02-T01 -->
### P02-T01: Update `## Layout` and `## Resource coverage register (issue 136)` in `infra/README.md`

#### Context

See P02 context and Research `C5`, `C11`, `C20`-`C22`.

#### Intent

Edit `infra/README.md` to:
1. Complete `## Layout` with all 20 `infra/modules/*.bicep` files, standalone entrypoints, and `scripts/bicep_inventory.py`.
2. Replace `## Resource coverage register (issue 136, 2026-11-04)` with `## Resource coverage register (issue 136)` stating clearly that static Bicep coverage, module status, and from-empty repository reproducibility are machine-verified offline by `python3 infra/scripts/bicep_inventory.py --check` (and `infra/tests/test_bicep_architecture_inventory_136.py`), while live Azure runtime health, `#144` real worker job images, `#147` paid Defender activation, and `#440` epic stabilization remain separate runtime/governance gates.
3. Author the three exact Markdown tables (`### Proposed architecture resource inventory (ADRs 0001, 0002, 0003)`, `### Bicep module delivery matrix`, and `### Reproducible from-empty deployment sequence`), retaining all non-stale capabilities from `infra/README.md:3862-3887` (including Contractor B2B guest policy, M365/SharePoint `Sites.Selected` permission grants via `infra/scripts/grant-sharepoint-access.sh`, GitHub protected environments/OIDC/branch protection, RG budget, and `#1258` ranking-archive Blob wiring), using verified Bicep container (`evidence`, `imports`, `quarantine`, `exports`, `audit-archive`, `ledger-digests`, `staff-results`, optional `ranking-archive`), queue (`agent-tasks`, `agent-tasks-poison`, `import-jobs`, `import-jobs-poison`), IoT (`iotHubRoutingReady`, unconditional `iotHub`/budget), and `pipeline.py` CLI (`plan`, `deploy`, `publish`, `changed-images`, `verify-environment`) identifiers, and verify `python3 infra/scripts/bicep_inventory.py --check` passes.

#### Boundaries

* Included: `infra/README.md`.
* Excluded: Other documentation files unless a broken link is discovered (none expected).

#### Likely Targets

* infra/README.md: Targeted section updates.

#### Dependencies

* P01-T01.

#### Validation Expectations

* `python3 infra/scripts/bicep_inventory.py --check` exits `0`.

#### Completion Evidence

* Clean diff of `infra/README.md` with zero em dashes or broken anchors, verified by `bicep_inventory.py --check`.

#### Unresolved Items

* None.

<!-- rpi:phase id=P03 -->
## P03: Add Unit and Mutation Tests and Run Focused Tier Validation

### Context

Caller prompt items 3 and 4 require `infra/tests/test_bicep_architecture_inventory_136.py` proving all three unticked `#136` engineering criteria plus full Focused validation (`ruff check`, `ruff format --isolated --line-length 100 --check`, `mypy --strict`, and `unittest discover -s infra/tests -p "test_*.py" -q`).

### Intent

Lock in automated unit and mutation coverage for `#136` and prove zero regressions across the infrastructure test suite, linter, formatter, and strict type checker.

### Boundaries

* Included: `infra/tests/test_bicep_architecture_inventory_136.py` (new test file, maximum 1 test file added, 0 test files removed) and Focused validation execution.
* Excluded: Unrelated pre-existing `infra/` scripts and tests.

### Likely Targets

* infra/tests/test_bicep_architecture_inventory_136.py: New unit and mutation regression test module.

### Dependencies

* P01, P02.

### Validation Expectations

* `PYTHONDONTWRITEBYTECODE=1 python3 -m ruff check --no-cache infra/scripts/bicep_inventory.py infra/tests/test_bicep_architecture_inventory_136.py` exits `0`.
* `PYTHONDONTWRITEBYTECODE=1 python3 -m ruff check --no-cache --isolated --select E,F,I,B,UP --target-version py312 --line-length 100 infra/scripts/bicep_inventory.py infra/tests/test_bicep_architecture_inventory_136.py` exits `0`.
* `PYTHONDONTWRITEBYTECODE=1 python3 -m ruff format --no-cache --isolated --line-length 100 --check infra/scripts/bicep_inventory.py infra/tests/test_bicep_architecture_inventory_136.py` exits `0`.
* `PYTHONDONTWRITEBYTECODE=1 python3 -m mypy --strict --no-incremental --cache-dir=/dev/null infra/scripts/bicep_inventory.py infra/tests/test_bicep_architecture_inventory_136.py` exits `0`.
* `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src/core/src:src/agents/src:src/api/src:src/orchestrator/src:src/importer/src python3 -m unittest discover -s infra/tests -p "test_*.py" -q` exits `0`.

### Completion Evidence

* Passing test and static-analysis transcripts recorded in `.copilot-tracking/changes/2026-11-15/infra-136-bicep-inventory-changes.md`, plus clean `git status --ignored --short` after commit.

### Unresolved Items

* None.

<!-- rpi:task id=P03-T01 -->
### P03-T01: Create `infra/tests/test_bicep_architecture_inventory_136.py`

#### Context

Following existing `infra/tests/test_deploy.py` and `infra/tests/test_pipeline.py` conventions, `infra/tests/test_bicep_architecture_inventory_136.py` adds `infra/scripts` to `sys.path`, imports `bicep_inventory`, and uses `unittest.TestCase` with full type annotations so `mypy --strict` passes on both the script and test file.

#### Intent

Implement focused semantic and fail-closed mutation tests in `infra/tests/test_bicep_architecture_inventory_136.py`:
1. `test_live_repository_passes_all_issue_136_verifications`: runs `verify_all(REPO_ROOT)` against real `infra/main.bicep`, `infra/modules/*.bicep`, `infra/README.md`, `docs/adrs/0001..0003`, `infra/scripts/deploy.py`, `infra/scripts/pipeline.py`, and `rebuild.py`; asserts 0 errors, all 20 modules present, `ledger-digests` / `ledgerVerify` marked delivered in Bicep (not "Not built"), `containerapps.bicep` marked `delivered-placeholder-workers`, and all manual/deferred rows attributed to a named owner.
2. `test_architecture_inventory_rejects_unmapped_resource_missing_owner_or_false_bicep_claim`: mutates parsed README rows / temporary fixture tree to prove fail-closed errors when (a) a required ADR component row is omitted, (b) a `manual` or `deferred` row has an empty or placeholder owner (`TBD`, `none`, `-`), or (c) a `bicep` row claims a nonexistent `.bicep` path or an ARM resource type not provisioned by that `.bicep` file.
3. `test_module_delivery_matrix_rejects_missing_extra_unwired_or_mismatched_module`: proves fail-closed errors when (a) an on-disk `infra/modules/*.bicep` file is missing from the README table, (b) a phantom module row exists in README without a `.bicep` file, (c) an entrypoint wiring claim is false, (d) provisioned ARM resource types drift from the `.bicep` file, or (e) `containerapps.bicep` claims `delivered` while placeholder worker defaults (`mcr.microsoft.com/k8se/quickstart:latest` in `infra/main.bicep` or missing `orchestrator`/`importJob` `command` overrides in `infra/modules/containerapps.bicep`) remain.
4. `test_from_empty_sequence_rejects_undocumented_step_missing_script_or_missing_rebuild_stage`: proves fail-closed errors when (a) a sequence step omits its repository script/template or verification check, (b) a cited script/template path does not exist, (c) step numbering has a gap, or (d) any of the 17 `rebuild.py` stages or `pipeline.py` CLI `operation` choices (`plan`, `deploy`, `publish`, `changed-images`, `verify-environment`) is dropped or out of order.
5. `test_bicep_parser_ignores_comments_and_separates_existing_resources`: verifies `//` and `/* ... */` commented-out `resource`/`module` lines and `existing` resources are never misclassified as provisioned ARM resources.
6. `test_cli_check_and_json_modes`: exercises `bicep_inventory.main(["--check"])` (`0`) and `bicep_inventory.main(["--json"])` (`0`, valid JSON payload with module count == 20 and `ok == True`).

#### Boundaries

* Included: `infra/tests/test_bicep_architecture_inventory_136.py`.
* Excluded: Modifying existing test files.

#### Likely Targets

* infra/tests/test_bicep_architecture_inventory_136.py: New test file.

#### Dependencies

* P01-T01, P02-T01.

#### Validation Expectations

* `python3 -m unittest discover -s infra/tests -p "test_bicep_architecture_inventory_136.py" -v` passes in <1s.

#### Completion Evidence

* All 6 test methods pass and reject their targeted mutations.

#### Unresolved Items

* None.

<!-- rpi:task id=P03-T02 -->
### P03-T02: Execute Focused validation suite and clean cache hygiene check

#### Context

Research Wave 3 (`C23`, `C24`) identified exact flags and environment variables required so validation leaves zero `.ruff_cache`, `.mypy_cache`, or `__pycache__` artifacts in the worktree and resolves `zava_forward` imports across all 482+ `infra/tests` tests.

#### Intent

Run:
1. Target strict static checks (`ruff check --no-cache` bare + `--isolated`, `ruff format --no-cache --isolated --line-length 100 --check`, `mypy --strict --no-incremental --cache-dir=/dev/null`) on `infra/scripts/bicep_inventory.py` and `infra/tests/test_bicep_architecture_inventory_136.py`, and also record the directory-wide `ruff --no-cache` status transparently without modifying unrelated legacy files.
2. Offline Bicep compile/lint sanity (`az bicep build` / `az bicep lint` if needed, also covered inside `test_bicep_policy.py` when `REQUIRE_AZ_BICEP=1`).
3. Full `infra/tests` discovery: `PYTHONDONTWRITEBYTECODE=1 REQUIRE_AZ_BICEP=1 PYTHONPATH=src/core/src:src/agents/src:src/api/src:src/orchestrator/src:src/importer/src python3 -m unittest discover -s infra/tests -p "test_*.py" -q` (`initial_wait: 300`).
4. Verify zero `.copilot-tracking/` leaks in new Python files, modified sections / diff of `infra/README.md`, and commit messages, plus clean `git status --ignored --short`.

#### Boundaries

* Included: Read-only validation execution and cache cleanup (`rm -rf` of any cache written inside worktree if created).
* Excluded: Editing unrelated pre-existing files.

#### Likely Targets

* None (verification task).

#### Dependencies

* P03-T01.

#### Validation Expectations

* Zero failures or errors across all checks.

#### Completion Evidence

* Recorded exit codes and summaries in `.copilot-tracking/changes/2026-11-15/infra-136-bicep-inventory-changes.md`.

#### Unresolved Items

* None.

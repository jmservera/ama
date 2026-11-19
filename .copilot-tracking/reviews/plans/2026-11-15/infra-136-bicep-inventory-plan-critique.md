<!-- markdownlint-disable-file -->
# RPI Plan Critique: Issue 136 Bicep Architecture Inventory and Reproducibility Verifier

## Metadata

* Task ID: issue-136-bicep-inventory-2026-11-15
* Critique date: 2026-11-15
* Plan: .copilot-tracking/plans/2026-11-15/infra-136-bicep-inventory-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/infra-136-bicep-inventory-phase-details.md
* Critique execution status: Complete

## Inputs and Criterion Boundary

* Task context and caller requirements: Deliver machine-checked repository evidence for the three unticked engineering acceptance criteria of issue `#136` via `infra/scripts/bicep_inventory.py`, targeted `infra/README.md` updates (`## Layout` and `## Resource coverage register (issue 136)` preserving `test_governance.py` and `test_container_hosting_completeness.py` substrings), and `infra/tests/test_bicep_architecture_inventory_136.py` (exact test removals: none; maximum test file additions: 1), validated at the Focused tier (`ruff check`, `ruff format --isolated --line-length 100 --check`, `mypy --strict`, and `unittest discover -s infra/tests -p "test_*.py" -q`) and committed locally without pushing.
* Research and evidence considered: .copilot-tracking/research/2026-11-15/infra-136-bicep-inventory-research.md (`C1`-`C24`), .copilot-tracking/plans/2026-11-15/infra-136-bicep-inventory-plan.md, .copilot-tracking/details/2026-11-15/infra-136-bicep-inventory-phase-details.md, infra/main.bicep, all 20 files in infra/modules/*.bicep, infra/scripts/deploy.py, infra/scripts/pipeline.py, infra/README.md, docs/adrs/0001-azure-architecture.md, docs/adrs/0002-pilot-readiness-architecture.md, docs/adrs/0003-journey-derived-capabilities-runtime-fit.md, src/orchestrator/src/zava_forward/orchestrator/rebuild.py, infra/tests/test_governance.py, and infra/tests/test_container_hosting_completeness.py.
* Decisions, dependencies, and acceptance criteria considered: `#136` engineering criteria 1-3, plan `FR-1`..`FR-5`, `NFR-1`..`NFR-3`, `AC-1`..`AC-5`, Focused validation tier rules, worktree cache hygiene, and non-goals (`#144` runtime worker image replacement, `#147` paid Defender activation, `#440` epic stabilization checkpoint, and live Azure calls remain out of scope).
* Assessment boundary: Evaluates static alignment and implementability of the plan and phase details against the supplied research and repository files. Does not execute live Azure CLI deployments, live `what-if` calls, or full `infra/tests` runtime execution.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
|------------------------------------------|----------|---------------------|
| FR-1 (`Bicep declaration parser`) | Partial | Covers 20 `infra/modules/*.bicep` files, `existing` separation, and zero-resource guards, but `P01-T01` assumes `Microsoft....` uppercase prefix while `infra/modules/monitoring.bicep:43,55,61` uses lowercase `microsoft.insights/...` (`PC-003`). |
| FR-2 / AC-1 (`ADR 0001-0003 inventory`) | Partial | Enforces `bicep`/`bicep-conditional`/`manual`/`deferred` dispositions and non-placeholder named owners, but replacing `infra/README.md:3852-3890` without explicitly retaining existing B2B guest, SharePoint admin-consent, and GitHub OIDC/environment rows drops tracked manual items (`PC-005`). |
| FR-3 / AC-2 (`20-module delivery matrix`) | Partial | Covers 20-of-20 module parity and fixes the stale ledger-digest row (`C11`), but checks `containerapps.bicep` for `mcr.microsoft.com/k8se/quickstart-jobs:latest` when placeholder defaults (`mcr.microsoft.com/k8se/quickstart:latest`) actually reside in `infra/main.bicep:55,66,68,452` (`PC-002`), and Research `C3`/`C9` carries stale parameter/container/queue names (`PC-003`). |
| FR-4 / AC-3 (`From-empty reproducibility`) | Partial | Ties steps to `rebuild.py` 17 `STAGES` and scripts on disk, but specifies non-existent `infra/scripts/pipeline.py` CLI subcommands (`parameters`, `release`, `what-if`, `smoke`) instead of actual `choices=("plan", "deploy", "publish", "changed-images", "verify-environment")` (`PC-001`). |
| FR-5 / AC-4 (`Unit and mutation tests`) | Partial | Positive and fail-closed mutation structure in `infra/tests/test_bicep_architecture_inventory_136.py` is well-bounded (1 file added, 0 removed), except mutations `3e` and `4d` encode the mismatched placeholder location (`PC-002`) and `pipeline.py` subcommand list (`PC-001`). |
| NFR-1 (`Offline stdlib <1s`) | Covered | Pure Python 3.12 stdlib static parsing without `az` or network calls is credible and avoids repeating 45s Bicep builds already run in `test_bicep_policy.py`. |
| NFR-2 (`Strict typing, lint, hygiene`) | Partial | Covers `mypy --strict`, bare and `--isolated` Ruff checks, and existing README test anchors (`C21`, `C22`), but `P03` hardcodes `/tmp` cache env vars instead of `--no-cache` and `--cache-dir=/dev/null` (`PC-006`). |
| NFR-3 (`Tracking path isolation`) | Partial | Requires zero `.copilot-tracking/` substrings across the entire `infra/README.md` file, which conflicts with pre-existing untouched historical occurrences at `infra/README.md:1652` and `infra/README.md:4421` (`PC-004`). |
|AC-5 (`Clean local commit, no push`) | Covered | Preserves branch, privacy-safe noreply email, Copilot trailer, and non-push boundary. |
| P01 / P01-T01 | Partial | Clear module architecture; requires targeted corrections for `PC-001`, `PC-002`, `PC-003`, and `PC-005`. |
| P02 / P02-T01 | Partial | Preserves `test_governance.py` and `test_container_hosting_completeness.py` substrings and `#115`/`#1258` sections; requires accurate CLI/Bicep identifiers (`PC-001`, `PC-003`) and manual-row retention (`PC-005`). |
| P03 / P03-T01 / P03-T02 | Partial | Strong fail-closed test coverage design; requires updated assertions/mutations (`PC-001`, `PC-002`), scoped `NFR-3` check (`PC-004`), and cache-free flags (`PC-006`). |

## Verdict

* Verdict: Revise
* Rationale: The three-phase architecture (`infra/scripts/bicep_inventory.py`, `infra/README.md`, and `infra/tests/test_bicep_architecture_inventory_136.py`) is sound and directly proves the three engineering acceptance criteria of `#136`, but six concrete repository-vs-plan discrepancies (`2 High`, `3 Medium`, `1 Low`) would cause false verification failures or introduce inaccurate CLI/Bicep claims in `infra/README.md` if implemented verbatim. Every finding has exact repository resolving evidence and can be corrected directly by the planning parent without user input.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: `infra/scripts/pipeline.py` CLI subcommands in FR-4, P01-T01, and P03-T01 do not match actual parser choices

* Related IDs: FR-4, AC-3, C19, C20, P01-T01, P02-T01, P03-T01
* Evidence: .copilot-tracking/plans/2026-11-15/infra-136-bicep-inventory-plan.md:92,146; .copilot-tracking/details/2026-11-15/infra-136-bicep-inventory-phase-details.md:107,230; .copilot-tracking/research/2026-11-15/infra-136-bicep-inventory-research.md:191; infra/scripts/pipeline.py:92,153,293,341,385,424-426; src/orchestrator/src/zava_forward/orchestrator/rebuild.py:40
* Concern: `FR-4` and `P01-T01` item 5 require `bicep_inventory.py` (via `ast.parse`) and `infra/README.md` to verify and document `infra/scripts/pipeline.py` CLI subcommands as `("parameters", "release", "what-if", "deploy", "smoke", "verify-environment")` (inherited from Research `C19`). In `infra/scripts/pipeline.py:424-426`, positional `operation` defines `choices=("plan", "deploy", "publish", "changed-images", "verify-environment")`. `parameters` (`infra/scripts/pipeline.py:92`) and `smoke` (`infra/scripts/pipeline.py:293`) are internal Python functions called inside `deployment()` (`infra/scripts/pipeline.py:341`); `az deployment group what-if` runs inside `deployment()` (`infra/scripts/pipeline.py:385`) for both `plan` and `deploy`; and `publish` (`infra/scripts/pipeline.py:153`) pushes images and writes digest metadata, whereas `release` appears only in the prose string `"infra/scripts/pipeline.py release"` on `Stage("images", ...)` in `src/orchestrator/src/zava_forward/orchestrator/rebuild.py:40`.
* Impact: Implementing `P01-T01` item 5 as written will either fail AST CLI verification against `infra/scripts/pipeline.py` or document non-existent CLI invocations (`pipeline.py parameters`, `pipeline.py release`, `pipeline.py what-if`, `pipeline.py smoke`) in `infra/README.md`, directly undermining `#136` criterion 2 ("reproducible from the repository without undocumented steps").
* Smallest useful change: Update `FR-4`, `P01-T01` item 5, `P02-T01`, and `P03-T01` item 4 so `bicep_inventory.py` checks `infra/scripts/pipeline.py`'s actual CLI `operation` choices `("plan", "deploy", "publish", "changed-images", "verify-environment")` (and optionally internal helper functions `parameters`, `deployment`, `smoke`), and explicitly documents in Table 3 how `rebuild.py` stage `images` (`"infra/scripts/pipeline.py release"` contract label) maps to `infra/scripts/pipeline.py publish` in CI and `az acr build` in operator rebuilds.
* Action owner: planning_parent
* Exact resolving evidence: Revised `FR-4` in .copilot-tracking/plans/2026-11-15/infra-136-bicep-inventory-plan.md and `P01-T01` / `P02-T01` / `P03-T01` in .copilot-tracking/details/2026-11-15/infra-136-bicep-inventory-phase-details.md matching `choices=("plan", "deploy", "publish", "changed-images", "verify-environment")` in `infra/scripts/pipeline.py:424-426`.
* Decision route: direct_planner_correction

<!-- rpi:critique id=PC-002 -->
### PC-002 [High]: `#144` placeholder worker image check inspects the wrong Bicep file and wrong placeholder image string

* Related IDs: FR-3, AC-2, C4, C6, P01-T01, P02-T01, P03-T01
* Evidence: .copilot-tracking/plans/2026-11-15/infra-136-bicep-inventory-plan.md:187; .copilot-tracking/details/2026-11-15/infra-136-bicep-inventory-phase-details.md:99,228; infra/modules/containerapps.bicep:40,46-48,340-432,530-583; infra/main.bicep:55,66,68,452; infra/scripts/deploy.py:12
* Concern: `P01-T01` item 4 (`phase-details.md:99`) and `P03-T01` item 3e (`phase-details.md:228`) require `bicep_inventory.py` to enforce `delivered-placeholder-workers` on `infra/modules/containerapps.bicep` *"while `containerapps.bicep` still carries placeholder worker defaults (`mcr.microsoft.com/k8se/quickstart-jobs:latest` / `#144`)"*. Inspection of `infra/modules/containerapps.bicep:40,46-48` shows `apiImage`, `agentImage`, `orchestratorImage`, and `importImage` have no default values in `containerapps.bicep` and zero occurrences of `mcr.microsoft.com/k8se/`. Instead, the placeholder defaults live in `infra/main.bicep:55,66,68,452` (and `infra/scripts/deploy.py:12`) with image string `mcr.microsoft.com/k8se/quickstart:latest` (not `quickstart-jobs:latest`), while `containerapps.bicep` exhibits `#144` via missing `command` definitions on `orchestrator` (`infra/modules/containerapps.bicep:396-432`) and `importJob` (`infra/modules/containerapps.bicep:530-583`) and standby-only `agents` Container App wiring (`infra/modules/containerapps.bicep:340-394`, lacking `ZF_AGENT_RESULT_ROUTE=enabled`).
* Impact: Searching `infra/modules/containerapps.bicep` for `mcr.microsoft.com/k8se/quickstart-jobs:latest` returns no match against the live repository, causing either false failure on valid `delivered-placeholder-workers` status or a dead guard that fails to reject premature `delivered` claims in `P03-T01` item 3e.
* Smallest useful change: Update `P01-T01` item 4, `P03-T01` item 3e, and Plan `Follow-Up Items` so `bicep_inventory.py` detects `#144` placeholder worker status from `mcr.microsoft.com/k8se/quickstart:latest` worker defaults in `infra/main.bicep` (`agentImage`, `importImage`, and empty `orchestratorImage` fallback) together with missing `command` overrides on `orchestrator` / `importJob` in `infra/modules/containerapps.bicep`.
* Action owner: planning_parent
* Exact resolving evidence: Revised `P01-T01` item 4 and `P03-T01` item 3e in .copilot-tracking/details/2026-11-15/infra-136-bicep-inventory-phase-details.md and `Follow-Up Items` in .copilot-tracking/plans/2026-11-15/infra-136-bicep-inventory-plan.md citing `mcr.microsoft.com/k8se/quickstart:latest` in `infra/main.bicep:55,66,68,452` and worker container blocks in `infra/modules/containerapps.bicep`.
* Decision route: direct_planner_correction

<!-- rpi:critique id=PC-003 -->
### PC-003 [Medium]: Lowercase ARM provider types in `monitoring.bicep`, module-to-module callers, and stale Research `C3`/`C9` identifiers risk false drift errors

* Related IDs: FR-1, FR-2, FR-3, C3, C8, C9, P01-T01, P02-T01
* Evidence: .copilot-tracking/details/2026-11-15/infra-136-bicep-inventory-phase-details.md:74-77,91,96-98,167-170; .copilot-tracking/research/2026-11-15/infra-136-bicep-inventory-research.md:106-107,141,173,181; infra/modules/monitoring.bicep:43,55,61; infra/modules/storage.bicep:59,130; infra/main.bicep:25-39,371-391; infra/modules/iothub.bicep:44,209
* Concern: Three concrete Bicep details differ from `P01-T01` and Research `C3`/`C9`: (1) `P01-T01` item 3 (`phase-details.md:91`) extracts backticked ARM types matching `Microsoft....` and item 4 (`phase-details.md:98`) checks exact set equality, but `infra/modules/monitoring.bicep:43,55,61` declares lowercase `'microsoft.insights/privateLinkScopes@2021-07-01-preview'` and `'microsoft.insights/privateLinkScopes/scopedResources@2021-07-01-preview'`. (2) `envDns.bicep` and `privateEndpoint.bicep` are wired via `module` declarations inside sibling `infra/modules/*.bicep` files (and standalone `infra/resident-assistant.bicep`), not directly in `infra/main.bicep`, so `scan_bicep_tree` must resolve module callers across both `infra/*.bicep` and `infra/modules/*.bicep`. (3) Research Wave 1 and `C3`/`C9` (`research.md:106-107,141,173,181`) cite non-existent flags `enableIotHub` and `enableIotTransportBudget` (`module iotHub` in `infra/main.bicep:371` and `resource budget` in `infra/modules/iothub.bicep:209` are unconditional; `iotHubRoutingReady` is the conditional route flag) and list outdated `storage.bicep` container/queue names (`reports`, `m365-fallback`, `agent-jobs`) instead of actual containers `['evidence', 'imports', 'quarantine', 'exports', 'audit-archive', 'ledger-digests', 'staff-results']` (`infra/modules/storage.bicep:59`) and queues `['agent-tasks', 'agent-tasks-poison', 'import-jobs', 'import-jobs-poison']` (`infra/modules/storage.bicep:130`).
* Impact: Case-sensitive `Microsoft.` matching fails on `monitoring.bicep` AMPLS resources, and carrying Research `C3`/`C9` flag/container/queue names into `infra/README.md` or `REQUIRED_ARCHITECTURE_COMPONENTS` introduces fresh factual inaccuracies in the `#136` coverage register.
* Smallest useful change: Specify case-insensitive `microsoft.*` ARM resource type parsing and normalized lowercase set comparison in `P01-T01` (consistent with `rebuild.py:70-100`), confirm `Wired in entrypoint(s)` accepts callers in both `infra/*.bicep` and `infra/modules/*.bicep`, and note in `P02-T01` that `infra/README.md` must record actual Bicep parameter, container, and queue names from `main.bicep`, `iothub.bicep`, and `storage.bicep`.
* Action owner: planning_parent
* Exact resolving evidence: Revised `P01-T01` and `P02-T01` in .copilot-tracking/details/2026-11-15/infra-136-bicep-inventory-phase-details.md specifying case-insensitive ARM type normalization, `infra/*.bicep` + `infra/modules/*.bicep` caller resolution, and verified `storage.bicep` / `iothub.bicep` / `main.bicep` names.
* Decision route: direct_planner_correction

<!-- rpi:critique id=PC-004 -->
### PC-004 [Medium]: `NFR-3` whole-file `infra/README.md` `.copilot-tracking/` ban conflicts with pre-existing untouched historical lines

* Related IDs: NFR-3, P02, P03-T01, P03-T02
* Evidence: .copilot-tracking/plans/2026-11-15/infra-136-bicep-inventory-plan.md:107-110; .copilot-tracking/details/2026-11-15/infra-136-bicep-inventory-phase-details.md:142-145,262; infra/README.md:1652,4421
* Concern: `NFR-3` (`plan.md:107-110`) and `P03-T02` item 4 (`phase-details.md:262`) require zero `.copilot-tracking/` substrings anywhere in `infra/README.md` (*"Content check confirms `.copilot-tracking/` appears only inside `.copilot-tracking/` files"*). However, `infra/README.md` already contains pre-existing `.copilot-tracking/` strings at lines `1652` (twice) and `4421` inside historical dated notes outside `P02`'s bounded edit sections (`## Layout` at `18-39` and `## Resource coverage register` at `3852-3890`).
* Impact: Running a whole-file substring check on `infra/README.md` will fail `NFR-3` unless implementation edits unrelated historical documentation that `P02` explicitly excludes.
* Smallest useful change: Scope `NFR-3` and `P03-T02` item 4 so `.copilot-tracking/` is forbidden anywhere in `infra/scripts/bicep_inventory.py`, `infra/tests/test_bicep_architecture_inventory_136.py`, commit messages, and the added/modified diff (or `## Layout` and `## Resource coverage register (issue 136)` sections) of `infra/README.md`.
* Action owner: planning_parent
* Exact resolving evidence: Updated `NFR-3` in .copilot-tracking/plans/2026-11-15/infra-136-bicep-inventory-plan.md and `P03-T02` in .copilot-tracking/details/2026-11-15/infra-136-bicep-inventory-phase-details.md scoping the `infra/README.md` check to modified sections / added diff lines.
* Decision route: direct_planner_correction

<!-- rpi:critique id=PC-005 -->
### PC-005 [Medium]: Replacing `infra/README.md` coverage register without carrying forward pre-existing manual rows drops tracked tenant and CI boundaries

* Related IDs: FR-2, AC-1, C1, C11, P01-T01, P02-T01
* Evidence: .copilot-tracking/details/2026-11-15/infra-136-bicep-inventory-phase-details.md:85-93,169-170; .copilot-tracking/research/2026-11-15/infra-136-bicep-inventory-research.md:112-122; infra/README.md:3862-3887; docs/adrs/0001-azure-architecture.md
* Concern: `P02-T01` replaces the existing `## Resource coverage register (issue 136, 2026-11-04)` section (`infra/README.md:3852-3890`) in place. That table currently records three manual governance/tenant items that were omitted from Research Wave 1's 10-bullet manual list (`research.md:112-122`): Contractor Entra B2B guest policy and cross-tenant settings (`infra/README.md:3879`, `ADR 0001`), Microsoft 365 and SharePoint `Sites.Selected` admin consent (`infra/README.md:3880`, `infra/scripts/grant-sharepoint-access.sh`, `ADR 0001`), and GitHub protected environments, required reviewers, OIDC federation, and branch protection (`infra/README.md:3881`, verified at deploy time by `infra/scripts/pipeline.py verify-environment`).
* Impact: Populating `REQUIRED_ARCHITECTURE_COMPONENTS` (`P01-T01`) and Table 1 (`P02-T01`) exclusively from Research Wave 1's 10 manual bullets would silently delete existing `#136` manual-owner disclosures when lines `3852-3890` are replaced.
* Smallest useful change: Explicitly require `REQUIRED_ARCHITECTURE_COMPONENTS` in `P01-T01` and Table 1 in `P02-T01` to preserve all non-stale capabilities from `infra/README.md:3862-3887` (including Contractor B2B guest policy, M365/SharePoint permission grants via `infra/scripts/grant-sharepoint-access.sh`, GitHub environments/OIDC/branch protection, and opt-in `#1258` ranking-archive Blob wiring) with explicit named owners.
* Action owner: planning_parent
* Exact resolving evidence: Updated `P01-T01` item 3 and `P02-T01` item 3 in .copilot-tracking/details/2026-11-15/infra-136-bicep-inventory-phase-details.md requiring retention of those existing `infra/README.md:3862-3887` rows in `REQUIRED_ARCHITECTURE_COMPONENTS` and Table 1.
* Decision route: direct_planner_correction

<!-- rpi:critique id=PC-006 -->
### PC-006 [Low]: Phase P03 validation commands write caches to `/tmp` instead of using tool-native cache-disable flags

* Related IDs: NFR-2, C23, P03, P03-T02
* Evidence: .copilot-tracking/details/2026-11-15/infra-136-bicep-inventory-phase-details.md:202-205,254-263
* Concern: `P03` Validation Expectations specify `RUFF_CACHE_DIR=/tmp/ruff-cache-136` and `MYPY_CACHE_DIR=/tmp/mypy-cache-136` to avoid creating `.ruff_cache` and `.mypy_cache` in the worktree. Both tools support native cacheless flags (`ruff check --no-cache`, `ruff format --no-cache`, and `mypy --no-incremental --cache-dir=/dev/null`) that avoid writing to `/tmp` as well as the worktree.
* Impact: Executing `P03` commands verbatim creates unnecessary `/tmp` directories and violates host rules in environments that prohibit `/tmp` writes.
* Smallest useful change: Replace `RUFF_CACHE_DIR=/tmp/ruff-cache-136` and `MYPY_CACHE_DIR=/tmp/mypy-cache-136` in `P03` and `P03-T02` with `--no-cache` for `ruff` and `--no-incremental --cache-dir=/dev/null` for `mypy --strict` alongside `PYTHONDONTWRITEBYTECODE=1`.
* Action owner: planning_parent
* Exact resolving evidence: Updated validation commands in `P03` and `P03-T02` of .copilot-tracking/details/2026-11-15/infra-136-bicep-inventory-phase-details.md with zero `/tmp` paths.
* Decision route: direct_planner_correction

## Strengths and Residual Risk

* Strong architectural fit: Splitting static verification into pure-stdlib `infra/scripts/bicep_inventory.py` plus three deterministic `infra/README.md` tables and fail-closed mutation tests in `infra/tests/test_bicep_architecture_inventory_136.py` directly proves all three engineering criteria of `#136` in under a second without duplicating slow `az bicep build` compilation already enforced in `test_bicep_policy.py`.
* Honest evidence boundaries: The plan rightly refuses to conflate static Bicep coverage and repository script reproducibility with live Azure deployment health, `#144` real background worker runtime wiring, `#147` paid Defender activation, or `#440` epic stabilization closure, and explicitly protects existing `test_governance.py` and `test_container_hosting_completeness.py` substrings in `infra/README.md`.
* Confirmed Bicep child-resource syntax: Inspection across all 20 `infra/modules/*.bicep` files confirms `P01-T01` item 1's parser observation that every child resource in `infra/modules/` uses top-level `resource <sym> '<Provider/parent/child>@<version>'` syntax with `parent:` (plus `existing` declarations in `authTokenStore.bicep`, `edge-existing-auth.bicep`, and `sql.bicep`, and four zero-resource compile-time parameter guards: `guard.bicep`, `edge-existing-guard.bicep`, `iothub-scope-guard.bicep`, and `staff-initializer-guard.bicep`).
* Explicitly accepted residual risk: Twenty-one pre-existing untouched Python files in `infra/scripts/` and `infra/tests/` pre-date non-isolated Ruff formatting; keeping edits strictly scoped to the three target files while passing both bare `ruff check` and `src-ci.yml` `--isolated` lint/format plus `mypy --strict` on modified files matches repository scope rules.

## Questions or Blocking Evidence Gaps

* None. All six findings are resolved by supplied repository files and require no user decision or additional research cycle.

## Limitations

* This critique verified static Bicep templates, ADRs 0001-0003, `deploy.py`, `pipeline.py`, `rebuild.py`, `infra/README.md`, and existing governance/container-hosting test invariants within the read-only boundary; it did not execute live Azure commands or modify repository files.

## Recommended Next Action

* Highest-impact finding: PC-001
* Action owner: planning_parent
* Smallest next action: Apply direct planner revisions for `PC-001` through `PC-006` in `.copilot-tracking/plans/2026-11-15/infra-136-bicep-inventory-plan.md` and `.copilot-tracking/details/2026-11-15/infra-136-bicep-inventory-phase-details.md`, record the critique disposition table, and finalize the plan for `rpi-implement` without running another critique pass.
* User response required: no

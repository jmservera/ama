<!-- markdownlint-disable-file -->
# Review: Issue 136 Bicep Architecture Inventory and Reproducibility Verifier

## Scope and Evidence

* Task ID: issue-136-bicep-inventory-2026-11-15
* Review date: 2026-11-15
* Review scope: Full task (`P01`, `P02`, `P03`)
* Assessed boundary: Offline architecture-to-Bicep resource inventory (`ADRs 0001-0003`), 20-module Bicep delivery matrix, 12-step (17-stage) reproducible from-empty deployment sequence verifier (`infra/scripts/bicep_inventory.py`), reconciled `infra/README.md` documentation register, unit/mutation test suite (`infra/tests/test_bicep_architecture_inventory_136.py`), and Focused tier validation (`ruff`, `mypy --strict`, `infra/tests`).
* Plan: .copilot-tracking/plans/2026-11-15/infra-136-bicep-inventory-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/infra-136-bicep-inventory-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-11-15/infra-136-bicep-inventory-plan-critique.md
* Changes: .copilot-tracking/changes/2026-11-15/infra-136-bicep-inventory-changes.md
* Other evidence considered: .copilot-tracking/research/2026-11-15/infra-136-bicep-inventory-research.md (`C1`-`C24`), `infra/scripts/bicep_inventory.py`, `infra/README.md` diff, `infra/tests/test_bicep_architecture_inventory_136.py`, and live Focused validation execution (`608` `infra/tests` unit tests, `ruff`, `mypy --strict`).

## Opening Review State

* Interpreted review goal: Verify once, with read-only discipline over source and planning artifacts, that the implemented `#136` verifier, `infra/README.md` tables, and unit/mutation test suite prove all three `#136` engineering acceptance criteria, honor all six critique dispositions (`PC-001`..`PC-006`), and remain reconciled across plan, details, changes, and validation evidence.
* Review scope: Full task (`P01`..`P03`)
* Evidence readiness: Ready (all canonical artifacts present, reconciled, and complete)
* Acceptance basis: Plan `FR-1`..`FR-5`, `NFR-1`..`NFR-3`, `AC-1`..`AC-5`, and resolved critique dispositions `PC-001`..`PC-006`
* First comparison boundary: Plan-to-change marker reconciliation across `P01-T01`, `P02-T01`, `P03-T01`, and `P03-T02` before inspecting implementation details and validation results
* Active read-only boundaries: Write authority restricted strictly to `.copilot-tracking/reviews/logs/2026-11-15/infra-136-bicep-inventory-review.md` (plus RPI Agent state record managed by the parent wrapper)
* Initial blockers: None

## Execution Status

* Execution status: Complete
* Review execution evidence: Completed single post-implementation review on 2026-11-15 across `.copilot-tracking/plans/2026-11-15/infra-136-bicep-inventory-plan.md`, `.copilot-tracking/details/2026-11-15/infra-136-bicep-inventory-phase-details.md`, `.copilot-tracking/reviews/plans/2026-11-15/infra-136-bicep-inventory-plan-critique.md`, `.copilot-tracking/changes/2026-11-15/infra-136-bicep-inventory-changes.md`, `infra/scripts/bicep_inventory.py`, `infra/README.md`, and `infra/tests/test_bicep_architecture_inventory_136.py`.

## Plan-to-Change Reconciliation

| Current plan scope | Descriptive changes-record summary | Current-state reconciliation | Gap or rationale |
| --- | --- | --- | --- |
| `P01` / `P01-T01` | `P01 / P01-T01: Architecture-to-Bicep and reproducibility verifier` | Reconciled | `[x]` checked in plan, `Complete` in phase details, and backed by `infra/scripts/bicep_inventory.py` |
| `P02` / `P02-T01` | `P02 / P02-T01: Reconciled infra/README.md layout, coverage register, module matrix, and deployment sequence` | Reconciled | `[x]` checked in plan, `Complete` in phase details, and verified via `bicep_inventory.py --check` |
| `P03` / `P03-T01`, `P03-T02` | `P03 / P03-T01 and P03-T02: Unit/mutation tests and Focused validation` | Reconciled | `[x]` checked in plan, `Complete` in phase details, and backed by 8 unit/mutation tests + 608 passing `infra/tests` |
| `Follow-Up Items` | `#144` placeholder worker image/command defaults; `#147` Defender cost approval and Policy enforcement | Reconciled | Kept outside active `Pxx`/`Pxx-Txx` completion claims in both plan and changes log |

## Completed Work Assessment

| Related marker | Files | What changed and why | Completion evidence | Validation | Assessment |
| --- | --- | --- | --- | --- | --- |
| `P01-T01` (`P01`) | `infra/scripts/bicep_inventory.py` | Added pure-stdlib offline Bicep parser, 29-row ADR 0001-0003 inventory verifier, 20-module delivery matrix checker (including `#144` placeholder worker detection across `main.bicep` and `containerapps.bicep`), and 17-stage rebuild / `deploy.py` / `pipeline.py` CLI reproducibility verifier | `bicep_inventory.py --check` and `--json` exit `0` | `ruff check`, `ruff format --check`, `mypy --strict` all passed | Reconciled and conformant |
| `P02-T01` (`P02`) | `infra/README.md` | Updated `ms.date` (`2026-11-15`), expanded `## Layout` to all 10 top-level `.bicep` files and all 20 `infra/modules/*.bicep` modules plus `bicep_inventory.py` and `pipeline.py`, and replaced the stale 2026-11-04 coverage table with the three canonical `#136` machine-verified tables while preserving governance and container-hosting test anchors | `102` insertions / `43` deletions in `infra/README.md`; zero `.copilot-tracking/` substrings in diff | `bicep_inventory.py --check` (`29` arch rows, `20` modules, `12` steps), `test_governance.py` and `test_container_hosting_completeness.py` (`20` tests OK) | Reconciled and conformant |
| `P03-T01` (`P03`) | `infra/tests/test_bicep_architecture_inventory_136.py` | Added 8 unit and fail-closed mutation tests proving live repository conformance plus rejection of missing ADR rows, missing manual owners, unprovisioned ARM types, missing/extra modules, premature `#144` worker status, caller drift, missing scripts, undocumented steps, and rebuild stage gaps | `8` tests pass in `0.523s` | `ruff check`, `ruff format --check`, `mypy --strict`, `unittest -v` passed | Reconciled and conformant |
| `P03-T02` (`P03`) | Worktree validation & hygiene | Executed Focused validation suite with cacheless flags (`--no-cache`, `--no-incremental --cache-dir=/dev/null`, `PYTHONDONTWRITEBYTECODE=1`) and removed child-process `src/__pycache__` | Clean `git status --ignored --short` | `608` tests in `infra/tests` passed (`4` skipped, `0` failed) | Reconciled and conformant |

## Implementation-Time Plan and Detail Update Assessment

| Affected area or marker | What changed and why | Triggering evidence and user decision | Reconciliation performed | Planning and critique state | Assessment |
| --- | --- | --- | --- | --- | --- |
| `P01-T01` in `.copilot-tracking/details/2026-11-15/infra-136-bicep-inventory-phase-details.md` | Replaced stale `infra/parameters/*.bicepparam` mention with actual repository paths (`infra/main.bicepparam`, `infra/main.test.bicepparam`, `infra/main.pilot.example.bicepparam`) | Direct glob of `infra/*.bicepparam` and `infra/README.md` (`## Layout`); no user decision required (immediately relevant current-state update) | Updated `P01-T01` in phase details and recorded in `changes.md` | Ready; single critique preserved without repetition per contract | Reconciled and justified |

## Critique and Material Revision Assessment

* Latest critique dispositions: All 6 findings (`PC-001`..`PC-006`) in `.copilot-tracking/reviews/plans/2026-11-15/infra-136-bicep-inventory-plan-critique.md` are recorded as `resolved` in `## Critique Disposition` on the plan and verified in the delivered code, README tables, and tests:
  * `PC-001`: `load_pipeline_operations` parses actual `pipeline.py` positional `operation` choices `("plan", "deploy", "publish", "changed-images", "verify-environment")`, and Step 5 documents how `rebuild.py` stage label `pipeline.py release` maps to `pipeline.py publish` / `az acr build`.
  * `PC-002`: `scan_bicep_tree` checks both `mcr.microsoft.com/k8se/quickstart:latest` in `infra/main.bicep` and missing `command:` overrides on `orchestrator` / `importJob` in `infra/modules/containerapps.bicep`, requiring `delivered-placeholder-workers`.
  * `PC-003`: ARM types are normalized with `.lower()`, sibling module callers across `infra/*.bicep` and `infra/modules/*.bicep` are verified, and exact container/queue/IoT names match Bicep source.
  * `PC-004`: Untouched historical lines in `infra/README.md` were left undisturbed; zero `.copilot-tracking/` references appear in new Python files or the `infra/README.md` diff.
  * `PC-005`: Contractor Entra B2B guest policy, M365/SharePoint `Sites.Selected` consent, GitHub protected environments/OIDC, RG + IoT budgets, and `#1258` `ranking-archive` Blob container are all retained and verified in Table 1.
  * `PC-006`: Cacheless Ruff/Mypy/Python invocations left zero `.ruff_cache` or `.mypy_cache` directories; `git status --ignored --short` is clean.
* Material revisions: None occurred during implementation.
* Dependent-work pause assessment: Not triggered; tasks executed sequentially (`P01` -> `P02` -> `P03`) after critique resolution.
* Justification assessment: Supported by direct repository evidence.

## Plan Follow-Up Assessment

| Follow-up item | Why outside immediate scope | Owner or next action | Assessment and route |
| --- | --- | --- | --- |
| Issue `#144`: Replace default placeholder worker image parameters (`mcr.microsoft.com/k8se/quickstart:latest` in `infra/main.bicep`) and wire explicit worker `command` overrides in `infra/modules/containerapps.bicep` | Runtime Container Apps worker wiring belongs to dedicated child issue `#144`; `#136` requires truthful module delivery status tracking (`delivered-placeholder-workers`) | Engineering follow-up under `#144` | Open distinct follow-up; enforced honestly by `bicep_inventory.py` |
| Issue `#147`: Obtain owner cost sign-off (`infra/defender-decision.json`) before enabling Microsoft Defender for Cloud plans (`enableDefenderPlans=true`) or switching Azure Policy from `DoNotEnforce` to `Default` | Requires explicit human budget/cost sign-off by `@jmservera` | Owner decision (`@jmservera`) under `#147` | Open distinct follow-up; preserved in `infra/README.md` and `test_governance.py` |

Unresolved plan follow-up items remain distinct follow-up work. Do not treat them as defects or add them to active `Pxx` or `Pxx-Txx` implementation, completion, or acceptance scope.

## Findings

<!-- rpi:review id=RV-001 -->
### RV-001 [Low]: Optional strict-lint registration of `bicep_inventory.py` in `.github/workflows/src-ci.yml`

* Related scope: `P03-T02`
* Evidence: `.github/workflows/src-ci.yml` runs `python -m unittest discover -s infra/tests -v` automatically on every PR (which executes `test_bicep_architecture_inventory_136.py`), while its `ruff` and `mypy --strict` lines enumerate specific `infra/scripts/*.py` files individually rather than wildcarding `infra/scripts` (because older untouched scripts in `infra/scripts/` predate the 100-column isolated lint gate). Editing `.github/workflows/src-ci.yml` was intentionally excluded from this Focused-tier slice to avoid workflow-file scope expansion.
* Impact: Non-blocking; unit and mutation tests run automatically in hosted CI via `unittest discover -s infra/tests -v`, and local Focused validation already proved `ruff check`, `ruff format --check`, and `mypy --strict` on both new files, though future edits to `bicep_inventory.py` will only receive hosted `mypy --strict` enforcement once added to `src-ci.yml`.
* Destination: follow-up
* Smallest useful next action: Append `infra/scripts/bicep_inventory.py` and `infra/tests/test_bicep_architecture_inventory_136.py` to the explicit `ruff` and `mypy --strict` file lists in `.github/workflows/src-ci.yml` during the next workflow maintenance PR.

## Defects

* None.

## Routed Findings

| Finding | Destination | Owner or next action | Reason for route |
| --- | --- | --- | --- |
| `RV-001` | `follow-up` | Optional CI workflow maintenance PR adding `bicep_inventory.py` and `test_bicep_architecture_inventory_136.py` to explicit `ruff`/`mypy --strict` lists in `.github/workflows/src-ci.yml` | Non-blocking residual hardening outside Focused-tier `infra/` scope (`unittest discover -s infra/tests` already runs the new test suite in hosted CI) |

Later implementation of a routed finding does not require another Review.

## Residual Work

* Issue `#144`: Replace placeholder quickstart worker image defaults in `infra/main.bicep` and add explicit `command` overrides for `orchestrator` and `importJob` in `infra/modules/containerapps.bicep`, then update `infra/modules/containerapps.bicep` status in `infra/README.md` from `delivered-placeholder-workers` to `delivered`.
* Issue `#147`: Record owner cost approval in `infra/defender-decision.json` before enabling Defender for Cloud pricing plans or `Default` Policy enforcement.
* `RV-001`: Add `infra/scripts/bicep_inventory.py` and `infra/tests/test_bicep_architecture_inventory_136.py` to the explicit `ruff` / `mypy --strict` commands in `.github/workflows/src-ci.yml` when workflow edits are next batched.

## Blockers and Remaining Work

* Blockers: None for the engineering scope of `#136` (note: Epic `#136` human/live gates such as `#440` stabilization checkpoint and live Azure apply sign-off remain owner-gated outside offline repository proof).
* Remaining active work: Complete local git commit (`AC-5`) on `feat/infra-136-bicep-inventory` with privacy-safe noreply email and Copilot trailer without pushing.

## Validation Evidence

| Command | Scope | Status | Summary |
| --- | --- | --- | --- |
| `python3 -m ruff check --no-cache` (default and `--isolated --select E,F,I,B,UP --target-version py312 --line-length 100`) | `infra/scripts/bicep_inventory.py`, `infra/tests/test_bicep_architecture_inventory_136.py` | Passed | `All checks passed!` (unscoped `ruff check infra/scripts infra/tests` hits pre-existing legacy style items in untouched `infra/scripts/*.py` files that `src-ci.yml` intentionally scopes around) |
| `python3 -m ruff format --no-cache --isolated --line-length 100 --check` | `infra/scripts/bicep_inventory.py`, `infra/tests/test_bicep_architecture_inventory_136.py` | Passed | `2 files already formatted` |
| `python3 -m mypy --strict --no-incremental --cache-dir=/dev/null` | `infra/scripts/bicep_inventory.py`, `infra/tests/test_bicep_architecture_inventory_136.py` | Passed | `Success: no issues found in 2 source files` |
| `python3 infra/scripts/bicep_inventory.py --check` | Repository Bicep templates, ADRs 0001-0003, `deploy.py`, `pipeline.py`, `rebuild.py`, `infra/README.md` | Passed | `Issue #136 Bicep inventory verified: 29 architecture rows, 20 Bicep modules, 12 from-empty steps (17 rebuild stages).` |
| `python3 -m unittest discover -s infra/tests -p "test_*.py" -q` | Full `infra/tests` suite | Passed | `Ran 608 tests in 285.023s — OK (skipped=4)` |
| `git status --ignored --short` and `.copilot-tracking/` diff scan | Worktree and modified files | Passed | Zero cache artifacts; zero `.copilot-tracking/` leaks in Python files or `infra/README.md` diff |

## Outcome

* Outcome: Conformant
* Outcome rationale: All planned phases and tasks (`P01-T01`, `P02-T01`, `P03-T01`, `P03-T02`) completed with verified Focused-tier evidence, all 6 plan-critique findings (`PC-001`..`PC-006`) are honored in code, documentation, and tests, and all three engineering acceptance criteria of Epic `#136` are machine-verified offline with fail-closed drift tests and zero defects.

## Closeout Routing Record

| Finding class | Destination | Owner or next action |
| --- | --- | --- |
| Implementation defect | none | None |
| Decision gap or invalid assumption | none | None |
| Material evidence gap | none | None |
| Non-blocking residual work | distinct follow-up (`#144`, `#147`, `RV-001`) | Track `#144` worker runtime defaults, `#147` owner Defender cost decision, and `RV-001` explicit `src-ci.yml` lint-list registration as separate follow-up items |

* Execution status: Complete
* Outcome: Conformant
* Validation coverage: Focused tier passed (`ruff check`, `ruff format --check`, `mypy --strict`, `bicep_inventory.py --check`, `608` `infra/tests` unit tests)
* Blockers: None

<!-- markdownlint-disable-file -->
# Review: Issue #119 Network Posture, Private Endpoints and Secret Store

## Scope and Evidence

* Task ID: issue-119-network-posture-2026-11-15
* Review date: 2026-11-15
* Review scope: Full task (`P01`, `P02`, `P03`)
* Assessed boundary: FR-01 through FR-03, NFR-01 through NFR-02, AC-01 through AC-04, critique findings `PC-001` through `PC-004`, Focused validation boundary (excluding `tools/rpi-checks.py` per caller instructions), and tracker attribution (`Refs #119, #143, #142`).
* Plan: .copilot-tracking/plans/2026-11-15/infra-119-network-posture-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/infra-119-network-posture-phase-details.md
* Plan critique: .copilot-tracking/reviews/2026-11-15/infra-119-network-posture-plan-critique.md
* Changes: .copilot-tracking/changes/2026-11-15/infra-119-network-posture-changes.md
* Other evidence considered: .copilot-tracking/research/2026-11-15/infra-119-network-posture-research.md, `infra/network-posture-inventory.json`, `docs/architecture/network-posture.md`, `docs/architecture/README.md`, `infra/README.md`, and `infra/tests/test_network_posture.py`.

## Opening Review State

* Interpreted review goal: Verify once, from committed/working-tree artifacts and Focused validation evidence, that every Bicep data store is backed by a verified `snet-pe` private endpoint (or AMPLS scope / `existing` reference) or an owned exercise exception, that all secrets are read from Key Vault via user-assigned managed identity with zero literal secrets in Bicep/bicepparam/runtime code, and that `docs/architecture/network-posture.md` matches Bicep 1:1.
* Review scope: Full task (`P01`, `P02`, `P03`)
* Evidence readiness: Plan, phase details, plan critique (`PC-001`..`PC-004` disposed), changes record (`Complete`), and all 5 delivered workspace files are present and reconciled.
* Acceptance basis: `AC-01`, `AC-02`, `AC-03`, `AC-04`, critique dispositions `PC-001`..`PC-004`, AMA Markdown style rules, and Focused validation commands.
* First comparison boundary: Reconcile plan markers (`P01`, `P01-T01`, `P02`, `P02-T01`, `P02-T02`, `P03`, `P03-T01`, `P03-T02`), critique resolutions, and implementation-time updates against `infra/network-posture-inventory.json`, `docs/architecture/network-posture.md`, `docs/architecture/README.md`, `infra/README.md`, and `infra/tests/test_network_posture.py`.
* Active read-only boundaries: This stage writes only `.copilot-tracking/reviews/logs/2026-11-15/infra-119-network-posture-review.md` (plus parent RPI state transitions).
* Initial blockers: None

## Execution Status

* Execution status: Complete
* Review execution evidence: Completed one-pass review on 2026-11-15 across the full declared plan (`P01`, `P02`, `P03`), reconciling `.copilot-tracking/plans/2026-11-15/infra-119-network-posture-plan.md`, `.copilot-tracking/details/2026-11-15/infra-119-network-posture-phase-details.md`, `.copilot-tracking/reviews/2026-11-15/infra-119-network-posture-plan-critique.md`, `.copilot-tracking/changes/2026-11-15/infra-119-network-posture-changes.md`, and `.copilot-tracking/research/2026-11-15/infra-119-network-posture-research.md` against `infra/network-posture-inventory.json`, `docs/architecture/network-posture.md`, `docs/architecture/README.md`, `infra/README.md`, and `infra/tests/test_network_posture.py`.

## Plan-to-Change Reconciliation

| Current plan scope | Descriptive changes-record summary | Current-state reconciliation | Gap or rationale |
|---|---|---|---|
| `P01` / `P01-T01` | `### P01-T01: Author infra/network-posture-inventory.json` | Reconciled | `infra/network-posture-inventory.json` covers VNet (`10.40.0.0/16`), 3 core + 1 standalone subnets, 2 NSGs, 15 private DNS zones and VNet links, 10 private-endpoint data stores + AMPLS `scopedResources`, conditional Front Door `sharedPrivateLinkOrigins`, 8 `existingStoreReferences`, 7 owned exercise exceptions (`NP-EX-001`..`NP-EX-007`), and 4 managed-identity Key Vault `secretBindings`. |
| `P02` / `P02-T01` | `### P02-T01: Author docs/architecture/network-posture.md` | Reconciled | `docs/architecture/network-posture.md` provides a canonical Mermaid `flowchart TB` and structured Markdown tables matching Bicep 1:1, obeying AMA Markdown style rules (YAML frontmatter `title` without H1, `*` unordered lists, ASCII punctuation, zero em dashes, zero bolded-prefix list items, and verified relative links). |
| `P02` / `P02-T02` | `### P02-T02: Cross-link docs/architecture/README.md and infra/README.md` | Reconciled | `docs/architecture/README.md` cross-links `./network-posture.md` and `../../infra/network-posture-inventory.json` and clarifies `snet-aca`, `snet-pe`, conditional `snet-aca-demo`, and `allowPublicNetworkAccess = false` defaults without touching `.excalidraw` artifacts; `infra/README.md` adds a single `## Layout` bullet while preserving `#136` tables intact. |
| `P03` / `P03-T01` | `### P03-T01: Implement infra/tests/test_network_posture.py (AC1, AC2, AC3 + negative mutation tests)` | Reconciled | `infra/tests/test_network_posture.py` compiles Bicep templates and all 4 committed `.bicepparam` files offline and enforces `AC-01`, `AC-02`, and `AC-03` plus 3 fail-closed negative mutation tests (`6` tests total, all passing). |
| `P03` / `P03-T02` | `### P03-T02: Run Focused validation suite and architecture/inventory regression checks` | Reconciled | Focused validation ran across all `637` tests in `infra/tests`, `ruff check --isolated`, `ruff format --isolated --line-length 100 --check`, `mypy`, `bicep_inventory.py --check`, and `git diff --check`, while intentionally omitting `tools/rpi-checks.py` per caller instructions. |
| `## Follow-Up Items` | Live Front Door Shared Private Link approval (`#143`), legacy `infra/tests` formatting hygiene, and pre-existing `.excalidraw` check mismatch | Reconciled | Explicitly outside offline Focused scope; preserved in plan `## Follow-Up Items` and changes record `## Follow-Up Work` without inflating active `Pxx` claims. |

## Completed Work Assessment

| Related marker | Files | What changed and why | Completion evidence | Validation | Assessment |
|---|---|---|---|---|---|
| `P01`, `P01-T01` | `infra/network-posture-inventory.json` | Added machine-readable network-posture, private-endpoint, exercise-exception, and Key Vault managed-identity secret-binding inventory contract (`schemaVersion: "1.0"`). | Verified JSON schema and compiled ARM cross-check against `infra/main.bicep`, `infra/modules/*.bicep`, `infra/private-proof-publisher.bicep`, `infra/bicep-architecture-inventory.json`, `infra/secret-inventory.json`, and `infra/policy-exceptions.json`. | `python3 -m unittest infra/tests/test_network_posture.py -v` (`OK`) | Reconciled |
| `P02`, `P02-T01` | `docs/architecture/network-posture.md` | Created canonical network-posture architecture specification with Mermaid `flowchart TB` and structured tables for subnets/NSGs, 15 private DNS zones/VNet links, data-store private endpoints, Key Vault MI secret bindings, and exercise exceptions (`NP-EX-001`..`NP-EX-007`). | Bidirectional Bicep-to-Markdown table/Mermaid assertions and Markdown style/relative-link verification. | `test_ac3_network_diagram_matches_bicep_modules` + `test_negative_network_diagram_drift_fails_closed` (`OK`) | Reconciled |
| `P02-T02` | `docs/architecture/README.md`, `infra/README.md` | Linked `network-posture.md` and `infra/network-posture-inventory.json`, clarified conditional `snet-aca-demo` and `allowPublicNetworkAccess = false` defaults, and added `## Layout` reference in `infra/README.md`. | `git diff` inspection, relative link check, and `infra/tests/test_bicep_policy.py` regression suite ensuring `#136` `infra/README.md` tables remain intact. | `python3 infra/scripts/bicep_inventory.py --check` + `infra/tests` (`637` tests `OK`) | Reconciled |
| `P03`, `P03-T01`, `P03-T02` | `infra/tests/test_network_posture.py` | Implemented 6 deterministic `unittest` checks (3 positive AC proofs + 3 negative fail-closed mutation tests) and ran Focused suite + isolated `ruff` and `mypy` checks. | Direct execution of `test_network_posture.py` (`6` tests `OK`) and full `infra/tests` discovery (`637` tests `OK, skipped=4`). | `unittest`, `ruff check --isolated --select E,F,I,B,UP --target-version py312 --line-length 100`, `ruff format --isolated --line-length 100 --check`, `mypy --follow-imports=silent --ignore-missing-imports` (`Passed`) | Reconciled |

## Implementation-Time Plan and Detail Update Assessment

| Affected area or marker | What changed and why | Triggering evidence and user decision | Reconciliation performed | Planning and critique state | Assessment |
|---|---|---|---|---|---|
| `P01-T01`, `P03-T01` (compiled nested deployment names + nested ARM `createObject(...)` parsing) | Aligned `mainModuleName` in `infra/network-posture-inventory.json` to compiled `Microsoft.Resources/deployments` resource names (e.g., `"auth-token-store"`, `"kv"`, `"storage"`, `"acr"`, `"sql"`, `"foundry"`, `"iothub"`, `"monitoring"`) and replaced flat regex extraction with parenthesis-depth parsing for `ca-${prefix}-api` `createObject('name', ..., 'keyVaultUrl', ..., 'identity', ...)` secrets. | Compiled `infra/main.bicep` ARM output during `P03-T01` verification; local implementation judgment requiring no user decision. | Recorded in `.copilot-tracking/changes/2026-11-15/infra-119-network-posture-changes.md` under `## Plan and Detail Updates`. | Preserves `PC-001`..`PC-004` intent; no material plan revision or repeat critique needed. | Reconciled |
| `P03-T01` (`private-proof-publisher.bicep` variable resolution and migrated `src/` module paths) | Added ARM `variables` resolution for standalone `Microsoft.Network/virtualNetworks` subnet extraction (`variables('stem')`) and aligned runtime secret-free audit targets to exact migrated `src/` module paths (`src/orchestrator/.../token_store.py`, `src/core/.../mssqlstore.py`, `src/agents/.../heldout_aoai.py`, `src/api/.../iot_stream.py`, `src/api/.../resident_demo/aoai.py`) while distinguishing Python f-string `PWD={` interpolation from hardcoded credentials. | Direct source inspection during `P03-T01`; local implementation judgment requiring no user decision. | Recorded in `.copilot-tracking/changes/2026-11-15/infra-119-network-posture-changes.md` under `## Plan and Detail Updates`. | Preserves `AC-02` and `PC-004` intent; no material plan revision needed. | Reconciled |

## Critique and Material Revision Assessment

* Latest critique dispositions: All four one-pass critique findings (`PC-001` complete 30-template Bicep store discovery including `existing` stores and AMPLS `scopedResources`, `PC-002` bidirectional diagram/table drift enforcement across all 15 private DNS zones and VNet links, `PC-003` compiled `.bicepparam` literal-secret inspection plus EasyAuth `keyVaultUrl` + `identity` verification, and `PC-004` fail-closed negative mutation tests) were applied directly in planning before implementation started and verified by `infra/tests/test_network_posture.py`.
* Material revisions: Zero material revisions or scope divergences occurred during implementation.
* Dependent-work pause assessment: No pause was needed; `P01` -> `P02` -> `P03` executed strictly in dependency order.
* Justification assessment: All local implementation refinements strengthen mechanical accuracy against compiled ARM output and migrated `src/` paths.

## Plan Follow-Up Assessment

| Follow-up item | Why outside immediate scope | Owner or next action | Assessment and route |
|---|---|---|---|
| Live Azure Front Door Premium Shared Private Link approval and VNet private DNS smoke proof (`#143`) | Requires live Azure subscription deployment and manual Private Endpoint connection approval outside offline Focused unit testing. | Infrastructure owner during live `#143` pilot deployment window. | Open distinct follow-up route (not a defect in this task). |
| Explicit `src-ci.yml` `ruff` coverage for `infra/tests/test_network_posture.py` and formatting cleanup of 12 pre-existing untouched `infra/tests/*.py` files | Editing `.github/workflows/src-ci.yml` or reformatting 12 unrelated legacy `infra/tests/*.py` files would widen scope across parallel demo worktrees and touch workflow gate files outside Issue #119. | Separate repository hygiene PR on `infra/tests` and `.github/workflows/src-ci.yml`. | Open distinct follow-up route (not a defect in this task). |
| Pre-existing `docs/architecture/zava-forward-executive-architecture.excalidraw` hash mismatch in `update-architecture.mjs --check` | Pre-existing on base branch `feat/demo-164-chat-grounding-provenance-0900`; `.excalidraw` files were explicitly excluded from this slice's write boundary. | Architecture diagram owner (`docs/architecture/update-architecture.mjs`). | Open distinct follow-up route (not a defect in this task). |

Unresolved plan follow-up items remain distinct follow-up work. Do not treat them as defects or add them to active `Pxx` or `Pxx-Txx` implementation, completion, or acceptance scope.

## Findings

No material defects, decision gaps, or evidence gaps were identified across `P01`, `P02`, or `P03`.

## Defects

* None

## Routed Findings

| Finding | Destination | Owner or next action | Reason for route |
|---|---|---|---|
| None | None | No routed defect, plan revision, or research gap | Full declared scope (`P01`–`P03`) is conformant with `AC-01`..`AC-04` and `PC-001`..`PC-004` |

Later implementation of a routed finding does not require another Review.

## Residual Work

* Live Azure Front Door Premium Shared Private Link approval and VNet private DNS smoke proof (`#143`) — distinct live-environment follow-up outside offline Bicep/documentation verification.
* Add `infra/tests/test_network_posture.py` to `.github/workflows/src-ci.yml`'s explicit `ruff` file list and format the 12 pre-existing untouched `infra/tests/*.py` files in an isolated hygiene PR so directory-wide `python3 -m ruff format --isolated --line-length 100 --check infra/tests` also exits `0`.
* Reconcile the pre-existing `docs/architecture/zava-forward-executive-architecture.excalidraw` hash in `node docs/architecture/update-architecture.mjs` on its owning architecture branch.

## Blockers and Remaining Work

* Blockers: None for the completed offline Focused slice (note: human/coordinator review of the frozen local commit remains an external workflow gate before any push or PR merge).
* Remaining active work: None (`P01`, `P01-T01`, `P02`, `P02-T01`, `P02-T02`, `P03`, `P03-T01`, and `P03-T02` are all complete).

## Validation Evidence

| Command | Scope | Status | Summary |
|---|---|---|---|
| `python3 -m unittest infra/tests/test_network_posture.py -v` | `infra/tests/test_network_posture.py` (`AC-01`, `AC-02`, `AC-03` + 3 negative mutation tests) | Passed | `Ran 6 tests in 20.452s — OK` |
| `PYTHONPATH=src/core/src:src/agents/src:src/api/src python3 -m unittest discover -s infra/tests -p 'test_*.py' -q` | Full `infra/tests` unit suite | Passed | `Ran 637 tests in 231.124s — OK (skipped=4)` |
| `python3 -m ruff check --isolated --select E,F,I,B,UP --target-version py312 --line-length 100 infra/tests/test_network_posture.py` | Modified `infra/` Python file matching `.github/workflows/src-ci.yml` | Passed | `All checks passed!` (`0` findings) |
| `python3 -m ruff format --isolated --line-length 100 --check infra/tests/test_network_posture.py` | Modified `infra/` Python file matching `.github/copilot-instructions.md` and `src-ci.yml` | Passed | `1 file already formatted` |
| `python3 -m ruff format --isolated --line-length 100 --check infra/tests` | Whole `infra/tests` directory including 34 untouched base-branch files | Skipped / Pre-existing base state noted | `test_network_posture.py` + 22 existing files formatted; 12 untouched pre-existing legacy `infra/tests/*.py` files on base branch left unformatted to avoid out-of-scope churn across parallel demo worktrees |
| `python3 -m mypy --follow-imports=silent --ignore-missing-imports infra/tests/test_network_posture.py` | Static typing on `infra/tests/test_network_posture.py` | Passed | `Success: no issues found in 1 source file` |
| `python3 infra/scripts/bicep_inventory.py --check` | `infra/bicep-architecture-inventory.json` and 20-module matrix regression | Passed | `OK: 29 architecture rows, 20 Bicep modules, 12 from-empty steps` |
| `git --no-pager diff --check` | Whitespace and conflict-marker check across working tree | Passed | Clean (`0` issues) |
| `python3 tools/rpi-checks.py` | Full repository gate | Skipped | Explicitly prohibited by caller instructions (`Validation tier: Focused ... Do NOT run tools/rpi-checks.py`) |

## Outcome

* Outcome: Conformant
* Outcome rationale: Every requirement (`FR-01`..`FR-03`, `NFR-01`..`NFR-02`), acceptance criterion (`AC-01`..`AC-04`), and one-pass critique disposition (`PC-001`..`PC-004`) is proven by committed/working-tree artifacts (`infra/network-posture-inventory.json`, `docs/architecture/network-posture.md`, `docs/architecture/README.md`, `infra/README.md`, `infra/tests/test_network_posture.py`) and passing Focused validation (`637` tests `OK`), with zero open defects or unaccepted divergences.

## Closeout Routing Record

<!-- Persist outcome and route facts only. The rpi-review reference owns rendered closeout prose. -->

| Finding class | Destination | Owner or next action |
|---|---|---|
| Implementation defect | None | None |
| Decision gap or invalid assumption | None | None |
| Material evidence gap | None | None |
| Non-blocking residual work | Distinct follow-up items (`#143` live Front Door Shared Private Link proof; isolated `infra/tests` + `src-ci.yml` `ruff` hygiene PR; pre-existing `.excalidraw` hash sync) | Coordinator / repository owners in separate follow-up tasks |

* Execution status: Complete
* Outcome: Conformant
* Validation coverage: Focused validation passed (`6/6` tests in `test_network_posture.py`, `637/637` tests in `infra/tests`, `ruff check --isolated`, `ruff format --isolated --line-length 100 --check` on `test_network_posture.py`, `mypy`, `bicep_inventory.py --check`, and `git diff --check`; `tools/rpi-checks.py` intentionally not run per caller directive).
* Blockers: None


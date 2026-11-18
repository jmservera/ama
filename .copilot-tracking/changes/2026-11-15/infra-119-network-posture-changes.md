<!-- markdownlint-disable-file -->
# RPI Changes: Issue #119 Network Posture, Private Endpoints and Secret Store

## Metadata

* Task ID: issue-119-network-posture-2026-11-15
* Related plan: .copilot-tracking/plans/2026-11-15/infra-119-network-posture-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/infra-119-network-posture-phase-details.md
* Implementation date: 2026-11-15

## Execution Status

* Status: Complete
* Declared invocation scope: full plan (`P01`, `P02`, `P03`)
* Completed scope markers: P01, P01-T01, P02, P02-T01, P02-T02, P03, P03-T01, P03-T02
* All remaining active-plan markers: none
* Status basis: Completed `P01`, `P02`, and `P03` with passing Focused validation across all 637 `infra/tests` unit tests, `ruff check`, `ruff format --check`, `mypy`, `bicep_inventory.py --check`, and `git diff --check`.

## Execution Summary

Implemented the deterministic network-posture, private-endpoint, exercise-exception, and managed-identity Key Vault secret contract (`infra/network-posture-inventory.json`), authored the canonical Mermaid topology diagram and reference specification (`docs/architecture/network-posture.md` + cross-links in `docs/architecture/README.md` and `infra/README.md`), and delivered `infra/tests/test_network_posture.py` proving AC-01, AC-02, and AC-03 with positive and fail-closed mutation tests.

## Completed Work

### P01: Deterministic network-posture and secret-binding inventory (`P01`, `P01-T01`)

* Added `infra/network-posture-inventory.json` defining the canonical JSON schema (`schemaVersion: "1.0"`) for VNet (`vnet-${prefix}`, `10.40.0.0/16`), subnets (`snet-aca`, `snet-pe`, conditional `snet-aca-demo`, plus standalone `issue360-publisher-20261019-subnet`), 15 private DNS zones and `link-${prefix}` VNet links, 10 private-endpoint data stores (`mainModuleName` matching exact `main.bicep` nested deployment names, plus AMPLS `scopedResources`), optional Front Door `sharedPrivateLinkOrigins`, 8 `existingStoreReferences`, 7 exercise exceptions (`NP-EX-001`..`NP-EX-007`) with owner and rationale, and 4 managed-identity Key Vault `secretBindings`.

### P02: Architecture network-posture diagram and infrastructure docs (`P02`, `P02-T01`, `P02-T02`)

* Added `docs/architecture/network-posture.md` (`P02-T01`) with YAML frontmatter, Mermaid `flowchart TB` covering every subnet, NSG, private DNS zone, VNet link, private endpoint, optional Front Door `sharedPrivateLinkResource`, and outside-core exercise exceptions, plus structured tables for subnets/NSGs, private DNS zones/VNet links, data-store private endpoints, managed-identity Key Vault secret bindings, and exercise exceptions.
* Updated `docs/architecture/README.md` (`P02-T02`) to link `docs/architecture/network-posture.md` and `infra/network-posture-inventory.json` and refine the subnet/public-access bullet (`snet-aca`, `snet-pe`, conditional `snet-aca-demo`, and `allowPublicNetworkAccess = false` default).
* Updated `infra/README.md` (`P02-T02`) `## Layout` list to register `network-posture-inventory.json` and `tests/test_network_posture.py` without altering the `#136` Markdown tables.

### P03: Offline network-posture, secret-store, and diagram-parity test suite and Focused validation (`P03`, `P03-T01`, `P03-T02`)

* Added `infra/tests/test_network_posture.py` (`P03-T01`) with 6 test methods (`test_ac1_every_data_store_has_private_endpoint_or_owned_exception`, `test_ac2_secrets_read_from_key_vault_via_managed_identity_zero_literal_secrets`, `test_ac3_network_diagram_matches_bicep_modules`, and 3 fail-closed negative mutation tests `test_negative_unprotected_data_store_or_ownerless_exception_fails_closed`, `test_negative_literal_secret_in_container_app_or_env_fails_closed`, `test_negative_network_diagram_drift_fails_closed`).
* Executed Focused validation (`P03-T02`) without invoking `tools/rpi-checks.py`: all 6 tests in `test_network_posture.py` and all 637 tests in `infra/tests` passed (`OK (skipped=4)`), alongside `ruff check`, `ruff format --check`, `mypy`, `bicep_inventory.py --check`, and `git diff --check`.

## Implementation-Time Plan and Detail Updates

* Current-state update (`P03-T02` in `.copilot-tracking/plans/2026-11-15/infra-119-network-posture-plan.md` and `.copilot-tracking/details/2026-11-15/infra-119-network-posture-phase-details.md`):
  * Recorded that `PYTHONPATH=src/core/src:src/agents/src:src/api/src` is required when `src/` distributions are not editable-installed in the host Python so `test_pipeline.SmokeTests.test_installed_local_api_denies_unauthenticated_requests` can execute `python3 -m zava_forward.api` (`637/637` tests `OK`).
  * Recorded that `python3 -m ruff format --isolated --line-length 100 --check infra/tests/test_network_posture.py` exits `0` (`1 file already formatted`, matching `.github/copilot-instructions.md` and `.github/workflows/src-ci.yml`), whereas directory-wide `ruff format --check infra/tests` reports 12 pre-existing untouched `infra/tests/*.py` files on the base branch (`23 files already formatted`) which were deliberately left unmodified to preserve surgical diff boundaries.
  * Recorded that `node docs/architecture/update-architecture.mjs --check` had a pre-existing base-branch hash mismatch on `zava-forward-executive-architecture.excalidraw`; `.excalidraw` artifacts were kept untouched per the locked plan boundary.

## Validation Record

| Check | Scope | Status | Evidence or reason |
|---|---|---|---|
| `python3 -m unittest infra/tests/test_network_posture.py -v` | `test_network_posture.py` (6 tests: AC-01, AC-02, AC-03 + 3 negative mutations) | Passed | Exit `0`, `Ran 6 tests in 27.848s - OK` |
| `PYTHONPATH=src/core/src:src/agents/src:src/api/src python3 -m unittest discover -s infra/tests -p 'test_*.py' -q` | Full `infra/tests` suite (637 tests) | Passed | Exit `0`, `Ran 637 tests in 231.124s - OK (skipped=4)` |
| `python3 -m ruff check --isolated --select E,F,I,B,UP --target-version py312 --line-length 100 infra/tests/test_network_posture.py` | Modified `infra/` Python file lint | Passed | Exit `0`, `All checks passed!` |
| `python3 -m ruff format --isolated --line-length 100 --check infra/tests/test_network_posture.py` | Modified `infra/` Python file format check | Passed | Exit `0`, `1 file already formatted` (directory-wide `ruff format --check infra/tests` flags 12 untouched pre-existing files on base branch) |
| `python3 -m mypy infra/tests/test_network_posture.py` | Static type check | Passed | Exit `0`, `Success: no issues found in 1 source file` |
| `python3 infra/scripts/bicep_inventory.py --check` | `#136` architecture inventory & `infra/README.md` table regression check | Passed | Exit `0`, `29 architecture rows, 20 Bicep modules, 12 from-empty steps (17 rebuild stages)` |
| `git --no-pager diff --check` | Whitespace and Markdown/JSON/Python diff hygiene | Passed | Exit `0`, zero warnings |
| `tools/rpi-checks.py` | Full local gate | Skipped | Explicitly prohibited by caller instructions (`Validation tier: Focused ... Do NOT run tools/rpi-checks.py`) |

## Pre-Review Reconciliation

* Plan markers and phase details: Reconciled (`P01`, `P01-T01`, `P02`, `P02-T01`, `P02-T02`, `P03`, `P03-T01`, `P03-T02` all checked `[x]`; `P03-T02` current-state notes aligned)
* Completed-work evidence and handoff prose: Reconciled across plan, phase details, and changes log
* Validation, blockers, remaining work, and follow-up items: All Focused validation checks passed; zero blockers; zero remaining in-scope work
* Review readiness: Ready for one-pass `rpi-review`

## Blockers

* None

## Remaining Work

* None (`P01` through `P03` complete).

## Follow-Up Items

* Canonical plan list: .copilot-tracking/plans/2026-11-15/infra-119-network-posture-plan.md, `## Follow-Up Items`
* Live Azure Front Door Premium Shared Private Link approval and VNet private DNS resolution smoke test: outside offline Bicep/documentation scope; tracked under `#143` / `#118` for owner-approved Azure deployment window.

## Return-to-Caller State

* Implementation execution status: Complete
* Declared scope and markers: Full plan; completed: P01, P01-T01, P02, P02-T01, P02-T02, P03, P03-T01, P03-T02; remaining: none
* Validation coverage: Focused tier complete (`637` `infra/tests` unit tests, `ruff check`, `ruff format --check` on `test_network_posture.py`, `mypy`, `bicep_inventory.py --check`, `git diff --check`; `tools/rpi-checks.py` skipped per caller instruction)
* Blockers: None
* Current plan and detail updates: `P03-T02` current-state validation notes recorded
* Planning and critique state: Ready (`PC-001`..`PC-004` resolved)
* Follow-up items: Live Azure Front Door Shared Private Link & VNet DNS smoke test (`#143` / `#118`)
* Review readiness or no-handoff reason: Ready for `rpi-review`
* Continuation owner: Confirmed automatic RPI Agent parent -> automatic transition to `Review` (`rpi-review`)

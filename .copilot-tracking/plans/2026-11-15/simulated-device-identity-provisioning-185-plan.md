<!-- markdownlint-disable-file -->
# RPI Plan: Simulated Device Identity and Provisioning (#185)

## Task Metadata

* Task ID: issue-185-simulated-device-identity-provisioning
* Task slug: simulated-device-identity-provisioning-185
* Planning status: ready
* Plan date: 2026-11-15
* Phase details: .copilot-tracking/details/2026-11-15/simulated-device-identity-provisioning-185-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-11-15/simulated-device-identity-provisioning-185-plan-critique.md

## Executive Summary

This plan delivers the remaining simulated device identity and provisioning contracts for issue #185 in `zava_forward.core.synthetic`. It introduces `src/core/src/zava_forward/core/synthetic/live_provisioning.py` for the `SIM-*` simulated device lifecycle and additively aligns `device_identity.py`, `device_provision.py`, and `src/core/README.md` so that every provisioning plan, manifest, report, audit record, logger emission, and teardown receipt records the decided identity approach (**per-device symmetric SAS / DPS enrollment group**) and credential owner role (**Platform Engineering / IoT Operations Owner**), keeps issued symmetric credentials isolated inside an in-memory vault behind opaque references with zero secrets in source or logs, and proves deterministic `SIM-*` teardown with a verifiable zero-residual receipt.

### User Decisions and Requirements Highlights

* **Explicit approach and credential owner recording**: Provisioning plans and manifests record `per-device symmetric SAS / DPS enrollment group` and `Platform Engineering / IoT Operations Owner`, closing the approach and ownership governance criterion of issue #185.
* **Vault-isolated issuance and multi-layer secret redaction**: Runtime per-device symmetric SAS credentials are derived from ephemeral CSPRNG bytes inside a vault boundary and never written to source; summaries, audit records, exceptions, and `logging` records redact symmetric keys, connection strings, and SAS tokens.
* **Deterministic `SIM-*` teardown and zero-residual receipt**: `teardown_simulated_identities` and its alias `deprovision_simulated_devices` remove every targeted `SIM-*` simulated identity, preserve non-simulated registry entries, verify zero residual simulated identities and credentials, and return a signed SHA-256 `TeardownReceipt`.
* **Focused validation boundary**: Validation runs targeted and package `unittest`, `mypy`, `ruff check`, and `ruff format --isolated --line-length 100 --check` in `src/core` without invoking `tools/rpi-checks.py`, pushing, or opening a pull request.

### What You May Not Know

* Earlier partial slices (PR #1205 and PR #1393) added `device_identity.py`, `device_provision.py`, and `device_registry_azure.py` with `SYN-*` device IDs, a CLI `--owner="unassigned"` refusal test (`test_device_provision.py`), and a strict `self.assertNoLogs(level=logging.DEBUG)` guard around `device_identity.provision` (`test_device_identity.py`). Keeping `SYN-*`, CLI `--owner="unassigned"`, and `device_identity.provision` log silence intact while implementing the `SIM-*` lifecycle and redacted structured logging in `live_provisioning.py` prevents regressions across 40+ existing tests.
* Full `src/core` unittest discovery imports `test_device_registry_azure.py`, which requires the pinned dev packages `azure-iot-hub==2.7.0` and `six==1.17.0` declared in `src/core/pyproject.toml`. Validation probes ambient `python3` first and falls back to a workspace-relative gitignored `src/core/.venv` (`pip install -e "src/core[dev]"`) if `azure.iot.hub` is missing, verifying `git status --short` contains zero untracked environment artifacts before committing.

### Unresolved Decisions or Blockers

* None. All requirements, target contracts, and validation boundaries are settled by caller direction and codebase evidence.

For current user input, see [User Decisions and Requirements](#user-decisions-and-requirements). The planner keeps the synthesized sections below current as evidence and user direction evolve.

## User Decisions and Requirements

* Run the full RPI loop in order (`research`, `plan`, `implement`, `review`) with dated artifacts under `.copilot-tracking/` (`2026-11-15`) for issue #185 on branch `feat/iot-185-device-provisioning` in `/home/azureuser/source/ama-demo-wt/feat-185-device-provisioning` (caller prompt).
* Record the decided device identity approach (`per-device symmetric SAS / DPS enrollment group`) and the named `credential_owner` role (`Platform Engineering / IoT Operations Owner`) explicitly in the provisioning manifest/plan in `src/core/src/zava_forward/core/synthetic/live_provisioning.py` and aligned synthetic provisioning modules (caller prompt Criterion 1; `ADR 0003` decision 6).
* Issue and store simulated device credentials without any raw symmetric key, connection string, or SAS token appearing in source code, returned summaries, audit records, exceptions, or logger calls (caller prompt Criterion 2; `PRD FR-050`, `AC-066`, `AC-067`).
* Provide deterministic teardown (`teardown_simulated_identities` / `deprovision_simulated_devices`) that removes every registered simulated `SIM-*` device identity and returns a verifiable teardown receipt confirming zero residual simulated identities (caller prompt Criterion 3).
* Preserve the already-delivered 1:1 mapping from each simulated consenting stock home to one device identity and one stock home ID (issue #185 criterion 2; `test_device_identity.py`, `test_device_provision.py`).
* Use the Focused validation tier in `src/core` (`unittest`, `mypy`, `ruff check`, `ruff format --isolated --line-length 100 --check`), do not run `tools/rpi-checks.py`, and commit all code and `.copilot-tracking/` artifacts locally on `feat/iot-185-device-provisioning` with the Copilot trailer without pushing or creating a PR (caller prompt).

## Goals

* Deliver a complete, strictly typed `zava_forward.core.synthetic.live_provisioning` module implementing `SIM-*` simulated device identity planning, ephemeral symmetric SAS / DPS enrollment-group credential issuance, secret-redacted logging and audit trails, and deterministic zero-residual teardown receipts.
* Additively align `device_identity.py`, `device_provision.py`, and `src/core/README.md` with the recorded approach, credential owner role constant, secret-bearing owner refusal, and `TeardownReceipt` contract while preserving 100% compatibility with existing `SYN-*` and X.509 registry tests.
* Prove all three remaining issue #185 acceptance criteria with focused unit tests and pass `src/core` `unittest`, strict `mypy`, `ruff check`, and `ruff format --check`.

## Scope and Non-Goals

### In Scope

* Creating `src/core/src/zava_forward/core/synthetic/live_provisioning.py` (canonical source target; no generated artifacts).
* Additive updates to `src/core/src/zava_forward/core/synthetic/device_identity.py` and `src/core/src/zava_forward/core/synthetic/device_provision.py`.
* Creating `src/core/tests/test_live_provisioning.py` and adding focused assertions in `src/core/tests/test_device_identity.py` and `src/core/tests/test_device_provision.py` (exact test removals: `none`; maximum test additions: `18` test methods total across the three files).
* Updating `#185` module documentation in `src/core/README.md`.
* Running `src/core` unit tests, `mypy`, `ruff check`, and `ruff format --isolated --line-length 100 --check`, then committing code and `.copilot-tracking/` artifacts locally.

### Non-Goals

* Live Azure IoT Hub or Azure Device Provisioning Service network mutations or cloud resource changes.
* Modifying `device_registry_azure.py`, `src/api/`, `infra/`, or web UI files.
* Running `tools/rpi-checks.py`, pushing to `origin`, or opening/updating a GitHub pull request.

## Functional Requirements

* **FR-1 (Approach & Credential Owner Recording)**: `live_provisioning.ProvisioningManifest` (and alias `ProvisioningPlan`), `plan_simulated_provisioning`, `device_identity.Manifest`, and `device_provision.report` shall record `approach = "per-device symmetric SAS / DPS enrollment group"` (plus `identity_approach` in serialized dicts) and default/canonical `credential_owner = "Platform Engineering / IoT Operations Owner"` alongside an explicit non-secret `rotation_policy`, rejecting blank, placeholder, personal-data, or secret-bearing `credential_owner` strings.
  * Observable acceptance criteria: Unit tests verify `manifest.approach == "per-device symmetric SAS / DPS enrollment group"`, `manifest.credential_owner == "Platform Engineering / IoT Operations Owner"`, serialized report/manifest dicts expose both fields and pass `privacy.emission_issues`, and invalid owners fail closed with fixed error codes.
* **FR-2 (Vault-Isolated Issuance & Multi-Layer Secret Redaction)**: `SymmetricSasCredentialStore` shall generate ephemeral runtime enrollment-group key bytes in memory (`secrets.token_bytes(32)`), derive per-device symmetric keys via HMAC-SHA256 inside private non-`repr` storage, return only immutable opaque `secretref://dps-sas/...` references, and `redact_provisioning_secrets` + `SecretRedactingFilter` shall scrub raw symmetric keys, IoT Hub/DPS connection strings, and `SharedAccessSignature` SAS tokens from manifests, provisioning summaries, audit records, exceptions, and `logging` records.
  * Observable acceptance criteria: Unit tests verify zero raw keys, connection strings, or SAS tokens appear in source files, `ProvisioningSummary.as_dict()`, `ProvisioningAuditRecord`, `repr()`, formatted tracebacks, or captured `logging` records even when caller/adapter notes or exceptions inject raw symmetric keys, connection strings, and SAS tokens.
* **FR-3 (Deterministic `SIM-*` Teardown & Zero-Residual Receipt)**: `teardown_simulated_identities` and its alias `deprovision_simulated_devices` (in `live_provisioning.py` and re-exported in `device_provision.py`) shall deterministically delete every targeted simulated `SIM-*` identity in sorted order, revoke all associated credentials, leave non-simulated identities (`PROD-*`, `REAL-*`) untouched, verify zero residual simulated identities and credentials post-cleanup (raising a fixed-code error if any remain), and return a frozen `TeardownReceipt` with `verified_zero_residual=True`, `residual_simulated_count=0`, `residual_simulated_identities=()`, and a deterministic `verification_sha256` digest; `device_identity.teardown` and `device_provision.run(..., "teardown", True, ...)` shall also surface `TeardownReceipt`.
  * Observable acceptance criteria: Unit tests verify complete removal of single-run and multi-run `SIM-*` identities, preservation of non-simulated registry entries, fail-closed error on stubborn residual `SIM-*` devices or unrevoked credentials, and exact `TeardownReceipt` fields and SHA-256 verification digest.

## Non-Functional Requirements

* **NFR-1 (Strict Static Typing & Lint Cleanliness)**: All new and modified Python modules and test files in `src/core` shall satisfy `mypy` (`strict = true`) and `ruff` (`E`, `F`, `I`, `B`, `UP`, `line-length = 100`) without adding `pyproject.toml` ignore overrides.
  * Objective threshold or evaluation condition: Zero errors from `python3 -m mypy`, `python3 -m ruff check`, and `python3 -m ruff format --isolated --line-length 100 --check` inside `src/core`.
  * Operating condition or verification approach, if needed: Executed directly against `src/core` (`src` and `tests`).
  * Observable acceptance criteria: All three static quality commands exit `0` with zero diagnostics.
* **NFR-2 (Thread Safety & Backward Compatibility)**: Per-run operations shall remain serialized under re-entrant run locks, and existing `SYN-*` identity, X.509 registry, `assertNoLogs` (`test_device_identity.py`), CLI `--owner="unassigned"` (`test_device_provision.py`), and synthetic emission audit (`test_synthetic_output_audit.py`) tests shall continue to pass with zero test removals.
  * Objective threshold or evaluation condition: 100% pass rate across targeted provisioning/identity tests and full `src/core` `unittest` discovery (`0` removed tests, `<= 18` added focused tests).
  * Operating condition or verification approach, if needed: Run in `src/core` with ambient `python3`, falling back to a workspace-relative gitignored `src/core/.venv` if `azure-iot-hub` dev extra is absent from ambient Python.
  * Observable acceptance criteria: `unittest` discovery exits `0` with all existing and new tests passing.

## Acceptance Criteria

* **AC-1**: `src/core/src/zava_forward/core/synthetic/live_provisioning.py`, `device_identity.py`, and `device_provision.py` explicitly record `approach = "per-device symmetric SAS / DPS enrollment group"` and `credential_owner = "Platform Engineering / IoT Operations Owner"` (with placeholder, personal-data, and secret-pattern refusal).
* **AC-2**: Per-device symmetric SAS credentials are issued at runtime behind opaque `secretref://` references; source files contain zero secret literals, and returned summaries, audit records, exceptions, `repr()`, and `logging` records redact/exclude symmetric keys, connection strings, and SAS tokens.
* **AC-3**: `teardown_simulated_identities` and `deprovision_simulated_devices` deterministically remove every targeted simulated `SIM-*` identity, preserve non-simulated identities, fail closed if any simulated identity or credential remains, and return a verifiable `TeardownReceipt` confirming `verified_zero_residual is True` and `residual_simulated_count == 0`.
* **AC-4**: All existing `src/core` synthetic identity/provisioning/audit tests and new focused unit tests pass, alongside `mypy`, `ruff check`, and `ruff format --isolated --line-length 100 --check` in `src/core`, with `src/core/README.md` updated and a clean local commit on `feat/iot-185-device-provisioning`.

## Implementation Context Record

| Context item                     | Current artifact or record                                                                                                         |
|----------------------------------|------------------------------------------------------------------------------------------------------------------------------------|
| Plan                             | .copilot-tracking/plans/2026-11-15/simulated-device-identity-provisioning-185-plan.md                                              |
| Phase details                    | .copilot-tracking/details/2026-11-15/simulated-device-identity-provisioning-185-phase-details.md                                   |
| Latest critique                  | .copilot-tracking/reviews/plans/2026-11-15/simulated-device-identity-provisioning-185-plan-critique.md with Revise resolved (`PC-001`-`PC-004` closed) |
| Relevant research                | .copilot-tracking/research/2026-11-15/simulated-device-identity-provisioning-185-research.md                                       |
| Changes-record role              | .copilot-tracking/changes/2026-11-15/simulated-device-identity-provisioning-185-changes.md completed across `P01` and `P02`        |
| Planning execution and readiness | Complete; full plan (`P01`, `P02`) implemented and validated                                                                       |
| Continuation context             | Confirmed automatic RPI Agent parent continues to `rpi-review`                                                                     |

## Sources

* `.copilot-tracking/research/2026-11-15/simulated-device-identity-provisioning-185-research.md`: Codebase evidence `C1`-`C14`, contrarian regression guards (`SYN-*` prefix, `assertNoLogs`, CLI `--owner` default), and converged module design.
* `src/core/src/zava_forward/core/synthetic/device_identity.py`: Existing `Manifest`, `DeviceIdentity`, `Registry`, `CredentialStore`, `plan`, `provision`, `rotate`, and `teardown` contracts.
* `src/core/src/zava_forward/core/synthetic/device_provision.py`: Existing `owner_named`, `build_manifest`, `report`, `run`, and `main` contracts.
* `src/core/src/zava_forward/core/diagnostic_logging.py` & `src/core/src/zava_forward/core/synthetic/privacy.py`: Secret regex conventions and synthetic emission audit rules (`source_type == "SYNTHETIC"`, `contains_real_data is False`).
* `docs/adrs/0003-journey-derived-capabilities-runtime-fit.md` (decision 6) & `docs/prds/zava-forward-retrofit-programme-demonstrator.md` (`FR-050`, `AC-066`, `AC-067`): Architectural authority for symmetric key / DPS provisioning, named credential owner, and zero secrets in source or logs.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Implement Simulated Provisioning, Vault Redaction, and Zero-Residual Teardown

* Intent: Author `live_provisioning.py` and additively align `device_identity.py` and `device_provision.py` to satisfy Criteria 1, 2, and 3 without breaking existing `SYN-*` or X.509 callers.
* Dependencies: None

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Create `live_provisioning.py` with DPS/SAS manifest, vault credential store, redaction filter, and `SIM-*` teardown receipts

* Requirement and evidence: FR-1, FR-2, FR-3, NFR-1, NFR-2; research `C1`, `C4`, `C5`, `C6`, `C9`, `C10`, `C11`
* Expected result: `src/core/src/zava_forward/core/synthetic/live_provisioning.py` provides `DEVICE_IDENTITY_APPROACH`, `CREDENTIAL_OWNER_ROLE`, `ProvisioningManifest` (`ProvisioningPlan`), `plan_simulated_provisioning`, `SymmetricSasCredentialStore`, `SimulatedDeviceRegistry`, `redact_provisioning_secrets`, `SecretRedactingFilter`, `provision_simulated_devices`, `rotate_simulated_credentials`, `teardown_simulated_identities`, `deprovision_simulated_devices`, `ProvisioningAuditRecord`, and `TeardownReceipt`.
* Detail section: P01-T01 in .copilot-tracking/details/2026-11-15/simulated-device-identity-provisioning-185-phase-details.md

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Additively align `device_identity.py` and `device_provision.py` with `approach`, `CREDENTIAL_OWNER_ROLE`, secret-owner check, and `TeardownReceipt`

* Requirement and evidence: FR-1, FR-2, FR-3, NFR-2; research `C1`, `C2`, `C7`, `C8`, `C12`
* Expected result: `device_identity.Manifest` carries `approach: str = DEVICE_IDENTITY_APPROACH` and `device_identity.teardown` returns `TeardownReceipt` while preserving 3-arg positional calls and `di.provision` log silence; `device_provision.report` and `device_provision.run` surface `approach`, `teardown_receipt` (on applied teardown), secret-bearing owner refusal, and re-exported `teardown_simulated_identities` / `deprovision_simulated_devices` while keeping CLI `--owner="unassigned"`.
* Detail section: P01-T02 in .copilot-tracking/details/2026-11-15/simulated-device-identity-provisioning-185-phase-details.md

<!-- rpi:phase id=P02 -->
### [x] P02: Focused Unit Tests, Documentation Alignment, and `src/core` Validation

* Intent: Prove AC-1, AC-2, AC-3, and AC-4 with focused semantic and regression unit tests, update `src/core/README.md`, and pass all required `src/core` checks.
* Dependencies: P01

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Author `test_live_provisioning.py` and extend `test_device_identity.py` and `test_device_provision.py`

* Requirement and evidence: AC-1, AC-2, AC-3, NFR-1, NFR-2; research `C7`, `C8`, `C9`, `C12`, `C13`
* Expected result: `src/core/tests/test_live_provisioning.py` (`<= 14` tests) and additive assertions in `test_device_identity.py` (`+2` tests) and `test_device_provision.py` (`+2` tests) with `0` test removals prove explicit approach/owner recording, source/summary/audit/logger secret redaction across keys/connection strings/SAS tokens, and deterministic `SIM-*` zero-residual teardown receipts.
* Detail section: P02-T01 in .copilot-tracking/details/2026-11-15/simulated-device-identity-provisioning-185-phase-details.md

<!-- rpi:task id=P02-T02 -->
#### [x] P02-T02: Update `src/core/README.md` (#185) and execute `src/core` focused validation suite

* Requirement and evidence: AC-4, NFR-1, NFR-2; research `C9`, `C14`
* Expected result: `src/core/README.md` documents `synthetic.live_provisioning`, the recorded DPS/symmetric SAS approach and credential owner role, secret redaction guarantees, and `SIM-*` teardown receipts; `unittest`, `mypy`, `ruff check`, and `ruff format --isolated --line-length 100 --check` all exit `0` in `src/core`.
* Detail section: P02-T02 in .copilot-tracking/details/2026-11-15/simulated-device-identity-provisioning-185-phase-details.md

## Dependencies

* `zava_forward.core.synthetic.sensor_identity` & `sensor_stock`: Used to derive collision-checked sensor keys and select consenting synthetic stock homes 1:1.
* `zava_forward.core.synthetic.privacy`: Used to verify zero personal-data patterns and valid `SYNTHETIC` emission labels on manifests, summaries, reports, and teardown receipts.
* Optional `iothub` / `dev` packages (`azure-iot-hub==2.7.0`, `six==1.17.0` in `src/core/pyproject.toml`): Needed in a workspace-relative gitignored `src/core/.venv` only if ambient `python3` lacks `azure.iot.hub` when running full `src/core` discovery including `test_device_registry_azure.py`.

## Critique Disposition

Record the latest critique findings, their disposition, and any explicitly accepted residual risk. Keep this section outside user decisions and current planning synthesis.

| Critique run and finding | Disposition | Plan response or residual risk |
|--------------------------|-------------|--------------------------------|
| Run 1 `PC-001` [High]    | resolved    | Updated `P01-T01` and `P02-T01` so `SecretRedactingFilter` formats `rendered = record.getMessage()` first, sets `record.msg = redact_provisioning_secrets(rendered)` and `record.args = None`, scrubs `extra`, `stack_info`, `exc_info`, and `exc_text`, and recurses into `tuple` as well as `dict` and `list`. |
| Run 1 `PC-002` [High]    | resolved    | Updated `P01-T01`, `P01-T02`, and `P02-T01` with explicit `mypy --strict` signatures, `audit_log` list capture across success/failure/teardown, sorted multi-run lock acquisition for `run_id=None` `SIM-*` sweeps, `TeardownReceipt.verify()`, and `"source_type": "SYNTHETIC"` + `"contains_real_data": False` + `list` serialization on all `.as_dict()` outputs. |
| Run 1 `PC-003` [Medium]  | resolved    | Removed `/tmp` paths across the plan and `P02`; specified ambient `python3` first with fallback only to workspace-relative gitignored `src/core/.venv` and clean pre-commit `git status --short`. |
| Run 1 `PC-004` [Low]     | resolved    | Updated `P01-T01` to protect `secretref://` and `kv://` URIs at token boundaries ahead of standalone base64 key matching, and updated `P02-T01` to assert URI preservation plus runtime vault-derived key non-leakage and post-teardown `_vault` purge within the `<= 18` test budget. |
| Residual risk (Azure live) | accepted_with_risk | Live Azure IoT Hub / DPS enrollment-group network mutations remain gated out of offline `src/core` tests per ADR 0003 decision 6 and caller non-goals. |

## Follow-Up Items

* Optional live Azure DPS enrollment-group transport adapter: Outside immediate offline `src/core` scope because issue #185 and ADR 0003 keep live Azure Hub/DPS mutations gated behind separate platform owner authorization; owned by Platform Engineering / IoT Operations Owner when live environment provisioning is authorized.

## Handoff

* Implementation artifact: .copilot-tracking/changes/2026-11-15/simulated-device-identity-provisioning-185-changes.md
* Ready phase or task: Complete (`P01`, `P02`); ready for `rpi-review`
* Remaining provisional question or blocker: none

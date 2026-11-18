<!-- markdownlint-disable-file -->
# RPI Changes: Simulated Device Identity and Provisioning (#185)

## Metadata

* Task ID: issue-185-simulated-device-identity-provisioning
* Related plan: .copilot-tracking/plans/2026-11-15/simulated-device-identity-provisioning-185-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/simulated-device-identity-provisioning-185-phase-details.md
* Implementation date: 2026-11-15

## Execution Status

* Status: Complete
* Declared invocation scope: full plan (`P01`, `P02`)
* Completed scope markers: `P01`, `P01-T01`, `P01-T02`, `P02`, `P02-T01`, `P02-T02`
* All remaining active-plan markers: none
* Status basis: Every planned phase and task in `P01` and `P02` is implemented and validated against `src/core` unit tests, strict `mypy`, `ruff check`, and `ruff format --check`.

## Execution Summary

Implemented the simulated device identity and provisioning contracts for issue #185 in `zava_forward.core.synthetic`. Created `src/core/src/zava_forward/core/synthetic/live_provisioning.py` for the `SIM-*` symmetric SAS / DPS enrollment-group lifecycle, additively aligned `device_identity.py` and `device_provision.py` without breaking existing `SYN-*`, X.509, CLI, or `assertNoLogs` callers, added 16 focused unit tests (`0` test removals) across `test_live_provisioning.py`, `test_device_identity.py`, and `test_device_provision.py`, updated `src/core/README.md`, and passed all focused and package-wide `src/core` validation checks.

## Completed Work

### Simulated DPS / Symmetric SAS Provisioning, Vault Redaction, and Zero-Residual Teardown (`P01`, `P01-T01`)

* Created `src/core/src/zava_forward/core/synthetic/live_provisioning.py` defining:
  * Explicit governance constants `DEVICE_IDENTITY_APPROACH = "per-device symmetric SAS / DPS enrollment group"`, `CREDENTIAL_OWNER_ROLE = "Platform Engineering / IoT Operations Owner"`, `DEFAULT_CREDENTIAL_OWNER = CREDENTIAL_OWNER_ROLE`, `CREDENTIAL_ROTATION_POLICY = "ephemeral-per-run-issue-before-revoke"`, and `SIMULATED_DEVICE_PREFIX = "SIM-"`.
  * `SimulatedDeviceIdentity`, `ProvisioningManifest` (aliased as `ProvisioningPlan`), `plan_simulated_provisioning`, and `plan_simulated_register` recording `approach`, `identity_approach`, `credential_owner`, `rotation_policy`, and 1:1 `SIM-*` home-to-device mappings while rejecting blank, placeholder, personal-data, and secret-bearing `credential_owner` strings.
  * `SymmetricSasCredentialStore` generating ephemeral runtime enrollment-group bytes (`secrets.token_bytes(32)`) and deriving per-device symmetric SAS keys via HMAC-SHA256 inside private non-`repr` `_vault` storage while returning only opaque `secretref://dps-sas/...` references.
  * `contains_raw_secret`, `redact_provisioning_secrets`, and `SecretRedactingFilter` protecting `secretref://` and `kv://` URIs at token boundaries first and scrubbing raw symmetric keys, IoT Hub/DPS connection strings, `SharedAccessSignature` SAS tokens, key assignments, and PEM blocks across nested `dict`/`list`/`tuple` payloads, audit records, exceptions (`LiveProvisioningError` with `__suppress_context__ = True`), and formatted `logging` records (`record.getMessage()`, `args`, `extra`, `stack_info`, `exc_info`, and `exc_text`).
  * `SimulatedDeviceRegistry`, `provision_simulated_devices`, `rotate_simulated_credentials`, `teardown_simulated_identities`, and alias `deprovision_simulated_devices` returning a frozen SHA-256 `TeardownReceipt` (`di.TeardownReceipt`) that deterministically removes all targeted `SIM-*` simulated identities under sorted per-run locks, revokes targeted credentials, preserves non-simulated registry entries, fails closed if any residual simulated identity or credential remains, and verifies `verified_zero_residual=True`.

### Additive Alignment in `device_identity.py` and `device_provision.py` (`P01`, `P01-T02`)

* Updated `src/core/src/zava_forward/core/synthetic/device_identity.py` to export `DEVICE_IDENTITY_APPROACH`, `CREDENTIAL_OWNER_ROLE`, and `TeardownReceipt`, add trailing defaulted `approach: str = DEVICE_IDENTITY_APPROACH` on `Manifest` (preserved across `plan`, `provision`, and `rotate`), and return a verified `TeardownReceipt` from `teardown(...)` while keeping 3-argument positional callers, `SYN-*` IDs, and `di.provision` log silence intact.
* Updated `src/core/src/zava_forward/core/synthetic/device_provision.py` to export `DEVICE_IDENTITY_APPROACH`, `CREDENTIAL_OWNER_ROLE`, `DEFAULT_CREDENTIAL_OWNER`, `teardown_simulated_identities`, and `deprovision_simulated_devices`, reject secret-bearing `credential_owner` values with `CREDENTIAL_OWNER_SECRET_MATERIAL`, and include `approach` (and `teardown_receipt` on applied teardowns) in `report`/`run` outputs while preserving CLI `--owner="unassigned"`.

### Focused Unit Tests, Documentation, and `src/core` Validation (`P02`, `P02-T01`, `P02-T02`)

* Created `src/core/tests/test_live_provisioning.py` (12 test methods) and added 2 focused test methods each to `src/core/tests/test_device_identity.py` and `src/core/tests/test_device_provision.py` (`16` added tests total within the `<= 18` cap; `0` test removals) proving Criterion 1 (approach & owner recording + invalid/secret owner refusal), Criterion 2 (zero static secrets in source + vault-derived key isolation + summary/audit/exception/logger redaction across raw keys, connection strings, and SAS tokens), and Criterion 3 (single-run and multi-run `SIM-*` teardown, non-simulated `PROD-*`/`REAL-*` preservation, fail-closed residual identity/credential errors, and verified `TeardownReceipt` digest).
* Updated the `#185` section in `src/core/README.md` to document `synthetic.live_provisioning`, the recorded `per-device symmetric SAS / DPS enrollment group` approach and `Platform Engineering / IoT Operations Owner` role, vault/logger secret redaction, and `SIM-*` zero-residual `TeardownReceipt` contracts.

## Implementation-Time Plan and Detail Updates

* Local judgment (`PC-003` execution): Ambient `python3` lacked optional `azure.iot.hub` imported by `test_device_registry_azure.py`; provisioned workspace-relative gitignored `src/core/.venv` (`pip install -e ".[dev]"`) as planned in `P02`, verified `git status --short` remained clean of `.venv`, and passed both the 115-test synthetic/registry targeted suite and the full 3,703-test `src/core` suite. No plan divergence required.

## Validation Record

| Check | Scope | Status | Evidence or reason |
|-------|-------|--------|--------------------|
| Targeted synthetic & IoT `unittest` | `src/core/tests/{test_live_provisioning,test_device_identity,test_device_provision,test_device_registry_azure,test_iot_device_identity_schema,test_synthetic_output_audit}.py` | Passed | `Ran 115 tests in 1.114s — OK` |
| Full `src/core` `unittest discover -s tests -q` | `src/core/tests` | Passed | `Ran 3703 tests in 1278.530s — OK (skipped=420)` |
| Strict `mypy` | `src/core` (`src` + `tests`) | Passed | `Success: no issues found in 357 source files` |
| `ruff check` | `src/core` | Passed | `All checks passed!` |
| `ruff format --check` (`pyproject.toml` + `--isolated --line-length 100 --check` on touched files) | `src/core` + 6 added/modified Python files | Passed | `304 files already formatted` (`ruff format --check .`) and `6 files already formatted` (`--isolated --line-length 100 --check`) |
| `tools/rpi-checks.py` | Repository gate | Skipped | Explicitly excluded by caller prompt (`Focused` validation tier: `Do NOT run tools/rpi-checks.py`) |

## Pre-Review Reconciliation

* Plan markers and phase details: reconciled (`P01`, `P01-T01`, `P01-T02`, `P02`, `P02-T01`, `P02-T02` checked `[x]`; `Phase Index` statuses set to `completed`)
* Completed-work evidence and handoff prose: reconciled across `plan.md`, `phase-details.md`, and `changes.md`
* Validation, blockers, remaining work, and follow-up items: reconciled (`0` blockers, `0` remaining plan items)
* Review readiness: ready for `rpi-review`

## Blockers

* None

## Remaining Work

* None in active plan (`P01` and `P02` complete).

## Follow-Up Items

* Canonical plan list: .copilot-tracking/plans/2026-11-15/simulated-device-identity-provisioning-185-plan.md, `## Follow-Up Items`
* Optional live Azure DPS enrollment-group transport adapter: Outside immediate offline `src/core` scope per ADR 0003 decision 6; owned by Platform Engineering / IoT Operations Owner when live environment provisioning is authorized.

## Return-to-Caller State

* Implementation execution status: Complete
* Declared scope and markers: full plan; completed: `P01`, `P01-T01`, `P01-T02`, `P02`, `P02-T01`, `P02-T02`; remaining: none
* Validation coverage: 115 targeted synthetic/IoT unit tests (`OK`), 3,703 full `src/core` unit tests (`OK, skipped=420`), `mypy` strict (`357` files, `0` issues), `ruff check` (`All checks passed!`), and `ruff format --check` (`304` package files and `6` touched `--isolated` files formatted)
* Blockers: none
* Current plan and detail updates: local execution of planned gitignored `src/core/.venv` fallback (`PC-003`); zero divergences
* Planning and critique state: ready (`PC-001`-`PC-004` resolved)
* Follow-up items: optional live Azure DPS enrollment-group adapter (deferred per ADR 0003)
* Review readiness or no-handoff reason: review-ready across full plan
* Continuation owner: parent (confirmed automatic RPI Agent continues to `rpi-review`)

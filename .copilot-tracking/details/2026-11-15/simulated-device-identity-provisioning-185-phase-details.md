<!-- markdownlint-disable-file -->
# RPI Phase Details: Simulated Device Identity and Provisioning (#185)

## Metadata

* Task ID: issue-185-simulated-device-identity-provisioning
* Task slug: simulated-device-identity-provisioning-185
* Related plan: .copilot-tracking/plans/2026-11-15/simulated-device-identity-provisioning-185-plan.md
* Evidence sources: .copilot-tracking/research/2026-11-15/simulated-device-identity-provisioning-185-research.md (`C1`-`C14`)

## Phase Index

| Phase ID | Name                                                                            | Status    | Detail sections        |
|----------|---------------------------------------------------------------------------------|-----------|------------------------|
| P01      | Implement Simulated Provisioning, Vault Redaction, and Zero-Residual Teardown   | completed | P01, P01-T01, P01-T02  |
| P02      | Focused Unit Tests, Documentation Alignment, and `src/core` Validation          | completed | P02, P02-T01, P02-T02  |

<!-- rpi:phase id=P01 -->
## P01: Implement Simulated Provisioning, Vault Redaction, and Zero-Residual Teardown

### Context

Research (`C1`-`C4`) established that `src/core/src/zava_forward/core/synthetic/` currently contains `device_identity.py`, `device_provision.py`, and `device_registry_azure.py` using `SYN-*` device IDs, while `live_provisioning.py` does not yet exist. Issue #185 requires: (1) explicit recording of `per-device symmetric SAS / DPS enrollment group` and `Platform Engineering / IoT Operations Owner`, (2) credential issuance and storage with raw symmetric keys, connection strings, and SAS tokens redacted/excluded from source, summaries, audit records, and logger calls, and (3) deterministic teardown (`teardown_simulated_identities` / `deprovision_simulated_devices`) removing every registered simulated `SIM-*` device identity and returning a verifiable zero-residual receipt.

### Intent

Create `live_provisioning.py` as the complete, strictly typed `SIM-*` symmetric SAS / DPS enrollment-group lifecycle module and additively enrich `device_identity.py` and `device_provision.py` without breaking any existing `SYN-*`, X.509, CLI, or `assertNoLogs` behavior.

### Boundaries

* Included: `src/core/src/zava_forward/core/synthetic/live_provisioning.py` (new canonical target), `src/core/src/zava_forward/core/synthetic/device_identity.py`, and `src/core/src/zava_forward/core/synthetic/device_provision.py` (generated targets: `none`).
* Excluded: `device_registry_azure.py`, `src/api/`, `infra/`, live Azure SDK calls, and `pyproject.toml` ignore overrides.

### Likely Targets

* `src/core/src/zava_forward/core/synthetic/live_provisioning.py`: New module implementing `SIM-*` planning, runtime symmetric SAS vault issuance, secret redaction (`redact_provisioning_secrets` + `SecretRedactingFilter`), audit records, and `teardown_simulated_identities` / `deprovision_simulated_devices` returning `TeardownReceipt`.
* `src/core/src/zava_forward/core/synthetic/device_identity.py`: Add `DEVICE_IDENTITY_APPROACH`, `CREDENTIAL_OWNER_ROLE`, `TeardownReceipt`, optional `approach` field on `Manifest`, and `TeardownReceipt` return from `teardown`.
* `src/core/src/zava_forward/core/synthetic/device_provision.py`: Expose `DEVICE_IDENTITY_APPROACH`, `CREDENTIAL_OWNER_ROLE`, `DEFAULT_CREDENTIAL_OWNER`, `teardown_simulated_identities`, and `deprovision_simulated_devices`; surface `approach` and `teardown_receipt` in `report`/`run`; reject secret-bearing `credential_owner` values.

### Dependencies

* None outside `zava_forward.core.synthetic` (`sensor_identity`, `sensor_stock`, `privacy`, `live_readings`) and Python 3.12 stdlib (`dataclasses`, `hashlib`, `hmac`, `json`, `logging`, `re`, `secrets`, `threading`).

### Validation Expectations

* `python3 -m mypy` and `python3 -m ruff check` pass with zero errors on `src/core`.
* Existing `test_device_identity.py`, `test_device_provision.py`, `test_iot_device_identity_schema.py`, and `test_synthetic_output_audit.py` pass unchanged.

### Completion Evidence

* `live_provisioning.py`, `device_identity.py`, and `device_provision.py` pass strict type-checking, lint checks, and import cleanly with zero static secrets.

### Unresolved Items

* None.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Create `live_provisioning.py` with DPS/SAS manifest, vault credential store, redaction filter, and `SIM-*` teardown receipts

#### Context

Caller prompt Criteria 1, 2, and 3 specifically name `src/core/src/zava_forward/core/synthetic/live_provisioning.py`, approach `per-device symmetric SAS / DPS enrollment group`, role `Platform Engineering / IoT Operations Owner`, secret redaction across outputs/audit records/logger calls, and teardown functions `teardown_simulated_identities` / `deprovision_simulated_devices` over `SIM-*` simulated device identities (`C4`, `C5`, `C6`, `C10`, `C11`).

#### Intent

Implement a self-contained, strictly typed `live_provisioning.py` module covering planning, vault-isolated symmetric SAS credential issuance/rotation, multi-layer secret redaction, audit logging, and deterministic `SIM-*` teardown verification.

#### Boundaries

* Included:
  * Canonical constants:
    * `VERSION = "simulated-live-provisioning-v1"`
    * `DEVICE_IDENTITY_APPROACH = "per-device symmetric SAS / DPS enrollment group"`
    * `CREDENTIAL_OWNER_ROLE = "Platform Engineering / IoT Operations Owner"`
    * `DEFAULT_CREDENTIAL_OWNER = CREDENTIAL_OWNER_ROLE`
    * `CREDENTIAL_ROTATION_POLICY = "ephemeral-per-run-issue-before-revoke"`
    * `SIMULATED_DEVICE_PREFIX = "SIM-"`
  * Secret detection and redaction:
    * `contains_raw_secret(text: str) -> bool` and `redact_provisioning_secrets(value: Any) -> Any`: recurse into `dict`, `list`, and `tuple` values; protect `secretref://\S+` and `kv://\S+` opaque URIs at token boundaries first so `/` delimiters inside valid credential references are never mistaken for base64 fragments (`PC-004`); then detect and replace connection strings (`HostName=...;...`, `Endpoint=...;...`), SAS tokens (`SharedAccessSignature ...`, `sig=...`), key assignments (`SharedAccessKey=...`, `PrimaryKey=...`, `SecondaryKey=...`, `AccountKey=...`, `SymmetricKey=...`, `sas_token=...`, `connection_string=...`), PEM private key blocks, and standalone base64 symmetric key tokens (`>=32` base64 chars with key shape/padding, while exempting safe identifiers, `SIM-*`/`SYN-*` device IDs, protected `secretref://`/`kv://` URIs, and 64-char lowercase hex SHA-256 verification digests) with `"<redacted>"`.
    * `SecretRedactingFilter(logging.Filter)` installed on `LOG = logging.getLogger("zava_forward.core.synthetic.live_provisioning")` (plus `install_provisioning_log_redaction(logger)`): resolves the formatted message first via `rendered = record.getMessage()` (falling back safely to `str(record.msg)` on formatting errors), assigns `record.msg = redact_provisioning_secrets(rendered)` and `record.args = None` so `%`-formatting never raises `TypeError` and split arguments cannot evade regexes (`PC-001`), scrubs custom `extra` attributes in `record.__dict__` and `record.stack_info`, clears `record.exc_info = None`, and redacts `record.exc_text`.
  * Error safety:
    * `LiveProvisioningError(RuntimeError)` setting `self.__suppress_context__ = True` and carrying fixed error codes only (with optional `new_manifest` for partial rotation recovery).
  * Manifest and planning:
    * `SimulatedDeviceIdentity(device_id: str, sensor_id: str, home_id: str, credential_ref: str = field(default="", repr=False))` enforcing `device_id == "SIM-" + sensor_id` and `sensor_id == sensor_identity.sensor_key(home_id)` (1:1 home-to-device mapping).
    * `ProvisioningManifest` (and alias `ProvisioningPlan = ProvisioningManifest`): frozen dataclass with `run_id`, `identities`, `approach: str = DEVICE_IDENTITY_APPROACH`, `credential_owner: str = CREDENTIAL_OWNER_ROLE`, `rotation_policy: str = CREDENTIAL_ROTATION_POLICY`, `identity_approach` property, `validate()`, and `as_dict()` (labelled `source_type="SYNTHETIC"`, `contains_real_data=False`, converting sequence fields to JSON `list` values, and exposing `approach`, `identity_approach`, `credential_owner`, `rotation_policy`, `device_count`, and non-secret `devices`).
    * `plan_simulated_provisioning(run_id: str, homes: Sequence[str | Mapping[str, object]] = (), *, credential_owner: str = CREDENTIAL_OWNER_ROLE, approach: str = DEVICE_IDENTITY_APPROACH, rotation_policy: str = CREDENTIAL_ROTATION_POLICY, seed: int = 7) -> ProvisioningManifest` and `plan_simulated_register(register_path: Path, homes: int, run_id: str, *, credential_owner: str = CREDENTIAL_OWNER_ROLE, seed: int = 7) -> ProvisioningManifest`.
  * Ephemeral runtime credential vault and simulated registry:
    * `SymmetricSasCredentialStore`: initializes `_enrollment_group_key = secrets.token_bytes(32)` at runtime (`repr=False`), derives per-device symmetric keys via `hmac.new` + `hashlib.sha256` inside private `_vault` (`repr=False`), issues immutable opaque `secretref://dps-sas/{run_id}/{device_id.lower()}/{seq}` references, never returns or prints raw symmetric keys, connection strings, or SAS tokens, and implements `issue(device_id: str, run_id: str) -> str`, `revoke(reference: str) -> None`, `run_references(run_id: str) -> Sequence[str]`, `all_simulated_references() -> tuple[str, ...]`, and `has_reference(reference: str) -> bool`.
    * `SimulatedDeviceRegistry`: thread-safe in-memory registry tracking `device_id -> run_id` for `SIM-*` simulated identities (and allowing pre-populated non-simulated entries such as `PROD-*` in shared-registry tests so teardown proves non-simulated preservation), implementing `create`, `run_of`, `delete`, `list_run`, `simulated_runs() -> tuple[str, ...]`, and `list_simulated(run_id: str | None = None) -> tuple[str, ...]`.
  * Provisioning, rotation, audit records, and deterministic teardown:
    * `ProvisioningAuditRecord` and `ProvisioningSummary`: `.as_dict()` includes `"source_type": "SYNTHETIC"`, `"contains_real_data": False`, converts all tuples to `list`, scrubs all strings via `redact_provisioning_secrets`, and passes `privacy.emission_issues` (`PC-002`).
    * `provision_simulated_devices(manifest: ProvisioningManifest, registry: di.Registry | SimulatedDeviceRegistry | None = None, store: di.CredentialStore | SymmetricSasCredentialStore | None = None, *, note: str = "", audit_log: list[ProvisioningAuditRecord] | None = None) -> ProvisioningSummary` and `rotate_simulated_credentials(manifest: ProvisioningManifest, store: di.CredentialStore | SymmetricSasCredentialStore, *, note: str = "", audit_log: list[ProvisioningAuditRecord] | None = None) -> ProvisioningSummary`: atomic per-run locked execution, rollback on partial adapter failure without chaining adapter secrets, appending redacted `ProvisioningAuditRecord` to `audit_log` on both success and failure/rollback, and redacted `LOG.info` / `LOG.warning` emission.
    * `TeardownReceipt`: frozen dataclass with `run_id: str | None`, `approach: str`, `credential_owner: str`, `removed_device_ids: tuple[str, ...]`, `removed_count: int`, `revoked_credential_count: int`, `residual_simulated_identities: tuple[str, ...]`, `residual_simulated_count: int`, `residual_credential_count: int`, `verified_zero_residual: bool`, and `verification_sha256: str`, plus `.verify() -> bool` (recomputing canonical JSON SHA-256 and checking `verified_zero_residual and residual_simulated_count == 0 and residual_credential_count == 0`) and `.as_dict()` (including `"source_type": "SYNTHETIC"`, `"contains_real_data": False`, and `list`-converted `removed_device_ids` and `residual_simulated_identities`).
    * `teardown_simulated_identities(registry: di.Registry | SimulatedDeviceRegistry, store: di.CredentialStore | SymmetricSasCredentialStore | None = None, *, manifest: ProvisioningManifest | None = None, run_id: str | None = None, credential_owner: str = CREDENTIAL_OWNER_ROLE, note: str = "", audit_log: list[ProvisioningAuditRecord] | None = None) -> TeardownReceipt` and alias `deprovision_simulated_devices = teardown_simulated_identities`: acquires per-run locks in sorted `run_id` order when sweeping across multiple runs (`run_id=None`) to prevent lock-order deadlocks (`PC-002`), deterministically removes all targeted `SIM-*` simulated identities in sorted order, revokes all targeted credentials (across the run or across all `SIM-*` entries when `run_id=None`), leaves non-simulated devices untouched, re-scans registry and store to verify `0` residual simulated `SIM-*` identities and `0` residual target credentials (appending a redacted failure audit record and raising `LiveProvisioningError("TEARDOWN_RESIDUAL_SIMULATED_IDENTITIES")` or `LiveProvisioningError("TEARDOWN_CREDENTIALS_REMAIN")` if non-zero), emits redacted audit + log records, and returns the verified `TeardownReceipt`.
* Excluded: Hardcoded keys, connection strings, or SAS tokens anywhere in source; network I/O.

#### Likely Targets

* `src/core/src/zava_forward/core/synthetic/live_provisioning.py`: Create module.

#### Dependencies

* None.

#### Validation Expectations

* Strict `mypy` and `ruff` pass on `live_provisioning.py`.

#### Completion Evidence

* `live_provisioning.py` created and verified against all public types and functions above.

#### Unresolved Items

* None.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Additively align `device_identity.py` and `device_provision.py` with `approach`, `CREDENTIAL_OWNER_ROLE`, secret-owner check, and `TeardownReceipt`

#### Context

Existing callers and tests construct `di.Manifest(run_id, credential_owner, identities)` positionally with `SYN-*` IDs (`C1`, `C7`), expect `di.provision` to emit zero log records (`C7`: `test_device_identity.py:106`), and expect `dp.main` without `--owner` to fail `--apply` with `CREDENTIAL_OWNER_NOT_NAMED` (`C8`: `test_device_provision.py:49`). Aligning `device_identity.py` and `device_provision.py` additively ensures callers inspecting either `live_provisioning` or `device_identity`/`device_provision` observe the same `approach`, `CREDENTIAL_OWNER_ROLE`, secret-safe report rules, and verifiable `TeardownReceipt`.

#### Intent

Extend `device_identity.py` and `device_provision.py` additively with zero breaking changes to existing `SYN-*` / X.509 / CLI contracts.

#### Boundaries

* Included:
  * `device_identity.py`:
    * Export `DEVICE_IDENTITY_APPROACH = "per-device symmetric SAS / DPS enrollment group"` and `CREDENTIAL_OWNER_ROLE = "Platform Engineering / IoT Operations Owner"`.
    * Add `approach: str = DEVICE_IDENTITY_APPROACH` as a trailing defaulted field on `Manifest`, validate `bool(self.approach.strip())` in `Manifest.validate()`, accept keyword `approach: str = DEVICE_IDENTITY_APPROACH` in `plan(...)`, and preserve `manifest.approach` in `provision`, `rotate`, and rollback manifests.
    * Add frozen `TeardownReceipt` dataclass (matching zero-residual verification fields, `verification_sha256`, `.verify() -> bool`, and `.as_dict()` with `"source_type": "SYNTHETIC"`, `"contains_real_data": False`, and `list`-converted tuples) and return it from `teardown(...)` after post-delete verification passes.
    * Keep `di.provision` completely silent on `logging` so `test_device_identity.py:106` (`assertNoLogs`) remains green.
  * `device_provision.py`:
    * Export `DEVICE_IDENTITY_APPROACH`, `CREDENTIAL_OWNER_ROLE`, `DEFAULT_CREDENTIAL_OWNER = CREDENTIAL_OWNER_ROLE`, and re-export `teardown_simulated_identities` and `deprovision_simulated_devices` from `live_provisioning`.
    * Refuse `credential_owner` values matching `live_provisioning.contains_raw_secret(...)` with `ProvisionError("CREDENTIAL_OWNER_SECRET_MATERIAL")` alongside the existing `CREDENTIAL_OWNER_PERSONAL_DATA` check.
    * Include `"approach": manifest.approach` in `report(...)` and `"teardown_receipt": receipt.as_dict()` when `run(..., "teardown", True, ...)` completes.
    * Retain `--owner` default `"unassigned"` in `main()` so CLI `--apply` without `--owner` still refuses with `CREDENTIAL_OWNER_NOT_NAMED`.
* Excluded: Changing `SYN-` prefix in `device_identity.py` or modifying `device_registry_azure.py`.

#### Likely Targets

* `src/core/src/zava_forward/core/synthetic/device_identity.py`
* `src/core/src/zava_forward/core/synthetic/device_provision.py`

#### Dependencies

* P01-T01 (`live_provisioning.py`).

#### Validation Expectations

* All existing tests in `test_device_identity.py`, `test_device_provision.py`, `test_device_registry_azure.py`, `test_iot_device_identity_schema.py`, and `test_synthetic_output_audit.py` pass without modification to existing assertions.

#### Completion Evidence

* Updated `device_identity.py` and `device_provision.py` pass strict `mypy`, `ruff`, and existing unit tests.

#### Unresolved Items

* None.

<!-- rpi:phase id=P02 -->
## P02: Focused Unit Tests, Documentation Alignment, and `src/core` Validation

### Context

Every acceptance criterion in issue #185 must be proven by deterministic, focused unit tests under `src/core/tests/`, accompanied by updated `src/core/README.md` documentation and passing `unittest`, `mypy`, `ruff check`, and `ruff format --check` runs (`C9`, `C14`).

### Intent

Add focused unit tests covering all three issue #185 criteria and edge cases, synchronize `src/core/README.md`, and record passing validation across `src/core`.

### Boundaries

* Included: `src/core/tests/test_live_provisioning.py` (new), `src/core/tests/test_device_identity.py` (modified), `src/core/tests/test_device_provision.py` (modified), `src/core/README.md` (modified).
* Excluded: Deleting or weakening any existing test (`0` removals; `<= 18` focused test additions total), running `tools/rpi-checks.py`, or pushing/creating PRs.

### Likely Targets

* `src/core/tests/test_live_provisioning.py`: Comprehensive focused unit tests for Criteria 1, 2, and 3 on `live_provisioning.py`.
* `src/core/tests/test_device_identity.py`: Focused assertions for `Manifest.approach` preservation and `di.teardown` zero-residual `TeardownReceipt`.
* `src/core/tests/test_device_provision.py`: Focused assertions for `approach`, secret-bearing owner refusal, and `teardown_receipt` in `dp.report` / `dp.run`.
* `src/core/README.md`: Updated `#185` section covering `synthetic.live_provisioning`, approach/owner recording, secret redaction, and `SIM-*` zero-residual teardown receipts.

### Dependencies

* P01 (`P01-T01`, `P01-T02`).

### Validation Expectations

* From `src/core`:
  * `python3 -m unittest discover -s tests -q` (using ambient `python3` first, falling back only to workspace-relative gitignored `src/core/.venv` if `azure-iot-hub` dev extra is needed for `test_device_registry_azure.py`, and verifying `git status --short` has zero untracked environment files)
  * `python3 -m mypy`
  * `python3 -m ruff check`
  * `python3 -m ruff format --isolated --line-length 100 --check`

### Completion Evidence

* Zero failures across targeted and full `src/core` unit tests, zero `mypy` errors, zero `ruff check` or `ruff format --check` diagnostics, and updated `src/core/README.md` with clean Markdown diff.

### Unresolved Items

* None.

<!-- rpi:task id=P02-T01 -->
### P02-T01: Author `test_live_provisioning.py` and extend `test_device_identity.py` and `test_device_provision.py`

#### Context

Focused tests must fail without the new contracts and cover happy paths plus adversarial secret-injection and partial/stubborn-teardown edge cases (`C7`, `C8`, `C12`).

#### Intent

Prove Criteria 1, 2, and 3 with `<= 18` crisp, non-redundant unit tests and `0` existing test removals:

1. **Criterion 1 (Approach & Owner)**:
   * `plan_simulated_provisioning` and `ProvisioningManifest.as_dict()` explicitly record `approach == "per-device symmetric SAS / DPS enrollment group"` and default `credential_owner == "Platform Engineering / IoT Operations Owner"`, map each consenting home 1:1 to a unique `SIM-*` identity, and pass `privacy.emission_issues`.
   * Blank, placeholder (`TBD`, `unassigned`), personal-data (`ops@example.org`), and secret-bearing (`SharedAccessKey=...`) `credential_owner` values are rejected with fixed error codes.
   * `device_identity.Manifest` and `device_provision.report` record `approach == "per-device symmetric SAS / DPS enrollment group"`.
2. **Criterion 2 (Secret-Free Source, Summaries, Audit, and Logs)**:
   * Source files (`live_provisioning.py`, `device_identity.py`, `device_provision.py`) contain no hardcoded `SharedAccessKey=`, `SharedAccessSignature`, or static base64 device keys.
   * `provision_simulated_devices` and `rotate_simulated_credentials` issue unique `secretref://dps-sas/...` opaque references into `SymmetricSasCredentialStore`; the runtime HMAC-SHA256 derived symmetric key inside `_vault` never appears in `repr(store)`, `ProvisioningSummary.as_dict()`, `ProvisioningAuditRecord`, or `assertLogs` while active and is purged from `_vault` on `teardown_simulated_identities`; legitimate `secretref://` and `kv://` URIs remain intact through `redact_provisioning_secrets`.
   * Adversarial injection test: injecting raw symmetric keys (`SharedAccessKey=...`), IoT Hub connection strings (`HostName=hub.azure-devices.net;DeviceId=SIM-1;SharedAccessKey=...`), and SAS tokens (`SharedAccessSignature sr=...&sig=...&se=...`) into audit notes, parameterized logger calls (`LOG.info("key=%s", ...)` / `LOG.error("SharedAccessKey=%s", ...)` / `extra={...}`), and failing adapter exceptions (observed via `audit_log=[...]`) confirms captured log records (`assertLogs`), audit records, returned summaries, and formatted tracebacks scrub every secret value without `%`-formatting `TypeError` while preserving `<redacted>` / fixed error codes.
3. **Criterion 3 (Deterministic `SIM-*` Teardown & Zero-Residual Receipt)**:
   * `teardown_simulated_identities` and `deprovision_simulated_devices` remove every registered `SIM-*` identity (both single-run and multi-run full-registry sweep), revoke all credentials, leave non-simulated `PROD-*` entries untouched, and return a `TeardownReceipt` with `verified_zero_residual is True`, `residual_simulated_count == 0`, `residual_simulated_identities == ()`, reproducible `verification_sha256`, and `privacy.emission_issues == []`.
   * Fail-closed teardown verification: when a broken registry leaves a residual `SIM-*` identity or a broken store leaves an unrevoked credential, teardown raises `TEARDOWN_RESIDUAL_SIMULATED_IDENTITIES` or `TEARDOWN_CREDENTIALS_REMAIN` without secret chaining instead of fabricating a clean receipt.
   * `device_identity.teardown` and `device_provision.run(..., "teardown", True, ...)` return/embed a verified zero-residual `TeardownReceipt`.

#### Boundaries

* Included: `src/core/tests/test_live_provisioning.py` (`<= 14` tests), `src/core/tests/test_device_identity.py` (`+2` tests), `src/core/tests/test_device_provision.py` (`+2` tests); exact test removals: `none`.
* Excluded: Trivial getter/constant restatement tests; external network calls.

#### Likely Targets

* `src/core/tests/test_live_provisioning.py`
* `src/core/tests/test_device_identity.py`
* `src/core/tests/test_device_provision.py`

#### Dependencies

* P01-T01, P01-T02.

#### Validation Expectations

* All new and existing tests pass under `unittest` and `mypy --strict`.

#### Completion Evidence

* Passing test output from `unittest` and `mypy`.

#### Unresolved Items

* None.

<!-- rpi:task id=P02-T02 -->
### P02-T02: Update `src/core/README.md` (#185) and execute `src/core` focused validation suite

#### Context

Repository instructions require updating directly related documentation (`src/core/README.md` around `#185`) and running focused validation in `src/core` (`unittest`, `mypy`, `ruff check`, `ruff format --isolated --line-length 100 --check`).

#### Intent

Document `synthetic.live_provisioning` and the aligned `#185` contracts in `src/core/README.md`, then execute and record all required validation commands in `src/core`.

#### Boundaries

* Included: `src/core/README.md` `#185` section update (following AMA Markdown style: `*` unordered lists, plain ASCII punctuation, no em dashes, no bolded-prefix list items); running `unittest`, `mypy`, `ruff check`, and `ruff format --isolated --line-length 100 --check` in `src/core`.
* Excluded: Running `tools/rpi-checks.py`; editing unrelated docs; leaving temporary files in the repository worktree.

#### Likely Targets

* `src/core/README.md`

#### Dependencies

* P02-T01.

#### Validation Expectations

* `python3 -m unittest` (targeted + full `src/core` discovery), `python3 -m mypy`, `python3 -m ruff check`, and `python3 -m ruff format --isolated --line-length 100 --check` all exit `0`.

#### Completion Evidence

* Recorded command exit codes and test counts in `.copilot-tracking/changes/2026-11-15/simulated-device-identity-provisioning-185-changes.md`.

#### Unresolved Items

* None.

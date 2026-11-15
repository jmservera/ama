<!-- markdownlint-disable-file -->
# RPI Plan Critique: Simulated Device Identity and Provisioning (#185)

## Metadata

* Task ID: issue-185-simulated-device-identity-provisioning
* Critique date: 2026-11-15
* Plan: .copilot-tracking/plans/2026-11-15/simulated-device-identity-provisioning-185-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/simulated-device-identity-provisioning-185-phase-details.md
* Critique execution status: Complete

## Inputs and Criterion Boundary

* Task context and caller requirements: Final-candidate critique for Issue #185 ("Simulated device identity and provisioning") in workspace `src/core`. Caller requires: (1) explicit recording of `per-device symmetric SAS / DPS enrollment group` and `credential_owner` role `Platform Engineering / IoT Operations Owner` in `src/core/src/zava_forward/core/synthetic/live_provisioning.py` and aligned manifest/plan contracts; (2) runtime credential issuance and storage with raw symmetric keys, connection strings, and SAS tokens redacted or excluded from source, returned summaries, audit records, and logger calls; (3) deterministic `SIM-*` teardown (`teardown_simulated_identities` / `deprovision_simulated_devices`) returning a verifiable zero-residual teardown receipt; and (4) focused validation tier only in `src/core` (`unittest`, `mypy`, `ruff check`, `ruff format --isolated --line-length 100 --check`), without running `tools/rpi-checks.py`, pushing, or opening a pull request.
* Research and evidence considered: .copilot-tracking/research/2026-11-15/simulated-device-identity-provisioning-185-research.md (`C1`-`C14`), .copilot-tracking/plans/2026-11-15/simulated-device-identity-provisioning-185-plan.md, .copilot-tracking/details/2026-11-15/simulated-device-identity-provisioning-185-phase-details.md, src/core/src/zava_forward/core/synthetic/device_identity.py, src/core/src/zava_forward/core/synthetic/device_provision.py, src/core/src/zava_forward/core/synthetic/privacy.py, src/core/tests/test_device_identity.py, src/core/tests/test_device_provision.py, and src/core/tests/test_synthetic_output_audit.py.
* Decisions, dependencies, and acceptance criteria considered: Confirmed decisions to add `live_provisioning.py` for `SIM-*` lifecycle, additively align `device_identity.py` and `device_provision.py` while preserving `SYN-*` prefixes, 3-argument `Manifest` calls, `di.provision` log silence (`assertNoLogs`), CLI `--owner="unassigned"` refusal, and `privacy.emission_issues` compatibility across `FR-1` through `FR-3`, `NFR-1`, `NFR-2`, and `AC-1` through `AC-4`.
* Assessment boundary: Evaluates internal contract completeness, Python 3.12 `logging` and `privacy` runtime behavior, strict static typing (`mypy --strict`), regression safety against supplied `src/core` source and test files, and host execution constraints. Does not evaluate live Azure IoT Hub or DPS network behavior, which is explicitly out of scope per caller direction and ADR 0003 gating.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern                                                                                                                                   |
|------------------------------------------|----------|-------------------------------------------------------------------------------------------------------------------------------------------------------|
| FR-1 / AC-1 (`C1`, `C2`, `C5`, `C8`)     | Covered  | `live_provisioning.py`, `device_identity.py`, and `device_provision.py` record exact approach and owner constants while preserving CLI `--owner` default. |
| FR-2 / AC-2 (`C6`, `C7`, `C10`, `C11`)   | Partial  | Vault design is sound, but `SecretRedactingFilter` pre-interpolation scrubbing, failed-call audit sink, and URI-vs-base64 ordering have gaps (`PC-001`, `PC-002`, `PC-004`). |
| FR-3 / AC-3 (`C1`, `C2`, `C4`, `C11`)    | Partial  | `SIM-*` teardown and `TeardownReceipt` are covered, but `P01-T01` omits `run_id=None` sweep signatures/locking and synthetic emission labels (`PC-002`). |
| NFR-1 (`C9`)                             | Partial  | Strict `mypy` and `ruff` checks are planned, but literal `(...)` ellipses in `P01-T01` leave public call signatures underspecified (`PC-002`).         |
| NFR-2 / AC-4 (`C3`, `C7`, `C8`, `C12`-`C14`) | Partial | Backward-compatibility guards are thorough, but fallback virtualenv guidance points to `/tmp/venv-185-core`, violating workspace-only write rules (`PC-003`). |
| P01 / P01-T01                            | Partial  | Needs post-`getMessage()` log redaction (`PC-001`), explicit signatures, `audit_log` sink, and `.as_dict()` synthetic labels + list conversion (`PC-002`). |
| P01-T02                                  | Covered  | Additive `Manifest.approach`, `TeardownReceipt` return from `di.teardown`, and `dp.report` / `dp.run` extensions preserve all existing `SYN-*` tests. |
| P02 / P02-T01                            | Partial  | Strong adversarial matrix within `<= 18` tests, but needs vault-derived runtime key non-leakage/purge check (`PC-004`) and aligned `audit_log` usage (`PC-002`). |
| P02-T02                                  | Partial  | Covers `src/core/README.md` and focused validation commands, subject to replacing `/tmp` virtualenv fallback in `P02` (`PC-003`).                      |

## Verdict

* Verdict: Revise
* Rationale: The architecture and backward-compatibility boundaries (`live_provisioning.py` for `SIM-*` plus additive `device_identity.py` and `device_provision.py` updates preserving `SYN-*`, `assertNoLogs`, and CLI `--owner="unassigned"`) are well-grounded in codebase evidence, and no user decisions remain open. However, four planner-resolvable defects in `P01-T01`, `P02`, and `P02-T01` would cause runtime `TypeError` failures or missed split secrets in `SecretRedactingFilter` (`PC-001`), `privacy.emission_issues` label/tuple mismatches and missing failure/teardown audit-sink signatures (`PC-002`), prohibited `/tmp` directory writes (`PC-003`), and incomplete verification of actual vault-derived secret material and `kv://` URI redaction safety (`PC-004`). All four items are direct planner corrections.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: SecretRedactingFilter pre-interpolation msg and args scrubbing breaks percent-formatting and misses split secrets

* Related IDs: FR-2, AC-2, P01-T01, P02-T01, C10
* Evidence: .copilot-tracking/details/2026-11-15/simulated-device-identity-provisioning-185-phase-details.md (P01-T01, P02-T01)
* Concern: `P01-T01` specifies that `SecretRedactingFilter(logging.Filter)` scrubs `record.msg` and `record.args` (tuples and mappings) separately while leaving string interpolation to downstream handlers. In Python 3.12 `logging`, when a caller invokes `LOG.error("Failed with SharedAccessKey=%s", raw_key)`, scrubbing `record.msg` first replaces `SharedAccessKey=%s` with `"<redacted>"` and strips the `%s` format specifier while `record.args` remains a 1-tuple, causing `record.getMessage()` inside handlers and `unittest.TestCase.assertLogs` to raise `TypeError: not all arguments converted during string formatting`. Conversely, split parameterized calls such as `LOG.warning("%s=%s", "SharedAccessKey", short_secret)` evade per-argument regexes before interpolation, and custom `extra={...}` fields or `stack_info` on `LogRecord` are left unscrubbed. In addition, `redact_provisioning_secrets` must explicitly recurse into `tuple` values as well as `dict` and `list`.
* Impact: Parameterized logger calls exercised by `P02-T01` (`LOG.info` / `LOG.error` with injected secrets) can crash with `TypeError` during handler formatting or leak split secret tokens and `extra` attributes into captured log records.
* Smallest useful change: Update `P01-T01` so `SecretRedactingFilter.filter(record)` first resolves the formatted message via `record.getMessage()` (falling back safely to `str(record.msg)` if formatting fails), assigns `record.msg = redact_provisioning_secrets(rendered)` and `record.args = None`, scrubs non-standard `LogRecord.__dict__` (`extra`) values and `record.stack_info` in addition to clearing `record.exc_info` and redacting `record.exc_text`, and specifies that `redact_provisioning_secrets` recurses into `dict`, `list`, and `tuple`.
* Action owner: planning_parent
* Exact resolving evidence: Revised `P01-T01` in .copilot-tracking/details/2026-11-15/simulated-device-identity-provisioning-185-phase-details.md specifying post-`getMessage()` redaction with `record.args = None`, `extra`/`stack_info` scrubbing, and `tuple` recursion, paired with parameterized `LOG.info`/`LOG.error` secret-injection coverage in `P02-T01`.
* Decision route: Direct planner correction; no user decision required.

<!-- rpi:critique id=PC-002 -->
### PC-002 [High]: P01-T01 omits typed lifecycle signatures, failure and teardown audit-sink access, and synthetic emission labels required by P02-T01 and privacy.py

* Related IDs: FR-2, FR-3, NFR-1, AC-2, AC-3, P01-T01, P02-T01, C9, C11, C12
* Evidence: .copilot-tracking/details/2026-11-15/simulated-device-identity-provisioning-185-phase-details.md (P01-T01, P02-T01), .copilot-tracking/research/2026-11-15/simulated-device-identity-provisioning-185-research.md (Complete Examples), src/core/src/zava_forward/core/synthetic/privacy.py
* Concern: Three contract gaps exist between `P01-T01`, `P02-T01`, and `privacy.py`: (1) `privacy.emission_issues` (`privacy.py:67-73`) returns `["missing_synthetic_label"]` unless a dictionary carries `"source_type": "SYNTHETIC"` and `"contains_real_data": False`, and `privacy.pattern_issues` (`privacy.py:30-47`) recurses into `dict` and `list` only, skipping `tuple` elements. `P01-T01` defines synthetic labels only on `ProvisioningManifest.as_dict()`, omitting them and `tuple`-to-`list` conversion on `TeardownReceipt.as_dict()`, `ProvisioningSummary.as_dict()`, and `ProvisioningAuditRecord.as_dict()` even though `P02-T01` asserts `privacy.emission_issues == []` on `TeardownReceipt` and `P01-T01` requires it on summaries and audit records. (2) `P01-T01` writes literal `(...)` ellipses for `provision_simulated_devices(...)`, `rotate_simulated_credentials(...)`, and `teardown_simulated_identities(...)` instead of typed signatures, leaving ambiguous how `teardown_simulated_identities` supports both single-manifest teardown and `run_id=None` multi-run full-registry `SIM-*` sweeps (including sorted multi-run lock acquisition to prevent lock-order deadlocks and revoking all simulated credentials across runs), and uses `homes_or_sensors` in `plan_simulated_provisioning` whereas research's example uses keyword `homes=(...)`. (3) `P02-T01` requires asserting redacted `ProvisioningAuditRecord` entries on failing adapter exceptions and teardown, but `provision_simulated_devices` raises `LiveProvisioningError` on rollback instead of returning `ProvisioningSummary` and `teardown_simulated_identities` returns `TeardownReceipt`, with no caller-supplied `audit_log` sink specified to observe audit records on failed or teardown calls.
* Impact: `privacy.emission_issues` assertions in `P02-T01` will fail with `missing_synthetic_label` (or bypass PII checks on un-serialized tuples), `mypy --strict` callers/tests face inconsistent signatures across single-run and `run_id=None` sweep modes, and `P02-T01` cannot inspect failure-path or teardown `ProvisioningAuditRecord` emissions.
* Smallest useful change: Update `P01-T01` to: (a) include `"source_type": "SYNTHETIC"`, `"contains_real_data": False`, and `list`-converted sequence fields on `.as_dict()` for `ProvisioningManifest`, `ProvisioningSummary`, `ProvisioningAuditRecord`, and `TeardownReceipt` (plus deterministic canonical JSON preimage and `.verify() -> bool` on `TeardownReceipt`, also matched on `device_identity.TeardownReceipt` in `P01-T02`); (b) replace `(...)` with explicit `mypy --strict` signatures for `plan_simulated_provisioning` (accepting `homes` / sensor rows cleanly), `provision_simulated_devices`, `rotate_simulated_credentials`, and `teardown_simulated_identities` (defining sorted multi-run lock ordering and simulated-store credential sweep when `run_id=None`); and (c) add optional `*, note: str = "", audit_log: list[ProvisioningAuditRecord] | None = None` parameters across provision, rotate, and teardown so redacted audit records are appended even when an adapter raises and triggers rollback.
* Action owner: planning_parent
* Exact resolving evidence: Revised `P01-T01` (and aligned `TeardownReceipt.as_dict()` / `.verify()` note in `P01-T02`) in .copilot-tracking/details/2026-11-15/simulated-device-identity-provisioning-185-phase-details.md documenting exact typed signatures, `audit_log` capture on success/failure/teardown, `run_id=None` multi-run lock/revocation semantics, and synthetic emission labels plus `list` conversion across all `.as_dict()` methods.
* Decision route: Direct planner correction; no user decision required.

<!-- rpi:critique id=PC-003 -->
### PC-003 [Medium]: Fallback test virtualenv path /tmp/venv-185-core violates workspace-only file creation constraints

* Related IDs: NFR-2, AC-4, P02, P02-T02, C9
* Evidence: .copilot-tracking/plans/2026-11-15/simulated-device-identity-provisioning-185-plan.md (What You May Not Know, NFR-2, Dependencies), .copilot-tracking/details/2026-11-15/simulated-device-identity-provisioning-185-phase-details.md (P02 Validation Expectations)
* Concern: The plan instructs implementation to create an isolated external virtualenv at `/tmp/venv-185-core` (and `P02` specifies an external `.venv` outside the repo) if ambient `python3` lacks `azure-iot-hub==2.7.0` for `test_device_registry_azure.py`. Writing files or directories under `/tmp` or `/var/tmp` violates active host environment rules requiring any scratch or environment files to stay relative to the current working directory and never touch `/tmp`.
* Impact: Executing the documented `/tmp/venv-185-core` fallback during `P02-T02` violates host execution constraints or fails sandbox checks.
* Smallest useful change: Revise .copilot-tracking/plans/2026-11-15/simulated-device-identity-provisioning-185-plan.md and `P02` in .copilot-tracking/details/2026-11-15/simulated-device-identity-provisioning-185-phase-details.md to test with ambient `python3` (or pre-existing non-`/tmp` environment) first, and only if `azure.iot.hub` is missing, create a workspace-relative gitignored `.venv` inside the repository worktree (verifying `git status --short` contains no untracked environment artifacts before committing) rather than writing to `/tmp` or outside the workspace.
* Action owner: planning_parent
* Exact resolving evidence: Updated .copilot-tracking/plans/2026-11-15/simulated-device-identity-provisioning-185-plan.md and .copilot-tracking/details/2026-11-15/simulated-device-identity-provisioning-185-phase-details.md with zero `/tmp` references and workspace-relative fallback environment handling.
* Decision route: Direct planner correction; no user decision required.

<!-- rpi:critique id=PC-004 -->
### PC-004 [Low]: P02-T01 and P01-T01 do not explicitly guard URI slashes before standalone base64 redaction or assert non-leakage and purge of actual vault-derived key material

* Related IDs: FR-2, FR-3, AC-2, AC-3, P01-T01, P02-T01
* Evidence: .copilot-tracking/details/2026-11-15/simulated-device-identity-provisioning-185-phase-details.md (P01-T01, P02-T01), src/core/tests/test_device_identity.py
* Concern: First, `/` is part of the standard base64 alphabet (`[A-Za-z0-9+/]`), so a naive standalone `>=32`-char base64 regex in `redact_provisioning_secrets` can match across `/`-delimited opaque credential URIs without hyphens (for example `kv://zavasim/syn0123456789abcdef01/1`, where `//zavasim/syn0123456789abcdef01/1` is 33 valid base64 characters) unless `secretref://\S+` and `kv://\S+` tokens are explicitly protected or excluded at token boundaries before standalone base64 matching. Second, `P02-T01` validates Criterion 2 against adversarially injected strings (`SharedAccessKey=...`, connection strings, SAS tokens), which tests the scrubber, but does not explicitly assert that the actual HMAC-SHA256 per-device symmetric key material derived at runtime inside `SymmetricSasCredentialStore` is absent from `repr(store)`, `ProvisioningSummary.as_dict()`, `ProvisioningAuditRecord`, and `assertLogs` while active, and removed from `_vault` after `teardown_simulated_identities`.
* Impact: Over-broad base64 matching could corrupt legitimate opaque `kv://` or `secretref://` references, and omitting an assertion against actual vault-derived key material leaves runtime vault isolation and teardown key purge indirectly tested.
* Smallest useful change: In `P01-T01`, specify token-boundary and `secretref://` / `kv://` URI protection ahead of standalone base64 key matching in `contains_raw_secret` and `redact_provisioning_secrets`; in `P02-T01` (within the existing `<= 18` test budget), add assertions confirming `kv://` / `secretref://` references remain intact through redaction and that the runtime-derived symmetric key material inside `SymmetricSasCredentialStore` never appears in `repr(store)`, summaries, audit records, or logs and is purged from `_vault` upon teardown.
* Action owner: planning_parent
* Exact resolving evidence: Updated `P01-T01` and `P02-T01` in .copilot-tracking/details/2026-11-15/simulated-device-identity-provisioning-185-phase-details.md specifying URI-safe standalone base64 token boundaries and vault-derived key non-leakage plus post-teardown purge assertions within the `<= 18` test cap.
* Decision route: Direct planner correction; no user decision required.

## Strengths and Residual Risk

* Contrarian regression analysis in research (`C3`, `C7`, `C8`, `C12`, `C13`) is accurately carried into the plan: keeping `SYN-*` in `device_identity.py`, preserving `self.assertNoLogs(level=logging.DEBUG)` around `di.provision`, and keeping `dp.main` `--owner` defaulted to `"unassigned"` prevents breaking 40+ existing unit tests across `src/core` and `src/api`.
* Exception context suppression (`raise ... from None` with `__suppress_context__ = True`) matches the established security pattern in `src/core/tests/test_device_identity.py` (`test_teardown_inside_except_does_not_chain_caller_secret`, `test_provision_inside_except_does_not_chain_caller_secret`).
* Explicitly accepted residual risk: Live Azure IoT Hub and Azure Device Provisioning Service enrollment-group mutations are not exercised in offline `src/core` unit tests; per ADR 0003 decision 6 and caller non-goals, live cloud provisioning remains gated behind separate Platform Engineering / IoT Operations Owner authorization.

## Questions or Blocking Evidence Gaps

* None. All four findings (`PC-001` through `PC-004`) are deterministic technical refinements fully resolved by supplied codebase evidence and confirmed caller requirements.

## Limitations

* Critique was bounded strictly to supplied planning, research, and `src/core` source/test artifacts without external research or live cloud execution.
* Ambient Python package availability (`azure-iot-hub==2.7.0` for `test_device_registry_azure.py`) was not probed during read-only critique; `PC-003` ensures any fallback environment stays inside workspace boundaries.

## Recommended Next Action

* Highest-impact finding: PC-001
* Action owner: planning_parent
* Smallest next action: Directly revise `P01-T01`, `P01-T02`, `P02`, and `P02-T01` in .copilot-tracking/details/2026-11-15/simulated-device-identity-provisioning-185-phase-details.md and update .copilot-tracking/plans/2026-11-15/simulated-device-identity-provisioning-185-plan.md (including `Critique Disposition` and `Planning status: finalized`) to resolve `PC-001` through `PC-004` without another critique pass.
* User response required: no

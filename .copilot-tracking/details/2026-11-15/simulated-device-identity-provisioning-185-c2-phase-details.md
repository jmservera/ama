---
title: "RPI Phase Details: PR #1801 c2 Credential-Hygiene Test Fixture Remediation (Issue #185)"
description: "Evidence-backed phase details for runtime assembly of synthetic secret test fixtures in src/core/tests and Focused validation"
ms.date: 2026-11-15
---
<!-- markdownlint-disable-file -->

## Metadata

* Task ID: issue-185-simulated-device-identity-provisioning-c2
* Task slug: simulated-device-identity-provisioning-185-c2
* Related plan: .copilot-tracking/plans/2026-11-15/simulated-device-identity-provisioning-185-c2-plan.md
* Evidence sources: .copilot-tracking/research/2026-11-15/simulated-device-identity-provisioning-185-c2-research.md (`C1`-`C9`), src/api/tests/test_iot_credential_hygiene.py, src/core/tests/test_live_provisioning.py, src/core/tests/test_device_provision.py, src/core/pyproject.toml, .github/workflows/src-ci.yml

## Phase Index

| Phase ID | Name                                                                   | Status   | Detail sections        |
|----------|------------------------------------------------------------------------|----------|------------------------|
| P01      | Runtime Synthetic Secret Assembly and Test-Source Hygiene Guard        | Complete | P01, P01-T01, P01-T02  |
| P02      | Focused Validation, CI Parity Verification, and Local Git Identity Check | Complete | P02, P02-T01         |

<!-- rpi:phase id=P01 -->
## P01: Runtime Synthetic Secret Assembly and Test-Source Hygiene Guard

### Context

On `PR #1801` (`ffce28c98`), `9/10` CI jobs succeeded and `src-api` failed solely on `test_iot_credential_hygiene.SourceScanTests.test_no_device_key_or_connection_string_in_repository_text` with `3` findings across `src/core/tests/test_live_provisioning.py` (`device connection string`, `private key block`) and `src/core/tests/test_device_provision.py` (`shared access key value`) (`C1`, `C2`). Research Wave 3 (`C3`) also showed that `PATTERNS["device connection string"]` and `PATTERNS["shared access signature"]` use greedy `[^\n]*` on a single source line, meaning naive single-line `" + "` concatenation without splitting keywords can still match after 100-column `ruff format`.

### Intent

Replace contiguous literal synthetic secret fixtures in `src/core/tests/test_live_provisioning.py` and `src/core/tests/test_device_provision.py` with runtime `"".join((...))` / string concatenation across split keyword, domain, and base64 segments so runtime strings passed to functions under test remain byte-for-byte identical while raw source text contains `0` matches for `PATTERNS`, and extend `test_live_provisioning.py` source-hygiene verification to scan synthetic provisioning test files too.

### Boundaries

* Included: `src/core/tests/test_live_provisioning.py` and `src/core/tests/test_device_provision.py`.
* Excluded: `src/api/tests/test_iot_credential_hygiene.py`, `src/core/src/zava_forward/core/synthetic/*`, `pyproject.toml`, and CI workflows.

### Likely Targets

* `src/core/tests/test_live_provisioning.py`: Module-level constants `RAW_KEY_B64`, `RAW_CONN_STR`, `RAW_SAS_TOKEN`, `RAW_PEM`, the 36-char signature assertion fragment in `test_outputs_and_audit_records_redact_keys_connection_strings_and_sas_tokens` / `test_logger_filter_redacts_percent_formatted_split_extra_and_exception_secrets`, and `test_source_modules_contain_no_embedded_keys_connection_strings_or_sas_tokens` (`C4`, `C7`).
* `src/core/tests/test_device_provision.py`: `test_report_refuses_secret_bearing_credential_owner` (`C5`, `C7`).

### Dependencies

* None.

### Validation Expectations

* Runtime SHA-256 digests of `RAW_KEY_B64`, `RAW_CONN_STR`, `RAW_SAS_TOKEN`, `RAW_PEM`, and the `test_device_provision.py` owner string equal their `ffce28c98` runtime digests.
* `test_iot_credential_hygiene.py` reports `0` findings across the entire repository.
* `ruff check .`, `ruff format --check .`, and `mypy` inside `src/core` exit `0`.

### Completion Evidence

* Clean diff confined to `src/core/tests/test_live_provisioning.py` and `src/core/tests/test_device_provision.py`, verified runtime digest invariance, and passing `test_source_modules_contain_no_embedded_keys_connection_strings_or_sas_tokens` and `test_iot_credential_hygiene.py` runs recorded in `.copilot-tracking/changes/2026-11-15/simulated-device-identity-provisioning-185-c2-changes.md`.

### Unresolved Items

* None.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Assemble synthetic secret constants at runtime and guard test sources in `src/core/tests/test_live_provisioning.py`

#### Context

`src/core/tests/test_live_provisioning.py` defines `RAW_KEY_B64`, `RAW_CONN_STR`, `RAW_SAS_TOKEN`, and `RAW_PEM` as contiguous string/f-string literals (`C4`). In addition, `test_source_modules_contain_no_embedded_keys_connection_strings_or_sas_tokens` currently checks only `live_provisioning.py`, `device_identity.py`, and `device_provision.py`, leaving test files unchecked during standalone `src-core` test runs (`C4`).

#### Intent

Assemble `RAW_KEY_B64`, `RAW_CONN_STR`, `RAW_SAS_TOKEN`, `RAW_PEM`, and a shared `RAW_SAS_SIG_FRAGMENT` constant (used at both assertion sites in `test_outputs_and_audit_records_redact_keys_connection_strings_and_sas_tokens` and `test_logger_filter_redacts_percent_formatted_split_extra_and_exception_secrets`) at runtime from split keyword, domain, and base64 segments (`"".join((...))` / `+`) so runtime values are unchanged, and extend `test_source_modules_contain_no_embedded_keys_connection_strings_or_sas_tokens` to assert:
1. Each runtime-assembled synthetic fixture (`RAW_KEY_B64`, `RAW_CONN_STR`, `RAW_SAS_TOKEN`, `RAW_PEM`) is still recognized by `lp.contains_raw_secret(...)` (proving negative-test potency).
2. Existing `ast` constant literal scanning (`lp.contains_raw_secret(node.value)`) continues to pass on `live_provisioning.py`, `device_identity.py`, and `device_provision.py` (preserving standalone base64 literal detection and keeping `import ast` active under `ruff` `F401`).
3. Raw source text of `live_provisioning.py`, `device_identity.py`, `device_provision.py`, `test_live_provisioning.py`, `test_device_provision.py`, and `test_device_identity.py` contains zero matches for the four credential-hygiene regex rules (`shared access key value`, `shared access signature`, `device connection string`, and `private key block`, compiled without literal self-matches).

#### Boundaries

* Included: `src/core/tests/test_live_provisioning.py`.
* Excluded: Production modules under `src/core/src/` and scanner rules under `src/api/tests/`.

#### Likely Targets

* `src/core/tests/test_live_provisioning.py`: Runtime constant definitions (`RAW_KEY_B64`, `RAW_CONN_STR`, `RAW_SAS_TOKEN`, `RAW_PEM`, `RAW_SAS_SIG_FRAGMENT`), both redaction assertion lists, and `test_source_modules_contain_no_embedded_keys_connection_strings_or_sas_tokens`.

#### Dependencies

* None.

#### Validation Expectations

* `(cd src/core && python3 -m ruff format --check tests/test_live_provisioning.py && python3 -m ruff check tests/test_live_provisioning.py)` exits `0`.
* `PYTHONPATH=src/core/src:src/core/tests python3 -m unittest src/core/tests/test_live_provisioning.py -v` passes all `12` tests.

#### Completion Evidence

* Zero source-scan matches in `test_live_provisioning.py` and `12/12` passing tests in `LiveProvisioningTests`.

#### Unresolved Items

* None.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Assemble the secret-bearing owner test input at runtime in `src/core/tests/test_device_provision.py`

#### Context

`test_report_refuses_secret_bearing_credential_owner` in `src/core/tests/test_device_provision.py` passes a contiguous `"Owner SharedAccess" + "Key=..."` literal into `di.plan(...)`, triggering `PATTERNS["shared access key value"]` in `test_iot_credential_hygiene.py` (`C2`, `C5`).

#### Intent

Construct the secret-bearing owner string at runtime by concatenating split `"Owner SharedAccess"`, `"Key="`, and the two 22-character halves of the synthetic base64 key so the exact same runtime string reaches `di.plan(...)` and `dp.report(...)` while `test_device_provision.py` contains `0` literal matches for `PATTERNS`.

#### Boundaries

* Included: `src/core/tests/test_device_provision.py`.
* Excluded: All other test methods in `test_device_provision.py` and `device_provision.py` production code.

#### Likely Targets

* `src/core/tests/test_device_provision.py`: `DeviceProvisionTests.test_report_refuses_secret_bearing_credential_owner`.

#### Dependencies

* None.

#### Validation Expectations

* `(cd src/core && python3 -m ruff format --check tests/test_device_provision.py && python3 -m ruff check tests/test_device_provision.py)` exits `0`.
* `PYTHONPATH=src/core/src:src/core/tests python3 -m unittest src/core/tests/test_device_provision.py -v` passes all `12` tests.

#### Completion Evidence

* Zero source-scan matches in `test_device_provision.py` and `12/12` passing tests in `DeviceProvisionTests`.

#### Unresolved Items

* None.

<!-- rpi:phase id=P02 -->
## P02: Focused Validation, CI Parity Verification, and Local Git Identity Check

### Context

Under owner decision D4 and Issue `#1294`, this test-only `c2` remediation takes the Focused validation tier (`C9`). `.github/workflows/src-ci.yml` executes `python -m unittest discover -s tests -v`, `ruff check . && ruff format --check .`, and `mypy` inside `src/core`, while `src-api` executes `src/api/tests/test_iot_credential_hygiene.py` (`C8`). Before creating the final frozen local commit after `rpi-review`, repository rules require resolving `gh api user` and configuring `{id}+{login}@users.noreply.github.com` locally.

### Intent

Execute all caller-specified and CI-parity Focused validation checks, verify runtime fixture SHA-256 invariance against `ffce28c98`, record exact outputs in `.copilot-tracking/changes/2026-11-15/simulated-device-identity-provisioning-185-c2-changes.md`, and confirm repository-local privacy-safe git identity for the single atomic post-Review local commit.

### Boundaries

* Included: Focused `unittest` runs in `src/core` and `src/api/tests/test_iot_credential_hygiene.py`, `ruff check .`, `ruff format --check .`, and `mypy` in `src/core`, runtime SHA-256 fixture verification, `gh api user` + `git config --local user.email` verification, and post-Review single local `git commit` with `Refs #185` and `Co-authored-by` trailer.
* Excluded: `tools/rpi-checks.py`, `git push`, `gh pr create`, `git commit --amend`, or global git config edits.

### Likely Targets

* `.copilot-tracking/changes/2026-11-15/simulated-device-identity-provisioning-185-c2-changes.md`: Implementation and validation record.
* Worktree-local git configuration (`user.email` and `user.name`).

### Dependencies

* P01 (`P01-T01`, `P01-T02`).

### Validation Expectations

* `PYTHONPATH=src/core/src:src/core/tests python3 -m unittest src/core/tests/test_device_provision.py src/core/tests/test_live_provisioning.py -v` exits `0` (`24` tests).
* `PYTHONPATH=src/api/src:src/api/tests:src/core/src:src/core/tests:src/agents/src:src/agents/tests python3 -m unittest src/api/tests/test_iot_credential_hygiene.py -v` exits `0` (`12` tests).
* `(cd src/core && PYTHONPATH=src:tests python3 -m unittest tests/test_live_provisioning.py tests/test_device_identity.py tests/test_device_provision.py tests/test_iot_device_identity_schema.py tests/test_synthetic_output_audit.py tests/test_dependency_rule.py tests/test_live_doc_links.py -q)` exits `0` (`80` tests), and `python3 tools/rename-zava-tests.py` exits `0` (`25` tests).
* `(cd src/core && python3 -m ruff check . && python3 -m ruff format --check . && python3 -m mypy)` exits `0`.
* Runtime SHA-256 comparison confirms `RAW_KEY_B64`, `RAW_CONN_STR`, `RAW_SAS_TOKEN`, `RAW_PEM`, and the `test_device_provision.py` secret-bearing owner string match `ffce28c98` byte-for-byte.

### Completion Evidence

* Passing outputs for all `unittest`, `ruff`, `mypy`, and SHA-256 checks recorded in `.copilot-tracking/changes/2026-11-15/simulated-device-identity-provisioning-185-c2-changes.md`, followed after `rpi-review` by a clean frozen local commit (`git status --short` empty) and a final post-commit `test_iot_credential_hygiene.py` pass.

### Unresolved Items

* None.

<!-- rpi:task id=P02-T01 -->
### P02-T01: Run Focused `unittest`, `ruff`, `mypy`, and runtime digest checks and confirm privacy-safe git identity

#### Context

Matches both the explicit caller validation commands and `.github/workflows/src-ci.yml` `src-core` / `src-api` `test_iot_credential_hygiene.py` checks (`C8`, `C9`).

#### Intent

Run all Focused validation commands, verify runtime string SHA-256 invariance, confirm repository-local `{id}+{login}@users.noreply.github.com` configuration via `gh api user`, and record complete evidence in the `c2` changes artifact.

#### Boundaries

* Included: Validation command execution, repository-local git email verification, and `.copilot-tracking/changes/2026-11-15/simulated-device-identity-provisioning-185-c2-changes.md` authoring.
* Excluded: Remote push or PR creation.

#### Likely Targets

* `.copilot-tracking/changes/2026-11-15/simulated-device-identity-provisioning-185-c2-changes.md`.

#### Dependencies

* P01-T01, P01-T02.

#### Validation Expectations

* All five validation commands under `P02` exit `0` and `git config --local user.email` equals `{id}+{login}@users.noreply.github.com`.

#### Completion Evidence

* Exact exit codes, test counts, SHA-256 invariance check, and local git identity check documented in `.copilot-tracking/changes/2026-11-15/simulated-device-identity-provisioning-185-c2-changes.md`.

#### Unresolved Items

* None.

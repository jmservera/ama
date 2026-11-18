---
title: "RPI Plan: PR #1801 c2 Credential-Hygiene Test Fixture Remediation (Issue #185)"
description: "Implementation plan for Issue #185 PR #1801 c2 src-api test_iot_credential_hygiene remediation in src/core/tests"
ms.date: 2026-11-15
---
<!-- markdownlint-disable-file -->

## Task Metadata

* Task ID: issue-185-simulated-device-identity-provisioning-c2
* Task slug: simulated-device-identity-provisioning-185-c2
* Planning status: Ready
* Plan date: 2026-11-15
* Phase details: .copilot-tracking/details/2026-11-15/simulated-device-identity-provisioning-185-c2-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-11-15/simulated-device-identity-provisioning-185-c2-plan-critique.md

## Executive Summary

This `c2` child plan resolves the sole hosted CI failure on `PR #1801` (`feat/iot-185-device-provisioning` at `ffce28c98`, targeting `feat/demo-164-chat-grounding-provenance-0900` / `PR #1641`) for Issue `#185`. Commit `ffce28c98` passed `9/10` CI checks (including `src-core`, `mssql`, `src-namespace`, `src-agents`, `src-importer`, and `src-orchestrator`) and failed only `src-api` on `test_iot_credential_hygiene.SourceScanTests.test_no_device_key_or_connection_string_in_repository_text` because negative secret-redaction and secret-refusal unit tests in `src/core/tests/test_live_provisioning.py` and `src/core/tests/test_device_provision.py` constructed synthetic secret fixtures as contiguous string literals in Python source text. Assembling those synthetic test inputs at runtime across split keyword, domain, and base64 segments via `"".join((...))` and string concatenation keeps every runtime string passed to the functions under test byte-for-byte identical while ensuring `0` literal source matches across `test_iot_credential_hygiene.PATTERNS` (including greedy `[^\n]*` single-line rules under 100-column `ruff format`). A focused test-source hygiene assertion in `src/core/tests/test_live_provisioning.py` also prevents standalone `src-core` runs from missing test-file literal regressions, verified under Focused validation and committed locally on `feat/iot-185-device-provisioning` without pushing.

### User Decisions and Requirements Highlights

* Complete the full `c2` RPI loop (`research`, `plan`, `implement`, `review`) in order, writing dated `2026-11-15` `c2` artifacts under `.copilot-tracking/` (`research`, `plans`, `details`, `reviews/plans`, `changes`, `reviews/logs`, `rpi-sessions`).
* Update `src/core/tests/test_live_provisioning.py` and `src/core/tests/test_device_provision.py` so synthetic secret test inputs are assembled at runtime via concatenation/join with byte-for-byte identical runtime values and `0` matches in `test_iot_credential_hygiene.PATTERNS`.
* Validate under the Focused tier (`src/core` provisioning unit tests, `src/api/tests/test_iot_credential_hygiene.py`, `ruff check`, `ruff format --check`, and `mypy` in `src/core`) and create one frozen clean local commit with `Refs #185` and the Copilot `Co-authored-by` trailer without pushing or running `gh pr create`.

### What You May Not Know

* Two regexes in `src/api/tests/test_iot_credential_hygiene.py` (`"device connection string"` and `"shared access signature"`) use greedy `[^\n]*` on a single source line. Simple `" + "` concatenation that leaves `HostName=...azure-devices.net;` and `SharedAccessKey=` on the same `<100`-character Ruff-formatted line still triggers `"device connection string"` (`test_iot_credential_hygiene.py` only passed its own similar fixture because it passes `skip=Path(__file__).resolve()` to `scan_directory`). Splitting both the marker keywords (`"Host"` + `"Name="`, `"azure-"` + `"devices.net"`, `"SharedAccess"` + `"Key="`, `"SharedAccess"` + `"Signature "`, `"-----BEGIN "` + `"PRIVATE KEY-----"`) and base64 payload halves eliminates both contiguous and single-line bridging matches under any formatter layout.
* Extending `test_source_modules_contain_no_embedded_keys_connection_strings_or_sas_tokens` in `src/core/tests/test_live_provisioning.py` to scan `src/core` synthetic test files alongside synthetic production modules closes the cross-package gap where `src-core` passed in `c1` while `src-api` caught the literal test fixtures.

### Unresolved Decisions or Blockers

* None.

For current user input, see [User Decisions and Requirements](#user-decisions-and-requirements). The planner keeps the synthesized sections below current as evidence and user direction evolve.

## User Decisions and Requirements

* Run the full RPI loop (`research`, `plan`, `implement`, `review`) in order, writing dated `c2` artifacts under `.copilot-tracking/` (`research`, `plans`, `details`, `changes`, `reviews`) for Issue `#185` (`PR #1801` CI failure remediation cycle `c2`) (user prompt).
* Fix `src/core/tests/test_live_provisioning.py` and `src/core/tests/test_device_provision.py` so synthetic secret test inputs are assembled at runtime via string concatenation/join, keeping the runtime strings passed to functions under test identical while literal source files contain `0` matches for `test_iot_credential_hygiene.PATTERNS` (user prompt; `.copilot-tracking/research/2026-11-15/simulated-device-identity-provisioning-185-c2-research.md` `C2`-`C7`).
* Execute Focused validation: run `src/core/tests/test_device_provision.py` and `src/core/tests/test_live_provisioning.py`, run `src/api/tests/test_iot_credential_hygiene.py`, and run `ruff check`, `ruff format --check`, and `mypy` in `src/core` (user prompt; `.copilot-tracking/research/2026-11-15/simulated-device-identity-provisioning-185-c2-research.md` `C8`, `C9`).
* Commit all changes and `.copilot-tracking/` `c2` artifacts locally on `feat/iot-185-device-provisioning` with a Conventional Commit message, `Refs #185`, privacy-safe GitHub noreply email, and `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>`; do NOT push or run `gh pr create` (user prompt; `.github/copilot-instructions.md`).

## Goals

* Eliminate all `3` repository text-scan findings in `test_iot_credential_hygiene.SourceScanTests.test_no_device_key_or_connection_string_in_repository_text` (`0` matches across `src/`, `infra/`, `docs/`, and `.github/`).
* Preserve byte-for-byte identical runtime synthetic secret strings in `test_live_provisioning.py` and `test_device_provision.py` so every negative redaction and refusal branch continues to be exercised with full fidelity.
* Guard `src/core` synthetic test files directly inside `test_live_provisioning.py` against literal credential-hygiene regex matches so standalone `src-core` runs fail immediately on any future literal secret fixture.
* Maintain strict `ruff` (`line-length = 100`, `E,F,I,B,UP`) and `mypy` (`strict = true`) compliance in `src/core` and leave one clean frozen local commit for coordinator review.

## Scope and Non-Goals

### In Scope

* Canonical Python test targets: `src/core/tests/test_live_provisioning.py` and `src/core/tests/test_device_provision.py` (generated targets: `none`; production module edits: `none`).
* Test ownership lock: existing suites `src/core/tests/test_live_provisioning.py` (`12` test methods), `src/core/tests/test_device_provision.py` (`12` test methods), `src/core/tests/test_device_identity.py`, and `src/api/tests/test_iot_credential_hygiene.py` (`12` test methods); exact test removals: `none`; maximum test additions: `1` (extending `test_source_modules_contain_no_embedded_keys_connection_strings_or_sas_tokens` in `src/core/tests/test_live_provisioning.py` with test-source hygiene and runtime fixture-reconstruction assertions while retaining the AST `lp.contains_raw_secret` check on the 3 synthetic production modules, or `0` new methods via focused in-method assertions).
* Focused validation: caller-specified `unittest` invocations for `src/core` and `src/api/tests/test_iot_credential_hygiene.py`, targeted `src/core` synthetic/IoT/boundary `unittest` suite (`80` tests across `test_live_provisioning.py`, `test_device_identity.py`, `test_device_provision.py`, `test_iot_device_identity_schema.py`, `test_synthetic_output_audit.py`, `test_dependency_rule.py`, and `test_live_doc_links.py`), `tools/rename-zava-tests.py`, `ruff check .`, `ruff format --check .`, and bare `mypy` inside `src/core`.
* Complete dated `2026-11-15` `c2` RPI tracking artifacts under `.copilot-tracking/` and a single post-Review local git commit on `feat/iot-185-device-provisioning`.

### Non-Goals

* Modifying `src/api/tests/test_iot_credential_hygiene.py`, `PATTERNS`, `SCANNED`, or any allowlist/skip behavior.
* Modifying `src/core/src/zava_forward/core/synthetic/` production modules (`live_provisioning.py`, `device_identity.py`, `device_provision.py`), `pyproject.toml`, `.github/workflows/src-ci.yml`, SQL, Bicep, `src/api/checks/`, or `src/api/src/zava_forward/api/web/`.
* Running `tools/rpi-checks.py`, amending `ffce28c98`, rebasing, pushing to `origin`, or calling `gh pr create`.

## Functional Requirements

* FR-1: Runtime assembly of synthetic secret test fixtures in `src/core/tests/test_live_provisioning.py` and `src/core/tests/test_device_provision.py`.
  * Observable acceptance criteria: `RAW_KEY_B64`, `RAW_CONN_STR`, `RAW_SAS_TOKEN`, `RAW_PEM` (and both SAS signature substring assertion sites across `test_outputs_and_audit_records_redact_keys_connection_strings_and_sas_tokens` and `test_logger_filter_redacts_percent_formatted_split_extra_and_exception_secrets`) in `src/core/tests/test_live_provisioning.py` and the secret-bearing `credential_owner` input in `src/core/tests/test_device_provision.py` are assembled at runtime from split keyword, domain, and base64 segments; `test_iot_credential_hygiene.SourceScanTests.test_no_device_key_or_connection_string_in_repository_text` passes with `findings == []`.
* FR-2: Standalone `src/core` synthetic test-source credential-hygiene guard.
  * Observable acceptance criteria: `test_source_modules_contain_no_embedded_keys_connection_strings_or_sas_tokens` in `src/core/tests/test_live_provisioning.py` retains the `ast` `lp.contains_raw_secret` literal scan across synthetic production modules (`live_provisioning.py`, `device_identity.py`, `device_provision.py`), adds a raw-text 4-pattern credential-hygiene scan across both those 3 production modules and the 3 synthetic provisioning test files (`test_live_provisioning.py`, `test_device_provision.py`, `test_device_identity.py`), and confirms the runtime-assembled fixtures still trigger `lp.contains_raw_secret(...)`.
* FR-3: Complete dated `c2` RPI artifact set and frozen clean local commit.
  * Observable acceptance criteria: All seven dated `c2` `.copilot-tracking/` artifacts (`research`, `plans`, `details`, `reviews/plans`, `changes`, `reviews/logs`, `rpi-sessions`) are reconciled and committed alongside `src/core/tests/test_live_provisioning.py` and `src/core/tests/test_device_provision.py` in one clean local commit atop `ffce28c98` on `feat/iot-185-device-provisioning` with `Refs #185` and `Co-authored-by` trailer, `git status --short` empty, and remote untouched.

## Non-Functional Requirements

* NFR-1: Byte-for-byte runtime fixture equivalence and negative-test semantic coverage (semantic coverage).
  * Objective threshold or evaluation condition: Runtime SHA-256 digests and lengths of `RAW_KEY_B64`, `RAW_CONN_STR`, `RAW_SAS_TOKEN`, `RAW_PEM`, and the `test_device_provision.py` secret-bearing owner string match their `ffce28c98` runtime values (`100%` equivalence), and `lp.contains_raw_secret(...)` evaluates `True` on each runtime-assembled fixture.
  * Operating condition or verification approach, if needed: Verified via SHA-256 comparison against `ffce28c98` values and unit-test assertions in `test_live_provisioning.py` and `test_device_provision.py`.
  * Observable acceptance criteria: Identical SHA-256 runtime digests and `24/24` passing tests in `test_device_provision.py` + `test_live_provisioning.py`.
* NFR-2: Formatter-resilient source hygiene, strict typing, and lint parity (regression coverage).
  * Objective threshold or evaluation condition: `0` issues in `ruff check .`, `ruff format --check .` (`line-length = 100`), and `mypy` (`strict = true`) inside `src/core`, `12/12` passing tests in `src/api/tests/test_iot_credential_hygiene.py`, and `0` failures across the targeted `src/core` synthetic/IoT/boundary `unittest` suites (`80` tests) and `tools/rename-zava-tests.py` (`25` tests).
  * Operating condition or verification approach, if needed: Run package-scoped `ruff` and `mypy` inside `src/core` plus both caller-listed `unittest` commands and targeted `src/core` synthetic/IoT/boundary suites under ambient `python3`.
  * Observable acceptance criteria: Every check exits `0` with zero warnings or findings.

## Acceptance Criteria

* `PYTHONPATH=src/core/src:src/core/tests python3 -m unittest src/core/tests/test_device_provision.py src/core/tests/test_live_provisioning.py -v` passes all `24` tests (`OK`) with runtime fixture SHA-256 digests unchanged from `ffce28c98`.
* `PYTHONPATH=src/api/src:src/api/tests:src/core/src:src/core/tests:src/agents/src:src/agents/tests python3 -m unittest src/api/tests/test_iot_credential_hygiene.py -v` passes all `12` tests (`OK`), including `test_no_device_key_or_connection_string_in_repository_text`.
* `(cd src/core && python3 -m ruff check . && python3 -m ruff format --check . && python3 -m mypy)` exits `0`, and `(cd src/core && PYTHONPATH=src:tests python3 -m unittest tests/test_live_provisioning.py tests/test_device_identity.py tests/test_device_provision.py tests/test_iot_device_identity_schema.py tests/test_synthetic_output_audit.py tests/test_dependency_rule.py tests/test_live_doc_links.py -q)` exits `0`.
* All seven dated `c2` `.copilot-tracking/` artifacts (`research`, `plans`, `details`, `reviews/plans`, `changes`, `reviews/logs`, `rpi-sessions`) and the 2 modified `src/core/tests/` files are committed locally atop `ffce28c98` on `feat/iot-185-device-provisioning` (`Refs #185`, privacy-safe noreply email, `Co-authored-by` trailer) with `git status --short` clean and no remote push.

## Implementation Context Record

| Context item                     | Current artifact or record                                                                                                         |
|----------------------------------|------------------------------------------------------------------------------------------------------------------------------------|
| Plan                             | .copilot-tracking/plans/2026-11-15/simulated-device-identity-provisioning-185-c2-plan.md                                           |
| Phase details                    | .copilot-tracking/details/2026-11-15/simulated-device-identity-provisioning-185-c2-phase-details.md                                |
| Latest critique                  | .copilot-tracking/reviews/plans/2026-11-15/simulated-device-identity-provisioning-185-c2-plan-critique.md (`Revise` disposition: `PC-001` and `PC-002` applied directly and closed) |
| Relevant research                | .copilot-tracking/research/2026-11-15/simulated-device-identity-provisioning-185-c2-research.md                                    |
| Changes-record role              | .copilot-tracking/changes/2026-11-15/simulated-device-identity-provisioning-185-c2-changes.md is created by implementation         |
| Planning execution and readiness | Complete; Ready for implementation                                                                                                 |
| Continuation context             | Active confirmed automatic RPI Agent parent continues to `Implement` after all planning gates pass                                 |

## Sources

* `.copilot-tracking/research/2026-11-15/simulated-device-identity-provisioning-185-c2-research.md`: Cycle 1 evidence (`C1`-`C9`) reproducing the 3 `test_iot_credential_hygiene` findings and proving the greedy `[^\n]*` single-line regex bridging constraint.
* `src/api/tests/test_iot_credential_hygiene.py`: Repository-wide `PATTERNS` and `SourceScanTests` definitions.
* `src/core/tests/test_live_provisioning.py` and `src/core/tests/test_device_provision.py`: Target negative secret-redaction and secret-refusal unit tests introduced in `ffce28c98`.
* `src/core/pyproject.toml` and `.github/workflows/src-ci.yml`: Package-scoped `ruff` (`line-length = 100`), strict `mypy`, and `unittest` CI configuration.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Runtime Synthetic Secret Assembly and Test-Source Hygiene Guard

* Intent: Replace contiguous literal synthetic secret fixtures in `src/core/tests/test_live_provisioning.py` and `src/core/tests/test_device_provision.py` with formatter-proof runtime assembly while preserving exact runtime string values and adding standalone `src/core` test-source hygiene verification.
* Dependencies: None

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Assemble synthetic secret constants at runtime and guard test sources in `src/core/tests/test_live_provisioning.py`

* Requirement and evidence: FR-1, FR-2, NFR-1, NFR-2 (`C2`, `C3`, `C4`, `C6`, `C7`)
* Expected result: `RAW_KEY_B64`, `RAW_CONN_STR`, `RAW_SAS_TOKEN`, `RAW_PEM`, and both 36-char SAS signature assertion fragments in `src/core/tests/test_live_provisioning.py` are constructed at runtime from split keyword, domain, and base64 segments with identical runtime SHA-256 digests, and `test_source_modules_contain_no_embedded_keys_connection_strings_or_sas_tokens` retains the `ast` `lp.contains_raw_secret` check on the 3 synthetic production modules while verifying zero credential-hygiene regex matches across all 6 synthetic production and test files.
* Detail section: P01-T01 in .copilot-tracking/details/2026-11-15/simulated-device-identity-provisioning-185-c2-phase-details.md

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Assemble the secret-bearing owner test input at runtime in `src/core/tests/test_device_provision.py`

* Requirement and evidence: FR-1, NFR-1, NFR-2 (`C2`, `C3`, `C5`, `C6`, `C7`)
* Expected result: `test_report_refuses_secret_bearing_credential_owner` in `src/core/tests/test_device_provision.py` constructs the secret-bearing owner string at runtime from split `"Owner SharedAccess"`, `"Key="`, and split base64 segments, producing the exact same runtime string and raising `CREDENTIAL_OWNER_SECRET_MATERIAL` with `0` literal source matches.
* Detail section: P01-T02 in .copilot-tracking/details/2026-11-15/simulated-device-identity-provisioning-185-c2-phase-details.md

<!-- rpi:phase id=P02 -->
### [x] P02: Focused Validation, CI Parity Verification, and Local Git Identity Check

* Intent: Prove zero findings in `test_iot_credential_hygiene.py`, full pass across `src/core` unit tests, `ruff`, and `mypy`, runtime fixture digest equivalence against `ffce28c98`, and verified privacy-safe local git identity ahead of post-Review local commit closeout.
* Dependencies: P01

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Run Focused `unittest`, `ruff`, `mypy`, and runtime digest checks and confirm privacy-safe git identity

* Requirement and evidence: FR-3, NFR-1, NFR-2 (`C6`, `C8`, `C9`; `.github/copilot-instructions.md`)
* Expected result: Both caller-specified `unittest` suites (`test_device_provision.py` + `test_live_provisioning.py` and `test_iot_credential_hygiene.py`), targeted `src/core` synthetic/IoT/boundary `unittest` suites (`80` tests) + `tools/rename-zava-tests.py`, `ruff check .`, `ruff format --check .`, and `mypy` in `src/core` all exit `0`; runtime fixture SHA-256 digests match `ffce28c98`; repository-local `user.email` matches `{id}+{login}@users.noreply.github.com` ready for the single post-Review local commit without push.
* Detail section: P02-T01 in .copilot-tracking/details/2026-11-15/simulated-device-identity-provisioning-185-c2-phase-details.md

## Dependencies

* Active Python 3.12 toolchain with `ruff` and `mypy` available (`ruff 0.17.3`, `mypy 2.4.1` verified locally).
* `gh api user` access to verify privacy-safe `{id}+{login}@users.noreply.github.com` repository-local git email before final commit.

## Critique Disposition

Single-pass `rpi-plan-critique` completed (`Complete`) with verdict `Revise` (`0` Critical, `0` High, `1` Medium, `1` Low). Both planner-owned findings were applied directly and closed without repeating critique.

| Critique run and finding | Disposition | Plan response or residual risk |
|--------------------------|-------------|--------------------------------|
| Single-pass critique `PC-001` (`Medium`): per-file test counts transposed as `10` and `14` instead of `12` and `12` | resolved | Corrected `In Scope` in `plan.md` and `P01-T01` / `P01-T02` validation and completion evidence in `phase-details.md` to `12` / `12/12` per file (`24` combined). |
| Single-pass critique `PC-002` (`Low`): preserve `ast` `lp.contains_raw_secret` production scan (`import ast`) and split both 36-char SAS signature fragment assertion sites | resolved | Updated `FR-1`, `FR-2`, `P01-T01`, and `phase-details.md` to explicitly retain the `ast` scan on the 3 synthetic production modules alongside the 6-file 4-pattern credential-hygiene scan and use a shared runtime-assembled `RAW_SAS_SIG_FRAGMENT` constant across both redaction test methods. |
| Residual risk: remote `PR #1801` stays at `ffce28c98` until coordinator push | accepted with risk | Explicit caller `exclude` control forbids pushing from this worktree; frozen local commit leaves clean `10/10`-ready code and `c2` tracking artifacts for coordinator push. |

## Follow-Up Items

* Coordinator push of the frozen local `c2` commit on `feat/iot-185-device-provisioning` to trigger and verify `10/10` passing checks on `PR #1801` (held outside `c2` by the caller no-push boundary).
* Carry-forward `c1` follow-up: Optional `--id-scheme sim-dps` CLI flag in `zava_forward.core.synthetic.device_provision` alongside default `SYN-*` dry-run/apply.
* Carry-forward `c1` follow-up: Optional live Azure DPS enrollment-group adapter behind explicit opt-in extra once authorized by `Platform Engineering / IoT Operations Owner`.
* Carry-forward `c1` follow-up: Tick proven acceptance criteria and close GitHub issue `#185` after parent `PR #1641` and `PR #1801` review and merge.

## Handoff

* Implementation artifact: .copilot-tracking/changes/2026-11-15/simulated-device-identity-provisioning-185-c2-changes.md
* Ready phase or task: P01 (`P01-T01`, `P01-T02`), P02 (`P02-T01`)
* Remaining provisional question or blocker: None

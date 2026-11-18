<!-- markdownlint-disable-file -->
# Implementation Plan: Conformance Closure for Key Vault Secret Lifecycle (#142 Child Loop 4)

## Metadata

* Task ID: issue-142-conformant
* Task slug: kv-secret-lifecycle-142-conformant
* Parent task: issue-142-final (`kv-secret-lifecycle-142-final`)
* Date: 2026-11-15
* Status: Completed
* Validation tier: Focused (`unittest`, `bicep_inventory.py --check`, `ruff check`, `ruff format --check`, `mypy`; do not run `tools/rpi-checks.py --all`)

## Executive Summary

This child plan closes `RV-001`..`RV-006` from `.copilot-tracking/reviews/logs/2026-11-15/kv-secret-lifecycle-142-final-review.md` so Issue #142's Entra client-secret rotation verifier, Key Vault RBAC/data-plane access review pipeline, CLI wrapper, runbook, and unit tests achieve conformant status offline:

1. **Key Vault version-resolution semantics on rollback and switchover (`RV-001`)**: Require version-pinned `priorVersionId` `keyVaultUrl` (`https://<vault>.vault.azure.net/secrets/<secretName>/<priorVersionId>`) for in-place (`priorSecretName.lower() == secretName.lower()`) `rollback` (because Key Vault versionless secret resolution never falls back when the newest version is disabled), allow versionless `rollback` only for two-name staged switchover (`priorSecretName.lower() != secretName.lower()`) when `priorVersionId` is enabled and has strictly the newest `created` timestamp among `secretVersions.entries` on `priorSecretName`, verify `nextVersionId` has strictly the newest `created` timestamp on `secretName` for versionless `post_switchover`/`post_retire`, and align `infra/README.md` step 4.
2. **Event-bound rotation probe windows (`RV-002`)**: Require guarded `created` timestamps (`created`, `createdAt`, or Unix epoch `attributes.created`) on `secretVersions.entries`, guarded `containerApp.switchoverAt` on `post_switchover` and `post_retire` (`>= max(overlapStart + minOverlapMinutes, nextVersionCreated)` and `<= now`), guarded `containerApp.rollbackAt` on `rollback` (`>= priorStart` and `<= now`), and guarded retirement timestamp (`credentials.retiredPriorCredential.retiredAt` or `credentials.priorRetiredAt`, `<= now` and `>= post_switchover.lastSampleAt`) on `post_retire`, and require each stage's `firstSampleAt` to be `>=` its causal event timestamp (`max(overlapStart, nextVersionCreated)` for `dual_secret_overlap`, `switchoverAt` for `post_switchover`, `retiredAt` for `post_retire`, and `rollbackAt` for `rollback`). Also guard all credential/version/revision integer and timestamp parses into structured `problems`.
3. **Pagination truncation rejection (`RV-003`)**: Reject non-empty `nextLink` or `@odata.nextLink` continuation links inside `unwrap_arm_list_envelope` with `SecretLifecycleError` after running `assert_no_secret_material`.
4. **Sanitized diagnostic/problem formatting (`RV-004`)**: Replace raw `{val!r}` interpolation of unvalidated inputs (`healthzStatus`, `anonymousApiStatus`, `signInRedirectStatus`, `authenticatedApiStatus`, invalid `stage`, invalid `decision`/`disposition`, invalid `nextReviewDue`, unknown `signingKeyId`, invalid `inherited_assignments` scope) with sanitized type/status tokens so unlabelled secrets cannot echo into receipts, ledgers, or exceptions.
5. **Finite-number & strict JSON constant guards (`RV-005`)**: Reject non-finite floats (`NaN`, `Infinity`, `-Infinity`) via `math.isfinite` in `assert_no_secret_material`, `_validate_probe_batch`, and `_parse_non_negative_float`, and reject non-standard JSON constants via `parse_constant` in `infra/scripts/secret_lifecycle.py`.
6. **Runbook `--years 1` parity & repo-wide `.copilot-tracking` check (`RV-006`)**: Align `infra/README.md` step 1 to `--years 1` (matching `rotation_plan()`) and verify `grep -rn '\.copilot-tracking' src/ infra/` across tracked and untracked files.

## Sources and Evidence

* `.copilot-tracking/reviews/logs/2026-11-15/kv-secret-lifecycle-142-final-review.md` (`RV-001`..`RV-006`)
* `.copilot-tracking/research/2026-11-15/kv-secret-lifecycle-142-conformant-research.md` (`CE-1`..`CE-6`)
* `src/core/src/zava_forward/core/secret_lifecycle.py`
* `infra/scripts/secret_lifecycle.py`
* `infra/README.md`
* `src/core/tests/test_secret_lifecycle.py` and `infra/tests/test_secret_lifecycle.py`

## User Decisions and Requirements

* Execute the full RPI loop (`rpi-research`, `rpi-plan` with independent critique, `rpi-implement`, `rpi-review`) with dated `2026-11-15` artifacts for Issue #142.
* Document and test Entra client-secret rotation without downtime and without secret exposure.
* Schedule and record Key Vault data-plane access reviews deterministically.
* Validate at the Focused tier (`unittest`, `ruff check`, `ruff format --check`, `mypy`; do not run `tools/rpi-checks.py --all`) and commit cleanly on `feat/infra-142-kv-secret-lifecycle` without pushing or opening a PR.

## Goals

* Match Azure Key Vault's exact versionless vs version-pinned resolution semantics on rollback and switchover (`RV-001`).
* Bind every probe stage's full sample window to its causal rotation event timestamp (`RV-002`).
* Fail closed on paginated ARM/Graph envelopes (`RV-003`), unvalidated string reflection (`RV-004`), and `NaN`/`Infinity` inputs (`RV-005`).
* Keep `infra/README.md` and `rotation_plan()` CLI flags identical and verify zero `.copilot-tracking` strings across all tracked and untracked files in `src/` and `infra/` (`RV-006`).

## Scope and Non-Goals

* **In scope**: `src/core/src/zava_forward/core/secret_lifecycle.py`, `infra/scripts/secret_lifecycle.py`, `infra/README.md`, `src/core/tests/test_secret_lifecycle.py`, and `infra/tests/test_secret_lifecycle.py`.
* **Non-goals**: Modifying Bicep modules, running `tools/rpi-checks.py --all`, performing live Azure mutations, or pushing/opening a PR.

## Functional Requirements

* **FR-C1 (`RV-001` — Version-resolution semantics)**:
  * Require `created` (`created`, `createdAt`, or Unix epoch `attributes.created` on a `Mapping` `attributes`) on `secretVersions.entries`, checking explicit key presence, rejecting `bool`, `<= 0`, non-finite, out-of-range (`OverflowError`/`OSError`/`ValueError`), `> now_utc`, or conflicting timestamps across those fields.
  * In `stage == "rollback"`: when `prior_secret_name.lower() == secret_name.lower()`, require `u_ver == prior_version_id` (reject `u_ver is None`); when `prior_secret_name.lower() != secret_name.lower()`, allow `u_ver == prior_version_id` or (`u_ver is None` only if `prior_version_id` is enabled, no other entry on `prior_secret_name` is enabled, and `prior_version_id` has strictly the greatest `created` timestamp among entries on `prior_secret_name`).
  * In `stage in {"post_switchover", "post_retire"}`: when `u_ver is None`, verify `next_version_id` has strictly the greatest `created` timestamp among entries on `secret_name`.
  * Update `infra/README.md` step 4 to instruct pinning `keyVaultUrl` to `priorVersionId` for in-place rollback (or reverting `entraClientSecretName` to the separate `priorSecretName` in two-name switchover).
* **FR-C2 (`RV-002` — Event-bound probe windows & guarded metadata parsing)**:
  * Guard all credential (`startDateTime`, `endDateTime`, `retiredAt`, `priorRetiredAt`), version (`created`, `expires`), containerApp (`switchoverAt`, `rollbackAt`), and revision (`trafficWeight`, `replicasReady`) parses so malformed/missing/boolean values record structured `problems` rather than raising `KeyError`/`ValueError`/`TypeError`.
  * Require `containerApp.switchoverAt` in `post_switchover` and `post_retire`: enforce `switchover_dt >= next_ver_created_dt`, `switchover_dt <= now_utc`, `switchover_dt >= overlap_start_dt + timedelta(minutes=min_overlap_minutes)` whenever `overlap_start_dt` is known, and `switchover_dt <= rp_end` when `retiredPriorCredential` is present; bind canonical UTC `switchoverAt` (`switchover_dt.isoformat()`) inside `post_switchover`/`post_retire` receipts and their HMAC-SHA256 payload, and verify `parse_time(priorSwitchoverReceipt["switchoverAt"]) == switchover_dt` in `post_retire`.
  * Gate `versionSwitchoverVerified` on `keyVaultUrl` / newest-`created` / `switchoverAt` validity, gate `zeroDowntimeVerified` on stage event-floor checks, and evaluate `containerApp.rollbackAt` (`p_start_dt <= rollback_dt <= now_utc`) + `rollback` probe-floor checks before `pre_rollback_hold_problems = len(problems)` so `rollbackVerified` stays `False` on violation.
  * Require an explicit retirement timestamp in `post_retire` (`credentials.retiredPriorCredential.retiredAt` or `credentials.priorRetiredAt`, matching if both are supplied, `<= now_utc`, `>= switchoverAt`, and `>= post_switchover.lastSampleAt`).
  * Enforce stage probe window floors:
    * `dual_secret_overlap`: `firstSampleAt >= max(overlap_start_dt, next_ver_created_dt)`
    * `post_switchover`: `firstSampleAt >= switchover_dt`
    * `post_retire`: `firstSampleAt >= effective_retired_at`
    * `rollback`: `firstSampleAt >= rollback_dt`
* **FR-C3 (`RV-003` — Pagination rejection)**:
  * `unwrap_arm_list_envelope` runs `assert_no_secret_material` first and then raises `SecretLifecycleError` if `payload.get("nextLink") not in (None, "")` or `payload.get("@odata.nextLink") not in (None, "")`.
* **FR-C4 (`RV-004` — Sanitized problem/exception strings)**:
  * Sanitize HTTP status formatting (`_fmt_http_status`), `healthProbes[].stage` (`VALID_ROTATION_STAGES` check + `"<invalid-stage>"`), `priorKeyId`/`nextKeyId`/`signingKeyId`/verification `key_id`/`review_status` `principalId` (`_KEY_ID_TOKEN_RE` check), `--signing-key-env` (`^[A-Za-z_][A-Za-z0-9_]*$` without echoing rejected/unset values), `prev_entry.vaultName`/`expected_vault_name` (`_VAULT_NAME_RE`), and invalid top-level `stage`/decision/disposition/date/scope messages so unvalidated caller strings are never echoed via `!r`.
* **FR-C5 (`RV-005` — Non-finite float & JSON constant rejection)**:
  * Reject non-finite floats (`not math.isfinite(val)`) in `assert_no_secret_material`, `_validate_probe_batch`, `_parse_non_negative_float`, and `audit_keyvault_data_plane_access` `status_raw` parsing (also rejecting `bool`), and route all four JSON decode sites in `infra/scripts/secret_lifecycle.py` (`load`, `_load_verification_keys`, and both `load_ledger_entries` branches, preserving public `__all__` names) through `_strict_json_loads(..., parse_constant=...)`.
* **FR-C6 (`RV-006` — Runbook `--years 1` & step 3/4 parity + repo-wide `.copilot-tracking` scan)**:
  * Update `infra/README.md` step 1 to use `--years 1` (matching `rotation_plan()`), step 2 to note `containerApp.switchoverAt`, step 3 to require `firstSampleAt >= retiredAt` plus `credentials.priorRetiredAt` and `containerApp.switchoverAt` alongside `priorSwitchoverReceipt`, and step 4 to require pinned `priorVersionId` `keyVaultUrl` (or two-name `priorSecretName`) + `containerApp.rollbackAt`, and verify `grep -rn '\.copilot-tracking' src/ infra/` returns zero matches.

## Non-Functional Requirements

* **NFR-C1**: Zero `.copilot-tracking/` references across all tracked and untracked files under `src/` and `infra/`.
* **NFR-C2**: Full `ruff check`, `ruff format --check`, and `mypy` (`--strict` on `infra`) compliance and zero layer-dependency violations.
* **NFR-C3 (Test ownership & bounds)**:
  * Owners: `src/core/tests/test_secret_lifecycle.py` and `infra/tests/test_secret_lifecycle.py`.
  * Exact removals: `none` (update existing `_rotation_fixture`, `_rotation_payload`, inline `retire_payload` in `test_cli_signing_flags_browser_gate_and_runbook_command_safety`, and rollback test expectations in place for pinned in-place rollback URL + two-name versionless rollback + `switchoverAt`/`rollbackAt`/`priorRetiredAt`/`created`).
  * Maximum additions: up to `6` focused semantic tests (`<= 4` in `src/core/tests/test_secret_lifecycle.py`, `<= 2` in `infra/tests/test_secret_lifecycle.py`).
  * Canonical targets: `src/core/src/zava_forward/core/secret_lifecycle.py`, `infra/scripts/secret_lifecycle.py`, `infra/README.md`; generated targets: `none`.

## Acceptance Criteria

* [x] **AC-C1**: In-place `rollback` rejects versionless `keyVaultUrl` even when `nextVersionId` is disabled and passes when `priorVersionId` is pinned (or in two-name `priorSecretName != secretName` rollback when `priorVersionId` is the newest enabled version on `priorSecretName`), and versionless `post_switchover`/`post_retire` rejects `nextVersionId` older than `priorVersionId` (`RV-001`).
* [x] **AC-C2**: Probe windows preceding `nextVersionCreated`, `switchoverAt`, `retiredAt`, or `rollbackAt` are rejected, and `post_retire` requires `firstSampleAt >= retiredAt` so the full `>= min_probe_span_seconds` window runs post-retirement (`RV-002`).
* [x] **AC-C3**: `unwrap_arm_list_envelope` rejects non-empty `nextLink` and `@odata.nextLink` envelopes (`RV-003`).
* [x] **AC-C4**: Unlabelled canary strings placed in `healthzStatus`, `anonymousApiStatus`, `signInRedirectStatus`, `authenticatedApiStatus`, `stage`, `decision`, `disposition`, or `signingKeyId` never appear in `problems` or error messages (`RV-004`).
* [x] **AC-C5**: Python `float("nan")` / `float("inf")` and CLI JSON `NaN` / `Infinity` inputs are rejected fail-closed (`RV-005`).
* [x] **AC-C6**: `infra/README.md` step 1 matches `rotation_plan()` (`--years 1`), Focused validation passes cleanly, and `grep -rn '\.copilot-tracking' src/ infra/` returns zero matches (`RV-006`).

## Phase Checklist

<!-- P01 -->
- [x] **P01**: Implement conformance fixes in `secret_lifecycle.py`, CLI wrapper, and `infra/README.md` (`FR-C1`..`FR-C6`)
  <!-- P01-T01 -->
  - [x] **P01-T01**: Implement pinned in-place rollback & newest-version checks, event-bound probe floors & guarded parsers, pagination rejection, sanitized problem strings, finite-number/JSON guards, and `infra/README.md` alignment
<!-- P02 -->
- [x] **P02**: Update fixtures, add semantic regression tests, and run Focused validation (`AC-C1`..`AC-C6`)
  <!-- P02-T01 -->
  - [x] **P02-T01**: Update `_rotation_fixture` / `_rotation_payload` and rollback tests, add semantic tests for `RV-001`..`RV-006`, and run Focused validation + repo-wide `.copilot-tracking` check

## Critique Disposition

* Critique artifact: `.copilot-tracking/reviews/plans/2026-11-15/kv-secret-lifecycle-142-conformant-plan-critique.md` (`Verdict: Revise`, 3 planner-owned findings, 0 user decisions required).
* **PC-001 (`Applied`)**: Expanded sanitization (`FR-C4`, `P01-T01`, `P02-T01`) to cover `healthProbes[].stage` (`VALID_ROTATION_STAGES` + `"<invalid-stage>"`), `verification_keys` `key_id` and `priorKeyId`/`nextKeyId`/`review_status` `principalId` (`_KEY_ID_TOKEN_RE`), `--signing-key-env` (`^[A-Za-z_][A-Za-z0-9_]*$` without echoing rejected/unset values), and `prev_entry.vaultName`/`expected_vault_name` (`_VAULT_NAME_RE`).
* **PC-002 (`Applied`)**: Preserved public `load` and `load_ledger_entries` in `infra/scripts/secret_lifecycle.py` (routing all 4 JSON decode sites across `load`, `_load_verification_keys`, and `load_ledger_entries` through `_strict_json_loads`), guarded `status_raw` in `audit_keyvault_data_plane_access` against booleans and non-finite/invalid numeric strings (`"NaN"`, `"Infinity"`), and included `retire_payload["credentials"]["priorRetiredAt"]` in `infra/tests/test_secret_lifecycle.py`.
* **PC-003 (`Applied`)**: Hardened `secretVersions.entries[].created` parsing against booleans, `<= 0`, non-finite/overflow epoch values, future timestamps (`> now_utc`), non-`Mapping` `attributes`, and conflicting `created`/`createdAt`/`attributes.created` fields; added `switchover_dt <= rp_end` and receipt sub-flag gating (`versionSwitchoverVerified`, `zeroDowntimeVerified`, `pre_rollback_hold_problems`); and aligned `infra/README.md` step 3 to require `firstSampleAt >= retiredAt` plus `priorRetiredAt` and `switchoverAt`.

## Follow-Up Items

* Execute live Azure test-environment staged Entra client-secret rotation drill and archive sanitized signed rotation receipt.
* Export live quarterly Log Analytics `AzureDiagnostics` + RBAC snapshot via `rbac-merge` and sign inaugural live access-review ledger entry.

## Handoff

* Changes record target: `.copilot-tracking/changes/2026-11-15/kv-secret-lifecycle-142-conformant-changes.md`.

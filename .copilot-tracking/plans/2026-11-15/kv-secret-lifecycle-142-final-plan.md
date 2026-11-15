<!-- markdownlint-disable-file -->
# Implementation Plan: Final Precision Closure for Key Vault Secret Lifecycle (#142 Child Loop 3)

## Metadata

* Task ID: issue-142-final
* Task slug: kv-secret-lifecycle-142-final
* Parent task: issue-142-seal (`kv-secret-lifecycle-142-seal`)
* Date: 2026-11-15
* Status: Implementation-ready (critique dispositions applied)
* Validation tier: Focused (`unittest`, `bicep_inventory.py --check`, `ruff check`, `ruff format --check`, `mypy`; do not run `tools/rpi-checks.py --all`)

## Executive Summary

This child plan closes the four precision findings (`RV-001`..`RV-004`) recorded in `.copilot-tracking/reviews/logs/2026-11-15/kv-secret-lifecycle-142-seal-review.md` so Issue #142's Entra secret-rotation and Key Vault access-review contracts are conformant offline before local commit:

1. **Authoritative inherited + child-secret RBAC snapshot helper (`RV-001`)**: Add `merge_vault_role_assignments(inherited_assignments, all_assignments, *, vault_resource_id)` in `zava_forward.core.secret_lifecycle` and `rbac-merge` in `infra/scripts/secret_lifecycle.py`, combining `az role assignment list --scope <vault-id> --include-inherited` (which resolves root `/`, management groups, subscription, resource group, and vault directly from ARM) with child-secret assignments (`<vault-id>/secrets/*`) from `az role assignment list --all`, deduplicated deterministically, and update `infra/README.md` to use `rbac-merge`.
2. **Durable rollback secret binding + fresh token exchange (`RV-002`)**: Require `verify_staged_entra_rotation(..., stage="rollback")` to verify fresh OAuth token exchange (`require_fresh_token_exchange=effective_browser_mode`) and prevent Container Apps' 30-minute versionless secret polling from reloading a broken `nextVersionId` by requiring either a `priorVersionId`-pinned `keyVaultUrl`, a distinct reverted `priorSecretName` with no other enabled versions on `priorSecretName`, or `nextVersionId` explicitly present with `enabled: false` (and no other version on `priorSecretName` besides `priorVersionId` enabled) in `secretVersions.entries`.
3. **Bounded-gap, multi-sample probe window coverage (`RV-003`)**: Strengthen `_validate_probe_batch` and `verify_staged_entra_rotation` (`min_probe_samples: int = 3`, `min_probe_span_seconds: int = 60`, `max_probe_gap_seconds: int = 60`, plus CLI flags) to require strict non-boolean integer `totalSamples >= min_probe_samples` and `errorCount == 0`, guarded UTC `firstSampleAt < lastSampleAt <= now`, `(lastSampleAt - firstSampleAt) >= min_probe_span_seconds`, `0 < maxGapSeconds <= max_probe_gap_seconds` with mathematical feasibility `(totalSamples - 1) * maxGapSeconds >= span`, contiguous intra-stage multi-batch handoffs, chronological cross-stage ordering (`prev_stage_end <= next_stage_start`), and `post_retire` sampling after `retiredPriorCredential.retiredAt` (`lastSampleAt > retiredAt`).
4. **Stdout-free `rotation_plan()` step 1 (`RV-004`)**: Update `rotation_plan(vault, app_id)` step 1+2 to stream `--years 1 --query password -o tsv | tr -d '\r\n'` directly into `az keyvault secret set --vault-name {vault} --name entra-client-secret --expires <iso> --file /dev/stdin --output none` and verify the `new version of entra-client-secret` metadata without printing secrets, preserving all ordered invariants tested by `NoDowntimeRotationTests`.

## Sources and Evidence

* `.copilot-tracking/reviews/logs/2026-11-15/kv-secret-lifecycle-142-seal-review.md` (`RV-001`..`RV-004`)
* `.copilot-tracking/research/2026-11-15/kv-secret-lifecycle-142-final-research.md` (`FE-1`..`FE-4`)
* `src/core/src/zava_forward/core/secret_lifecycle.py`
* `infra/scripts/secret_lifecycle.py`
* `infra/README.md`
* `src/core/tests/test_secret_lifecycle.py` and `infra/tests/test_secret_lifecycle.py`

## User Decisions and Requirements

* Complete the full RPI loop (`rpi-research`, `rpi-plan` with independent critique, `rpi-implement`, `rpi-review`) with dated `2026-11-15` artifacts for Issue #142.
* Ensure rotation of the Entra client secret is documented and tested without downtime and without secret exposure.
* Ensure Key Vault data-plane access is reviewed on a schedule and recorded deterministically.
* Validate at the Focused tier (`unittest`, `ruff check`, `ruff format --check`, `mypy`; do not run `tools/rpi-checks.py --all`) and commit cleanly on `feat/infra-142-kv-secret-lifecycle` without pushing or opening a PR.

## Goals

* Eliminate root `/` and management-group omission from RBAC export via a tested `merge_vault_role_assignments` / `rbac-merge` workflow (`RV-001`).
* Guarantee rollback verification proves both durable secret version binding against 30-minute polling and fresh OAuth token exchange (`RV-002`).
* Require continuous multi-sample probe window coverage with bounded intra-stage and inter-stage gaps before certifying zero downtime (`RV-003`).
* Ensure `rotation_plan()` never instructs operators to run a bare password-printing CLI command (`RV-004`).

## Scope and Non-Goals

* **In scope**: `src/core/src/zava_forward/core/secret_lifecycle.py`, `infra/scripts/secret_lifecycle.py`, `infra/README.md`, `src/core/tests/test_secret_lifecycle.py`, and `infra/tests/test_secret_lifecycle.py`.
* **Non-goals**: Modifying Bicep templates, executing `tools/rpi-checks.py --all`, running live Azure mutations, or pushing/opening a PR.

## Functional Requirements

* **FR-F1 (`RV-001` — Inherited + child-secret RBAC snapshot merge)**:
  * `merge_vault_role_assignments(inherited_assignments, all_assignments, *, vault_resource_id)` validates `vault_resource_id` as an ARM `Microsoft.KeyVault/vaults/<vault>` ID, rejects secret material, verifies every entry in `inherited_assignments` classifies as `"vault"` or `"broader_parent"` (`/` / management group / subscription / resource group) for `<vault>`, selects `<vault>` and `<vault>/secrets/<secret>` entries from `all_assignments` using `_classify_arm_kv_scope`, and returns deterministically deduplicated assignment dicts.
  * `infra/scripts/secret_lifecycle.py` adds `rbac-merge --vault-id <id> --inherited <json> --all <json> [--out <json>]`, and `infra/README.md` (`### Access review`, step 1) documents the two `az role assignment list` commands (`--scope <vault-id> --include-inherited` + `--all`) piped through `rbac-merge`.
* **FR-F2 (`RV-002` — Durable rollback secret binding & fresh token exchange)**:
  * In `verify_staged_entra_rotation(..., stage="rollback")`:
    * `_validate_probe_batch` runs with `require_fresh_token_exchange=effective_browser_mode`.
    * When `u_ver is None` (versionless `keyVaultUrl`): if `prior_secret_name.lower() == secret_name.lower()`, `next_version_id` must be explicitly present in `secretVersions.entries` with `enabled: False`; in addition, for any versionless `rollback` URL targeting `prior_secret_name`, no entry in `secretVersions.entries` on `prior_secret_name` other than `prior_version_id` may be `enabled: True`.
* **FR-F3 (`RV-003` — Bounded-gap, multi-sample probe window coverage)**:
  * `verify_staged_entra_rotation` accepts `min_probe_samples: int = 3`, `min_probe_span_seconds: int = 60`, and `max_probe_gap_seconds: int = 60` (validated `>= 2` / `>= 1` / `>= 1`, exposed via `--min-probe-samples`, `--min-probe-span-seconds`, `--max-probe-gap-seconds` on `rotation-verify`).
  * `_validate_probe_batch` requires strict non-boolean `int` `totalSamples >= min_probe_samples` and `errorCount == 0`, guarded timezone-aware ISO-8601 `firstSampleAt` and `lastSampleAt` (recording structured `problems` on invalid/naive strings rather than raising `ValueError`, with `firstSampleAt < lastSampleAt <= now_utc` and `(lastSampleAt - firstSampleAt).total_seconds() >= min_probe_span_seconds`), and non-boolean float/int `0 < maxGapSeconds <= max_probe_gap_seconds` satisfying `(totalSamples - 1) * maxGapSeconds >= span_seconds`.
  * Multiple batches within the same stage must be contiguous (`0 <= (next_start - prev_end).total_seconds() <= max_probe_gap_seconds`); across multi-stage forward verification (`dual_secret_overlap -> post_switchover`, `post_switchover -> post_retire`), consecutive stages must satisfy chronological ordering `prev_stage_end <= next_stage_start` (allowing legitimate multi-hour soak intervals), and in `post_retire` when `retiredPriorCredential.retiredAt` is present, the `post_retire` stage's `lastSampleAt` must satisfy `lastSampleAt > retiredAt`.
* **FR-F4 (`RV-004` — Stdout-free `rotation_plan()` step 1)**:
  * `rotation_plan(vault, app_id)` step 1 streams `az ad app credential reset --id {app_id} --append --display-name container-apps-auth-NEW --years 1 --query password -o tsv | tr -d '\r\n' | az keyvault secret set --vault-name {vault} --name entra-client-secret --expires <iso> --file /dev/stdin --output none`, and step 2 confirms the enabled `new version of entra-client-secret` metadata in `{vault}`, keeping `("--append", "new version of entra-client-secret", "refresh", "confirm /app", "credential delete")` in ascending order.

## Non-Functional Requirements

* **NFR-F1**: Zero `.copilot-tracking/` strings in `src/`, `infra/`, docstrings, comments, or commit message.
* **NFR-F2**: Strict `mypy` and `ruff check` / `ruff format --check` compliance across `src/core` and `infra`, plus pure stdlib layer isolation (`test_dependency_rule.py`).
* **NFR-F3 (Test ownership & bounds)**:
  * Owners: `src/core/tests/test_secret_lifecycle.py` and `infra/tests/test_secret_lifecycle.py`.
  * Exact removals: `none` (update existing `_rotation_fixture` and `_rotation_payload` helpers in place with probe timestamps/gaps and rollback `nextVersionId` disabled + `freshTokenExchangeVerified`).
  * Maximum additions: up to `8` focused semantic test cases (`<= 5` in `src/core/tests/test_secret_lifecycle.py`, `<= 3` in `infra/tests/test_secret_lifecycle.py`).
  * Canonical targets: `src/core/src/zava_forward/core/secret_lifecycle.py`, `infra/scripts/secret_lifecycle.py`, `infra/README.md`; generated targets: `none`.

## Acceptance Criteria

* [x] **AC-F1**: `merge_vault_role_assignments` and `secret_lifecycle.py rbac-merge` preserve root `/`, management-group, subscription, resource-group, vault, and `<vault>/secrets/*` assignments, reject cross-vault `--inherited` rows, and `infra/README.md` documents the `rbac-merge` flow (`RV-001`).
* [x] **AC-F2**: `verify_staged_entra_rotation(..., stage="rollback")` rejects versionless rollback while `nextVersionId` is enabled or omitted from `secretVersions.entries` (or when another version on `priorSecretName` stays enabled) and requires `freshTokenExchangeVerified: true` in browser mode (`RV-002`).
* [x] **AC-F3**: `verify_staged_entra_rotation` rejects single-sample, boolean-typed, short-span, wide-gap, mathematically inconsistent, future-dated, or non-contiguous multi-stage probe batches (`RV-003`).
* [x] **AC-F4**: `rotation_plan(vault, app_id)` emits the stdout-free `tr -d '\r\n' | az keyvault secret set ... --output none` pipeline while preserving all `NoDowntimeRotationTests` assertions (`RV-004`).
* [x] **AC-F5**: Focused validation (`unittest`, `bicep_inventory.py --check`, `ruff check`, `ruff format --check`, `mypy`) passes cleanly.

## Phase Checklist

- [x] **P01**: Implement core helpers, CLI flags/subcommand, and runbook updates (`FR-F1`..`FR-F4`)
  - [x] **P01-T01**: Implement `merge_vault_role_assignments`, rollback durability + fresh token check, bounded-gap probe window validation, stdout-free `rotation_plan`, `rbac-merge` CLI subcommand + probe CLI flags, and `infra/README.md` updates
- [x] **P02**: Update deterministic fixtures, add negative regression tests, and run Focused validation (`AC-F1`..`AC-F5`)
  - [x] **P02-T01**: Update `_rotation_fixture` / `_rotation_payload`, add semantic tests in `src/core/tests/test_secret_lifecycle.py` and `infra/tests/test_secret_lifecycle.py`, and pass Focused validation

## Critique Disposition

* Critique artifact: `.copilot-tracking/reviews/plans/2026-11-15/kv-secret-lifecycle-142-final-plan-critique.md` (`Verdict: Revise`, 4 planner-owned findings, 0 user decisions required).
* **PC-001 (`Applied`)**: Replaced strict `<= max_probe_gap_seconds` inter-stage gap restriction with intra-batch / intra-stage bounded gaps (`0 < maxGapSeconds <= max_probe_gap_seconds` and `(totalSamples - 1) * maxGapSeconds >= span`), chronological cross-stage non-overlap (`prev_stage_end <= next_stage_start`) so multi-hour soak intervals remain valid, and `post_retire` `lastSampleAt > retiredAt` enforcement so pre-deletion probes cannot satisfy `post_retire`.
* **PC-002 (`Applied`)**: Guarded `firstSampleAt` and `lastSampleAt` parsing inside `_validate_probe_batch` so missing, malformed, or naive timestamps append structured `problems` rather than raising uncaught `ValueError`.
* **PC-003 (`Applied`)**: Documented explicit filtering of `"vault"` and `"secret:*"` scopes on the exact ARM `<vault-id>` prefix from `all_assignments` (ignoring non-secret `/keys/*` and `/certificates/*` child scopes and same-named vaults in other resource groups/subscriptions).
* **PC-004 (`Applied`)**: Standardized `--years 1` in `rotation_plan()` step 1 to match `infra/README.md`.

## Follow-Up Items

* Execute live Azure test-environment staged Entra client-secret rotation drill and archive sanitized signed rotation receipt.
* Export live quarterly Log Analytics `AzureDiagnostics` + RBAC snapshot via `rbac-merge` and sign inaugural live access-review ledger entry.

## Handoff

* Changes record target: `.copilot-tracking/changes/2026-11-15/kv-secret-lifecycle-142-final-changes.md`.

<!-- markdownlint-disable-file -->
# Implementation Details: Conformance Closure for Key Vault Secret Lifecycle (#142 Child Loop 4)

## Metadata

* Task ID: issue-142-conformant
* Task slug: kv-secret-lifecycle-142-conformant
* Plan: `.copilot-tracking/plans/2026-11-15/kv-secret-lifecycle-142-conformant-plan.md`
* Research: `.copilot-tracking/research/2026-11-15/kv-secret-lifecycle-142-conformant-research.md`
* Date: 2026-11-15

<!-- P01 -->
## Phase P01: Core, CLI, and Runbook Conformance Fixes

<!-- P01-T01 -->
### Task P01-T01: Implement `FR-C1`..`FR-C6` across core, CLI, and runbook

* **Target files**:
  * `src/core/src/zava_forward/core/secret_lifecycle.py`
  * `infra/scripts/secret_lifecycle.py`
  * `infra/README.md`
* **Key expectations**:
  1. **Non-finite float & strict JSON guards (`FR-C5`)**:
     * In `assert_no_secret_material`: check `if not isinstance(payload, bool) and isinstance(payload, float) and not math.isfinite(payload): raise SecretLifecycleError(f"non-finite numeric value refused at {path}")`.
     * In `_validate_probe_batch` and `_parse_non_negative_float`: verify `math.isfinite(float(val))`.
     * In `audit_keyvault_data_plane_access`: guard `status_raw` parsing against `bool` and non-finite/malformed numeric strings (`"NaN"`, `"Infinity"`, etc.), raising `SecretLifecycleError` on invalid status codes.
     * In `infra/scripts/secret_lifecycle.py`: define `_strict_json_loads(raw_text: str, *, label: str) -> Any` with `parse_constant` raising `SecretLifecycleError(f"{label} contains non-standard JSON numeric constant")`, and route all four JSON decode sites in `load`, `_load_verification_keys`, and `load_ledger_entries` through it while preserving public `__all__` exports (`load`, `load_ledger_entries`).
  2. **Pagination continuation rejection (`FR-C3`)**:
     * In `unwrap_arm_list_envelope`: after running `assert_no_secret_material` on all envelope keys and `value`, inspect `"nextLink"` and `"@odata.nextLink"`; if either is present with a value other than `None` or `""` (including whitespace-only or non-string non-None values; specifically if `payload.get(k) is not None and (not isinstance(payload.get(k), str) or bool(payload[k].strip()) or payload[k] != "")`), raise `SecretLifecycleError(f"{label} is paginated ({link_key} present); export all pages before auditing")`.
  3. **Sanitized diagnostic/problem formatting (`FR-C4`)**:
     * Add `_fmt_http_status(val: Any) -> str` returning `str(val)` only for non-bool `int` in `100..599`, else `"<invalid-status>"`, and use it for `healthzStatus`, `anonymousApiStatus`, `signInRedirectStatus`, and `authenticatedApiStatus`.
     * Validate `batch.get("stage")` in `healthProbes` against `VALID_ROTATION_STAGES` (substituting `"<invalid-stage>"` as `stage_label` and appending an invalid probe stage problem without echoing raw strings).
     * Validate `priorKeyId`/`nextKeyId` in `verify_staged_entra_rotation`, `key_id` in `verify_access_review_ledger` and `_load_verification_keys`, and `principalId` in `review_status` against `_KEY_ID_TOKEN_RE` before formatting (substituting `"<invalid-key-id>"` / `"<invalid-principal>"`).
     * Validate `--signing-key-env` against `^[A-Za-z_][A-Za-z0-9_]*$` without echoing rejected or unset values.
     * Validate `prev_entry.vaultName` and `expected_vault_name` against `_VAULT_NAME_RE` (`"<invalid-vault>"`) before formatting, and replace unvalidated top-level `{stage!r}`, `{row.get('decision')!r}`, `{due_str!r}`, `{dec_val!r}`, `{disp_val!r}`, `{due_raw!r}`, `{dec!r}`, `{disp!r}`, `{key_id!r}`, and `{raw_scope!r}` interpolations on error branches with fixed sanitized descriptions.
  4. **Version-resolution semantics (`FR-C1`)**:
     * Parse required `created` timestamp on each `secretVersions.entries[i]` across explicit presence of `"created"`, `"createdAt"`, and `Mapping`-guarded `attributes["created"]`: reject `bool`, `<= 0`, non-finite, out-of-range (`OverflowError`/`OSError`/`ValueError`), future (`> now_utc`), non-`Mapping` `attributes`, or conflicting timestamps across those fields, recording structured `problems`.
     * In `post_switchover` and `post_retire`, when `u_ver is None`, verify `next_version_id` has strictly the greatest `created` timestamp among all `secretVersions.entries` targeting `secret_name`.
     * In `rollback`: if `prior_secret_name.lower() == secret_name.lower()`, reject `u_ver is None` and require `u_ver == prior_version_id`; if `prior_secret_name.lower() != secret_name.lower()`, allow `u_ver == prior_version_id` or (`u_ver is None` only when `prior_version_id` is enabled, no other version on `prior_secret_name` is enabled, and `prior_version_id` has strictly the greatest `created` timestamp among entries targeting `prior_secret_name`).
  5. **Event-bound probe windows & guarded metadata parsing (`FR-C2`)**:
     * Guard all credential `startDateTime`/`endDateTime`/`retiredAt`/`priorRetiredAt`, version `expires`, containerApp `switchoverAt`/`rollbackAt`, and revision `trafficWeight`/`replicasReady` parses into structured `problems`.
     * Require `containerApp.switchoverAt` on `post_switchover` and `post_retire` (including canonical UTC `switchover_dt.isoformat()` in the rotation receipt and its HMAC-SHA256 canonical payload when present), verifying:
       * `switchover_dt <= now_utc`
       * `switchover_dt >= next_ver_created_dt` (when `next_ver_created_dt` is valid)
       * `switchover_dt >= overlap_start_dt + timedelta(minutes=min_overlap_minutes)` whenever `overlap_start_dt` is known
       * `switchover_dt <= rp_end` when `retiredPriorCredential` is present in `post_retire`
       * in `post_retire` with `priorSwitchoverReceipt`: `parse_time(priorSwitchoverReceipt["switchoverAt"]) == switchover_dt`
     * Require `containerApp.rollbackAt` on `rollback` (`p_start_dt <= rollback_dt <= now_utc`).
     * Require `effective_retired_at` on `post_retire` from `credentials.retiredPriorCredential.retiredAt` and/or `credentials.priorRetiredAt` (requiring equality if both are supplied, `effective_retired_at <= now_utc`, `effective_retired_at >= switchover_dt`, and `effective_retired_at >= post_switchover.lastSampleAt`).
     * Enforce stage probe window floors (`dual_secret_overlap`: `firstSampleAt >= max(overlap_start_dt, next_ver_created_dt)`; `post_switchover`: `firstSampleAt >= switchover_dt`; `post_retire`: `firstSampleAt >= effective_retired_at`; `rollback`: `firstSampleAt >= rollback_dt`), gate `versionSwitchoverVerified` on `keyVaultUrl` / newest-`created` / `switchoverAt` validity, gate `zeroDowntimeVerified` on stage event-floor checks, and evaluate `rollbackAt` + `rollback` probe-floor checks before `pre_rollback_hold_problems = len(problems)`.
  6. **Runbook alignment (`FR-C6`)**:
     * Update `infra/README.md` (`### Rotate the Entra client secret`, steps 1..4) to use `--years 1` (matching `rotation_plan()`), document `containerApp.switchoverAt` in step 2, require `firstSampleAt >= retiredAt` plus `credentials.priorRetiredAt` and `containerApp.switchoverAt` alongside `priorSwitchoverReceipt` in step 3, and require pinned `priorVersionId` `keyVaultUrl` (or two-name `priorSecretName`) + `containerApp.rollbackAt` in step 4.

<!-- P02 -->
## Phase P02: Fixtures, Semantic Regression Tests, and Focused Validation

<!-- P02-T01 -->
### Task P02-T01: Update fixtures, add regression tests (`AC-C1`..`AC-C6`), and run Focused validation

* **Target files**:
  * `src/core/tests/test_secret_lifecycle.py`
  * `infra/tests/test_secret_lifecycle.py`
* **Completion evidence**:
  * Update `_rotation_fixture`, `_rotation_payload`, and inline `retire_payload` (`retire_payload["credentials"]["priorRetiredAt"] = "2026-10-16T00:25:00Z"`) with `created` on `secretVersions.entries`, `switchoverAt` / `rollbackAt` on `containerApp`, pinned `priorVersionId` `keyVaultUrl` on default in-place `rollback`, and `priorRetiredAt` + `firstSampleAt >= retiredAt` on `post_retire`.
  * Add `<= 4` semantic tests in `src/core/tests/test_secret_lifecycle.py` and `<= 2` in `infra/tests/test_secret_lifecycle.py` proving:
    1. In-place versionless `rollback` is rejected even when `nextVersionId` is disabled, pinned `priorVersionId` `rollback` and two-name `priorSecretName != secretName` versionless `rollback` succeed, and versionless `post_switchover` rejects `nextVersionId` older than `priorVersionId` (`AC-C1`).
    2. Probe windows starting before `nextVersionCreated`, `switchoverAt`, `retiredAt`, or `rollbackAt` (or tampered `priorSwitchoverReceipt.switchoverAt` or `switchoverAt > rp_end`) are rejected (`AC-C2`).
    3. `unwrap_arm_list_envelope` rejects `nextLink` and `@odata.nextLink` (`AC-C3`).
    4. Unlabelled canary strings in `healthzStatus`, `anonymousApiStatus`, `signInRedirectStatus`, `authenticatedApiStatus`, top-level `stage`, `healthProbes[].stage`, `priorKeyId`/`nextKeyId`, `decision`, `disposition`, `signingKeyId`, and `verification_keys` `key_id` never echo in `problems` or exceptions, and `float("nan")` / `float("inf")` / diagnostic `"NaN"` status values are refused (`AC-C4`, `AC-C5`).
    5. CLI rejects JSON `NaN`/`Infinity`, `--signing-key-env` canary reflection, and paginated `roles-inherited.json` (`nextLink`), and `infra/README.md` matches `rotation_plan()` (`--years 1`) (`AC-C3`, `AC-C4`, `AC-C5`, `AC-C6`).
  * Focused validation (`unittest`, `bicep_inventory.py --check`, `ruff check`, `ruff format --check`, `mypy`) and `grep -rn '\.copilot-tracking' src/ infra/` pass cleanly.

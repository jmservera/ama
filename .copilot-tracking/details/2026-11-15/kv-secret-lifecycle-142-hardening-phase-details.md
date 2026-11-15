<!-- markdownlint-disable-file -->
# RPI Phase Details: Verification Hardening for Key Vault Secret Lifecycle (#142 Child Loop)

## Metadata

* Task ID: issue-142-hardening
* Task slug: kv-secret-lifecycle-142-hardening
* Plan: .copilot-tracking/plans/2026-11-15/kv-secret-lifecycle-142-hardening-plan.md
* Research: .copilot-tracking/research/2026-11-15/kv-secret-lifecycle-142-hardening-research.md

<!-- rpi:phase id=P01 -->
## P01: Harden domain verifiers, CLI ledger append guard, and operator documentation

### P01 Direction and Context

Tighten validation boundaries in `src/core/src/zava_forward/core/secret_lifecycle.py` and `infra/scripts/secret_lifecycle.py` so adversarial or incomplete evidence cannot bypass `rotation-verify`, `access-audit`, `review-sign`, or `ledger-verify`.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Implement `RV-001`..`RV-005` hardening in `secret_lifecycle.py` (core + CLI) and `infra/README.md`

* Target files:
  * `src/core/src/zava_forward/core/secret_lifecycle.py`
  * `infra/scripts/secret_lifecycle.py`
  * `infra/README.md`
* Evidence-backed contracts:
  * `RV-001` (`PC-002`): Normalize `window_start`/`window_end` to `dt.UTC` in `audit_keyvault_data_plane_access`, deduplicate emitted anomalies by `anomalyId` and deduplicate identical `(principalId, principalType, roleDefinitionName, scope)` RBAC tuples, extract `_compute_audit_digest(vault_name, window_start, window_end, rbac_assignments, caller_summaries, anomalies, system_notification_count)`, and verify in `create_signed_access_review_record` that `rbacAssignments`, `callerSummaries`, and `anomalies` are lists of mappings with unique `assignmentId`/`anomalyId`, `systemNotificationCount` is a non-boolean `int >= 0`, and `audit["auditDigest"]` equals the recomputed digest.
  * `RV-002` (`PC-002`): Populate `allowedRoles: list[str]` per identity in `default_expected_caller_policy` from `infra/role-assignments.json`. In `audit_keyvault_data_plane_access`, if a mapped non-forbidden principal holds a data-plane RBAC role (`access in {"read", "write", "admin"}`) not in `caller_rule["allowedRoles"]`, emit anomaly `excess_rbac_privilege`. For each in-window diagnostic row, evaluate vault scope BEFORE `PLATFORM_NOTIFICATION_OPS` skipping: require at least one non-empty vault-identifying field among `id_s`, `requestUri_s`, `ResourceId`, `_ResourceId`, `resourceId`, verify every present URI parses as `https://<vault_name>.vault.azure.net/...` and every present ARM resource ID parses as `.../providers/Microsoft.KeyVault/vaults/<vault_name>(/...)` case-insensitively, and on mismatch emit deduplicated `wrong_vault_diagnostic` and skip attributing the foreign event as clean target-vault traffic.
  * `RV-003` (`PC-001`, `PC-003`): In `verify_staged_entra_rotation`:
    * Validate `browserMode` (if present in `evidence`) is a `bool`.
    * Compute `elapsedOverlapMinutes = _compute_overlap_minutes(p_start, min(p_end, now), n_start, min(n_end, now))` during `dual_secret_overlap` and `post_switchover`; in `post_switchover`, append a `problems` message whenever `elapsedOverlapMinutes < float(min_overlap_minutes)` and gate `overlap_ok` on both configured and elapsed overlap.
    * Set `before_kv_problems = len(problems)` BEFORE iterating `secretVersions.entries`, reject non-mapping or duplicate-version rows, require every `secretVersions.entries` item to include a non-empty versioned `id` URI (`v_host`, `v_sec`, `v_ver` all non-None, `v_host == vault_name.lower()`), reject any mismatch between `row["secretName"]` (if provided) and `v_sec`, and compare `v_sec` directly against `prior_secret_name` / `secret_name`.
    * In `post_retire`, enforce `retired_at <= now` on `retiredPriorCredential` (capping overlap at `min(rp_end, retired_at, now)` and `min(n_end, retired_at, now)`), and validate `priorSwitchoverReceipt` AFTER `prior_version_id` and `next_version_id` are parsed against all eight binding fields (`vaultName`, `appId`, `secretName`, `priorSecretName`, `priorKeyId`, `nextKeyId`, `priorVersionId`, `nextVersionId`) plus `stage == "post_switchover"`, `ok is True`, `safeToRetirePriorCredential is True`, `overlapMinutes >= min_overlap_minutes`, `elapsedOverlapMinutes >= min_overlap_minutes`, and valid 64-hex `evidenceDigest`.
    * Add `require_fresh_token_exchange: bool = False` on `_validate_probe_batch` (enabled for `browser_mode and p_stage in {"post_switchover", "post_retire"}`, keeping `rollback` compatible with session recovery probes) requiring `probe.get("freshTokenExchangeVerified") is True` alongside `authenticatedApiStatus == 200`.
    * Include `elapsedOverlapMinutes`, `appId`, `priorSecretName`, `priorKeyId`, `nextKeyId`, `priorVersionId`, and `nextVersionId` in the returned receipt dict.
  * `RV-004` (`PC-003`): Guard `reviewer` in `access_review` (preserving short legacy `"R"` acceptance), `vault` and `app_id` in `rotation_plan`, `reviewer` in `validate_human_reviewer`, and `vault_name` / `expected_vault_name` scalars with `assert_no_secret_material`. Enforce `windowStart < windowEnd <= reviewedAt` and `(reviewedAt - windowEnd) <= dt.timedelta(days=review_interval_days)` in `create_signed_access_review_record`, and in `verify_access_review_ledger` safely validate `isinstance(interval_raw, int) and not isinstance(interval_raw, bool) and 1 <= interval_raw <= max_interval_days`, guard cross-field timestamp checks when individual timestamps fail `parse_time`, and enforce `windowStart < windowEnd <= reviewedAt <= now`, `(reviewedAt - windowEnd) <= dt.timedelta(days=max_interval_days)`, and `nextReviewDue == (reviewed_at.astimezone(dt.UTC) + dt.timedelta(days=interval_raw)).date().isoformat()`.
  * `RV-005` (`PC-003`): In `infra/scripts/secret_lifecycle.py` (`main()` `review-sign` branch before `load_ledger_entries` and inside `_append_jsonl_entry`), if `--ledger` exists and its stripped text starts with `[`, raise `SecretLifecycleError("--ledger must be JSONL (.jsonl) for append; JSON array ledgers are read-only")` (`exit 2`), and if an existing non-empty JSONL file lacks a trailing `\n`, prepend `\n` before writing the new JSONL record.
  * Update `infra/README.md` step 2 under `### Rotate the Entra client secret` to document at least 60 minutes of elapsed dual-secret overlap and `freshTokenExchangeVerified: true`.

<!-- rpi:phase id=P02 -->
## P02: Add negative regression tests and run Focused validation

### P02 Direction and Context

Update existing positive fixtures (`freshTokenExchangeVerified: True`) and add explicit negative assertions for every `RV-001`..`RV-005` vector, then execute the Focused validation suite.

<!-- rpi:task id=P02-T01 -->
### P02-T01: Extend `src/core/tests/test_secret_lifecycle.py` and `infra/tests/test_secret_lifecycle.py` and execute Focused validation

* Target files:
  * `src/core/tests/test_secret_lifecycle.py`
  * `infra/tests/test_secret_lifecycle.py`
* Test ownership & lock:
  * Exact removals: `none` (all 19 original infra tests and all 21 prior lifecycle tests preserved; update positive `post_switchover`/`post_retire` probes in both `_rotation_fixture` in `src/core/tests/test_secret_lifecycle.py` and `_rotation_payload` in `infra/tests/test_secret_lifecycle.py` to include `freshTokenExchangeVerified: True` while preserving `rollback` probe fixtures).
  * Bounded additions: focused negative assertions/methods covering tampered `audit` with stale `auditDigest`, duplicate `assignmentId`/`anomalyId`, `excess_rbac_privilege`, multi-row deduplicated `wrong_vault_diagnostic` -> `create_signed_access_review_record` signability, 1-second elapsed overlap `ok=False` refusal at `post_switchover`, future `retiredAt` refusal at `post_retire`, missing `freshTokenExchangeVerified`, missing/conflicting version URI (`versionSwitchoverVerified=False`), cross-rotation `priorSwitchoverReceipt` rejection, scalar canary refusal in `access_review`/`rotation_plan`/`validate_human_reviewer`, future `reviewedAt` / forged `nextReviewDue` / stale `windowEnd` / boolean `reviewIntervalDays`, and JSON-array `--ledger` append refusal + newline-less JSONL append framing.
* Completion expectations: Focused validation (`unittest`, `bicep_inventory.py --check`, `mypy`, `ruff check`, `ruff format --check`) exits `0`.

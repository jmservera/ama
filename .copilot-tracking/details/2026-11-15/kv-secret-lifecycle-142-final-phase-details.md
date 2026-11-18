<!-- markdownlint-disable-file -->
# Phase Details: Final Precision Closure for Key Vault Secret Lifecycle (#142 Child Loop 3)

## Metadata

* Task ID: issue-142-final
* Task slug: kv-secret-lifecycle-142-final
* Plan path: `.copilot-tracking/plans/2026-11-15/kv-secret-lifecycle-142-final-plan.md`
* Research path: `.copilot-tracking/research/2026-11-15/kv-secret-lifecycle-142-final-research.md`
* Date: 2026-11-15

## P01: Implement core helpers, CLI flags/subcommand, and runbook updates

### P01-T01: Core, CLI, and runbook precision closure

* **Targets**:
  * `src/core/src/zava_forward/core/secret_lifecycle.py`
  * `infra/scripts/secret_lifecycle.py`
  * `infra/README.md`
* **Implementation specifications**:
  1. **`merge_vault_role_assignments` (`FR-F1`)**:
     * Validate `vault_resource_id` matches `^/subscriptions/[^/\s]+/resourceGroups/[^/\s]+/providers/Microsoft\.KeyVault/vaults/([A-Za-z0-9-]{3,24})/?$` (`re.IGNORECASE`) and extract `expected_vault_lower` plus normalized subscription and resource-group prefixes (`expected_sub_lower`, `expected_rg_lower`).
     * Call `assert_no_secret_material` on `inherited_assignments`, `all_assignments`, and `vault_resource_id`. Verify `inherited_assignments` and `all_assignments` are non-string sequences of mappings.
     * For every row in `inherited_assignments`: classify `row.get("scope")` via `_classify_arm_kv_scope(scope, expected_vault_lower)`. Require classification in `{"vault", "broader_parent"}`; additionally, if `scope` starts with `/subscriptions/` (case-insensitive), verify it equals `expected_sub_lower` or `expected_rg_lower` (or the vault path) so an inherited dump from a different subscription/RG is rejected with `SecretLifecycleError`.
     * For every row in `all_assignments`: classify `row.get("scope")` via `_classify_arm_kv_scope(scope, expected_vault_lower)`. Include rows whose classification is `"vault"` or starts with `"secret:"` AND whose subscription + resource-group prefix matches `vault_resource_id` case-insensitively! (Rejecting a same-named vault in a different resource group/subscription if ever encountered.)
     * Deduplicate deterministically preserving order using `str(row.get("id") or "").strip().lower() or _sha256_canonical(row)`.
     * Export `merge_vault_role_assignments` in `src/core/src/zava_forward/core/secret_lifecycle.py` and `infra/scripts/secret_lifecycle.py`, and add CLI subcommand `rbac-merge --vault-id <arm-id> --inherited <path> --all <path> [--out <path>]`.
  2. **Durable `rollback` secret binding & fresh token exchange (`FR-F2`)**:
     * Track `ver_secret_by_id: dict[str, str]` alongside `ver_enabled_by_id` when parsing `secretVersions.entries` (`v_sec.lower()`).
     * In `stage == "rollback"`, when `u_vault == vault_name.lower()` and `u_sec is not None` and `u_sec.lower() == prior_secret_name.lower()`:
       * If `u_ver is None`:
         * When `prior_secret_name.lower() == secret_name.lower()`, require `next_version_id in ver_enabled_by_id and ver_enabled_by_id[next_version_id] is False`; otherwise append `"rollback with versionless in-place keyVaultUrl requires nextVersionId confirmed disabled in secretVersions.entries or pinning priorVersionId"`.
         * For all versionless `rollback` URLs targeting `prior_secret_name`, check if any other version `vid != prior_version_id` with `ver_secret_by_id.get(vid) == prior_secret_name.lower()` has `ver_enabled_by_id.get(vid) is True`; if so, append `"rollback with versionless keyVaultUrl cannot leave another version enabled on priorSecretName"`.
     * In `stage == "rollback"` probe loop, pass `require_fresh_token_exchange=effective_browser_mode` to `_validate_probe_batch`.
  3. **Bounded-gap, multi-sample probe window coverage (`FR-F3`)**:
     * Add keyword arguments `min_probe_samples: int = 3`, `min_probe_span_seconds: int = 60`, `max_probe_gap_seconds: int = 60` to `verify_staged_entra_rotation` (raising `SecretLifecycleError` if non-bool `int` bounds `min_probe_samples < 2`, `min_probe_span_seconds < 1`, or `max_probe_gap_seconds < 1` are violated).
     * Update `_validate_probe_batch` to accept `now_utc`, `min_probe_samples`, `min_probe_span_seconds`, `max_probe_gap_seconds` and return `(issues, batch_start, batch_end)`:
       * Reject boolean or non-`int` `totalSamples` or `errorCount`; require `totalSamples >= min_probe_samples` and `errorCount == 0`.
       * Parse `firstSampleAt` and `lastSampleAt` through a guarded helper catching `(ValueError, TypeError)` so missing, non-string, naive, or invalid ISO-8601 timestamps append structured `probe[<stage>]: ...` messages to `issues` rather than raising uncaught `ValueError`; require `first_dt < last_dt <= now_utc` and `span_s = (last_dt - first_dt).total_seconds() >= float(min_probe_span_seconds)`.
       * Require non-boolean `int | float` `maxGapSeconds` with `0.0 < max_gap <= float(max_probe_gap_seconds)` and `(total_samples - 1) * max_gap + 1e-6 >= span_s`.
     * For each stage with multiple batches in `probes_by_stage[req_stage]`, sort valid batch windows by `firstSampleAt`, verify consecutive batches within the stage have `0.0 <= (next_start - prev_end).total_seconds() <= float(max_probe_gap_seconds)`, and record `(stage_first_start, stage_last_end)`.
     * Across `required_probe_stages[stage]` (`dual_secret_overlap -> post_switchover`, `post_switchover -> post_retire`), verify consecutive stages satisfy chronological ordering `prev_stage_end <= next_stage_start` (allowing legitimate multi-hour soak intervals), and when `stage == "post_retire"` and a valid `retiredAt` was parsed from `retiredPriorCredential`, require `post_retire` `stage_last_end > retired_at`.
     * Expose `--min-probe-samples`, `--min-probe-span-seconds`, `--max-probe-gap-seconds` on `infra/scripts/secret_lifecycle.py rotation-verify`.
  4. **Stdout-free `rotation_plan` (`FR-F4`) & `infra/README.md` alignment**:
     * Update `rotation_plan(vault, app_id)` step 1+2 so step 1 pipes `--query password -o tsv | tr -d '\r\n' | az keyvault secret set --vault-name {vault} --name entra-client-secret --expires <iso> --file /dev/stdin --output none` and step 2 confirms the `new version of entra-client-secret` metadata in `{vault}` without printing secret values.
     * Update `infra/README.md` (`### Rotate the Entra client secret` probe schema note for `firstSampleAt`/`lastSampleAt`/`maxGapSeconds` and rollback version-disable/pin rule, and `### Access review` step 1 using `--scope <vault-id> --include-inherited` + `--all` + `rbac-merge`).
* **Completion expectation**: All 4 findings resolved cleanly with strict typing.

## P02: Update deterministic fixtures, add negative regression tests, and run Focused validation

### P02-T01: Unit/CLI regression coverage and Focused validation

* **Targets**:
  * `src/core/tests/test_secret_lifecycle.py`
  * `infra/tests/test_secret_lifecycle.py`
* **Test scenarios**:
  * Update `_rotation_fixture` and `_rotation_payload` with contiguous probe `firstSampleAt`, `lastSampleAt`, and `maxGapSeconds`, plus rollback `nextVersionId` `enabled: False` and `freshTokenExchangeVerified: True`.
  * Add semantic tests covering:
    1. `merge_vault_role_assignments` preserving root `/`, management-group `/providers/Microsoft.Management/managementGroups/mg-zava`, subscription, RG, vault, and `<vault>/secrets/entra-client-secret` while rejecting wrong-subscription `--inherited` inputs and ignoring other vaults (`RV-001`).
    2. CLI `rbac-merge` end-to-end feeding `access-review` (`RV-001`).
    3. Versionless `rollback` failing when `nextVersionId` remains `enabled: True` or is omitted from `secretVersions.entries`, or when `freshTokenExchangeVerified` is `False`, and passing when `nextVersionId` is `enabled: False` or `keyVaultUrl` pins `priorVersionId` (`RV-002`).
    4. Probe batch rejections for `totalSamples < min_probe_samples`, short span, wide `maxGapSeconds`, impossible `(totalSamples - 1) * maxGapSeconds < span`, future `lastSampleAt`, and inter-stage blind gap `> max_probe_gap_seconds` (`RV-003`).
    5. `rotation_plan()` asserting stdout-free `--query password -o tsv`, `tr -d`, `--file /dev/stdin`, and `--output none` in `plan[0]` alongside existing `NoDowntimeRotationTests` ordering checks (`RV-004`).
* **Validation commands**:
  * `PYTHONPATH=src/core/src python3 -m unittest src/core/tests/test_secret_lifecycle.py src/core/tests/test_dependency_rule.py infra/tests/test_secret_lifecycle.py -v`
  * `PYTHONPATH=src/core/src python3 infra/scripts/bicep_inventory.py --check`
  * `cd src/core && python3 -m ruff check && python3 -m ruff format --check && python3 -m mypy`
  * `python3 -m ruff check --isolated --line-length 100 infra/scripts/secret_lifecycle.py infra/tests/test_secret_lifecycle.py && python3 -m ruff format --isolated --line-length 100 --check infra/scripts/secret_lifecycle.py infra/tests/test_secret_lifecycle.py && MYPYPATH=src/core/src python3 -m mypy --strict --explicit-package-bases infra/scripts/secret_lifecycle.py infra/tests/test_secret_lifecycle.py`

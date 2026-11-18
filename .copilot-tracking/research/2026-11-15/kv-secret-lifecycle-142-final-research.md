<!-- markdownlint-disable-file -->
# Research: Final Precision Closure for Key Vault Secret Lifecycle (#142 Child Loop 3)

## Metadata

* Task ID: issue-142-final
* Task slug: kv-secret-lifecycle-142-final
* Parent task: issue-142-seal (`kv-secret-lifecycle-142-seal`)
* Date: 2026-11-15
* Research disposition: reused
* Planning Readiness: Ready

## Reused Evidence Summary

All evidence required to resolve `RV-001`..`RV-004` from `.copilot-tracking/reviews/logs/2026-11-15/kv-secret-lifecycle-142-seal-review.md` is verified directly in the current worktree:

* **FE-1 (`RV-001` - Inherited ancestor + child-secret RBAC export)**:
  * `az role assignment list --scope <vault-id> --include-inherited -o json` returns Azure's authoritative set of assignments on the vault and all ARM ancestors (root `/`, management groups `/providers/Microsoft.Management/managementGroups/*`, subscription, and resource group), while `az role assignment list --all -o json` includes child-secret assignments under `<vault-id>/secrets/*`.
  * Providing a first-class pure helper `merge_and_filter_vault_role_assignments(inherited_vault_assignments, all_assignments, vault_resource_id)` in `zava_forward.core.secret_lifecycle` (exposed as CLI subcommand `rbac-filter --vault-id <vault-id> --inherited <file> --all <file> --out roles.json`) eliminates brittle shell one-liners, preserves root `/` and management-group ancestors from `--include-inherited`, attaches child `<vault-id>/secrets/*` assignments from `--all`, deduplicates deterministically, and is 100% unit-testable offline!
* **FE-2 (`RV-002` - Durable rollback secret binding & fresh OAuth token exchange)**:
  * In `verify_staged_entra_rotation` (`stage == "rollback"`), when `containerApp.secrets[*].keyVaultUrl` is versionless (`u_ver is None`) and `secretName.lower() == priorSecretName.lower()`, Container Apps' 30-minute versionless secret polling will re-pull `nextVersionId` if `nextVersionId` remains `enabled: True` in Key Vault. Rollback must therefore require either `u_ver == prior_version_id` (version-pinned URL), `prior_secret_name.lower() != secret_name.lower()` (reverted secret name), or `nextVersionId` confirmed `enabled: False` in `secretVersions.entries`, AND `rollback` health probes must pass `require_fresh_token_exchange=effective_browser_mode`.
* **FE-3 (`RV-003` - Bounded-gap, multi-sample probe window coverage)**:
  * `_validate_probe_batch` in `src/core/src/zava_forward/core/secret_lifecycle.py` currently accepts `totalSamples >= 1` with no time-span or sampling-gap bounds. Enforcing strict non-boolean integer `totalSamples >= min_probe_samples` (default `3`), `errorCount == 0`, `firstSampleAt` and `lastSampleAt` UTC timestamps (`firstSampleAt < lastSampleAt <= now_utc`, `(lastSampleAt - firstSampleAt).total_seconds() >= min_probe_span_seconds` default `60`), and non-boolean numeric `0 < maxGapSeconds <= max_probe_gap_seconds` (default `30`) guarantees multi-sample continuous coverage across the probe window without blind spots.
* **FE-4 (`RV-004` - Stdout-free `rotation_plan()` step 1)**:
  * `NoDowntimeRotationTests` in `infra/tests/test_secret_lifecycle.py` asserts `"--append" in plan[0]` and strict ascending substring order `("--append", "new version of entra-client-secret", "refresh", "confirm /app", "credential delete")` across `"\n".join(rotation_plan("kv", "app"))`.
  * Updating `rotation_plan(vault, app_id)` step 1+2 so step 1 streams `az ad app credential reset --id {app_id} --append --display-name container-apps-auth-NEW --end-date <iso> --query password -o tsv | tr -d '\r\n' | az keyvault secret set --vault-name {vault} --name entra-client-secret --expires <iso> --file /dev/stdin --output none` and step 2 confirms the `new version of entra-client-secret` metadata in `{vault}` (without printing secret values) eliminates password exposure on stdout while preserving every `NoDowntimeRotationTests` invariant.

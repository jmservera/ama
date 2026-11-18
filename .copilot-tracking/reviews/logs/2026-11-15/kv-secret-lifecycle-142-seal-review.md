<!-- markdownlint-disable-file -->
# Review Log: Verification Seal for Key Vault Secret Lifecycle (#142 Child Loop 2)

## Metadata

* Task ID: issue-142-seal
* Task slug: kv-secret-lifecycle-142-seal
* Date: 2026-11-15
* Execution status: Complete
* Outcome: Defects found

## Compared Artifacts

* Plan: `.copilot-tracking/plans/2026-11-15/kv-secret-lifecycle-142-seal-plan.md`
* Phase details: `.copilot-tracking/details/2026-11-15/kv-secret-lifecycle-142-seal-phase-details.md`
* Plan critique: `.copilot-tracking/reviews/plans/2026-11-15/kv-secret-lifecycle-142-seal-plan-critique.md`
* Research: `.copilot-tracking/research/2026-11-15/kv-secret-lifecycle-142-seal-research.md`
* Prior review: `.copilot-tracking/reviews/logs/2026-11-15/kv-secret-lifecycle-142-hardening-review.md`
* Changes record: `.copilot-tracking/changes/2026-11-15/kv-secret-lifecycle-142-seal-changes.md`

## Implementation-Time Updates and Follow-Up Assessment

* `P01-T01` and `P02-T01` closed the prior review's HMAC `priorSwitchoverReceipt` authenticity, `require_browser_mode=True` default, strict boolean `enabled` parsing, URI redaction, child-secret RBAC scope classification, review window continuity, and end-of-day UTC due-date checks.
* Independent `rubber-duck` review identified four remaining precision gaps (`RV-001`..`RV-004`) across the runbook RBAC export snippet, versionless rollback durability + fresh token exchange proof, probe batch continuity/gap bounds, and `rotation_plan()` step 1 CLI output safety.
* Plan `## Follow-Up Items` (live Azure test-environment staged rotation drill and inaugural live 90-day `AzureDiagnostics` + RBAC review record) remain external cloud operational follow-ups outside offline code scope.

## Findings

### RV-001 (`High`) — Runbook RBAC export snippet drops root `/` and management-group ancestor assignments

* Evidence: `infra/README.md` (`### Access review`, step 1).
* Impact: `s:=str(r.get("scope","")).rstrip("/").lower()` reduces `"/"` to `""` (falsy), and management-group scopes (`/providers/Microsoft.Management/managementGroups/<mg>`) are not path prefixes of `/subscriptions/<sub>/...`, omitting root and management-group inherited grants from `roles.json`.
* Destination: `rpi-implement` (combine `az role assignment list --scope <vault-id> --include-inherited -o json` for all ARM ancestors including `/` and management groups with child scopes `<vault-id>/secrets/*` from `az role assignment list --all -o json`, deduplicated by assignment `id`).

### RV-002 (`High`) — Versionless `rollback` accepts an still-enabled `nextVersionId` and omits `freshTokenExchangeVerified`

* Evidence: `src/core/src/zava_forward/core/secret_lifecycle.py` (`verify_staged_entra_rotation` rollback branch).
* Impact: When `containerApp.secrets[*].keyVaultUrl` is versionless (`u_ver is None`) on the same secret name while `nextVersionId` remains `enabled: true` in Key Vault, Container Apps' 30-minute secret polling will reload the broken `nextVersionId`; additionally, `rollback` probe validation does not require `freshTokenExchangeVerified: true` in browser mode.
* Destination: `rpi-implement` (require `rollback` to either pin `keyVaultUrl` to `priorVersionId`, revert to a distinct `priorSecretName`, or disable `nextVersionId` in Key Vault, and pass `require_fresh_token_exchange=effective_browser_mode` for `rollback` probes).

### RV-003 (`Medium`) — Probe validation accepts single-sample batches without span or sampling-gap bounds

* Evidence: `src/core/src/zava_forward/core/secret_lifecycle.py` (`_validate_probe_batch`).
* Impact: A single probe sample (`totalSamples: 1`) without time-span or maximum-gap evidence satisfies `zeroDowntimeVerified` and `safeToRetirePriorCredential`.
* Destination: `rpi-implement` (enforce strict integer `totalSamples >= min_probe_samples` (default `3`), `errorCount == 0`, `firstSampleAt`/`lastSampleAt` timestamps with `(lastSampleAt - firstSampleAt) >= min_probe_span_seconds` (default `60`) and `lastSampleAt <= now`, and `maxGapSeconds <= max_probe_gap_seconds` (default `30`)).

### RV-004 (`Medium`) — `rotation_plan()` step 1 still prints a bare stdout-emitting `az ad app credential reset` command

* Evidence: `src/core/src/zava_forward/core/secret_lifecycle.py` (`rotation_plan`); `infra/README.md` (`### Rotate the Entra client secret`).
* Impact: Operators instructed to run `secret_lifecycle.py rotation-plan` receive a bare `az ad app credential reset` command in step 1 whose stdout prints the generated password unless piped with `--query password -o tsv | tr -d '\r\n'` into `az keyvault secret set --file /dev/stdin --output none`.
* Destination: `rpi-plan` / `rpi-implement` (update `rotation_plan()` to emit the stdout-free pipeline while preserving the ordered substrings checked by `NoDowntimeRotationTests`).

## Validation Coverage

* Verified locally: `51` targeted unit/CLI/dependency tests (`OK`), `637` `infra/tests` (`OK`, `skipped=4`), `bicep_inventory.py --check` (`OK`), `src/core` `ruff check` + `ruff format --check` + `mypy` (`363` files `OK`), isolated `infra` `ruff check` + `ruff format --check` + `mypy --strict` (`2` files `OK`), and zero `.copilot-tracking` diff leak check (`CLEAN_DIFF`).
* Intentionally skipped per user instruction: `python3 tools/rpi-checks.py --all` (Focused tier).

## Routing Summary

* Route `RV-001`..`RV-004` into child RPI loop `issue-142-final` (`kv-secret-lifecycle-142-final`) to resolve both code/runbook defects and the `rotation_plan()` plan decision cleanly before committing.

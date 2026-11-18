<!-- markdownlint-disable-file -->
# Research: Verification Seal for Key Vault Secret Lifecycle (#142 Child Loop 2)

## Metadata

* Task ID: issue-142-seal
* Task slug: kv-secret-lifecycle-142-seal
* Parent task: issue-142-hardening (`kv-secret-lifecycle-142-hardening`)
* Date: 2026-11-15
* Research disposition: reused
* Planning Readiness: Ready
* Research posture: focused (reusing `.copilot-tracking/reviews/logs/2026-11-15/kv-secret-lifecycle-142-hardening-review.md` `RV-001`..`RV-004` and `infra/role-assignments.json`)
* Output mode: convergence

## Research Brief

* Topic: Seal the four verification and runbook-safety gaps (`RV-001`..`RV-004`) found during independent review of `kv-secret-lifecycle-142-hardening`.
* Scope: `src/core/src/zava_forward/core/secret_lifecycle.py`, `infra/scripts/secret_lifecycle.py`, `infra/README.md`, `src/core/tests/test_secret_lifecycle.py`, and `infra/tests/test_secret_lifecycle.py`.
* Non-goals: Mutating prior `kv-secret-lifecycle-142-*` or `kv-secret-lifecycle-142-hardening-*` review artifacts, modifying Bicep files, or running `tools/rpi-checks.py --all`.

## Reused Evidence (`SE-1`..`SE-4`)

* **`SE-1` (`RV-001` - Rotation browser-mode default, strict boolean `enabled`, redacted URI problems, and HMAC-signed `priorSwitchoverReceipt`)**:
  * In `src/core/src/zava_forward/core/secret_lifecycle.py`, `verify_staged_entra_rotation` should enforce `require_browser_mode: bool = True` by default (rejecting `"browserMode": false` unless `require_browser_mode=False` / `--allow-non-browser-mode` is explicitly configured by the operator), validate `isinstance(enabled, bool)` on both Entra `credentials.entries[*].enabled` and Key Vault `secretVersions.entries[*].attributes.enabled` (rejecting string `"false"` or integer `1`), never interpolate raw untrusted `version_uri` or `secret_name` strings into `problems` messages, and optionally sign `post_switchover` receipts with `HMAC-SHA256` (`signing_key` / `--signing-key-env`) while requiring a valid `HMAC-SHA256` `signature` whenever `priorSwitchoverReceipt` is presented at `post_retire` (`credentials.retiredPriorCredential` remains available when unsigned).
* **`SE-2` (`RV-002` - Secret-level RBAC assignment scope enforcement)**:
  * `infra/role-assignments.json` grants `api` `Key Vault Secrets User` at `"scope": "Key Vault"` (`/providers/Microsoft.KeyVault/vaults/<vault>`), `token-maintenance` `Key Vault Secrets Officer` at `"scope": "Secret entra-token-store-sas only"` (`/providers/Microsoft.KeyVault/vaults/<vault>/secrets/entra-token-store-sas`), and `resident-demo` `Key Vault Secrets User` at `"scope": "Secret resident-demo-password-verifier only"` and `"scope": "Secret resident-demo-session-key only"`.
  * `default_expected_caller_policy` should map each role to its allowed scope descriptors (`"vault"` vs `"secret:<name>"`), and `audit_keyvault_data_plane_access` should normalize each ARM assignment `scope` against `vault_name`—rejecting missing/foreign-vault ARM scopes and flagging `excess_rbac_privilege` whenever an assignment has subscription/RG/parent scope or vault-wide scope for an identity restricted to child secret scope(s). `infra/README.md` (`### Access review`) should export RBAC with `az role assignment list --all --include-inherited --query "[?contains(scope, '<vault-id>')]"` so child-secret assignments are captured alongside vault and inherited parent assignments.
* **`SE-3` (`RV-003` - Review window coverage, cross-entry continuity, and end-of-day UTC due date)**:
  * `create_signed_access_review_record` and `verify_access_review_ledger` should enforce `(windowEnd - windowStart) >= dt.timedelta(days=effective_min_window_days)` on standalone/initial records (defaulting `min_window_days` to `reviewIntervalDays`, e.g., `90` days, unless explicitly overridden), enforce contiguous `windowStart <= prev_window_end < windowEnd` and monotonic `reviewedAt >= prev_reviewed_at` across chained ledger entries `index >= 1`, and evaluate `nextReviewDue` (`YYYY-MM-DD`) overdue status at end-of-day UTC (`now.date() > dt.date.fromisoformat(next_due)`).
* **`SE-4` (`RV-004` - Stdout-free Entra credential reset pipeline & `auditDigest` checksum wording)**:
  * `infra/README.md` (`### Rotate the Entra client secret`, step 1) should pipe `az ad app credential reset --id <app-id> --append ... --query password -o tsv` directly into `az keyvault secret set --vault-name <vault> --name <secret> --expires <iso> --value @- --output none` (and read `keyId` metadata separately via `az ad app credential list`) so plaintext credentials never print to stdout. Clarify in `infra/README.md` and docstrings that `auditDigest` is a canonical SHA-256 integrity checksum authenticated under the reviewer's `HMAC-SHA256` signature.

## Decisions and Planning Readiness

* Selected approach: Implement `SE-1`..`SE-4` in one focused core/CLI/docs phase (`P01`) followed by negative regression tests and Focused validation (`P02`).
* Research disposition: `reused`
* Planning Readiness: `Ready`

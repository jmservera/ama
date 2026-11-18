<!-- markdownlint-disable-file -->
# Phase Details: Verification Seal for Key Vault Secret Lifecycle (#142 Child Loop 2)

## Metadata

* Task ID: issue-142-seal
* Task slug: kv-secret-lifecycle-142-seal
* Plan: .copilot-tracking/plans/2026-11-15/kv-secret-lifecycle-142-seal-plan.md
* Date: 2026-11-15

<!-- rpi:phase id=P01 -->
## P01: Seal rotation verification, child-secret RBAC scope checks, ledger window continuity, and runbook commands

<!-- rpi:task id=P01-T01 -->
### P01-T01: Update `secret_lifecycle.py` (core + CLI) and `infra/README.md` for `RV-001`..`RV-004`

* Canonical targets:
  * `src/core/src/zava_forward/core/secret_lifecycle.py`
  * `infra/scripts/secret_lifecycle.py`
  * `infra/README.md`
* Generated targets: none
* Evidence and design expectations:
  1. **Rotation verifier hardening (`FR-S1` / `RV-001` / `PC-003`)**:
     * Add `require_browser_mode: bool = True` and `signing_key: str | bytes | bytearray | None = None` to `verify_staged_entra_rotation` (validating `isinstance(require_browser_mode, bool)`). When `require_browser_mode` is `True` and `browserMode` is `False`, append a `problems` entry refusing browser-mode probe bypass, force `effective_browser_mode = True` for `_validate_health_probes`, and set `rollback_verified = True` only when zero pre-hold `problems` exist.
     * In Entra credential parsing and Key Vault secret-version parsing, inspect `enabled` and `attributes.enabled`: when omitted, default `True`; when present, require `isinstance(val, bool)` and non-conflicting values when both are present—recording structural `problems` (treating the entry as neither active nor confirmed-disabled) on invalid/conflicting types, and recording a `problems` entry if required active Entra credentials (`priorKeyId`, `nextKeyId`) have `enabled is False`.
     * Remove raw interpolation of untrusted `version_uri`, `keyVaultUrl`, `secretName`, or `secretVersionId` strings from all `secretVersions`, `containerApp.secrets`, and `containerApp.revisions` `problems` messages, reporting structural index-based diagnostics instead.
     * Add `_normalize_rotation_signing_key(signing_key)` enforcing `isinstance(signing_key, (str, bytes, bytearray))` (rejecting `bool`) and `>= 32` stripped UTF-8 bytes without echoing key material, plus `_compute_rotation_receipt_signature(receipt_payload, key_bytes)`. When `signing_key` is provided, attach `"signatureAlgorithm": "HMAC-SHA256"` and 64-hex `"signature"` over canonical receipt payload fields (all keys except `"signature"` and `"signatureAlgorithm"`). At `post_retire`, when `priorSwitchoverReceipt` is used instead of `retiredPriorCredential`, require `signing_key`, guard `isinstance(sig, str) and bool(_HEX64_RE.match(sig))` before `hmac.compare_digest`, and verify `stage == "post_switchover"`, `ok is True`, `safeToRetirePriorCredential is True`, `elapsedOverlapMinutes >= min_overlap_minutes`, and 8-field identity binding.
     * In `infra/scripts/secret_lifecycle.py`, add `--allow-non-browser-mode` and mutually exclusive `--signing-key-env` / `--signing-key-file` to `rotation-verify` via `_resolve_rotation_signing_key` (routing `--signing-key-file` through `_read_owner_only_key_bytes(..., flag_name="--signing-key-file")`).
  2. **Secret-level RBAC scope enforcement (`FR-S2` / `RV-002` / `PC-001`)**:
     * In `default_expected_caller_policy`, fail closed with `SecretLifecycleError` on unmapped `roleId` or unrecognized Key Vault `scope` descriptors in `role_matrix`, normalize `allowedSecrets` and child secret scope tokens to lowercase (`"vault"` for `"Key Vault"` and `"secret:<name.lower()>"` for `"Secret <name> only"`), and match lowercase secret names in `_secret_allowed` while keeping raw names in `callerSummaries[*].secrets`.
     * Add `_classify_arm_kv_scope(scope_value: Any, vault_name: str) -> str` using `re.IGNORECASE`:
       * `/providers/microsoft.keyvault/vaults/<vault>` -> `"vault"` if `<vault>.lower() == vault_name.lower()` else `"wrong_vault"`.
       * `/providers/microsoft.keyvault/vaults/<vault>/secrets/<secret>` -> `f"secret:{secret.lower()}"` if `<vault>.lower() == vault_name.lower()` else `"wrong_vault"`.
       * True ARM ancestor scopes (`/`, `/providers/microsoft.management/managementgroups/<mg>`, `/subscriptions/<sub>`, `/subscriptions/<sub>/resourcegroups/<rg>`) -> `"broader_parent"`.
       * Foreign/sibling `/providers/<other>...` -> `"wrong_vault"`; empty/other malformed strings -> `"invalid_scope"`.
     * In `audit_keyvault_data_plane_access`, emit `wrong_vault_rbac_scope` when an assignment's scope is `"wrong_vault"` or `"invalid_scope"`, and emit `excess_rbac_privilege` when a mapped identity's data-plane role assignment has `"broader_parent"` or any scope token outside `rule["allowedRoleScopes"].get(role_name, [])`.
     * Update `infra/README.md` (`### Access review`, step 1) RBAC export command to pipe `az role assignment list --all -o json` through a standard boundary-safe Python filter (`s == "/" or s == vid or s.startswith(vid + "/") or vid.startswith(s + "/")`) rather than invalid JMESPath `tolower()`.
  3. **Review window coverage, continuity, and end-of-day UTC due date (`FR-S3` / `RV-003` / `PC-002`)**:
     * Add `min_window_days: int | None = None` to `create_signed_access_review_record` and `verify_access_review_ledger` (CLI `review-sign` and `ledger-verify` expose optional `--min-window-days`).
     * In `create_signed_access_review_record`: when `prev_entry is None`, require `(w_end - w_start) >= dt.timedelta(days=interval if min_window_days is None else min_window_days)`; when `prev_entry is not None`, parse `prev_entry["windowEnd"]`, require contiguous `w_start <= prev_w_end < w_end`, strict `reviewed_at > prev_reviewed_at`, and `(w_end - w_start) >= dt.timedelta(days=1 if min_window_days is None else min_window_days)`.
     * In `verify_access_review_ledger`: enforce matching `idx == 0` and `idx >= 1` rules (preserving strict `reviewed_dt > prev_reviewed_dt`), compute `overdue = check_now.date() > dt.date.fromisoformat(next_due)` (end-of-day UTC, mirrored in `review_status`), and include `"overdue": overdue` (`False` when empty) in the returned dictionary alongside the overdue `problems` entry.
  4. **Runbook secret-safe credential reset & checksum wording (`FR-S4` / `RV-004` / `PC-004`)**:
     * In `infra/README.md` (`### Rotate the Entra client secret`, step 1 & steps 2-3), use `az ad app credential reset --id <app-id> --append --display-name container-apps-auth-YYYY-MM --end-date <iso> --query password -o tsv | tr -d '\r\n' | az keyvault secret set --vault-name <vault> --name entra-client-secret --expires <iso> --file /dev/stdin --output none` (retrieving `keyId` via `az ad app credential list --id <app-id>`), and document both `--signing-key-env` and `--signing-key-file` (`0600` outside repo) while keeping `rotation_plan()` step strings unchanged.
     * Clarify in `infra/README.md` (`### Access review`) and `secret_lifecycle.py` docstrings that `auditDigest` is a canonical SHA-256 integrity checksum bound under the human reviewer's `HMAC-SHA256` signature.

<!-- rpi:phase id=P02 -->
## P02: Update fixtures, add negative regression tests, and execute Focused validation

<!-- rpi:task id=P02-T01 -->
### P02-T01: Extend `src/core/tests/test_secret_lifecycle.py` and `infra/tests/test_secret_lifecycle.py` and run Focused validation

* Test ownership:
  * `src/core/tests/test_secret_lifecycle.py`
  * `infra/tests/test_secret_lifecycle.py`
  * Exact test removals: `none`
  * Maximum test additions: up to 10 focused test methods / assertions across those 2 files
* Fixture updates & negative regression cases:
  * Update `OID_TOKEN` / `oid_token` clean RBAC fixture scope from `vault_scope` to `f"{vault_scope}/secrets/entra-token-store-sas"` in `src/core/tests/test_secret_lifecycle.py` and `infra/tests/test_secret_lifecycle.py`, pass `signing_key=SIGNING_KEY_A` on the positive `priorSwitchoverReceipt` case, and update the unchained `future_audit` fixture window in `src/core/tests/test_secret_lifecycle.py` from `days=30` to `days=90`.
  * Assert `"browserMode": false` fails under default `require_browser_mode=True` (including `rollbackVerified=False` at `stage="rollback"`) and passes only when `require_browser_mode=False` / `--allow-non-browser-mode` is explicitly set.
  * Assert `"enabled": "false"` and active Entra `enabled: False` fail closed.
  * Assert malformed `secretVersions[*].id` and `containerApp.secrets[*].keyVaultUrl` containing a canary substring are never echoed in `receipt["problems"]`.
  * Assert unsigned, non-hex-signature, wrong-key, or tampered-field `priorSwitchoverReceipt` fails `post_retire`.
  * Assert mixed-case `/providers/Microsoft.KeyVault/vaults/.../secrets/Entra-Token-Store-Sas` passes cleanly while `token-maintenance` at vault scope, `api` at RG scope, and foreign-vault/sibling ARM scopes emit `excess_rbac_privilege` / `wrong_vault_rbac_scope`.
  * Assert 1-second initial review window fails signing and ledger verification, a 1-day unreviewed gap between Entry 0 `windowEnd` and Entry 1 `windowStart` fails signing and ledger verification, and `now` at `2027-01-28T18:00:00Z` on `nextReviewDue == "2027-01-28"` reports `overdue=False` whereas `2027-01-29T00:00:00Z` reports `overdue=True`.
* Validation commands:
  * `PYTHONPATH=src/core/src python3 -m unittest src/core/tests/test_secret_lifecycle.py src/core/tests/test_dependency_rule.py infra/tests/test_secret_lifecycle.py -q`
  * `python3 infra/scripts/bicep_inventory.py --check`
  * `(cd src/core && python3 -m ruff check . && python3 -m ruff format --check . && python3 -m mypy)`
  * `python3 -m ruff check --isolated --select E,F,I,B,UP --target-version py312 --line-length 100 infra/scripts/secret_lifecycle.py infra/tests/test_secret_lifecycle.py && python3 -m ruff format --isolated --line-length 100 --check infra/scripts/secret_lifecycle.py infra/tests/test_secret_lifecycle.py && MYPYPATH=src/core/src python3 -m mypy --strict infra/scripts/secret_lifecycle.py infra/tests/test_secret_lifecycle.py`

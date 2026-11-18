<!-- markdownlint-disable-file -->
# RPI Research: Verification Hardening for Key Vault Secret Lifecycle (#142 Child Loop)

## Metadata

* Task ID: issue-142-hardening
* Task slug: kv-secret-lifecycle-142-hardening
* Parent task: issue-142 (`kv-secret-lifecycle-142`)
* Date: 2026-11-15
* Research disposition: reused
* Planning Readiness: Ready

## Reused Evidence Summary

Existing evidence from parent research `.copilot-tracking/research/2026-11-15/kv-secret-lifecycle-142-research.md` (`C1`-`C17`) and parent review `.copilot-tracking/reviews/logs/2026-11-15/kv-secret-lifecycle-142-review.md` (`RV-001`..`RV-005`) completely specifies all code symbols, contracts, and test targets with zero open research gaps:

* **HE-1 (`RV-001` - Canonical `auditDigest` recomputation and duplicate ID guard)**: In `src/core/src/zava_forward/core/secret_lifecycle.py`, `audit_keyvault_data_plane_access` computes `auditDigest` over `{vaultName, windowStart, windowEnd, rbacAssignments, callerSummaries, anomalies, systemNotificationCount}`. Extracting `_compute_audit_digest` and verifying inside `create_signed_access_review_record` that `audit["auditDigest"] == _compute_audit_digest(...)` alongside uniqueness checks on `assignmentId` and `anomalyId` blocks post-audit mutation before signing.
* **HE-2 (`RV-002` - Per-identity allowed RBAC roles and diagnostic vault scope)**: `infra/role-assignments.json` grants `Key Vault Secrets User` to `api` and `resident-demo`, `Key Vault Secrets Officer` to `token-maintenance`, and zero Key Vault roles to `agents`, `orchestrator`, and `import`. Adding `allowedRoles` to `default_expected_caller_policy` lets `audit_keyvault_data_plane_access` emit `excess_rbac_privilege` when a mapped principal holds an unauthorized data-plane role (such as `Key Vault Secrets Officer` on `api`), and checking diagnostic `id_s` / `ResourceId` / `_ResourceId` against `vault_name` emits `wrong_vault_diagnostic` when cross-vault diagnostic rows are mixed in.
* **HE-3 (`RV-003` - Elapsed overlap, fresh OAuth token exchange, strict versioned URIs, and bound `post_retire` receipts)**: In `verify_staged_entra_rotation`:
  * Measure both configured window overlap and elapsed overlap through `now` (`_compute_overlap_minutes(p_start, min(p_end, now), n_start, min(n_end, now))`). `dual_secret_overlap` validates configured window overlap `>= min_overlap_minutes` (with `safeToRetirePriorCredential=False`), whereas `post_switchover` additionally requires `elapsedOverlapMinutes >= min_overlap_minutes` before `ok` and `safeToRetirePriorCredential` can be `True`.
  * Require `freshTokenExchangeVerified is True` alongside `authenticatedApiStatus == 200` on `post_switchover` and `post_retire` when `browserMode=True` so a pre-existing session cookie cannot masquerade as a live OAuth code redemption with `nextKeyId`/`nextVersionId`.
  * Require every `secretVersions.entries` row for `priorVersionId` and `nextVersionId` to carry a valid versioned Key Vault URI `https://<vault>.vault.azure.net/secrets/<secret>/<version>` matching `vaultName`, expected secret name (`priorSecretName` / `secretName`), and `version` (never allowing `row["secretName"]` to override a conflicting URI secret name).
  * Include `{vaultName, appId, secretName, priorSecretName, priorKeyId, nextKeyId, priorVersionId, nextVersionId}` in the returned rotation receipt and require exact field match when `post_retire` validates `priorSwitchoverReceipt`.
* **HE-4 (`RV-004` - Timestamp bounds and scalar secret guards)**: Call `assert_no_secret_material` on `reviewer` in `access_review` and `vault`, `app_id` in `rotation_plan`; enforce `windowEnd <= reviewedAt` and `(reviewedAt - windowEnd) <= max_interval_days` in `create_signed_access_review_record` and `verify_access_review_ledger`, plus `reviewedAt <= now` and `nextReviewDue == (reviewedAt + reviewIntervalDays).date()` in `verify_access_review_ledger`.
* **HE-5 (`RV-005` - JSONL ledger append safety)**: In `infra/scripts/secret_lifecycle.py`, `_cmd_review_sign` rejects existing non-empty `--ledger` files whose stripped content starts with `[` so JSON-array files are never corrupted by JSONL line appends.

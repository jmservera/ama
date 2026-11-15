<!-- markdownlint-disable-file -->
# RPI Phase Details: Key Vault Secret Lifecycle Rotation Verification and Scheduled Access Review (#142)

## Metadata

* Task ID: issue-142
* Task slug: kv-secret-lifecycle-142
* Related plan: .copilot-tracking/plans/2026-11-15/kv-secret-lifecycle-142-plan.md
* Evidence sources: .copilot-tracking/research/2026-11-15/kv-secret-lifecycle-142-research.md (`C1`-`C17`), `infra/scripts/secret_lifecycle.py`, `infra/tests/test_secret_lifecycle.py`, `infra/secret-inventory.json`, `infra/role-assignments.json`, `infra/modules/containerapps.bicep`, `src/core/src/zava_forward/core/ledger.py`, `src/core/src/zava_forward/core/restart_authority.py`

## Phase Index

| Phase ID | Name                                                                                                    | Status | Detail sections        |
|----------|---------------------------------------------------------------------------------------------------------|--------|------------------------|
| P01      | Author pure Key Vault secret lifecycle verification and signed review ledger module in `src/core`       | complete | P01, P01-T01           |
| P02      | Extend `infra/scripts/secret_lifecycle.py` CLI and backward-compatible operator commands                | ready  | P02, P02-T01           |
| P03      | Add deterministic unit and CLI regression tests in `src/core/tests/` and `infra/tests/`                 | ready  | P03, P03-T01, P03-T02  |
| P04      | Update `infra/README.md` lifecycle contracts, run Focused validation, and commit cleanly                | ready  | P04, P04-T01, P04-T02  |

## Locked Test Ownership and Target Matrix

* Canonical implementation targets:
  * `src/core/src/zava_forward/core/secret_lifecycle.py` (new pure domain module)
  * `infra/scripts/secret_lifecycle.py` (extended CLI + backward-compatible exports)
  * `infra/README.md` (updated operator procedure and scheduled review ledger contract)
* Generated targets: `none`
* Exact test removals: `none` (all 19 existing tests in `infra/tests/test_secret_lifecycle.py` preserved)
* Maximum test additions:
  * 1 new unit test file `src/core/tests/test_secret_lifecycle.py` (<= 28 focused semantic test methods covering positive/negative invariants across rotation overlap, staged secret-name & version switchover, mandatory post-switchover authenticated probes, rollback, secret refusal, data-plane caller/operation/notification/`401`-`403` rules, human reviewer validation, vault/audit-bound HMAC+SHA256 ledger integrity, and 90-day schedule gaps)
  * Bounded extension to `infra/tests/test_secret_lifecycle.py` (<= 14 focused CLI/contract regression test methods covering `rotation-verify`, `access-audit` against `infra/role-assignments.json` + fail-closed OID mapping, `review-sign` non-symlink/outside-repo `0600` key-file checks + chaining, and `ledger-verify`, plus strict type annotations on existing helpers)
* Semantic vs regression split:
  * `src/core/tests/test_secret_lifecycle.py` owns pure domain semantics and negative mutation cases.
  * `infra/tests/test_secret_lifecycle.py` owns CLI argument/exit-code contracts, POSIX key-file permission enforcement, backward-compatibility regressions, and live JSON/Bicep repository wiring (`secret-inventory.json`, `role-assignments.json`, `keyvault.bicep`, `containerapps.bicep`, `resident-demo.bicep`).

<!-- rpi:phase id=P01 -->
## P01: Author pure Key Vault secret lifecycle verification and signed review ledger module in `src/core`

### Context

`src/core` enforces Python 3.12 `mypy --strict`, `ruff` (`E,F,I,B,UP`, line-length 100), and zero imports outside Python stdlib and `zava_forward.core` (`C16`, `C17`). Existing modules establish clear idioms: `ledger.py` (`C8`) hashes canonical `sort_keys=True` JSON chained from `GENESIS = "0" * 64`; `diagnostic_logging.py` (`C10`) identifies credential-bearing strings; `restart_authority.py` (`C11`) rejects placeholder and non-human actors without echoing PII; and `containerapps.bicep` (`C6`) + `role-assignments.json` (`C12`) define Container Apps secret bindings and Key Vault data-plane RBAC boundaries.

### Intent

Provide a single, zero-dependency, strictly typed source of truth in `zava_forward.core.secret_lifecycle` for inventory/expiry checks, staged zero-downtime Entra secret rotation verification, Key Vault data-plane access auditing, and signed hash-chained access review ledgers.

### Boundaries

* Included: Pure domain types, validators, rotation verifier, data-plane log + RBAC auditor, HMAC-SHA256 + SHA-256 ledger builder/verifier, and legacy-compatible helper functions.
* Excluded: Network/Azure SDK calls, subprocess execution, CLI `argparse` handling, or reading/storing raw secret values.

### Likely Targets

* `src/core/src/zava_forward/core/secret_lifecycle.py`: New domain module.

### Dependencies

* None (stdlib only).

### Validation Expectations

* `PYTHONPATH=src/core/src python3 -m mypy --config-file src/core/pyproject.toml src/core/src/zava_forward/core/secret_lifecycle.py` exits `0`.
* `python3 -m ruff check src/core/src/zava_forward/core/secret_lifecycle.py` and `ruff format --check` exit `0`.

### Completion Evidence

* `src/core/src/zava_forward/core/secret_lifecycle.py` exists, exports all documented functions/constants, and passes strict type and lint checks.

### Unresolved Items

* None.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Implement `src/core/src/zava_forward/core/secret_lifecycle.py`

#### Context

Issue #142 requires two substantive capabilities beyond PR #265's ordering simulation and pending RBAC template (`C3`):
1. **Staged Entra rotation verification (`verify_staged_entra_rotation`)**:
   * Accepts a structured metadata dictionary describing `stage` (`"dual_secret_overlap"`, `"post_switchover"`, `"post_retire"`, or `"rollback"`), `vaultName`, `secretName` (e.g., `"entra-client-secret"` or staged `"entra-<client>-<suffix>"`), optional `priorSecretName` (defaulting to `secretName` for in-place rotation, or distinct for staged two-name handoffs per `setup-entra.py` / `credential_arm.py`), `appId`, `expectedIdentityId`, Entra `credentials` metadata (`priorKeyId`, `nextKeyId`, `entries` with `keyId`, `displayName`, `startDateTime`, `endDateTime`, plus optional `retiredPriorCredential` `{keyId, startDateTime, endDateTime, retiredAt}` or `priorSwitchoverDigest` for `post_retire`), Key Vault `secretVersions` metadata (`priorVersionId`, `nextVersionId`, `entries` with `id`/`version`, `secretName`, `enabled`, `expires`, `updated`), Container Apps `containerApp` revision/secret binding state (`activeRevisionsMode`, `clientSecretSettingName`, `secrets` list with `name`, `keyVaultUrl`, `identity`, and `revisions` list with `name`, `active`, `trafficWeight`, `runningState`, `replicasReady`, `secretVersionId`, optional `secretName`), and `healthProbes` across stages (`stage`, `healthzStatus`, `anonymousApiStatus`, `signInRedirectStatus`, `authenticatedApiStatus`, `errorCount`, `totalSamples`).
   * Runs `assert_no_secret_material(evidence)` first: recursively scans keys and string values (allowing `"value"` ONLY when unwrapping a top-level ARM `{"value": [...]}` metadata list envelope at CLI load boundary; rejecting `"value"` everywhere else), raising `SecretExposureError` (a subclass of `SecretLifecycleError`) with only a sanitized path label if any forbidden key (`value`, `secretText`, `password`, `clientSecret`, `secretValue`, `cookie`, `token`, `accessToken`, `refreshToken`, `sas`, `connectionString`) or targeted credential pattern (`?sig=`, `&sig=`, `?sv=`, `Bearer `, `Basic `, 3-segment JWT `eyJ[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]+`, `sk-`, `SharedAccessSignature`, `AccountKey=`) is present (never matching bare 32/64-hex version IDs or SHA-256 digests).
   * Computes overlap window between `priorKeyId` (`[prior_start, prior_end]`) and `nextKeyId` (`[next_start, next_end]`): requires `overlap_seconds >= min_overlap_minutes * 60` (default `60` minutes >= Container Apps' 30-minute versionless secret polling interval), `priorKeyId != nextKeyId`, and `next` validity `<= max_validity_days` (default `366` days). For `post_retire`, `priorKeyId` must no longer appear in active `credentials.entries`, AND verifiable pre-retirement overlap must be proven via `retiredPriorCredential` (`[startDateTime, min(endDateTime, retiredAt)]` overlapped `nextKeyId` by `>= min_overlap_minutes`) or a matching 64-hex `priorSwitchoverDigest`.
   * Verifies Key Vault version metadata: vault URI matches `https://<vaultName>.vault.azure.net/secrets/<expectedSecretName>/<versionId>`, `nextVersionId` (under `secretName`) is `enabled=True` with non-null `expires > now` and `<= max_validity_days`, `priorVersionId != nextVersionId`, and `priorVersionId` (under `priorSecretName`) remains `enabled=True` during `dual_secret_overlap`, `post_switchover`, and `rollback`, becoming `enabled=False` in `post_retire`.
   * Verifies Container Apps secret reference switchover: referenced secret entry matches `clientSecretSettingName`, `identity` matches `expectedIdentityId` (case-insensitive ARM resource ID match), `keyVaultUrl` points to the stage-expected vault/secret (`priorSecretName` during `rollback` or pre-switchover `dual_secret_overlap`; `secretName` during `post_switchover` and `post_retire`), and every traffic-bearing revision (`trafficWeight > 0`, total weight `100`) is healthy (`runningState` in `{"Running", "RunningAtMaxScale"}`, `replicasReady >= 1`). In `post_switchover` and `post_retire`, all traffic-bearing revisions must serve `nextVersionId` (and `secretName`).
   * Verifies zero-downtime health/auth probes: every probe batch recorded up to the active stage must have `totalSamples >= 1`, `errorCount == 0`, `healthzStatus == 200`, `anonymousApiStatus == 401` (explicitly flagging `200` or `302` as an auth regression), and when `browserMode=True` (default `True`), `signInRedirectStatus == 302` across stages PLUS mandatory `authenticatedApiStatus == 200` on `post_switchover` and `post_retire` probes (proving OAuth callback/session token redemption with the new `entra-client-secret`; `authenticatedApiStatus` may be omitted only in pre-switchover `dual_secret_overlap`, or checked if provided).
   * Verifies rollback behavior and strict retirement gating: if `stage == "rollback"` (or forward `post_switchover` fails and rollback probes/revisions are supplied), verifies active traffic (`weight == 100`) points back to healthy `priorVersionId` (`priorSecretName`) while `priorKeyId` remains valid (`prior_start <= now < prior_end`) and `priorVersionId` remains enabled in Key Vault and post-rollback probes pass (`rollbackVerified = True`). `safeToRetirePriorCredential` is `True` IF AND ONLY IF `stage == "post_switchover"` and `ok is True` (`False` in `dual_secret_overlap`, failed `post_switchover`, `rollback`, and `post_retire`).
   * Emits deterministic receipt dict: `ok`, `stage`, `zeroDowntimeVerified`, `overlapMinutes`, `versionSwitchoverVerified`, `rollbackVerified`, `postRetireVerified`, `safeToRetirePriorCredential`, `problems` (list of sanitized strings), and `evidenceDigest` (SHA-256 of canonical sanitized input metadata).
2. **Scheduled Key Vault data-plane access review & signed ledger (`audit_keyvault_data_plane_access`, `create_signed_access_review_record`, `verify_access_review_ledger`)**:
   * `default_expected_caller_policy(role_matrix, principal_map)`: validates `principal_map` values are distinct non-empty GUID/principal strings and maps only explicitly declared symbolic identities (`{"api": "<oid>", "token-maintenance": "<oid>", "resident-demo": "<oid>", "agents": "<oid>", "orchestrator": "<oid>", "import": "<oid>", ...}`) onto `infra/role-assignments.json` Key Vault scopes (NEVER auto-trusting OIDs from live `assignments`, so any unmapped OID fails closed):
     * `api`: allowed data-plane operations `{"SecretGet"}` on `{"entra-client-secret", "entra-token-store-sas"}` (plus staged `"entra-*"` secrets).
     * `token-maintenance`: allowed `{"SecretGet", "SecretSet"}` on `{"entra-token-store-sas"}` only.
     * `resident-demo`: allowed `{"SecretGet"}` on `{"resident-demo-password-verifier", "resident-demo-session-key"}` only.
     * `agents`, `orchestrator`, `import`: explicitly forbidden (`forbidden=True`, allowed operations `set()`).
   * `audit_keyvault_data_plane_access(..., denied_401_threshold=5)`: runs `assert_no_secret_material`, validates window (`window_start < window_end`, span `<= max_window_days`), separates OID-less platform notification rows (`OperationName` in `{"SecretNearExpiryEventGridNotification", "SecretExpiredEventGridNotification", "VaultGet"}` without caller OID) into `systemNotificationCount` rather than false-positive caller anomalies while bucketing OID-less secret data-plane operations (`SecretGet`, `SecretSet`, `SecretDelete`, `SecretPurge`, `SecretBackup`, `SecretRestore`, `SecretList`, etc.) under `"<anonymous>"`, normalizes `AzureDiagnostics` rows (`identity_claim_oid_g` / `callerObjectId` / `principalId`, `OperationName`, `httpStatusCode_d` / `statusCode`, `id_s` / `requestUri_s` / `secretName` stripped to bare secret name, `TimeGenerated`), summarizes per-principal call counts, operations, secret targets, status codes, and timestamps, evaluates RBAC assignments with `DATA_ROLES` (assigning stable deterministic `assignmentId` and flagging unmapped data-plane RBAC grantees as `unmapped_rbac_principal`), builds deterministic `anomalies` list with stable `anomalyId` (`unexpected_caller`, `unmapped_rbac_principal`, `forbidden_workload_caller`, `unexpected_operation`, `out_of_scope_secret`, `denied_access_activity` on any `403` or when a caller's `401` count `>= denied_401_threshold` [default `5`], and `unclassified_rbac_role`), and computes canonical SHA-256 `auditDigest` over `{vaultName, windowStart, windowEnd, rbacAssignments, callerSummaries, anomalies}`.
   * `create_signed_access_review_record(...)`: runs `assert_no_secret_material`, validates `reviewer` is a real named human (rejecting placeholders/automation without echoing raw strings), enforces exact 1-to-1 keyed coverage between audited `assignmentId`s and `decisions.assignments` (`"keep"` or `"remove"`, requiring non-empty `rationale` when `"remove"` or unclassified/unmapped) and exact 1-to-1 keyed coverage between audited `anomalyId`s and `decisions.anomalies` (`"remediated"`, `"revoked"`, or `"accepted_exception"` with non-empty `rationale`), binds `vaultName`, `windowStart`, `windowEnd`, and `auditDigest`, computes `nextReviewDue` (`(reviewed_at + timedelta(days=review_interval_days)).date().isoformat()`), sets `prevHash` (`GENESIS_HASH` or prior `entryHash`, enforcing matching `vaultName` when chaining onto a prior entry), computes `entryHash` (`sha256` over canonical JSON excluding `entryHash` and `signature`), and computes `signature` (`hmac.new(signing_key, entry_hash.encode("ascii"), hashlib.sha256).hexdigest()`) with `signatureAlgorithm: "hmac-sha256"` and `signingKeyId: key_id` (requiring `len(signing_key) >= 32` bytes and non-empty token-safe `key_id`).
   * `verify_access_review_ledger(entries, verification_keys, *, now, max_interval_days=90, expected_vault_name=None)`: runs `assert_no_secret_material(entries)` first (raising `SecretExposureError` on secret material per `FR-1`), then walks entries in order without raising on non-secret integrity/schema/schedule errors, checking non-empty `vaultName` and cross-entry `vaultName` continuity (plus match with `expected_vault_name` when provided), valid `auditDigest` + non-empty 1-to-1 decision/anomaly dispositions, `prevHash` continuity from `GENESIS_HASH`, `entryHash` recomputation, `signingKeyId` lookup in `verification_keys` and `hmac.compare_digest` check, human reviewer check on every entry, monotonic `reviewedAt` with inter-review gap `<= max_interval_days`, and latest entry `nextReviewDue` not overdue at `now`.

#### Intent

Deliver complete, deterministic, strictly typed core primitives covering `FR-1`..`FR-4` and `NFR-1`..`NFR-2`.

#### Boundaries

* Included: `src/core/src/zava_forward/core/secret_lifecycle.py`.
* Excluded: Modifying `src/core/pyproject.toml` mypy overrides (module must pass `strict = true` natively).

#### Likely Targets

* `src/core/src/zava_forward/core/secret_lifecycle.py`

#### Dependencies

* None.

#### Validation Expectations

* Strict `mypy` and `ruff` pass on `src/core`.

#### Completion Evidence

* Module authored and clean under static analysis.

#### Unresolved Items

* None.

<!-- rpi:phase id=P02 -->
## P02: Extend `infra/scripts/secret_lifecycle.py` CLI and backward-compatible operator commands

### Context

`infra/tests/test_secret_lifecycle.py` (`C4`) loads `infra/scripts/secret_lifecycle.py` via `importlib.util.spec_from_file_location` and directly calls `parse_time`, `validate_inventory`, `check_secrets`, `access_review`, `rotation_plan`, `rotation_timeline`, `SAFE_ORDER`, `review_status`, `DATA_ROLES`, `REQUIRED`, and `main(...)`. In addition, operators need offline-testable CLI subcommands to run staged rotation verification, data-plane `AzureDiagnostics` + RBAC access auditing, owner-key review signing, and append-only ledger verification.

### Intent

Upgrade `infra/scripts/secret_lifecycle.py` to expose the new verification and ledger subcommands while keeping 100% compatibility with all existing module attributes and CLI invocations.

### Boundaries

* Included: `infra/scripts/secret_lifecycle.py` CLI subcommands (`check`, `review`, `rotation-plan`, `rotation-simulate`, `rotation-verify`, `review-status`, `access-audit`, `review-sign`, `ledger-verify`), worktree-local `src/core/src` sys.path prepend, and `0600` POSIX signing-key file validation.
* Excluded: Direct `az` subprocess execution or accepting raw keys/secrets on CLI flags.

### Likely Targets

* `infra/scripts/secret_lifecycle.py`: Refactored and extended CLI wrapper over `zava_forward.core.secret_lifecycle`.

### Dependencies

* P01 (`zava_forward.core.secret_lifecycle`).

### Validation Expectations

* `ruff check --isolated --select E,F,I,B,UP --target-version py312 --line-length 100 infra/scripts/secret_lifecycle.py` exits `0`.
* `ruff format --isolated --line-length 100 --check infra/scripts/secret_lifecycle.py` exits `0`.
* `PYTHONPATH=src/core/src python3 -m mypy --strict infra/scripts/secret_lifecycle.py` exits `0`.

### Completion Evidence

* All legacy and new subcommands work deterministically with clean exit codes (`0` pass, `1` domain verification failure, `2` usage/input/secret-exposure refusal).

### Unresolved Items

* None.

<!-- rpi:task id=P02-T01 -->
### P02-T01: Update `infra/scripts/secret_lifecycle.py` with staged rotation and signed ledger CLI subcommands

#### Context

Shared host Python resolves `zava_forward.core` to a sibling worktree unless this worktree's `src/core/src` precedes it on `sys.path`. Prepending `Path(__file__).resolve().parents[2] / "src" / "core" / "src"` ensures `infra/scripts/secret_lifecycle.py` always loads the matching `zava_forward.core.secret_lifecycle` implementation both in CI and in multi-worktree developer environments.

#### Intent

Wire CLI commands cleanly with strict typing and safe file handling:
* `rotation-verify --evidence PATH [--min-overlap-minutes 60] [--now ISO] [--out PATH]`: validates staged rotation JSON, writes optional sanitized receipt JSON, prints summary/problems, returns `0` when `ok` (`1` on verification failure, `2` on missing args or `SecretExposureError`).
* `access-audit --assignments PATH --diagnostics PATH --vault-name NAME [--inventory infra/secret-inventory.json] [--role-matrix infra/role-assignments.json] [--expected-principals PATH] [--window-days 90] [--denied-401-threshold 5] [--now ISO] [--out PATH]`: unwraps optional top-level ARM `{"value": [...]}` list envelopes on `--assignments` / `--diagnostics`, applies fail-closed `principal_map` resolution (when `--expected-principals` is omitted or partial, unmapped OIDs surface as `unexpected_caller` / `unmapped_rbac_principal` rather than being auto-trusted from `--assignments`), produces vault-bound data-plane + RBAC audit report JSON with canonical `auditDigest`, and exits `0` (or `2` on invalid input / `SecretExposureError`).
* `review-sign --audit PATH --decisions PATH --reviewer NAME --key-file PATH --key-id ID [--ledger PATH] [--inventory infra/secret-inventory.json] [--now ISO]`: checks `--key-file` is a non-symlink regular file located outside the repository root (`not path.is_symlink()`, `path.is_file()`, not relative to repo root) with POSIX mode `0600` (`(st_mode & 0o077) == 0`) and `>= 32` trimmed key bytes, links to the tail entry of `--ledger` (JSONL or JSON list, defaulting to `GENESIS_HASH` when absent), appends or outputs the signed record without echoing the key, and exits `0` (`1` on domain/decision failure, `2` on key-file/usage/`SecretExposureError` refusal).
* `ledger-verify --ledger PATH --keys-file PATH [--vault-name NAME] [--inventory infra/secret-inventory.json] [--now ISO]`: checks `--keys-file` is a non-symlink regular file outside the repository root with POSIX mode `0600` containing a JSON object `{"<key_id>": "<utf8-key>"}` (each key `>= 32` bytes, never echoed), verifies every hash link, cross-entry `vaultName`, HMAC signature, human decision, and 90-day schedule window, prints sanitized JSON status, and exits `0` if `intact`, `1` on ledger/signature/schedule failure, or `2` on key-file refusal or `SecretExposureError`.

#### Boundaries

* Included: `infra/scripts/secret_lifecycle.py`.
* Excluded: Modifying any other script in `infra/scripts/`.

#### Likely Targets

* `infra/scripts/secret_lifecycle.py`

#### Dependencies

* P01-T01.

#### Validation Expectations

* Existing 19 tests in `infra/tests/test_secret_lifecycle.py` pass immediately before adding new tests, plus strict `ruff` and `mypy`.

#### Completion Evidence

* CLI subcommands verified via unit tests and static analysis.

#### Unresolved Items

* None.

<!-- rpi:phase id=P03 -->
## P03: Add deterministic unit and CLI regression tests in `src/core/tests/` and `infra/tests/`

### Context

Both `src/core` (`src-core` CI job) and `infra` (`src-namespace` CI job) run `unittest discover` and `ruff`/`mypy` (`C16`). Focused, deterministic tests with synthetic fixtures must fail without our implementation and verify every positive and negative security/availability edge case.

### Intent

Add comprehensive deterministic unit tests in `src/core/tests/test_secret_lifecycle.py` and CLI/contract tests in `infra/tests/test_secret_lifecycle.py`.

### Boundaries

* Included: `src/core/tests/test_secret_lifecycle.py` (new) and `infra/tests/test_secret_lifecycle.py` (extended).
* Excluded: Live network calls, time-dependent flakiness (all tests pass explicit `now`), or deleting any existing test.

### Likely Targets

* `src/core/tests/test_secret_lifecycle.py`
* `infra/tests/test_secret_lifecycle.py`

### Dependencies

* P01, P02.

### Validation Expectations

* Both test suites pass under `unittest` and pass `ruff check`, `ruff format --check`, and `mypy --strict`.

### Completion Evidence

* Zero test failures, zero skips, and 100% pass on static checks.

### Unresolved Items

* None.

<!-- rpi:task id=P03-T01 -->
### P03-T01: Create `src/core/tests/test_secret_lifecycle.py` for domain invariants and edge cases

#### Context

Tests in `src/core/tests/` run under `mypy` (`strict = true`) and `ruff` (`E,F,I,B,UP`, line-length 100).

#### Intent

Cover the core domain invariants:
1. **Zero-secret fail-closed guard**: Canary secret values inside `value`, `secretText`, `password`, `token`, `cookie`, nested lists/dicts, or `?sig=` query strings raise `SecretExposureError` and never leak the canary string in exception messages.
2. **Staged Entra rotation verification**:
   * Happy path across `dual_secret_overlap` (`safeToRetirePriorCredential=False`), `post_switchover` (`safeToRetirePriorCredential=True`), and `post_retire` (`postRetireVerified=True`, `safeToRetirePriorCredential=False`, `zeroDowntimeVerified=True`), plus staged two-name (`priorSecretName` -> `secretName`, `entra-<client>-<suffix>`) switchover.
   * Omitting `authenticatedApiStatus == 200` at `post_switchover` or `post_retire` (when `browserMode=True`) fails verification and blocks `safeToRetirePriorCredential` (`PC-001`).
   * Insufficient overlap window (`< 60` minutes), missing overlap, or `post_retire` lacking verifiable `retiredPriorCredential` / `priorSwitchoverDigest` fails verification.
   * Key Vault target version disabled, missing expiry, or wrong vault/identity fails verification.
   * Container Apps active revision still presenting `priorVersionId` in `post_switchover`, unhealthy replica state, or traffic weight mismatch fails switchover check.
   * Probe outage or auth regression (`healthz != 200`, anonymous `/api/me` returning `200` or `302` instead of `401`, `errorCount > 0`, or browser `/sign-in != 302`) fails zero-downtime check.
   * Rollback path: when `post_switchover` fails and traffic rolls back to `priorVersionId` while `priorKeyId` and `priorVersionId` remain active and post-rollback probes succeed, `rollbackVerified=True` and `safeToRetirePriorCredential=False`; if `priorKeyId` was prematurely deleted, rollback also fails.
3. **Data-plane access auditing & signed review ledger**:
   * Clean `AzureDiagnostics` events matching `api`, `token-maintenance`, and `resident-demo` scopes (plus OID-less platform `SecretNearExpiryEventGridNotification` rows and `< 5` OAuth preflight `401`s) produce accurate per-principal summaries and zero anomalies.
   * Anomaly detection catches unlisted/unmapped `principalId` (`unexpected_caller`), `<anonymous>` `SecretGet` (`unexpected_caller`), unmapped data-plane RBAC OID (`unmapped_rbac_principal`), `agents`/`orchestrator`/`import` OID (`forbidden_workload_caller`), `api` calling `SecretSet`/`SecretPurge` (`unexpected_operation`), `token-maintenance` reading `entra-client-secret` (`out_of_scope_secret`), any `403` and `>= 5` `401` bursts (`denied_access_activity`), and broad `Contributor` RBAC role (`unclassified_rbac_role`).
   * Reviewer validation rejects empty/whitespace, `"pending"`, `"TBD"`, `"system"`, `"copilot"`, `"automation"`, and accepts named humans.
   * Ledger chaining & HMAC verification passes across multiple consecutive 90-day reviews for the same `vaultName` and fails on payload mutation, cross-entry `vaultName` mismatch, missing/mismatched `assignmentId` or `anomalyId` coverage, broken `prevHash`, wrong/missing signing key, >90-day gap between consecutive reviews, overdue `nextReviewDue`, or `SecretExposureError` on embedded secret material.

#### Boundaries

* Included: `src/core/tests/test_secret_lifecycle.py`.
* Excluded: CLI subprocess spawning (covered in `infra/tests/test_secret_lifecycle.py`).

#### Likely Targets

* `src/core/tests/test_secret_lifecycle.py`

#### Dependencies

* P01-T01.

#### Validation Expectations

* `cd src/core && PYTHONPATH=src:tests python3 -m unittest discover -s tests -p "test_secret_lifecycle.py" -v` exits `0`.

#### Completion Evidence

* Passing unit suite + `ruff` + `mypy` clean in `src/core`.

#### Unresolved Items

* None.

<!-- rpi:task id=P03-T02 -->
### P03-T02: Extend `infra/tests/test_secret_lifecycle.py` for CLI workflows and repository contract alignment

#### Context

`infra/tests/test_secret_lifecycle.py` currently has 19 tests across `InventoryTests`, `CheckTests`, `ReviewAndRotationTests`, `NoDowntimeRotationTests`, `ReviewStatusTests`, and `BicepWiringTests`.

#### Intent

Preserve all 19 existing tests (adding strict return/parameter type annotations and non-None `spec.loader` assertions on existing helpers so `mypy --strict` passes without altering any existing assertion) and add CLI workflow and repository-contract tests (`StagedRotationCliTests` and `ScheduledDataPlaneReviewCliTests`) verifying:
* `rotation-verify` CLI exit codes (`0` valid switchover/retire, `1` failed probe / missing authenticated probe / rollback hold / insufficient overlap, `2` canary secret exposure with zero canary output on stdout/stderr) and `--out` receipt writing.
* `access-audit` CLI wired directly to the repository's real `infra/secret-inventory.json` and `infra/role-assignments.json` with synthetic `AzureDiagnostics` JSON fixtures (including ARM `{"value": [...]}` envelopes and fail-closed unmapped-OID checks).
* `review-sign` + `ledger-verify` CLI workflow using `tempfile.TemporaryDirectory()` outside the repository root to append chained Q3 and Q4 signed review records to a JSONL ledger, enforcing `0600` key-file permissions (rejecting `0644`, symlinks, and repo-resident key files), detecting tampered ledger lines, and failing overdue schedules.

#### Boundaries

* Included: `infra/tests/test_secret_lifecycle.py`.
* Excluded: Removing or weakening any existing test in `infra/tests/`.

#### Likely Targets

* `infra/tests/test_secret_lifecycle.py`

#### Dependencies

* P02-T01, P03-T01.

#### Validation Expectations

* `PYTHONPATH=src/core/src python3 -m unittest discover -s infra/tests -p "test_secret_lifecycle.py" -v` exits `0`, and `ruff` + `mypy` pass on `infra/tests/test_secret_lifecycle.py`.

#### Completion Evidence

* All existing + new CLI tests pass deterministically.

#### Unresolved Items

* None.

<!-- rpi:phase id=P04 -->
## P04: Update `infra/README.md` lifecycle contracts, run Focused validation, and commit cleanly

### Context

`infra/README.md` contains `## Key Vault secret lifecycle` (around lines 1504-1533) as well as structured tables parsed by `infra/scripts/bicep_inventory.py` (`C5`, `C15`). Repository Markdown style requires `*` for unordered lists in new content, plain ASCII punctuation (no em dashes), no bolded-prefix list items, fenced code blocks with language identifiers, updated `ms.date` (`2026-11-15`, already set), and strict separation of repository-tested deterministic verification from unexecuted live Azure runs.

### Intent

Document the staged zero-downtime Entra client-secret rotation procedure (with `rotation-verify` and rollback gate) and the scheduled 90-day Key Vault data-plane access review & signed ledger contract (`access-audit`, `review-sign`, `ledger-verify`) in `infra/README.md`, then execute the Focused validation suite.

### Boundaries

* Included: `infra/README.md` updates and Focused validation runs (`unittest`, `ruff`, `mypy`, `bicep_inventory.py --check`, `rename-zava-tests.py`).
* Excluded: Altering `#136` Markdown table headers/rows parsed by `bicep_inventory.py`, running `tools/rpi-checks.py --all`, pushing, or opening a PR.

### Likely Targets

* `infra/README.md`

### Dependencies

* P01, P02, P03.

### Validation Expectations

* `python3 infra/scripts/bicep_inventory.py --check` exits `0`.
* Focused `unittest`, `ruff check`, `ruff format --check`, and `mypy` commands exit `0`.

### Completion Evidence

* Clean documentation diff adhering to AMA Markdown conventions and 100% green Focused validation results recorded in `.copilot-tracking/changes/2026-11-15/kv-secret-lifecycle-142-changes.md`.

### Unresolved Items

* None.

<!-- rpi:task id=P04-T01 -->
### P04-T01: Document staged Entra rotation and scheduled signed data-plane access review in `infra/README.md`

#### Context

Lines 1504-1533 of `infra/README.md` currently document only `check`, `review`, `rotation-plan`, `rotation-simulate`, and `review-status`.

#### Intent

Expand `## Key Vault secret lifecycle` (and add `scripts/secret_lifecycle.py` to `## Layout` if helpful without disturbing `#136` tables) to document:
1. **Zero-downtime staged Entra client-secret rotation procedure**:
   * Step-by-step dual-secret overlap workflow: append new Entra credential (`--append` with bounded `--end-date`, keeping prior `keyId` valid across `>= 60` minutes overlap), store new Key Vault version with `--expires` without printing values, refresh Container Apps secret reference/revision (versionless refresh up to 30 minutes or active revision restart / staged credential tag switchover), verify continuous `/healthz` (`200`), anonymous `/api/me` (`401`), and `/sign-in` (`302`) / authenticated probes, run `secret_lifecycle.py rotation-verify --evidence <metadata.json> --out <receipt.json>` to confirm `safeToRetirePriorCredential: true`, and only then delete the superseded Entra `keyId` and disable the prior Key Vault secret version (followed by `post_retire` receipt verification).
   * Explicit rollback contract: if revision readiness or post-switchover probes fail, restore serving traffic / secret reference to the still-enabled prior Key Vault version while the prior Entra `keyId` remains valid, confirm rollback health with `rotation-verify` (`stage: rollback`, `safeToRetirePriorCredential: false`), and never delete the prior credential until a fresh forward rotation succeeds (unless rotating for confirmed compromise, which requires owner-approved ingress suspension rather than restoring a compromised secret).
2. **Scheduled Key Vault data-plane access review and signed ledger contract**:
   * 90-day cadence (`reviewIntervalDays: 90` in `infra/secret-inventory.json`).
   * Log Analytics KQL export query for `AzureDiagnostics` (`ResourceProvider == "MICROSOFT.KEYVAULT"`, projecting `TimeGenerated`, `OperationName`, `identity_claim_oid_g`, `identity_claim_appid_g`, `httpStatusCode_d`, `ResultType`, `id_s` without any secret material) paired with `az role assignment list --scope <vault-id> --include-inherited -o json`.
   * Running `secret_lifecycle.py access-audit` against `infra/role-assignments.json` and `infra/secret-inventory.json` to inspect caller principal IDs, operations, out-of-scope secret touches, forbidden workload callers (`agents`, `orchestrator`, `import`), and `401`/`403` denials.
   * Named human reviewer disposition of every RBAC assignment (`keep`/`remove`) and every anomaly (`remediated`/`revoked`/`accepted_exception`), followed by `secret_lifecycle.py review-sign` (using a `0600` key file outside Git to append an HMAC-SHA256 signed, SHA-256 hash-chained entry) and scheduled `secret_lifecycle.py ledger-verify` enforcement.
   * Explicit boundary statement distinguishing deterministic repository verification from live Azure tenant/vault drill execution.

#### Boundaries

* Included: `infra/README.md` prose, command examples, and contract tables under `## Key Vault secret lifecycle`.
* Excluded: Modifying `#136` architecture/module/sequence tables or fabricating live cloud execution claims.

#### Likely Targets

* `infra/README.md`

#### Dependencies

* P02-T01.

#### Validation Expectations

* Markdown style check (ASCII punctuation, `*` bullets, no em dashes, no bold-prefix bullets, valid relative links) and `python3 infra/scripts/bicep_inventory.py --check`.

#### Completion Evidence

* Updated `infra/README.md` verified by `test_bicep_architecture_inventory_136.py` and diff inspection.

#### Unresolved Items

* None.

<!-- rpi:task id=P04-T02 -->
### P04-T02: Run Focused validation suite (`unittest`, `ruff`, `mypy`) and verify clean repository state

#### Context

User prompt specifies Focused validation tier: unit + infra/core tests, `ruff`, `mypy`, and explicitly instructs **not** to run `tools/rpi-checks.py --all`, and to commit cleanly on `feat/infra-142-kv-secret-lifecycle` with the Copilot trailer without pushing or opening a PR.

#### Intent

Run and record exact validation commands:
* `cd src/core && PYTHONPATH=src:tests python3 -m unittest discover -s tests -p "test_secret_lifecycle.py" -v`
* `cd src/core && PYTHONPATH=src:tests python3 -m unittest discover -s tests -p "test_dependency_rule.py" -v`
* `cd src/core && python3 -m ruff check . && python3 -m ruff format --check .`
* `cd src/core && PYTHONPATH=src:tests python3 -m mypy`
* `PYTHONPATH=src/core/src:src/agents/src:src/api/src:src/orchestrator/src python3 -m unittest discover -s infra/tests -v`
* `python3 -m ruff check --isolated --select E,F,I,B,UP --target-version py312 --line-length 100 infra/scripts/secret_lifecycle.py infra/tests/test_secret_lifecycle.py`
* `python3 -m ruff format --isolated --line-length 100 --check infra/scripts/secret_lifecycle.py infra/tests/test_secret_lifecycle.py`
* `PYTHONPATH=src/core/src python3 -m mypy --strict infra/scripts/secret_lifecycle.py infra/tests/test_secret_lifecycle.py`

#### Boundaries

* Included: Focused local test, lint, format, and type-check execution.
* Excluded: `tools/rpi-checks.py --all`, global `pip install`, `git push`, `gh pr create`.

#### Likely Targets

* Validation execution and `.copilot-tracking/changes/2026-11-15/kv-secret-lifecycle-142-changes.md`.

#### Dependencies

* P01, P02, P03, P04-T01.

#### Validation Expectations

* Every listed command exits `0`.

#### Completion Evidence

* Command outputs and test counts captured in `.copilot-tracking/changes/2026-11-15/kv-secret-lifecycle-142-changes.md`.

#### Unresolved Items

* None.

<!-- markdownlint-disable-file -->
# RPI Phase Details: Issue #115 Immutable Blob Ledger Digest Container and Retention-Lock Posture

## Metadata

* Task ID: issue-115-platform-blob-immutability
* Task slug: platform-115-blob-immutability
* Related plan: .copilot-tracking/plans/2026-11-15/platform-115-blob-immutability-plan.md
* Evidence sources: .copilot-tracking/research/2026-11-15/platform-115-blob-immutability-research.md, docs/adrs/0002-pilot-readiness-architecture.md

## Phase Index

| Phase ID | Name                                                                               | Status | Detail sections        |
|----------|------------------------------------------------------------------------------------|--------|------------------------|
| P01      | Harden Bicep Container-Level Immutability, Production Guard, and Job Lock Wiring                  | Ready  | P01, P01-T01, P01-T02  |
| P02      | Check and Record Container Immutability Posture Across `src/core` and `src/orchestrator`          | Ready  | P02, P02-T01           |
| P03      | Focused Unit/Policy Tests and Static/Runtime Verification                                         | Ready  | P03, P03-T01           |

<!-- rpi:phase id=P01 -->
## P01: Harden Bicep Container-Level Immutability, Production Guard, and Job Lock Wiring

### Context

Research findings `C1`–`C6`, `C13`, and `C15`–`C18` established that `infra/modules/storage.bicep` already enables `isVersioningEnabled: true` on `blobService` and attaches an unconditional `digestRetention` (`immutabilityPolicies@2024-01-01`) child resource to `blobContainers[5]` (`ledger-digests`), but omits `immutableStorageWithVersioning` on the `ledger-digests` container itself, provides no `production`-profile `guard.bicep` failure if mutable or unlocked digest posture is requested, and omits `ZF_DIGEST_REQUIRE_RETENTION_LOCK` and `ZF_DIGEST_MIN_RETENTION_DAYS` on the scheduled `ledgerVerify` Container Apps Job.

### Intent

Ensure compiled Bicep enables version-level immutable storage (`immutableStorageWithVersioning: { enabled: true }`) on `ledger-digests` alongside `digestRetention`, rejects unlocked, mutable, or sub-365-day digest container configurations in `production` profile via `guard.bicep`, and wires `ZF_DIGEST_REQUIRE_RETENTION_LOCK` and `ZF_DIGEST_MIN_RETENTION_DAYS` into `ledgerVerify`.

### Boundaries

* Included: `infra/modules/storage.bicep`, `infra/main.bicep`, `infra/modules/guard.bicep`, `infra/modules/containerapps.bicep`, and the `#115` parameter table in `infra/README.md`.
* Excluded: Adding/removing ARM resources or altering `infra/README.md` `bicep-inventory` generated blocks; setting invalid read-only `state: 'Locked'` on ARM `immutabilityPolicies`.

### Likely Targets

* `infra/modules/storage.bicep`: Add `ledgerDigestImmutableStorage` parameter and conditional `immutableStorageWithVersioning` on `blobContainers` for `'ledger-digests'`.
* `infra/main.bicep`: Add `ledgerDigestImmutableStorage` and `ledgerDigestRequireRetentionLock` parameters, bind `productionProfileRequiresImmutableLedgerDigests` on `guard`, and forward parameters to `storage` and `containerapps`.
* `infra/modules/guard.bicep`: Add `@minLength(1)` `productionProfileRequiresImmutableLedgerDigests` parameter with `'Empty means ...'` description.
* `infra/modules/containerapps.bicep`: Add `ledgerDigestRequireRetentionLock` and `ledgerDigestMinRetentionDays` parameters and wire `ZF_DIGEST_REQUIRE_RETENTION_LOCK` and `ZF_DIGEST_MIN_RETENTION_DAYS` on `ledgerVerify`.
* `infra/README.md`: Document the new `#115` parameters and honesty boundary in the existing `#115` section.

### Dependencies

* None.

### Validation Expectations

* `az bicep build` and `az bicep lint` succeed with zero diagnostics on `infra/main.bicep`, `infra/modules/storage.bicep`, `infra/modules/guard.bicep`, and `infra/modules/containerapps.bicep`.
* `python3 infra/scripts/bicep_inventory.py --check` exits `0`.

### Completion Evidence

* Compiled JSON shows `immutableStorageWithVersioning` evaluated to `{"enabled": True}` on `ledger-digests`, `productionProfileRequiresImmutableLedgerDigests` enforced in `guard.bicep`, and `ZF_DIGEST_REQUIRE_RETENTION_LOCK` / `ZF_DIGEST_MIN_RETENTION_DAYS` rendered on `ledgerVerify`.

### Unresolved Items

* None.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Configure `immutableStorageWithVersioning` and conditional `digestRetention` on `ledger-digests` in `infra/modules/storage.bicep`

#### Context

`infra/tests/test_staff_azure.py` (`C16`) asserts literal `'ledger-digests', 'staff-results']`, `parent: blobContainers[4]`, `parent: blobContainers[5]`, and `publicAccess: 'None'` in `infra/modules/storage.bicep`. `infra/tests/test_bicep_policy.py` (`C15`) mutates `container_copy["properties"]["publicAccess"]` directly as a dict key, so `properties` on `blobContainers` must remain a Bicep object literal rather than a top-level conditional expression. Critique `PC-002` further identified that `digestRetention` must be gated with `if (ledgerDigestImmutableStorage)` so opting out in `development` does not leave an active container-level `immutabilityPolicies/default` WORM policy attached.

#### Intent

Enable `immutableStorageWithVersioning: { enabled: true }` and `digestRetention` (`if (ledgerDigestImmutableStorage)`) on the `ledger-digests` container by default while keeping `properties` as an object literal and preserving container loop indices `4` and `5`.

#### Boundaries

* Included: `param ledgerDigestImmutableStorage bool = true`, `immutableStorageWithVersioning: container == 'ledger-digests' && ledgerDigestImmutableStorage ? { enabled: true } : null` inside `blobContainers` `properties`, and `if (ledgerDigestImmutableStorage)` on `resource digestRetention` in `infra/modules/storage.bicep`.
* Excluded: Splitting `ledger-digests` into a separate container resource or modifying `digestRetention` parent indexing.

#### Likely Targets

* `infra/modules/storage.bicep`: Parameter declaration, `blobContainers` resource `properties`, and `digestRetention` condition.

#### Dependencies

* None.

#### Validation Expectations

* `az bicep build --file infra/modules/storage.bicep --stdout` and `az bicep lint --file infra/modules/storage.bicep` exit `0` with zero warnings or errors.

#### Completion Evidence

* Evaluating compiled `blobContainers` `properties` yields `{"publicAccess": "None", "immutableStorageWithVersioning": {"enabled": True}}` and `digestRetention["condition"] == True` for `copyIndex() == 5` (`ledger-digests`) when `ledgerDigestImmutableStorage == true`, and `immutableStorageWithVersioning: None` with `digestRetention["condition"] == False` when `ledgerDigestImmutableStorage == false` (`None` for all other container indices).

#### Unresolved Items

* None.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Enforce `production`-profile fail-closed digest immutability guard and wire `ledgerVerify` lock env vars

#### Context

In `infra/main.bicep` (`C5`) and `infra/modules/guard.bicep` (`C6`), `deploymentProfile` defaults to `'production'`. Currently no guard stops someone from disabling digest immutability, lowering retention below the 365-day baseline in `production` profile, or running `ledgerVerify` without `ZF_DIGEST_REQUIRE_RETENTION_LOCK=true` (`C13`). Every `guard.bicep` parameter must carry `@minLength(1)` and include `'Empty means'` in its `@description(...)` (`C17`).

#### Intent

Reject mutable, unlocked, or sub-365-day `ledger-digests` configurations at template-guard evaluation in `production` profile and propagate `ZF_DIGEST_REQUIRE_RETENTION_LOCK` and `ZF_DIGEST_MIN_RETENTION_DAYS` into the `ledgerVerify` Container Apps Job.

#### Boundaries

* Included:
  * `infra/main.bicep`: Add `param ledgerDigestImmutableStorage bool = true` and `param ledgerDigestRequireRetentionLock bool = true`; pass `productionProfileRequiresImmutableLedgerDigests: isDev || (ledgerDigestImmutableStorage && ledgerDigestRequireRetentionLock && ledgerDigestImmutabilityDays >= 365) ? 'ok' : ''` to `guard`; pass `ledgerDigestImmutableStorage` to `storage`; pass `ledgerDigestRequireRetentionLock` and `ledgerDigestMinRetentionDays: ledgerDigestImmutabilityDays` to `containerapps`.
  * `infra/modules/guard.bicep`: Add `@minLength(1) @description('Empty means production profile was combined with a mutable, unlocked, or sub-365-day ledger-digests container configuration.') param productionProfileRequiresImmutableLedgerDigests string`.
  * `infra/modules/containerapps.bicep`: Add `param ledgerDigestRequireRetentionLock bool = true` and `@minValue(1) param ledgerDigestMinRetentionDays int = 365`; add `{ name: 'ZF_DIGEST_REQUIRE_RETENTION_LOCK', value: ledgerDigestRequireRetentionLock ? 'true' : 'false' }` and `{ name: 'ZF_DIGEST_MIN_RETENTION_DAYS', value: string(ledgerDigestMinRetentionDays) }` to `ledgerVerify` container `env`.
  * `infra/README.md`: Update the `#115` parameter table and bullet notes to document `ledgerDigestImmutableStorage`, `ledgerDigestRequireRetentionLock`, `productionProfileRequiresImmutableLedgerDigests`, and `ZF_DIGEST_REQUIRE_RETENTION_LOCK` / `ZF_DIGEST_MIN_RETENTION_DAYS`.
* Excluded: Changing `.bicepparam` defaults in a way that breaks `test_governance.py` or `test_environment_quota_parameters.py`.

#### Likely Targets

* `infra/main.bicep`, `infra/modules/guard.bicep`, `infra/modules/containerapps.bicep`, `infra/README.md`.

#### Dependencies

* P01-T01 (`ledgerDigestImmutableStorage` parameter on `modules/storage.bicep`).

#### Validation Expectations

* `az bicep build --file infra/main.bicep --stdout` and `az bicep lint --file infra/main.bicep` exit `0`.
* `python3 infra/scripts/bicep_inventory.py --check` exits `0`.

#### Completion Evidence

* Compiled `main.bicep` passes all `parameter-guard` checks under default parameters (`deploymentProfile == 'production'`) and fails with `productionProfileRequiresImmutableLedgerDigests` under `ledgerDigestImmutableStorage=False`, `ledgerDigestRequireRetentionLock=False`, or `ledgerDigestImmutabilityDays=30` in `production` profile while allowing those overrides in `development` profile.

#### Unresolved Items

* None.

<!-- rpi:phase id=P02 -->
## P02: Check and Record Container Immutability Posture Across `src/core` and `src/orchestrator` Publisher and Verifier

### Context

Research findings `C7`–`C13`, `C19` and Critique findings `PC-001`, `PC-002`, `PC-004`, and `PC-005` established that:
1. `src/core/src/zava_forward/core/ledger_digest_blob.py` lacks canonical weakest-link `immutability_policy_state`, `retention_days`, `locked` posture fields across publisher, verifier, reconcile, and scheduled-runner paths, discards `PUT` response headers during `BlobLedgerDigestStore.create_anchor`, performs zero container immutability/lock validation in `publish_ledger_digests` / `publish_store_digests`, omits `x-ms-creation-time` + `min_retention_days` when `verify_ledger_digests` / `reconcile_ledger_digests` inspect blob WORM headers, and chains raw exceptions (`from exc`) in `BlobLedgerDigestStore.__init__` / `_send` / `read_anchor_with_headers` / `_parse_listing_page`.
2. `ledgerVerify` in `infra/modules/containerapps.bicep:494` executes `python -m zava_forward.orchestrator.digest_blob --publish`, which previously never read `ZF_DIGEST_REQUIRE_RETENTION_LOCK` or `ZF_DIGEST_MIN_RETENTION_DAYS` and never delegated WORM posture verification to `zava_forward.core.ledger_digest_blob` (`PC-001`).

### Intent

Provide uniform, deterministic weakest-link container immutability and retention-lock posture evaluation and recording (`immutability_policy_state`, `retention_days`, `locked`, plus human-gate honesty metadata) across `src/core/src/zava_forward/core/ledger_digest_blob.py` and `src/orchestrator/src/zava_forward/orchestrator/digest_blob.py`, failing closed whenever `require_retention_lock=True` / `ZF_DIGEST_REQUIRE_RETENTION_LOCK=true` and a valid locked retention policy is absent, `Unlocked`, expired, or under-retained.

### Boundaries

* Included: `src/core/src/zava_forward/core/ledger_digest_blob.py`, `src/core/README.md`, and `src/orchestrator/src/zava_forward/orchestrator/digest_blob.py`.
* Excluded: Changing `publish_ledger_digests(...) -> list[str]` or `orchestrator.digest_blob.publish(...) -> list[str]` return types, breaking `put_digest`/`read_digest` monkeypatch hooks in `src/orchestrator/tests/test_digest_blob.py`, altering `monitoring_coverage.ALLOWED_FIELDS`, or claiming live Azure WORM lock activation.

### Likely Targets

* `src/core/src/zava_forward/core/ledger_digest_blob.py`: Weakest-link posture synthesis, publisher/verifier/reconcile/scheduled-runner lock enforcement, and exception-cause sanitization.
* `src/orchestrator/src/zava_forward/orchestrator/digest_blob.py`: `ZF_DIGEST_REQUIRE_RETENTION_LOCK` / `ZF_DIGEST_MIN_RETENTION_DAYS` enforcement and posture metadata integration with `core.ledger_digest_blob`.
* `src/core/README.md`: Update `#115` section to document posture metadata fields and fail-closed publisher/verifier behavior.

### Dependencies

* None.

### Validation Expectations

* `cd src/core && PYTHONPATH=src:tests python3 -m unittest tests/test_ledger_digest_blob.py -v` and `python3 -m mypy` exit `0`.
* `cd src/orchestrator && PYTHONPATH=src:tests:../core/src:../core/tests python3 -m unittest tests/test_digest_blob.py -v` and `PYTHONPATH=../core/src python3 -m mypy` exit `0`.

### Completion Evidence

* Both `src/core` and `src/orchestrator` publisher, verifier, and reconcile flows check and record `immutability_policy_state`, `retention_days`, and `locked` (plus `live_worm_lock_human_gated: True`, `retention_schedule_human_gated: True`), failing closed when `require_retention_lock=True` / `ZF_DIGEST_REQUIRE_RETENTION_LOCK=true` and the policy/header is absent, `Unlocked`, expired, or `< min_retention_days`.

### Unresolved Items

* None.

<!-- rpi:task id=P02-T01 -->
### P02-T01: Add canonical weakest-link posture metadata and fail-closed checks across `src/core/ledger_digest_blob.py` and `src/orchestrator/digest_blob.py`

#### Context

Critique findings `PC-001`, `PC-002`, `PC-004`, and `PC-005` locked exact behavioral contracts for multi-blob weakest-link aggregation, dual-source `retention_policy` vs header conflicts, zero-anchor and broken-chain publish recording, decoupled `locked` vs ledger chain `intact`, `BlobLedgerDigestStore` exception sanitization, `monitoring_coverage.sanitize_diagnostic` compatibility, `report=None` scheduled alert posture, and `orchestrator.digest_blob` job parity.

#### Intent

Implement canonical weakest-link immutability posture synthesis, checking, and recording across `src/core/ledger_digest_blob.py` and `src/orchestrator/digest_blob.py`:

1. `verify_container_retention_lock` (`PC-002`):
   * Accept `require_immutable_versioning: bool = False`. When `require_immutable_versioning=True`, require `immutableStorageWithVersioning` mapping in `container_properties` with `enabled is True` (else append `"immutable_storage_with_versioning_disabled"`); when `False`, still reject explicit `enabled is False` or malformed non-Mapping non-None `immutableStorageWithVersioning`.
   * Compute `immutability_policy_state`: `"Absent"` when policy is missing/empty; `"Unlocked"` when policy is present with `state is None` (ARM pre-lock `PUT` shape) or `"Unlocked"`; `"Locked"` when `state == "Locked"`; otherwise preserve raw `state` string (which fails `retention_policy_not_locked` when `require_locked=True`). Preserve `"state"` key alongside `"immutability_policy_state"`, `"retention_days"`, `"locked"`, `"live_worm_lock_human_gated": True`, `"retention_schedule_human_gated": True`.
2. `verify_blob_retention_headers` & weakest-link `synthesize_immutability_posture` (`PC-004`):
   * Parse optional `x-ms-creation-time` header (or explicit `created_at`) and optional `require_min_remaining_days: bool = False` (used on fresh `PUT` where creation instant is `reference`). Include `"immutability_policy_state"` (`"Locked"` / `"Unlocked"` / `"Absent"` / raw mode), `"retention_days"`, `"retention_days_exact"` (`True` when derived from `created_at` / fresh `PUT`), and `"locked"`.
   * Aggregate across optional `policy_rep` and zero or more `header_reps` by weakest link:
     * If neither `policy_rep` nor any `header_rep` was inspected: `immutability_policy_state="Absent"`, `retention_days=None`, `locked=False`.
     * Otherwise `locked=True` and `immutability_policy_state="Locked"` hold ONLY when every inspected source (`policy_rep` if supplied and every inspected `header_rep`) has `locked is True` and zero retention/container problems (`policy_rep["problems"] == []` with `state == "Locked"`, and `header_rep["intact"] is True`). Any non-locked state wins over `"Locked"` (`"Absent"` > `"Unlocked"` > raw invalid state, or `"Unlocked"` when present).
     * `retention_days` takes `min` across exact day sources (`policy_rep["retention_days"]` and exact `created_at`/fresh-`PUT` `header_rep["retention_days"]`), falling back to `min` of remaining whole days `(until_dt - ref_time) // timedelta(days=1)` only when neither `retention_policy` nor `x-ms-creation-time`/fresh-`PUT` exact window is present.
     * Include `"live_worm_lock_human_gated": True` and `"retention_schedule_human_gated": True`.
3. `BlobLedgerDigestStore` (`PC-005`):
   * Add `last_immutability_posture: dict[str, Any] | None = None`.
   * Replace `from exc` with `from None` in `BlobLedgerDigestStore.__init__`, `BlobLedgerDigestStore._send`, `read_anchor_with_headers`, and `_parse_listing_page` so secret URLs/SAS strings never survive in `__cause__`.
   * Add `create_anchor_with_headers(name, digest) -> tuple[bool, dict[str, str]]` returning `(True, dict(put_headers))` on `200`/`201` (reading back headers via `read_anchor_with_headers(name)` if a `200`/`201` `PUT` omitted `x-ms-immutability-policy-mode` when `require_retention_lock` checks need headers or simply returning `put_headers` and letting publisher fall back to `read_anchor_with_headers(name)` when `put_headers` lacks `x-ms-immutability-policy-mode`) and `(False, get_headers)` on verified `409`/`412`; delegate `create_anchor` to `create_anchor_with_headers`.
4. `publish_ledger_digests(entries, blob, *, ...)` (`+ publish_ledger_digests_with_posture`, `publish_store_digests`) (`PC-004`):
   * Preserve `*` immediately after `blob` (`publish_ledger_digests(entries, blob, *, head_digests=None, ..., require_retention_lock=False, retention_policy=None, container_properties=None, lifecycle_prefixes=(), min_retention_days=DEFAULT_MIN_RETENTION_DAYS, as_of=None, posture_out=None) -> list[str]`).
   * Validate `min_retention_days` and run `verify_container_retention_lock` BEFORE broken-chain or zero-anchor returns whenever `retention_policy is not None or container_properties is not None or lifecycle_prefixes` (recording initial posture and failing closed with `LedgerDigestBlobError` if `not policy_rep["intact"]`).
   * On broken local chain, record synthesized posture on `blob.last_immutability_posture` and `posture_out` before returning `[]` (or raising `LedgerDigestBlobError` if `require_retention_lock=True` and no locked policy was verified).
   * Evaluate each anchor's headers immediately upon `create_anchor_with_headers` (using `require_min_remaining_days=created` on fresh `PUT`, falling back to `read_anchor_with_headers` if a `200`/`201` `PUT` lacks `x-ms-immutability-policy-mode` while `require_retention_lock=True`); on the FIRST non-compliant anchor when `require_retention_lock=True`, update `blob.last_immutability_posture` and `posture_out` with weakest-link posture and raise `LedgerDigestBlobError` immediately without uploading remaining anchors!
   * On zero-anchor paths (`not anchor_evals`), synthesize posture from `policy_rep` (or `"Absent"`), persist to `blob.last_immutability_posture` and `posture_out`, and fail closed with `LedgerDigestBlobError` if `require_retention_lock=True` and `not posture["locked"]`.
5. `verify_ledger_digests`, `reconcile_ledger_digests`, `_run_reconcile_cli`, and `run_scheduled_verification` (`PC-004`, `PC-005`):
   * Always evaluate `verify_blob_retention_headers` (with parsed `x-ms-creation-time` and `min_retention_days`) across all read anchors in both `verify_ledger_digests` and `reconcile_ledger_digests` (extending `reconcile_ledger_digests` and `_run_reconcile_cli` with `min_retention_days`, `retention_policy`, `container_properties`, `lifecycle_prefixes`).
   * Decouple `report["locked"]` (`posture["locked"]`) from unrelated ledger hash-chain/record mismatches (`report["intact"]`), while ensuring `require_retention_lock=True` appends a retention problem and sets `intact=False` and `retention_lock_verified=False` whenever `not posture["locked"]`.
   * Keep `_emit_ok` and `_emit_alert` compliant with `monitoring_coverage.sanitize_diagnostic` (`ALLOWED_FIELDS`), and in `run_scheduled_verification`, forward lock/policy parameters into `publish_ledger_digests` when `publish=True` and populate `immutability_policy_state`, `retention_days`, `locked`, and `immutability_posture` on ALL return dicts (reading `blob.last_immutability_posture` or default `"Absent"` posture when `report is None`).
6. `src/orchestrator/src/zava_forward/orchestrator/digest_blob.py` (`PC-001`):
   * Parse `ZF_DIGEST_REQUIRE_RETENTION_LOCK` and `ZF_DIGEST_MIN_RETENTION_DAYS` via `zava_forward.core.ledger_digest_blob` helpers (`LedgerDigestBlobError` mapped cleanly to `DocumentStoreError` so invalid env or unlocked container emits `LEDGER_DIGEST_ALERT` / `RECONCILE_ALERT_MARKER` with exit code `1`).
   * Update `BlobDigestStore.put_digest` and `read_digest` to save `self.last_response_headers = dict(headers)` (and initialize `self.last_immutability_posture = None`) while preserving exact `put_digest(name, digest) -> bool` and `read_digest(name) -> dict` signatures so existing monkeypatches (`self.blob.put_digest = fail`) continue working unchanged.
   * Update `publish`, `verify`, and `reconcile` (plus `_publish_and_verify` and `_reconcile_main`) to accept optional `require_retention_lock: bool = False`, `min_retention_days: int = 365`, `as_of: datetime | None = None`, evaluate WORM response headers via `core.ledger_digest_blob.verify_blob_retention_headers` / `synthesize_immutability_posture`, record `immutability_policy_state`, `retention_days`, `locked`, and `immutability_posture` on `blob.last_immutability_posture` and in `verify()` / `reconcile()` reports, and fail closed (`DocumentStoreError` on `publish`, `intact=False` -> `LEDGER_DIGEST_ALERT` / `RECONCILE_ALERT_MARKER` exit `1` on `verify` / `reconcile`) when `require_retention_lock=True` and the container/blob lock is absent, `Unlocked`, expired, or `< min_retention_days`.

#### Boundaries

* Included: `src/core/src/zava_forward/core/ledger_digest_blob.py`, `src/core/README.md`, `src/orchestrator/src/zava_forward/orchestrator/digest_blob.py`.
* Excluded: Modifying `monitoring_coverage.ALLOWED_FIELDS` or breaking existing `test_digest_blob.py` / `test_ledger_digest_blob.py` interfaces.

#### Likely Targets

* `src/core/src/zava_forward/core/ledger_digest_blob.py`, `src/core/README.md`, `src/orchestrator/src/zava_forward/orchestrator/digest_blob.py`.

#### Dependencies

* None.

#### Validation Expectations

* Existing 18 tests in `src/core/tests/test_ledger_digest_blob.py` and all existing tests in `src/orchestrator/tests/test_digest_blob.py` pass, and `mypy` passes in both `src/core` and `src/orchestrator`.

#### Completion Evidence

* Publisher, verifier, reconcile, and scheduled-job flows in both `src/core` and `src/orchestrator` record `immutability_policy_state`, `retention_days`, `locked`, and human-gate honesty flags, and fail closed under `require_retention_lock=True` / `ZF_DIGEST_REQUIRE_RETENTION_LOCK=true`.

#### Unresolved Items

* None.

<!-- rpi:phase id=P03 -->
## P03: Focused Unit/Policy Tests and Static/Runtime Verification

### Context

Objectives 2, 3, and 4 and Critique findings `PC-001`–`PC-005` require focused tests across `src/core/tests/`, `src/orchestrator/tests/`, and `infra/tests/`, preserving all existing suites and passing `ruff check`, `ruff format --check`, and `mypy`.

### Intent

Prove every new Bicep, `src/core`, and `src/orchestrator` immutability / retention-lock control with focused positive and negative tests, verify zero regressions across `infra/tests/`, `src/core/tests/`, and `src/orchestrator/tests/`, and pass all lint/format/type checks before committing.

### Boundaries

* Included: `infra/tests/test_bicep_policy.py`, `infra/tests/test_environment_quota_parameters.py`, `src/core/tests/test_ledger_digest_blob.py`, `src/orchestrator/tests/test_digest_blob.py`.
* Excluded: Running `tools/rpi-checks.py --all`, pushing, or opening a PR.

### Likely Targets

* `infra/tests/test_bicep_policy.py`: Add `"false": lambda: False` to `evaluate()` and pass `context={"copyIndex": lambda *_: idx}` to evaluate `container_copy["properties"]` across all container indices (`idx == 5` requires `immutableStorageWithVersioning == {"enabled": True}` with `require_immutable_versioning=True`, other indices `None`); assert conditional `digestRetention` (`[parameters('ledgerDigestImmutableStorage')]` default `True`, `False` when opted out); assert `main.bicep` -> `storage` (`ledgerDigestImmutableStorage`) and `containerapps` (`ledgerDigestRequireRetentionLock`, `ledgerDigestMinRetentionDays`) forwarding; assert `ZF_DIGEST_REQUIRE_RETENTION_LOCK == "true"` and `ZF_DIGEST_MIN_RETENTION_DAYS == "365"` on `ledgerVerify`; add `"productionProfileRequiresImmutableLedgerDigests"` to `assert_parameter_controls` and `test_mutations_reject_production_guard_bypass`; and add negative mutations for disabling `immutableStorageWithVersioning`, breaking module forwarding, and stripping `ZF_DIGEST_REQUIRE_RETENTION_LOCK`.
* `infra/tests/test_environment_quota_parameters.py`: Update `self.assertEqual(len(self.guard["parameters"]), 30)`.
* `src/core/tests/test_ledger_digest_blob.py`: Add focused tests covering (1) `verify_container_retention_lock` `immutability_policy_state`, `require_immutable_versioning`, and honesty flags, (2) `publish_ledger_digests` + `publish_ledger_digests_with_posture` weakest-link posture recording, mixed-header immediate abort, zero-anchor/broken-chain posture, and fail-closed `LedgerDigestBlobError` when required lock is absent/`Unlocked`/under-retained, (3) `verify_ledger_digests`, `reconcile_ledger_digests`, and `run_scheduled_verification` posture metadata (`immutability_policy_state`, `retention_days`, `locked` decoupled from chain mismatch, policy-vs-header conflict, and `report=None` fail-closed publish alert posture), and (4) `BlobLedgerDigestStore._send`/`__init__` `exc.__cause__ is None`.
* `src/orchestrator/tests/test_digest_blob.py`: Add focused tests verifying `ZF_DIGEST_REQUIRE_RETENTION_LOCK=true` and `ZF_DIGEST_MIN_RETENTION_DAYS` fail closed on absent/unlocked/short-retention headers during `--publish`, verify, and `--reconcile`, and pass with recorded `immutability_policy_state="Locked"`, `retention_days`, `locked=True` when locked WORM headers are returned.

### Dependencies

* P01, P02.

### Validation Expectations

* `python3 infra/scripts/bicep_inventory.py --check` -> exit `0`
* `python3 -m unittest discover -s infra/tests -p 'test_*.py' -q` -> exit `0`
* `cd src/core && PYTHONPATH=src:tests python3 -m unittest discover -s tests -p 'test_*.py' -q` -> exit `0`
* `cd src/orchestrator && PYTHONPATH=src:tests:../core/src:../core/tests python3 -m unittest discover -s tests -p 'test_*.py' -q` -> exit `0`
* `cd src/core && python3 -m mypy` -> exit `0`
* `cd src/orchestrator && PYTHONPATH=../core/src python3 -m mypy` -> exit `0`
* `python3 -m ruff check src/core src/orchestrator` and `python3 -m ruff format --check src/core src/orchestrator` -> exit `0`
* `python3 -m ruff check --isolated --line-length 100 infra/tests/test_bicep_policy.py infra/tests/test_environment_quota_parameters.py` and `python3 -m ruff format --isolated --line-length 100 --check infra/tests/test_bicep_policy.py infra/tests/test_environment_quota_parameters.py` -> exit `0`

### Completion Evidence

* All commands above pass cleanly with zero lint/type errors.

### Unresolved Items

* None.

<!-- rpi:task id=P03-T01 -->
### P03-T01: Extend `infra/tests/`, `src/core/tests/`, and `src/orchestrator/tests/` and run focused validation suite

#### Context

Locked in `## Test Ownership and Validation Lock` of the plan: zero test removals, at most 8 focused new test methods plus assertion/mutation extensions in existing suites, and alignment of `test_environment_quota_parameters.py`'s `guard.bicep` parameter count (`29` -> `30`).

#### Intent

Add high-signal tests that fail without `P01`/`P02` and run the complete focused validation suite across `infra/`, `src/core/`, and `src/orchestrator/`.

#### Boundaries

* Included: `infra/tests/test_bicep_policy.py`, `infra/tests/test_environment_quota_parameters.py`, `src/core/tests/test_ledger_digest_blob.py`, `src/orchestrator/tests/test_digest_blob.py`.
* Excluded: Unrelated suites (`src/api`, browser checks, `tools/rpi-checks.py --all`).

#### Likely Targets

* `infra/tests/test_bicep_policy.py`, `infra/tests/test_environment_quota_parameters.py`, `src/core/tests/test_ledger_digest_blob.py`, `src/orchestrator/tests/test_digest_blob.py`.

#### Dependencies

* P01-T01, P01-T02, P02-T01.

#### Validation Expectations

* Every command listed in `P03` Validation Expectations exits `0`.

#### Completion Evidence

* Recorded command outputs and test counts in `.copilot-tracking/changes/2026-11-15/platform-115-blob-immutability-changes.md`.

#### Unresolved Items

* None.

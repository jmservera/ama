<!-- markdownlint-disable-file -->
# Review Log: Conformance Closure for Key Vault Secret Lifecycle (#142 Child Loop 4)

## Metadata

* Task ID: issue-142-conformant
* Task slug: kv-secret-lifecycle-142-conformant
* Parent task: issue-142-final (`kv-secret-lifecycle-142-final`)
* Date: 2026-11-15
* Execution status: Complete
* Outcome: Defects found

## Compared Artifacts

* Research: `.copilot-tracking/research/2026-11-15/kv-secret-lifecycle-142-conformant-research.md`
* Plan: `.copilot-tracking/plans/2026-11-15/kv-secret-lifecycle-142-conformant-plan.md`
* Phase details: `.copilot-tracking/details/2026-11-15/kv-secret-lifecycle-142-conformant-phase-details.md`
* Plan critique: `.copilot-tracking/reviews/plans/2026-11-15/kv-secret-lifecycle-142-conformant-plan-critique.md`
* Changes log: `.copilot-tracking/changes/2026-11-15/kv-secret-lifecycle-142-conformant-changes.md`
* Prior review: `.copilot-tracking/reviews/logs/2026-11-15/kv-secret-lifecycle-142-final-review.md`
* Source, runbook, and tests inspected:
  * `src/core/src/zava_forward/core/secret_lifecycle.py`
  * `infra/scripts/secret_lifecycle.py`
  * `infra/README.md` (`### Rotate the Entra client secret` and `### Scheduled Key Vault data-plane access review`)
  * `src/core/tests/test_secret_lifecycle.py`
  * `infra/tests/test_secret_lifecycle.py`

## Validation Coverage

* `PYTHONPATH=src/core/src python3 -m unittest src/core/tests/test_secret_lifecycle.py src/core/tests/test_dependency_rule.py infra/tests/test_secret_lifecycle.py -q`: `62` tests passed (`OK`).
* `PYTHONPATH=src/core/src python3 -m unittest discover -s infra/tests -p 'test_*.py' -q`: `640` tests passed (`OK`, `skipped=4`).
* `PYTHONPATH=src/core/src python3 infra/scripts/bicep_inventory.py --check`: verified (`29 architecture rows, 20 Bicep modules, 12 from-empty steps`).
* `src/core` `ruff check`, `ruff format --check`, and `mypy`: passed (`310` formatted files, `363` type-checked files).
* `infra/scripts/secret_lifecycle.py` & `infra/tests/test_secret_lifecycle.py` `ruff check --isolated --line-length 100`, `ruff format --isolated --line-length 100 --check`, and `mypy --strict --explicit-package-bases`: passed (`2` files).
* `.copilot-tracking` hygiene check: `0` matches across all modified/added `#142` source, test, and runbook sections (`src/core/src/zava_forward/core/secret_lifecycle.py`, `src/core/tests/test_secret_lifecycle.py`, `infra/scripts/secret_lifecycle.py`, `infra/tests/test_secret_lifecycle.py`, and `#142` sections of `infra/README.md`; unrelated historical `.copilot-tracking` citations exist elsewhere in pre-existing repository docs/tests).
* `tools/rpi-checks.py --all` and full `src/core/tests` discovery: skipped intentionally per caller Focused-tier and execution-time bounds.

## Implementation-Time Updates & Prior Finding Closure Assessment

* Plan markers (`P01`, `P01-T01`, `P02`, `P02-T01`, `AC-C1`..`AC-C6`), phase details, critique dispositions (`PC-001`..`PC-003`), changes record, and follow-up items are reconciled.
* Closed from prior review (`kv-secret-lifecycle-142-final-review.md`):
  * **Key Vault versionless vs version-pinned rollback & switchover semantics**: In-place (`priorSecretName == secretName`) `rollback` now rejects versionless `keyVaultUrl` even when `nextVersionId` is disabled and requires pinning `priorVersionId`; two-name rollback and versionless `post_switchover`/`post_retire` verify newest `created` ordering.
  * **Paginated ARM/Graph envelope rejection**: `unwrap_arm_list_envelope` runs `assert_no_secret_material` first and fails closed on non-empty `nextLink` / `@odata.nextLink`.
  * **Finite-number & strict JSON constant rejection**: `assert_no_secret_material`, `_validate_probe_batch`, `_parse_non_negative_float`, `audit_keyvault_data_plane_access`, and all four JSON decode paths in `infra/scripts/secret_lifecycle.py` (`_strict_json_loads`) reject `NaN`, `Infinity`, and `-Infinity` while preserving public `load` and `load_ledger_entries` exports.
  * **Runbook parity**: `infra/README.md` step 1 matches `rotation_plan()` (`--years 1`), and steps 2..4 document `switchoverAt`, `firstSampleAt >= retiredAt`, `priorRetiredAt`, and pinned `priorVersionId` rollback (`SecretDisabled`).
* Remaining operational items in `## Follow-Up Items` (live staging Entra rotation drill and inaugural live 90-day `AzureDiagnostics` + RBAC signed ledger entry) remain outside offline repository scope and are routed as distinct operational follow-ups.

## Findings

### RV-001 (Major) — Invalid top-level `stage` / receipt identifier fields and token-shaped unknown `signingKeyId` can still echo unlabelled caller strings

* **Evidence**: `src/core/src/zava_forward/core/secret_lifecycle.py` (`verify_staged_entra_rotation` receipt construction and `verify_access_review_ledger` unknown `signingKeyId` message). While `problems` omits invalid `stage` strings, `receipt["stage"]` and top-level receipt string fields still echo the caller-supplied string when `ok=False`, and `verify_access_review_ledger` emits `_safe_token(key_id, '<invalid-key-id>')`, which echoes an unlabelled secret if it happens to match `^[A-Za-z0-9._:-]{1,128}$`.
* **Destination**: `rpi-implement` (normalize invalid `stage` / untrusted identifier fields in returned receipts and omit raw unknown `signingKeyId` values from ledger problem messages; add token-shaped canary assertions over full receipt/ledger dicts).

### RV-002 (Major) — `priorSwitchoverReceipt` does not sign `post_switchover` probe `lastSampleAt`

* **Evidence**: `src/core/src/zava_forward/core/secret_lifecycle.py` (`_compute_rotation_receipt_signature` and `verify_staged_entra_rotation` `needs_receipt_overlap_check` / `post_retire` probe chronology check). `switchoverAt` is signed inside `priorSwitchoverReceipt`, so `post_switchover` cannot be shifted before `switchoverAt`, but `post_switchover.lastSampleAt` is taken from the caller's `post_retire` `healthProbes` array rather than signed receipt state, allowing an earlier synthetic `post_switchover` probe window to precede an early `retiredAt`.
* **Destination**: `rpi-implement` (include `postSwitchoverProbeLastSampleAt` in `post_switchover` receipts and `_compute_rotation_receipt_signature`, and enforce `effective_retired_at >= signed_post_switchover_last_sample_at` in `post_retire`).

### RV-003 (Medium) — Cross-stage probe transition gap is ordered (`<`) but not upper-bounded

* **Evidence**: `src/core/src/zava_forward/core/secret_lifecycle.py` (`verify_staged_entra_rotation` cross-stage chronology check). Intra-batch gaps are bounded by `max_probe_gap_seconds`, and per-stage `firstSampleAt` floors bind each stage to its event timestamp, but an arbitrarily wide unprobed gap between `dual_secret_overlap.lastSampleAt` and `switchoverAt` / `post_switchover.firstSampleAt` is accepted without a transition-gap check.
* **Destination**: `rpi-implement` (bound cross-stage probe gaps around `switchoverAt` and `effective_retired_at` or document/parameterize an explicit `max_stage_transition_gap_seconds` contract).

### RV-004 (Medium) — Missing causal event timestamp leaves `zeroDowntimeVerified` sub-flag `True` when `ok` is `False`

* **Evidence**: `src/core/src/zava_forward/core/secret_lifecycle.py` (`verify_staged_entra_rotation` stage probe floor checks). When `containerApp.switchoverAt` (on `post_switchover`), `effective_retired_at` (on `post_retire`), or `containerApp.rollbackAt` (on `rollback`) is missing (`None`), `problems` records the missing timestamp (`ok=False` / `safeToRetirePriorCredential=False`), but `probe_issues` is not appended so `zeroDowntimeVerified` still evaluates to `True`.
* **Destination**: `rpi-implement` (require non-null causal event timestamps for the active stage before setting `zero_downtime_verified = True`).

### RV-005 (Medium) — Explicit `null` sibling `created` field and oversized `int` (`> 10**309`) conversion edge cases

* **Evidence**: `src/core/src/zava_forward/core/secret_lifecycle.py` (`_parse_kv_version_created`, `_parse_single_created_value`, `_validate_probe_batch`, and `audit_keyvault_data_plane_access`). `_parse_kv_version_created` skips `created: None` when `createdAt` is populated instead of flagging the explicit `null`, and calling `float(val)` on an adversarial huge Python `int` (`10**400`) can raise `OverflowError` before `math.isfinite`.
* **Destination**: `rpi-implement` (treat explicit `None` on present `created`/`createdAt`/`attributes.created` keys as invalid and wrap `float(...)` conversions with `OverflowError` guards across all numeric parsers).

## Routing Summary

* **Code follow-up (`rpi-implement`)**: Route `RV-001`..`RV-005` as a single consolidated hardening follow-up item in a future session (no further correction loop in the current frozen local candidate per caller direction).
* **Operational follow-ups**: Retain live Azure test-environment staged Entra rotation drill and inaugural live 90-day `AzureDiagnostics` + RBAC signed access-review ledger entry as distinct post-merge operational follow-ups.

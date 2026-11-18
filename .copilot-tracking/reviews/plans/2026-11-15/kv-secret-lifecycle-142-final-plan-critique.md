<!-- markdownlint-disable-file -->
# Plan Critique: Final Precision Closure for Key Vault Secret Lifecycle (#142 Child Loop 3)

## Metadata

* Task ID: issue-142-final
* Task slug: kv-secret-lifecycle-142-final
* Plan path: `.copilot-tracking/plans/2026-11-15/kv-secret-lifecycle-142-final-plan.md`
* Phase details path: `.copilot-tracking/details/2026-11-15/kv-secret-lifecycle-142-final-phase-details.md`
* Date: 2026-11-15
* Execution status: Complete
* Verdict: Revise

## Findings

### PC-001 (`High`) — Cross-stage `<= max_probe_gap_seconds` falsely rejects legitimate multi-hour soak intervals before credential retirement

* **Action owner**: Planner (`direct`, no user decision needed)
* **Evidence**: `src/core/src/zava_forward/core/secret_lifecycle.py` (`verify_staged_entra_rotation`), `src/core/tests/test_secret_lifecycle.py` (`_rotation_fixture`).
* **Issue**: In staged Entra secret rotation, operators run `dual_secret_overlap` probes during append/refresh, wait `>= min_overlap_minutes` (`60`m+) before `post_switchover` and/or before `az ad app credential delete` (`retiredAt`), and then run `post_retire` probes. Requiring `(next_stage_start - prev_stage_end) <= max_probe_gap_seconds` (`60`s) across stages rejects valid multi-hour soak intervals unless a single uninterrupted probe script runs across the entire multi-hour window.
* **Resolving update**: Enforce `0 < maxGapSeconds <= max_probe_gap_seconds` and `(totalSamples - 1) * maxGapSeconds >= span` *within* each probe batch and across multiple batches of the *same* stage, require strict chronological non-overlap across consecutive stages (`prev_stage_end <= next_stage_start`), and when `stage == "post_retire"` with `retiredPriorCredential.retiredAt` present, require the `post_retire` stage's `lastSampleAt > retiredAt` so pre-deletion probes cannot satisfy `post_retire`.

### PC-002 (`Medium`) — Uncaught `parse_time` errors on missing or naive probe timestamps would raise `ValueError` instead of recording structured `problems`

* **Action owner**: Planner (`direct`, no user decision needed)
* **Evidence**: `src/core/src/zava_forward/core/secret_lifecycle.py` (`parse_time`, `_validate_probe_batch`).
* **Issue**: `parse_time()` raises `ValueError` on empty, malformed, or timezone-naive timestamps. Calling `parse_time()` directly inside `_validate_probe_batch` without catching `(ValueError, TypeError)` would abort `verify_staged_entra_rotation` instead of returning `ok: False` with descriptive `problems`.
* **Resolving update**: Parse `firstSampleAt` and `lastSampleAt` inside a guarded helper in `_validate_probe_batch` that appends structured `probe[<stage>]: ...` entries to `issues` when missing, non-string, naive, or invalid.

### PC-003 (`Low`) — `merge_vault_role_assignments` treatment of `/keys/*` and `/certificates/*` child scopes should be explicit

* **Action owner**: Planner (`direct`, no user decision needed)
* **Evidence**: `src/core/src/zava_forward/core/secret_lifecycle.py` (`_classify_arm_kv_scope`).
* **Issue**: `az role assignment list --all` may contain child assignments on `<vault-id>/keys/*` or `<vault-id>/certificates/*`, which `_classify_arm_kv_scope` classifies as `"invalid_scope"` for secret reviews.
* **Resolving update**: Specify explicitly in `P01-T01` that `merge_vault_role_assignments` selects `"vault"` and `"secret:*"` scopes for the exact ARM `<vault-id>` prefix from `all_assignments` (ignoring non-secret child scopes on `/keys/*` or `/certificates/*` and vaults in other resource groups/subscriptions) while requiring every entry in `inherited_assignments` to classify as `"vault"` or `"broader_parent"` on the matching subscription/RG chain.

### PC-004 (`Low`) — Align `rotation_plan()` flag `--years 1` with `infra/README.md`

* **Action owner**: Planner (`direct`, no user decision needed)
* **Evidence**: `src/core/src/zava_forward/core/secret_lifecycle.py` (`rotation_plan`), `infra/README.md` (`### Rotate the Entra client secret`).
* **Issue**: The candidate plan wrote `--end-date <iso>` in `FR-F4` while `infra/README.md` and existing `rotation_plan()` use `--years 1`.
* **Resolving update**: Keep `--years 1` in `rotation_plan()` step 1 so `rotation_plan()` and `infra/README.md` use identical flags.

<!-- markdownlint-disable-file -->
# RPI Plan Critique: Conformance Closure for Key Vault Secret Lifecycle (#142 Child Loop 4)

## Metadata

* Task ID: issue-142-conformant
* Critique date: 2026-11-15
* Plan: .copilot-tracking/plans/2026-11-15/kv-secret-lifecycle-142-conformant-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/kv-secret-lifecycle-142-conformant-phase-details.md
* Critique execution status: Complete

## Inputs and Criterion Boundary

* Task context and caller requirements: Assess whether `FR-C1`..`FR-C6` and tasks `P01-T01` / `P02-T01` completely and soundly resolve prior review defects `RV-001`..`RV-006` without breaking existing tests, introducing new bypasses or contradictions, or altering intended CLI fail-closed exit contracts. Specifically verify: (1) `switchoverAt` vs `min_overlap_minutes` interactions with existing tests (`test_rejects_overlap_shorter_than_minimum_window`, `test_rejects_premature_elapsed_overlap_missing_fresh_exchange_and_bad_uris`, `test_supports_staged_two_name_secret_switchover`, and `post_retire` tests); (2) Unix epoch `created` parsing safety for booleans, negative/zero/non-finite/overflow timestamps, and `attributes.created` conflicts; (3) completeness of `!r` and raw input reflection sanitization across `src/core/src/zava_forward/core/secret_lifecycle.py` and `infra/scripts/secret_lifecycle.py`; and (4) CLI exit-code impact of `assert_no_secret_material` raising `SecretLifecycleError` vs `SecretExposureError`.
* Research and evidence considered:
  * .copilot-tracking/plans/2026-11-15/kv-secret-lifecycle-142-conformant-plan.md
  * .copilot-tracking/details/2026-11-15/kv-secret-lifecycle-142-conformant-phase-details.md
  * .copilot-tracking/research/2026-11-15/kv-secret-lifecycle-142-conformant-research.md
  * .copilot-tracking/reviews/logs/2026-11-15/kv-secret-lifecycle-142-final-review.md
  * src/core/src/zava_forward/core/secret_lifecycle.py
  * infra/scripts/secret_lifecycle.py
  * infra/README.md
  * src/core/tests/test_secret_lifecycle.py
  * infra/tests/test_secret_lifecycle.py
* Decisions, dependencies, and acceptance criteria considered: `FR-C1`..`FR-C6`, `NFR-C1`..`NFR-C3`, `AC-C1`..`AC-C6`, Focused validation tier (`unittest`, `bicep_inventory.py --check`, `ruff check`, `ruff format --check`, `mypy`; `tools/rpi-checks.py --all` intentionally excluded), and zero `.copilot-tracking` strings across tracked and untracked files under `src/` and `infra/`.
* Assessment boundary: Evaluates offline verifier, CLI wrapper, runbook, and unit/CLI test correctness against Azure Key Vault and Container Apps contracts documented in supplied research and review logs. Does not validate live Azure staging execution, which remains an explicit follow-up item.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
|------------------------------------------|----------|---------------------|
| FR-C1 / CE-1 / AC-C1 (`RV-001`) | Partial | Version-pinned in-place rollback, two-name versionless rollback, and newest-`created` checks match Key Vault resolution semantics, but `P01-T01` item 4 omits `bool` exclusion (`isinstance(True, int)`), falsy/conflicting `created` vs `attributes.created` handling, and `OverflowError`/`OSError` epoch bounds (`PC-003`). |
| FR-C2 / CE-2 / AC-C2 (`RV-002`) | Partial | `switchoverAt`, `rollbackAt`, `retiredAt`/`priorRetiredAt`, and `firstSampleAt` event floors preserve `test_rejects_overlap_shorter_than_minimum_window`, `test_rejects_premature_elapsed_overlap_missing_fresh_exchange_and_bad_uris`, and `test_supports_staged_two_name_secret_switchover`, but `P02-T01` misses an ad-hoc `retire_payload` in `infra/tests/test_secret_lifecycle.py` (`PC-002`), and `P01-T01` omits `switchoverAt <= retiredPriorCredential.endDateTime` plus receipt boolean gating order (`PC-003`). |
| FR-C3 / CE-3 / AC-C3 (`RV-003`) | Covered | `unwrap_arm_list_envelope` runs `assert_no_secret_material` first and rejects non-empty or non-string `nextLink` and `@odata.nextLink` with `SecretLifecycleError`. |
| FR-C4 / CE-4 / AC-C4 (`RV-004`) | Partial | `_fmt_http_status` and the listed `!r` replacements miss `healthProbes[].stage` (`probe[{stage_label}]`), `verification_keys` `key_id` length errors, `--signing-key-env` reflection, unvalidated `prev_entry.vaultName` / `expected_vault_name`, and `priorKeyId`/`nextKeyId` (`PC-001`). |
| FR-C5 / CE-5 / AC-C5 (`RV-005`) | Partial | `assert_no_secret_material` raising `SecretLifecycleError` on non-finite floats preserves CLI exit codes (`2` across CLI file loads via `_strict_json_loads`; `1` only for direct in-memory `review-sign` validation errors), but `P01-T01` misnames exported loader functions in `infra/scripts/secret_lifecycle.py` and misses string `"NaN"`/`"Infinity"` in `audit_keyvault_data_plane_access` `status_raw` (`PC-002`). |
| FR-C6 / CE-6 / AC-C6 (`RV-006`) | Partial | `infra/README.md` step 1 `--years 1` parity and `grep -rn '\.copilot-tracking' src/ infra/` cover `RV-006`, while `infra/README.md` step 3 (line 1535) needs explicit alignment from `"probes ending after retiredAt"` to `firstSampleAt >= retiredAt` and `priorRetiredAt` (`PC-003`). |
| P01 / P01-T01 | Partial | Needs targeted tightening in items 1, 3, 4, 5, and 6 for `PC-001`..`PC-003`. |
| P02 / P02-T01 / NFR-C3 | Partial | Fixture and test bounds (`<= 4` core, `<= 2` infra) are sound once `retire_payload` in `test_cli_signing_flags_browser_gate_and_runbook_command_safety` and `healthProbes[].stage` canary coverage are included (`PC-001`, `PC-002`). |

## Verdict

* Verdict: Revise
* Rationale: The candidate architecture soundly resolves `RV-001`..`RV-006`, preserves existing overlap/switchover tests, and maintains fail-closed CLI exit codes (`SecretLifecycleError` returns `2` on all CLI JSON loads via `_strict_json_loads` and `2` in outer `main()` handlers, while `review-sign` maps domain `SecretLifecycleError` to `1` after strict JSON loading). However, three concrete planner-correctable gaps (`PC-001`..`PC-003`) would leave unvalidated secret-reflection paths open (`healthProbes[].stage`, `--signing-key-env`, short `verification_keys` `key_id`), break `infra/tests/test_secret_lifecycle.py` (`LIFE.load_ledger_entries` public name and inline `retire_payload` missing `priorRetiredAt`), and allow `"created": true` (`isinstance(True, int)`) or epoch overflow in `secretVersions.entries` if implemented literally.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Residual unvalidated input reflection paths in probe stages, key IDs, CLI `--signing-key-env`, and chained vault names

* Related IDs: FR-C4, AC-C4, P01-T01, P02-T01 (`RV-004`)
* Evidence: `src/core/src/zava_forward/core/secret_lifecycle.py` (`_validate_probe_batch` line 409; `verify_staged_entra_rotation` lines 685-753, 862, 899; `create_signed_access_review_record` line 1986; `verify_access_review_ledger` lines 2054, 2078) and `infra/scripts/secret_lifecycle.py` (`_resolve_rotation_signing_key` lines 192, 197; `_load_verification_keys` line 217).
* Concern: `P01-T01` item 3 sanitizes top-level `{stage!r}` and unknown `signingKeyId`, and `AC-C4` requires that unlabelled canary strings placed in `stage` or `signingKeyId` never appear in `problems` or error messages, but five reflection paths remain unguarded:
  1. `_validate_probe_batch` formats `stage_label = str(batch.get("stage") or "unknown")` into every `f"probe[{stage_label}]: ..."` problem without checking `batch.get("stage") in VALID_ROTATION_STAGES` (nor flagging unknown `healthProbes[].stage` entries).
  2. `verify_access_review_ledger` (line 2054) and `_load_verification_keys` (`infra/scripts/secret_lifecycle.py` line 217) format `f"verification key {key_id!r} must be at least 32 bytes"` before validating `key_id` against `_KEY_ID_TOKEN_RE`, echoing raw secret material if a `--keys-file` swaps key ID and secret or puts an unlabelled secret in the key slot.
  3. `_resolve_rotation_signing_key` (`infra/scripts/secret_lifecycle.py` lines 192, 197) echoes `{env_name!r}` to `stderr` when unset or `< 32` bytes; if an operator mistakenly passes a raw secret value to `--signing-key-env <secret>` instead of an environment variable name, `os.environ.get` misses and prints the secret verbatim.
  4. `create_signed_access_review_record` (line 1986) echoes unvalidated `{prev_vault!r}` from `prev_entry`, and `verify_access_review_ledger` (line 2078) echoes `{ledger_vault!r}` when seeded from unvalidated `expected_vault_name`.
  5. `verify_staged_entra_rotation` interpolates `prior_key_id` and `next_key_id` directly into `problems` without validating them against `_KEY_ID_TOKEN_RE` (echoing `<invalid-key-id>` when malformed) and `review_status` interpolates unvalidated `row.get("principalId")`.
* Impact: Leaves `RV-004` / `AC-C4` incomplete by allowing unlabelled secret strings in `healthProbes[].stage`, `verification_keys`, `--signing-key-env`, `prev_entry.vaultName`, or `priorKeyId`/`nextKeyId` to leak into receipts, `stderr`, or exceptions.
* Smallest useful change: Expand `P01-T01` item 3 and `P02-T01` (`AC-C4`) to: (a) reject `batch.get("stage") not in VALID_ROTATION_STAGES` using `"<invalid-stage>"` as `stage_label`; (b) validate `key_id` in `verify_access_review_ledger` and `_load_verification_keys`, `priorKeyId`/`nextKeyId` in `verify_staged_entra_rotation`, and `principalId` in `review_status` against `_KEY_ID_TOKEN_RE` before formatting (substituting `"<invalid-key-id>"` / `"<invalid-principal>"`); (c) validate `--signing-key-env` against `^[A-Za-z_][A-Za-z0-9_]*$` without echoing rejected or unset values; and (d) validate `prev_entry.vaultName` and `expected_vault_name` against `_VAULT_NAME_RE` before formatting.
* Action owner: planning_parent
* Exact resolving evidence: Updated `P01-T01` item 3 and `P02-T01` item 4 covering `healthProbes[].stage`, `verification_keys` `key_id`, `--signing-key-env`, `prev_entry.vaultName`/`expected_vault_name`, and `priorKeyId`/`nextKeyId` canary non-reflection.
* Decision route: direct_planner_correction

<!-- rpi:critique id=PC-002 -->
### PC-002 [High]: Inline `post_retire` CLI test payload, exported CLI loader names, and string `"NaN"` status parsing break `P01-T01` / `P02-T01` if left implicit

* Related IDs: FR-C2, FR-C5, NFR-C3, P01-T01, P02-T01 (`RV-002`, `RV-005`)
* Evidence: `infra/tests/test_secret_lifecycle.py` (`test_review_sign_rejects_json_array_ledger_and_preserves_missing_newline_jsonl` line 778; `test_cli_signing_flags_browser_gate_and_runbook_command_safety` lines 846-885), `infra/scripts/secret_lifecycle.py` (`__all__` lines 115-128; `load` line 131; `_load_verification_keys` line 199; `load_ledger_entries` lines 215-234), and `src/core/src/zava_forward/core/secret_lifecycle.py` (`audit_keyvault_data_plane_access` line 1629).
* Concern: Three concrete implementation mismatches exist against current source and tests:
  1. In `infra/tests/test_secret_lifecycle.py` lines 846-865, `test_cli_signing_flags_browser_gate_and_runbook_command_safety` builds `retire_payload` inline from `self._rotation_payload(switched=True)` (which returns a `post_switchover` payload evaluated earlier at `--now 2026-10-16T00:00:00Z`) and mutates `stage = "post_retire"` with `post_retire.firstSampleAt = "2026-10-16T00:30:00Z"` (`--now 2026-10-16T01:00:00Z`). `_rotation_payload(switched=True)` cannot pre-populate `priorRetiredAt = "2026-10-16T00:25:00Z"` without mutating `sw_payload`, so unless `P02-T01` explicitly updates `retire_payload["credentials"]["priorRetiredAt"]` in that test, `rc_env_ok` fails under `FR-C2`.
  2. `P01-T01` item 1 instructs wiring `_strict_json_loads` across `_load_json`, `_load_jsonl`, and `_load_verify_keys`, whereas `infra/scripts/secret_lifecycle.py` publicly exports `load` and `load_ledger_entries` in `__all__` (and `infra/tests/test_secret_lifecycle.py` line 778 calls `LIFE.load_ledger_entries` directly) alongside `_load_verification_keys`, with four JSON decode sites (`load`, `_load_verification_keys`, JSON-array `load_ledger_entries`, and JSONL line `load_ledger_entries`).
  3. In `audit_keyvault_data_plane_access` (line 1629), `int(float(str(status_raw)))` accepts JSON string `"NaN"` or `"Infinity"` past both `_strict_json_loads` and `assert_no_secret_material` and raises uncaught `ValueError`/`OverflowError` instead of `SecretLifecycleError` (and accepts boolean `True`/`False` if `status_raw` is a `bool`).
* Impact: Literal execution of `P01-T01` and `P02-T01` would break existing CLI unit tests in `infra/tests/test_secret_lifecycle.py` and leave string `"NaN"`/`"Infinity"` diagnostic status values crashing outside `SecretLifecycleError`.
* Smallest useful change: Update `P01-T01` item 1 to preserve public `load` and `load_ledger_entries` (routing all four JSON decode sites in `load`, `_load_verification_keys`, and `load_ledger_entries` through `_strict_json_loads`) and guard `status_raw` parsing in `audit_keyvault_data_plane_access` against `bool` and non-finite/invalid strings with `SecretLifecycleError`; update `NFR-C3` and `P02-T01` to explicitly set `retire_payload["credentials"]["priorRetiredAt"]` (for example `"2026-10-16T00:25:00Z"`) in `test_cli_signing_flags_browser_gate_and_runbook_command_safety`.
* Action owner: planning_parent
* Exact resolving evidence: Updated `P01-T01` item 1, `NFR-C3`, and `P02-T01` naming `load`, `load_ledger_entries`, `_load_verification_keys`, guarded `status_raw` parsing, and `retire_payload["credentials"]["priorRetiredAt"]`.
* Decision route: direct_planner_correction

<!-- rpi:critique id=PC-003 -->
### PC-003 [Medium]: `secretVersions.entries[].created` parser edge cases, `post_retire` credential-expiry vs `switchoverAt` gap, receipt flag gating, and `infra/README.md` step 3 wording

* Related IDs: FR-C1, FR-C2, FR-C6, P01-T01 (`RV-001`, `RV-002`, `RV-006`)
* Evidence: `.copilot-tracking/details/2026-11-15/kv-secret-lifecycle-142-conformant-phase-details.md` (`P01-T01` items 4, 5, 6), `src/core/src/zava_forward/core/secret_lifecycle.py` (`verify_staged_entra_rotation` lines 740-980), and `infra/README.md` (`### Rotate the Entra client secret` step 3 line 1535).
* Concern:
  1. `P01-T01` item 4 specifies parsing `created` from `row.get("created")`, `row.get("createdAt")`, or `(row.get("attributes") or {}).get("created")` accepting `"positive finite int/float Unix epoch seconds"`. Because `isinstance(True, int)` is `True` (`float(True) == 1.0 > 0`), omitting `not isinstance(val, bool)` silently parses `"created": true` as `1970-01-01T00:00:01Z`; truthy `or` chaining skips falsy malformed values (`"created": false`, `0`, `""`) when `attributes.created` is present and ignores conflicting `created`/`createdAt`/`attributes.created` values (unlike `_parse_strict_enabled`); `(row.get("attributes") or {})` assumes `attributes` is a `Mapping`; and `dt.datetime.fromtimestamp(..., tz=dt.UTC)` can raise `OverflowError`/`OSError`/`ValueError` on huge finite floats (e.g. `1e20`) or accept future `created > now_utc`.
  2. In `P01-T01` item 5: `post_switchover` guarantees `switchoverAt < p_end` via `switchoverAt <= now_utc < p_end`, but in `post_retire` with `retiredPriorCredential`, `rp_end` may precede `switchoverAt` even when an earlier window satisfied `overlap_minutes >= min_overlap_minutes`, leaving an undetected pre-switchover expiry outage unless `switchover_dt <= rp_end` is verified. In addition, `iso_utc(switchover_dt)` is referenced without noting canonical UTC normalization (`dt.isoformat()` is used elsewhere in `secret_lifecycle.py`), `versionSwitchoverVerified` currently ignores `keyVaultUrl` / newest-`created` / `switchoverAt` failures, `zeroDowntimeVerified` must be gated on stage event-floor checks, and `rollbackAt` + `rollback` probe-floor checks must run before `pre_rollback_hold_problems = len(problems)` so `rollbackVerified` stays `False` on violation.
  3. In `P01-T01` item 6, `infra/README.md` step 3 (line 1535) currently states `"with post_retire probes ending after retiredAt, or the HMAC-SHA256-signed priorSwitchoverReceipt"`, which contradicts `FR-C2` (`firstSampleAt >= retiredAt` and mandatory `priorRetiredAt` + `switchoverAt` even when `priorSwitchoverReceipt` is supplied).
* Impact: Risks silent boolean/conflict bypass or `OverflowError` on `created` timestamps, an unverified pre-switchover credential expiry window in `post_retire`, inconsistent sub-flags (`versionSwitchoverVerified` / `zeroDowntimeVerified` / `rollbackVerified`) on invalid receipts, and stale step 3 runbook guidance.
* Smallest useful change: Tighten `P01-T01` items 4, 5, and 6 to: (a) check explicit key presence across `created`, `createdAt`, and `Mapping`-guarded `attributes.created`, rejecting `bool`, `<= 0`, non-finite, out-of-range (`OverflowError`/`OSError`/`ValueError`), `> now_utc`, or conflicting timestamps; (b) enforce `switchover_dt <= rp_end` when `retiredPriorCredential` is present in `post_retire`, normalize `switchoverAt` receipt comparisons with `parse_time(...).isoformat()`, and gate `versionSwitchoverVerified`, `zeroDowntimeVerified`, and `pre_rollback_hold_problems` on the new URL/timestamp/floor checks; and (c) explicitly update `infra/README.md` step 3 to require `firstSampleAt >= retiredAt` and `credentials.priorRetiredAt` + `containerApp.switchoverAt` alongside `priorSwitchoverReceipt`.
* Action owner: planning_parent
* Exact resolving evidence: Updated `P01-T01` items 4, 5, and 6 incorporating strict `created` parsing, `switchover_dt <= rp_end`, receipt flag gating order, canonical UTC `switchoverAt` comparison, and `infra/README.md` step 3 alignment.
* Decision route: direct_planner_correction

## Strengths and Residual Risk

* **Existing overlap and two-name tests remain conflict-free**: Verified against `src/core/tests/test_secret_lifecycle.py` that `test_rejects_overlap_shorter_than_minimum_window` and `test_rejects_premature_elapsed_overlap_missing_fresh_exchange_and_bad_uris` continue to record `"dual-secret overlap"` and `"elapsed dual-secret overlap"` problems independently of `switchoverAt`, `test_supports_staged_two_name_secret_switchover` satisfies strict newest-`created` on `secretName` (`entra-client-secret-2026-11`), and adding `priorRetiredAt` to `_rotation_fixture("post_retire")` preserves both `test_post_retire_requires_retired_prior_and_verifiable_overlap_proof` and `test_post_retire_rejects_future_retired_at_and_unbound_prior_receipt`.
* **CLI exit-code contract verified**: Raising `SecretLifecycleError` in `assert_no_secret_material` for non-finite floats and in `_strict_json_loads` (`parse_constant`) yields exit code `2` across all CLI commands (`check`, `rotation-verify`, `rbac-merge`, `review`, `review-status`, `access-audit`, `review-sign`, `ledger-verify`) when reading malformed JSON/JSONL files from disk, and fails closed (`1` on `review-sign`, `2` elsewhere) for programmatic callers without misclassifying numeric corruption as `SecretExposureError`.
* **Accepted operational residual risk**: Offline CI tests prove deterministic contract enforcement; live staging rotation execution and the inaugural 90-day live `AzureDiagnostics` + RBAC signed ledger entry remain explicitly tracked follow-up items requiring coordinator-attended live Azure access.

## Questions or Blocking Evidence Gaps

* None. All three findings are self-contained planner corrections fully resolved by the supplied repository evidence.

## Limitations

* Critique is bounded to offline static and unit-testable behavior across the five supplied source, runbook, and test files; live Azure Key Vault and Container Apps control/data-plane behavior is evaluated against the documented Azure contracts in `.copilot-tracking/research/2026-11-15/kv-secret-lifecycle-142-conformant-research.md`.

## Recommended Next Action

* Highest-impact finding: PC-001
* Action owner: planning_parent
* Smallest next action: Revise `P01-T01`, `P02-T01`, and `NFR-C3` directly in the plan and phase details to incorporate `PC-001`, `PC-002`, and `PC-003`, then finalize the plan for `rpi-implement` without another critique pass.
* User response required: no

<!-- markdownlint-disable-file -->
# RPI Plan Critique: Verification Hardening for Key Vault Secret Lifecycle (#142 Child Loop)

## Metadata

* Task ID: issue-142-hardening
* Critique date: 2026-11-15
* Plan: .copilot-tracking/plans/2026-11-15/kv-secret-lifecycle-142-hardening-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/kv-secret-lifecycle-142-hardening-phase-details.md
* Critique execution status: Complete

## Inputs and Criterion Boundary

* Task context and caller requirements: Critique the final-candidate child plan for `issue-142-hardening` (`kv-secret-lifecycle-142-hardening`) to verify whether `FR-H1`..`FR-H4`, `P01-T01`, and `P02-T01` completely and accurately resolve parent review defects `RV-001`..`RV-005` without breaking existing legacy CLI tests or callers, while keeping original parent review records untouched and respecting the Focused validation boundary.
* Research and evidence considered:
  * .copilot-tracking/plans/2026-11-15/kv-secret-lifecycle-142-hardening-plan.md
  * .copilot-tracking/details/2026-11-15/kv-secret-lifecycle-142-hardening-phase-details.md
  * .copilot-tracking/research/2026-11-15/kv-secret-lifecycle-142-hardening-research.md
  * .copilot-tracking/reviews/logs/2026-11-15/kv-secret-lifecycle-142-review.md
  * src/core/src/zava_forward/core/secret_lifecycle.py
  * infra/scripts/secret_lifecycle.py
  * src/core/tests/test_secret_lifecycle.py
  * infra/tests/test_secret_lifecycle.py
* Decisions, dependencies, and acceptance criteria considered: Complete resolution of `RV-001`..`RV-005`, preservation of all 19 legacy `infra/tests/test_secret_lifecycle.py` tests and 21 parent #142 lifecycle tests (`exact removals: none`), preservation of parent review record `.copilot-tracking/reviews/logs/2026-11-15/kv-secret-lifecycle-142-review.md`, stdlib-only core boundary (`NFR-H1`), and Focused validation without running `tools/rpi-checks.py --all`, pushing, or opening a PR.
* Assessment boundary: Evaluates exact symbol-level contract completeness, execution-order correctness, fail-closed security invariants, and backward compatibility across the supplied plan, phase details, research, review log, implementation modules, and test suites. Live Azure Entra and Key Vault runtime behavior remains outside offline repository evaluation scope.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
|------------------------------------------|----------|---------------------|
| `FR-H1`, `HE-1` (`RV-001`) | Partial | Canonical `auditDigest` recomputation and duplicate ID rejection in `create_signed_access_review_record` are well scoped, but `audit_keyvault_data_plane_access` can emit duplicate `anomalyId`s on repeated wrong-vault diagnostic rows and lacks UTC timestamp normalization and strict `callerSummaries`/`systemNotificationCount` type checks before digest computation (`PC-002`). |
| `FR-H2`, `HE-2` (`RV-002`) | Partial | `allowedRoles` (`excess_rbac_privilege`) fits existing RBAC fixtures cleanly, but `wrong_vault_diagnostic` needs deduplication, evaluation prior to `PLATFORM_NOTIFICATION_OPS` skipping, rejection of non-`.vault.azure.net` URIs or non-KeyVault ARM resource IDs, and rejection of diagnostic rows lacking all vault-identifying fields (`PC-002`). |
| `FR-H3`, `HE-3` (`RV-003`) | Partial | Covers all four `RV-003` themes, but `P01-T01` leaves `ok` (`len(problems) == 0`) passing on insufficient `elapsedOverlapMinutes` unless a problem is appended, omits `elapsedOverlapMinutes` from `post_retire` `priorSwitchoverReceipt` verification and `retiredAt <= now` on `retiredPriorCredential`, and hits ordering bugs with `prior_version_id`/`next_version_id` and `before_kv_problems` (`PC-001`) plus shared `_validate_probe_batch` `rollback` behavior (`PC-003`). |
| `FR-H4`, `HE-4`, `HE-5` (`RV-004`, `RV-005`) | Partial | Covers scalar guards, review freshness bounds, and JSON-array `--ledger` append refusal, but needs scalar guard coverage in `validate_human_reviewer` without breaking short reviewer `"R"` in `access_review`, safe `reviewIntervalDays` parsing in `verify_access_review_ledger`, and exact symbol anchoring (`main()` `review-sign` branch and `_append_jsonl_entry` rather than nonexistent `_cmd_review_sign`) (`PC-003`). |
| `NFR-H1` | Covered | Static typing (`mypy` and `mypy --strict`), `ruff check` (default and isolated), `ruff format --check`, `test_dependency_rule.py`, and `bicep_inventory.py --check` match repository CI rules. |
| `P01`, `P01-T01` | Partial | Target files and overall architecture are sound, subject to the concrete contract corrections in `PC-001`..`PC-003`. |
| `P02`, `P02-T01` | Partial | Preserves all 40 existing tests (`exact removals: none`), but must explicitly update `infra/tests/test_secret_lifecycle.py` (`_rotation_payload`) alongside `src/core/tests/test_secret_lifecycle.py` (`_rotation_fixture`) for `freshTokenExchangeVerified` while preserving `rollback` fixture behavior (`PC-001`..`PC-003`). |

## Verdict

* Verdict: Revise
* Rationale: The child plan targets every routed review defect (`RV-001`..`RV-005`) within a clean two-phase scope, but symbol-level trace against `src/core/src/zava_forward/core/secret_lifecycle.py`, `infra/scripts/secret_lifecycle.py`, and both test suites reveals three substantive gaps (`PC-001`..`PC-003`) that would allow premature `post_switchover`/`post_retire` verification or misreported `versionSwitchoverVerified`, cause repeated foreign-vault diagnostic rows to emit unsignable duplicate `anomalyId`s or bypass vault-scope checks, and break `rollbackVerified` or CLI positive fixtures. All three require direct planner updates with no user decision needed.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Fail `problems`/`ok` on insufficient elapsed overlap, enforce `elapsedOverlapMinutes` and `retiredAt <= now` in `post_retire`, and fix `secretVersions` ordering in `verify_staged_entra_rotation`

* Related IDs: `FR-H3`, `HE-3`, `P01`, `P01-T01`, `P02`, `P02-T01`
* Evidence: src/core/src/zava_forward/core/secret_lifecycle.py (lines 397-403, 435-540, 609-632); infra/scripts/secret_lifecycle.py (line 258); .copilot-tracking/details/2026-11-15/kv-secret-lifecycle-142-hardening-phase-details.md (`P01-T01`)
* Concern: Three execution-path gaps exist in `P01-T01`'s `RV-003` specification for `verify_staged_entra_rotation`:
  1. `ok` is computed as `len(problems) == 0 and stage != "rollback"` (line 609), and CLI `rotation-verify` returns exit code `0` whenever `bool(receipt["ok"])` is `True` (`infra/scripts/secret_lifecycle.py` line 258). `P01-T01` specifies gating `overlap_ok = True` on `elapsedOverlapMinutes >= float(min_overlap_minutes)` in `post_switchover` without requiring a `problems.append(...)` failure when configured window `overlap_minutes >= min_overlap_minutes` passes but `elapsedOverlapMinutes < min_overlap_minutes` fails; that leaves `receipt["ok"] == True` and CLI exit `0` after a 1-second overlap.
  2. `P01-T01` omits `"elapsedOverlapMinutes"` from the explicit list of returned receipt keys, checks only `overlapMinutes >= min_overlap_minutes` (configured window overlap) rather than also `elapsedOverlapMinutes >= min_overlap_minutes` on `priorSwitchoverReceipt` during `post_retire`, and does not enforce `retired_at <= now` when `post_retire` uses `retiredPriorCredential` (lines 439-443 currently allow a future `retiredAt > now` to manufacture overlap).
  3. In `src/core/src/zava_forward/core/secret_lifecycle.py`, `post_retire` validates `priorSwitchoverReceipt` inside the `credentials` block (lines 450-462) before `prior_version_id` and `next_version_id` are parsed from `secretVersions` (lines 469-476), and `before_kv_problems = len(problems)` (line 507) sits after the `secretVersions.entries` URI loop (lines 483-501) while non-mapping rows in `secretVersions.entries` are silently skipped (`continue`), allowing `kv_versions_ok` and `versionSwitchoverVerified` to report `True` even when version URI validation recorded errors.
* Impact: `rotation-verify` could still exit `0` (`ok=True`) at `post_switchover` before the required soak has elapsed, `post_retire` could accept premature retirement via a future `retiredAt` or a receipt with unelapsed overlap, and `post_retire` receipt binding / `versionSwitchoverVerified` would fail or misreport due to check ordering.
* Smallest useful change: Update `P01-T01` and `P02-T01` so `verify_staged_entra_rotation`: (1) includes `"elapsedOverlapMinutes"` in the returned receipt and appends a `problems` message in `post_switchover` whenever `elapsedOverlapMinutes < float(min_overlap_minutes)`, (2) validates `priorSwitchoverReceipt` after `secretVersions` IDs are parsed, requiring `float(prior_receipt.get("elapsedOverlapMinutes", 0.0)) >= float(min_overlap_minutes)` alongside `overlapMinutes >= float(min_overlap_minutes)` and all eight identity fields, and enforces `retired_at <= now` (capping overlap at `min(rp_end, retired_at, now)` and `min(n_end, retired_at, now)`) for `retiredPriorCredential`, and (3) sets `before_kv_problems = len(problems)` before the `secretVersions.entries` loop and appends a problem on non-mapping rows or duplicate version entries. Add unit assertions in `P02-T01` verifying `ok is False` on 1-second elapsed overlap, rejection of future `retiredAt` in `post_retire`, and `versionSwitchoverVerified is False` on URI mismatch.
* Action owner: planning parent
* Exact resolving evidence: Updated `P01-T01` and `P02-T01` contracts in `.copilot-tracking/details/2026-11-15/kv-secret-lifecycle-142-hardening-phase-details.md` and `FR-H3` / Critique Disposition in `.copilot-tracking/plans/2026-11-15/kv-secret-lifecycle-142-hardening-plan.md` specifying all three invariants and corresponding negative tests.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-002 -->
### PC-002 [High]: Deduplicate `anomalyId`/`assignmentId` emission and close non-KeyVault, Event Grid, and missing-URI vault-scope bypasses across `RV-001` and `RV-002`

* Related IDs: `FR-H1`, `FR-H2`, `HE-1`, `HE-2`, `P01`, `P01-T01`, `P02`, `P02-T01`
* Evidence: src/core/src/zava_forward/core/secret_lifecycle.py (lines 289-300, 541-556, 600-683, 791-806, 840-936); .copilot-tracking/details/2026-11-15/kv-secret-lifecycle-142-hardening-phase-details.md (`P01-T01`)
* Concern: Three interacting audit/digest edge cases remain between `RV-001` and `RV-002`:
  1. `_add_anomaly` (lines 600-610) derives `anomalyId` deterministically from `f"{cleaned_vault}|{kind}|{principal_id}|{detail}"` and appends unconditionally without deduplicating. Under `P01-T01`'s per-row diagnostic check ("For each in-window diagnostic row... otherwise emit `wrong_vault_diagnostic`"), two diagnostic events targeting the same foreign vault URI/ResourceId emit duplicate `anomalyId` entries in `audit["anomalies"]`, which `FR-H1`'s new duplicate-`anomalyId` guard in `create_signed_access_review_record` will then refuse to sign. Duplicate identical tuples in `assignments` likewise produce duplicate `assignmentId` / `anomalyId` entries.
  2. In `audit_keyvault_data_plane_access`, vault-scope checking must execute before `if not pid and op in PLATFORM_NOTIFICATION_OPS: system_notification_count += 1; continue` (lines 677-679) so foreign-vault Event Grid notifications are flagged rather than counted as clean target-vault events. Furthermore, using `_extract_secret_uri_parts` alone only detects `.vault.azure.net` hosts: a non-KeyVault URI in `id_s`/`requestUri_s` (for example `https://evil.example/secrets/entra-client-secret`, from which `_extract_diag_secret_name` still extracts `entra-client-secret`), a non-KeyVault ARM `ResourceId`, a row where `id_s` matches `vault_name` while `ResourceId` names another vault, or a row stripped of all five URI/resource-ID fields (`id_s`, `requestUri_s`, `ResourceId`, `_ResourceId`, `resourceId`) and carrying only bare `secretName` would bypass `wrong_vault_diagnostic`.
  3. For `_compute_audit_digest` (`RV-001`), `audit_keyvault_data_plane_access` currently serializes `window_start.isoformat()` without normalizing non-UTC aware datetimes via `.astimezone(dt.UTC)` (whereas `create_signed_access_review_record` normalizes via `parse_time(...).isoformat()`), and `create_signed_access_review_record` does not validate that `audit["callerSummaries"]` is a `list` and `audit["systemNotificationCount"]` is a non-negative `int` (not `bool`) before recomputing the digest.
* Impact: Multi-row foreign-vault logs in real `AzureDiagnostics` exports would produce self-invalidating audit files that `review-sign` rejects for duplicate `anomalyId`, while foreign Event Grid rows, non-`.vault.azure.net` URIs, or stripped-URI rows with bare `secretName` could slip past `wrong_vault_diagnostic`.
* Smallest useful change: Specify in `P01-T01` and `P02-T01` that: (1) `audit_keyvault_data_plane_access` deduplicates anomalies by `anomalyId` (and deduplicates identical `(principalId, principalType, roleDefinitionName, scope)` RBAC rows or keys `assignmentId` uniquely), (2) diagnostic vault-scope validation runs before `PLATFORM_NOTIFICATION_OPS` handling, requires at least one non-empty vault-identifying field among `id_s`/`requestUri_s`/`ResourceId`/`_ResourceId`/`resourceId` (all existing test fixtures already include `id_s`), and verifies every present URI field parses as `https://<vault_name>.vault.azure.net/...` and every present ARM resource ID parses as `.../providers/Microsoft.KeyVault/vaults/<vault_name>(/...)` case-insensitively (omitting wrong-vault rows from target-vault `allowed_ops`/`_secret_allowed` approval or recording `wrong_vault_diagnostic` cleanly), and (3) `audit_keyvault_data_plane_access` normalizes `window_start`/`window_end` to `dt.UTC` and `create_signed_access_review_record` validates `callerSummaries` (`list`) and `systemNotificationCount` (non-boolean `int >= 0`) plus non-mapping row rejection before `_compute_audit_digest`. Add a multi-row wrong-vault diagnostic -> `create_signed_access_review_record` signing test in `P02-T01`.
* Action owner: planning parent
* Exact resolving evidence: Updated `P01-T01` and `P02-T01` sections in `.copilot-tracking/details/2026-11-15/kv-secret-lifecycle-142-hardening-phase-details.md` and Critique Disposition in `.copilot-tracking/plans/2026-11-15/kv-secret-lifecycle-142-hardening-plan.md` capturing deduplication, strict multi-field vault-scope parsing before `PLATFORM_NOTIFICATION_OPS`, and UTC/type normalization for `_compute_audit_digest`.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-003 -->
### PC-003 [Medium]: Preserve `rollback` probe and legacy `"R"` reviewer compatibility, update CLI rotation fixtures, and harden `reviewIntervalDays` and JSONL append edge cases

* Related IDs: `FR-H3`, `FR-H4`, `HE-3`, `HE-4`, `HE-5`, `P01`, `P01-T01`, `P02`, `P02-T01`
* Evidence: src/core/src/zava_forward/core/secret_lifecycle.py (lines 310-340, 361, 572-601, 820-831, 1018-1055); infra/scripts/secret_lifecycle.py (lines 168-191, 339-384); src/core/tests/test_secret_lifecycle.py (lines 56-88); infra/tests/test_secret_lifecycle.py (lines 195-204, 302-310)
* Concern: Four implementation and test-compatibility details across `RV-003`..`RV-005` need explicit precision in `P01-T01` and `P02-T01`:
  1. `_validate_probe_batch` is called by `stage == "rollback"` with `require_authenticated_probe=browser_mode` (line 579), whereas `_rotation_fixture("rollback")` (`src/core/tests/test_secret_lifecycle.py` lines 78-88) does not set `freshTokenExchangeVerified`. Enforcing `freshTokenExchangeVerified is True` inside `_validate_probe_batch` whenever `require_authenticated_probe` is `True` would break `test_rollback_stage_verifies_prior_restore_and_blocks_retirement` unless gated by a distinct `require_fresh_token_exchange` flag (`browser_mode and p_stage in {"post_switchover", "post_retire"}`). Additionally, `verify_staged_entra_rotation` line 361 (`bool(evidence.get("browserMode", True))`) silently treats `"browserMode": null` as `False`, and `P02-T01` must explicitly note updating `StagedRotationAndLedgerCliTests._rotation_payload` in `infra/tests/test_secret_lifecycle.py` (line 302) in addition to `_rotation_fixture` in `src/core/tests/test_secret_lifecycle.py`.
  2. `P01-T01` adds `assert_no_secret_material` to `access_review` (`reviewer`) and `rotation_plan` (`vault`, `app_id`), but `validate_human_reviewer` / `create_signed_access_review_record` also accept scalar `reviewer` strings before persisting signed ledger entries; adding `assert_no_secret_material` inside `validate_human_reviewer` (and on scalar `vault_name` / `expected_vault_name` inputs) closes that gap while keeping `validate_human_reviewer` out of legacy `access_review`, which must continue accepting 1-character reviewer `"R"` in `ReviewStatusTests.test_generated_record_is_not_complete_until_decided` (`infra/tests/test_secret_lifecycle.py` line 198).
  3. In `verify_access_review_ledger`, `P01-T01` writes `1 <= int(entry["reviewIntervalDays"]) <= max_interval_days`; unguarded `int(entry["reviewIntervalDays"])` raises uncaught `KeyError`/`TypeError`/`ValueError` (or accepts `True` as `1`) instead of recording a ledger problem and returning `intact=False`.
  4. `P01-T01` names `_cmd_review_sign` in `infra/scripts/secret_lifecycle.py`, which does not exist (`review-sign` lives in `main()` at line 339 and writes via `_append_jsonl_entry` at line 186); additionally, `_append_jsonl_entry` appends directly without checking whether an existing non-empty JSONL file lacks a trailing `\n`, which would concatenate two JSON objects onto one line.
* Impact: Without these clarifications, implementation risks breaking `rollbackVerified` and existing CLI tests, crashing `verify_access_review_ledger` on malformed `reviewIntervalDays` entries instead of returning `intact=False`, allowing credential patterns in signed `reviewer` names, or corrupting newline-stripped JSONL files.
* Smallest useful change: Clarify in `P01-T01` and `P02-T01`: (1) add a dedicated `require_fresh_token_exchange: bool = False` parameter on `_validate_probe_batch` (enabled for `browser_mode and p_stage in {"post_switchover", "post_retire"}`), require `browserMode` (when present) to be a `bool`, and update positive `post_switchover`/`post_retire` probes in both `src/core/tests/test_secret_lifecycle.py` and `infra/tests/test_secret_lifecycle.py`; (2) run `assert_no_secret_material` in `validate_human_reviewer` (preserving legacy `access_review` acceptance of `"R"`) and on scalar `vault_name`/`expected_vault_name` inputs; (3) validate `reviewIntervalDays` in `verify_access_review_ledger` without uncaught exceptions (`isinstance(raw, int) and not isinstance(raw, bool)`) and guard cross-field timestamp comparisons when individual timestamps fail `parse_time`; and (4) place the JSON-array `[` rejection in `main()`'s `review-sign` branch (before `load_ledger_entries`) and inside `_append_jsonl_entry`, prepending `\n` if an existing non-empty JSONL file does not end with `\n`.
* Action owner: planning parent
* Exact resolving evidence: Updated `P01-T01` and `P02-T01` contracts in `.copilot-tracking/details/2026-11-15/kv-secret-lifecycle-142-hardening-phase-details.md` and Critique Disposition in `.copilot-tracking/plans/2026-11-15/kv-secret-lifecycle-142-hardening-plan.md`.
* Decision route: direct planner correction

## Strengths and Residual Risk

* Complete `RV-001`..`RV-005` traceability: Every finding from `.copilot-tracking/reviews/logs/2026-11-15/kv-secret-lifecycle-142-review.md` maps cleanly to `FR-H1`..`FR-H4`, `P01-T01`, and `P02-T01` while keeping the parent review artifact immutable.
* Legacy CLI compatibility: Keeping all 19 original tests in `infra/tests/test_secret_lifecycle.py` intact (`exact removals: none`), preserving vault-level RBAC assignment scope compatibility for `token-maintenance`, and keeping `access_review` permissive of short placeholder reviewer strings (`"R"`) prevents regressions across `infra/tests`.
* Residual risk (explicitly accepted in plan `Follow-Up Items`): Live Azure staged Entra rotation execution and inaugural 90-day `AzureDiagnostics` export in the `ama` environment remain post-merge operator actions owned by `@jmservera` outside offline CI.

## Questions or Blocking Evidence Gaps

* None. All findings are deterministic planner corrections resolvable from the supplied repository artifacts.

## Limitations

* Critique is bounded strictly to the supplied plan, phase details, research, parent review log, and four source/test Python modules; `infra/README.md` was not modified or opened outside the supplied input set, and live Azure control-plane/data-plane behavior is not exercised offline.

## Recommended Next Action

* Highest-impact finding: `PC-001`
* Action owner: planning parent
* Smallest next action: Directly revise `.copilot-tracking/plans/2026-11-15/kv-secret-lifecycle-142-hardening-plan.md` and `.copilot-tracking/details/2026-11-15/kv-secret-lifecycle-142-hardening-phase-details.md` to incorporate `PC-001`..`PC-003`, record dispositions in `## Critique Disposition`, and finalize the plan for `rpi-implement` without another critique pass.
* User response required: no

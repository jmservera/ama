<!-- markdownlint-disable-file -->
# Changes Log: Final Precision Closure for Key Vault Secret Lifecycle (#142 Child Loop 3)

## Metadata

* Task ID: issue-142-final
* Task slug: kv-secret-lifecycle-142-final
* Plan path: `.copilot-tracking/plans/2026-11-15/kv-secret-lifecycle-142-final-plan.md`
* Phase details path: `.copilot-tracking/details/2026-11-15/kv-secret-lifecycle-142-final-phase-details.md`
* Date: 2026-11-15
* Status: completed

## P01: Core, CLI, and Runbook Precision Closure (`P01-T01`)

* Added `merge_vault_role_assignments` in `src/core/src/zava_forward/core/secret_lifecycle.py` and `rbac-merge` in `infra/scripts/secret_lifecycle.py` (`FR-F1` / `RV-001`) to unwrap ARM envelopes before secret-material inspection and merge `az role assignment list --scope <vault-id> --include-inherited` (root `/`, management groups, subscription, resource group, vault) with child `<vault-id>/secrets/*` assignments from `az role assignment list --all`, rejecting cross-subscription/RG `--inherited` inputs and ignoring non-secret child scopes.
* Tightened `verify_staged_entra_rotation(..., stage="rollback")` (`FR-F2` / `RV-002`) to require `freshTokenExchangeVerified: true` in browser mode and reject versionless rollback when `nextVersionId` is enabled or omitted from `secretVersions.entries` (or when another version on `priorSecretName` stays enabled).
* Added `_validate_stage_probe_batches` and bounded-gap probe window enforcement (`FR-F3` / `RV-003`, `PC-001`, `PC-002`) requiring strict integer `totalSamples >= min_probe_samples` (default `3`), `errorCount == 0`, guarded UTC `firstSampleAt < lastSampleAt <= now`, `span >= min_probe_span_seconds` (default `60`s), `0 < maxGapSeconds <= max_probe_gap_seconds` (default `60`s) with `(totalSamples - 1) * maxGapSeconds >= span`, intra-stage contiguity, chronological cross-stage ordering, and `post_retire.lastSampleAt > retiredAt`.
* Updated `rotation_plan()` (`FR-F4` / `RV-004`, `PC-004`) to emit the stdout-free `--years 1 --query password -o tsv | tr -d '\r\n' | az keyvault secret set ... --output none` pipeline while preserving all `NoDowntimeRotationTests` ordering invariants, and updated `infra/README.md`.

## P02: Deterministic Fixtures, Regression Tests, and Focused Validation (`P02-T01`)

* Updated `_rotation_fixture` in `src/core/tests/test_secret_lifecycle.py` and `_rotation_payload` in `infra/tests/test_secret_lifecycle.py` with bounded-gap probe sample timestamps (`firstSampleAt`, `lastSampleAt`, `maxGapSeconds`) and rollback durability inputs (`nextVersionId` disabled + `freshTokenExchangeVerified: true`).
* Added 5 focused semantic tests across `src/core/tests/test_secret_lifecycle.py` (4) and `infra/tests/test_secret_lifecycle.py` (1):
  * `test_merge_vault_role_assignments_preserves_root_mg_ancestors_and_child_secrets`
  * `test_rollback_requires_disabled_next_version_on_versionless_url_and_fresh_exchange`
  * `test_probe_batches_enforce_sample_count_span_gap_feasibility_and_post_retire_ordering`
  * `test_rotation_plan_streams_secret_without_stdout_exposure`
  * `test_rbac_merge_cli_preserves_root_and_mg_ancestors_and_feeds_access_audit`

## Validation Evidence

* `PYTHONPATH=src/core/src python3 -m unittest src/core/tests/test_secret_lifecycle.py src/core/tests/test_dependency_rule.py infra/tests/test_secret_lifecycle.py -q`: `Ran 56 tests in 2.351s — OK`
* `PYTHONPATH=src/core/src python3 -m unittest discover -s infra/tests -q`: `Ran 638 tests in 212.172s — OK (skipped=4)`
* `PYTHONPATH=src/core/src python3 infra/scripts/bicep_inventory.py --check`: `Issue #136 Bicep inventory verified`
* `(cd src/core && python3 -m ruff check && python3 -m ruff format --check && python3 -m mypy)`: `All checks passed! / 310 files already formatted / Success: no issues found in 363 source files`
* `python3 -m ruff check --isolated --line-length 100 infra/scripts/secret_lifecycle.py infra/tests/test_secret_lifecycle.py && python3 -m ruff format --isolated --line-length 100 --check infra/scripts/secret_lifecycle.py infra/tests/test_secret_lifecycle.py && MYPYPATH=src/core/src python3 -m mypy --strict --explicit-package-bases infra/scripts/secret_lifecycle.py infra/tests/test_secret_lifecycle.py`: `All checks passed! / 2 files already formatted / Success: no issues found in 2 source files`
* `git --no-pager diff src/ infra/ | grep -c '\.copilot-tracking'`: `0`
* `tools/rpi-checks.py --all`: Skipped intentionally per user instruction (`Validation tier: Focused; do not run tools/rpi-checks.py --all`).

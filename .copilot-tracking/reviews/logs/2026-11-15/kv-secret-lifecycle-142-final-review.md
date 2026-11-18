<!-- markdownlint-disable-file -->
# Review Log: Final Precision Closure for Key Vault Secret Lifecycle (#142 Child Loop 3)

## Metadata

* Task ID: issue-142-final
* Task slug: kv-secret-lifecycle-142-final
* Parent task: issue-142-seal (`kv-secret-lifecycle-142-seal`)
* Date: 2026-11-15
* Execution status: Complete
* Outcome: Defects found

## Compared Artifacts

* Research: `.copilot-tracking/research/2026-11-15/kv-secret-lifecycle-142-final-research.md`
* Plan: `.copilot-tracking/plans/2026-11-15/kv-secret-lifecycle-142-final-plan.md`
* Phase details: `.copilot-tracking/details/2026-11-15/kv-secret-lifecycle-142-final-phase-details.md`
* Plan critique: `.copilot-tracking/reviews/plans/2026-11-15/kv-secret-lifecycle-142-final-plan-critique.md`
* Changes log: `.copilot-tracking/changes/2026-11-15/kv-secret-lifecycle-142-final-changes.md`
* Prior review: `.copilot-tracking/reviews/logs/2026-11-15/kv-secret-lifecycle-142-seal-review.md`
* Source & tests inspected:
  * `src/core/src/zava_forward/core/secret_lifecycle.py`
  * `infra/scripts/secret_lifecycle.py`
  * `infra/README.md`
  * `src/core/tests/test_secret_lifecycle.py`
  * `infra/tests/test_secret_lifecycle.py`

## Validation Coverage

* `PYTHONPATH=src/core/src python3 -m unittest src/core/tests/test_secret_lifecycle.py src/core/tests/test_dependency_rule.py infra/tests/test_secret_lifecycle.py -q`: `56` tests passed (`OK`).
* `PYTHONPATH=src/core/src python3 -m unittest discover -s infra/tests -q`: `638` tests passed (`OK`, `skipped=4`).
* `PYTHONPATH=src/core/src python3 infra/scripts/bicep_inventory.py --check`: passed.
* `src/core` `ruff check`, `ruff format --check`, and `mypy`: passed (`363` files).
* `infra/scripts/secret_lifecycle.py` & `infra/tests/test_secret_lifecycle.py` `ruff check --isolated --line-length 100`, `ruff format --isolated --line-length 100 --check`, and `mypy --strict`: passed.
* `tools/rpi-checks.py --all`: Skipped intentionally per Focused validation tier instruction.

## Implementation-Time Updates & Follow-Up Assessment

* `PC-002` (guarded probe timestamp parsing), `PC-003` (`merge_vault_role_assignments` child-secret scope filtering), and `RV-004` (stdout-free `rotation_plan()` pipeline) are verified in code and tests.
* Live Azure staging rotation drill and inaugural live 90-day `AzureDiagnostics` + RBAC signed ledger entry remain appropriately tracked as operational follow-up items outside offline CI scope.

## Findings

### RV-001 (Major) — Versionless in-place Key Vault URL on rollback cannot fall back to an older version

* **Evidence**: `src/core/src/zava_forward/core/secret_lifecycle.py` (`verify_staged_entra_rotation`, `stage == "rollback"`) and `infra/README.md` (`### Rotate the Entra client secret`, step 4). Azure Key Vault versionless secret resolution (`GET /secrets/<name>`) resolves only the newest version (`max created`) and returns `403 SecretDisabled` when that newest version is disabled rather than falling back to an older enabled version. Allowing `u_ver is None` on in-place (`priorSecretName == secretName`) rollback when `nextVersionId` is disabled can certify a configuration that fails on Container Apps' next 30-minute secret poll.
* **Destination**: `rpi-implement` (require version-pinned `priorVersionId` `keyVaultUrl` for in-place `priorSecretName == secretName` rollback, and for two-name `priorSecretName != secretName` versionless rollback verify `priorVersionId` is the newest enabled version on `priorSecretName`; update `infra/README.md` step 4 accordingly).

### RV-002 (Major) — Probe sample windows are not bound to rotation event timestamps

* **Evidence**: `src/core/src/zava_forward/core/secret_lifecycle.py` (`verify_staged_entra_rotation`, stage probe window checks). Cross-stage chronological order is checked, but `dual_secret_overlap` and `post_switchover` probe windows are not verified against credential overlap start, `nextVersionId` creation (`created`), and traffic switchover (`containerApp.switchoverAt`), and `post_retire` checks `lastSampleAt > retiredAt` rather than `firstSampleAt >= retiredAt` (allowing nearly the entire `post_retire` window to precede retirement).
* **Destination**: `rpi-implement` (require `created` on `secretVersions.entries`, `containerApp.switchoverAt` on `post_switchover`/`post_retire`, `containerApp.rollbackAt` on `rollback`, and `retiredPriorCredential.retiredAt` or `credentials.priorRetiredAt` on `post_retire`, and bind each stage's `firstSampleAt` to its corresponding event floor so the full `>= min_probe_span_seconds` probe window runs post-event).

### RV-003 (Major) — Paginated ARM/Graph list envelopes (`nextLink` / `@odata.nextLink`) are silently truncated

* **Evidence**: `src/core/src/zava_forward/core/secret_lifecycle.py` (`unwrap_arm_list_envelope`). Non-empty `nextLink` or `@odata.nextLink` fields are accepted and discarded, allowing a truncated first-page RBAC or diagnostics envelope to pass `rbac-merge` and `access-audit`.
* **Destination**: `rpi-implement` (reject non-empty `nextLink` / `@odata.nextLink` in `unwrap_arm_list_envelope` with `SecretLifecycleError` after running `assert_no_secret_material`).

### RV-004 (Major) — Unvalidated status/enum values reflected via `!r` in `problems` can echo unlabelled secrets

* **Evidence**: `src/core/src/zava_forward/core/secret_lifecycle.py` (`_validate_probe_batch`, `verify_staged_entra_rotation`, `review_status`, `create_signed_access_review_record`, `verify_access_review_ledger`, `merge_vault_role_assignments`). Interpolating unvalidated input values with `!r` (e.g., `healthzStatus`) into `problems` can echo an unlabelled secret string that did not match heuristic key/regex filters.
* **Destination**: `rpi-implement` (sanitize all status/enum/date/scope problem messages so unvalidated arbitrary strings are never reflected into receipts, ledgers, or exceptions).

### RV-005 (Minor) — `NaN` / `Infinity` bypass numeric comparisons

* **Evidence**: `src/core/src/zava_forward/core/secret_lifecycle.py` (`_validate_probe_batch`, `_parse_non_negative_float`, `assert_no_secret_material`) and `infra/scripts/secret_lifecycle.py` (`json.loads`). IEEE `NaN` makes `<= 0` and `> max_probe_gap_seconds` both `False`, bypassing `maxGapSeconds` validation, and Python `json.loads` accepts `NaN`/`Infinity` by default.
* **Destination**: `rpi-implement` (reject non-finite floats via `math.isfinite` in `assert_no_secret_material`, `_validate_probe_batch`, and `_parse_non_negative_float`, and reject non-standard JSON constants via `parse_constant` in `infra/scripts/secret_lifecycle.py`).

### RV-006 (Minor) — Runbook `--end-date` vs `--years 1` drift and untracked-file `.copilot-tracking` check

* **Evidence**: `infra/README.md` (`### Rotate the Entra client secret`, step 1 uses `--end-date <iso>` while `rotation_plan()` uses `--years 1`), `.copilot-tracking/details/2026-11-15/kv-secret-lifecycle-142-final-phase-details.md` wording prior to `PC-001`, and `git diff` excluding untracked files.
* **Destination**: `rpi-implement` (standardize `--years 1` in `infra/README.md` step 1 and verify `grep -rn '\.copilot-tracking' src/ infra/` across tracked and untracked files).

## Routing Summary

* Route `RV-001`..`RV-006` to a bounded child RPI loop (`issue-142-conformant` / `kv-secret-lifecycle-142-conformant`) for surgical implementation, Focused validation, and conformant review before committing on `feat/infra-142-kv-secret-lifecycle`.

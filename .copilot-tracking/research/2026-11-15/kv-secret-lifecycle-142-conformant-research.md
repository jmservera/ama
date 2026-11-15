<!-- markdownlint-disable-file -->
# Research Synthesis: Conformance Closure for Key Vault Secret Lifecycle (#142 Child Loop 4)

## Metadata

* Task ID: issue-142-conformant
* Task slug: kv-secret-lifecycle-142-conformant
* Parent task: issue-142-final (`kv-secret-lifecycle-142-final`)
* Date: 2026-11-15
* Research disposition: reused
* Planning Readiness: Ready

## Evidence Summary (`CE-1`..`CE-6`)

* **CE-1 (`RV-001` — Azure Key Vault versionless secret resolution on rollback)**:
  * Azure Key Vault REST `GET {vaultBaseUrl}/secrets/{secret-name}` (versionless) resolves exclusively to the newest secret version (`max created`) and returns `403 Forbidden (SecretDisabled)` if that newest version has `enabled: false`; it never falls back to an older enabled version.
  * Consequently, for an in-place single-name secret (`priorSecretName.lower() == secretName.lower()`), `verify_staged_entra_rotation(..., stage="rollback")` must require `containerApp.secrets[].keyVaultUrl` to pin `priorVersionId` (`https://<vault>.vault.azure.net/secrets/<secretName>/<priorVersionId>`). For a two-name staged switchover (`priorSecretName.lower() != secretName.lower()`), versionless `https://<vault>.vault.azure.net/secrets/<priorSecretName>` is valid only when `priorVersionId` is enabled and has strictly the newest `created` timestamp among all `secretVersions.entries` on `priorSecretName` (with no other version on `priorSecretName` enabled). Similarly, for versionless `post_switchover` and `post_retire`, `nextVersionId` must have strictly the newest `created` timestamp among `secretVersions.entries` on `secretName`.
* **CE-2 (`RV-002` — Event-bound probe windows)**:
  * Requiring `created` (ISO-8601 `created`/`createdAt` or Unix epoch `attributes.created`/`created`) on `secretVersions.entries`, `containerApp.switchoverAt` on `post_switchover` and `post_retire` (with `switchoverAt >= max(overlapStart + minOverlapMinutes, nextVersionCreated)` and `switchoverAt <= now`), `containerApp.rollbackAt` on `rollback` (with `rollbackAt >= priorStart` and `rollbackAt <= now`), and `retiredAt` (`credentials.retiredPriorCredential.retiredAt` or `credentials.priorRetiredAt`, `<= now` and `>= post_switchover.lastSampleAt` when present) on `post_retire` lets `verify_staged_entra_rotation` bind every stage's `firstSampleAt` to its causal event floor:
    * `dual_secret_overlap`: `firstSampleAt >= max(overlapStart, nextVersionCreated)`
    * `post_switchover`: `firstSampleAt >= switchoverAt`
    * `post_retire`: `firstSampleAt >= retiredAt` (guaranteeing at least `min_probe_span_seconds` of post-retirement sampling after credential deletion)
    * `rollback`: `firstSampleAt >= rollbackAt`
* **CE-3 (`RV-003` — Truncated ARM/Graph paginated envelopes)**:
  * `unwrap_arm_list_envelope` must inspect `payload` with `assert_no_secret_material` first and then raise `SecretLifecycleError` whenever `"nextLink"` or `"@odata.nextLink"` is present and non-empty (`payload.get(k) not in (None, "")`).
* **CE-4 (`RV-004` — Sanitized error/problem formatting without input reflection)**:
  * Replacing raw `{val!r}` interpolation of unvalidated inputs (`healthzStatus`, `anonymousApiStatus`, `signInRedirectStatus`, `authenticatedApiStatus`, invalid `stage`, invalid `decision`/`disposition`, invalid `nextReviewDue`, unknown `signingKeyId`, invalid `inherited_assignments` scope) with bounded enum/integer formatters prevents accidental unlabelled secret strings from leaking into `problems` or exception messages.
* **CE-5 (`RV-005` — Non-finite float and JSON constant rejection)**:
  * Rejecting `isinstance(payload, float) and not math.isfinite(payload)` inside `assert_no_secret_material` (plus `math.isfinite` in `_validate_probe_batch` and `_parse_non_negative_float`) and parsing CLI JSON/JSONL inputs with `json.loads(..., parse_constant=_reject_json_constant)` blocks `NaN`, `Infinity`, and `-Infinity` across both Python and CLI callers.
* **CE-6 (`RV-006` — Runbook `--years 1` parity & repo-wide `.copilot-tracking` check)**:
  * Aligning `infra/README.md` step 1 to `--years 1` (matching `rotation_plan()`) and running `grep -rn '\.copilot-tracking' src/ infra/` verifies tracked and untracked source/test/doc files alike.

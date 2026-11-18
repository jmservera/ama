<!-- markdownlint-disable-file -->
# Review: Verification Hardening for Key Vault Secret Lifecycle (#142 Child Loop)

## Scope and Evidence

* Task ID: issue-142-hardening
* Review date: 2026-11-15
* Review scope: Full plan (`P01`, `P02`)
* Assessed boundary: Resolution of parent review findings `RV-001`..`RV-005` and child critique findings `PC-001`..`PC-003` across `src/core/src/zava_forward/core/secret_lifecycle.py`, `infra/scripts/secret_lifecycle.py`, `infra/README.md`, `src/core/tests/test_secret_lifecycle.py`, and `infra/tests/test_secret_lifecycle.py` under Focused validation.
* Plan: .copilot-tracking/plans/2026-11-15/kv-secret-lifecycle-142-hardening-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/kv-secret-lifecycle-142-hardening-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-11-15/kv-secret-lifecycle-142-hardening-plan-critique.md
* Changes: .copilot-tracking/changes/2026-11-15/kv-secret-lifecycle-142-hardening-changes.md
* Other evidence considered: .copilot-tracking/research/2026-11-15/kv-secret-lifecycle-142-hardening-research.md; .copilot-tracking/reviews/logs/2026-11-15/kv-secret-lifecycle-142-review.md; `infra/role-assignments.json`; Focused validation outputs (`48` + `138` + `636` unittest passes, `ruff`, `mypy`, `bicep_inventory.py --check`); bounded read-only `rubber-duck` verification lens (`review-lens-142-hardening`).

## Opening Review State

* Interpreted review goal: Verify that parent findings `RV-001`..`RV-005` and child critique dispositions `PC-001`..`PC-003` are closed without introducing or leaving substantive verification bypasses, scope escalations, or secret-exposure risks.
* Review scope: Full plan (`P01`, `P02`)
* Evidence readiness: Ready; all plan markers, phase details, critique dispositions, changes evidence, and Focused validation outputs are reconciled.
* Acceptance basis: `FR-H1`..`FR-H4`, `NFR-H1`, `PC-001`..`PC-003`, and Issue #142's rotation and scheduled access-review acceptance criteria.
* First comparison boundary: `src/core/src/zava_forward/core/secret_lifecycle.py`, `infra/scripts/secret_lifecycle.py`, `infra/README.md`, and `infra/role-assignments.json`.
* Active read-only boundaries: Review writes only `.copilot-tracking/reviews/logs/2026-11-15/kv-secret-lifecycle-142-hardening-review.md` and does not mutate implementation or planning files.
* Initial blockers: none

## Execution Status

* Execution status: Complete
* Review execution evidence: Completed on 2026-11-15 across reconciled plan, phase details, critique, changes log, source/test diffs, `infra/role-assignments.json`, and an independent read-only `rubber-duck` lens (`review-lens-142-hardening`).

## Plan-to-Change Reconciliation

| Current plan scope | Descriptive changes-record summary | Current-state reconciliation | Gap or rationale |
|--------------------|------------------------------------|------------------------------|------------------|
| `P01` (`P01-T01`) | Harden Core Verification, Access Review Integrity & CLI Ledger Guard | Reconciled | Planned `RV-001`..`RV-005` and `PC-001`..`PC-003` edits implemented in core, CLI, and `infra/README.md`; deeper verification-seal defects identified below (`RV-001`..`RV-004`). |
| `P02` (`P02-T01`) | Add Negative Regression Tests & Focused Validation | Reconciled | 22 core tests and 24 infra tests implemented and passing alongside 636 `infra/tests`, `ruff`, `mypy`, and `bicep_inventory.py --check`. |
| `Follow-Up Items` | Live Azure rotation drill and inaugural live 90-day access-review ledger entry | Reconciled | Preserved outside offline repository CI scope under owner `@jmservera`. |

## Completed Work Assessment

| Related marker | Files | What changed and why | Completion evidence | Validation | Assessment |
|----------------|-------|----------------------|---------------------|------------|------------|
| `P01` / `P01-T01` | `src/core/src/zava_forward/core/secret_lifecycle.py`, `infra/scripts/secret_lifecycle.py`, `infra/README.md` | Added canonical `_compute_audit_digest` check, `allowedRoles` + `_validate_diag_row_vault`, `elapsedOverlapMinutes` + `freshTokenExchangeVerified` + versioned URI + 8-field receipt checks, freshness bounds, scalar secret guards, and JSONL array/newline guard | Diff and symbol verification confirm all planned `PC-001`..`PC-003` mechanics | Passed `ruff`, `mypy`, `bicep_inventory.py --check`, and unit/CLI suites | Partial defect gap (`RV-001`..`RV-004` below) |
| `P02` / `P02-T01` | `src/core/tests/test_secret_lifecycle.py`, `infra/tests/test_secret_lifecycle.py` | Added negative regression tests for forged digests, excess roles, wrong-vault diagnostics, short overlap, missing fresh token exchange, unbound receipts, future/stale review dates, canary scalars, and JSON array `--ledger` refusal | 46 lifecycle tests + 2 dependency-rule tests pass in 2.44s; 636 `infra/tests` pass | Passed Focused validation | Reconciled for planned cases; needs tests for `RV-001`..`RV-004` |

## Implementation-Time Plan and Detail Update Assessment

| Affected area or marker | What changed and why | Triggering evidence and user decision | Reconciliation performed | Planning and critique state | Assessment |
|-------------------------|----------------------|---------------------------------------|--------------------------|-----------------------------|------------|
| `P01-T01` (`NFR-H1` lint alignment) | Simplified `parse_time`, `_secret_allowed`, and `firstSeen`/`lastSeen` clamping for isolated `ruff` compliance | Isolated `ruff check` during Focused validation; local judgment | Recorded under `## Implementation Discoveries and Decisions` in changes record | No plan revision needed; `PC-001`..`PC-003` preserved | Reconciled |

## Critique and Material Revision Assessment

* Latest critique dispositions: `PC-001`, `PC-002`, and `PC-003` were all applied directly in planning and implemented in `P01-T01`/`P02-T01`.
* Material revisions: None occurred during implementation.
* Dependent-work pause assessment: `P02` executed after `P01` completed; no premature resumption occurred.
* Justification assessment: Local `ruff` simplifications preserved approved behavior.

## Plan Follow-Up Assessment

| Follow-up item | Why outside immediate scope | Owner or next action | Assessment and route |
|----------------|-----------------------------|----------------------|----------------------|
| Live Azure test-environment staged Entra rotation drill | Requires live tenant/vault mutation and deployed Container App session | `@jmservera` | Distinct operational follow-up |
| Live 90-day Log Analytics + RBAC export and inaugural signed ledger record | Requires live deployed vault diagnostics and operator `HMAC-SHA256` signing secret | `@jmservera` | Distinct operational follow-up |

Unresolved plan follow-up items remain distinct follow-up work. Do not treat them as defects or add them to active `Pxx` or `Pxx-Txx` implementation, completion, or acceptance scope.

## Findings

<!-- rpi:review id=RV-001 -->
### RV-001 [High]: `verify_staged_entra_rotation` allows untrusted `browserMode: false`, string `"enabled": "false"`, untrusted URI echoing, and unsigned `priorSwitchoverReceipt`

* Related scope: `P01-T01`
* Evidence: `src/core/src/zava_forward/core/secret_lifecycle.py` (`verify_staged_entra_rotation`, `_parse_entra_credentials`, `_parse_secret_versions`, `_validate_health_probes`, `priorSwitchoverReceipt` branch)
* Impact: Evidence JSON setting `"browserMode": false` bypasses `signInRedirectStatus`, `authenticatedApiStatus`, and `freshTokenExchangeVerified` while still returning `safeToRetirePriorCredential=True` unless browser mode is required by verifier configuration; string `"enabled": "false"` evaluates truthy under `bool(...)`; malformed version URIs are echoed verbatim into `problems` (risking leakage if an operator misplaces secret text inside `id`); and `priorSwitchoverReceipt` at `post_retire` accepts an unsigned JSON dict with a fabricated hex `evidenceDigest` when no HMAC signature is verified.
* Destination: `rpi-implement`
* Smallest useful next action: Require `browserMode is True` by default (`require_browser_mode: bool = True`, opt-out only via explicit CLI flag/parameter), enforce strict `isinstance(..., bool)` on `enabled` fields in Entra credentials and Key Vault secret versions, avoid echoing raw `id` strings in `problems`, and require HMAC-SHA256 receipt signing/verification (`signing_key` / `--signing-key-env`) whenever `priorSwitchoverReceipt` is used in place of `retiredPriorCredential`.

<!-- rpi:review id=RV-002 -->
### RV-002 [High]: `audit_keyvault_data_plane_access` does not enforce secret-level RBAC assignment scope from `infra/role-assignments.json`

* Related scope: `P01-T01`
* Evidence: `src/core/src/zava_forward/core/secret_lifecycle.py` (`default_expected_caller_policy`, `audit_keyvault_data_plane_access`); `infra/role-assignments.json`; `infra/README.md` (`### Access review`)
* Impact: `infra/role-assignments.json` scopes `token-maintenance` (`Key Vault Secrets Officer`) strictly to `Secret entra-token-store-sas only` and `resident-demo` (`Key Vault Secrets User`) strictly to `resident-demo-password-verifier` and `resident-demo-session-key`, whereas `api` is scoped to `Key Vault`. Checking only `allowedRoles` accepts a vault-wide or RG-inherited `Key Vault Secrets Officer` assignment on `token-maintenance` (allowing it to overwrite `entra-client-secret`) without raising `excess_rbac_privilege`, and `infra/README.md`'s `az role assignment list --scope <vault-id> --include-inherited` command omits child-secret scopes unless `--all` filtered by `<vault-id>` prefix is used.
* Destination: `rpi-implement`
* Smallest useful next action: Encode allowed ARM scopes (`vault` vs exact `/secrets/<name>` child scopes) in `default_expected_caller_policy`, flag `excess_rbac_privilege` whenever an assignment's `scope` is broader than or outside the identity's allowed vault/secret scopes (including subscription/RG parent scopes), and update `infra/README.md`'s `az role assignment list` command to capture both inherited/vault and child-secret scopes.

<!-- rpi:review id=RV-003 -->
### RV-003 [Medium]: Access review signing and ledger verification allow 1-second audit windows, unreviewed gaps between ledger entries, and midnight-start due-date expiry

* Related scope: `P01-T01`
* Evidence: `src/core/src/zava_forward/core/secret_lifecycle.py` (`create_signed_access_review_record`, `verify_access_review_ledger`)
* Impact: `windowStart < windowEnd` accepts a 1-second diagnostic window as a valid quarterly review, multi-entry ledger verification does not verify `entry[i].windowStart <= entry[i-1].windowEnd < entry[i].windowEnd` continuity (allowing multi-week gaps between reviews), and `due_dt = parse_time(f"{next_due}T00:00:00+00:00")` marks a review overdue at `00:00:01Z` on its stated due date rather than end-of-day UTC (`23:59:59.999999+00:00`).
* Destination: `rpi-implement`
* Smallest useful next action: Enforce minimum window coverage (`reviewIntervalDays` by default on initial/standalone records unless an explicit `min_window_days` override is supplied), enforce contiguous `windowStart <= prev_window_end < windowEnd` and monotonic `reviewedAt >= prev_reviewed_at` across chained ledger entries, and evaluate `nextReviewDue` overdue status against end-of-day UTC (`now.date() > due_date`).

<!-- rpi:review id=RV-004 -->
### RV-004 [High]: `infra/README.md` rotation step 1 shows bare `az ad app credential reset --append` which prints the new password to stdout by default

* Related scope: `P01-T01`
* Evidence: `infra/README.md` (`### Rotate the Entra client secret`, step 1)
* Impact: Although step 1 instructs operators to write the new secret version in Key Vault "without printing its value", bare `az ad app credential reset --id <app-id> --append ...` prints JSON containing the plaintext `password` to stdout unless piped directly with `--query password -o tsv` into `az keyvault secret set ... --value @- --output none`. Additionally, `auditDigest` should be explicitly described as a canonical SHA-256 integrity checksum authenticated under the reviewer's `HMAC-SHA256` signature rather than standalone origin authentication.
* Destination: `rpi-implement`
* Smallest useful next action: Update step 1 in `infra/README.md` to show a secret-safe stdout-free `az ad app credential reset ... --query password -o tsv | az keyvault secret set ... --value @- --output none` pipeline (retrieving `keyId` via metadata-only `az ad app credential list`), and clarify `auditDigest` checksum semantics in `infra/README.md` and module docstrings.

## Defects

* `RV-001` (`High`) -> `rpi-implement`
* `RV-002` (`High`) -> `rpi-implement`
* `RV-003` (`Medium`) -> `rpi-implement`
* `RV-004` (`High`) -> `rpi-implement`

## Routed Findings

| Finding | Destination | Owner or next action | Reason for route |
|---------|-------------|----------------------|------------------|
| `RV-001` | `rpi-implement` | Tighten `require_browser_mode=True` default, strict bool `enabled`, redacted URI error messages, and HMAC-signed `priorSwitchoverReceipt` | Implementation defect in rotation verifier |
| `RV-002` | `rpi-implement` | Enforce vault vs `/secrets/<name>` RBAC scope matching in `access-audit` and update `infra/README.md` RBAC export query | Implementation and runbook defect in RBAC scope check |
| `RV-003` | `rpi-implement` | Enforce review window coverage, cross-entry window continuity, and end-of-day UTC `nextReviewDue` evaluation | Implementation defect in ledger coverage verification |
| `RV-004` | `rpi-implement` | Replace bare `az ad app credential reset` snippet with stdout-free pipeline to `az keyvault secret set --value @- --output none` and clarify `auditDigest` checksum wording | Runbook secret-handling defect |

Later implementation of a routed finding does not require another Review.

## Residual Work

* Live operator-attended staged Entra client-secret rotation drill in `ama` test environment (`@jmservera`).
* Inaugural live 90-day Log Analytics `AzureDiagnostics` + RBAC snapshot export and signed access-review ledger entry (`@jmservera`).

## Blockers and Remaining Work

* Blockers: none for offline repository scope; `RV-001`..`RV-004` routed to child follow-up loop before commit.
* Remaining active work: none inside `issue-142-hardening` (`P01` and `P02` completed).

## Validation Evidence

| Command | Scope | Status | Summary |
|---------|-------|--------|---------|
| `PYTHONPATH=src/core/src python3 -m unittest src/core/tests/test_secret_lifecycle.py src/core/tests/test_dependency_rule.py infra/tests/test_secret_lifecycle.py -q` | Core + CLI secret lifecycle & dependency rule | Passed | `Ran 48 tests in 2.441s - OK` |
| Expanded 7-module targeted suite (`test_secret_lifecycle`, `test_dependency_rule`, `test_identity_rbac`, `test_diagnostic_log_privacy`, `test_bicep_architecture_inventory_136`, `test_bicep_policy`) | Core + infra security/RBAC/Bicep invariants | Passed | `Ran 138 tests in 91.329s - OK` |
| `PYTHONPATH=src/core/src python3 -m unittest discover -s infra/tests -q` | Full `infra/tests` suite | Passed | `Ran 636 tests in 233.297s - OK (skipped=4)` |
| `python3 infra/scripts/bicep_inventory.py --check` | Issue #136 Bicep inventory | Passed | `29 architecture rows, 20 Bicep modules, 12 from-empty steps` |
| `(cd src/core && python3 -m ruff check . && python3 -m ruff format --check . && python3 -m mypy)` | `src/core` lint, format, and static types | Passed | `All checks passed!`, `310 files already formatted`, `363 source files` clean |
| Isolated `ruff check` + `ruff format --check` + `MYPYPATH=src/core/src mypy --strict` | `infra/scripts/secret_lifecycle.py` & `infra/tests/test_secret_lifecycle.py` | Passed | `All checks passed!`, `2 files already formatted`, `2 source files` clean |
| `tools/rpi-checks.py --all` | Full local gate | Skipped | Explicitly excluded by user prompt (Focused validation tier) |

## Outcome

* Outcome: Defects found
* Outcome rationale: All five parent findings (`RV-001`..`RV-005`) and child critique items (`PC-001`..`PC-003`) were implemented and tested, but independent review surfaced four deeper verification and runbook-safety gaps (`RV-001`..`RV-004`) that should be sealed before final commit.

## Closeout Routing Record

| Finding class | Destination | Owner or next action |
|---------------|-------------|----------------------|
| Implementation defect | `rpi-implement` | Child follow-up loop (`RV-001`..`RV-004`) |
| Decision gap or invalid assumption | none | none |
| Material evidence gap | none | none |
| Non-blocking residual work | distinct follow-up | Live Azure rotation drill & inaugural live 90-day ledger entry (`@jmservera`) |

* Execution status: Complete
* Outcome: Defects found
* Validation coverage: Focused tier passed (`48` + `138` + `636` unittest passes, `ruff check`, `ruff format --check`, `mypy`, `bicep_inventory.py --check`).
* Blockers: none

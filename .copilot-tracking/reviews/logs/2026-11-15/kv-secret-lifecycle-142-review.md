<!-- markdownlint-disable-file -->
# Review: Key Vault Secret Lifecycle Rotation Verification and Scheduled Access Review (#142)

## Scope and Evidence

* Task ID: issue-142
* Review date: 2026-11-15
* Review scope: Full task (`P01` through `P04`, `P01-T01` through `P04-T02`)
* Assessed boundary: Requirements `FR-1`..`FR-5` and `NFR-1`..`NFR-2`, resolved critique findings `PC-001`..`PC-005`, `src/core/src/zava_forward/core/secret_lifecycle.py`, `infra/scripts/secret_lifecycle.py`, `src/core/tests/test_secret_lifecycle.py`, `infra/tests/test_secret_lifecycle.py`, `infra/README.md`, and Focused validation evidence.
* Plan: .copilot-tracking/plans/2026-11-15/kv-secret-lifecycle-142-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/kv-secret-lifecycle-142-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-11-15/kv-secret-lifecycle-142-plan-critique.md
* Changes: .copilot-tracking/changes/2026-11-15/kv-secret-lifecycle-142-changes.md
* Other evidence considered: .copilot-tracking/research/2026-11-15/kv-secret-lifecycle-142-research.md (`C1`-`C17`), Focused validation command outputs, and independent read-only logic/security review lens.

## Opening Review State

* Interpreted review goal: Verify independently and from repository evidence whether the completed implementation, tests, documentation, and Focused validation satisfy Issue #142's approved plan (`FR-1`..`FR-5`, `NFR-1`, `NFR-2`) and critique dispositions (`PC-001`..`PC-005`) without secret exposure, regression, or overclaim of live Azure execution.
* Review scope: Full task (`P01` through `P04`, `P01-T01` through `P04-T02`)
* Evidence readiness: Ready; plan markers, phase details, plan critique (`PC-001`..`PC-005`), and changes record (`Status: Complete`, `Review readiness: ready`) are reconciled and available.
* Acceptance basis: `FR-1`..`FR-5`, `NFR-1`..`NFR-2`, five plan acceptance criteria, and critique dispositions `PC-001`..`PC-005`.
* First comparison boundary: Reconcile `P01`..`P04` plan markers and requirements against `src/core/src/zava_forward/core/secret_lifecycle.py`, `infra/scripts/secret_lifecycle.py`, unit/CLI test suites, and `infra/README.md`.
* Active read-only boundaries: Read-only across source code, tests, documentation, research, plan, phase details, critique, and changes record; write authority restricted strictly to `.copilot-tracking/reviews/logs/2026-11-15/kv-secret-lifecycle-142-review.md` (and parent RPI state file).
* Initial blockers: none

## Execution Status

* Execution status: Complete
* Review execution evidence: Completed 2026-11-15 across the full `P01`..`P04` boundary (`kv-secret-lifecycle-142-plan.md`, `kv-secret-lifecycle-142-phase-details.md`, `kv-secret-lifecycle-142-plan-critique.md`, `kv-secret-lifecycle-142-changes.md`, `src/core/src/zava_forward/core/secret_lifecycle.py`, `infra/scripts/secret_lifecycle.py`, `src/core/tests/test_secret_lifecycle.py`, `infra/tests/test_secret_lifecycle.py`, `infra/README.md`, Focused validation outputs, and an independent `rubber-duck` logic/security lens).

## Plan-to-Change Reconciliation

| Current plan scope | Descriptive changes-record summary | Current-state reconciliation | Gap or rationale |
|--------------------|------------------------------------|------------------------------|------------------|
| `P01` / `P01-T01` | Pure Secret Lifecycle Verification and Signed Ledger Module | Reconciled | `src/core/src/zava_forward/core/secret_lifecycle.py` created and matched to `P01-T01`; five hardening defects (`RV-001`..`RV-005`) routed to follow-up `rpi-implement`. |
| `P02` / `P02-T01` | CLI Wrapper and Backward-Compatible Orchestration | Reconciled | `infra/scripts/secret_lifecycle.py` exposes `rotation-verify`, `access-audit`, `review-sign`, and `ledger-verify` while preserving all 19 legacy tests; JSON-array append edge case captured in `RV-005`. |
| `P03` / `P03-T01`, `P03-T02` | Deterministic Core and CLI Lifecycle Tests | Reconciled | 40 unit and CLI contract tests (`17` core + `23` infra) authored and passing; edge-case regression tests for `RV-001`..`RV-005` routed with their fixes. |
| `P04` / `P04-T01`, `P04-T02` | Operator Documentation and Focused Validation | Reconciled | `infra/README.md` updated cleanly without `.copilot-tracking/` leaks or `#136` inventory drift; Focused validation (`unittest`, `ruff`, `mypy`, `bicep_inventory.py --check`) passed. |
| `Follow-Up Items` | Live Azure test-environment rotation drill and inaugural quarterly `AzureDiagnostics` export | Reconciled | Preserved outside offline CI claims and mirrored in both `kv-secret-lifecycle-142-plan.md` and `kv-secret-lifecycle-142-changes.md`. |

## Completed Work Assessment

| Related marker | Files | What changed and why | Completion evidence | Validation | Assessment |
|----------------|-------|----------------------|---------------------|------------|------------|
| `P01`, `P01-T01` | `src/core/src/zava_forward/core/secret_lifecycle.py` | Pure domain implementation of zero-secret guards, staged Entra rotation verification, `AzureDiagnostics` + RBAC caller auditing, and HMAC-SHA256 hash-chained review ledgers. | Module present with zero external dependencies. | `mypy` (363 files), `ruff`, `test_dependency_rule.py`, and 17 unit tests passed. | Implemented; hardening gaps `RV-001`..`RV-004` routed to child `rpi-implement`. |
| `P02`, `P02-T01` | `infra/scripts/secret_lifecycle.py` | CLI wrapper preserving legacy subcommands and adding `rotation-verify`, `access-audit`, `review-sign`, and `ledger-verify` with outside-repo `0600` non-symlink key-file validation. | CLI subcommands operational and backward compatible. | `ruff` (default + isolated `E,F,I,B,UP`), `ruff format --check`, `mypy --strict`, and 23 infra tests passed. | Implemented; JSON-array ledger append guard (`RV-005`) routed to child `rpi-implement`. |
| `P03`, `P03-T01`, `P03-T02` | `src/core/tests/test_secret_lifecycle.py`, `infra/tests/test_secret_lifecycle.py` | Added 17 core tests and 4 CLI/repo-contract tests while strictly typing existing helpers without modifying the 19 legacy assertions. | 40 lifecycle tests + 635 total `infra/tests` passing. | `unittest`, `ruff`, and `mypy --strict` passed. | Reconciled; add regression coverage for `RV-001`..`RV-005` in child task. |
| `P04`, `P04-T01`, `P04-T02` | `infra/README.md` | Documented zero-downtime staged Entra rotation + rollback and 90-day `AzureDiagnostics` + RBAC signed ledger contract. | `infra/README.md` diff clean, ASCII-compliant, no `.copilot-tracking/` paths. | `bicep_inventory.py --check` and `test_bicep_architecture_inventory_136.py` (8 tests) passed. | Reconciled. |

## Implementation-Time Plan and Detail Update Assessment

| Affected area or marker | What changed and why | Triggering evidence and user decision | Reconciliation performed | Planning and critique state | Assessment |
|-------------------------|----------------------|---------------------------------------|--------------------------|-----------------------------|------------|
| `P02-T01` (`infra/scripts/secret_lifecycle.py`) | Prepended worktree `src/core/src/zava_forward/core` to `sys.modules["zava_forward.core"].__path__` when already imported so full `infra/tests` discovery loads this worktree's module instead of a sibling worktree editable install. | Multi-worktree `unittest discover -s infra/tests` import ordering; local judgment preserving approved isolation intent (`C16`). | Recorded in `kv-secret-lifecycle-142-changes.md` under `## Implementation-Time Plan and Detail Updates`. | Not needed (ordinary local implementation judgment preserving `NFR-2`). | Reconciled and justified. |

## Critique and Material Revision Assessment

* Latest critique dispositions: All five critique findings (`PC-001`..`PC-005`) in `kv-secret-lifecycle-142-plan-critique.md` were disposed and applied in `kv-secret-lifecycle-142-plan.md` (`## Critique Disposition`) and `kv-secret-lifecycle-142-phase-details.md` prior to implementation.
* Material revisions: None occurred during implementation.
* Dependent-work pause assessment: No material discovery required pausing dependent phases; phases executed in plan order `P01` -> `P02` -> `P03` -> `P04`.
* Justification assessment: Supported by repository and validation evidence; independent review identified tightness gaps in how several invariants (`auditDigest` recomputation, excess RBAC role matching, rotation receipt/URI/fresh-exchange binding, review timestamp bounds, and scalar/JSONL guards) are enforced against adversarial or malformed inputs (`RV-001`..`RV-005`).

## Plan Follow-Up Assessment

| Follow-up item | Why outside immediate scope | Owner or next action | Assessment and route |
|----------------|-----------------------------|----------------------|----------------------|
| Live operator-attended staged Entra client-secret rotation drill in `ama` test environment | Requires live Entra app registration + Key Vault mutation outside offline repository CI | `@jmservera` (post-merge live environment runbook execution) | Open distinct follow-up; preserved honestly in `infra/README.md` `### Open items` without fabricating cloud execution. |
| Inaugural live 90-day Log Analytics `AzureDiagnostics` + vault RBAC export and `review-sign` ledger entry | Requires live deployed Log Analytics workspace query and outside-repo operator signing key | `@jmservera` (quarterly operations schedule) | Open distinct follow-up; preserved honestly in `infra/README.md` `### Open items`. |

Unresolved plan follow-up items remain distinct follow-up work. Do not treat them as defects or add them to active `Pxx` or `Pxx-Txx` implementation, completion, or acceptance scope.

## Findings

<!-- rpi:review id=RV-001 -->
### RV-001 [High]: Recompute canonical `auditDigest` and reject duplicate audited IDs before signing review records

* Related scope: `P01-T01`
* Evidence: `src/core/src/zava_forward/core/secret_lifecycle.py` (`audit_keyvault_data_plane_access`, `create_signed_access_review_record`)
* Impact: `create_signed_access_review_record` currently validates that `audit["auditDigest"]` matches `_HEX64_RE` rather than recomputing the canonical digest from `audit`'s `vaultName`, `windowStart`, `windowEnd`, `rbacAssignments`, `callerSummaries`, `anomalies`, and `systemNotificationCount` (and checking uniqueness of `assignmentId` / `anomalyId`). A modified `audit` JSON with an anomaly removed while retaining the original `auditDigest` string would otherwise sign without error.
* Destination: `rpi-implement`
* Smallest useful next action: Recompute canonical `auditDigest` inside `create_signed_access_review_record`, fail closed on any mismatch or duplicate `assignmentId`/`anomalyId`, and add a negative tampering unit test.

<!-- rpi:review id=RV-002 -->
### RV-002 [High]: Enforce per-identity allowed RBAC roles and vault resource scope in `audit_keyvault_data_plane_access`

* Related scope: `P01-T01`
* Evidence: `src/core/src/zava_forward/core/secret_lifecycle.py` (`default_expected_caller_policy`, `audit_keyvault_data_plane_access`), `infra/role-assignments.json`
* Impact: `audit_keyvault_data_plane_access` flags unmapped OIDs, forbidden workloads, and unclassified roles, but does not verify that a mapped allowed identity holds only its permitted Key Vault RBAC role from `infra/role-assignments.json` (for example `api` or `resident-demo` holding `Key Vault Secrets Officer` instead of `Key Vault Secrets User`) or validate diagnostic row resource/URI vault host against `vault_name`.
* Destination: `rpi-implement`
* Smallest useful next action: Include `allowedRoles` per identity in `default_expected_caller_policy`, emit `excess_rbac_privilege` when a mapped principal holds a broader data-plane role than permitted, flag/reject diagnostic rows targeting a different vault (`wrong_vault_diagnostic`), and add unit tests.

<!-- rpi:review id=RV-003 -->
### RV-003 [High]: Tighten staged Entra rotation elapsed overlap, fresh post-switchover OAuth exchange proof, mandatory versioned URIs, and bound `post_retire` switchover receipts

* Related scope: `P01-T01`, `P04-T01`
* Evidence: `src/core/src/zava_forward/core/secret_lifecycle.py` (`verify_staged_entra_rotation`), `infra/README.md`
* Impact: Four rotation-verifier checks can be bypassed by incomplete or mismatched metadata: (1) `post_switchover` permits `safeToRetirePriorCredential=True` based solely on future credential `endDateTime` overlap even if insufficient soak/overlap has elapsed or `priorSwitchoverReceipt` in `post_retire` is unbound to the current `vaultName`, `appId`, `secretName`, `priorSecretName`, `priorKeyId`, `nextKeyId`, `priorVersionId`, and `nextVersionId`; (2) `authenticatedApiStatus == 200` alone could come from a pre-existing session cookie unless `freshTokenExchangeVerified` (post-switchover OIDC callback/token redemption after `nextVersionId` activation) is required when `browserMode=True`; and (3) `secretVersions.entries` allows entries missing a versioned `id` URI or lets `row["secretName"]` mask a conflicting secret segment in `id`.
* Destination: `rpi-implement`
* Smallest useful next action: Require versioned `id` URIs matching `vaultName`, expected secret name, and `version`; require `freshTokenExchangeVerified is True` alongside `authenticatedApiStatus == 200` on `post_switchover`/`post_retire` when `browserMode=True`; bind `rotation-verify` receipts to `{vaultName, appId, secretName, priorSecretName, priorKeyId, nextKeyId, priorVersionId, nextVersionId}` and verify exact field match on `post_retire`; document `freshTokenExchangeVerified` in `infra/README.md`; and add negative unit tests.

<!-- rpi:review id=RV-004 -->
### RV-004 [Medium]: Enforce non-future `reviewedAt`, exact `nextReviewDue` bounds, audit-window freshness, and scalar secret guards

* Related scope: `P01-T01`
* Evidence: `src/core/src/zava_forward/core/secret_lifecycle.py` (`access_review`, `rotation_plan`, `create_signed_access_review_record`, `verify_access_review_ledger`)
* Impact: `verify_access_review_ledger` does not reject future-dated `reviewedAt > now`, `windowEnd > reviewedAt`, stale audit windows (`reviewedAt - windowEnd > max_interval_days`), or `nextReviewDue` exceeding `(reviewedAt + reviewIntervalDays).date()`, and legacy helpers `access_review` / `rotation_plan` do not run `assert_no_secret_material` on scalar `reviewer`, `vault`, and `app_id` arguments.
* Destination: `rpi-implement`
* Smallest useful next action: Guard scalar string arguments in `access_review` and `rotation_plan`, enforce `windowEnd <= reviewedAt <= now` and exact `nextReviewDue <= (reviewedAt + reviewIntervalDays)` bounds in `create_signed_access_review_record` and `verify_access_review_ledger`, and add unit tests.

<!-- rpi:review id=RV-005 -->
### RV-005 [Medium]: Prevent JSONL append corruption when `--ledger` points to a JSON-array file

* Related scope: `P02-T01`
* Evidence: `infra/scripts/secret_lifecycle.py` (`_load_ledger_entries`, `_cmd_review_sign`)
* Impact: `_load_ledger_entries` accepts either JSONL or a JSON `[...]` array for read compatibility, whereas `_cmd_review_sign` appends a JSONL line directly to `--ledger`. Appending a JSONL line onto a `[...]` array file produces invalid hybrid syntax on subsequent reads.
* Destination: `rpi-implement`
* Smallest useful next action: Refuse `--ledger` files whose existing non-empty content starts with `[` in `_cmd_review_sign` (requiring JSONL `.jsonl` append format) with a clear `SecretLifecycleError` and CLI regression test.

## Defects

* `RV-001` (`High`) -> `rpi-implement`
* `RV-002` (`High`) -> `rpi-implement`
* `RV-003` (`High`) -> `rpi-implement`
* `RV-004` (`Medium`) -> `rpi-implement`
* `RV-005` (`Medium`) -> `rpi-implement`

## Routed Findings

| Finding | Destination | Owner or next action | Reason for route |
|---------|-------------|----------------------|------------------|
| `RV-001` | `rpi-implement` | Child hardening task (`kv-secret-lifecycle-142-hardening`) | Implementation defect within approved `FR-4` signed ledger design |
| `RV-002` | `rpi-implement` | Child hardening task (`kv-secret-lifecycle-142-hardening`) | Implementation defect within approved `FR-3` least-privilege caller/RBAC audit design |
| `RV-003` | `rpi-implement` | Child hardening task (`kv-secret-lifecycle-142-hardening`) | Implementation defect within approved `FR-2` staged rotation verification design |
| `RV-004` | `rpi-implement` | Child hardening task (`kv-secret-lifecycle-142-hardening`) | Implementation defect within approved `FR-1`/`FR-4` guard and cadence enforcement |
| `RV-005` | `rpi-implement` | Child hardening task (`kv-secret-lifecycle-142-hardening`) | Implementation defect within approved `P02-T01` JSONL ledger CLI handling |

Later implementation of a routed finding does not require another Review on `issue-142`.

## Residual Work

* Execute live operator-attended staged Entra client-secret rotation drill in `ama` test environment and archive sanitized `rotation-verify` receipt (`@jmservera`, post-merge cloud operations).
* Export first live 90-day Log Analytics `AzureDiagnostics` + vault RBAC snapshot from `ama` and record inaugural `review-sign` ledger entry (`@jmservera`, quarterly operations schedule).

## Blockers and Remaining Work

* Blockers: none
* Remaining active work: none in parent task `kv-secret-lifecycle-142`; routed defects `RV-001`..`RV-005` proceed via child automatic RPI task `kv-secret-lifecycle-142-hardening`.

## Validation Evidence

| Command | Scope | Status | Summary |
|---------|-------|--------|---------|
| `PYTHONPATH=... python3 -m unittest src/core/tests/test_secret_lifecycle.py src/core/tests/test_dependency_rule.py src/core/tests/test_diagnostic_logging.py infra/tests/test_secret_lifecycle.py infra/tests/test_bicep_architecture_inventory_136.py infra/tests/test_diagnostic_log_privacy.py infra/tests/test_identity_rbac.py -q` | `src/core/tests` + `infra/tests` (80 tests) | Passed | `Ran 80 tests in 2.802s - OK` |
| `PYTHONPATH=... python3 -m unittest discover -s infra/tests -q` | `infra/tests` (635 tests) | Passed | `Ran 635 tests in 529.215s - OK (skipped=4)` |
| `python3 infra/scripts/bicep_inventory.py --check` | `infra/README.md` + `infra/` | Passed | `29 architecture rows, 20 Bicep modules, 12 from-empty steps (17 rebuild stages)` (`exit 0`) |
| `(cd src/core && PYTHONPATH=src python3 -m mypy && python3 -m ruff check . && python3 -m ruff format --check .)` | `src/core` (363 mypy files, 310 ruff files) | Passed | `Success: no issues found in 363 source files`; `All checks passed! 310 files already formatted` |
| `ruff check` + `ruff check --isolated --select E,F,I,B,UP --target-version py312 --line-length 100` + `ruff format --isolated --line-length 100 --check` + `MYPYPATH=src/core/src python3 -m mypy --strict` | `infra/scripts/secret_lifecycle.py` & `infra/tests/test_secret_lifecycle.py` | Passed | `All checks passed!`; `2 files already formatted`; `Success: no issues found in 2 source files` |
| `python3 tools/rpi-checks.py --all` | Full local RPI gate | Skipped | Explicitly excluded by user prompt (`Validation tier: Focused`; `do not run tools/rpi-checks.py --all`) |

## Outcome

* Outcome: Defects found
* Outcome rationale: Planned implementation, unit/CLI suites, documentation, and Focused validation executed completely (`Execution status: Complete`), but independent review identified five concrete verification-tightness defects (`RV-001`..`RV-005`, three `High` and two `Medium`) that could allow forged `auditDigest` payloads, excess RBAC grants on mapped principals, unbound `post_retire` receipts or stale-cookie `200` probes, future-dated reviews, or JSON-array append corruption. Per `rpi-review` rules, these defects are recorded honestly and routed to a child hardening task rather than masked as conformant.

## Closeout Routing Record

<!-- Persist outcome and route facts only. The rpi-review reference owns rendered closeout prose. -->

| Finding class | Destination | Owner or next action |
|---------------|-------------|----------------------|
| Implementation defect | `rpi-implement` | Resolve `RV-001`..`RV-005` in child task `kv-secret-lifecycle-142-hardening` with regression tests |
| Decision gap or invalid assumption | none | none |
| Material evidence gap | none | none |
| Non-blocking residual work | distinct follow-up | Live Azure rotation drill and inaugural live 90-day `AzureDiagnostics` export (`@jmservera`) |

* Execution status: Complete
* Outcome: Defects found
* Validation coverage: Focused validation passed (`80` targeted tests, `635` `infra/tests`, `bicep_inventory.py --check`, `mypy`, `ruff check`, `ruff format --check`); `tools/rpi-checks.py --all` skipped per user prompt
* Blockers: none

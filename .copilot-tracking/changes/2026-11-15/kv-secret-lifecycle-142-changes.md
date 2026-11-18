<!-- markdownlint-disable-file -->
# RPI Changes: Key Vault Secret Lifecycle Rotation Verification and Scheduled Access Review (#142)

## Metadata

* Task ID: issue-142
* Related plan: .copilot-tracking/plans/2026-11-15/kv-secret-lifecycle-142-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/kv-secret-lifecycle-142-phase-details.md
* Implementation date: 2026-11-15

## Execution Status

* Status: Complete
* Declared invocation scope: full plan (`P01` through `P04`)
* Completed scope markers: `P01`, `P01-T01`, `P02`, `P02-T01`, `P03`, `P03-T01`, `P03-T02`, `P04`, `P04-T01`, `P04-T02`
* All remaining active-plan markers: none
* Status basis: All planned phases (`P01`..`P04`) and tasks (`P01-T01`..`P04-T02`) completed and verified under Focused validation (`unittest`, `ruff check`, `ruff format --check`, `mypy`, `bicep_inventory.py --check`).

## Execution Summary

Delivered zero-downtime dual-secret Entra client-secret rotation verification and scheduled 90-day Key Vault data-plane access review auditing + HMAC-SHA256 signed, SHA-256 hash-chained review ledgers across `src/core/src/zava_forward/core/secret_lifecycle.py` (`P01`) and `infra/scripts/secret_lifecycle.py` (`P02`), backed by 40 deterministic unit and CLI contract tests across `src/core/tests/test_secret_lifecycle.py` and `infra/tests/test_secret_lifecycle.py` (`P03`), updated operator procedures and contracts in `infra/README.md` (`P04-T01`), and passed the full `infra/tests` suite (635 tests) plus targeted `src/core` tests, `ruff`, and `mypy --strict` (`P04-T02`).

## Completed Work

### Pure Secret Lifecycle Verification and Signed Ledger Module (`P01` / `P01-T01`)

* Related phase or task: `P01`, `P01-T01`
* Files: `src/core/src/zava_forward/core/secret_lifecycle.py`
* What changed and why: Created zero-dependency, strictly typed domain module implementing fail-closed `assert_no_secret_material` + `unwrap_arm_list_envelope`, backward-compatible inventory/expiry/timeline helpers, `verify_staged_entra_rotation` (dual-secret overlap, in-place and two-name `priorSecretName` version switchover, mandatory post-switchover authenticated probe, rollback safety, strict `stage == "post_switchover"` retirement gating, and verifiable `post_retire` overlap proof), fail-closed `default_expected_caller_policy` + `audit_keyvault_data_plane_access` (separating OID-less Event Grid expiry notifications from `<anonymous>` secret operations and enforcing `403` / `>= 5` `401` thresholds), and `create_signed_access_review_record` + `verify_access_review_ledger` (1-to-1 RBAC/anomaly coverage, `vaultName` + `auditDigest` binding, SHA-256 hash chaining, HMAC-SHA256 verification, and 90-day schedule enforcement).
* Completion evidence: `src/core/src/zava_forward/core/secret_lifecycle.py` authored cleanly.
* Validation: Passed (`ruff check`, `ruff format --check`, `mypy`, and `test_dependency_rule.py` all exited `0`).

### CLI Wrapper and Backward-Compatible Orchestration (`P02` / `P02-T01`)

* Related phase or task: `P02`, `P02-T01`
* Files: `infra/scripts/secret_lifecycle.py`
* What changed and why: Extended `infra/scripts/secret_lifecycle.py` to delegate lifecycle helpers to `zava_forward.core.secret_lifecycle`, preserve all existing module symbols and subcommands, prepend this worktree's `src/core/src` (including `zava_forward.core.__path__` when preloaded), enforce outside-repository `0600` non-symlink checks on `--key-file` and `--keys-file`, and expose `rotation-verify`, `access-audit`, `review-sign`, and `ledger-verify`.
* Completion evidence: All 19 existing tests in `infra/tests/test_secret_lifecycle.py` pass immediately alongside `ruff` and `mypy --strict`.
* Validation: Passed (`ruff check`, `ruff check --isolated --select E,F,I,B,UP --target-version py312 --line-length 100`, `ruff format --isolated --line-length 100 --check`, `MYPYPATH=src/core/src python3 -m mypy --strict`, and `unittest infra/tests/test_secret_lifecycle.py` all exited `0`).

### Deterministic Core and CLI Lifecycle Tests (`P03` / `P03-T01`, `P03-T02`)

* Related phase or task: `P03`, `P03-T01`, `P03-T02`
* Files: `src/core/tests/test_secret_lifecycle.py`, `infra/tests/test_secret_lifecycle.py`
* What changed and why: Added 17 domain unit tests in `src/core/tests/test_secret_lifecycle.py` covering fail-closed canary secret refusal, ARM list-envelope unwrapping, dual-secret overlap/switchover/two-name handoff/authenticated probe/rollback/post-retire proof, data-plane `AzureDiagnostics` caller/operation/secret/status auditing, Event Grid notification separation, `401` threshold, human reviewer validation, and HMAC-SHA256 hash-chained ledger verification/key rotation/tampering/>90-day schedule gaps. Extended `infra/tests/test_secret_lifecycle.py` with strict type annotations on existing helpers (leaving all 19 pre-existing tests intact) plus 4 end-to-end CLI and `infra/role-assignments.json` alignment tests (23 tests total).
* Completion evidence: `40` lifecycle tests (`17` core + `23` infra) pass in `~0.05s` with `mypy --strict` and `ruff` clean.
* Validation: Passed (`unittest`, `ruff check`, `ruff format --check`, and `mypy --strict` all exited `0`).

### Operator Documentation and Focused Validation (`P04` / `P04-T01`, `P04-T02`)

* Related phase or task: `P04`, `P04-T01`, `P04-T02`
* Files: `infra/README.md`
* What changed and why: Updated `## Layout` and `## Key Vault secret lifecycle` (`### Rotate the Entra client secret`, `### Access review`, and `### Open items`) in `infra/README.md` to document the 4-step zero-downtime staged Entra rotation procedure (with `rotation-verify` and rollback hold), the 90-day `AzureDiagnostics` + RBAC `access-audit` / `review-sign` / `ledger-verify` contract, outside-repository `0600` key-file custody, and honest live-Azure operational boundaries without modifying `#136` Markdown tables or introducing `.copilot-tracking/` paths.
* Completion evidence: `python3 infra/scripts/bicep_inventory.py --check`, `infra/tests/test_bicep_architecture_inventory_136.py` (8 tests), full `infra/tests` suite (635 tests), targeted `src/core` tests, `mypy`, and `ruff` all passed (`exit 0`).
* Validation: Passed (all Focused validation commands exited `0`).

## Implementation-Time Plan and Detail Updates

* Local judgment (`P02-T01`): Prepending this worktree's `src/core/src/zava_forward/core` to `sys.modules["zava_forward.core"].__path__` when preloaded ensures `python3 -m unittest discover -s infra/tests` resolves this worktree's module even when an earlier test imported `zava_forward.core` from a sibling worktree install.

## Validation Record

| Check | Scope | Status | Evidence or reason |
|-------|-------|--------|--------------------|
| Core + Infra lifecycle, dependency, diagnostic, RBAC, and inventory tests | `src/core/tests` + `infra/tests` (80 tests) | Passed | `Ran 80 tests in 2.802s - OK` (`test_secret_lifecycle` core 17 + infra 23, `test_dependency_rule` 2, `test_diagnostic_logging` 11, `test_bicep_architecture_inventory_136` 8, `test_diagnostic_log_privacy` 7, `test_identity_rbac` 12) |
| Full `infra/tests` discovery suite | `infra/tests` (635 tests) | Passed | `Ran 635 tests in 529.215s - OK (skipped=4)` |
| Bicep architecture inventory check | `infra/README.md` + `infra/` | Passed | `python3 infra/scripts/bicep_inventory.py --check` (`exit 0`: 29 architecture rows, 20 Bicep modules, 12 from-empty steps) |
| `mypy` type checking (`src/core` + `infra` strict) | `src/core` (363 files) + `infra/scripts/secret_lifecycle.py` & `infra/tests/test_secret_lifecycle.py` | Passed | `Success: no issues found in 363 source files` and `MYPYPATH=src/core/src python3 -m mypy --strict` (`Success: no issues found in 2 source files`) |
| `ruff check` and `ruff format --check` (`src/core` + `infra` isolated) | `src/core` (310 files) + modified `infra/` files | Passed | `All checks passed! 310 files already formatted` and `ruff check --isolated --select E,F,I,B,UP --target-version py312 --line-length 100` + `ruff format --isolated --line-length 100 --check` (`exit 0`) |
| `tools/rpi-checks.py --all` | Full local gate | Skipped | Explicitly excluded by user prompt (`Validation tier: Focused`; `do not run tools/rpi-checks.py --all`) |

## Pre-Review Reconciliation

* Plan markers and phase details: current (`P01`, `P02`, `P03`, `P04` and all `P01-T01`..`P04-T02` checked `[x]`)
* Completed-work evidence and handoff prose: current and reconciled against repository diff
* Validation, blockers, remaining work, and follow-up items: current
* Review readiness: ready

## Blockers

* None

## Remaining Work

* None in active implementation scope (`rpi-review` and local git commit follow next in the parent automatic RPI loop).

## Follow-Up Items

* Canonical plan list: .copilot-tracking/plans/2026-11-15/kv-secret-lifecycle-142-plan.md, `## Follow-Up Items`
* Execute a live operator-attended staged Entra client-secret rotation drill in the `ama` test environment and archive the sanitized `rotation-verify` receipt (outside offline repository CI scope; owner: `@jmservera`).
* Export the first live 90-day Log Analytics `AzureDiagnostics` + vault RBAC snapshot from `ama` and record the inaugural live `review-sign` entry in operations evidence (outside offline repository CI scope; owner: `@jmservera`).

## Return-to-Caller State

* Implementation execution status: Complete
* Declared scope and markers: full plan; completed: `P01`, `P01-T01`, `P02`, `P02-T01`, `P03`, `P03-T01`, `P03-T02`, `P04`, `P04-T01`, `P04-T02`; remaining: none
* Validation coverage: Focused validation passed (`80` targeted tests, `635` `infra/tests`, `bicep_inventory.py --check`, `mypy` on `363` core files + strict on `2` infra files, `ruff check` and `ruff format --check`)
* Blockers: none
* Current plan and detail updates: local judgment noted for preloaded `zava_forward.core.__path__` resolution in multi-worktree test discovery
* Planning and critique state: Ready (`PC-001`..`PC-005` resolved)
* Follow-up items: live Azure rotation drill and inaugural live quarterly access review export (`@jmservera`)
* Review readiness or no-handoff reason: ready
* Continuation owner: parent (confirmed automatic RPI Agent -> `rpi-review`)

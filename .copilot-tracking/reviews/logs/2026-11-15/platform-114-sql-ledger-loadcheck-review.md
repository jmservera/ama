<!-- markdownlint-disable-file -->
# Review: Issue #114 Per-Year Ledger Pre-Reliance Verification and Load-Check Cost Contract

## Scope and Evidence

* Task ID: issue-114-platform-sql-ledger-loadcheck
* Review date: 2026-11-15
* Review scope: Full task (`P01`, `P02`, `P03`)
* Assessed boundary: FR-1 (`LedgerRelianceError`, `verify_ledger_before_reliance`, `require_verified_ledger_for_reliance` across `Store`, `SqlStore`, and `MssqlStore`), FR-2 (`loadcheck.evaluate_cost`, `run`, and `main` `--vcore-seconds` / `--meter-rate` / `--cost-target`), FR-3 (`src/core/README.md`), secret-free/deterministic year-boundary/typing NFRs, critique dispositions `PC-001`–`PC-006`, multi-year (`2024`, `2025`, `2026`) unit proofs, and focused-tier validation.
* Plan: .copilot-tracking/plans/2026-11-15/platform-114-sql-ledger-loadcheck-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/platform-114-sql-ledger-loadcheck-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-11-15/platform-114-sql-ledger-loadcheck-plan-critique.md
* Changes: .copilot-tracking/changes/2026-11-15/platform-114-sql-ledger-loadcheck-changes.md
* Other evidence considered: .copilot-tracking/research/2026-11-15/platform-114-sql-ledger-loadcheck-research.md, `git diff` across `src/core/`, focused validation outputs, and independent read-only review lens.

## Opening Review State

* Interpreted review goal: Verify whether the completed `P01`–`P03` implementation and focused validation satisfy all offline-testable Issue #114 requirements, acceptance criteria, and `PC-001`–`PC-006` critique dispositions without secret leakage, behavioral regressions, or scope drift.
* Review scope: Full task (`P01`, `P02`, `P03`)
* Evidence readiness: Ready; plan markers (`P01`–`P03`), phase details (`Complete`), critique (`PC-001`–`PC-006` resolved), changes record (`Complete`), and validation outputs are reconciled.
* Acceptance basis: Plan Functional Requirements (`FR-1`–`FR-3`), Non-Functional Requirements, Acceptance Criteria, Test Ownership and Validation Lock, and `PC-001`–`PC-006` critique dispositions.
* First comparison boundary: Reconcile `P01`, `P02`, `P03`, and `## Follow-Up Items` between plan, phase details, changes record, and `src/core/` diff before assessing defects or residual items.
* Active read-only boundaries: Review writes only `.copilot-tracking/reviews/logs/2026-11-15/platform-114-sql-ledger-loadcheck-review.md` (and parent RPI state pointer); source code, plan, details, critique, research, and changes record are read-only.
* Initial blockers: None

## Execution Status

* Execution status: Complete
* Review execution evidence: Completed single-pass full-boundary comparison on 2026-11-15 across plan, phase details, single-pass critique (`PC-001`–`PC-006`), changes record, `git diff` over all 8 modified `src/core` files, focused validation outputs (60 targeted unit tests, 11 doc-link/cutover tests, `ruff check`, `ruff format --check`, `mypy`), and an independent read-only review lens.

## Plan-to-Change Reconciliation

| Current plan scope | Descriptive changes-record summary | Current-state reconciliation | Gap or rationale |
|--------------------|------------------------------------|------------------------------|------------------|
| `P01` (`P01-T01`, `P01-T02`) | `### P01 (P01-T01, P01-T02): Pre-Reliance Per-Year Ledger Verification Contract` | Reconciled | Plan markers `[x]`, phase-details status `Complete`, and changes record match implemented `ledger.py`, `store.py`, and `sqlstore.py` symbols. |
| `P02` (`P02-T01`) | `### P02 (P02-T01): Load-Check Latency and Structured PRD Cost Contract` | Reconciled | Plan markers `[x]`, phase-details status `Complete`, and changes record match `loadcheck.py` (`evaluate_cost`, `run`, `main`). |
| `P03` (`P03-T01`, `P03-T02`) | `### P03 (P03-T01, P03-T02): Multi-Year Unit Proofs, Documentation, and Focused Validation` | Reconciled | Plan markers `[x]`, phase-details status `Complete`, and changes record match 11 added unit tests across `test_recovery.py`, `test_sqlstore.py`, `test_loadcheck.py` (within `<= 14` lock) and `src/core/README.md`. |
| `## Follow-Up Items` | `## Follow-Up Items` (live Azure SQL `loadcheck` and witnessed `DH-005` restore drill) | Reconciled | Preserved outside active `P01`–`P03` completion claims under `Refs #114`. |

## Completed Work Assessment

| Related marker | Files | What changed and why | Completion evidence | Validation | Assessment |
|----------------|-------|----------------------|---------------------|------------|------------|
| `P01-T01` | `src/core/src/zava_forward/core/ledger.py`, `src/core/src/zava_forward/core/store.py` | Added atomic `_write_json_once`, `inspect_digest_directory`, `LedgerRelianceError`, `write_year_digests(*, before=None)`, `verify_ledger_before_reliance`, and `require_verified_ledger_for_reliance` so completed past years seal only when pre-checks pass and any tamper, missing year, unsealed past year, or corrupt digest blocks reliance secret-free. | `YearLedgerTests` multi-year (`2024`, `2025`, `2026`) cases in `src/core/tests/test_recovery.py`. | Passed (`test_recovery.py`, `ruff check`, `mypy`) | Reconciled |
| `P01-T02` | `src/core/src/zava_forward/core/sqlstore.py` | Re-exported `LedgerRelianceError`, overrode `_reliance_lock` and `write_year_digests` under `self.dblock` (`PC-001`), and implemented `_reliance_audit_snapshot` checking `audit_head WHERE id=1` and unfiltered `audit` rows (`PC-003`), inherited by `MssqlStore`. | `SqlStoreTests` multi-year (`2024`, `2025`, `2026`), `audit_head`, `MssqlStore` inheritance, and secret-scrubbing tests in `src/core/tests/test_sqlstore.py`. | Passed (`test_sqlstore.py`, `ruff check`, `mypy`) | Reconciled |
| `P02-T01` | `src/core/src/zava_forward/core/synthetic/loadcheck.py` | Added `evaluate_cost` (`Decimal` `prec=60`, float-range guard, `-0.0` normalization, strict `meter_rate > 0`, honest `"Unknown"` missing-input reporting with `azure_live_run_human_gated: True`), extended `run` with `load` and `cost` without extra clock reads (`PC-002`), and added `--vcore-seconds`, `--meter-rate`, `--cost-target` in `main`. | `LoadcheckEvidenceTests` in `src/core/tests/test_loadcheck.py`. | Passed (`test_loadcheck.py`, `ruff check`, `ruff format --check`, `mypy`) | Reconciled |
| `P03-T01` | `src/core/tests/test_recovery.py`, `src/core/tests/test_sqlstore.py` | Added 7 focused multi-year (`2024`, `2025`, `2026`) unit test methods covering intact sealing, rollover, pre-seal tamper refusal, corrupt/swapped digests, dropped sealed years, unsealed past years, `audit_head` mismatch/deletion, `MssqlStore` inheritance, and driver secret scrubbing. | Direct test execution under `TMPDIR=/dev/shm`. | Passed (`40` tests in `test_recovery.py` + `test_sqlstore.py`) | Reconciled |
| `P03-T02` | `src/core/tests/test_loadcheck.py`, `src/core/README.md` | Added 4 strict-`mypy`-typed `loadcheck` unit test methods (preserving all existing assertions and exit codes `0`/`1`/`2`) and updated `src/core/README.md` Issue #114 documentation with explicit live-Azure honesty boundaries. | Direct test execution, lint, format, type check, and live doc-link check. | Passed (`60` focused tests, `11` doc-link/cutover tests, `ruff`, `mypy`) | Reconciled |

## Implementation-Time Plan and Detail Update Assessment

| Affected area or marker | What changed and why | Triggering evidence and user decision | Reconciliation performed | Planning and critique state | Assessment |
|-------------------------|----------------------|---------------------------------------|--------------------------|-----------------------------|------------|
| None | No implementation-time scope, architecture, or task-boundary revisions were needed; implementation followed the post-critique `Ready` plan directly. | None | Verified `## Implementation-Time Plan and Detail Updates` in changes record matches unchanged plan requirements. | Not needed (`PC-001`–`PC-006` remained current) | Reconciled |

## Critique and Material Revision Assessment

* Latest critique dispositions: All six critique findings (`PC-001` lock ordering & atomic write-once digests, `PC-002` zero extra clock calls in `loadcheck.run`, `PC-003` direct `audit_head` + unfiltered `audit` SQL snapshot, `PC-004` `Decimal` `prec=60` non-truncating float-range-guarded `evaluate_cost`, `PC-005` `Store` `last_hash` test seeding + 4-digit year cutoffs + problem mapping + no unused `# type: ignore`, `PC-006` `loadcheck.run` signature & `F401`-clean re-export) were applied in planning and verified in implementation.
* Material revisions: None occurred during implementation.
* Dependent-work pause assessment: No dependent work bypassed plan order; `P03` executed after `P01` and `P02` passed smoke checks.
* Justification assessment: Supported by passing focused tests and static checks.

## Plan Follow-Up Assessment

| Follow-up item | Why outside immediate scope | Owner or next action | Assessment and route |
|----------------|-----------------------------|----------------------|----------------------|
| Live Azure SQL serverless (`GP_S_Gen5`) `loadcheck` run with billed `vcore_seconds` and subscription meter rate (`Refs #114`) | Requires provisioned Azure SQL environment, live billing telemetry, and human cloud gate approval (`BRD OD-51`). | Platform operator / coordinator once live Azure SQL environment is approved. | Open outside-scope operational item; routed as distinct follow-up (`Refs #114`). |
| Witnessed Azure SQL point-in-time restore drill (`DH-005`) with `recovery.reapply_deletions` and `verify_ledger_before_reliance` (`Refs #114`) | Requires live Azure SQL point-in-time restore and immutable WORM Blob storage container (`ADR-0002`). | Platform operator / human compliance witness during pilot-readiness drill. | Open outside-scope operational item; routed as distinct follow-up (`Refs #114`). |

Unresolved plan follow-up items remain distinct follow-up work. Do not treat them as defects or add them to active `Pxx` or `Pxx-Txx` implementation, completion, or acceptance scope.

## Findings

<!-- rpi:review id=RV-001 -->
### RV-001 [Low]: Suppress caller-side implicit `__context__` on `raise LedgerRelianceError(...) from None` and avoid non-hardlink fallback partial writes

* Related scope: `P01-T01`
* Evidence: `src/core/src/zava_forward/core/store.py` (`Store.require_verified_ledger_for_reliance`) and `src/core/src/zava_forward/core/ledger.py` (`_write_json_once`)
* Impact: All internal store, JSON, and SQL driver exceptions are caught inside `verify_ledger_before_reliance()` before returning a plain `dict`, so `LedgerRelianceError.__cause__` and internal `__context__` are already `None` and secret-free (verified by `test_pre_reliance_scrubs_driver_secrets_and_is_inherited_by_mssqlstore`). However, if an external caller invokes `require_verified_ledger_for_reliance()` directly inside an external `except` block holding a credential-bearing exception, Python's implicit `__context__` remains attached unless `raise LedgerRelianceError(...) from None` is used. Additionally, `_write_json_once` uses atomic `mkstemp` + `os.link` on POSIX filesystems (`ext4`/`tmpfs`), with an `open(path, "x")` fallback on filesystems lacking hardlinks (`EXDEV`/`ENOTSUP`) that could use `os.replace` only when `not os.path.exists` or fail closed if interrupted mid-write. Neither affects any Issue #114 acceptance criterion on supported Linux/container filesystems.
* Destination: follow-up
* Smallest useful next action: Optional defense-in-depth hardening pass appending `from None` to `raise LedgerRelianceError(...)` in `store.py` and tightening the non-hardlink fallback in `ledger._write_json_once`.

<!-- rpi:review id=RV-002 -->
### RV-002 [Low]: Pass verified audit snapshot directly when sealing past-year digests across multi-process SQL writers

* Related scope: `P01-T01`, `P01-T02`
* Evidence: `src/core/src/zava_forward/core/store.py` (`Store.verify_ledger_before_reliance`, `Store._invoke_write_year_digests`) and `src/core/src/zava_forward/core/sqlstore.py` (`SqlStore.write_year_digests`)
* Impact: `verify_ledger_before_reliance` honors the prompt contract by calling `write_year_digests()` after pre-checks pass and then re-verifying `ledger.verify_years(entries, post_year_digests)` against the pre-seal `entries` snapshot, so `reliance_allowed` fails closed (`False`) even if another OS process tampered with past-year rows in between. Passing the verified `entries` snapshot directly to `year_digests(...)` during sealing would prevent a concurrent rogue cross-process trigger-bypass race from writing an unverified `year-YYYY.json` file that subsequently fails verification.
* Destination: follow-up
* Smallest useful next action: Optional defense-in-depth hardening pass adding an optional internal `_entries` parameter to `write_year_digests` so pre-reliance sealing computes `year_digests` directly from the verified snapshot.

## Defects

* None blocking active acceptance criteria (`RV-001` and `RV-002` are non-blocking `Low` defense-in-depth hardening items routed to follow-up).

## Routed Findings

| Finding | Destination | Owner or next action | Reason for route |
|---------|-------------|----------------------|------------------|
| `RV-001` | `follow-up` | Optional `src/core` hardening follow-up (`store.py`, `ledger.py`) | Non-blocking `Low` defense-in-depth improvement for caller-side outer `except` chaining (`from None`) and non-hardlink filesystems |
| `RV-002` | `follow-up` | Optional `src/core` hardening follow-up (`store.py`, `sqlstore.py`) | Non-blocking `Low` defense-in-depth improvement to seal `year-YYYY.json` directly from the already-verified `entries` snapshot |

Later implementation of a routed finding does not require another Review.

## Residual Work

* `RV-001` [Low]: Append `from None` on `raise LedgerRelianceError(...)` in `store.py` for caller-side outer `except` blocks and harden non-hardlink fallback in `ledger._write_json_once`.
* `RV-002` [Low]: Seal completed past-year digests directly from the verified `entries` snapshot inside `verify_ledger_before_reliance` while preserving `write_year_digests()` compatibility.
* Issue #114 live Azure SQL serverless (`GP_S_Gen5`) `loadcheck` run with billed `vcore_seconds` and subscription meter rate (`Refs #114`, human/Azure-gated).
* Issue #114 witnessed Azure SQL point-in-time restore drill (`DH-005`) with `recovery.reapply_deletions` and `verify_ledger_before_reliance` (`Refs #114`, human/Azure-gated).

## Blockers and Remaining Work

* Blockers: None for the offline-testable `src/core` Issue #114 slice (live Azure SQL / DH-005 criteria on Issue #114 remain human- and cloud-gated under `Refs #114`).
* Remaining active work: None in declared `P01`–`P03` scope.

## Validation Evidence

| Command | Scope | Status | Summary |
|---------|-------|--------|---------|
| `TMPDIR=/dev/shm PYTHONPATH=src/core/src:src/core/tests python3 -m unittest src/core/tests/test_loadcheck.py src/core/tests/test_recovery.py src/core/tests/test_sqlstore.py -q` | `src/core` ledger reliance, SQL store, and loadcheck suites | Passed | `Ran 60 tests in 1.527s — OK` |
| `TMPDIR=/dev/shm PYTHONPATH=src/core/src:src/core/tests python3 -m unittest src/core/tests/test_live_doc_links.py src/core/tests/test_cutover_audit.py -q` | `src/core` documentation link and cutover hygiene checks | Passed | `Ran 11 tests in 4.359s — OK` |
| `python3 -m ruff check` | `src/core` | Passed | `All checks passed!` |
| `python3 -m ruff format --check` | `src/core` | Passed | `314 files already formatted` |
| `python3 -m mypy` | `src/core` | Passed | `Success: no issues found in 367 source files` |
| `python3 tools/rpi-checks.py --all` | Full repository gate | Skipped | Explicitly excluded by caller focused-tier instructions (`Do NOT run python3 tools/rpi-checks.py --all`). |

## Outcome

* Outcome: Conformant
* Outcome rationale: Every in-scope requirement (`FR-1`–`FR-3`), NFR threshold (secret-free error/report surface with `__cause__ is None`, deterministic `2024`/`2025`/`2026` year cutoffs, zero `ruff`/`mypy` issues), `PC-001`–`PC-006` critique disposition, and prompt acceptance criterion is implemented and proven by 60 passing focused unit tests and 11 doc-link/cutover tests. Two `Low` non-blocking defense-in-depth hardening opportunities (`RV-001`, `RV-002`) and the two human-gated live Azure SQL operational items (`Refs #114`) are recorded cleanly as distinct follow-up work.

## Closeout Routing Record

<!-- Persist outcome and route facts only. The rpi-review reference owns rendered closeout prose. -->

| Finding class | Destination | Owner or next action |
|---------------|-------------|----------------------|
| Implementation defect | none | None blocking active acceptance criteria |
| Decision gap or invalid assumption | none | None |
| Material evidence gap | none | None |
| Non-blocking residual work | distinct follow-up | Optional `src/core` defense-in-depth hardening (`RV-001`, `RV-002`) and human-gated live Azure SQL `loadcheck` + `DH-005` restore drill (`Refs #114`) |

* Execution status: Complete
* Outcome: Conformant
* Validation coverage: Passed focused `unittest` (`60` tests + `11` doc-link/cutover tests), `ruff check`, `ruff format --check`, and `mypy` (`367` files); full `rpi-checks.py --all` intentionally skipped per caller instruction.
* Blockers: None for the offline `src/core` slice; live Azure SQL criteria on `#114` remain human-gated (`Refs #114`).


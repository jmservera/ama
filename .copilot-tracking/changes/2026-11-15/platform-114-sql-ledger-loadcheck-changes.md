<!-- markdownlint-disable-file -->
# RPI Changes: Issue #114 Per-Year Ledger Pre-Reliance Verification and Load-Check Cost Contract

## Metadata

* Task ID: issue-114-platform-sql-ledger-loadcheck
* Related plan: .copilot-tracking/plans/2026-11-15/platform-114-sql-ledger-loadcheck-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/platform-114-sql-ledger-loadcheck-phase-details.md
* Implementation date: 2026-11-15

## Execution Status

* Status: Complete
* Declared invocation scope: full plan (`P01`, `P02`, `P03`)
* Completed scope markers: `P01` (`P01-T01`, `P01-T02`), `P02` (`P02-T01`), `P03` (`P03-T01`, `P03-T02`)
* All remaining active-plan markers: none
* Status basis: All planned tasks (`P01-T01`, `P01-T02`, `P02-T01`, `P03-T01`, `P03-T02`) implemented and verified against focused unit tests, `ruff check`, `ruff format --check`, and `mypy`.

## Execution Summary

Implemented the deterministic pre-reliance per-year ledger verification contract (`LedgerRelianceError`, `verify_ledger_before_reliance`, `require_verified_ledger_for_reliance`) across `Store`, `SqlStore`, and `MssqlStore` (via `SqlStore` inheritance), extended `loadcheck.py` with `evaluate_cost`, measured `load` and `cost` report sections, and optional `--vcore-seconds`, `--meter-rate`, and `--cost-target` CLI flags, added 11 focused unit tests across `test_recovery.py`, `test_sqlstore.py`, and `test_loadcheck.py`, updated `src/core/README.md`, and verified all focused checks exit `0`.

## Completed Work

### P01 (`P01-T01`, `P01-T02`): Pre-Reliance Per-Year Ledger Verification Contract

* `src/core/src/zava_forward/core/ledger.py`: Added 4-digit ASCII year formatting in `year_digests`, atomic write-once `_write_json_once` (sibling temp file + `os.link` tolerating `FileExistsError`) in `write_digest` and `write_year_digest`, and `inspect_digest_directory` validating root `digest-{count:010d}.json` (including `count == 0` `GENESIS`) and `year-{YYYY}.json` filename-to-payload `year` and schema invariants without leaking filesystem paths.
* `src/core/src/zava_forward/core/store.py`: Added `LedgerRelianceError` carrying `.report` and `.problems` with `from None` cause suppression, optional `before` parameter on `write_year_digests`, `_reliance_lock`, `ImportError`-safe `_reliance_db_errors`, `_reliance_audit_snapshot`, `verify_ledger_before_reliance`, and `require_verified_ledger_for_reliance`. Seals completed past years (`< f"{effective_year:04d}"`) only when pre-seal chain, `audit_head`, root-digest, and existing year-digest checks pass.
* `src/core/src/zava_forward/core/sqlstore.py` (inherited by `MssqlStore`): Re-exported `LedgerRelianceError`, overrode `_reliance_lock` (`self.dblock`) and `write_year_digests` under `self.dblock` (avoiding `_SyncLock` lock inversion), and implemented `_reliance_audit_snapshot` checking `audit_head WHERE id=1` directly and unfiltered `SELECT seq, ... FROM audit ORDER BY seq`.

### P02 (`P02-T01`): Load-Check Latency and Structured PRD Cost Contract

* `src/core/src/zava_forward/core/synthetic/loadcheck.py`: Added `_validate_cost_number` and `evaluate_cost` using `decimal.localcontext(Context(prec=60))` with float-range bounds checking (`[-sys.float_info.max, sys.float_info.max]`), `-0.0` normalization, strict positive `meter_rate_per_vcore_second > 0`, full finite IEEE-754 product precision (`0.0 if raw == 0 else float(raw)`), and honest `"Unknown"` missing-input reporting (`azure_live_run_human_gated: True`). Extended `run` with `load` (`sessions`, `writers`, `seconds`, `total_requests`, `achieved_rps` with zero extra clock reads) and `cost`, and extended `main` with `--vcore-seconds`, `--meter-rate`, and `--cost-target` validated before `open_store(env)` while preserving CLI exit codes (`0`, `1`, `2`).

### P03 (`P03-T01`, `P03-T02`): Multi-Year Unit Proofs, Documentation, and Focused Validation

* `src/core/tests/test_recovery.py`: Added 4 focused multi-year (`2024`, `2025`, `2026`) pre-reliance tests covering intact sealing, rollover (`current_year=2027`), refusal to seal tampered chains, unsealed past years (`seal_past_years=False`), corrupt/swapped `year-*.json`, tampered `digest-*.json`, dropped sealed years, non-directory `digest_dir`, malformed entry years, and corrupt `audit.jsonl`.
* `src/core/tests/test_sqlstore.py`: Added 3 focused multi-year (`2024`, `2025`, `2026`) SQL tests covering intact `SqlStore` verification, trigger-bypassed row tampering, dropped `2024` rows against sealed `year-2024.json`, unsealed `2026` tail deletion caught by `audit_head`, missing `audit_head`, `MssqlStore` subclass inheritance, and connection-string secret scrubbing (`__cause__ is None`).
* `src/core/tests/test_loadcheck.py`: Added 4 strict-`mypy`-typed tests covering `evaluate_cost` measured within/exceeding/without target (preserving 8-decimal vCore-second rate precision), `"Unknown"` missing-input posture, invalid numeric/bool/overflow rejection before `store.cases` or `open_store`, `run` `load`/`cost`/`LIMITS` sections, and CLI exit codes `0`/`1`/`2`.
* `src/core/README.md`: Updated `### Per-year ledger digests, load check and recovery drill (issue #114)` to document `verify_ledger_before_reliance` / `require_verified_ledger_for_reliance` and `loadcheck` `--vcore-seconds` / `--meter-rate` / `--cost-target` while preserving the explicit live Azure SQL and DH-005 honesty boundary.

## Implementation-Time Plan and Detail Updates

* None.

## Validation Record

| Check | Scope | Status | Evidence or reason |
|-------|-------|--------|--------------------|
| Focused `unittest` (`test_loadcheck`, `test_recovery`, `test_sqlstore`) | `src/core/tests` | Passed | `Ran 60 tests in 1.527s — OK` (`TMPDIR=/dev/shm`) |
| `python3 -m ruff check` | `src/core` | Passed | `All checks passed!` |
| `python3 -m ruff format --check` | `src/core` | Passed | `314 files already formatted` |
| `python3 -m mypy` | `src/core` | Passed | `Success: no issues found in 367 source files` |

## Pre-Review Reconciliation

* Plan markers and phase details: Reconciled (`P01`, `P01-T01`, `P01-T02`, `P02`, `P02-T01`, `P03`, `P03-T01`, `P03-T02` all checked; phase index statuses `Complete`).
* Completed-work evidence and handoff prose: Reconciled across `ledger.py`, `store.py`, `sqlstore.py`, `loadcheck.py`, `test_recovery.py`, `test_sqlstore.py`, `test_loadcheck.py`, and `src/core/README.md`.
* Validation, blockers, remaining work, and follow-up items: Reconciled; zero blockers, zero remaining active-plan items, two human/Azure-gated follow-ups preserved.
* Review readiness: Ready for `rpi-review`.

## Blockers

* None

## Remaining Work

* None in declared full-plan scope.

## Follow-Up Items

* Canonical plan list: .copilot-tracking/plans/2026-11-15/platform-114-sql-ledger-loadcheck-plan.md, `## Follow-Up Items`
* Live Azure SQL serverless (`GP_S_Gen5`) `loadcheck` execution with billed `vcore_seconds` and subscription meter rate (`Refs #114`, human/Azure-gated).
* Witnessed Azure SQL point-in-time restore drill (`DH-005`) with `recovery.reapply_deletions` re-redaction verification (`Refs #114`, human/Azure-gated).

## Return-to-Caller State

* Implementation execution status: Complete
* Declared scope and markers: full plan (`P01`–`P03`); completed: `P01` (`P01-T01`, `P01-T02`), `P02` (`P02-T01`), `P03` (`P03-T01`, `P03-T02`); remaining: none
* Validation coverage: Focused `unittest` (60 tests), `ruff check`, `ruff format --check`, and `mypy` in `src/core` all passed (`0` exit)
* Blockers: None
* Current plan and detail updates: None
* Planning and critique state: Ready (`PC-001`–`PC-006` resolved)
* Follow-up items: Two human/Azure-gated Issue #114 items preserved from plan
* Review readiness or no-handoff reason: Ready for `rpi-review`
* Continuation owner: Confirmed automatic RPI Agent parent

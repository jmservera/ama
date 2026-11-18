<!-- markdownlint-disable-file -->
# RPI Plan: Issue #114 Per-Year Ledger Pre-Reliance Verification and Load-Check Cost Contract

## Task Metadata

* Task ID: issue-114-platform-sql-ledger-loadcheck
* Task slug: platform-114-sql-ledger-loadcheck
* Planning status: Ready
* Plan date: 2026-11-15
* Phase details: .copilot-tracking/details/2026-11-15/platform-114-sql-ledger-loadcheck-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-11-15/platform-114-sql-ledger-loadcheck-plan-critique.md

## Executive Summary

This plan delivers the remaining offline-testable engineering and contract slice for Issue #114 (**Durable Azure SQL store with ledger audit**) across `src/core`:

1. **Deterministic pre-reliance per-year audit chain and sealed ledger digest verification (`P01`)**: Adds `LedgerRelianceError`, `verify_ledger_before_reliance(self, *, require_sealed_past_years: bool = True, current_year: int | None = None, seal_past_years: bool = True) -> dict[str, Any]`, and `require_verified_ledger_for_reliance(self, *, require_sealed_past_years: bool = True, current_year: int | None = None, seal_past_years: bool = True) -> dict[str, Any]` across `Store` (`store.py`), `SqlStore` (`sqlstore.py`), and inherited `MssqlStore` (`mssqlstore.py`). Before sealing completed past years via `write_year_digests()`, the verifier checks audit readability, full chain continuity, root digests (`digest-*.json`), `year-*.json` filename-to-payload binding and schema invariants, and SQL `audit_head` parity (`SqlStore`/`MssqlStore`) so tampered history is never sealed into write-once digest files. It then seals completed past years, runs `verify_ledger_by_year()`, verifies that every past year with audit entries has a matching intact sealed digest when `require_sealed_past_years=True`, and returns `reliance_allowed=False` with secret-free machine-readable `problems` (or raises secret-free `LedgerRelianceError` in `require_verified_ledger_for_reliance`) on any tampering, dropped year, unsealed past year, head mismatch, or corrupt/unreadable digest.
2. **Structured load, latency, and cost evaluation against PRD targets (`P02`)**: Extends `src/core/src/zava_forward/core/synthetic/loadcheck.py` with `evaluate_cost`, updated `run`, and updated `main` (`--vcore-seconds`, `--meter-rate`, `--cost-target`) so every load-check report records measured load (`sessions`, `writers`, `seconds`, `total_requests`, `achieved_rps`) and per-class latency (`n`, `p50`, `p95`, `max`, `limit`, `within` against PRD `NFR-002` `LIMITS`) alongside a structured `cost` section (`status: "measured" | "Unknown"`, `vcore_seconds`, `meter_rate_per_vcore_second`, `measured_cost`, `target_cost`, `within_target`, `missing_inputs`, and `azure_live_run_human_gated: True`), preserving all existing `test_loadcheck.py` assertions and CLI exit-code semantics.
3. **Multi-year unit proofs, documentation alignment, and focused validation (`P03`)**: Proves multi-year (`2024`, `2025`, `2026`) pre-reliance verification across `Store`, `SqlStore`, and `MssqlStore` inheritance in `test_recovery.py` and `test_sqlstore.py`, proves measured vs `Unknown` cost reporting and CLI exit codes in `test_loadcheck.py`, updates `src/core/README.md`, and passes focused `TMPDIR=/dev/shm` unit tests, `ruff check`, `ruff format --check`, and `mypy`.

### User Decisions and Requirements Highlights

* **Full RPI loop with dated `2026-11-15` artifacts**: Run `rpi-research`, `rpi-plan` (with one-pass `rpi-plan-critique`), `rpi-implement`, and `rpi-review` on branch `feat/platform-114-sql-ledger-loadcheck` (stacked on `feat/demo-164-chat-grounding-provenance-0900`, PR #1641), leaving a clean frozen local commit (`Refs #114`) without pushing or opening a PR.
* **Pre-reliance per-year ledger verification before operational reliance**: `verify_ledger_before_reliance` and `require_verified_ledger_for_reliance` must work across `Store`, `SqlStore`, and `MssqlStore`, sealing completed past years, verifying per-year chains and sealed digests, enforcing sealed past-year digests, and emitting secret-free errors/problems, proven across `2024`, `2025`, and `2026` audit entries.
* **Honest load-check latency and cost contract**: `loadcheck.py` must compute `measured_cost` and `within_target` when meter inputs are provided and report `status: "Unknown"` with `missing_inputs` and `azure_live_run_human_gated: True` when omitted, without breaking existing CLI exit codes.
* **Focused validation tier**: Execute `TMPDIR=/dev/shm` targeted unit tests plus `ruff check`, `ruff format --check`, and `mypy` inside `src/core`; do not run `python3 tools/rpi-checks.py --all`.

### What You May Not Know

* **Unconditional `write_year_digests()` before verification would seal tampered past years**: Because `ledger.write_year_digest` writes `year-YYYY.json` once (`open(..., "x")`) and never overwrites, calling `write_year_digests()` before checking chain integrity would permanently seal tampered unsealed past-year entries. **P01** verifies chain continuity, `audit_head`, and existing digests *before* sealing completed past years, then seals and re-verifies `verify_ledger_by_year()`.
* **`SqlStore` unsealed tail deletion and lock-hierarchy safety (`PC-001`, `PC-003`)**: Deleting all rows of the current unsealed year (`2026`) directly in SQL without updating `audit_head` would leave `verify_ledger_by_year()` reporting `intact=True` if `audit_head` (`count`, `hash`) were ignored. **P01** holds one backend-appropriate reliance lock (`self.lock` on `Store`; re-entrant `self.dblock` on `SqlStore`/`MssqlStore`, overriding `SqlStore.write_year_digests` under `self.dblock` to prevent `dblock -> _SyncLock` lock-order inversion), queries `audit_head` and unfiltered `ORDER BY seq` directly (`PC-003`), writes `year-YYYY.json` atomically via sibling temp-file + `os.link` (`PC-001`), and wraps the entire snapshot/pre-check/seal/post-check flow in one `ImportError`-safe DB/OS/JSON error handler.
* **`test_loadcheck.py` is strictly checked by `mypy` and `ruff format`**: In `src/core/pyproject.toml`, `test_loadcheck.py` runs under strict `mypy` (`disallow_untyped_defs = true`) and `ruff format --check`, whereas `store.py`, `sqlstore.py`, `loadcheck.py`, `test_recovery.py`, and `test_sqlstore.py` are in `[tool.ruff.format].exclude` and `mypy` `ignore_errors`. Every new helper and test in `test_loadcheck.py` must be fully typed and formatted.

### Unresolved Decisions or Blockers

* None for offline `src/core` implementation and verification. Live Azure SQL `GP_S_Gen5` load/cost execution and witnessed DH-005 point-in-time restore drills remain external human/cloud gates (`Refs #114`, `azure_live_run_human_gated: True`).

For current user input, see [User Decisions and Requirements](#user-decisions-and-requirements). The planner keeps the synthesized sections below current as evidence and user direction evolve.

## User Decisions and Requirements

* Run the full RPI loop in order (`rpi-research`, `rpi-plan` including one-pass `rpi-plan-critique`, `rpi-implement`, and `rpi-review`) writing dated `2026-11-15` artifacts under `.copilot-tracking/` (`research/`, `plans/`, `details/`, `reviews/plans/`, `changes/`, `reviews/logs/`) for Issue #114 (`Refs #114`) on branch `feat/platform-114-sql-ledger-loadcheck` in `/home/azureuser/source/ama-demo-wt/feat-114-sql-ledger-loadcheck` (caller prompt).
* Add deterministic pre-reliance verification `verify_ledger_before_reliance(self, *, require_sealed_past_years: bool = True) -> dict[str, Any]` and helper `require_verified_ledger_for_reliance(self)` (plus secret-free `LedgerRelianceError`) in `src/core/src/zava_forward/core/store.py` / `sqlstore.py` (inherited by `mssqlstore.py`), sealing completed past years (`write_year_digests()`), running per-year chain and sealed-digest verification (`verify_ledger_by_year()`), verifying every past year with audit entries has a matching intact sealed digest, and raising `LedgerRelianceError` (or returning `reliance_allowed=False` with machine-readable `problems`) when any year's audit chain or sealed digest is tampered with, missing, or unreadable before reliance (caller Objective 1; ADR-0001; ADR-0002).
* Prove pre-reliance verification with focused multi-year (`2024`, `2025`, `2026`) unit tests in `src/core/tests/test_recovery.py` and `src/core/tests/test_sqlstore.py` covering intact sealed years and tampered, dropped-year, unsealed, and corrupt-digest failures (caller Objective 1).
* Extend `src/core/src/zava_forward/core/synthetic/loadcheck.py` (`evaluate_cost`, `run`, `main` with optional `--vcore-seconds`, `--meter-rate`, `--cost-target`) so every report records measured load and per-class latency (`p50`, `p95`, `max`, `limit`, `within` against `LIMITS`) alongside a structured `cost` section (`status: "measured" | "Unknown"`, `vcore_seconds`, `meter_rate_per_vcore_second`, `measured_cost`, `target_cost`, `within_target`, `missing_inputs`, `azure_live_run_human_gated: True`), computing measured cost against PRD targets when meter inputs are supplied and reporting `status: "Unknown"` with `missing_inputs` when absent, proven in `src/core/tests/test_loadcheck.py` while preserving all existing assertions and CLI exit-code semantics (caller Objective 2; PRD `NFR-002`; `BRD OD-51`).
* Run focused validation (`TMPDIR=/dev/shm` targeted unit tests, `ruff check`, `ruff format --check`, `mypy` inside `src/core`; do not run `python3 tools/rpi-checks.py --all`) and commit all changes plus `.copilot-tracking/` artifacts locally with `Refs #114` and the Copilot `Co-authored-by` trailer without pushing or opening a PR (caller Validation Tier).

## Goals

* Establish one deterministic, secret-free pre-reliance ledger verification contract across `Store`, `SqlStore`, and `MssqlStore` that seals completed past years only when history is intact and blocks reliance on any chain, `audit_head`, root-digest, or year-digest anomaly.
* Record structured workload, latency (`LIMITS`), and `Decimal`-accurate Azure SQL cost evaluation (or honest `"Unknown"` missing-input posture) in `loadcheck.py` without breaking existing programmatic or CLI callers.
* Prove all multi-year (`2024`, `2025`, `2026`) ledger reliance invariants and `loadcheck` cost/latency invariants under `src/core` unit tests, `ruff`, and `mypy`.

## Scope and Non-Goals

### In Scope

* `src/core/src/zava_forward/core/store.py`, `src/core/src/zava_forward/core/sqlstore.py`, and `src/core/src/zava_forward/core/ledger.py` (only if non-breaking year-digest filename/schema validation helper is shared; `MssqlStore` inherits via `SqlStore`).
* `src/core/src/zava_forward/core/synthetic/loadcheck.py`.
* `src/core/tests/test_recovery.py`, `src/core/tests/test_sqlstore.py`, and `src/core/tests/test_loadcheck.py`.
* `src/core/README.md` (`### Per-year ledger digests, load check and recovery drill (issue #114)` section).

### Non-Goals

* Running live Azure SQL serverless workloads, live Azure CLI commands, or witnessed DH-005 point-in-time restore drills.
* Claiming `Closes #114` (live Azure criteria on Issue #114 remain open; commit uses `Refs #114`).
* Running `python3 tools/rpi-checks.py --all`, pushing to remote, or creating a pull request.
* Modifying web UI, API routes, Bicep templates, or unrelated packages.

## Functional Requirements

* **FR-1 (`LedgerRelianceError` and `Store` / `SqlStore` / `MssqlStore` pre-reliance verification contract)**:
  * `store.py` defines `LedgerRelianceError(RuntimeError)` carrying `.report: dict[str, Any]` and `.problems: list[dict[str, Any]]` with a secret-free message and `from None` suppression, re-exported in `sqlstore.py`.
  * `Store.write_year_digests(self, *, before: int | str | None = None)` preserves zero-argument behavior (`before=f"{datetime.now().year:04d}"` when `before is None`, formatting integer `before` as 4-digit ASCII `f"{before:04d}"`, `PC-005`), writes `year-YYYY.json` atomically via sibling temporary file + `os.link` (`PC-001`), and is overridden on `SqlStore` under `self.dblock` (`PC-001`).
  * `Store.verify_ledger_before_reliance(self, *, require_sealed_past_years: bool = True, current_year: int | None = None, seal_past_years: bool = True) -> dict[str, Any]` validates keyword arguments, acquires `_reliance_lock()` (`self.lock` on `Store`; `self.dblock` on `SqlStore`/`MssqlStore`) across the entire snapshot + pre-check + seal + post-check flow wrapped in one `(_reliance_db_errors(), OSError, ValueError, TypeError, KeyError, RuntimeError)` secret-free handler (`PC-001`), snapshots audit entries and backend head state via `_reliance_audit_snapshot()` (overridden on `SqlStore` to query `audit_head` directly first and unfiltered `SELECT ... FROM audit ORDER BY seq` with `seq >= 1` validation, `PC-003`), validates ASCII 4-digit entry years (`^[0-9]{4}$` in `0001..9999`), `not os.path.lexists` vs readable directory `digest_dir`, root `digest-{count:010d}.json` files (including `count == 0` with `head == GENESIS`), and `year-{YYYY}.json` filename-to-payload `year` and schema invariants (`algorithm == "sha256"`, `chain == "main"`, positive `int` `count`, lowercase 64-hex `first_prev` and `head`, `PC-005`), seals completed past years (`< f"{effective_year:04d}"`) from the verified snapshot via `write_year_digests` only when pre-seal checks pass and `seal_past_years=True`, runs `verify_ledger_by_year()`, maps `missing_years`, `bad_digests`, and `digest_mismatches` into `problems` (`PC-005`), verifies every past year (`< f"{effective_year:04d}"`) with audit entries has an intact matching sealed digest when `require_sealed_past_years=True`, and returns a deterministic dict with `reliance_allowed: bool`, `intact: bool`, `current_year: str`, `require_sealed_past_years: bool`, `entries: int`, `head: str`, `audit_head_matches: bool`, `digests_checked: int`, `digest_mismatches: list[dict[str, Any]]`, `years: dict[str, Any]`, `sealed_years: list[str]`, `missing_years: list[str]`, `bad_digests: list[Any]`, `sealed_digest_files: list[str]`, and `problems: list[dict[str, Any]]`.
  * `Store.require_verified_ledger_for_reliance(self, *, require_sealed_past_years: bool = True, current_year: int | None = None, seal_past_years: bool = True) -> dict[str, Any]` delegates to `verify_ledger_before_reliance(...)`, returning the report when `reliance_allowed` is `True` and raising `LedgerRelianceError` when `False`.
  * Observable acceptance criteria: Intact multi-year (`2024`, `2025`, `2026`) `Store`, `SqlStore`, and `MssqlStore`-inherited stores seal `2024` and `2025` (`2026` remains active current year) and return `reliance_allowed=True` with `problems=[]`; tampering any entry, mutating `audit_head`, dropping a sealed year's rows, omitting a past-year digest when `seal_past_years=False` and `require_sealed_past_years=True`, corrupting/swapping `year-*.json` or `digest-*.json`, or corrupting `audit.jsonl` / raising a DB error returns `reliance_allowed=False` with machine-readable `problems` and causes `require_verified_ledger_for_reliance()` to raise secret-free `LedgerRelianceError`.
* **FR-2 (`loadcheck.evaluate_cost`, `run`, and `main` measured load, latency, and cost contract)**:
  * `evaluate_cost(vcore_seconds: float | None = None, meter_rate_per_vcore_second: float | None = None, target_cost: float | None = None) -> dict[str, Any]` validates finite numeric inputs within `[-sys.float_info.max, sys.float_info.max]` before `float(...)` conversion (`vcore_seconds >= 0`, `meter_rate_per_vcore_second > 0` rejecting zero/negative/`bool`/`NaN`/`Inf`/large-`int` overflow, `target_cost >= 0`, normalizing `-0.0` to `0.0`, `PC-004`), computes `raw` inside `decimal.localcontext(prec=60)` with traps cleared and sets non-truncating finite `measured_cost = 0.0 if raw == 0 else float(raw)` (raising `ValueError` on product overflow/underflow, `PC-004`) when both `vcore_seconds` and `meter_rate_per_vcore_second` are supplied (`status: "measured"`), evaluates `within_target: bool` when `target_cost` is also supplied (`None` when `target_cost is None`), and returns `status: "Unknown"`, `measured_cost: None`, `within_target: None`, ordered `missing_inputs` (`["vcore_seconds", "meter_rate_per_vcore_second", "target_cost"]` subset), and `azure_live_run_human_gated: True` whenever `vcore_seconds` or `meter_rate_per_vcore_second` is omitted.
  * `loadcheck.run(store: Any, user: dict[str, Any], seconds: float, sessions: int = 5, writers: int = 2, *, vcore_seconds: float | None = None, meter_rate_per_vcore_second: float | None = None, target_cost: float | None = None) -> dict[str, Any]` (`PC-006`) validates cost inputs before reading `store.cases` and returns `classes` (`n`, `p50`, `p95`, `max`, `limit`, `within` against `LIMITS`), `load` (`sessions`, `writers`, `seconds`, `total_requests`, `achieved_rps = round(total_requests / float(seconds), 4)` with zero extra clock reads, `PC-002`), `cost`, `errors`, and `error_kinds`.
  * `loadcheck.main(argv=None)` adds optional `--vcore-seconds`, `--meter-rate`, and `--cost-target`, validates them via `ap.error(...)` (exit `2`) before `open_store(env)` without changing `env` keys (`{"ZF_DATA", "ZF_STATE", "ZF_STORE"}`), embeds `load` and `cost` in stdout JSON, and exits `0` iff `errors == 0`, all `classes[*]["within"]` are `True`, and `cost["within_target"] is not False` (`1` otherwise).
  * Observable acceptance criteria: Unit tests in `test_loadcheck.py` verify measured cost within target (exit `0`), measured cost exceeding target (`within_target=False`, exit `1`), measured cost without target (`status="measured"`, `within_target=None`, `missing_inputs=["target_cost"]`, exit `0`), omitted meter inputs (`status="Unknown"`, `missing_inputs`, `azure_live_run_human_gated=True`, exit `0` when latency passes), invalid CLI/API cost inputs rejected before store access, and 100% pass of all pre-existing `test_loadcheck.py` cases.
* **FR-3 (Documentation synchronization)**:
  * `src/core/README.md` (`### Per-year ledger digests, load check and recovery drill (issue #114)`) documents `verify_ledger_before_reliance` / `require_verified_ledger_for_reliance` and the optional `--vcore-seconds` / `--meter-rate` / `--cost-target` `loadcheck` flags while keeping the unverified live Azure SQL / DH-005 honesty boundary explicit.
  * Observable acceptance criteria: `git diff -- src/core/README.md` accurately matches implemented names, flags, and honesty boundaries.

## Non-Functional Requirements

* **Secret-free, path-free error and problem reporting**
  * Objective threshold or evaluation condition: Zero raw connection strings, credentials, tokens, SQL driver exception messages, or full filesystem paths in `verify_ledger_before_reliance()["problems"]`, `sealed_digest_files` (basenames only), `LedgerRelianceError` string/cause (`__cause__ is None`), or `loadcheck` JSON output.
  * Operating condition or verification approach: Simulated DB/OS errors containing sentinel secrets (e.g., `Server=tcp:secret.database.windows.net;Password=TOPSECRET`) verified absent from returned reports and raised `LedgerRelianceError` exceptions.
  * Observable acceptance criteria: Unit tests assert sentinel strings do not appear in `json.dumps(report)` or `str(cm.exception)` and `cm.exception.__cause__ is None`.
* **Deterministic calendar-year boundary handling**
  * Objective threshold or evaluation condition: Multi-year (`2024`, `2025`, `2026`) tests produce identical sealed/active year results regardless of wall-clock execution year when `current_year=2026` (and under default `current_year=None` in 2026).
  * Operating condition or verification approach: Default `datetime.now().year` at runtime with optional keyword `current_year: int | None = None`.
  * Observable acceptance criteria: Multi-year unit tests pass deterministically for both default and explicit `current_year=2026` / `current_year=2027` cutoffs.
* **Lint, format, and static typing compliance**
  * Objective threshold or evaluation condition: Zero errors from `python3 -m ruff check`, `python3 -m ruff format --check`, and `python3 -m mypy` inside `src/core`.
  * Operating condition or verification approach: Run exact `src-ci.yml` commands in `src/core` plus `TMPDIR=/dev/shm` targeted unittest run.
  * Observable acceptance criteria: All validation commands exit `0`.

## Acceptance Criteria

* `Store`, `SqlStore`, and `MssqlStore` expose `verify_ledger_before_reliance` and `require_verified_ledger_for_reliance` (with `LedgerRelianceError`), sealing completed past years only when pre-checks pass, verifying per-year chains, sealed digests, and `audit_head`, and blocking reliance with secret-free machine-readable `problems` when any year chain, `audit_head`, root digest, or sealed year digest is tampered, missing, dropped, unsealed, or unreadable.
* Focused multi-year (`2024`, `2025`, `2026`) unit tests pass in `src/core/tests/test_recovery.py` and `src/core/tests/test_sqlstore.py` (including `MssqlStore` inheritance coverage and sentinel secret-scrubbing checks).
* `src/core/src/zava_forward/core/synthetic/loadcheck.py` implements `evaluate_cost` and extends `run` and `main` (`--vcore-seconds`, `--meter-rate`, `--cost-target`) with measured `load`, per-class `LIMITS` latency, and structured `cost` (`status: "measured" | "Unknown"`, `vcore_seconds`, `meter_rate_per_vcore_second`, `measured_cost`, `target_cost`, `within_target`, `missing_inputs`, `azure_live_run_human_gated: True`), preserving existing `test_loadcheck.py` assertions and CLI exit codes.
* Focused unit tests in `src/core/tests/test_loadcheck.py` pass alongside `ruff check`, `ruff format --check`, and `mypy` inside `src/core`.
* Changes and dated `.copilot-tracking/` RPI artifacts are committed cleanly on `feat/platform-114-sql-ledger-loadcheck` with `Refs #114` and `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>`, without pushing or opening a PR.

## Test Ownership and Validation Lock

* **Canonical test targets**:
  * `src/core/tests/test_recovery.py` (`Store` and `SqlStore` multi-year `2024`/`2025`/`2026` pre-reliance verification: intact pass + sealing idempotence, tampered past/current entry, corrupt/swapped/duplicate `year-*.json`, corrupt `digest-*.json`, dropped sealed year, unsealed past year when `seal_past_years=False`, corrupt `audit.jsonl`, and sentinel secret scrubbing).
  * `src/core/tests/test_sqlstore.py` (`SqlStore` and `MssqlStore`-inherited multi-year `2024`/`2025`/`2026` pre-reliance verification: intact pass, SQL trigger-bypassed entry tampering, SQL `audit_head` mismatch / unsealed `2026` tail deletion, dropped `2024` rows against sealed `year-2024.json`, corrupt digest, simulated DB driver fault with connection-string secret scrubbing).
  * `src/core/tests/test_loadcheck.py` (strict-`mypy` typed tests for `evaluate_cost`, `run`, and `main`: measured cost within/over PRD target, measured cost without target, omitted/partial meter inputs yielding `status="Unknown"` + `missing_inputs` + `azure_live_run_human_gated=True`, invalid numeric/zero-rate CLI and `run` inputs rejected before store access, and preserved CLI exit codes `0`/`1`/`2`).
* **Exact removals**: `none` (all existing test methods and assertions are preserved).
* **Maximum test additions**: Up to 14 focused test methods across `test_recovery.py`, `test_sqlstore.py`, and `test_loadcheck.py`.
* **Generated targets**: `none`.
* **Validation commands**:
  * `TMPDIR=/dev/shm PYTHONPATH=src/core/src:src/core/tests python3 -m unittest src/core/tests/test_loadcheck.py src/core/tests/test_recovery.py src/core/tests/test_sqlstore.py -q`
  * `(cd src/core && python3 -m ruff check && python3 -m ruff format --check && python3 -m mypy)`

## Implementation Context Record

| Context item                     | Current artifact or record                                                                                                               |
|----------------------------------|------------------------------------------------------------------------------------------------------------------------------------------|
| Plan                             | .copilot-tracking/plans/2026-11-15/platform-114-sql-ledger-loadcheck-plan.md                                                             |
| Phase details                    | .copilot-tracking/details/2026-11-15/platform-114-sql-ledger-loadcheck-phase-details.md                                                  |
| Latest critique                  | .copilot-tracking/reviews/plans/2026-11-15/platform-114-sql-ledger-loadcheck-plan-critique.md with Revise disposition resolved (`PC-001`–`PC-006`) |
| Relevant research                | .copilot-tracking/research/2026-11-15/platform-114-sql-ledger-loadcheck-research.md                                                      |
| Changes-record role              | .copilot-tracking/changes/2026-11-15/platform-114-sql-ledger-loadcheck-changes.md is created by implementation as its evidence record    |
| Planning execution and readiness | Complete and Ready for `rpi-implement`                                                                                                   |
| Continuation context             | Automatic RPI Agent parent advances directly to `rpi-implement` (`P01-T01`)                                                              |

## Sources

* `.copilot-tracking/research/2026-11-15/platform-114-sql-ledger-loadcheck-research.md`: Primary research findings (`C1`–`C12`), contrarian failure hypotheses, and selected Option A architecture.
* `docs/adrs/0001-azure-architecture.md` and `docs/adrs/0002-pilot-readiness-architecture.md`: Azure SQL serverless (`GP_S_Gen5`) ledger audit, immutable Blob digest anchoring, and pre-reliance verification rules.
* `docs/prds/zava-forward-retrofit-programme-demonstrator.md`: `NFR-002` core workload latency limits (`1.0s` / `1.0s` / `2.0s` at 5 sessions, 2 writers) and `BRD OD-51` cost honesty boundary.
* `src/core/src/zava_forward/core/{store,sqlstore,mssqlstore,ledger}.py` and `src/core/src/zava_forward/core/synthetic/loadcheck.py`: Existing store hierarchy, ledger digest primitives, and synthetic load-check runner.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Pre-Reliance Per-Year Ledger Verification Contract

* Intent: Implement `LedgerRelianceError`, `verify_ledger_before_reliance`, and `require_verified_ledger_for_reliance` across `Store`, `SqlStore`, and `MssqlStore` with pre-seal chain/anchor verification, `audit_head` validation, filename/schema year-digest checks, and secret-free `problems`.
* Dependencies: None

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Implement `LedgerRelianceError` and pre-reliance verification on `Store` and `ledger.py`

* Requirement and evidence: FR-1, NFR secret-free/deterministic year boundary (`C6`, `C7`, `C8`)
* Expected result: `store.py` exports `LedgerRelianceError`, supports optional `before` in `write_year_digests`, and implements `verify_ledger_before_reliance` and `require_verified_ledger_for_reliance` with pre-seal integrity checks, filename-bound year-digest validation, past-year seal enforcement, and basename/code-only secret-free `problems`.
* Detail section: P01-T01 in .copilot-tracking/details/2026-11-15/platform-114-sql-ledger-loadcheck-phase-details.md

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Wire atomic `audit_head` snapshot and `dberror`-safe reliance hook in `SqlStore` (inherited by `MssqlStore`)

* Requirement and evidence: FR-1, NFR secret-free DB fault handling (`C9`, `C10`)
* Expected result: `sqlstore.py` re-exports `LedgerRelianceError` and overrides `_reliance_audit_snapshot()` using `self.dblock` and `_audit_rows(0)` to detect missing or mismatched `audit_head` rows and scrub SQL/driver exceptions (guarding `MssqlStore.dberror` against `ImportError`).
* Detail section: P01-T02 in .copilot-tracking/details/2026-11-15/platform-114-sql-ledger-loadcheck-phase-details.md

<!-- rpi:phase id=P02 -->
### [x] P02: Load-Check Latency and Structured PRD Cost Contract

* Intent: Extend `loadcheck.py` with `evaluate_cost`, measured `load` and `cost` report sections in `run`, and `--vcore-seconds` / `--meter-rate` / `--cost-target` CLI flags in `main` while preserving existing behavior and CLI exit-code semantics.
* Dependencies: None

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Implement `evaluate_cost`, extend `run`, and add cost CLI flags to `main` in `loadcheck.py`

* Requirement and evidence: FR-2 (`C3`, `C4`, `C11`, `C12`)
* Expected result: `loadcheck.py` exports `evaluate_cost`, records `load` and structured `cost` (`status: "measured" | "Unknown"`, `vcore_seconds`, `meter_rate_per_vcore_second`, `measured_cost`, `target_cost`, `within_target`, `missing_inputs`, `azure_live_run_human_gated: True`) in `run` and `main`, rejects invalid inputs before touching the store, and exits `1` on explicit cost-target breach while keeping exit `0` for passing un-metered (`Unknown`) runs.
* Detail section: P02-T01 in .copilot-tracking/details/2026-11-15/platform-114-sql-ledger-loadcheck-phase-details.md

<!-- rpi:phase id=P03 -->
### [x] P03: Multi-Year Unit Proofs, Documentation, and Focused Validation

* Intent: Add focused multi-year (`2024`, `2025`, `2026`) ledger reliance tests and `loadcheck` cost/latency tests, update `src/core/README.md`, and run all focused validation checks cleanly.
* Dependencies: P01, P02

<!-- rpi:task id=P03-T01 -->
#### [x] P03-T01: Add multi-year (`2024`, `2025`, `2026`) pre-reliance unit tests in `test_recovery.py` and `test_sqlstore.py`

* Requirement and evidence: FR-1, NFR secret-free & deterministic year boundary (`C7`–`C10`)
* Expected result: Focused tests cover intact multi-year pass and fail-closed rejection on entry tampering, dropped sealed years, corrupt/swapped digests, unsealed past years, `audit_head` mismatch, unreadable audit/DB faults, secret scrubbing, and `MssqlStore` inheritance parity.
* Detail section: P03-T01 in .copilot-tracking/details/2026-11-15/platform-114-sql-ledger-loadcheck-phase-details.md

<!-- rpi:task id=P03-T02 -->
#### [x] P03-T02: Add typed `loadcheck` cost/latency unit tests in `test_loadcheck.py`, update `src/core/README.md`, and run focused validation

* Requirement and evidence: FR-2, FR-3, NFR lint/format/typing (`C5`, `C11`, `C12`)
* Expected result: `test_loadcheck.py` covers measured within/exceeding/target-omitted cost, `Unknown` missing-input reporting, invalid input rejection, and CLI exit codes with strict `mypy` annotations; `src/core/README.md` documents the new contracts; unittest, `ruff check`, `ruff format --check`, and `mypy` all exit `0`.
* Detail section: P03-T02 in .copilot-tracking/details/2026-11-15/platform-114-sql-ledger-loadcheck-phase-details.md

## Dependencies

* Active Python 3.12 toolchain with `zava_forward.core`, `ruff`, and `mypy` installed (verified present in workspace environment).
* Writable `/dev/shm` tmpfs (`TMPDIR=/dev/shm`) for deterministic SQLite temporary test stores.

## Critique Disposition

Record the latest critique findings, their disposition, and any explicitly accepted residual risk. Keep this section outside user decisions and current planning synthesis.

| Critique run and finding | Disposition | Plan response or residual risk |
|--------------------------|-------------|--------------------------------|
| `PC-001` [High]: Unlocked multi-snapshot sealing, uncaught SQL faults, and non-atomic `write_year_digest` | Resolved | Updated `FR-1`, `P01-T01`, and `P01-T02` to hold one backend-appropriate reliance lock (`self.lock` on `Store`; `self.dblock` on `SqlStore`/`MssqlStore` with `SqlStore.write_year_digests` under `self.dblock`), wrap the entire snapshot/pre-check/seal/post-check flow in one secret-free DB/OS/JSON handler, and write `year-YYYY.json` atomically via sibling temp-file + `os.link`. |
| `PC-002` [High]: Clock-mocked `test_loadcheck.py` compatibility for `achieved_rps` | Resolved | Updated `FR-2` and `P02-T01` to compute `achieved_rps = round(total_requests / float(seconds), 4)` directly from `seconds` with zero extra calls to `time.monotonic`, `time.perf_counter`, or `time.time`. |
| `PC-003` [High]: `SqlStore._audit_rows(0)` missing-head `RuntimeError` and `seq <= 0` filter | Resolved | Updated `FR-1` and `P01-T02` so `SqlStore._reliance_audit_snapshot` directly queries `audit_head WHERE id=1` first (`audit_head_missing` / schema validation) and fetches unfiltered `SELECT ... FROM audit ORDER BY seq` with `seq >= 1` validation and `audit_head` recheck. |
| `PC-004` [Medium]: `evaluate_cost` large-`int` `OverflowError`, `Decimal` overflow/`-0.0`, and 6-decimal truncation | Resolved | Updated `FR-2` and `P02-T01` to check `[-sys.float_info.max, sys.float_info.max]` before `float(val)`, normalize `-0.0` to `0.0`, evaluate `raw` in `decimal.localcontext(prec=60)` with traps cleared, and emit non-truncating finite `float(raw)` with overflow/underflow `ValueError` guards. |
| `PC-005` [Medium]: `< 1000` year cutoff, ASCII year/hex regexes, `count=0` `GENESIS` root digest, and `problems` mapping | Resolved | Updated `FR-1` and `P01-T01` to format `before` as `f"{effective_year:04d}"`, enforce ASCII regexes, validate `count == 0` root digests (`head == GENESIS`), check `not os.path.lexists(digest_dir)`, and map `missing_years`, `bad_digests`, and `digest_mismatches` into `problems`. |
| `PC-006` [Medium]: `ruff` `F401` re-export, `mypy --strict` kwargs/bool typing, and `Store` multi-year test seeding | Resolved | Updated `P01-T02`, `P02-T01`, `P03-T01`, and `P03-T02` to use `LedgerRelianceError as LedgerRelianceError`, full `float | None = None` annotations without `[unused-ignore]` on `bool`, pre-init `audit.jsonl` seeding in `test_recovery.py`, and explicit `current_year=2026` rollover-safe assertions. |
| Residual risk: Live Azure SQL serverless load/cost and `DH-005` restore drill | Accepted with risk | Preserved explicitly via `azure_live_run_human_gated: True`, `src/core/README.md` honesty boundary, and `Refs #114` non-closing attribution. |

## Follow-Up Items

* Live Azure SQL serverless (`GP_S_Gen5`) `loadcheck` execution with billed `vcore_seconds` and subscription meter rate against a target Azure SQL database (`Refs #114`, human/Azure-gated).
* Witnessed Azure SQL point-in-time restore drill (`DH-005`) with `recovery.reapply_deletions` re-redaction verification on a live Azure SQL backup (`Refs #114`, human/Azure-gated).

## Handoff

* Implementation artifact: .copilot-tracking/changes/2026-11-15/platform-114-sql-ledger-loadcheck-changes.md
* Ready phase or task: P01-T01
* Remaining provisional question or blocker: None

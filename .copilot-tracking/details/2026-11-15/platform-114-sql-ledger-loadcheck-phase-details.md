<!-- markdownlint-disable-file -->
# RPI Phase Details: Issue #114 Per-Year Ledger Pre-Reliance Verification and Load-Check Cost Contract

## Metadata

* Task ID: issue-114-platform-sql-ledger-loadcheck
* Task slug: platform-114-sql-ledger-loadcheck
* Related plan: .copilot-tracking/plans/2026-11-15/platform-114-sql-ledger-loadcheck-plan.md
* Evidence sources: .copilot-tracking/research/2026-11-15/platform-114-sql-ledger-loadcheck-research.md, docs/adrs/0001-azure-architecture.md, docs/adrs/0002-pilot-readiness-architecture.md, docs/prds/zava-forward-retrofit-programme-demonstrator.md

## Phase Index

| Phase ID | Name                                                  | Status   | Detail sections          |
|----------|-------------------------------------------------------|----------|--------------------------|
| P01      | Pre-Reliance Per-Year Ledger Verification Contract    | Complete | P01, P01-T01, P01-T02    |
| P02      | Load-Check Latency and Structured PRD Cost Contract   | Complete | P02, P02-T01             |
| P03      | Multi-Year Unit Proofs, Documentation, and Validation | Complete | P03, P03-T01, P03-T02    |

<!-- rpi:phase id=P01 -->
## P01: Pre-Reliance Per-Year Ledger Verification Contract

### Context

`Store` (`src/core/src/zava_forward/core/store.py`) already implements `write_year_digests()` and `verify_ledger_by_year()`, inherited by `SqlStore` (`sqlstore.py`) and `MssqlStore` (`mssqlstore.py`). Research (`C7`–`C10`) identified four nuances that a production-grade pre-reliance gate must handle:
1. `write_year_digests()` creates `year-YYYY.json` once and never overwrites; calling it before checking chain integrity would seal tampered unsealed past-year entries.
2. `Store.audit_entries()` and `ledger.read_digests()` raise raw `ValueError`/`OSError` on corrupt JSON, and `SqlStore`/`MssqlStore` may raise DB driver exceptions containing server or credential strings.
3. `SqlStore` and `MssqlStore` maintain `audit_head (id=1, count, hash)`; deleting all rows of an unsealed tail year (`2026`) without updating `audit_head` is only caught when `audit_head` is checked alongside `verify_years`.
4. `ledger.read_year_digests()` drops the `year-YYYY.json` filename once parsed, so a swapped file (`year-2024.json` containing `"year": "2025"`) or wrong `algorithm` / non-64-hex hash must be checked explicitly.

### Intent

Provide `LedgerRelianceError`, `verify_ledger_before_reliance`, and `require_verified_ledger_for_reliance` on `Store` and `SqlStore` (inherited by `MssqlStore`) with fail-closed, secret-free machine-readable `problems`.

### Boundaries

* Included: `src/core/src/zava_forward/core/store.py`, `src/core/src/zava_forward/core/sqlstore.py`, and non-breaking digest-validation helpers in `src/core/src/zava_forward/core/ledger.py`.
* Excluded: Live Azure SQL DDL changes, Blob network transport (`ledger_digest_blob.py` is owned by #115), or web/API endpoints.

### Likely Targets

* `src/core/src/zava_forward/core/ledger.py`: Add helper(s) to inspect `digest_dir` year and root digest files with filename-to-year agreement and strict field-type/hex64 validation without breaking existing `read_year_digests` / `verify_years` callers.
* `src/core/src/zava_forward/core/store.py`: Add `LedgerRelianceError`, optional `before` parameter on `write_year_digests`, `_reliance_audit_snapshot()`, `verify_ledger_before_reliance(...)`, and `require_verified_ledger_for_reliance(...)`.
* `src/core/src/zava_forward/core/sqlstore.py`: Re-export `LedgerRelianceError` and override `_reliance_audit_snapshot()` using `self.dblock` and `_audit_rows(0)` to include `audit_head` verification and `ImportError`-safe `dberror` exception catching.

### Dependencies

* None.

### Validation Expectations

* Multi-year (`2024`, `2025`, `2026`) unit tests on `Store`, `SqlStore`, and `MssqlStore` subclass harness plus `ruff check`.

### Completion Evidence

* `verify_ledger_before_reliance` returns `reliance_allowed=True` for intact sealed multi-year chains and `reliance_allowed=False` with structured secret-free `problems` on every tampered, dropped, unsealed, head-mismatched, or unreadable condition; `require_verified_ledger_for_reliance` returns the report or raises `LedgerRelianceError`.

### Unresolved Items

* None.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Implement `LedgerRelianceError` and pre-reliance verification on `Store` and `ledger.py`

#### Context

`Store` (`store.py:190-226`) provides the base ledger interface inherited by `SqlStore` and `MssqlStore`. Downstream callers (`ledger_digest_blob.py`, `orchestrator/digest_blob.py`) call `write_year_digests()` with zero arguments (`C6`).

#### Intent

Implement `LedgerRelianceError`, backward-compatible `write_year_digests(self, *, before=None)`, `verify_ledger_before_reliance`, and `require_verified_ledger_for_reliance` in `store.py` (with supporting digest-directory inspection in `ledger.py`).

#### Boundaries

* Included:
  * `LedgerRelianceError(RuntimeError)` with `.report` and `.problems` attributes and secret-free summary message.
  * Atomic write-once `ledger.write_year_digest` (and `write_digest`) via sibling temp file in `directory` + `os.link`, treating `FileExistsError` as benign already-sealed completion and unlinking the temp file in `finally` (`PC-001`).
  * Input validation on `require_sealed_past_years: bool = True`, `current_year: int | None = None` (`1..9999`, rejecting `bool`), and `seal_past_years: bool = True`, formatting `year_cutoff = f"{effective_year:04d}"` (`PC-005`).
  * Single-lock execution under `self._reliance_lock()` (`self.lock` on `Store`, `self.dblock` on `SqlStore`/`MssqlStore`) wrapped across snapshot, pre-check, sealing, and post-check in one `(_reliance_db_errors(), OSError, ValueError, TypeError, KeyError, RuntimeError)` secret-free handler (`PC-001`).
  * `_reliance_audit_snapshot()` on `Store` reading `list(self.audit_entries())` and comparing tail hash against `self.last_hash`.
  * Validation using ASCII regexes (`^[0-9]{4}$` in `0001..9999`, `^[0-9a-f]{64}$`, `^year-([0-9]{4})\.json$`, `^digest-([0-9]{10})\.json$`) across audit entries, `digest_dir` (`not os.path.lexists` treated as empty; non-directory, broken symlink, or `scandir` `OSError` failing closed), root `digest-{count:010d}.json` files (non-bool `int` `count >= 0`, `head == GENESIS` when `count == 0`), and `year-{YYYY}.json` filename-to-`year` agreement plus `sha256` / `main` / positive `int` `count` / 64-hex `first_prev` & `head` (`PC-005`).
  * Pre-seal verification (`verify_entries` + existing `verify_years` + backend head parity) so `write_year_digests(before=year_cutoff)` runs only when `seal_past_years=True` and pre-checks have zero problems (falling back to 0-arg `self.write_year_digests()` if a custom mock overrides it without `before`, `PC-001`, `PC-005`).
  * Post-seal `self.verify_ledger_by_year()` check, explicit mapping of `missing_years`, `bad_digests`, and `digest_mismatches` into `problems` (`PC-005`), and verification that every year `< year_cutoff` present in `years` has `sealed == True` and `intact == True` when `require_sealed_past_years=True`.
  * Sanitization of all `problems` (`code`, `year`, `reason`, optional `entry`/`digest_count`) and `sealed_digest_files` (basenames only).
* Excluded: SQL `audit_head` query logic (handled in `P01-T02`).

#### Likely Targets

* `src/core/src/zava_forward/core/ledger.py`
* `src/core/src/zava_forward/core/store.py`

#### Dependencies

* None.

#### Validation Expectations

* `Store` unit tests in `test_recovery.py` and `python3 -m ruff check` in `src/core`.

#### Completion Evidence

* `Store.verify_ledger_before_reliance` and `Store.require_verified_ledger_for_reliance` pass all intact and negative cases without leaking file paths or raw exception strings.

#### Unresolved Items

* None.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Wire atomic `audit_head` snapshot and `dberror`-safe reliance hook in `SqlStore` (inherited by `MssqlStore`)

#### Context

`SqlStore` (`sqlstore.py:414-424, 486-496`) tracks `(count, hash)` in `audit_head` under `self.dblock`. `MssqlStore` (`mssqlstore.py:217-224`) inherits from `SqlStore` and defines `dberror` as a property that imports `mssql_python`.

#### Intent

Re-export `LedgerRelianceError` in `sqlstore.py` and override `_reliance_audit_snapshot()` on `SqlStore` so both `SqlStore` and `MssqlStore` atomically read `(entries, audit_head)` and catch database driver errors without leaking connection strings or failing when `mssql_python` is not installed.

#### Boundaries

* Included:
  * Re-export `from .store import LedgerRelianceError as LedgerRelianceError` in `sqlstore.py` (`PC-006` `F401`-clean).
  * Override `_reliance_lock(self)` returning `self.dblock` and override `write_year_digests(self, *, before=None)` under `with self.dblock:` so `SqlStore`/`MssqlStore` never invert `self.dblock -> _SyncLock` (`PC-001`).
  * Implement `_reliance_db_errors(self)` helper on `Store`/`SqlStore` that safely resolves `self.dberror` (catching `ImportError` so mocked/offline `MssqlStore` instances work without `mssql_python`).
  * Override `_reliance_audit_snapshot(self)` in `SqlStore` under `with self.dblock:` to query `SELECT count, hash FROM audit_head WHERE id=1` directly first (reporting `audit_head_missing` if `None` and validating non-bool `int` `count >= 0` and lowercase 64-hex `hash`, equal to `GENESIS` when `count == 0`), then fetch unfiltered `SELECT seq, at, who, action, case_id, detail, prev, hash FROM audit ORDER BY seq` (flagging any non-int or `seq < 1` row) bracketed by an `audit_head` equality recheck (`PC-003`).
* Excluded: Changes to `mssqlstore.py` DDL or live network driver logic.

#### Likely Targets

* `src/core/src/zava_forward/core/sqlstore.py`

#### Dependencies

* `P01-T01`.

#### Validation Expectations

* `SqlStore` and `MssqlStore`-subclass tests in `test_sqlstore.py` and `test_recovery.py`.

#### Completion Evidence

* Trigger-bypassed edits, `audit_head` mismatches, unsealed `2026` tail deletions, and simulated DB driver errors with secret connection strings all fail closed with `reliance_allowed=False` and secret-free `LedgerRelianceError`.

#### Unresolved Items

* None.

<!-- rpi:phase id=P02 -->
## P02: Load-Check Latency and Structured PRD Cost Contract

### Context

`src/core/src/zava_forward/core/synthetic/loadcheck.py` measures NFR-002 request latency (`list <= 1.0s`, `detail <= 1.0s`, `write <= 2.0s` at 5 sessions, 2 writers) but currently records no `cost` or structured `load` section (`C11`). PRD and `BRD OD-51` (`C3`, `C4`) require honest `"Unknown"` reporting when meter evidence is missing rather than fabricating `0`, and `test_loadcheck.py` (`C12`) requires existing CLI invocations without cost flags to exit `0` when latency passes and `errors == 0`.

### Intent

Add `evaluate_cost` and extend `run` and `main` (`--vcore-seconds`, `--meter-rate`, `--cost-target`) in `loadcheck.py` to record measured load, per-class latency against `LIMITS`, and structured `cost` against PRD targets.

### Boundaries

* Included: `src/core/src/zava_forward/core/synthetic/loadcheck.py`.
* Excluded: Live Azure Billing/Retail Prices API network calls or changes to `LIMITS`.

### Likely Targets

* `src/core/src/zava_forward/core/synthetic/loadcheck.py`: Add `evaluate_cost`, extend `run` and `main`.

### Dependencies

* None.

### Validation Expectations

* Strict-`mypy` and `ruff format`-compliant unit tests in `src/core/tests/test_loadcheck.py`.

### Completion Evidence

* `loadcheck.evaluate_cost`, `loadcheck.run`, and `loadcheck.main` emit exact structured `cost` and `load` sections and preserve all existing tests and CLI exit codes.

### Unresolved Items

* None.

<!-- rpi:task id=P02-T01 -->
### P02-T01: Implement `evaluate_cost`, extend `run`, and add cost CLI flags to `main` in `loadcheck.py`

#### Context

`test_loadcheck.py` verifies pre-store validation (`Mock(spec=[])`), pre-`open_store` CLI `ap.error` exit `2` on invalid parameters (`nan`, `inf`, overflow, negative/zero), exact `env` keys `{"ZF_DATA", "ZF_STATE", "ZF_STORE"}`, and exit `0`/`1` tracking (`C12`).

#### Intent

Implement `evaluate_cost`, integrate `load` and `cost` into `run`, and add `--vcore-seconds`, `--meter-rate`, and `--cost-target` into `main`.

#### Boundaries

* Included:
  * `evaluate_cost(vcore_seconds: float | None = None, meter_rate_per_vcore_second: float | None = None, target_cost: float | None = None) -> dict[str, Any]`:
    * Reject `bool`, non-numeric, out-of-float-range (`not -sys.float_info.max <= val <= sys.float_info.max` checked before `float(val)`), non-finite (`NaN`, `Inf`), `vcore_seconds < 0`, `meter_rate_per_vcore_second <= 0`, and `target_cost < 0` with `ValueError`, normalizing `-0.0` to `0.0` (`PC-004`).
    * Populate `missing_inputs` in canonical order from `("vcore_seconds", "meter_rate_per_vcore_second", "target_cost")` for any `None` input.
    * When both `vcore_seconds` and `meter_rate_per_vcore_second` are provided: inside `decimal.localcontext(prec=60)` with traps cleared, compute `raw = Decimal(str(vcore_val)) * Decimal(str(rate_val))`, set `measured_cost = 0.0 if raw == 0 else float(raw)`, raise `ValueError` if `not math.isfinite(measured_cost)` or (`raw > 0 and measured_cost == 0.0`), set `status = "measured"`, and set `within_target = bool(raw <= Decimal(str(target_val)))` if `target_cost is not None` else `None` (`PC-004`).
    * When either `vcore_seconds` or `meter_rate_per_vcore_second` is `None`: set `status = "Unknown"`, `measured_cost = None`, `within_target = None`.
    * Always include `azure_live_run_human_gated: True`.
  * `run(store: Any, user: dict[str, Any], seconds: float, sessions: int = 5, writers: int = 2, *, vcore_seconds: float | None = None, meter_rate_per_vcore_second: float | None = None, target_cost: float | None = None) -> dict[str, Any]` (`PC-006`):
    * Call `evaluate_cost(...)` at function entry (before accessing `store.cases`).
    * Return `classes`, `load` (`sessions`, `writers`, `seconds`, `total_requests`, `achieved_rps = round(total_requests / float(seconds), 4)` with zero extra calls to `time.monotonic`, `time.perf_counter`, or `time.time`, `PC-002`), `cost`, `errors`, `error_kinds`.
  * `main(argv=None)`:
    * Add `--vcore-seconds`, `--meter-rate`, `--cost-target` (`type=float, default=None`).
    * Validate `evaluate_cost(args.vcore_seconds, args.meter_rate, args.cost_target)` inside the pre-`open_store` validation block, calling `ap.error(str(exc))` on `ValueError`.
    * Pass cost arguments to `run(...)` and return `0` iff `rep["errors"] == 0 and all(c["within"] for c in rep["classes"].values()) and rep["cost"]["within_target"] is not False` else `1`.
* Excluded: Mutating `env` passed to `open_store(env)`.

#### Likely Targets

* `src/core/src/zava_forward/core/synthetic/loadcheck.py`

#### Dependencies

* None.

#### Validation Expectations

* `src/core/tests/test_loadcheck.py` passes under `unittest`, `ruff`, and `mypy`.

#### Completion Evidence

* Measured and `Unknown` cost scenarios and CLI exit-code tests (`0`, `1`, `2`) pass alongside all 16 existing `test_loadcheck.py` tests.

#### Unresolved Items

* None.

<!-- rpi:phase id=P03 -->
## P03: Multi-Year Unit Proofs, Documentation, and Focused Validation

### Context

Acceptance requires multi-year (`2024`, `2025`, `2026`) unit proofs in `test_recovery.py` and `test_sqlstore.py`, cost/latency unit proofs in `test_loadcheck.py`, synchronized documentation in `src/core/README.md`, and clean focused validation (`TMPDIR=/dev/shm` unittest, `ruff check`, `ruff format --check`, `mypy`).

### Intent

Author focused unit tests across all three test modules, update `src/core/README.md`, and verify zero test, lint, format, or typing issues.

### Boundaries

* Included: `src/core/tests/test_recovery.py`, `src/core/tests/test_sqlstore.py`, `src/core/tests/test_loadcheck.py`, `src/core/README.md`.
* Excluded: `python3 tools/rpi-checks.py --all`, unrelated test suites outside `src/core`.

### Likely Targets

* `src/core/tests/test_recovery.py`
* `src/core/tests/test_sqlstore.py`
* `src/core/tests/test_loadcheck.py`
* `src/core/README.md`

### Dependencies

* `P01`, `P02`.

### Validation Expectations

* `TMPDIR=/dev/shm PYTHONPATH=src/core/src:src/core/tests python3 -m unittest src/core/tests/test_loadcheck.py src/core/tests/test_recovery.py src/core/tests/test_sqlstore.py -q`
* `(cd src/core && python3 -m ruff check && python3 -m ruff format --check && python3 -m mypy)`

### Completion Evidence

* Zero failures across targeted unit tests, full `src/core` unit test sanity run, `ruff check`, `ruff format --check`, and `mypy`.

### Unresolved Items

* None.

<!-- rpi:task id=P03-T01 -->
### P03-T01: Add multi-year (`2024`, `2025`, `2026`) pre-reliance unit tests in `test_recovery.py` and `test_sqlstore.py`

#### Context

`test_recovery.py` tests year digest primitives and `SqlStore` year sealing (`lines 51-82`), and `test_sqlstore.py` exercises `SqlStore` and SQL audit triggers. A new multi-year `Store` helper in `test_recovery.py` will seed `audit.jsonl` prior to constructing `Store(data_path)` so `Store.last_hash` matches the seeded tail (`PC-006`).

#### Intent

Prove pre-reliance verification across `2024`, `2025`, and `2026` audit entries in both `test_recovery.py` and `test_sqlstore.py` (including `MssqlStore` inheritance), using `current_year=2026` for rollover-safe `2026`-active assertions alongside default wall-clock tests (`PC-006`).

#### Boundaries

* Included:
  * `test_recovery.py`: Multi-year (`2024`, `2025`, `2026`) `Store` tests verifying intact pre-reliance sealing (`2024` & `2025` sealed, `2026` active) and `require_verified_ledger_for_reliance` success; blocking reliance on tampered `2024`/`2026` entries (confirming pre-seal tampering does not write `year-2024.json`), dropped `2024` entries after sealing, corrupt/swapped `year-2024.json`, corrupt `digest-*.json`, unsealed past year when `seal_past_years=False`, and corrupt `audit.jsonl` without path/secret leakage.
  * `test_sqlstore.py`: Multi-year (`2024`, `2025`, `2026`) `SqlStore` and `MssqlStore`-subclass tests verifying intact pass, SQL trigger-bypassed tampering, dropped sealed year, unsealed `2026` tail deletion caught via `audit_head`, corrupt digest, and DB driver exception secret scrubbing (`Server=tcp:...;Password=...` absent from `problems` and `LedgerRelianceError`).
* Excluded: Live SQL Server container requirement (offline tests run in-process with `TMPDIR=/dev/shm`).

#### Likely Targets

* `src/core/tests/test_recovery.py`
* `src/core/tests/test_sqlstore.py`

#### Dependencies

* `P01-T01`, `P01-T02`.

#### Validation Expectations

* `TMPDIR=/dev/shm PYTHONPATH=src/core/src:src/core/tests python3 -m unittest src/core/tests/test_recovery.py src/core/tests/test_sqlstore.py -q`

#### Completion Evidence

* All multi-year positive and negative reliance assertions pass.

#### Unresolved Items

* None.

<!-- rpi:task id=P03-T02 -->
### P03-T02: Add typed `loadcheck` cost/latency unit tests in `test_loadcheck.py`, update `src/core/README.md`, and run focused validation

#### Context

`test_loadcheck.py` is type-checked by strict `mypy` and formatted by `ruff format` (`src/core/pyproject.toml`). `src/core/README.md` (`lines 4671-4702`) documents Issue #114 ledger and `loadcheck` usage.

#### Intent

Add fully typed unit tests in `test_loadcheck.py` for measured vs `Unknown` cost reporting and CLI exit codes, update `src/core/README.md`, and run the focused validation suite.

#### Boundaries

* Included:
  * `test_loadcheck.py`: Typed tests (avoiding `[unused-ignore]` on `bool` arguments under PEP-484 `bool <: float`, `PC-006`) for `evaluate_cost` (measured within target including 8-decimal Azure vCore-second rates, measured over target, measured without target, omitted/partial inputs returning `status="Unknown"` with `missing_inputs` and `azure_live_run_human_gated=True`, invalid negative/zero/NaN/Inf/large-`int`/bool rejection), `run` (`load` + `cost` fields and pre-store invalid cost rejection), and `main` (`--vcore-seconds`, `--meter-rate`, `--cost-target` exit `0` within target, exit `1` exceeding target, exit `0` when omitted on good latency run, exit `2` before `open_store` on invalid flags).
  * `src/core/README.md`: Concise update in the Issue #114 subsection documenting `verify_ledger_before_reliance` / `require_verified_ledger_for_reliance` and `loadcheck` cost options + `Unknown` / Azure human-gated boundaries.
* Excluded: Modifying any existing assertions in `test_loadcheck.py`.

#### Likely Targets

* `src/core/tests/test_loadcheck.py`
* `src/core/README.md`

#### Dependencies

* `P02-T01`, `P03-T01`.

#### Validation Expectations

* Targeted unittest command + `ruff check` + `ruff format --check` + `mypy` inside `src/core`.

#### Completion Evidence

* Zero failures across unit tests, `ruff check`, `ruff format --check`, and `mypy`.

#### Unresolved Items

* None.

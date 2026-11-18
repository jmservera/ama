<!-- markdownlint-disable-file -->
# RPI Plan Critique: Issue #114 Per-Year Ledger Pre-Reliance Verification and Load-Check Cost Contract

## Metadata

* Task ID: issue-114-platform-sql-ledger-loadcheck
* Critique date: 2026-11-15
* Plan: .copilot-tracking/plans/2026-11-15/platform-114-sql-ledger-loadcheck-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/platform-114-sql-ledger-loadcheck-phase-details.md
* Critique execution status: Complete

## Inputs and Criterion Boundary

* Task context and caller requirements: Deliver the bounded offline `src/core` engineering slice for Issue #114 (`Durable Azure SQL store with ledger audit`, `Refs #114`): (1) `verify_ledger_before_reliance(self, *, require_sealed_past_years: bool = True) -> dict[str, Any]`, `require_verified_ledger_for_reliance(self)`, and secret-free `LedgerRelianceError` across `Store`, `SqlStore`, and inherited `MssqlStore`, proven across multi-year (`2024`, `2025`, `2026`) audit entries in `src/core/tests/test_recovery.py` and `src/core/tests/test_sqlstore.py`; (2) `evaluate_cost`, `run`, and `main` (`--vcore-seconds`, `--meter-rate`, `--cost-target`) in `src/core/src/zava_forward/core/synthetic/loadcheck.py` recording measured load, per-class latency against `LIMITS`, and structured `cost` (`status: "measured" | "Unknown"`, `vcore_seconds`, `meter_rate_per_vcore_second`, `measured_cost`, `target_cost`, `within_target`, `missing_inputs`, `azure_live_run_human_gated: True`), proven in `src/core/tests/test_loadcheck.py` while preserving all existing assertions and CLI exit codes; and (3) focused validation (`TMPDIR=/dev/shm` targeted unittest, `ruff check`, `ruff format --check`, `mypy` inside `src/core`; no `tools/rpi-checks.py --all`, local commit only, no push or PR).
* Research and evidence considered: .copilot-tracking/research/2026-11-15/platform-114-sql-ledger-loadcheck-research.md, .copilot-tracking/plans/2026-11-15/platform-114-sql-ledger-loadcheck-plan.md, .copilot-tracking/details/2026-11-15/platform-114-sql-ledger-loadcheck-phase-details.md, src/core/src/zava_forward/core/store.py, src/core/src/zava_forward/core/sqlstore.py, src/core/src/zava_forward/core/mssqlstore.py, src/core/src/zava_forward/core/ledger.py, src/core/src/zava_forward/core/synthetic/loadcheck.py, src/core/tests/test_recovery.py, src/core/tests/test_sqlstore.py, src/core/tests/test_loadcheck.py, src/core/pyproject.toml, src/core/README.md.
* Decisions, dependencies, and acceptance criteria considered: Confirmed `Option A` inheritance design (`Store` contract + `SqlStore` `audit_head` hook inherited by `MssqlStore`), pre-seal integrity verification before writing immutable year digests, honest `"Unknown"` cost reporting when meter inputs are absent (`BRD OD-51`), `azure_live_run_human_gated: True`, `Refs #114` non-closing attribution, and focused `src/core` validation tier.
* Assessment boundary: Evaluates full correctness, concurrency/locking, numeric/CLI parsing, schema/digest edge cases, and `ruff`/`mypy`/unittest compatibility against the supplied artifacts and referenced `src/core` files. Live Azure SQL `GP_S_Gen5` metered execution and witnessed `DH-005` point-in-time restore drills are explicitly external human/cloud gates outside this offline boundary.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
|------------------------------------------|----------|---------------------|
| FR-1 (`Store`/`SqlStore`/`MssqlStore` pre-reliance verification) | Partial | Core inheritance and pre-seal design are sound (`C6`-`C10`), but `P01-T01` and `P01-T02` leave unlocked multi-snapshot TOCTOU/`_SyncLock` hazards, uncaught DB errors during seal/post-check, non-atomic `write_year_digest` races (`PC-001`), `_audit_rows(0)` missing-head/negative-`seq` traps (`PC-003`), and `< 1000` year/empty-digest/Unicode/dropped-year mapping edge cases (`PC-005`). |
| FR-2 (`loadcheck` measured load, latency, and PRD cost contract) | Partial | Report fields and CLI exit-code preservation align with `C3`, `C4`, `C11`, and `C12`, but `P02-T01` omits the zero-extra-clock-call constraint for `achieved_rps` (`PC-002`) and has `int->float` `OverflowError`, `Decimal` product float-overflow/`-0.0`, and 6-decimal truncation defects on Azure vCore-second rates (`PC-004`). |
| FR-3 (`src/core/README.md` synchronization) | Covered | `P03-T02` targets `src/core/README.md` (`lines 4671-4702`) while preserving explicit unverified Azure SQL / `DH-005` honesty boundaries (`C5`). |
| NFR Secret-free, path-free error and problem reporting | Partial | Sentinel scrubbing is planned for `_reliance_audit_snapshot`, but `P01-T01` catches only `OSError` around `write_year_digests` and wraps post-seal `verify_ledger_by_year` in no DB-error handler (`PC-001`). |
| NFR Deterministic calendar-year boundary handling | Partial | `current_year` injection is planned, but `< 1000` `str(before)` comparison, `0`-arg `write_year_digests()` clock re-read, Unicode `.isdigit()`, and `2026` active-year rollover after `2027-01-01` need explicit specification (`PC-005`, `PC-006`). |
| NFR Lint, format, and static typing compliance | Partial | Validation commands match `src/core/pyproject.toml`, but `P01-T02`, `P02-T01`, and `P03-T02` contain concrete `ruff` `F401` and `mypy --strict` (`no-untyped-call` / `unused-ignore`) traps (`PC-006`). |
| C1-C12 (Research evidence mapping) | Covered | All 12 research citations trace accurately to `store.py`, `sqlstore.py`, `mssqlstore.py`, `ledger.py`, `loadcheck.py`, `test_loadcheck.py`, and `src/core/README.md`. |
| P01 / P01-T01 | Partial | Needs single-lock verified-snapshot sealing, full exception trapping across seal/post-check, atomic write-once year digests, 4-digit ASCII year/digest rules, and `count == 0` `GENESIS` root-digest handling (`PC-001`, `PC-005`). |
| P01 / P01-T02 | Partial | Needs explicit `audit_head` pre-check and unfiltered `ORDER BY seq` query instead of `_audit_rows(0)` (`PC-003`), plus `F401`-safe `LedgerRelianceError as LedgerRelianceError` re-export (`PC-006`). |
| P02 / P02-T01 | Partial | Needs clock-free `achieved_rps` definition (`PC-002`), `sys.float_info.max` pre-float bounds + `decimal.localcontext` + non-truncating finite `float(raw)` (`PC-004`), and full type annotations on `run` keyword arguments (`PC-006`). |
| P03 / P03-T01 | Partial | References a non-existent `_store_with_years` helper in `test_recovery.py` and needs pre-init `audit.jsonl` seeding (`Store.last_hash`) plus explicit `current_year=2026` for rollover-safe `2026`-active assertions (`PC-006`). |
| P03 / P03-T02 | Partial | Needs PEP-484 `bool <: float` awareness so `test_loadcheck.py` does not trigger `mypy` `[unused-ignore]` (`PC-006`). |

## Verdict

* Verdict: Revise
* Rationale: The candidate plan's overall architecture (`Option A` inheritance across `Store`/`SqlStore`/`MssqlStore`, pre-seal integrity gate, and `Decimal`-backed `loadcheck` cost contract with `"Unknown"` missing-input reporting) is well-aligned with all caller requirements, ADRs, and PRD boundaries, and has no missing research or unresolved user decisions. However, six concrete implementation-level defects in the plan and phase details (`PC-001` through `PC-006`) would cause secret leakage or lock hazards during SQL sealing, break six existing `test_loadcheck.py` clock-mocked tests, mishandle missing `audit_head` or `seq <= 0` rows in `SqlStore`, raise `OverflowError` or truncate real Azure vCore-second costs in `evaluate_cost`, or fail `ruff check` (`F401`) and `mypy --strict`. All six findings are bounded planner-owned corrections requiring no user input.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Unlocked multi-snapshot sealing/verification, uncaught non-OSError SQL faults during seal/post-check, and non-atomic `write_year_digest` file creation

* Related IDs: FR-1, NFR Secret-free, path-free error and problem reporting, C7, C8, C9, C10, P01, P01-T01, P01-T02
* Evidence: .copilot-tracking/details/2026-11-15/platform-114-sql-ledger-loadcheck-phase-details.md, src/core/src/zava_forward/core/store.py, src/core/src/zava_forward/core/sqlstore.py, src/core/src/zava_forward/core/ledger.py
* Concern: `P01-T01` reads `_reliance_audit_snapshot()`, releases the lock, calls `self.write_year_digests(...)` catching only `OSError`, and then calls `self.verify_ledger_by_year()` with no exception wrapper. Three bugs interact here: (1) on `SqlStore`/`MssqlStore`, inherited `Store.write_year_digests()` (`store.py:206`) acquires `self.lock` (`_SyncLock`), which runs `self._sync()` across unrelated tables (`cases`, `recommendations`, `meta`) and re-reads `self.audit_entries()` in a second unverified snapshot, while `verify_ledger_by_year()` (`store.py:203`) re-reads `self.audit_entries()` in a third snapshot; holding `self.dblock` across `self.write_year_digests()` would invert `SqlStore`'s `self.lock -> self.dblock` lock hierarchy (`sqlstore.py:135, 146, 1534, 1565`) and deadlock, whereas releasing the lock opens a TOCTOU window where unverified concurrent entries can be sealed or `entries`/`head` can diverge from `years`; (2) neither `sqlite3.Error` nor `mssql_python.Error` inherits from `OSError`, so any DB/driver error or `_sync()` `RuntimeError` during `write_year_digests()` or `verify_ledger_by_year()` escapes uncaught with raw connection strings; and (3) `ledger.write_year_digest` (`ledger.py:121-124`) checks `if not os.path.exists(path): with open(path, "x") ... json.dump(...)`, so concurrent callers sharing `digest_dir` either hit `FileExistsError` (falsely reported as `year_digest_seal_failed`) or read a 0-byte half-written `year-YYYY.json`.
* Impact: Can leak database credentials on transient driver faults during seal/post-check, cause AB-BA deadlocks or seal unverified concurrent mutations, and falsely fail multi-process startup reliance checks.
* Smallest useful change: Hold one backend-appropriate reliance lock across the full snapshot + pre-check + seal + post-check flow (`self.lock` on `Store`; `self.dblock` on `SqlStore`/`MssqlStore`, never acquiring `_SyncLock` inside `self.dblock`, and overriding or routing `write_year_digests` on `SqlStore` under `self.dblock` so `_SyncLock` is not entered); seal completed past years directly from the already-verified `entries` snapshot; wrap sealing and post-seal digest verification in the same `(_reliance_db_errors(), OSError, ValueError, TypeError, KeyError, RuntimeError)` secret-free handler; and make `ledger.write_year_digest` (and `write_digest`) write to a sibling temporary file in `directory` and publish write-once via `os.link` (treating `FileExistsError` as benign already-sealed completion and unlinking the temp file in `finally`).
* Action owner: planning_parent
* Exact resolving evidence: Revised `P01-T01` and `P01-T02` specifying single-lock verified-snapshot sealing without `dblock -> _SyncLock` inversion, full DB/OS/JSON error trapping across seal and post-check, and atomic write-once `write_year_digest` creation.
* Decision route: Direct planner correction.

<!-- rpi:critique id=PC-002 -->
### PC-002 [High]: Unspecified `achieved_rps` clock usage in `loadcheck.run` would break six existing clock-mocked tests in `test_loadcheck.py`

* Related IDs: FR-2, C11, C12, P02, P02-T01
* Evidence: .copilot-tracking/details/2026-11-15/platform-114-sql-ledger-loadcheck-phase-details.md, src/core/src/zava_forward/core/synthetic/loadcheck.py, src/core/tests/test_loadcheck.py
* Concern: `P02-T01` adds `load` (`sessions`, `writers`, `seconds`, `total_requests`, `achieved_rps`) to `loadcheck.run` without defining how `achieved_rps` obtains elapsed time. In `src/core/tests/test_loadcheck.py` (`lines 67-80, 142, 167, 187, 197, 208-212, 241, 330-358`), existing tests forbid `time.time` (`AssertionError("wall clock used")`), pass exact-length `side_effect` lists to `time.monotonic` while asserting `self.assertEqual(clock.call_count, 4)` (`line 212`), and pass exact `[start, end]` request pairs to `time.perf_counter`. Any extra call to `time.monotonic()`, `time.perf_counter()`, or `time.time()` to compute `achieved_rps` raises `StopIteration`, corrupts per-request latency pairs, or fails `clock.call_count == 4`.
* Impact: Directly breaks Caller Requirement 2 to preserve all existing `test_loadcheck.py` assertions.
* Smallest useful change: Specify in `P02-T01` that `total_requests = sum(c["n"] for c in rep.values())` and `achieved_rps = round(total_requests / float(seconds), 4)` using the validated `seconds` argument directly, with zero additional calls to `time.monotonic`, `time.perf_counter`, or `time.time`.
* Action owner: planning_parent
* Exact resolving evidence: Revised `P02-T01` specifying `achieved_rps = round(total_requests / float(seconds), 4)` without extra clock reads, verified by all 16 existing `test_loadcheck.py` tests passing unchanged.
* Decision route: Direct planner correction.

<!-- rpi:critique id=PC-003 -->
### PC-003 [High]: `SqlStore._audit_rows(0)` raises retry `RuntimeError` when `audit_head` is missing and skips tampered `seq <= 0` rows read by `audit_entries()`

* Related IDs: FR-1, C9, C10, P01-T02, P03-T01
* Evidence: .copilot-tracking/details/2026-11-15/platform-114-sql-ledger-loadcheck-phase-details.md, src/core/src/zava_forward/core/sqlstore.py
* Concern: `P01-T02` instructs `SqlStore._reliance_audit_snapshot(self)` to detect `audit_head_missing` and `audit_head_mismatch` alongside `_audit_rows(0)`. In `src/core/src/zava_forward/core/sqlstore.py` (`lines 414-424`), `_audit_rows(0)` has three incompatibilities with pre-reliance tamper detection: (1) if `audit_head` (`id=1`) is missing (`before is None`), `_audit_rows(0)` retries 5 times and raises `RuntimeError("The audit ledger kept changing while its creation events were read.")` instead of reporting `audit_head_missing`; (2) `_audit_rows(0)` filters `WHERE seq > 0`, whereas `SqlStore.audit_entries()` (`line 1491`) queries `SELECT ... FROM audit ORDER BY seq` with no `WHERE seq > 0` predicate, so a trigger-bypassed row inserted with `seq <= 0` is invisible to `_audit_rows(0)` yet visible to `audit_entries()`; and (3) `int(before[0])` does not reject `bool` or negative counts or non-64-hex `audit_head.hash` values.
* Impact: Missing `audit_head` rows fail with the wrong error reason, and `seq <= 0` SQL tampering bypasses snapshot parity against `audit_entries()`.
* Smallest useful change: Specify in `P01-T02` that `SqlStore._reliance_audit_snapshot` directly queries `SELECT count, hash FROM audit_head WHERE id=1` first (immediately recording `audit_head_missing` if `None`, and validating non-bool `int` `count >= 0` and 64-lowercase-hex `hash`, equal to `GENESIS` when `count == 0`), then fetches `SELECT seq, at, who, action, case_id, detail, prev, hash FROM audit ORDER BY seq` (with no `WHERE seq > 0` filter, flagging any non-int or `seq < 1` row) bracketed by an `audit_head` equality recheck.
* Action owner: planning_parent
* Exact resolving evidence: Revised `P01-T02` replacing `_audit_rows(0)` reliance with explicit `audit_head` existence/schema validation and unfiltered `ORDER BY seq` snapshot query.
* Decision route: Direct planner correction.

<!-- rpi:critique id=PC-004 -->
### PC-004 [Medium]: `loadcheck.evaluate_cost` has large-`int` `OverflowError`, `Decimal` product float-overflow/`-0.0`, and 6-decimal truncation defects on Azure vCore-second rates

* Related IDs: FR-2, C3, C4, C11, C12, P02-T01
* Evidence: .copilot-tracking/details/2026-11-15/platform-114-sql-ledger-loadcheck-phase-details.md, src/core/src/zava_forward/core/synthetic/loadcheck.py, src/core/tests/test_loadcheck.py
* Concern: `P02-T01` computes `raw = Decimal(str(float(vcore_seconds))) * Decimal(str(float(meter_rate_per_vcore_second)))`, `measured_cost = round(float(raw), 6)`, and `within_target = bool(raw <= Decimal(str(float(target_cost))))`. Four numeric edge cases arise: (1) passing a huge `int` such as `10**400` (already tested in `test_loadcheck.py:114, 281`) causes `float(...)` to raise `OverflowError` instead of `ValueError` unless `-sys.float_info.max <= x <= sys.float_info.max` is checked before `float(x)`; (2) multiplying two finite floats such as `1e200 * 1e200` produces `float(raw) == inf` (emitting invalid JSON `Infinity` instead of raising `ValueError`), and using the ambient thread-local `Decimal` context (`prec=28`) instead of `decimal.localcontext(prec=60)` risks caller trap/precision interference; (3) `-0.0` passes `< 0` checks and emits `-0.0` unless normalized to `0.0`; and (4) `round(float(raw), 6)` truncates real Azure SQL Serverless per-vCore-second rates (`~$0.00014494/vCore-s`, 8 decimal places), rounds small positive runs (`e.g., 0.001 * 0.000145 = 1.45e-7`) to a misleading `0.0` (`BRD OD-51`), and can report `measured_cost == target_cost` alongside `within_target: False`.
* Impact: Large-integer inputs raise `OverflowError` instead of `ValueError` / CLI exit `2`, extreme products leak `Infinity`, and 6-decimal rounding distorts small or per-second Azure SQL meter calculations.
* Smallest useful change: In `P02-T01`, validate `-sys.float_info.max <= val <= sys.float_info.max` before `float(val)` conversion (raising `ValueError`), normalize `-0.0` to `0.0`, compute `raw` inside `decimal.localcontext(prec=60)` with traps cleared, set `measured_cost = 0.0 if raw == 0 else float(raw)`, and raise `ValueError` if `not math.isfinite(measured_cost)` or (`raw > 0 and measured_cost == 0.0`).
* Action owner: planning_parent
* Exact resolving evidence: Revised `P02-T01` specifying `sys.float_info.max` pre-float bounds, `-0.0` normalization, isolated `decimal.localcontext(prec=60)`, and non-truncating finite `float(raw)` with overflow/underflow `ValueError` guards.
* Decision route: Direct planner correction.

<!-- rpi:critique id=PC-005 -->
### PC-005 [Medium]: Year-cutoff `< 1000` string comparison, Unicode `.isdigit()` bypass, empty-store `digest-0000000000.json` (`count=0`), and dropped-year `problems` mapping gaps in `P01-T01`

* Related IDs: FR-1, NFR Deterministic calendar-year boundary handling, C7, C8, P01-T01, P03-T01
* Evidence: .copilot-tracking/details/2026-11-15/platform-114-sql-ledger-loadcheck-phase-details.md, src/core/src/zava_forward/core/ledger.py, src/core/src/zava_forward/core/store.py, src/core/src/zava_forward/core/sqlstore.py
* Concern: Four subtle edge cases exist in `P01-T01`'s validation rules: (1) `P01-T01` allows `current_year` in `1..9999` and passes `before=effective_year` (or `0` args when `current_year is None`) to `write_year_digests`, while `ledger.year_digests` (`ledger.py:74`) evaluates `y < str(before)` - for `effective_year < 1000` (e.g., `999`), `"2024" < "999"` is `True`, sealing future years, and `0`-arg `write_year_digests()` re-reads `datetime.now().year` instead of reusing `effective_year`; (2) `Store.write_digest()` on an empty store creates `digest-0000000000.json` (`count=0, head=GENESIS`), where `ledger.verify_entries` (`ledger.py:53`) skips checking `head` when `cnt == 0` while `SqlStore._malformed_anchor` (`sqlstore.py:493`) rejects `count < 1`, and `P01-T01` does not specify `digest-{count:010d}.json` filename-to-`count` binding or `count == 0` `GENESIS` rules; (3) Python `str.isdigit()` accepts non-ASCII digits (e.g., `"٢٠٢٤"`), which sort `> "2026"` and evade past-year sealing unless ASCII `^[0-9]{4}$` is enforced, and `digest_dir` validation must treat a non-existent path (`not os.path.lexists`) as empty while failing closed on non-directories, broken symlinks, or unreadable directories; and (4) when an entire sealed year is dropped (or all entries are wiped while `year-2024.json` remains), `rep["years"]` omits `"2024"` and only `rep["missing_years"]` is non-empty, requiring explicit translation of `missing_years`, `bad_digests`, and `digest_mismatches` into `problems` so `bool(problems) == (not reliance_allowed)` always holds.
* Impact: Can mis-seal years on `< 1000` cutoffs or midnight rollovers, falsely fail or overlook tampered `digest-0000000000.json` on empty ledgers, or produce `reliance_allowed=False` with empty `problems` when a sealed year is completely dropped.
* Smallest useful change: Format `before` as `f"{effective_year:04d}"` in `Store.write_year_digests` and `verify_ledger_before_reliance`; enforce ASCII patterns (`^[0-9]{4}$` in `0001..9999`, `^[0-9a-f]{64}$`, `^year-([0-9]{4})\.json$`, `^digest-([0-9]{10})\.json$`); accept root `digest-*.json` with non-bool `int` `count >= 0`, filename agreement, and `head == GENESIS` when `count == 0`; accept absent `digest_dir` via `not os.path.lexists` while rejecting non-directories or `scandir` `OSError`; and explicitly map `missing_years`, `bad_digests`, and `digest_mismatches` into `problems`.
* Action owner: planning_parent
* Exact resolving evidence: Revised `P01-T01` specifying 4-digit ASCII `before`, ASCII regex validation, `count == 0` `GENESIS` root-digest validation, `lexists` `digest_dir` semantics, and complete `problems` mapping.
* Decision route: Direct planner correction.

<!-- rpi:critique id=PC-006 -->
### PC-006 [Medium]: `ruff` `F401` re-export failure in `sqlstore.py`, `mypy --strict` traps in `loadcheck.py` and `test_loadcheck.py`, and missing `_store_with_years` / `2027` rollover setup in `P03-T01`

* Related IDs: FR-1, FR-2, NFR Lint, format, and static typing compliance, C12, P01-T02, P02-T01, P03-T01, P03-T02
* Evidence: src/core/pyproject.toml, .copilot-tracking/details/2026-11-15/platform-114-sql-ledger-loadcheck-phase-details.md, src/core/tests/test_recovery.py, src/core/tests/test_loadcheck.py
* Concern: Three Concrete tooling/test pitfalls appear in the phase details: (1) `src/core/pyproject.toml` (`line 50`) does not ignore `F401` on `sqlstore.py`, so `P01-T02`'s bare re-export of `LedgerRelianceError` in `sqlstore.py` (where `LedgerRelianceError` is not otherwise referenced) fails `python3 -m ruff check` unless written as `from .store import LedgerRelianceError as LedgerRelianceError` (or exported via `__all__`); (2) `test_loadcheck.py` runs under full `mypy` `strict = true` (`disallow_untyped_calls = true`, `warn_unused_ignores = true`), so `P02-T01` must annotate `loadcheck.run`'s new keyword-only parameters (`vcore_seconds: float | None = None, meter_rate_per_vcore_second: float | None = None, target_cost: float | None = None`), and `P03-T02` must not place `# type: ignore[arg-type]` on `bool` arguments passed to `float | None` parameters (`bool <: int <: float` in PEP 484, triggering `[unused-ignore]`); and (3) `P03-T01` states "`test_recovery.py` already has a `_store_with_years` helper (`lines 51-67`) for `Store`", whereas `test_recovery.py` currently neither defines `_store_with_years` nor imports `Store` - the new helper must write `audit.jsonl` *before* constructing `Store(data_path)` (so `Store.__init__` sets `self.last_hash` to the seeded tail hash), and tests asserting `2026` stays unsealed/active must pass `current_year=2026` (alongside a clock-patched or dynamic-year default test) so they do not fail after `2027-01-01`.
* Impact: Causes avoidable `ruff check` (`F401`), `mypy` (`unused-ignore` / untyped signature), `Store.last_hash` setup, and `2027` rollover test failures.
* Smallest useful change: Update `P01-T02` to require explicit `LedgerRelianceError as LedgerRelianceError` re-export; update `P02-T01` and `P03-T02` with typed `float | None = None` `run` kwargs and `mypy --strict`-clean invalid-argument typing; and update `P03-T01` to author the multi-year `Store` helper in `test_recovery.py` (seeding `audit.jsonl` prior to `Store` init) and pass `current_year=2026` when asserting `2026` remains active.
* Action owner: planning_parent
* Exact resolving evidence: Revised `P01-T02`, `P02-T01`, `P03-T01`, and `P03-T02` details and clean `0` exit codes from `ruff check`, `ruff format --check`, `mypy`, and targeted `unittest`.
* Decision route: Direct planner correction.

## Strengths and Residual Risk

* Strong architectural reuse: Anchoring `verify_ledger_before_reliance` and `require_verified_ledger_for_reliance` on `Store` with `SqlStore`'s `audit_head` snapshot hook cleanly covers `Store`, `SqlStore`, and `MssqlStore` without duplicating verification logic (`C8`-`C10`).
* Sound pre-seal invariant: Checking chain continuity, root digests, year-digest schema/filename binding, and `audit_head` *before* sealing completed past years prevents permanently sealing tampered unsealed history into write-once `year-YYYY.json` anchors.
* Honest PRD/OD-51 cost boundary: Preserving exit `0` when meter inputs are omitted (`status: "Unknown"`, `within_target: None`, `azure_live_run_human_gated: True`) while exiting `1` when an explicit `target_cost` is exceeded satisfies both `BRD OD-51` and existing `test_loadcheck.py` CLI exit contracts.
* Accepted residual risk: Live Azure SQL serverless (`GP_S_Gen5`) load/cost measurement and witnessed `DH-005` point-in-time restore drills remain external human/cloud gates tracked on Issue #114 (`Refs #114`, never `Closes #114`).

## Questions or Blocking Evidence Gaps

* None. All six findings are deterministic engineering refinements fully resolvable from the supplied codebase evidence without user input or further research.

## Limitations

* This critique is read-only and static against the supplied plan, phase details, research, and referenced `src/core` modules; validation commands (`unittest`, `ruff`, `mypy`) execute during `rpi-implement` after the plan revisions and code changes are applied.
* Live Azure SQL `mssql-python` connectivity and Azure Blob WORM container policies are out of scope for this offline `src/core` slice.

## Recommended Next Action

* Highest-impact finding: PC-001
* Action owner: planning_parent
* Smallest next action: Directly revise `.copilot-tracking/plans/2026-11-15/platform-114-sql-ledger-loadcheck-plan.md` and `.copilot-tracking/details/2026-11-15/platform-114-sql-ledger-loadcheck-phase-details.md` to incorporate `PC-001` through `PC-006`, record the critique disposition table, and mark the plan `Ready` for `rpi-implement` without a second critique pass.
* User response required: no

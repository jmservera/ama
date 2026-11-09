# Changes: issue 1288 extension E2

Plan: [plan](../plans/2026-11-09-quality-sensor-demo-1288-e2-plan.md) (with amendment A1 from the single critique). Start: E1 head `21763da`, merged with origin/main `1f28d09` as `c772364` (no conflicts, no overlap with E2 paths).

## Source

* F1 `core/ai_consumption.py`: the Deadline/DISPATCH_GATE machinery is replaced by a `CAPTURED_READINGS` context variable and `captured_readings()`.
* F1 `core/ai.py`: `_request` refuses with `DispatchWithdrawn("captured-readings-transmission-unavailable")` first, before data protection, metering, token or socket, whenever the context is set. `bounded_send`, `_gated_opener`, `CHUNK` removed. `may_carry_captured_readings(carrier)` is true only for a non-`Ai` carrier declaring `sends_no_bytes`.
* F1 `core/assistants.py`: tasks with captured sensor readings run the provider inside `captured_readings(...)`. A carrier that may not carry them holds the task with a manual-route reason. `DispatchGate` is described truthfully as a consent re-check, not a physical-send guarantee.
* F1 `api/server.py` and `agents/dispatch.py`: the API composition and the agents worker apply the same policy (A1.1).
* F2 `core/assistants.py`: `_adopt` is pure and returns a slot. The first window is unchanged (newest first, 100 rows). The following scans walk `id > cursor` in id order from a durable cursor kept in the INCOMPLETE schedule row (visible as `incomplete_history`). `_due` persists only when observing.
* F3 `core/assistants.py` and `core/assistant_release.py`: `forecast` runs under `read_only()`, so `invalidate_changed` writes no release rows or events. Forecast no longer persists adoption, slots or markers.
* F4 `core/assistants.py` and `api/web/assistants.js`: review-flag wording is "not in the current bounded capture (they may still be stored)", with a `basis` field. Real deletion is still reported separately.

## Tests and checks

* New `api/tests/test_quality_sensors_e2.py` (30 SQLite plus 30 real-SQL variants): real TLS loopback peer with partial (trickle) reads, a suspended final-check hook with an other-process withdrawal, worker redelivery, API composition, cursor over 120 tasks with restart and a `dispatched` rewrite, forecast purity over the complete schedule/task/event/release/allowance/attempt/gate tables and in-memory state on fresh and legacy stores, and rotation that retains the rows.
* C7 PhysicalSend and E1 Fence/send tests that asserted the old physical-send behaviour were removed or converted (see the review artifact). No old-review regrade.
* `api/checks/quality_sensors_browser_check.py`: absence assertions also require "deleted" to be absent.

## web-design-guidelines refresh (changed web file)

Source `https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md` fetched in full this session. Changed lines: `src/api/src/zava_forward/api/web/assistants.js:23` and `:25` (text strings only). No finding: no interactive element, focus, label, motion, or layout was touched; plain-language wording kept. No redesign. This is an engineering review, not native or assistive-technology acceptance.

## Evidence

All logs are in the coordinator `logs-1288-e2/` directory.

* Reproduction on unchanged source (`reproduction-unchanged-source.txt`): 7 failures and 1 error of 21 new tests (suspension, manual-route text, cursor x2, forecast x3, rotation). The positive control passed.
* API SQLite set (9 modules): 548 tests OK, 216 skipped (the SQL variants) (`api-sqlite.txt`). Agents `test_dispatch`: 15 OK. Core sensor modules: OK.
* Real SQL (owned disposable SQL Server 2022, nonqueued heavy lock, removed afterwards): E2 SQL variants 30 tests OK, 1 skip (the SQLite-only subprocess test); E1, C7, `test_assistants`, `test_quality_sensors`, `test_sensor_sql_check`: 430 OK, 0 skips; core sensor modules: 52 OK, 7 skipped, the SQLite-only store tests.
* Browser and axe 4.10.3 (sha256 matched the pin): 18 checks passed, 0 violations. Incompletes: color-contrast in the unapproved-flag, withheld and unavailable states (not verifiable by axe; same class as earlier). No native or assistive-technology acceptance.
* Ruff: core 2 E501 in `sensor_consumer.py`, identical to baseline; api clean. Two newly unused imports in `ai_consumption.py` were removed. mypy (default config, both sides run): core 61 vs 61, no new; api 810 vs 896: 0 new outside the new test file, 126 new in `test_quality_sensors_e2.py` of the untyped-test class already present in the existing test files (40 resolved by the removed tests). They are not ignored or suppressed.

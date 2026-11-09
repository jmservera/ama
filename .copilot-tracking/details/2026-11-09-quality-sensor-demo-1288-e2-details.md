---
title: Quality sensor demo 1288 E2 details
ms.date: 2026-11-09
---

Written 2026-11-09T10:22Z before any E2 source edit.

## Files and exact changes

* `src/core/src/zava_forward/core/ai_consumption.py`: replace `Deadline`, `DISPATCH_GATE` and `dispatch_gate` with a `CAPTURED_READINGS` context variable and a `captured_readings()` context manager. `DispatchWithdrawn` stays.
* `src/core/src/zava_forward/core/ai.py`: remove `_gated_opener`, `bounded_send`, `CHUNK`, `honours_dispatch_gate`. `_request` raises `DispatchWithdrawn("captured-readings-transmission-unavailable")` as its first statement when `CAPTURED_READINGS` is set, before the data-protection check, the reservation, `_token` and any socket. Add `may_carry_captured_readings(carrier)`: true only when the carrier is not an `Ai` and declares `sends_no_bytes`.
* `src/core/src/zava_forward/core/assistants.py`: `execute` holds a captured-readings task with the explicit manual-route text unless `may_carry_captured_readings(carrier)`; the provider call runs inside `captured_readings()` when captured; non-transmitting carriers still run `DispatchGate` (consent re-check) before the call; `DispatchGate` returns nothing and its docstring states only that it re-checks consent and blocks direct control writes while live, and that it is NOT a physical-send guarantee. Adoption: `_adopt` becomes a pure computation returning a slot tuple plus `_write_slot`; `_due` persists only when `observe`; the incomplete row stores the keyset cursor in `paused_at` (dispatched) and `task_id`; `ORDER BY dispatched DESC, id`; the cursor query is `dispatched<? OR (dispatched=? AND id>?)`. `review_flag` adds `basis` to `cited_comparison` and a docstring that rotation is not deletion.
* `src/api/src/zava_forward/api/server.py`: `fenced` applies `may_carry_captured_readings` when `CAPTURED_READINGS` is set.
* `src/api/src/zava_forward/api/web/assistants.js`: wording "not present in the current bounded capture (they may still be stored)".
* `src/api/checks/quality_sensors_browser_check.py`: replace the "no longer retained" absence assertions with the new wording and add a rotation assertion where cheap.
* Tests: new `src/api/tests/test_quality_sensors_e2.py`; edit `test_quality_sensors_c7.py` and `test_quality_sensors_e1.py` to remove tests that asserted a real captured send (now replaced by S1/S2) and to adapt the F2 trigger test and the adoption tests to the cursor.

## Test mechanics

* TLS peer: a threaded `ssl` server on `127.0.0.1` with a self-signed certificate from the `openssl` CLI (SAN `IP:127.0.0.1`), trusted through `SSL_CERT_FILE` in the test process only. It counts accepted connections and received bytes. A trickling reader (small `SO_RCVBUF`, short reads) proves partial sends in the control.
* Controlled suspension: a hook at the old final-check point (`Meter.dispatch_check` and `Ai._token`) blocks on an event while a separate `python` subprocess commits the withdrawal and expires any gate row through `sqlite3` on `self.dbpath`; the main thread then resumes. On SQL Server the cross-process variant is skipped with an explicit reason; the same-process hold and zero-byte assertions run on both.
* Forecast purity: a helper dumps all `assistant_schedule` rows (every column), `assistant_tasks` and `assistant_events` counts, `incomplete`, `scan_cursor` before and after.

## Success criteria

Each regression fails on the unchanged source and passes after; all selected modules pass with zero unexplained skips on SQLite; the SQL groups pass on a real disposable SQL Server or are reported as blocked; no new ruff or mypy diagnostic after normalization against the baseline captured at `c772364fc` under the same imports and config.

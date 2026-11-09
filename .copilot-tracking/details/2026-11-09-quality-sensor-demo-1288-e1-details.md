---
title: Quality sensor demo 1288 E1 details
ms.date: 2026-11-09
---

Written 2026-11-09T08:52Z before any E1 source edit.

## Files

* `src/core/src/zava_forward/core/ai.py`: `_gated_opener` chunked, bounded sends.
* `src/core/src/zava_forward/core/assistants.py`: `DispatchGate` returns a validity object with `remaining()`; `transport` hook and `sends_no_bytes` policy; `_enqueue`, `_adopt`, `_due`, `_occupy`, `_upgrade` (`seen`), `review_flag`.
* `src/core/src/zava_forward/core/sensor_consumer.py`: `ensure_control_guard` gate-aware triggers; `_replace_controls` diffed.
* `src/api/src/zava_forward/api/server.py`: declare the real `store.ai` transport.
* `src/api/src/zava_forward/api/web/assistants.js`: unknown comparison wording.
* Tests: `src/api/tests/test_quality_sensors_e1.py` (new, SQLite and `ZF_TEST_MSSQL=1`), one browser check file, and mock `Provider` in `test_assistants.py` declares `sends_no_bytes`.
* `src/core/README.md` and the C-cycle documented guarantee text: state the unsupported residual.

## Step details

1. P1: write each S1-S6 test first; run on unchanged source and keep the failing output.
2. P2: trigger body rejects when a row in `assistant_dispatch_gate` has `expires_at` greater than the database clock and `home_id` equals the home in `OLD.body` or `NEW.body` (SQLite `json_extract` and `RAISE(ABORT)`; SQL Server `JSON_VALUE` over `inserted` and `deleted` and `THROW 50002`). The gate table is created if missing by `ensure_control_guard`. Triggers keep names that `sensor_view._guarded` expects and are redefined in place when their stored text lacks the gate check. `_replace_controls` deletes only controls absent from the new set and inserts or updates only changed ones, then rewrites the policy and home index and the marker as now.
3. P3: in each connection `send`, require bytes-like data, split into 16 KiB chunks, call the gate check before each chunk, set the socket timeout to `min(current, remaining)` for that chunk and restore it afterwards. `Assistants._provider_fenced()` is true for a transport that honours the gate or declares `sends_no_bytes`; otherwise a captured-readings task is held before dispatch with the manual-route reason. The API passes `transport=lambda: store.ai`.
4. P4: `_enqueue` skips `_occupy` for a non-proactive `quality-evidence` request. `_adopt` pages `ADOPT_ROWS` rows with `OFFSET` up to `ADOPT_PAGES`; on exhaustion with no match it writes the empty slot; on the cap it writes signature `incomplete-history`. `_due` treats that marker as changed. `assistant_schedule.seen` (`''` default) is added by `_upgrade` and the DDL; `_due` while paused updates `seen`/`at` on a different signature and resumes only after an unchanged full quiet interval; `_occupy` keeps resetting `replaced` only through that path.
5. P5: `review_flag` compares only for current states `ok` and `no-readings`; the UI shows "could not be compared with current readings" for `unknown`.
6. P6: verify `playwright` and `axe` absence in `.venv-1288` and in `node_modules`, install only into an isolated path, reuse the existing API browser harness; assert displayed reading IDs and values equal the captured model snapshot, stale, withheld and unavailable text, attributed unapproved flag, role denial.
7. P7: commands recorded verbatim in the changes artifact.

## Risks

* `seen` and trigger changes touch persistence overlapping #1292; additive, idempotent.
* TLS partial-send bounding is covered by chunk checks, not by a real TLS peer.

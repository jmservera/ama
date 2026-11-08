# Details: #1288 correction 4 (C4)

Written 2026-11-08T21:36Z (real clock), before product or test edits. Refs #1288.

## F1 index proof (`sensor_view.py`, `sensor_consumer.py`, `assistants.py`)

* `sensor_view.home_digest(sensor_ids)`: sha256 of the sorted ids joined by newline; `sensor_view.index_state(pairs)` builds `{count, homes}`.
* `sensor_consumer_index_state (id INT PK, body)`, created beside the other tables and by `ensure_control_home`.
* `configure` writes the marker from the supplied controls in its transaction. `reconcile_control_home` parses every control first (malformed body, missing or invalid home raises `ConsumerError`), then adds/removes index rows and rewrites the marker. `ensure_control_home` deletes the marker when reconcile raises, and `Assistants.migrate` logs and continues.
* `_controls`: marker missing or unreadable, count mismatch, or per-home digest mismatch means incomplete, so consent is not granted. A decline in any loaded control still wins.

## F2/F3 scheduling (`assistants.py`)

* `_serviced(db, cap, c)`: tasks for (cap, case) whose body `release` and `continuity_epoch` equal the current ones, excluding `state='stale'` with `attempts==0`; returns the coarse signatures of those with the maximum `created_at`.
* `_due`: not eligible means false; an exact task already present means true (idempotent enqueue); otherwise true unless the current coarse signature is in `_serviced`. `changed` for `eligible` is "serviced set non-empty and current not in it". `scan` and `forecast` share it.

## F4 dispatch (`assistants.py`)

* `_mark_requested` sets only `manual_requested` for pending, leased or disabled tasks and never edits `dispatch`. `claim` still freezes the trigger per fence.

## F5 wording (`sensor_view.py`)

* `AS_OF_RULE` names: newest readings, at or before the request and within 366 days; context readings, up to four each side within 30 days of the quality record time, never after the request, possibly older than 366 days; later-dated excluded and never fresh; freshness not asserted.

## Files

`sensor_view.py`, `sensor_consumer.py` (small), `assistants.py`, `src/api/tests/test_quality_sensors.py`, `src/core/README.md`. No web source.

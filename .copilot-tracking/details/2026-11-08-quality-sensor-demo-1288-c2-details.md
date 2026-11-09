# Details: #1288 correction 2 (C2)

Written 2026-11-08T20:19Z (header corrected from 20:22Z, which was ahead of the real clock), before product edits. Phase detail for the C2 plan.

## P1 Identity

* `signature(snapshot)`: `digest(snapshot)`; the sensor source and `sensor:`/`source:sensors` citations are part of it.
* `scheduling_signature(snapshot)`: the C1 coarse form (state, anchor, six-hour bucket, classes). Stored in `assistant_tasks.signature`; `scan` and `forecast` compare against it; `_task_id` uses the exact value.
* `eligible(..., known)` unchanged in meaning with scheduling keys.

## P2 Withdrawal

* `_withhold_sensors` (state ok, consent not granted now): `output` becomes the stub for any non-null output; `_scrub_events` stubs `output` and `edited_output` on every event of that task.

## P3 Dispatch

* `claim`: read the earliest 50 `invocation` events; trigger `requested` if any has mode `reactive`, else `proactive`; set `task["dispatch"]`, add to claimed event. `review_flag` reads `task["dispatch"]["trigger"]`.

## P4 Consent

* `sensor_consumer_control_home(home_id key, sensor_id key, PRIMARY KEY(home_id, sensor_id))`; `configure` fills it with the controls; `_schema` backfills once when the table is created.
* `sensor_view.consent`: fetch indexed sensor IDs for the home (bounded 101), PK-load each control, verify home, union named sensors; declined wins; granted only when all granted, all named sensors indexed, and none indexed is missing; any error is unknown.

## P5 Time

* `capture_source(db, home, reference, mssql, now)`: upper bound `observed_at<=as_of`; window lower bound as_of minus 366 days; context bounds reference +/- 30 days, capped at as_of; `future_dated_excluded` boolean from a one-row probe after as_of (bounded to as_of + 1 day). No clock stored.
* `view`: negative age cannot occur; defensive `future` freshness.

## P6 Web

* `index.html:25`: give the account summary an accessible name that contains its visible text.
* ops.js: show the future-excluded note and the bounded-time wording; assistants.js: unchanged unless attribution wording needs it.
* Fetch web-design-guidelines raw before the first web edit; review every changed web file against all rules, terse `file:line` findings.

## Evidence rules

Unique output files per command under `/tmp/c2-*`, individual exits, skip counts, source hashes. No heavy checks until separate admission.

# Plan: #1288 correction 3 (C3)

Written 2026-11-08T20:53Z after the C3 research and before product or test edits. Refs #1288, #107. No closing claim.

## Phases

* [ ] P1 Red tests first (SQLite, `src/api/tests/test_quality_sensors.py` and `src/core/tests/test_sensor_consumer.py`); record failing results in unique `/tmp/c3-red-*.txt` with exit codes.
* [ ] P2 Finding 1: source state from any captured array; projection keyed on citations.
* [ ] P3 Finding 2: stub notes under withdrawal; Finding 6: review writes stored body, refuses verify/accept while withheld.
* [ ] P4 Finding 4: durable `manual_requested`, claim binds it, unknown is requested.
* [ ] P5 Finding 3: shared due-ness helper for scan and forecast.
* [ ] P6 Finding 5: idempotent index reconcile, run at Assistants migrate and via the consumer, count guard on read.
* [ ] P7 Green light suites, ruff, README; web only if the UI needs it (refresh web-design-guidelines source before editing and review, report file:line).
* [ ] P8 Changes artifact, one Review, state, commit (privacy-safe email, Refs #1288, Copilot trailer).

## Red/green test plan

| Test | Red now because | Green means |
| --- | --- | --- |
| Context-only old anchor (anchor over 366 days old) | state is `no-readings`, withdrawal not projected | state `ok` with latest null, context visible when granted, withheld across detail/list/export after withdrawal, snapshot, provider request and UI model share IDs |
| Notes under withdrawal | verification/review/event notes still carry the value and ID | all stubbed in detail/list/export/raw JSON; originals intact; restored when consent returns |
| Reject after withdrawal | stored snapshot/output overwritten with stubs | stored row unchanged apart from review; consent restored shows original; verify/accept refused while withheld |
| Throttle for missing measures, missing record, incomplete checklist | each same-bucket arrival enqueues a task | one task per bucket; a non-sensor change still enqueues; manual invoke still works and is labelled requested; forecast matches; allowance used once |
| Dispatch with over 50 prior events | manual request after event 50 labelled proactive | requested; legacy task without the field is requested; in-flight manual request marks requested |
| Pre-C2 store: controls present, index absent or partial | capture unavailable or a decline missed | migration restores it idempotently, policy and controls byte-identical, repeat is a no-op, stale index fails closed |

## Critique (one, final candidate)

Verdict: proceed with amendments, applied directly.

* Throttle must not suppress existing-task re-enable or non-sensor changes: apply it only when no task exists for the exact capture and the coarse signature is known.
* Do not change the `sensor_view` public signatures used by the #184-touching `sensor_consumer.py`; keep that diff to a reconcile function and call sites.
* Refusing verify/accept while withheld is a tightening consistent with human-review rules; reject stays available.
* Heavy checks stay pending and are labelled so.

No conflict with a confirmed owner decision; no owner-approved contract change is needed.

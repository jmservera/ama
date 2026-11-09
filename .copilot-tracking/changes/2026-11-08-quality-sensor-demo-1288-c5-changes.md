---
title: Quality sensor demo 1288 C5 changes
ms.date: 2026-11-08
---

Recorded 2026-11-08T22:11Z after the C5 plan commit `36b10d353`. Source base `b938ed73`, tree `d011e210`. Light SQLite only; no heavy process, real data, cloud or live model. Mock provider tests are not live AI.

## Finding dispositions

* C5-1 (High) marker versus control body: SQLite guard triggers (three) and an MSSQL trigger (unexercised, PENDING) delete `sensor_consumer_index_state` on any control insert, update or delete. The marker carries `v: 2`; `sensor_view._controls` also requires the guard. `ensure_control_home` and `SensorConsumer._schema` create it; `configure` and reconcile rewrite the marker last. Changed home, older marker and missing guard fail closed until `migrate()`; migration is idempotent and never writes policy or consent.
* C5-2 (High) exact A-B-A: `_enqueue` requeues a never-dispatched stale task whose exact evidence is current (event `requeued`), for scan, forecast (`new_proposals` counts it) and manual invoke, Quality and `assessment-preparation`.
* C5-3 (High) stale-before-claim churn: a queued unrequested proactive task whose coarse schedule is unchanged takes the current capture at claim (event `refreshed`), so no replacement tasks accrue; one dispatch uses the current readings and the allowance.
* C5-4 (High) flag continuity: a returned proactive flag whose only difference is newer same-schedule readings stays `review-suggested` with `newer_readings` and an effect note; the task stays stale and acceptance stays blocked. A new bucket, a manual task or any non-sensor change is `not-current`.
* C5-5 (High) withdrawal race: consent is re-checked in the pre-dispatch transaction and in the dispatch thread right before the provider call; a withdrawal yields `suspended-before-dispatch` and nothing is sent. Residual: a withdrawal after the final check is ordered after dispatch; projections withhold the output.
* C5-6 (High) scale: new `assistant_schedule` (both DDL lists; PK capability, case_id). `_due` reads the slot and tasks by primary key only; `_serviced` is removed. Test with 300 historical tasks asserts no task-table scan.
* C5-7 (Medium) as-of: claim stores `dispatch.as_of`; `build_request` adds `request_as_of`, `freshness` (fresh, stale, unknown), `age_minutes` and a notice to the sensors source; not part of the capture identity or `SYSTEM`. `review_flag` repeats `evidence_as_of`, `freshness`, `age_minutes`.
* C5-8 (Medium) far future: the future probe has no upper bound (one indexed row), so 1 day plus, 2 and 40 day readings report `future_dated_excluded`.

## Tests

* New in `src/api/tests/test_quality_sensors.py`: R1 to R8 (13 tests). Removed superseded C4 `test_arrival_before_claim_replaces_the_stale_task_once...` (semantics intentionally changed to refresh at claim; replaced by the churn test). Adjusted: spy test accepts the lower-only future probe and the guard read; stale-proposal test uses a real later bucket via the clock; `test_assistants` DDL count 5 to 6.

## Evidence (raw exits)

* Red on unchanged source: `/tmp/c5-red-1.txt` exit 1 (ReadModel, 5 failures incl. subtests) and `/tmp/c5-red-2.txt` exit 1 (Http, 7 failures, 2 errors; the started-call withdrawal test already passed and guards preserved behaviour).
* Green: `/tmp/c5-green-final-qs.txt` exit 0 (test_quality_sensors plus test_sensor_consumer, 195 run, 79 skipped MSSQL). Earlier `/tmp/c5-green-qs-1.txt` exit 1 (3 intended C4-semantics changes) and `/tmp/c5-green-qs-2.txt` exit 0 (158 run, 79 skipped); `/tmp/c5-green-readmodel-1.txt` exit 1 (spy test), `-2` exit 0.
* Exit 0: test_assistant_release (54, 4 skipped), test_sensor_consumer (37), test_sensor_ingestion (47), test_sensor_consistency (38), test_iot_stream (36), test_regulatory_chat_api (9); test_assistants `/tmp/c5-green-test_assistants.txt` exit 1 (DDL count), `-2` exit 0 (120, 58 skipped).
* Ruff check and format at line length 100 clean for changed files; `assistants.py` and `test_assistants.py` with `--select F,E9`.

## Source sha256

* assistants.py 24e419cc0575d13401087256b0c5aaf267c5a16b18fe4e6bb86a5a96dcf15ee5
* sensor_view.py 908df1af8a65f4561bcdacb4604d46823cd5f787a94097eafb78fc2efd2e2610
* sensor_consumer.py b918ccfecd9a30ac249fbdb4eb38e293105bc4f30eed4513536fba20569ae632
* test_quality_sensors.py 8fb488f360ab07a9e166d4948ef7c027046e623923b32e4f3ff006cbcb242a0b
* test_assistants.py 837d78baa81b2fe72ed460b9fc760870d2915639d4a8089ccd38e8c5a0fe81ef
* core/README.md d2bb8c32d65cbff1133d2a7b2cefd3772d03b66675829a9b944d4a800b3a2a22

## Pending

Actual SQL Server (trigger DDL, schedule table, plans, MSSQL variants), browser/axe, #184 semantic integration, FULL receipt, release and attestation, live walkthrough. No web file changed.

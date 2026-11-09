---
title: "Research: #184 correction 2 (C1 c80f receiver store initialisation)"
ms.date: 2026-11-08
---

Disposition: executed (bounded, read-only inspection of source at frozen head
`c80f507b`, tree `3f1d0c95`; the independent review is
`review-184-c80f-20261108-functional/functional-findings.json` in session
`f751a4dc`). Written and committed before any C2 source edit.

## Chronology acknowledgement (additive, nothing rewritten)

* The original `ee2f` H2/M1 review, the C1 `c80f` High review and the first SQL
  attempt's four import errors are preserved unchanged.
* The C1 artifacts (`...-184-c1-*`) were created after the C1 implementation and
  validation, not before. They are not prospective and must not be cited as
  such. C2 is the first correction whose Research and Plan precede edits.
* Missing C1 evidence stays a limitation: the final corrected mypy run and the
  individual Bicep and infra exit codes were not captured in a transcript.
  C1's mypy and unit reruns in the later turn did capture exits; the Bicep and
  infra results are re-captured in C2.

## Finding (High, one)

`live_receiver.main` calls `SensorIngestion(open_store(env))` before
`run_window` can refuse a stopped, expired or invalid control. With
`ZF_STORE=mssql`, `open_store` builds the general `MssqlStore`, whose
constructor runs `_create_schema`, `_create_indexes`, migrations, seeding,
metadata and queue set-up. Under the documented minimum receiver grants this
fails or, if overprivileged, mutates unrelated application state.

## Evidence

* `SensorConsumer.__init__` demands `isinstance(store, SqlStore)` but uses only
  `store.assistant_connection()`, `store.dberror` and the `mssql` flag.
  `assistant_connection()` is a bare `_Conn(connection_string(env), token)`;
  `connection_string` raises `SystemExit` on missing settings and makes no
  connection.
* `process()` executes only: SELECT on `sensor_delivery`,
  `sensor_data_quality_exception`, `sensor_reading`, `sensor_consumer_policy`,
  `sensor_consumer_control`, `cases`; `INFORMATION_SCHEMA.COLUMNS` (visible on
  tables the principal can read); INSERT on `sensor_reading`, `sensor_delivery`,
  `sensor_data_quality_exception`. It never calls `_schema` (DDL is in
  `configure`, a trusted setup path).
* `sensor_register` is read by nothing on the receive path, yet C1 documented a
  SELECT grant on it. The exact grant list should drop it.
* `HubReceiver` itself issues no SQL.

## Shared-contract risk

`#1288` (original 7442) is correcting Quality sensor-view logic in
`sensor_consumer.py`. The minimum change here touches only the
`SensorConsumer.__init__` store check and `mssql` flag, not `retained_envelopes`,
`home_consent`, `observed_series` or any retained-reading shape. The unmerged
sibling source is not imported. A textual merge conflict is possible at the
constructor only; to be reported.

## Environment

Shared heavy lock `/tmp/ama-rpi-heavy.lock` was held at inspection by
`flock -n ... /tmp/ama-1288-sql2.sh` (task 1288, container `ama-1288-c1-sql`).
No duplicate SQL job will be queued or spun on; one non-queued attempt is made
after implementation and a failure is reported with the holder.

main `6354b13f` differs from the frozen head's merge base only in
`.github/rubric/scores/latest.json`; no integration is needed for a source
correction.

Planning Readiness: Ready.

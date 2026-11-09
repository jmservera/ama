---
title: Research for #188 live simulator ingestion into the store
ms.date: 2026-11-05
---

* Research disposition: executed (code reading plus PR history). Planning Readiness: Ready.
* Prior delivery (merged, all Refs #188): #587 consistency with backfill, #645 operator handover verifier for SQL stores, #698 local live-versus-backfill demo, #791 re-validation, #847 and #889 demo fixtures and owner run sheet, #1131 status r8. #184 live simulator container merged in #1088 (not deployed). #508 delivered the bounded IoT consumer candidate (#110).
* Gap found: `SensorConsumer._shape` only admitted `sensor-fault-input-v1` (13 fields, uppercase scenario, `calibrated`). The `live-sim-reading-v1` row (16 fields, `sunlight_wm2`, lowercase scenario `live-simulator`, no `calibrated`) was rejected as SCHEMA, so live readings could not land. `iot_stream.decode` already passes any row within preflight bounds, so the gap was in core.
* Idempotence already exists via primary key (sensor_id, reading_id) plus a content-hash delivery reference; `reading_id` is `LIVE-<sensor>-<slot>`, so it is unique per home and slot (one sensor per home in bindings).
* Constraint: `sensor_reading` has no sunlight column and its DDL is checked strictly; adding one is a SQL change and out of scope for the focused tier.
* Unmet after this slice: statistical no-discontinuity check on real live data (needs deployed container, #185 device registration, owner approval); sunlight in the backfill series (the backfill has no sunlight, so a sunlight seam check needs #183 or #186 support).

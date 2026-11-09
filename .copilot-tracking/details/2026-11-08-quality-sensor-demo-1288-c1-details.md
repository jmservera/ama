---
title: Quality sensor demo #1288 correction 1 details
ms.date: 2026-11-08
---

Written 2026-11-08T19:40Z (UTC). Companion to the [c1 plan](../plans/2026-11-08-quality-sensor-demo-1288-c1-plan.md).

## Interface

* `sensor_view.capture_source(db, home_id, reference, mssql=False)`: no clock. Keys: `state`, `readings` (newest 12,
  oldest first), `latest`, `before`/`after` (4 each around the quality-record anchor), `anchor`, `retrofit_context`,
  `provenance` classes, `citation_keys`.
* `sensor_view.signature(sensors)`: state, anchor, six-hour bucket of the latest observation, provenance classes.
* `sensor_view.citations(sensors)`: key `sensor:{sensor_id}:{reading_id}` to the reading.
* `sensor_view.view(db, home_id, reference, now, mssql)`: capture plus freshness from the capture's own latest.
* `sensor_view.consent(db, home_id, sensor_ids)`: primary-key lookups in `sensor_consumer_control`.
* `assistants.signature(snapshot)`: digest used for identity/staleness; other capabilities keep `digest(snapshot)`.
* `assistants.review_flag(task, provenance, current, consent_ok, held)`: status matrix below.

## Provenance classes

| schema_version / scenario | class | label |
| --- | --- | --- |
| `reading-v1` family, `BACKFILL_2Y` or backfill scenarios | `synthetic-modelled-indoor` | Synthetic modelled indoor reading, not calibrated |
| `live-sim-reading-v1`, `live-simulator` | `synthetic-weather-derived` | Synthetic simulator reading derived from outdoor weather, not a calibrated indoor measurement |
| anything else with `source_type=SYNTHETIC` | `synthetic-unclassified` | Synthetic reading of unknown origin, not calibrated |

## Flag matrix

| Condition | status | autonomous |
| --- | --- | --- |
| consent not granted now | `withheld` | no |
| rejected | `rejected` | no |
| accepted by a person | `reviewed` | no |
| stale, suspended, release denied or epoch stale | `not-current` | no |
| requested by a person | `manual-proposal` | no |
| proactive, no sensor citation | `uncited` | no |
| proactive, current, ready, cites captured sensor reading | `review-suggested` | yes, L4 |

## Validation

SQLite unit/API tests; local SQL Server with `ZF_TEST_MSSQL=1` and `ZF_SQL_*` loopback under one holder of
`/tmp/ama-rpi-heavy.lock`; local Chromium; pinned axe-core 4.14.0 on full states; ruff; `node --check`.

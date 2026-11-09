---
title: Issue 1288 plan details
description: Phase details for the retained sensor read model and Quality AI grounding
ms.date: 2026-11-08
---

Plan: [plan](../plans/2026-11-08-quality-sensor-demo-1288-plan.md). Authored 2026-11-08T19:17Z.

## Interface frozen for this increment

`sensor_view.read(db, home_id, reference_iso, now_epoch)` returns:

* `state`: ok, no-readings, consent-withheld, unavailable.
* `unit`: temperature_c "degC", humidity_pct "%RH"; `kind` "indoor-observation"; `provenance` "synthetic" (source_type SYNTHETIC only).
* `latest`: newest reading or null; `window`: sealed `start`, `end` and at most 12 readings; `before`, `after`: at most 4 each relative to `reference`, or null with `absent_reason`.
* Reading: reading_id, sensor_id, home_id, observed_at (UTC Z), temperature_c, humidity_pct, scenario.
* `capture_source(...)` returns the time-invariant subset (window, before, after, reference, state) used by the quality snapshot; `view(...)` adds latest and freshness (fresh at most 15 min, stale otherwise, from now).
* Reads use the existing `sensor_reading`/`sensor_consumer_control` tables by `home_id` with bound `LIMIT`; they never create tables or write.

## Phase 1

Files: core/sensor_view.py, core/store.py (`sensor_view(user, case_id)` with the assistants authorization rule). Done when unit tests cover each state and the bounds.

## Phase 2

Files: api/server.py (route inside the existing "case" kind), web/ops.js (Quality tab panel: table with ids, units, UTC times, freshness text, before/after or explicit absence, synthetic label), web/assistants.js (flag block). Native table semantics, text states, no colour-only status, no motion.

## Phase 3

Files: core/assistants.py. Add `sensors` category to quality-evidence, extend capture (`sensors` argument) and citations `sensor:{reading_id}`, extend eligibility, add `review_flag(task)` in `_view`.

## Phase 4 tests

core/tests/test_sensor_view.py; api/tests/test_quality_sensors.py (SQLite SQL, handler, role and scope denial, bounds, restart and dedupe, captured request correlation with mocked provider, stale after new sealed window, revocation, unavailable); browser/axe check script for the Quality tab.

## Phase 5

core/README.md section; changes and review artifacts.

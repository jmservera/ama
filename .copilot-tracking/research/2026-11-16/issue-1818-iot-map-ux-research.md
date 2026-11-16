---
title: Issue 1818 research - IoT sensor status in employee map and resident sensor view
date: 2026-11-16
task_id: issue-1818
disposition: executed
planning_readiness: Ready
---

## Scope

Surface bounded, permission-projected latest sensor summary in `/api/map` (`insights.map_view`), the employee `mapPanel`, `map-home-card` and `maplist`, and make resident `#sec-sensors` freshness/provenance explicit. Live Azure IoT Hub walkthrough criterion stays unticked.

## Evidence

* `src/core/src/zava_forward/core/insights.py:143` `map_view(cases, f, bbox, zoom, cap=500)` is pure over the in-memory case store. Points mode (<= cap) yields `items` with id, name, address, stage, kind. `store.py:818` wraps it. `server.py:865` serves `/api/map`; the route is open to all STAFF_ROLES (`projection.allowed`).
* Retained readings live only in SQL `sensor_reading` (index `ix_sensor_reading_home_time`, `sensor_consumer.py:635`). `sensor_view.py` already holds the bounded read model (`_select`, `consent`, `CLASSES`, `FRESH_SECONDS=900`, `CALIBRATION`) and requires per-home recorded consent `granted`, else withheld.
* Sensor read access is role-gated by `assistants.REGISTRY["quality-evidence"]["roles"]` (Quality Inspector, Retrofit Programme Manager) via `Assistants.authorize`, which also enforces current staff row, case_ids and area scope. `/api/map` itself does not apply staff scope.
* `Assistants.sql`/`.mssql` flags and `store.assistant_connection()` give SQL access; JSON-only stores have no sensors.
* Resident view: `resident_showcase.showcase_view` builds `sensors={synthetic, note, stale, history, forecast}` (history <= 48 readings, own home only, source_type SYNTHETIC). `resident_demo/web/demo.js:288 renderSensors` already shows a synthetic note, a stale badge, per-reading UK-time stamps and a table. Gaps: no explicit "retained stored history, not live" freshness statement with the latest timestamp age, no explicit provenance/uncalibrated badge text; `stale` uses `resident_forecast.STALE_AFTER`.
* Employee UI: `web/app.js:2457-2760` `mapSymbol`, `MAP_SIGNALS`, `mapPanel`, `showHome`, `renderList`; list item text is `name, signal label`; map-home-card is a `dl` of Case, Current stage, Map status.
* Existing gates: `src/api/checks/map_fullscreen_browser_check.py`, `resident_sensors_browser_check.py`; tests `test_ui_support.py`, `test_sensor_privacy.py` (map payload must stay clean of private packets), `test_role_matrix.py`, `test_ranking_scale.py`.

## Design decisions

* New core module `sensor_map.py`: `summaries(db, home_ids, now, mssql)` runs one bounded grouped query for the newest SYNTHETIC reading per home over at most `SENSOR_HOME_CAP` (100) homes, then applies the existing fail-closed `sensor_view.consent` per home. States: `fresh` (<=15 min), `stale` (<=24 h), `offline` (>24 h), `no-readings`, `consent-withheld`, `unavailable`, `future-dated`; `alert` true for stale/offline. Always `calibrated=False`, `provenance="Synthetic simulator reading. Not calibrated."`. No history leaves the function: only latest temperature, humidity, observed_at, age.
* `insights.map_view(..., sensors=None)`: optional callable `ids -> {id: summary}` invoked only in points mode; homes beyond the cap get state `not-loaded`. Callers without permission or SQL pass a restricted/none provider so items carry `sensor` with state `restricted` or `not-connected` and no values (role projection decided server-side, not in the browser).
* `Store.map_view(f, bbox, zoom, sensors=None)`; server builds the provider from `app.assistants` only for roles in the quality-evidence registry and with `authorize`d scope; other roles get `restricted`.
* Filter: client-side "Sensor alerts or stale" checkbox over loaded points (applies to points mode only; clusters carry no sensor data), plus plain text for each state. Non-colour cues: text badge, symbol, label.
* Resident: extend `sensors` envelope with `freshness` text/state, `latest_at`, `provenance` text and `calibrated=False`; render it as a labelled status block above gauges. Single-home isolation unchanged.

## Risks

* Consent check cost is per home; capped at 100 homes per response.
* Map payload privacy tests must still pass; new keys carry no free text from stores.

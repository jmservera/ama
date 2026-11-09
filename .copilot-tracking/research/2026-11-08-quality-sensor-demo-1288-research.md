---
title: Issue 1288 retained sensor values and Quality AI grounding research
description: Native Research for the bounded visible sensor read model and sensor-grounded quality-evidence capture
ms.date: 2026-11-08
---

## Scope and disposition

Task 1288-quality-sensor-demo, branch feat/quality-sensor-demo-1288, worktree issue-1288-quality-sensor-demo. Source and local only. Research disposition: executed (read-only code inspection started 2026-11-08T19:14Z; this artifact written 2026-11-08T19:17Z before any source edit). Planning Readiness: Ready.

The coordinator reports under `session-state/f751a4dc.../iot-quality-demo-scope` were read as orientation only. Everything below was re-verified in this worktree.

## Base

* Source base: origin/main ecb28815b2f5dd354ba1d34046cf02784b49bdd2 (fetched 2026-11-08T19:13Z, equals HEAD, clean tree).
* Target: main. Independent increment; no parent stack is required. Parent 184 live-envelope admission is not on main and is not consumed.

## Findings

* Retained store: `sensor_consumer.SensorConsumer` owns `sensor_reading` (sensor_id, reading_id, home_id, observed_at, temperature_c, humidity_pct, source_type, scenario, seed, schema_version, injected_fault), written only by `process()` after SYNTHETIC/identity/number/calibration/consent/window admission. `observed_series()` is unbounded unless windows are supplied and reconstructs live witnesses; it is not suitable for a request path.
* Units are fixed by column name (temperature_c in degrees C, humidity_pct in percent relative humidity). Weather references are not in `sensor_reading`; reading only this table keeps indoor observations separate.
* Consent: `sensor_consumer_control` carries per-home consent. `home_consent()` fails closed to unknown. The read path must withhold values unless consent is granted.
* Case to home mapping: the case id is the stock home id (simulator enumerates `cases.id`). Case access follows `Assistants.authorize` (staff row, role, `case_ids`, `areas`) and `projection.allowed`.
* No retained retrofit stage marker exists on readings. The only dated, retained anchor is the active quality record `recorded_at` for a measure. Before/after context can therefore be stated only relative to the earliest active quality evidence record, and must say so; it is not an install date.
* Quality AI: `assistants.capture('quality-evidence')` captures home, measures, quality items, checklists and permitted documents; no sensor source. `snapshot()` already has the SQL connection. Citations are generated per top-level source key; `validate_output` accepts only captured citation keys, so reading-level citations only need to be added to the capture.
* Dedupe hazard: the task id and staleness digest are over the whole snapshot. A snapshot containing newest readings would change every five minutes and create a new proactive task per scan. The sensor source must be sealed to a coarse UTC boundary and bounded in size.
* Release controls: runtime binding hashes RULES, REGISTRY categories and purpose. Changing the quality-evidence rule text and categories invalidates existing quality releases, which is the intended existing control. SYSTEM is shared by five capabilities and stays unchanged.
* UI: employee Quality tab is `qualityPanel` (ops.js) plus `assistantProposal` (assistants.js) in the AI tab; proposals already show output, citations, envelope and provenance. No sensor display exists. API routes are in `server.py`; `get_kind` maps `/api/cases/...` to the existing "case" kind.
* Environment: installed editable distributions pointed at the primary checkout; a /tmp venv with editable installs of core, agents and api from this worktree was created so tests import this source. Tests run from `src/api` with `PYTHONPATH=tests:../core/tests:../agents/tests`. Baseline `test_assistants`: 120 tests OK, 58 skipped (SQL-only variants).

## Decisions

* New pure core module `sensor_view` provides one bounded, permission-gated read model used by both the API and the quality capture, so the UI and the model request carry identical reading ids and values.
* Bounds: at most 12 readings in a window sealed to the last 6 hour UTC boundary, 4 readings before and 4 after the reference, and 1 latest reading with live freshness; indexed `ORDER BY observed_at LIMIT n` queries only.
* States: ok, no-readings, consent-withheld, no-home, unavailable; before/after each ok or explicit absence reason. No zero or fixture substitution; no generation on the read path.
* Proactive: sensor window present for a case with a quality record makes quality-evidence eligible; sealed window plus signature dedupe gives at most one task per case per 6 hours, still under the existing finite allowance, expiry and release admission, default off.
* Flag: derived only from a stored proposal whose envelope source is ai and outcome returned; carries serving model, cited ids and "human review requested"; states it is not acceptance, defect closure, payment, consent, hazard diagnosis or ranking.

## Unknowns and omissions

* Real model, SQL Server, Azure, Hub, simulator, live-envelope schema and release attestation are not exercised. No private data read.
* The 6 hour seal, window sizes and the proactive predicate are exercise values for the demo, not approved operational thresholds.

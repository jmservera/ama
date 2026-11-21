---
title: Issue 2192 research, sensor monitoring consent checkbox
date: 2026-11-21
---

Research disposition: executed (2026-11-21). Planning Readiness: Ready.

## Findings

* Consent is stored as `consent` in each `sensor_consumer_control` row (JSON body, one row per sensor), indexed by `sensor_consumer_control_home` and a verified marker `sensor_consumer_index_state`. A guard trigger drops the marker on any direct write and rejects writes while a dispatch gate is live (`src/core/src/zava_forward/core/sensor_consumer.py`).
* Readers: `sensor_view.consent()` (employee Home sensors view, `consent-withheld` state) and `SensorConsumer.home_consent()`. A decline on any control wins; anything unclear is `unknown`, which withholds.
* The only sanctioned writer is `SensorConsumer.configure`; `telemetry_consent.withdraw` (issue 151) declines a home through it, but nothing grants and nothing is exposed to residents.
* The resident website is `src/api/src/zava_forward/api/resident_demo` (ca-resident-demo). It is read-only: its SQL principal holds SELECT on `[resident_showcase].[v_resident_case]` only. Its view already carries `sensor_home_id` and sensor history.
* Employee view of the withheld state already exists (`ops.js`, `sensor_badges.py`).
* There is no existing audit sink for consent changes in the sensor tables.

## Decision for the demo

Add `SensorConsumer.set_home_consent` (atomic, reuses the dispatch-gate wait and marker rewrite, writes an audit row in the same transaction), a resident-demo port plus `POST /demo/sensor-consent`, and a native checkbox in the sensors card. The writer is opt-in through a separate SQL principal (`ZF_DEMO_SENSOR_CONSENT_*`); without it the card states that consent changes go through the housing officer.

## Limits

Deploying a new image and a new SQL principal to ca-resident-demo is a live Azure change that needs an image build and a database grant; not done in this local-commit task. Live proof is therefore recorded as unproven (see changes record).

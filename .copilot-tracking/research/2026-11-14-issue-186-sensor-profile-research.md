---
title: Issue 186 indoor temperature and RH profile generator research
ms.date: 2026-11-14
---

## Disposition and readiness

* Research disposition: executed. Planning Readiness: Ready.

## Findings

* `src/core/src/zava_forward/core/synthetic/indoor_projection.py` already couples indoor temperature and RH to dwelling type, age band, construction factor, heating pattern and outdoor temperature/RH (`project`, `project_composed`). Noise is a bounded Gaussian (3 sigma cap), so output envelopes are derivable.
* `sensor_backfill.sensor_for` draws a per-home archetype deterministically from `Random(f"{seed}-sensor-{home_id}")`; `outdoor_series` and `readings` are seeded string-keyed `random.Random` streams, so output is a pure function of seed and config.
* `tests/test_indoor_projection.py` covers equations, endpoints, envelopes and invalid input per archetype, but no test exercised a 24-home portfolio end to end.
* No code defect found. The repository has no separate "archetype" generator module; archetype means the dwelling/age/construction/heating tuple.

## Gap

* Missing evidence that all 24 homes are seed-deterministic, bounded by the derived envelope against the shared weather series, archetype/weather sensitive, and reject out-of-domain weather.

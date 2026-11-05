---
title: Plan for #188 live-sim retained round-trip repair
ms.date: 2026-11-05
---

* Add `SensorConsumer.retained_envelopes`: lossless retained wire rows. Live rows return the original 16-field witness unchanged; other managed rows keep the existing exact projection. No field is invented.
* Keep `observed_series` as the comparison projection for the exact backfill contract, now excluding live-sim rows instead of reshaping them, so no `calibrated` value is fabricated.
* `sensor_handover_verify.run` replay uses `retained_envelopes`; its report keeps `observed_series`.
* `analyse_retained` partitions envelopes: live-sim rows are weather-shaped, ineligible for indoor analysis, and are never passed to the comparator. With no indoor rows the signal is INSUFFICIENT with reason `WEATHER_INPUT_NOT_INDOOR`; with indoor rows the analysis uses only those. No hazard, threshold or model change.
* Excluded: schema or version changes, sunlight stripping, calibration invention, schema relaxation, weather-to-indoor modelling, SQL column (slice 2), deployment.
* Critique (executed once inline): compatible findings applied (exclude rather than raise in `observed_series` so the verified backfill report stays usable; explicit reason string); nothing conflicts with confirmed decisions. Verdict: proceed.
* Validation: focused regressions (round-trip, mixed schema, consent, mapping, calibration interval, clock, replay negatives, indoor exclusion) plus ruff and mypy. Tier is FULL for this SQL/provenance-sensitive candidate. The complete gate is pending: the earlier receipt `/tmp/rpi188-full-20261105T0740/receipt.json` failed and is preserved; engineering recovery is dependency-blocked on #1208 (hermetic Chromium ordering) and the heavy lock held by #96. No duplicate gate or partial pass is claimed.
* [ ] Human review required and left unchecked.

---
title: Changes for #188 functional findings F1 and F2
ms.date: 2026-11-06
---

* Planning commit 7dda74df preceded the RED reproduction and every source edit.
* RED (/tmp/188-functional-contract-r16-1106/red-repro.log, i188 module identities printed, read-only gate api venv with explicit i188 PYTHONPATH): F1 `KeyError 'calibrated'` from direct core `report(weather, weather)`; F2 `weather_report passed=True` and `verify` `passed=True idempotent=True` for a relabelled copy. Both findings reproduced.
* `sensor_consistency.py`: `_index` now requires the exact `READING_FIELDS` key set before the shared shape check (weather rows raise ValueError INVALID_HANDOVER_OBSERVATION); `weather_report` refuses equal parsed-integer declared seeds with `HANDOVER_REFERENCE_NOT_DISTINCT` before numeric comparison (so before replay writes in `verify`); docstring states the provenance limitation.
* `test_sensor_consistency.py`: two regressions (equal-seed relabelled copy refused on both paths including `-0`/`0` handling where applicable, retained envelopes unchanged after replay_check; direct core report refuses weather rows). `src/core/README.md`: contract sentence.
* GREEN: repro now raises HANDOVER_REFERENCE_NOT_DISTINCT (green-repro.log, only F2 line shown because it raises first; F1 asserted by the new test); focused 10 tests OK; sensor consistency, live consumer, ingestion, analysis store, consumer and live readings 171 tests OK, 0 skip mentions (green-set.log; final-set.log after docstring edit OK). Ruff check and format pass after one E501 docstring fix; mypy core 128 and API 24 files clean. Maintained mypy used is the shell `mypy`, not the gate venv; checks are source-import checks, not installed-package or FULL acceptance.
* Not run: SQL, Docker, gate, install. Old r14 FULL receipt is historical for 505ad799 and does not cover this head.

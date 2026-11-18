---
title: Issue 187 anomaly injector plan
ms.date: 2026-11-14
---

## Plan

* [x] Add `synthetic/sensor_injector.py`: five named scenarios, `InjectedEvent` manifest, `live_view` leak guard, non-overwriting manifest writer.
* [x] Add `tests/test_sensor_injector.py` covering scenario effects, isolation, leak refusal, bad input, deterministic manifest.
* [x] Run ruff check, ruff format check and focused unittest.

## Critique

One pass: keep the module separate from `sensor_scenarios` so the 11-case inventory and its hashes are unchanged. Accepted.

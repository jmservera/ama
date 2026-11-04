---
title: Issue 190 retained-store scenario plan
ms.date: 2026-11-04
---

* [x] Add `test_retrofit_scenarios_retained_store.py`: ingest the four retrofit scenarios through `SensorConsumer`, read them back with `analyse_retained`, compare with the pure derivation.
* [x] Cover fail-closed paths: declined consent, partial ingest, unmapped home.
* [x] Run the new tests, ruff and mypy; commit; open a PR with Refs #190, Refs #193.

Critique executed once by the implementing agent: keep to constructed exercise data, assert priority effect NONE and no task candidate, reduce ingest volume in fail-closed tests to keep the focused run short, claim nothing beyond the tests.

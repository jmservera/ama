---
title: Issue 2304 round 2 plan (2026-11-24)
ms.date: 2026-11-24
---

# Plan

Tier: FULL (src code changes); the coordinator runs the gate; no rpi-checks --all here. No deploy.

* [x] Phase 1: record the profile and live probes (research note).
* [ ] Phase 2: add `ForecastReads.once` and memoise `release_reference` inside the forecast view.
* [ ] Phase 3: regression test: registry builds do not grow with open cases and the forecast answer is unchanged.
* [ ] Phase 4: run core and api tests sequentially, mypy and ruff; write the evidence note with the per-criterion table.

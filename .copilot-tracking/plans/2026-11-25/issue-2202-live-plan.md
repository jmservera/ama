---
title: Issue 2202 live plan 2026-11-25
ms.date: 2026-11-25
---

Refs #2202. Tier: FULL (src/core change), local gate only through targeted tests, mypy and ruff; no rpi-checks --all.

* [x] Phase 1: re-prove criteria live (done, research note).
* [ ] Phase 2: switch `AssistantService.sensors` and `map_sensors` to `_read_connection()`; add a test that both leave the write lock untouched.
* [ ] Phase 3: run `src/core` and `src/api` targeted tests, mypy, ruff; write note, index and log entries.

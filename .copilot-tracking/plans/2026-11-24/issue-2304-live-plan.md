---
title: Issue 2304 live plan (2026-11-24)
ms.date: 2026-11-24
---

# Plan

* [x] Phase 1: split `Assistants.forecast` into a request wrapper and `_forecast_compute`.
* [x] Phase 2: background job per (identity, period) with `FORECAST_BUDGET_SECONDS` as the job cap, `FORECAST_WAIT_SECONDS` (8 s, counted from request start) as the client wait, and `FORECAST_TTL_SECONDS` (60 s) cache of the last good answer.
* [x] Phase 3: regression tests: a slow computation returns the named state inside the wait and the retry is served from the cache; a fresh cache hit issues no SQL statement; permission errors still propagate.
* [x] Phase 4: live read-only probe before, evidence note, index, log.

Details: `.copilot-tracking/details/2026-11-24/issue-2304-live-details.md`. Tier FULL (src change); no `rpi-checks.py --all`.

---
title: Issue 2312 live details (2026-11-23)
ms.date: 2026-11-23
---

## Phase details

* Result shape: `outcome` (`pass`, `fail`, `not_frozen`), `thresholds` (per-threshold name, limit, observed, pass), `critical_errors` (per defined error: count observed, pass), `cohorts`, `manifest_digest`, `versions`, `note`.
* Thresholds: `min_accuracy` (correct over denominator), `max_critical_misses` (observed critical errors), `min_sample_per_cohort` (smallest cohort size).
* Predictions: mapping case id to `{answer, critical_errors}`; missing case counts as incorrect; unknown case ids or undeclared critical errors are input errors.
* `verify_recorded(manifest, result)` returns `valid` or `invalidated` with reasons.
* No network, clock or randomness.

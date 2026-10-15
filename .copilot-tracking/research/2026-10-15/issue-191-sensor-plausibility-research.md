---
title: Issue 191 sensor plausibility research
ms.date: 2026-10-15
---

Task: add plausibility and statistical range tests for the #183 sensor backfill (parent #190).

Evidence

* `mvp/zavaforward_mvp/sensor_backfill.py` is deterministic, synthetic and tied to scale_fixture homes. Fault profiles: none 70, outlier 12, stuck 6, dropout 12 percent. Dropout drops 2 percent of readings, outliers 0.4 percent, stuck runs 5 days.
* Outdoor climate is a labelled synthetic model; Met Office and Environment Agency data (#178) are not retrieved, so ranges are labelled exercise values.
* CI already runs `unittest discover -s tests` (`.github/workflows/mvp-ci.yml`), so a new test module runs in CI.
* Measured on 150 homes at 6-hourly cadence: dropout missing about 1.96 percent, outlier rate about 0.39 percent, pre-1919 mean RH about 59.3 vs 55.4 for 2003+.

Planning readiness: Ready. Disposition: executed. Open item: swap exercise ranges for #178 climate source.

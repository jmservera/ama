---
title: Issue 190 retained-store scenario research
ms.date: 2026-11-04
---

Research disposition: reused (issue comments, merged PRs #505, #588, #631, #699, #700, #848, #996, #1032 and a fresh code check on main 5e6d5a837).

* Delivered: #191, #192 and #194 closed. #193 criteria 1 and 2 met. #1032 drives the labelled retrofit scenarios through production `derive_signal` (#111) and `AftercareRegister` (#133), but only on in-memory rows.
* Gap recorded by the r6 review: no test passes the scenarios through the real retained SQL path (`SensorConsumer` intake, then `sensor_analysis_store.analyse_retained`).
* Finding: intake rejects scenario homes with `HOME_UNAVAILABLE` unless the home exists in `cases`; the test must add the constructed homes.
* Planning readiness: Ready. Test-only slice in `src/core/tests`; no production, SQL-script, infrastructure or deployment change. Focused tier.

---
title: Issue 111 round 2 details
ms.date: 2026-11-04
---

* `sensor_consumer.py`: `home_consent(home_id)` reads `sensor_consumer_control` bodies for the home.
* `sensor_analysis_store.py`: `analyse_retained` wraps `observed_series` and `home_consent` over `derive_signal`.
* Tests: equality with pure derivation, reproducibility, read-only snapshot, consent matrix, stale/missing, dropped table, unmapped or invalid home.

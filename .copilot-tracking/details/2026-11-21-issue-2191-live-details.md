---
title: Issue 2191 live details (2026-11-21)
ms.date: 2026-11-21
---

* `select_cohort(all_homes, coverage=0.5)`: sort unique ids, take `ceil(n * coverage)` evenly spaced homes, raise `COHORT_INVALID` for empty input or a coverage outside (0, 1].
* `plan()` alternates granted and declined by index so any prefix keeps the mix.
* Skip decision: `random.Random(f"{seed}|{home}|{slot}").random() < rate`, so reruns of a slot are repeatable.
* Tests: `src/api/tests/test_live_control.py`, `src/api/tests/test_live_simulator.py`, `tools/test_demo_consent_mix.py`.

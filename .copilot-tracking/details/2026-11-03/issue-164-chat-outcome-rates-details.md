---
title: Issue 164 chat outcome rates details
ms.date: 2026-11-03
---

* `run_scenario` records per-turn `outcomes` (expected kind, actual kind, ok).
* `outcome_rates` aggregates by expected kind; critical-error rate is critical failures over turns.
* `summarise` adds `rates`; `main` prints rates and consumption (cost Unknown with missing inputs).
* Tests: rates on the golden run, failed-turn counting, empty denominators.

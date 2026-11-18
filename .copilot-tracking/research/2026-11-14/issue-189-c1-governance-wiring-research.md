---
title: C1 research, wire run governance into RunPlan (#189)
ms.date: 2026-11-14
---

Evidence: review `independent-direct-189-controls-2368a2f25.md` found RunGovernance/RunMeter unused by `run_plan.py` (High), unvalidated projected cost and `>=` cap boundary (High), halt reason lost after deadline (Medium), docs/tests (Low).

* `RunPlan` is a frozen dataclass serialised with `asdict` into the estimate digest, so governance is carried as primitive string fields, not a RunGovernance object.
* `RunController` already owns `clock` and `stop()`, so a `RunMeter` fits at `start()`.
* Costs are caller-declared GBP planning figures, no billing call.

Planning Readiness: Ready. Research disposition: executed.

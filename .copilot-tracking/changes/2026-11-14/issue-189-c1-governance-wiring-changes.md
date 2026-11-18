---
title: C1 changes, wire run governance into RunPlan (#189)
ms.date: 2026-11-14
---

* `run_governance.py`: validation of projected and admit costs, `>=` cap halt, `halt_reason` preserving RUN_DEADLINE.
* `run_plan.py`: governance fields, `RunController.admit`, CLI flags.
* `tests/test_simulator_run_budget_controls.py`: new regression tests; `src/core/README.md` documented.

Validation (focused tier): core mypy clean, ruff check and format clean, 15 + 27 targeted tests OK. Not run: `rpi-checks.py --all`, hosted CI.

---
title: Issue 189 changes - placeholder guard
ms.date: 2026-11-04
---

* src/core/src/zava_forward/core/synthetic/sensor_stream.py: `accountable_text`, used by RunBudget.validate.
* src/core/src/zava_forward/core/synthetic/run_plan.py: RunPlan.validate uses it.
* src/core/tests/test_run_plan.py, test_sensor_stream.py: new refusal cases.
* src/core/README.md: one sentence.

Validation run: run_plan (27 OK), sensor_stream, api test_iot* (48 OK), ruff check/format, mypy --cache-dir=/tmp/mypy-189 (clean). Not run: gate, benchmarks, full suites, what-if.

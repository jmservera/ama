---
title: Issue 82 gates changes
date: 2026-11-04
---

* src/core/src/zava_forward/core/gates.py: evidence rule and `evidence_gate`.
* src/core/src/zava_forward/core/store.py: evidence gate wired into booking gates.
* src/core/tests/test_gates.py: behavioural tests.

Validation run: test_gates, test_resident_decisions, test_hazard_referral, test_quality_procurement, ruff, mypy on gates.py (cache /tmp/mypy-82). Not run: gate, benchmarks, full suites, full mypy.

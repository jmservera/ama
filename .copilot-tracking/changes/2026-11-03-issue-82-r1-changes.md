---
title: Issue 82 round 1 changes
ms.date: 2026-11-03
---

* Added `src/core/src/zava_forward/core/gates.py` and `src/core/tests/test_gates.py`.
* Changed `src/core/src/zava_forward/core/workflows.py` (accountable-role check on release).
* Added `test_release_needs_the_named_accountable_role` to `src/core/tests/test_hazard_referral.py`.
* Changed `src/api/tests/test_workflows.py`: a manager who is not the accountable role is now refused.

Divergence: none from plan. Behaviour change: managers can no longer release a hold accountable to the Building Safety Liaison.

Validation run: unittest test_gates, test_hazard_referral, test_handoff_lifecycle (core, 56 OK) and api test_workflows (19 OK); ruff check and format on changed files; mypy on gates.py and workflows.py.
Not run: complete local gate, benchmarks, full suites, browser checks.

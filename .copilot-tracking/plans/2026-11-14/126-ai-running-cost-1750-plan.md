---
title: Issue 126 AI running-cost line plan
ms.date: 2026-11-14
---

* [x] Add `named_denominator`, `total_cost_of_ai`, `accepted_outcome_count`, `cost_per_accepted_outcome` to the register line; `Unknown` unless a price source, recorded total and accepted count above zero exist.
* [x] Snapshot the line onto every phase/tranche release decision beside the economics report reference and limit breach.
* [x] Focused tests in `src/core/tests/test_governance.py`; run targeted tests, ruff and mypy only.

Critique (single pass, self): compatible; no conflict with confirmed decisions. Divergence: none.

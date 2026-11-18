---
title: Issue 216 citation and card gates changes
ms.date: 2026-11-14
---

* Added `src/agents/src/zava_forward/agents/citation_card_gates.py` (gates, owners, adversarial prompts, comparator).
* Added `src/agents/tests/test_regulatory_citation_card_gates.py` (7 tests).

Validation: new tests and `test_regulatory_*` (33) pass; mypy, ruff check and ruff format clean in `src/agents`. Full tier and hosted CI not run or observed. Structural benchmark only, not a staff trial; thresholds provisional, not owner-agreed.

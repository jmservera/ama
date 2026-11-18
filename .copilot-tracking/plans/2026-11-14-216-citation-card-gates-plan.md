---
title: Issue 216 citation and card gates plan
ms.date: 2026-11-14
---

Critique: executed once; compatible findings applied (no new spend or model calls; thresholds stay provisional; ship mode defaults to cards_only).

* Add `src/agents/src/zava_forward/agents/citation_card_gates.py`: named gate owners and thresholds, graded and adversarial sets (fixture cases plus unsupported-claim prompts run through the refusal policy), and a paired comparator measuring grounding and completeness of chat against deterministic cards with links.
* `ship_mode` is `cards_only` unless lift is positive with no regression, there are paired cases and every gate is met.
* Add `src/agents/tests/test_regulatory_citation_card_gates.py`.
* Validate with the focused tier: targeted tests, mypy and ruff in `src/agents` with /tmp caches.

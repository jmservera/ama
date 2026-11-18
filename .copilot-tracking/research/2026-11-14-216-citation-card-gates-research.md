---
title: Issue 216 citation and card gates research
ms.date: 2026-11-14
---

Disposition: executed. Issue #216 has two unticked criteria: owned citation validity and refusal gates on a graded and adversarial set, and a paired chat-versus-cards report that ships cards alone without measured value.

Evidence: `src/agents/src/zava_forward/agents/regulatory_gates.py` already grades answers (`evaluate_answers`, `check`) with provisional thresholds and an unconditional `cards_only` comparison; `regulatory_eval.py` holds the card baseline; `evals/regulatory_gates_cases.json` holds 24 cases including injection, obfuscation and extraction prompts. Gap: no per-set gate with named owners, and no measured comparator that can decide ship mode. Thresholds remain provisional, not owner-agreed.

Planning Readiness: Ready.

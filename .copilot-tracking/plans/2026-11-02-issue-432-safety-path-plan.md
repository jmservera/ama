---
title: "Plan: #432 safety path slice"
ms.date: 2026-11-02
---

* [x] 1. Add `src/core/tests/test_ai_consumption_safety.py` (import-graph test and stop-then-hazard test).
* [x] 2. Update criteria table in `docs/reference/resources/ai-tokenomics.md`, core README command and `docs/reference/log.md`.
* [x] 3. Focused validation: consumption tests, ruff, mypy on the new test.
* [x] 4. Review, commit, push, PR with `Refs #432`.

## Critique (single pass)

Risk: overclaiming statutory-clock proof. Disposition: wording limits the claim to hazard recording and awareness time; live clock behaviour is stated as unobserved. Applied directly.

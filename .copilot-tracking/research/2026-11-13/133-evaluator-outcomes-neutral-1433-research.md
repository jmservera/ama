---
title: Issue 133 evaluator outcomes column and neutral text guard research
ms.date: 2026-11-13
---

## Scope

Refs #133, #89. Two local gaps from the 133-aftercare-ac-audit-1416 audit. Research disposition: executed (code read only).

## Findings

* `AftercareService.evaluator_view` (`src/core/src/zava_forward/core/aftercare_intake.py:739`) gives each row a `concerns` list whose items carry `outcome` (`no_outcome_yet` or a recorded outcome key). Row-level `outcomes` does not exist; the per-concern values are the evidence, so no API change is needed.
* `aftercareEvaluatorView` (`src/api/src/zava_forward/api/web/aftercare.js`) renders six columns and omits outcomes. `AFTERCARE_LABELS` already maps `no_outcome_yet`, `advice_given`, `remedy_needed`, `cannot_determine` and others to plain text.
* `neutral_text` (`src/core/src/zava_forward/core/aftercare.py`) rejects a literal substring list only; paraphrases such as "you'll save" pass. It also guards sensor context and generated pack text, so new patterns must not reject neutral factual text (higher bills reported, cannot determine).
* `test_aftercare_screen.py` asserts six table columns; this changes to seven. `aftercare_browser_check.py` is not touched.

## Planning readiness

Ready.

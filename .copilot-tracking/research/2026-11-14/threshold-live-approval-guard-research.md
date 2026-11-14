---
title: Issue 146 live threshold approval research
ms.date: 2026-11-14
---

Refs #146. Research disposition: executed. Planning Readiness: Ready.

* Thresholds live in `cohort_eval.py` (`thresholds` plus `approval` block), not in `rai_metrics.py` (counts only, no thresholds).
* Gap 1: `evaluate()` had one mode; a manifest with `synthetic: true` and approval returned `activation_allowed` true. Owners were checked by `named()`, which accepts "system" or "agent". No expiry.
* Gap 2: `rai_release.missing_binding(live=True)` rejected `constructed-fixture` evidence class but not blank-equivalent or system/agent approver attribution.
* Existing tests (`test_cohort_eval`, `test_rai_release*`) rely on offline default behaviour, so changes must be opt-in via `live=True`.
* Decision: add `named_human`, `evaluate(live, now)`, live approver check; pure, no clock access.

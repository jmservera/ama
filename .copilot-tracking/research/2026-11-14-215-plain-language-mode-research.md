---
title: Issue 215 plain-language mode announcement research
description: Evidence for the 2026-11-14 #215 UX slice
---

## Scope and evidence

* Issue #215 criteria 3 (WCAG 2.2 AA, plain-language mode) and 5 (staff comprehension) are unticked.
* Already delivered: glyph and border cues, Escape closing the lookup disclosure with focus on the summary, widget Escape and focus return, polite log regions, role guidance (`test_regulatory_a11y_cues.py`, `test_alert_chat_role_wcag_plain_matrix.py`).
* Gaps found in `src/api/src/zava_forward/api/web/chat.js`: the plain-language checkbox changed content silently (WCAG 4.1.3); always-visible copy used technical phrases ("Inference is disabled", "Active bounded control", "Audit records only") against `docs/reference/research/ux/content-standard.md`.
* Constraint: `test_accessibility_baseline.py` inventories `aria-invalid`; no new site may be added.
* Planning readiness: Ready. Disposition: executed.

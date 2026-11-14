---
title: Review - #215 non-colour, keyboard and plain-language matrix
description: Single post-implementation review
ms.date: 2026-11-14
ms.topic: reference
---

Execution: executed once by the implementing agent (not independent; independent exact-head review and human approval remain required). Outcome: conformant for the stated test-only scope; no open material findings.

## Findings routed to later work

* The widget error element pairs `role="alert"` with explicit `aria-live="polite"`. Left unchanged because existing focus and browser checks assert both. Follow-up: choose one semantics, update `test_chat_widget_focus.py` and `test_chat_panel.py`, and if a check script changes, the `scenario-manifest.json` recipe SHA.
* Suppliers reach only the fallback guidance line; a supplier-specific line needs an owner content decision.
* Screen reader, keyboard walk-through and staff comprehension remain manual evidence; the #215 criterion stays unticked.

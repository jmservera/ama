---
title: Chat input guardrail a11y changes (Refs #215)
date: 2026-11-14
---

* Added `src/api/tests/test_alert_chat_input_label_pii_notice_a11y.py` (8 tests).
* Validation: 22 tests OK (new plus `test_accessibility_baseline`), ruff check, ruff format, mypy pass.
* Not run: browser harness, hosted CI, full gate. No source or `aria-invalid` change.

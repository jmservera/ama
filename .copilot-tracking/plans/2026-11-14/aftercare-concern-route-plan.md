---
title: Aftercare concern route plan (#133)
date: 2026-11-14
---

* [x] Add `strip_unsafe_sentences` and `assert_templates_neutral` to `aftercare.py`; run it at import on fixed templates.
* [x] Guard intake `manual_route`, `owner_note` and fixed notes in `aftercare_intake.py`.
* [x] Add focused tests in `test_aftercare.py` (strip, nested template guard, all fixed templates, every channel with representative recorded).
* [x] Run targeted tests, `ruff check`, `mypy`. No `unittest discover`.

Critique: executed once; compatible, no conflict with confirmed decisions.

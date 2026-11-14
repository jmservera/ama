---
title: Aftercare concern route changes (#133)
date: 2026-11-14
---

* `src/core/src/zava_forward/core/aftercare.py`: `strip_unsafe_sentences`, `assert_templates_neutral`, import-time template check.
* `src/core/src/zava_forward/core/aftercare_intake.py`: import-time guard on fixed notes and labels; `manual_route` and `owner_note` pass `neutral_text`.
* `src/core/tests/test_aftercare.py`: `TemplateGuardTests` (4 tests).

Validation: `tests.test_aftercare`, `tests.test_aftercare_intake`, `tests.test_aftercare_store` ran with sources from this worktree on PYTHONPATH (the installed package points at another checkout); the only failure was a test typo, since fixed, and `tests.test_aftercare` passes (35 tests). `ruff check` and `mypy` clean. The intake/store suites passed in the earlier run apart from that typo.

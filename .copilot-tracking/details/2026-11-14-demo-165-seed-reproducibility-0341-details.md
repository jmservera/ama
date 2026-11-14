---
title: Epic 165 seed reproducibility details
ms.date: 2026-11-14
---

## Phase 1: Add test

* Create `src/core/tests/test_epic165_deterministic_reproducibility.py` only.
* Cases: byte identity of stock register, scale fixture (homes, households, case events) and sensor readings; seed sensitivity; record identity; provenance markers; no postcode (other than reserved TE), UPRN (12 digits), email, phone or NI pattern.
* Validation: unittest, ruff check and format, mypy from `src/core`.

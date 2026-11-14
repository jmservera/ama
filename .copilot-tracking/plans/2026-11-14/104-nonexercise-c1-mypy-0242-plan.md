---
title: C1 mypy correction Plan
ms.date: 2026-11-14
---

Remove the `test_ai_consumption` import; define a typed `Port` and constants locally in the api test. Validate with api `mypy`, ruff check/format and the targeted unittest. Critique: one pass, no conflicting findings. Details: see the details file.

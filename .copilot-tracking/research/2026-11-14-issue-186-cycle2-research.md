---
title: Issue 186 cycle 2 research
ms.date: 2026-11-14
---

* Finding: mypy reported two no-untyped-def errors at src/core/tests/test_indoor_projection.py:316 (PortfolioProfileTests.rows had no return or outdoor annotation).
* Typing the signature exposed three arg-type errors on float(row[...]) because row values are object.

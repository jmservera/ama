---
title: Issue 949 plan
ms.date: 2026-11-04
---

* [ ] Phase 1: derive the version in the test helper (details: `.copilot-tracking/details/2026-11-04/issue-949-details.md`).
* [ ] Phase 2: focused tests, ruff, mypy strict.
* Critique (one pass, direct): compatible. Keep the version-pin test explicit so it still proves binding to an older version. Assert the stored version so a contract change fails the test.

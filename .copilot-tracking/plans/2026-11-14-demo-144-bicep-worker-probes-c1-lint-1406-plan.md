---
title: Plan: C1 ruff correction
ms.date: 2026-11-14
---

* Re-run CI-parity ruff check and format on the target file.
* Apply fixes only if they fail; none needed.
* Verify ruff, `az bicep build`, and `unittest discover -s infra/tests`.
* Record changes and review, commit locally, do not push.

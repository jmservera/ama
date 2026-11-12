---
title: Issue 153 restore type ignore research
ms.date: 2026-11-12
task_id: 153-restore-ignore-1112
---

Hosted src-api Type check on a76417e8d failed at tests/test_case_journey.py:560 [no-untyped-call]. Diagnosis (raw: native files/153-hosted-mypy-diagnostic-1112/): canonical mypy (236 files) reproduces; the earlier narrow three-file run passed only because server is skipped as an import there, so the ignore looked unused. Original line in 4e47be813 carried `# type: ignore[no-untyped-call]`. Owner approved one bounded correction: restore it only.

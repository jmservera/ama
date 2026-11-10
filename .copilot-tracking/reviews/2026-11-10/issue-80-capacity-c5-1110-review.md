---
title: Issue 80 capacity C5 review
description: One native review of the C5 test stub alignment (not independent)
ms.date: 2026-11-10
---

## Outcome

Native author review, not independent. Outcome: conformant with open limits.

* Scope: one test-only hunk in `src/api/tests/test_case_journey.py`; the stub now mirrors production `show` (`app.js`), which already filters null children. No app, checker, ops.js or assertion change; no fallback added.
* Evidence: failing test and whole journey module (31) pass; API 11 and static 60 pass; Ruff check/format pass after fixing one E501 introduced by the first edit (adverse log preserved); Node syntax on unchanged ops.js passes.
* Limits: no browser run; whole-run PASS carried from C4 validation on `2cc34027` because no served file changed. Other `show` stubs in the test file were not changed and passed. Ruff-only lint scope; type checking not run (no type config applies to this test file was verified). Independent exact-head assessment, C2/C4/#73 and owner thresholds remain open. The whole every-list criterion is NOT proven. No C6.

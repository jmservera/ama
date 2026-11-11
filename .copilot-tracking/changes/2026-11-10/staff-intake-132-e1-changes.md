---
title: Staff intake 132 extension E1 changes
ms.date: 2026-11-10
---

Extension E1 of five. Refs #132. Implement complete after the implement-start marker (seq 4).

* Merge `173cd9ff7` of origin/main `6d4cd624` (done before the chain, recorded in Research).
* `src/api/tests/test_staff_intake_api.py`: `correction()` returns `dict[str, Any]` (wrapped by `ruff format` to meet E501); `view()` returns a typed `result: dict[str, Any]`. No other source change.

Validation (raw logs under /tmp, own venv `/tmp/zf132-e1-venv`):

* Red: `/tmp/zf132-e1-mypy-red.log`, two introduced errors.
* Green: `cd src/api && mypy` exit 0, 228 files (`/tmp/zf132-e1-mypy-green.log`).
* `ruff format --check` and `ruff check` on the file pass; `ruff check` over core and api passes.
* Unit: `test_staff_intake_api test_role_endpoint_inventory test_content_standard`, 132 tests OK, 34 skipped (`/tmp/zf132-e1-unit.log`). Skips are the env-gated MSSQL class and JSON-store SQL-contract tests; they are unobserved, not passes.
* Not re-run, unobserved: MSSQL, browser/axe, live acceptance. Behaviour is unchanged (annotation-only).

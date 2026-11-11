---
title: Staff intake 132 extension E1 details
ms.date: 2026-11-10
---

## Phase 2 details

* `correction(self, record: int, label: str = LOFT[0], note: str = "Corrected") -> dict[str, Any]`: parameterise only.
* `view`: keep the `assertEqual(code, 200, out)` check, then `result: dict[str, Any] = out` and `return result`. This narrows the Any from the untyped JSON helper at the single boundary and adds no cast import or ignore comment.
* No other line changes. `ruff format` must leave the file unchanged.

## Phase 3 commands (from `src/api`, own venv `/tmp/zf132-e1-venv`)

* `mypy` (project command, no flags)
* `ruff format --check tests/test_staff_intake_api.py` and `ruff check tests/test_staff_intake_api.py`
* `cd tests && PYTHONPATH=../../core/tests:../../agents/tests python -m unittest test_staff_intake_api test_role_endpoint_inventory`
* Env-gated MSSQL and browser cases are reported as skipped or unobserved, never counted as pass.

## Evidence

Raw logs under `/tmp/zf132-e1-*.log`, copied to the coordinator root with the handoff.

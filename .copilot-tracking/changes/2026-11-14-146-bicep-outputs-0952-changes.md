---
title: Changes - 146 bicep outputs wiring tests (Cycle 1 fix)
ms.date: 2026-11-14
---

## Cycle 1 fix (Refs #146)

* Removed tracked bytecode `infra/tests/__pycache__/test_bicep_monitoring_outputs_wiring.cpython-312.pyc` (`git rm --cached`) and deleted the untracked `infra/tests/__pycache__` directory, resolving the blocking finding in `independent-review-146-outputs-9aa7add18-0959.md` (file not present in the workspace).
* Validation: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest infra/tests/test_bicep_monitoring_outputs_wiring.py -v` ran 7 tests, OK; `ruff check` and `ruff format --check` passed.

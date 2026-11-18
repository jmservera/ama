---
title: Issue 221 restart authority and NFR-014 drill changes
ms.date: 2026-11-14
---

* `src/core/src/zava_forward/core/governance.py`: breach records carry `restart_rule` and `automatic_restart`; restart refuses automatic requests and authority mismatch.
* `src/core/src/zava_forward/core/continuity.py`: suspension records carry the same fields; `restart_decide` refuses automatic requests.
* Tests: `test_governance.py` (breach authority), `test_operator_suspension.py` (RULE-024 fields, NFR-014 drill).
* Validation: `test_governance` 73 OK; `test_operator_suspension` 19 OK; ruff clean on changed files; mypy clean on both core modules. Hosted CI not run; no push.

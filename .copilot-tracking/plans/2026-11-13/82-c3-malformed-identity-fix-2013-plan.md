---
title: 82-c3 malformed identity fix plan
ms.date: 2026-11-13
---

Details: [details](../../details/2026-11-13/82-c3-malformed-identity-fix-2013-details.md). Research: [research](../../research/2026-11-13/82-c3-malformed-identity-fix-2013-research.md).

* [x] Phase 1: failing-first tests (test_grant_lifecycle_controls, test_gates, test_finance_signoffs)
* [x] Phase 2: finance.py type-safe `_norm` and identity validation in `_independent`
* [x] Phase 3: grants.py `_complete` requires `oid` None or str, explicit malformed reason
* [x] Phase 4: gates.py boundary hardening (non-string items, blank/non-string reasons)
* [x] Phase 5: focused validation (tests, ruff, mypy), venv cleanup, commit

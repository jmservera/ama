---
title: Issue 82 C2 plan
ms.date: 2026-11-13
---

* Add string-guarded `_norm` in grants.py (replace finance import use).
* Add malformed-identity test in test_grant_lifecycle_controls.py driving `grant_eligibility_verdict` with code=123, oid=456, email=["bad"].
* Run test_gates*, test_grant*, test_finance* (core, api), ruff, mypy.

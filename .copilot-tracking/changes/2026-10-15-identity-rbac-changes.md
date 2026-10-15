---
title: Identity and RBAC changes (#141)
---

Added infra/role-assignments.json, infra/entra/app-registration.json, infra/tests/test_identity_rbac.py; edited infra/README.md, docs/reference/README.md, docs/reference/log.md. No Bicep change was needed. Validation: infra tests and mvp tests.

## Review-fix round (PR 277)

* Test parses Bicep role assignments into (identity, role, scope) tuples and compares them with the matrix, including token-maintenance rows.
* Owner wording corrected in app-registration.json and README; criterion 4 stated as manual steps plus owner.
* db_ddladmin kept and listed as a tracked open item; criterion 5 B2B decision (#116) stays open.

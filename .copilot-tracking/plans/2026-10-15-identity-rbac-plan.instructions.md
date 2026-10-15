---
title: Identity and RBAC plan (#141)
---

* [x] Matrix JSON from Bicep (role-assignments.json)
* [x] Declarative Entra manifest with owners and contractor decision status
* [x] Tests: matrix vs Bicep, no broad roles, no shared keys/SQL logins/connection strings, manifest vs script vs DEFAULT_ROLE_MAP
* [x] README section, index row, log entry
* Critique: executed once; compatible findings applied (allow-list App Insights string, record open items).

## Review-fix round

* [x] Tuple-level matrix test
* [x] Owner wording
* [x] Criterion 4 statement
* [x] db_ddladmin and B2B open items in PR body

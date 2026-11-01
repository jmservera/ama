---
title: "Issue 141 research: identity, RBAC and Entra registration as code"
ms.date: 2026-11-01
---

* Disposition: executed (repo evidence review). Planning Readiness: Ready.
* Criteria 1-4 are already delivered: `infra/role-assignments.json` (matrix, SQL grants, custom roles), `infra/entra/app-registration.json` (declarative registration, owners, manual steps), `infra/tests/test_identity_rbac.py` (Bicep-vs-matrix tuple equality, no broad roles, no shared keys/SQL logins/connection strings, manifest-vs-script parity). IoT Hub rows exist (Event Hubs receiver for api only). The chat store (ADR 0004) has no Bicep resource yet; README states the rule for when it lands.
* Baseline: 10 of 11 identity tests pass; the parity test needs the `src/api` package installed (environment, not a defect).
* Criterion 5 gap: the contractor B2B guest model is only a free-text `contractorIdentity` block (status "Proposed ... open (#116)"). Nothing machine-checks that the design is consistent: Contractor is the only guest-assignable role, the roster initializers reject guests (`userType == Member` in `setup-entra.py`, `staff_roster.py`, `grant-application-admin.py`), `appRoleAssignmentRequired` is true, and Contractor holds no capability role.
* The owner decision on the B2B model (ADR 0002 open items, OD-14/OD-19, #116 last criterion) is not evidenced, so criterion 5 can only be reflected as a proposal with explicit owner and tests, not closed.
* Follow-ups: (1) owner/tenant-admin confirmation of B2B guests and access reviews; (2) live `az role assignment list` comparison; (3) drop `db_ddladmin` from api; (4) chat-store role row when ADR 0004 resource is added.

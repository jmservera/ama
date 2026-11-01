---
title: "Issue 141 changes: contractor guest design machine-checked"
ms.date: 2026-11-01
---

* `infra/entra/app-registration.json`: structured `contractorIdentity` (`guestAssignableRoles`, `memberOnlyInitializers`, `decisionOwner`); status stays open.
* `infra/tests/test_identity_rbac.py`: `test_contractor_guest_design_is_enforced_by_code`.
* `infra/README.md`: open item now describes the recorded design and checks.
* Validation: `test_identity_rbac` and `test_setup_entra` 136 passed (venv with src/core, agents, api installed via pip). `ruff check` reports 11 pre-existing findings in the test file, none from this change; the file is outside CI's lint set. mypy not configured for infra tests.
* No divergence from plan.
* Review thread fix: the same test now pins the exact `memberOnlyInitializers` list before iterating, so deleting an entry or emptying the list fails.

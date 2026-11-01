---
title: "Issue 141 plan: make the contractor B2B guest design machine-checked"
ms.date: 2026-11-01
---

* Scope: criterion 5 only; criteria 1-4 stay proven by existing tests.
* Step 1: replace the free-text `contractorIdentity` in `infra/entra/app-registration.json` with structured fields (`guestAssignableRoles`, `memberOnlyInitializers`, `blockedWithoutAssignment`, `decisionOwner`, `status`).
* Step 2: add tests in `infra/tests/test_identity_rbac.py` asserting: guest-assignable roles are exactly Contractor; Contractor is not a capability role; `appRoleAssignmentRequired` is true in manifest and script; each listed initializer script rejects non-Member users; status stays open until the owner confirms.
* Step 3: document the design in `infra/README.md` (identity section) with the open owner decision; append nothing to the knowledge-base log (no `docs/reference/` change).
* Validation: identity tests, ruff check/format on touched test file, mypy not applicable to infra tests (no project config; verify).
* Critique (single pass, self-applied): risk of claiming closure; mitigation is PR uses "Refs #141" naming criterion 5 unmet. No conflicting decisions.

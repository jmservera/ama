# Issue 462 correction cycle 3: research and plan (2026-10-26T15:08Z)

Written before the edit. Full gate on head 2e4fe98a (failed receipt SHA 9445db16...20ea, historical) failed in
`0121-infra.log`: `test_identity_rbac.RoleMatrixTests.test_bicep_assignments_equal_matrix_tuples` raised
`AttributeError` at `test_identity_rbac.py:52`. `parse_bicep_assignments` scans every non-main Bicep file, and
the new standalone `infra/resident-demo.bicep` has three assignments whose shape the parser does not model:
two use `roleDefinitionId: secretsUserRole` (a variable holding a `subscriptionResourceId(...)` call), and the
principal, scope and module mapping have no entry for the standalone file. The coordinator read the same
traceback and template.

Second finding from reading the matrix: `resident-demo.bicep` line 62 uses GUID `4633458b-...-0151c3af1c1b`
for Key Vault Secrets User, but the matrix (and Azure) built-in id is `4633458b-17de-408a-b874-0445c86b69e6`.
The template GUID matches no built-in role in the matrix, so the deployment would have referenced a role
definition that does not exist. The resident test at `test_resident_demo_deploy.py:114` pinned the wrong value.
This is a directly coupled defect that the matrix check exists to catch; correcting it is not scope growth.

Plan:

* Template: replace the wrong GUID with the matrix Secrets User id. No new role, no broader scope.
* Matrix: add three rows with `bicep: resident-demo.bicep`: identity `resident-demo`, Secrets User scoped to
  the verifier secret only, Secrets User scoped to the session-key secret only, AcrPull on the registry. Scope
  strings `Secret resident-demo-password-verifier only`, `Secret resident-demo-session-key only`, `Container registry`.
* Parser: resolve a role from either an inline `roleDefinitions` call or a `var` holding
  `subscriptionResourceId(..., 'GUID')`; add a standalone mapping for `resident-demo.bicep` (identity
  `resident-demo`, scopes verifier, sessionKey, registry). A missing mapping raises a clear assertion, so an
  unknown assignment in any new file still fails rather than being skipped. Existing full-equality and
  broad-role prohibitions are unchanged.
* Resident test: update the pinned GUID to the correct one and assert it is in the matrix built-in roles.
* Not changed: gate selectors, other templates, scope, roles, the failing test itself.

Validate: reproduce the failure first; then identity/RBAC plus resident deploy tests together; ruff
format/check as the infra project does; the full infra suite (443 tests). No Docker, no Azure.

## Critique (pending, filled before edits)

Critique (2026-10-26T15:12Z, one independent rubber-duck pass): no blocking or non-blocking issues. It confirmed
Key Vault Secrets User `4633458b-17de-408a-b874-0445c86b69e6` and AcrPull `7f951dda-...-172d538d`, that the
template GUID is wrong, and that no other tests or docs depend on assignment counts. Applied unchanged.

## Implementation and results (2026-10-26T15:25Z)

* Reproduced before the edit: `test_bicep_assignments_equal_matrix_tuples` AttributeError at the same parser line
  (11 tests, 2 errors; the second was a missing `zava_forward` in the namespace venv, an environment gap).
* Edits: `infra/resident-demo.bicep` Secrets User GUID corrected to `...0445c86b69e6`; `infra/role-assignments.json`
  three `resident-demo` rows; `infra/tests/test_identity_rbac.py` standalone mapping plus `var`-held role resolution;
  `infra/tests/test_resident_demo_deploy.py` pinned GUID corrected.
* Mutation check: restoring the wrong GUID makes the matrix equality test fail; reverted.
* Results (local venv `/mnt/ama-rpi-gates/issue462-c3-venv` with core, agents and api installed, bicep 0.x via az):
  identity/RBAC 11 OK; resident deploy 14 OK; full infra discover with REQUIRE_AZ_BICEP=1 443 OK (was 1 error);
  `az bicep build` and `lint` of `resident-demo.bicep` clean. The two edited test files are not in the gate's ruff
  groups and keep their pre-existing ruff findings (no new ones after correcting two raw-string escapes).
* No Docker, Azure resource, secret, SQL or gate operations. No images or containers created.

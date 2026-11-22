# Research: issue 2204 combinations live (2026-11-22)

Scope: the two cases left open after #2236: Contractor with a roster binding, and the four capability roles stacked on a staff role.

## Evidence (code, read 2026-11-22 on origin/main 3a0af69ed8)

* `src/api/src/zava_forward/api/auth.py` `TrustedProxyProvider.authenticate`: requires exactly one mapped staff role or the admin role; capability roles (`RULE_ROLE_MAP`) are excluded from the staff count and surface as `rule_roles`. Capability alone is refused; capability plus one staff role is accepted. A contractor with the admin role is refused.
* `src/core/src/zava_forward/core/identity.py` `bind`: a Contractor needs exactly one enabled roster row matching tenant and object id with `role == Contractor` and a non-empty `contractor` company; otherwise the sign-in is refused (None).
* Capability gates: RuleAuthor/RuleOwner in `server.py` `_rulecards` (POST needs `rule_roles`; 403 without, validation 400 with); RegulatoryChat in `_regulatory_access` and `/api/chat/regulatory/status`; AIRestart in `continuity.restart_decide` (needs a Suspended scope with a proposal; every refusal is PermissionError, so no non-mutating probe separates it from other refusals).

## Evidence (live, in-network)

`az containerapp exec` on `ca-cutover-test-demo-api` (managed identity to Azure SQL `retrofit`) read the `staff` table: 2 rows. Aadi Kapoor (Programme Manager, no oid) and Kat Larsson (Contractor, company `Northern Facade Systems Ltd`, tid equals the app tenant, oid equals her Entra object id, 316 cases carry that company). Kat already holds `ZavaForward.Contractor` in Entra. So the binding the owner expected exists; no bind is needed. I hold no credential for Kat, so her own sign-in cannot be driven by me.

## Approach

Prove the path with the test account: add a temporary synthetic Contractor roster row for its object id, assign Contractor, sign in, probe, then delete the row and restore ProgrammeManager. For capabilities: keep ProgrammeManager and add one capability at a time, compared against a ProgrammeManager-only baseline.

Planning Readiness: Ready.

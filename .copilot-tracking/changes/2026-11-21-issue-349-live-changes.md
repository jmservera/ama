# Changes: issue 349 live round 7

Files: docs/reference/research/issue-349-tenant-prerequisites-live-r7-2026-11-21.md (new), docs/reference/README.md (index row), docs/reference/log.md (entry). Evidence: .copilot-tracking/evidence/2026-11-21/issue-349-live7/. No src change; tier focused. Azure: reads only, nothing created or to delete.

## Per-criterion table

| # | Criterion | Status | Why |
| --- | --- | --- | --- |
| 1 | Tenant owner provisions app, roles, credential | Partly proven | Registration, role claim and vault credential work; Graph read denied (needs Application Administrator), so provisioner, single-tenant flag and role definitions unproven |
| 2 | Credential in private vault, nothing published | Proven for the demo | Key Vault reference; vault public Disabled, Deny, 1 private endpoint |
| 3 | Audience and callback use the registration; prior callbacks kept | Partly proven | Sign-in completes; prior callback list unreadable |
| 4 | Private roster reconciled in VNet | Unproven, not applicable | No owner-supplied roster |
| 5 | Sign-in, role-scoped /api/me, workbench, logout, switching, denials | Proven with the test account; wrong-role and unknown-staff denial unproven at app layer live | Resident account federated to NXDOMAIN host sts.microsoftonline.com; Entra denies an unassigned principal (AADSTS501051); code-level tests cover app denial |
| 6 | Anonymous 401, forged-header denial, positive request | Proven with qualification | 401 for bad bearer, XHR 403, browser mode 302 to Entra by design; /api/cases 200 signed in |

No acceptance box ticked.

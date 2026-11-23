# Changes: issue 349 live round 9

Files: docs/reference/research/issue-349-tenant-prerequisites-live-r9-2026-11-23.md (new), docs/reference/README.md (index row), docs/reference/log.md (entry). Evidence: .copilot-tracking/evidence/2026-11-23/issue-349-live9/. No src change; tier focused. Azure: reads only, nothing created or to delete. Live revisions API 0000054, resident 0000026, both Healthy.

## Per-criterion table

| # | Criterion | Status | Why |
| --- | --- | --- | --- |
| 1 | Tenant owner provisions single-tenant app, roles, valid credential; others preserved | Proven for the demo registration; provisioner owner-gated | AzureADMyOrg, 13 roles, credential to 2027-04-22 (graph9-app.txt); provisioner not recorded |
| 2 | Credential in private vault in-VNet; networking not weakened | Proven for the demo | Vault public Disabled, Deny, 1 private endpoint (kv9.txt); no change made |
| 3 | Auth and audience use registration; callbacks preserved | Proven for resulting state; tool run unproven | ENTRA_CLIENT_ID set (env9.txt), 3 callbacks; initialize-api-auth.py run unobservable |
| 4 | Owner-supplied roster reconciled in VNet, replicas reloaded | Unproven, owner-gated | No owner roster; `bound` null |
| 5 | Real user sign-in, /api/me, workbench, logout/switching, wrong-role and unknown-staff denial | Partly proven | Test account proven (proof9.json); resident account federated to unresolvable host (realm9.json); denial only code-level test_entra_authoritative.py |
| 6 | Anonymous 401 and forged-header denial; positive request | Proven with qualification | Bad bearer 401, XHR 403, browser 302 by design, forged headers ignored, /api/cases 200 |

No acceptance box ticked on #349.

# Changes: issue 349 live round 8

Files: docs/reference/research/issue-349-tenant-prerequisites-live-r8-2026-11-22.md (new), docs/reference/README.md (index row), docs/reference/log.md (entry). Evidence: .copilot-tracking/evidence/2026-11-22/issue-349-live8/. No src change; tier focused. Azure: reads only, nothing created or to delete.

## Per-criterion table

| # | Criterion | Status | Why |
| --- | --- | --- | --- |
| 1 | Tenant owner provisions single-tenant app, roles, valid credential; unrelated registrations preserved | Proven for the demo registration; provisioner identity unproven | Graph now readable: AzureADMyOrg, 13 enabled app roles, 1 password credential valid to 2027-04-22, 3 unrelated registrations present. Who provisioned it is not recorded |
| 2 | Credential in private vault in-VNet; nothing published; networking not weakened | Proven for the demo | Only app secret is a Key Vault reference; vault public Disabled, Deny, 1 private endpoint; no change made |
| 3 | Auth and runtime audience use registration; edge callback added with prior callbacks preserved | Proven for the resulting state; tool invocation unproven | Runtime ENTRA_CLIENT_ID equals Easy Auth client id; audience api://GUID; 3 redirect URIs (demo host, Front Door, previous host). The initialize-api-auth.py run itself is not observable |
| 4 | Owner-supplied private roster reconciled in VNet, replicas reloaded | Unproven, not applicable to the demo | No owner-supplied roster; `bound` null; admission by Entra identity and app role |
| 5 | Callback/session, role-scoped /api/me, workbench, logout/switching, wrong-role and unknown-staff denial | Partly proven | Test account: callback, /api/me 200 ProgrammeManager, /app, logout 302, account picker proven. Wrong-role and unknown-staff live denial unproven: resident account federated to unresolvable sts.microsoftonline.com; code-level test test_entra_authoritative.py only. Real-user (non-test) sign-in not provable for the synthetic demo |
| 6 | Anonymous 401 and forged-header denial in browser mode; positive request | Proven with qualification | Bad bearer 401, XHR 403, browser mode 302 to Entra by design, forged headers 302 and ignored with a session; /api/cases 200 signed in |

No acceptance box ticked on #349 (criteria 4 and 5 remain open).

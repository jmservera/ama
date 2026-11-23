# Research: issue 349 live round 8 (2026-11-22)

Disposition: executed. Planning Readiness: Ready.

Evidence: .copilot-tracking/evidence/2026-11-22/issue-349-live8/ (GUIDs masked, no credentials, no screenshots because signed-in views show staff names). Baseline: docs/reference/research/issue-349-tenant-prerequisites-live-r7-2026-11-21.md.

Findings:

* New versus rounds 1 to 7: Microsoft Graph reads now succeed for the existing login (`az ad app show/list`, `az ad sp show`, `appRoleAssignedTo`). Criterion 1 and the callback half of criterion 3 can now be proven from the registration itself.
* Registration `zava-forward-api`: signInAudience AzureADMyOrg (single tenant), 13 enabled `ZavaForward.*` User app roles, one password credential valid 2026-10-24 to 2027-04-22, no certificates, identifier URI `api://<GUID>`, created 2026-10-16.
* Redirect URIs (3): current demo host, Front Door endpoint, previous `ca-cutover-test-api` host; prior callbacks preserved.
* Service principal: assignment required true, enabled; 20 user assignments covering all 13 roles (one assignment refers to a role id not in the current role list).
* Four app registrations in the tenant; unrelated ones present (m365-squad, ExchangeOnlineApp, proper-warm-api).
* Runtime `ENTRA_CLIENT_ID` equals the Easy Auth client id; Easy Auth audience `api://<GUID>`; token store off; unauthenticated action RedirectToLoginPage; the only app secret is a Key Vault reference.
* Vault `kv-cutovertest-rzsrg`: public Disabled, default Deny, 1 private endpoint.
* Browser: anonymous 302 to Entra (`code id_token`, GUID client), XHR 403, bad bearer 401, forged headers 302; test account signs in, `/api/me` 200 ProgrammeManager (source entra), `/api/cases` 200, `/app` loads, forged role header ignored, logout 302, account picker on re-login.
* Resident account: realm discovery shows federation to `sts.microsoftonline.com` (unresolvable); sign-in cannot complete; wrong-role live proof still unavailable.
* No defect found; no src change planned.

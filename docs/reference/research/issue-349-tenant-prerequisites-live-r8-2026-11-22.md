---
title: Issue 349 Tenant Prerequisites for Browser Sign-in, Live Demo Round 8
description: Eighth live demo check of issue 349; Microsoft Graph is now readable, so the registration, roles, credential and callbacks are proven directly
author: AMA programme
ms.date: 2026-11-22
ms.topic: reference
---

## Scope and authority

Owner decisions of 2026-11-18 apply: synthetic demo, desktop only, live Azure in resource
group `ama` (cap USD 700, no drills, no Key Vault rotation, no production change). Every
Azure and Graph call was a read; nothing was created, so nothing needs deleting.
Credentials were read at run time and never printed; GUIDs are masked and assignee
identities are not listed. Evidence is in
`.copilot-tracking/evidence/2026-11-22/issue-349-live8/` (`proof8.py`, `proof8.json`,
`realm8.json`, `auth-show-redacted.txt`, `graph8-app.txt`, `graph8-sp.txt`,
`redirects8.txt`, `credential-validity8.txt`, `tenant-apps8.txt`, `role-distribution8.txt`,
`audience-match8.txt`, `kv8.txt`, `secrets8.txt`). No screenshots were kept because signed-in
views show staff names. Rounds 1 to 7 ([round 7](issue-349-tenant-prerequisites-live-r7-2026-11-21.md))
stand except where noted below.

## What changed since round 7

Rounds 4 to 7 recorded `az ad app list` as denied. On 2026-11-22 the same login reads the
registration, its service principal and its role assignments. Criterion 1 and the callback
half of criterion 3 no longer depend on inference from a working sign-in.

## Results

| Check | Result |
| --- | --- |
| Registration `zava-forward-api` | `signInAudience` AzureADMyOrg (single tenant); identifier URI `api://<GUID>`; created 2026-10-16; ID-token issuance on |
| Application roles | 13 enabled `ZavaForward.*` roles, member type User |
| Client credential | 1 password credential, valid 2026-10-24 to 2027-04-22; no certificates |
| Service principal | Enabled; assignment required; 20 user assignments covering all 13 roles (one assignment points at a role id no longer in the role list) |
| Other registrations | 3 further tenant registrations present (`m365-squad`, `ExchangeOnlineApp-26-04-15-01`, `proper-warm-api`), all single tenant |
| Redirect URIs | 3 `/.auth/login/aad/callback` entries: current demo host, Front Door endpoint, previous `ca-cutover-test-api` host |
| Runtime audience | `ENTRA_CLIENT_ID` equals the Easy Auth client ID; allowed audience `api://<GUID>`; token store off; unauthenticated action `RedirectToLoginPage` |
| Credential path | The one app secret is a Key Vault reference |
| Vault | `kv-cutovertest-rzsrg`: public access Disabled, default Deny, 1 private endpoint |
| Anonymous browser `/api/me` | 302 to `login.microsoftonline.com`, callback `/.auth/login/aad/callback`, `code id_token`, GUID client |
| Anonymous XHR; bad bearer; forged principal headers without session | 403; 401; 302 |
| Test-account sign-in | `/api/me` 200, role `Retrofit Programme Manager`, app role `ZavaForward.ProgrammeManager`, source `entra`, `bound` null, 13 navigation entries |
| Positive authenticated request; workbench | `/api/cases` 200; `/app` titled "My cases today" |
| Forged role header with session | Role unchanged |
| Logout, re-login | `/api/me` 302 after logout; Entra account picker shown |
| Resident account | Realm discovery: federated to `sts.microsoftonline.com`, which does not resolve; password sign-in cannot complete (Next button stays disabled) |

## Acceptance criteria

| # | Criterion | Demo status | Basis |
| --- | --- | --- | --- |
| 1 | Tenant owner provisions single-tenant app, roles, valid credential; unrelated registrations preserved | Proven for the demo registration; provisioner identity unproven | Single tenant, 13 roles, valid credential and three other registrations are read directly. Who provisioned it is not recorded |
| 2 | Credential in private vault in-VNet; nothing published; networking not weakened | Proven for the demo | Key Vault reference, vault public access disabled with a private endpoint, no change made, secret value not read |
| 3 | Auth and runtime audience use the registration; edge callback added, prior callbacks preserved | Proven for the resulting state; tool run unproven | Client IDs match, audience matches, the Front Door and earlier host callbacks sit beside the current one. The `initialize-api-auth.py --public-url` invocation itself cannot be observed |
| 4 | Owner-supplied roster reconciled in the VNet, replicas reloaded | Unproven, not applicable to the demo | No owner-supplied roster exists and none may be invented; `bound` is null; admission is by Entra identity and app role |
| 5 | Callback and session, role-scoped `/api/me`, workbench, logout and switching, wrong-role and unknown-staff denial | Partly proven | Proven with the test account. Live wrong-role and unknown-staff denial need a second signed-in account; the resident account cannot sign in. Code-level denial: `src/api/tests/test_entra_authoritative.py`. A non-test real user is out of scope for the synthetic demo |
| 6 | Anonymous 401 and forged-header denial in browser mode; positive request | Proven with a qualification | 401 for a bad bearer, 403 for XHR, browser mode redirects to Entra by design and never returns 200; forged headers ignored; `/api/cases` 200 when signed in |

## Conclusion

No defect was found, so no source code or test changed. Criteria 4 and 5 stay open for
want of an owner roster and a second working staff account; no box on #349 is ticked from
this evidence.

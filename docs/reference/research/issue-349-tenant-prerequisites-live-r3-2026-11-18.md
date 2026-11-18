---
title: Issue 349 Tenant Prerequisites for Browser Sign-in, Live Demo Round 3
description: Third live demo check of the six issue 349 acceptance criteria, adding the Entra authorize redirect URI and fresh browser, curl and Azure read-only evidence
author: AMA programme
ms.date: 2026-11-18
ms.topic: reference
---

## Scope and authority

Owner decisions of 2026-11-18: synthetic demo, desktop only; live Azure
authorised in resource group `ama` (cap USD 700, no drills, no Key Vault
rotation, no production change). Billing reconciliation, DPO and Legal
approval and person-run assistive-technology testing are not needed.
Every Azure call was a read; nothing was created, changed or needs deleting.
Credentials were read from the owner's files at run time and never printed; a
literal scan of the retained evidence for each credential value found no match.

This round follows [the first note](entra-signin-live-demo-2026-11-18.md) and
[round 2](issue-349-tenant-prerequisites-live-2026-11-18.md). It re-runs the
checks on 2026-11-18 14:15 UTC and adds the redirect URI that Entra received.
Target: `ca-cutover-test-demo-api`. Evidence is in
`.copilot-tracking/evidence/2026-11-18/issue-349-live2/` (`proof2.py`,
`proof2.json`, `curl-status.txt`, `auth-show.txt`, `secrets.txt`,
`kv-network.txt`, `env.txt`, `env-auth.txt`). A
screenshot of the account picker rendered blank and was deleted; the picker
result rests on `proof2.json` and round 2.

## Findings

| Finding | Result | Evidence |
| --- | --- | --- |
| Redirect URI sent to Entra | Anonymous `/api/me` gives 302 to `login.microsoftonline.com` with `redirect_uri` of `https://<app-host>/.auth/login/aad/callback`, `response_type` `code id_token` and a GUID `client_id` | `proof2.json` |
| Redirect URI is registered | The callback returned to the app and `/api/me` was 200. Entra rejects an unregistered URI before sign-in, so the edge callback is registered; the full list stays unreadable | `proof2.json` |
| Roles | `/api/me`: role `Retrofit Programme Manager`, app role `ZavaForward.ProgrammeManager`, `view_only` false, `identity_source` `entra`, provider `trusted-proxy`, tenant GUID, 13 navigation entries | `proof2.json` |
| Easy Auth config | Enabled, `RedirectToLoginPage`, GUID client ID (not `systemAssignedIdentity`), allowed audiences client ID and `api://` form, token store off, `prompt=select_account` | `auth-show.txt` |
| Credential path | One app secret, a Key Vault reference through a user-assigned identity | `secrets.txt` |
| Vault networking | `kv-cutovertest-rzsrg`: public access Disabled, default action Deny, one private endpoint; environment is VNet-integrated, not internal | `kv-network.txt`, `env.txt` |
| Graph objects | `az ad app list` and a direct Graph `applications` call return insufficient privileges | command output, this note |
| Anonymous, no session | Browser mode `/api/me` 302 to Entra; `curl` `/api/me` and `/api/cases` 401; XHR 403; bad bearer 401 | `proof2.json`, `curl-status.txt` |
| Forged headers, no session | `X-MS-CLIENT-PRINCIPAL-*` plus `X-ZF-Role: Admin`: 302 to Entra in browser mode, 401 with `curl`; never 200 | `proof2.json`, `curl-status.txt` |
| Forged headers with session | Role stays `Retrofit Programme Manager` | `proof2.json` |
| Positive authenticated request | `/api/cases` 200 | `proof2.json` |
| Workbench entry | `/app` titled "Zava Forward, Zava North Homes" with briefing and filters | Screenshot not retained (showed names) |
| Logout and re-login | `/.auth/logout`, then `/api/me` 302 to Entra and an Entra picker or form is shown | `proof2.json` |
| Roster binding | `bound` is null in this run (false in earlier rounds): no private roster binds the account | `proof2.json` |

## Acceptance criteria

| # | Criterion | Demo status | Basis |
| --- | --- | --- | --- |
| 1 | Owner provisions single-tenant app, roles, credential; unrelated registrations preserved | Partly proven | Working GUID registration, vault credential and role claim exist. Provisioner, single-tenant audience and role definitions are unreadable (Graph denied) |
| 2 | Credential reaches the private vault in-VNet; nothing published; networking not weakened | Proven for the demo | Key Vault reference via user-assigned identity; vault public-disabled with a private endpoint; no change made. The secret value was not read |
| 3 | API auth and audience use the registration; edge callback added with prior callbacks preserved | Partly proven | Edge callback is registered (proven by a completed sign-in); audiences and client ID are consistent. The prior callback list and `initialize-api-auth.py` history are unreadable, so preservation is unproven |
| 4 | Private staff roster reconciled in the VNet, replicas reloaded, no fictional identity | Unproven, not applicable to the demo | No owner-supplied roster; admission is by Entra identity and app role |
| 5 | Real user completes callback, role-scoped `/api/me`, workbench entry; logout, switching, wrong-role and unknown-staff denial | Proven with the test account only | Callback, `/api/me`, `/app`, logout and re-login prompt shown. Unknown-staff and second-role denial need a real roster and another role account; no real person took part |
| 6 | Anonymous 401 and forged-header denial in browser mode, plus a positive authenticated request | Proven with a qualification | 401 with `curl`, 302 to Entra in a browser by design, never 200; authenticated `/api/cases` 200; forged headers ignored with a session |

## Open items

* A tenant owner with Application Administrator rights must confirm the
  registration (audience, roles, redirect URI list, assignment requirement),
  supply a staff roster and a second-role account.
* Criteria 1, 3, 4 stay unticked; 5 is limited to the test account. Nothing
  here ticks an item on #349.

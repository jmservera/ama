---
title: Issue 349 Tenant Prerequisites for Browser Sign-in, Live Demo Round 4
description: Fourth live demo check of the six issue 349 acceptance criteria with fresh Playwright and Azure read-only evidence
author: AMA programme
ms.date: 2026-11-19
ms.topic: reference
---

## Scope and authority

Owner decisions of 2026-11-18 apply: synthetic demo, desktop only, live Azure in
resource group `ama` (cap USD 700, no drills, no Key Vault rotation, no production
change). Every Azure call on 2026-11-19 was a read; nothing was created, so nothing
needs deleting. Credentials were read at run time and never printed. Evidence is in
`.copilot-tracking/evidence/2026-11-19/issue-349-live4/` with GUIDs masked. Screenshots
were not retained because the signed-in views show staff names. Round 3
([note](issue-349-tenant-prerequisites-live-r3-2026-11-18.md)) is unchanged; this run
reproduces it.

## Results

| Check | Result | Evidence |
| --- | --- | --- |
| Anonymous `/api/me`, browser mode | 302 to `login.microsoftonline.com`, callback `https://<app-host>/.auth/login/aad/callback`, `code id_token`, GUID client ID | `proof4.json` |
| Anonymous with `curl` | `/api/me` 401, `/api/cases` 401; XHR 403; bad bearer 401 | `curl-status.txt`, `proof4.json` |
| Forged principal headers, no session | 302 to Entra, never 200 | `proof4.json` |
| Sign-in with the test account | Callback returned; `/api/me` 200, role `Retrofit Programme Manager`, app role `ZavaForward.ProgrammeManager`, `identity_source` `entra`, 13 navigation entries | `proof4.json` |
| Forged headers with session | Role unchanged | `proof4.json` |
| Positive authenticated request | `/api/cases` 200 | `proof4.json` |
| Workbench entry | `/app` titled "Zava Forward" with the Zava North Homes suffix | `proof4.json` |
| Logout and re-login | `/api/me` 302 after logout; Entra account picker shown | `proof4.json` |
| Easy Auth | Enabled, `RedirectToLoginPage`, GUID client ID, audiences client ID and `api://` form, token store off | `auth-show.txt` |
| Credential path | One secret, Key Vault reference | `secrets.txt` |
| Vault networking | `kv-cutovertest-rzsrg`: public Disabled, default Deny, 1 private endpoint | `kv-network.txt` |
| Graph application objects | `az ad app list` fails: insufficient privileges | `graph.txt` |
| Roster binding | `bound` null: no private roster binds the account | `proof4.json` |

## Acceptance criteria

| # | Criterion | Demo status | Basis |
| --- | --- | --- | --- |
| 1 | Tenant owner provisions single-tenant app, roles, credential; unrelated registrations preserved | Partly proven | A working GUID registration, vault credential and role claim exist. Provisioner, single-tenant setting and role definitions are unreadable (Graph denied) |
| 2 | Credential reaches the private vault in-VNet; no publication; networking not weakened | Proven for the demo | Vault reference; public access disabled with a private endpoint; no change made; secret value not read |
| 3 | API auth and audience use the registration; edge callback added, prior callbacks preserved | Partly proven | The sign-in completed, so the callback is registered and audiences match; the prior callback list is unreadable, so preservation is unproven |
| 4 | Private staff roster reconciled in the VNet, replicas reloaded | Unproven, not applicable to the demo | No owner-supplied roster exists; admission is by Entra identity and app role |
| 5 | Real user completes callback, `/api/me`, workbench entry; logout, switching, wrong-role and unknown-staff denial | Proven with the test account only | Callback, role-scoped `/api/me`, `/app`, logout and picker shown. Wrong-role and unknown-staff denial need another role account and a roster |
| 6 | Anonymous 401 and forged-header denial in browser mode; positive authenticated request | Proven with a qualification | 401 with `curl`; browser mode redirects to Entra by design and never returns 200; `/api/cases` 200 when signed in |

## Conclusion

The first unmet criterion (1) needs Application Administrator rights in the tenant and
is not a source change; no code or test was added. No box on #349 is ticked from this
evidence.

---
title: Issue 349 Tenant Prerequisites for Browser Sign-in, Live Demo Round 5
description: Fifth live demo check of the six issue 349 acceptance criteria, adding a resident-account wrong-role probe
author: AMA programme
ms.date: 2026-11-19
ms.topic: reference
---

## Scope and authority

Owner decisions of 2026-11-18 apply: synthetic demo, desktop only, live Azure in resource
group `ama` (cap USD 700, no drills, no Key Vault rotation, no production change). Every
Azure call was a read and nothing was created, so nothing needs deleting. Credentials were
read at run time and never printed; GUIDs are masked. Evidence is in
`.copilot-tracking/evidence/2026-11-19/issue-349-live5/` (`proof5.py`, `proof5.json`,
`resident5.py`, `resident5.json`, `auth-show.txt`, `secrets.txt`, `kv-network.txt`,
`graph.txt`, `curl-status.txt`). No screenshots were kept because signed-in views show
staff names. Round 4 ([note](issue-349-tenant-prerequisites-live-r4-2026-11-19.md)) is
reproduced and not changed. The first call to the app timed out once on a cold start and
passed on the immediate retry.

## Results

| Check | Result |
| --- | --- |
| Anonymous browser `/api/me` | 302 to `login.microsoftonline.com`, callback `/.auth/login/aad/callback`, `code id_token`, GUID client ID |
| Anonymous with `curl` | `/api/me` 401, `/api/cases` 401; XHR 403; bad bearer 401 |
| Forged principal headers, no session | 302 to Entra, never 200 |
| Sign-in with the test account | `/api/me` 200, role `Retrofit Programme Manager`, app role `ZavaForward.ProgrammeManager`, source `entra`, 13 navigation entries |
| Forged `X-ZF-Role` with session | Role unchanged |
| Positive authenticated request | `/api/cases` 200 |
| Workbench entry | `/app` title "Zava Forward \| Zava North Homes" |
| Logout, then re-login | `/api/me` 302; Entra account picker shown |
| Easy Auth | Enabled, `RedirectToLoginPage`, audiences client ID and `api://` form, token store off |
| Credential path | One secret, Key Vault reference |
| Vault | `kv-cutovertest-rzsrg`: public Disabled, default Deny, 1 private endpoint |
| Graph application objects | `az ad app list`: insufficient privileges |
| Roster binding | `bound` null |
| Resident test account, wrong-role probe | Not completed: the Entra form disabled the Next button, then the browser landed on a Chrome error page (`chromewebdata`) in two attempts. No role decision was observed |

## Acceptance criteria

| # | Criterion | Demo status | Basis |
| --- | --- | --- | --- |
| 1 | Tenant owner provisions single-tenant app, roles, credential; unrelated registrations preserved | Partly proven | Working GUID registration, vault credential and role claim exist; provisioner, single-tenant flag and role definitions unreadable (Graph denied) |
| 2 | Credential in the private vault in-VNet; nothing published | Proven for the demo | Vault reference, public access disabled, private endpoint, no change made |
| 3 | API auth and audience use the registration; callback added, prior callbacks preserved | Partly proven | Sign-in completes so the callback and audiences match; prior callback list unreadable |
| 4 | Private roster reconciled in the VNet, replicas reloaded | Unproven, not applicable to the demo | No owner-supplied roster; admission is by Entra identity and app role |
| 5 | Real user completes callback, `/api/me`, workbench; logout, switching, wrong-role and unknown-staff denial | Proven with the test account only | Wrong-role and unknown-staff denial remain unproven: the resident account probe failed at sign-in |
| 6 | Anonymous 401 and forged-header denial in browser mode; positive request | Proven with a qualification | 401 by `curl`; browser mode redirects to Entra by design; `/api/cases` 200 when signed in |

## Conclusion

The first unmet criterion (1) needs Application Administrator rights and is not a source
change, so no code or test was added and no box on #349 is ticked. Next evidence that
would close criterion 5 is a second-role staff account or a fixed resident sign-in path.

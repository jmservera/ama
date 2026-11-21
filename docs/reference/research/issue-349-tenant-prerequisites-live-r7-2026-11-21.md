---
title: Issue 349 Tenant Prerequisites for Browser Sign-in, Live Demo Round 7
description: Seventh live demo check of issue 349, correcting the round 6 DNS diagnosis and adding an Entra-level unassigned-principal denial
author: AMA programme
ms.date: 2026-11-21
ms.topic: reference
---

## Scope and authority

Owner decisions of 2026-11-18 apply: synthetic demo, desktop only, live Azure in resource
group `ama` (cap USD 700, no drills, no Key Vault rotation, no production change). Every
Azure call was a read and nothing was created, so nothing needs deleting. Credentials were
read at run time and never printed; GUIDs are masked. Evidence is in
`.copilot-tracking/evidence/2026-11-21/issue-349-live7/` (`proof7.py`, `proof7.json`,
`realm7.py`, `realm7.json`, `auth-show-redacted.txt`, `kv7.txt`, `graph7.txt`). Rounds 4 to 6
([round 6](issue-349-tenant-prerequisites-live-r6-2026-11-19.md)) stand unchanged except
for the correction below. No screenshots were kept because signed-in views show staff names.

## Results

| Check | Result |
| --- | --- |
| Anonymous browser `/api/me` | 302 to `login.microsoftonline.com`, callback `/.auth/login/aad/callback`, `code id_token`, GUID client ID |
| Anonymous XHR; bad bearer | 403; 401 |
| Forged principal headers, no session | 302 to Entra, never 200 |
| Sign-in with the test account | `/api/me` 200, role `Retrofit Programme Manager`, app role `ZavaForward.ProgrammeManager`, source `entra`, 13 navigation entries |
| Positive authenticated request | `/api/cases` 200; `/app` loads "My cases today" |
| Forged `X-ZF-Role` with session | Role unchanged |
| Logout, then re-login | `/api/me` 302; Entra account picker shown |
| Easy Auth | Enabled, `RedirectToLoginPage`, audience `api://<GUID>` |
| Vault | `kv-cutovertest-rzsrg`: public Disabled, default Deny, 1 private endpoint; the one app secret is a Key Vault reference |
| Graph application objects | `az ad app list`: insufficient privileges |
| Azure CLI token for the app audience | `AADSTS501051`: the CLI application is not assigned to a role for the API, so Entra denies it before the app sees a token |

## Correction to round 6

Round 6 blamed the worker host's DNS for the resident account failure. Realm discovery
(`realm7.json`) shows the resident account is federated to `sts.microsoftonline.com`, and
that name returns NXDOMAIN from a public resolver (8.8.8.8) as well as from this host. The
account therefore cannot complete a password sign-in from any browser; this is a property
of the account, not of the worker host or the application. A resident sign-in retried in
Playwright failed the same way (`chromewebdata` after a disabled Next button). No app-layer
wrong-role decision was observed.

## Acceptance criteria

| # | Criterion | Demo status | Basis |
| --- | --- | --- | --- |
| 1 | Tenant owner provisions single-tenant app, roles, credential | Partly proven | Working GUID registration, role claim and vault credential exist; provisioner, single-tenant flag and role definitions unreadable (Graph denied, needs Application Administrator) |
| 2 | Credential in private vault in-VNet; nothing published | Proven for the demo | Vault reference, public access disabled, private endpoint, no change made |
| 3 | Audience and callback use the registration; prior callbacks preserved | Partly proven | Sign-in completes, so callback and audience match; prior callback list unreadable |
| 4 | Private roster reconciled in the VNet, replicas reloaded | Unproven, not applicable to the demo | No owner-supplied roster; admission is by Entra identity and app role |
| 5 | Callback, role-scoped `/api/me`, workbench, logout, switching, wrong-role and unknown-staff denial | Proven with the test account; unassigned-principal denial proven at Entra only | App-layer wrong-role live proof needs a signed-in staff account without the role; the only candidate (resident) is federated to an unresolvable host. Code-level denial: `src/api/tests/test_entra_authoritative.py::test_anonymous_unassigned_wrong_tenant_and_bad_oid_are_denied` |
| 6 | Anonymous 401, forged-header denial, positive request | Proven with a qualification | 401 by `curl`-style request; browser mode redirects to Entra by design; `/api/cases` 200 when signed in |

## Conclusion

No real defect was found, so no source code or test changed and no box on #349 is
ticked. Criterion 1 needs a tenant owner; criterion 4 needs an owner roster; the
app-layer half of criterion 5 needs a second staff account that can sign in.

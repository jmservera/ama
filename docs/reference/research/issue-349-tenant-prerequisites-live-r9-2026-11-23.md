---
title: Issue 349 Tenant Prerequisites for Browser Sign-in, Live Demo Round 9 Close-out
description: Close-out pass for issue 349 against main and the live revisions API 0000054 and resident 0000026, with a per-criterion proven, unproven or owner-gated verdict
author: AMA programme
ms.date: 2026-11-23
ms.topic: reference
---

## Scope and authority

Owner decisions of 2026-11-18 apply: synthetic demo, desktop only, live Azure in resource
group `ama` (cap USD 700, no drills, no Key Vault rotation, no production change). Every
Azure and Graph call was a read and the browser proof used a throwaway Playwright
context, so nothing was created and nothing needs deleting. Credentials were read at run
time and never printed; GUIDs are masked. Evidence is in
`.copilot-tracking/evidence/2026-11-23/issue-349-live9/` (`proof9.py`, `proof9.json`,
`realm9.json`, `revisions9.txt`, `graph9-app.txt`, `kv9.txt`, `env9.txt`). No screenshots
were kept because signed-in views show staff names. Round 8
([r8](issue-349-tenant-prerequisites-live-r8-2026-11-22.md)) stands except where noted.

## Comparison with main and live

* Live revisions: API `ca-cutover-test-demo-api--0000054` and resident
  `ca-resident-demo--0000026`, both Healthy at 100 percent traffic (created 2026-11-22).
* Main: the last src commits touching the API and core (for example `6a03928ccb`,
  roster-scoped Entra staff, and `a6ba1956db`) do not change the sign-in path. No code gap
  against any criterion was found, so no source or test changed.
* The 0000054 digest is still not traceable to a commit, so "live equals main" is not
  claimed.

## Results

| Check | Result |
| --- | --- |
| Registration | `AzureADMyOrg`, 13 app roles, one password credential ending 2027-04-22, 3 callback URIs |
| Runtime | `ENTRA_CLIENT_ID` set on the API app; browser authorize request uses a GUID client and `code id_token` |
| Vault | `kv-cutovertest-rzsrg`: public access Disabled, default Deny, 1 private endpoint |
| Anonymous browser `/api/me` | 302 to `login.microsoftonline.com`, callback `/.auth/login/aad/callback` |
| Anonymous XHR; bad bearer; forged principal headers without session | 403; 401; 302 |
| Test-account sign-in | `/api/me` 200, `Retrofit Programme Manager`, `ZavaForward.ProgrammeManager`, source `entra`, `bound` null, 13 navigation entries; `/api/cases` 200; `/app` "My cases today" |
| Forged role header with session | Role unchanged |
| Logout, re-login | `/api/me` 302 after logout; account picker shown |
| Resident account | Realm discovery federates to `sts.microsoftonline.com`; Next stays disabled; sign-in cannot complete |

## Acceptance criteria

| # | Criterion | Verdict | Basis |
| --- | --- | --- | --- |
| 1 | Tenant owner provisions single-tenant app, roles, valid credential; others preserved | Proven for the demo registration; provisioner owner-gated | Registration facts read directly; who provisioned it is not recorded |
| 2 | Credential in private vault via in-VNet path; nothing published; networking not weakened | Proven for the demo | Vault public access Disabled with a private endpoint; no change made; secret not read |
| 3 | Auth and audience use the registration; edge callback added with prior callbacks preserved | Proven for the resulting state; tool run unproven | Client ID set and callbacks include earlier hosts; the `initialize-api-auth.py --public-url` run is not observable |
| 4 | Owner-supplied staff roster reconciled in the VNet, replicas reloaded | Unproven, owner-gated | No owner roster exists and none may be invented; `bound` null |
| 5 | Real user callback, role-scoped `/api/me`, workbench, logout and switching, wrong-role and unknown-staff denial | Partly proven | Proven with the test account. Live denial needs a second working account (resident account unreachable); denial is covered only by `src/api/tests/test_entra_authoritative.py`. A non-test real user is outside the synthetic demo |
| 6 | Anonymous 401 and forged-header denial in browser mode; positive request | Proven with a qualification | Bad bearer 401, XHR 403, browser mode redirects by design; forged headers ignored; `/api/cases` 200 signed in |

## Conclusion

No defect and no code gap, so no src change. Criteria 4 and 5 stay open; no box on #349
is ticked from this evidence.

---
title: Entra Browser Sign-in Proof on the Deployed Demo (Issue 349)
description: Live Playwright evidence for browser sign-in, anonymous 401, role-scoped /api/me and denial paths on the synthetic demo apps, with what a real-user tenant registration would still need
author: AMA programme
ms.date: 2026-11-18
ms.topic: reference
---

## Scope and authority

Owner decisions of 2026-11-18: this is the synthetic demo, desktop only. Live
Azure was authorised (resource group `ama`, cap USD 700, no drills, no Key
Vault rotation, no production change). Azure billing reconciliation, DPO and
Legal approval and person-run assistive-technology testing are not needed for
the demo. The checks were read-only: no Azure resource, setting or secret was
changed, and nothing was created or needs deleting. Credentials were read from
the owner's files at run time and were never printed or stored; a literal scan
of every retained evidence file for each credential value found no match.

Targets: `ca-cutover-test-demo-api` (Easy Auth with Entra, employee workbench)
and `ca-resident-demo` (application-local shared demo sign-in, no Easy Auth).
Browser: Playwright Chromium, 1366 by 900 desktop viewport, 2026-11-18
07:50 to 08:15 UTC. Issue #349 describes the older `ca-cutover-test-api` gap
of 2026-10-16; this note does not re-test that app.

Evidence files (scripts, redacted JSON outputs, screenshots and the original
failed attempts) are under
`.copilot-tracking/evidence/2026-11-18/issue-349-live/`.

## Observations

| Observation | Result | Evidence |
| --- | --- | --- |
| Anonymous browser request to `/api/me` | 302 to `login.microsoftonline.com` (`RedirectToLoginPage`) | `run1.json`, `employee-1-entra-redirect.png` |
| Anonymous non-browser request (`curl`) to `/api/me`, `/api/cases`, `/workspace-shell.js` | 401 each; `X-Requested-With: XMLHttpRequest` gives 403; invalid bearer token gives 401 | curl status codes recorded in the changes record |
| Forged `X-MS-CLIENT-PRINCIPAL-NAME` and `-ID` headers, no session | 401 (curl); 302 to Entra (Playwright request) | `run1.json` |
| Forged `X-ZF-Role: Admin` header, no session | 401 | curl |
| Employee test account Entra sign-in in the browser | Callback returned to the app origin, `/api/me` 200 | `run1.json` |
| Role-scoped `/api/me` | Role `Retrofit Programme Manager`, app role `ZavaForward.ProgrammeManager`, `view_only` false, `identity_source` `entra`, provider `trusted-proxy`, tenant and object IDs are GUIDs (values not retained), 13 navigation entries | `run1.json` |
| Positive platform-authenticated API request | `/api/cases` 200; `/api/workorders/x/job-pack` 404 (unknown id); `/api/law/alerts` 503 (law service not configured, existing behaviour) | `run1.json` |
| Forged header sent with a valid session | Role unchanged (`Retrofit Programme Manager`): the header is ignored | `logout-run1.json` |
| Workbench entry | `/sign-in` shows the Entra account picker (select-account prompt), selecting the account lands on `/app` titled "Zava Forward" with the briefing and filters | `employee-2b-workbench.png` |
| Logout | `/.auth/logout` ends at Entra sign-out; the next `/api/me` is 302 to Entra again | `logout-run1.json`, `employee-3-after-logout.png` |
| Resident demo sign-in (shared demo credentials, form) | `/demo/login` 200, `/demo/view` 200; before sign-in `/demo/view` 401 | `resident-run5.json`, `resident-2-signed-in.png` |
| Resident session against staff paths | `/api/me`, `/api/cases`, `/api/staff`, `/demo/staff`, `/demo/admin` all 404 (the resident app exposes no staff surface) | `resident-run5.json` |
| Wrong credentials on the resident app | Wrong password 401; the employee Entra account on the resident form 401; neither gets a session | `resident-run5.json` |
| Resident sign-out | `#signout` returns to the form; the old session fence gives 401 and `signed_in` is false | `resident-run5.json` |
| Resident test account on the employee Entra sign-in | Not an Entra tenant user: the account's domain is `example.com` and Entra's federation lookup fails (`ERR_NAME_NOT_RESOLVED`), so no sign-in is possible | `run1.json` (timeout), `resident-run1-initial-failure.err` |

## Read-only Azure configuration facts

* Easy Auth is enabled with `RedirectToLoginPage`; the registration client ID
  is a GUID (not the literal `systemAssignedIdentity` seen on 2026-10-16), a
  client secret setting name is present with one matching app secret, token
  store is off, and allowed audiences are the client ID and its `api://` form.
  The issuer is the deployment tenant.
* Application settings: `ZF_AUTH=trusted-proxy`, `ZF_TRUSTED_PROXY=1`,
  `ZF_ENV=production`, `ZF_DEPLOYMENT_PROFILE=demo`, minimum replicas 0.
* `az ad app list` and `az ad sp list` with the existing login returned
  insufficient privileges, so the registration's sign-in audience, app-role
  definitions and assignment requirement could not be read directly. The
  `app_roles` claim in `/api/me` is the only evidence of the role assignment.

## Observed incidents (kept as adverse evidence)

* The first resident attempts failed: a wrong selector for the sign-out
  control, then HTTP 429 from the demo login limiter (five failures per source
  in a 600 second window, which the deliberate wrong-credential checks and
  retries exhausted), then a cold-start request timeout. The limiter is a
  working control; the passing run followed a 10 minute wait and a warm-up.
* The first combined run reported the resident account as an Entra timeout;
  the diagnostic traced it to the unresolvable federation host above. The
  blank diagnostic screenshot of that attempt was deleted during the session
  and is not retained.

## Acceptance criteria

| # | Criterion | Status for the demo | Basis |
| --- | --- | --- | --- |
| 1 | Authorised tenant owner provisions single-tenant app, roles and credential | Partly proven | A GUID registration with a client secret setting and a role claim exists and works for the demo. Provisioning authority, single-tenant audience and the role definitions cannot be read (Graph privileges), so who provisioned it is unproven |
| 2 | Credential reaches the private vault through an approved in-VNet path | Unproven | The app carries one app-level secret; the vault path was not inspected and Key Vault rotation was excluded. Nothing here proves the in-VNet delivery |
| 3 | API auth and runtime audience use the real registration; edge callback added with `--public-url` and prior callbacks preserved | Partly proven | Sign-in callback works end to end on the demo edge and the audiences match the registration. The callback list and `initialize-api-auth.py` history were not read |
| 4 | Private staff roster reconciled in the VNet, replicas reloaded, no fictional identity | Unproven for the demo | `/api/me` shows `bound` false: the account is admitted by Entra identity and role, not a roster. A roster is a real-staff feature; the demo has none |
| 5 | Real user completes callback, role-scoped `/api/me`, workbench entry; logout and account switching; wrong-role and unknown-staff denial | Proven with the test account, not a real user | Callback, `/api/me`, `/app` entry, logout and account picker are shown. Wrong-account denial is shown at the resident form and at Entra; a wrong-role denial inside the employee app needs a second staff account with a different role, which the demo does not have. Real-user and unknown-staff denial are unproven |
| 6 | Anonymous 401 and forged-header denial in browser mode, with a positive authenticated request | Proven | See the observations table. Browsers get a 302 to Entra by design; non-browser and XHR clients get 401 or 403 |

## What a real-user tenant registration would still need

* A tenant owner (Application Administrator or Cloud Application
  Administrator, plus Privileged Role Administrator if roles need consent)
  confirms the single-tenant app registration, its app roles and the
  enterprise application's assignment requirement, and assigns named staff to
  roles. Our login cannot read these objects.
* A client credential held in the private vault, delivered through the
  approved in-VNet path, with an owner-approved rotation plan.
* The `--public-url` callback registered with prior callbacks preserved.
* An owner-supplied private staff roster reconciled inside the VNet, so that
  `bound` becomes true and unknown staff are denied; replicas reloaded.
* At least one real staff user and one second-role staff user for the
  logout, account switching and wrong-role denial runs.
* For any resident-facing real identity (rather than the shared demo
  sign-in), a separate decision: the resident demo uses an application-local
  shared credential that does not prove who the user is.

None of these is needed for the synthetic demo; criteria 1, 2 and 4 therefore
stay unticked on #349 and criteria 3, 5 and 6 are partly or demo-proven only.

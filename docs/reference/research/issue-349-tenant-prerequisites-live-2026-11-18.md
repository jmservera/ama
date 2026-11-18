---
title: Issue 349 Tenant Prerequisites for Browser Sign-in, Live Demo Re-verification
description: Per-criterion proof status for the six issue 349 acceptance criteria on the synthetic demo, from read-only Azure checks and Playwright runs with the test sign-in
author: AMA programme
ms.date: 2026-11-18
ms.topic: reference
---

## Scope and authority

Owner decisions of 2026-11-18: synthetic demo, desktop only. Live Azure is
authorised in resource group `ama` (cap USD 700, no drills, no Key Vault
rotation, no production change). Billing reconciliation, DPO and Legal
approval and person-run assistive-technology testing are not needed for the
demo. This run changed nothing in Azure: every Azure call was a read, and no
throwaway resource was created. Credentials were read from the owner's files
at run time and never printed; a literal scan of every retained text file for
each credential value found no match. Screenshots show the test account
address masked as `[email]`; one screenshot that displayed the account display
name was deleted.

It extends [the earlier 2026-11-18 sign-in note](entra-signin-live-demo-2026-11-18.md),
which stays as the first run. This run closes the gaps that note left open:
retained anonymous and forged-header results, the secret's vault path, the
Entra-side wrong-credential denial and the role-scoped denial.

Target: `ca-cutover-test-demo-api` (Easy Auth with Entra). Evidence is in
`.copilot-tracking/evidence/2026-11-18/issue-349-live2/` (script
`prereq_proof.py`, `prereq-run1.json`, redacted Azure outputs, two
screenshots; a signed-out welcome capture that was mislabelled as the workbench was deleted). Run time 2026-11-18 11:38 to 11:45 UTC.

## Findings

| Finding | Result | Evidence |
| --- | --- | --- |
| Auth client is a real registration | Client ID is a GUID, not `systemAssignedIdentity`; equals the `ENTRA_CLIENT_ID` app setting; issuer tenant equals `ENTRA_TENANT_ID` and the Azure login tenant; audiences are the client ID and its `api://` form | `auth-show-redacted.json`, `config-consistency.txt` |
| Credential path | The only app secret is a Key Vault reference (`keyVaultUrl` set) resolved by a user-assigned identity; the Easy Auth `clientSecretSettingName` points at it | `secret-source.txt`, `auth-show-redacted.json` |
| Vault networking | `kv-cutovertest-rzsrg`: public network access Disabled, default action Deny, RBAC authorisation on, private endpoint `pe-kv-cutovertest-rzsrg` Approved; a direct secret list from this host is refused as "not an approved private link" | `kv-show.json`, `private-endpoints.txt`, `kv-list-attempt.txt` |
| Graph objects | `az ad app show` and `az ad sp show` return insufficient privileges; sign-in audience, role definitions and assignment requirement stay unreadable | `graph-app-show.txt`, `graph-sp-show.txt` |
| Anonymous browser request | `/api/me`, `/api/cases`, `/workspace-shell.js` give 302 to `login.microsoftonline.com`, also with `Accept: application/json` | `prereq-run1.json` (`anon`) |
| Anonymous non-redirect clients | `X-Requested-With: XMLHttpRequest` gives 403; invalid bearer token gives 401 | `prereq-run1.json` |
| Forged identity headers, no session | `X-MS-CLIENT-PRINCIPAL-NAME`/`-ID`, `X-MS-CLIENT-PRINCIPAL` and `X-ZF-Role: Admin` each give 302 to Entra, never 200 | `prereq-run1.json` |
| Forged headers with a valid session | Status 200, role and object identity unchanged | `prereq-run1.json` (`forged_with_session`) |
| Entra sign-in | Callback returns to the app; `/api/me` 200, role `Retrofit Programme Manager`, app role `ZavaForward.ProgrammeManager`, `identity_source` `entra`, provider `trusted-proxy`, tenant and object IDs GUIDs (values not retained), 13 navigation entries | `prereq-run1.json` (`session`) |
| Positive platform-authenticated requests | `/api/cases` 200, `/api/me` 200 | `prereq-run1.json` (`positive_requests`) |
| Workbench entry | `/app` loads titled "Zava Forward, Zava North Homes" with briefing and filters | `app-entry.json`, `employee-app-entry.png` |
| Role-scoped denial | The programme manager role gets 403 on `/api/admin/simulator-control`; `/api/audit-check` 200 | `prereq-run1.json` (`role_scoped_denial_probe`) |
| Wrong credential at Entra | Wrong password stays on Entra with the error shown and no app session (`/api/me` 302) | `prereq-run1.json`, `entra-wrong-password-denied.png` |
| Logout and account switching | `/.auth/logout` then `/api/me` 302 to Entra; `/sign-in` shows the Entra picker with a "Use another account" option (screenshot deleted, see scope) | `prereq-run1.json` (`after_logout`, `account_switch`) |
| Roster binding | `bound` is false: the account is admitted by Entra identity and app role, with no private roster | `prereq-run1.json` |
| Resident demo (`ca-resident-demo`) | Not re-run; see the first note: application-local shared demo sign-in, no staff surface | first note |

## Evidence limits

The redacted outputs, `prereq-run1.json` and two screenshots are retained. The Entra sign-in and logout/picker rows rest on boolean fields in `prereq-run1.json` alone, and the picker screenshot was deleted because it showed a display name; those two rows are observed; raw output not retained beyond those fields.

## Acceptance criteria

| # | Criterion | Demo status | Basis |
| --- | --- | --- | --- |
| 1 | Tenant owner identifies the single-tenant app, roles and credential, preserving other registrations | Partly proven | A working GUID registration, a vault-held credential and a granted app role claim exist. Who provisioned it, single-tenant audience and role definitions are unreadable with this login; no other registration was touched |
| 2 | Credential reaches the private vault by an approved in-VNet path; no secret or ID published; no networking weakened | Proven for the demo | Secret is a Key Vault reference through a user-assigned identity; the vault is public-disabled with an approved private endpoint; nothing published; this run did not alter networking. The secret value was not read |
| 3 | API auth and audience use that registration; edge callback added with `--public-url`, prior callbacks preserved | Partly proven | Client ID, issuer, tenant and audiences are consistent and the callback works end to end. The registration's redirect URI list and the `initialize-api-auth.py` run history are unreadable, so preservation of prior callbacks is unproven |
| 4 | Private staff roster reconciled in the VNet, replicas reloaded, no fictional identity or email fallback | Unproven, not applicable to the demo | `bound` is false; the demo admits by Entra identity and role. A roster is a real-staff feature and no owner-supplied roster exists |
| 5 | Real user completes callback and session, role-scoped `/api/me`, workbench entry; logout, account switching, wrong-role and unknown-staff denial | Proven with the test account only | Callback, `/api/me`, `/app`, logout, picker, wrong-password denial and a role-scoped 403 are retained. A real person, a second-role account and unknown-staff denial are unavailable for the demo |
| 6 | Anonymous 401 and forged-header denial in browser mode, plus a positive authenticated request | Proven with a qualification | Browser mode answers anonymous and forged requests with 302 to Entra, XHR 403, bad bearer 401, never 200; the authenticated `/api/cases` is 200 and forged headers do not change a session. A literal 401 for browser-style requests does not occur by design |

## Open items

* A tenant owner with Application Administrator rights must read or confirm
  the registration (audience, roles, redirect URIs, assignment requirement)
  and supply any real-staff roster and a second-role account to close
  criteria 1, 3, 4 and 5 beyond the demo.
* The issue stays open: criteria 1, 3, 4 are not fully proven and criterion 5
  is limited to the test account. None is ticked from this evidence.

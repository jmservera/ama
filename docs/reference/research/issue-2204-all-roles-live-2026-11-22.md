---
title: All ZavaForward App Roles Signed In Live, One at a Time (Issue 2204)
description: Live Entra and Playwright proof for each of the 13 ZavaForward.* app roles assigned one at a time to the demo test account through Microsoft Graph, with permitted views, a wrong-role denial per role, restoration of the original assignment and a per-criterion table
author: AMA programme
ms.date: 2026-11-22
ms.topic: reference
---

## Scope and authority

Owner decisions of 2026-11-18: synthetic demo, desktop only, live Azure authorised (resource
group `ama`, cap USD 700, no drills, no Key Vault rotation, no production change). The
existing `az` login now holds Graph `AppRoleAssignment.ReadWrite.All`. This note extends the
[2026-11-21 note](./issue-2204-role-signin-wrong-role-denial-live-2026-11-21.md), which could
show only the Programme Manager live.

Method (`live_all_roles.py`, in `.copilot-tracking/evidence/2026-11-22/issue-2204-live/`):

* Resolve the service principal `zava-forward-api` (the app behind `ca-cutover-test-demo-api`) and its 13 app roles through `az rest`.
* Record the account's original assignment on that service principal: `ZavaForward.ProgrammeManager` only. An unrelated assignment on another application (`proper-warm-api`) was never touched.
* Remove it, then for each role: assign that one role, confirm through Graph it is the only one held, sign in with Playwright Chromium (1366 by 900, fresh context), read `/api/me`, probe data routes and the administrator-only simulator control, screenshot the workbench and `/app#/simulator`, then delete the assignment and confirm none remains.
* A `finally` block restores `ProgrammeManager`; the final Graph read shows exactly that role (`final-assignments.txt`).
* Credentials were read from the owner's files at run time and never printed. A literal scan of every retained evidence file for each credential value found no match (observed). Screenshots mask email addresses and hide the account chip.

Run on 2026-11-22 from about 10:20 UTC. Only transient role assignments were created, all removed.

## Observed finding about the run

A first full pass was interrupted by the tool timeout while `RuleOwner` was assigned; the
original assignment was restored by hand through Graph before the next pass. In the second
pass Entra issued a token carrying the previous role for three sign-ins (SafetyLiaison,
GrantsOfficer and SupportOfficer returned the preceding role claim). The script now waits 20
seconds after assignment, checks that `app_roles` equals the assigned role, and retries after
45 seconds. Those three roles and the five that were refused were rerun under that check, and
the table uses the verified results. Role claim propagation after an assignment is therefore
not instant; a role-change demo needs a short wait or a fresh sign-in.

## Per-role result

`only held` and `removed` were true for all 13 roles. "Nav" is the number of navigation
entries from `/api/me`.

| App role | Sign-in | Application role | Nav | Data routes (cases, stats, finance, packages, funding, audit check) | Wrong-role denial |
| --- | --- | --- | --- | --- | --- |
| ProgrammeManager | 200 | Retrofit Programme Manager | 13 | 200 all | simulator control 403; browser denial page |
| Coordinator | 200 | Retrofit Coordinator | 10 | finance 403; others 200 | same |
| LiaisonOfficer | 200 | Resident Liaison Officer | 10 | finance 403; others 200 | same |
| SafetyLiaison | 200 | Building Safety Liaison | 9 | finance 403; others 200 | same |
| QualityInspector | 200 | Quality Inspector | 9 | finance 403; others 200 | same |
| GrantsOfficer | 200 | Grants and Evidence Officer | 10 | 200 all | same |
| SupportOfficer | 200 | Programme Support Officer | 13 | 200 all | same |
| ApplicationAdmin | 200 | Application Administrator, `app_admin` true | 14, all 14 flagged "needs a role with this authority" | 403 all; simulator control 200 | cases and finance 403 for the administrator |
| Contractor | 401 "Please sign in." | none | 0 | 401 all | "Account not authorised" page |
| RuleAuthor | 401 | none | 0 | 401 all | "Account not authorised" page |
| RuleOwner | 401 | none | 0 | 401 all | "Account not authorised" page |
| RegulatoryChat | 401 | none | 0 | 401 all | "Account not authorised" page |
| AIRestart | 401 | none | 0 | 401 all | "Account not authorised" page |

Reading of the table:

* The eight roles that sign in match the local matrix of the previous note: finance is refused to the Coordinator, Liaison, Safety and Quality roles and open to Grants, Support and Programme Manager; every non-administrator is refused the simulator control (403, browser page "Nothing was changed").
* The administrator alone sees every navigation entry, each flagged as needing a role with this authority, and the server returns no business data (403) but permits simulator control (200). This is the designed "sees every option, reads no data" boundary, not a defect.
* The Contractor role alone is refused (401), consistent with the local matrix where a contractor claim without a roster company binding is refused. The four capability roles (RuleAuthor, RuleOwner, RegulatoryChat, AIRestart) are refused alone, consistent with the local rule that a principal with no staff role is refused; the live run did not test them on top of a staff role.
* `/api/work-orders` returned 403 for every signed-in staff role, including roles the local matrix allows, so the path was probably wrong in this probe (default deny for unknown routes); work orders are not claimed. `/api/retention` returned 200 for the Programme Manager on 2026-11-21 but 500 here, and 403 for the other roles; the 500 is unexplained and routed as a follow-up.

Screenshots (`live-<Role>-workbench.png`, `live-<Role>-denied-simulator.png`) and the machine
record `live-all-roles.json` are in the evidence folder.

## Acceptance criteria

| # | Criterion | Status for the demo | Basis |
| --- | --- | --- | --- |
| 1 | Each role signs in and sees only its permitted views; admin sees all | Proven live for the eight roles that sign in alone, including the administrator; proven refused for the five that do not | Table above. Contractor with a roster binding and capability roles combined with a staff role were not run live |
| 2 | One wrong-role denial shown; no credentials printed or stored | Proven | Each role has a recorded denial; credential literal scan found no match; screenshots mask the account |
| 3 | Evidence recorded | Proven | This note, the evidence folder and the changes record |

Whether to tick criterion 1 is the owner's decision: it depends on accepting the refused-alone
results for the Contractor and the four capability roles.

## Follow-ups

* Investigate the `/api/retention` 500 for the Programme Manager.
* Run live combinations: a staff role with each capability role, and the Contractor with a roster binding.
* Add a short propagation wait to any live role-change demo script.

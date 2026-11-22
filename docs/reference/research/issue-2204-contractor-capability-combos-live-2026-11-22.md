---
title: Contractor Roster Binding and Capability Roles Stacked on a Staff Role, Live (Issue 2204)
description: Live Entra, Azure SQL and Playwright proof for the Contractor with a roster binding and for each capability role stacked on the Programme Manager, with restoration and a per-criterion table
author: AMA programme
ms.date: 2026-11-22
ms.topic: reference
---

## Scope and authority

Owner decisions of 2026-11-18 apply: synthetic demo, desktop only, live Azure authorised (resource group `ama`, cap USD 700, no drills, no Key Vault rotation, no production change). This note closes the two cases left open by the [all-roles note](./issue-2204-all-roles-live-2026-11-22.md). The script and machine records are in [the evidence folder](./issue-2204-contractor-capability-combos-live-2026-11-22/live_combos.py) (`live-combos.json`; `live-combos-pass1.json` is the first pass, before error text was recorded).

## Roster path (code and Azure SQL)

* `identity.bind` accepts a Contractor only with exactly one enabled roster row matching tenant id and object id, `role` Contractor and a non-empty `contractor` company; otherwise the sign-in is refused.
* In-network read (`az containerapp exec` on `ca-cutover-test-demo-api`, managed identity to Azure SQL `retrofit`): the `staff` table held 2 rows. Kat Larsson already has a Contractor row for `Northern Facade Systems Ltd` with the app tenant id and her own Entra object id, and 316 cases carry that company. She also holds `ZavaForward.Contractor` on the service principal. The binding the owner expected is in place and needed no change; her row was not touched.
* I have no credential for Kat's account, so her own sign-in is not driven here. The path was proven with the test account instead (below). Why she was reported unauthorised earlier cannot be established from the available replica logs, which held no `auth denied` lines.

## Contractor with a roster binding, live

A temporary synthetic row (`Temp Contractor 2204`, company `Northern Facade Systems Ltd`, the test account's object id) was inserted in Azure SQL, ProgrammeManager was swapped for Contractor, and the account signed in with Playwright (1366 by 900). Entra served the previous role claim for the first sign-ins, so the script retried until the claim matched (attempt 4).

| Check | Result |
| --- | --- |
| Sign-in | 200, role Contractor, 2 navigation entries (My jobs, Specialist screens) |
| Views | "Your jobs", "Assigned jobs", "Your work orders" ([screenshot](./issue-2204-contractor-capability-combos-live-2026-11-22/live-Contractor-bound-workbench.png)) |
| Data routes | cases 200, work orders 200; stats 403, finance 403, simulator control 403, regulatory chat 403 |
| Row removed | `staff` back to 2 rows after the run |

The same role without a binding was refused (401) in the all-roles run, so the binding is what admits the Contractor.

## Capability roles stacked on ProgrammeManager, live

Each capability was added to ProgrammeManager one at a time (Graph showed exactly the two roles each time); a ProgrammeManager-only baseline ran first.

| Assignment | Sign-in | `rule_roles` in `/api/me` | Staff views | Observed capability gate |
| --- | --- | --- | --- | --- |
| ProgrammeManager only | 200, 13 navigation entries | none | cases, stats, finance 200 | regulatory chat status 403: "A separately assigned RegulatoryChat capability is required." |
| plus RuleAuthor | 200 | `rule_author` | unchanged | not separable (see below) |
| plus RuleOwner | 200 | `rule_owner` | unchanged | not separable (see below) |
| plus RegulatoryChat | 200 | `regulatory_chat` | unchanged | status moves from the capability refusal to 403 "restricted to an enabled synthetic-demo dataset", a later gate ([screenshot](./issue-2204-contractor-capability-combos-live-2026-11-22/live-PM+RegulatoryChat-workbench.png)) |
| plus AIRestart | 200 | `ai_restart` | unchanged | not separable (see below) |

Findings:

* Every capability is accepted on top of a staff role and appears only in `rule_roles`; it adds no navigation and changes no staff view. The simulator control stays 403 throughout. Alone, each capability was refused in the all-roles run.
* RegulatoryChat is the only one with a non-mutating live discriminator, and it shows the capability gate passing. The next refusal is the demo dataset gate, so no regulatory answer was shown.
* The RuleAuthor and RuleOwner write routes returned 403 with an empty body for the Programme Manager with and without the capability, and the law store reports "not loaded" (503) on this deployment, so a rule action cannot run live. AIRestart needs an open suspension with a proposal and every refusal is a 403; a drill is not permitted. For these three only the claim reaching the application is proven, not a permitted action.

## Restoration

After each run the script removed every assignment and re-added ProgrammeManager; the final Graph read shows `only_pm` true. The temporary roster row is deleted (2 rows). An unrelated assignment on another application was not touched. A scan of every evidence file for the credential values found no match.

## Acceptance criteria

| # | Criterion | Status for the demo | Basis |
| --- | --- | --- | --- |
| 1 | Each role signs in and sees only its permitted views; admin sees all | Proven for 8 staff roles and admin (all-roles note) and refused alone for 5; Contractor with a binding proven here; the four capability roles proven to sign in on a staff role with the claim present. Not proven: a permitted action for RuleAuthor, RuleOwner and AIRestart (law store not loaded; no drill) and Kat Larsson's own sign-in (no credential) | Tables above |
| 2 | One wrong-role denial shown; no credentials printed or stored | Proven | Simulator control 403 for every non-administrator; credential scan found no match |
| 3 | Evidence recorded | Proven | This note and the evidence folder |

Whether to tick criterion 1 is the owner's decision.

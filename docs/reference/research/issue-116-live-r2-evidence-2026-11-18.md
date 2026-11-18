---
title: Entra Roles and Field-Level Visibility Live Demo Evidence, Round 2 (Issue 116)
description: Second live pass on the deployed synthetic demo for the unticked criteria of issue 116, with a reason-value leak scan across exports and AI surfaces and the reason a second role cannot be signed in
author: AMA programme
ms.date: 2026-11-18
ms.topic: reference
---

## Scope and authority

Owner decisions of 2026-11-18 apply: synthetic demo, desktop only, live Azure
authorised in resource group `ama` (cap USD 700, no drills, no Key Vault
rotation, no production change). DPO and Legal approval, billing
reconciliation and person-run assistive-technology testing are not needed for
the demo. No source file, Azure resource, setting or secret was changed or
created, so nothing needs deleting. Credentials were read from the owner's
files at run time and never printed; a literal scan of every retained round 2
file for the account name and password found no match.

This round adds to the [round 1 record](./issue-116-live-demo-evidence-2026-11-18.md).
Target `ca-cutover-test-demo-api`, Playwright Chromium 1366 by 900, 2026-11-18
about 13:50 UTC. Evidence is under
`.copilot-tracking/evidence/2026-11-18/issue-116-live-r2/` (scripts, JSON,
no screenshot retained).

## Observations

| Observation | Result | Evidence |
| --- | --- | --- |
| Signed-in identity | Entra sign-in, `Retrofit Programme Manager`, app role `ZavaForward.ProgrammeManager`, `view_only` false, provider `trusted-proxy` | `probe_r2b.json` |
| Second role | Not obtainable. `az ad app show` and `az ad sp list` return insufficient privileges, so no app role can be read, no throwaway user created and no role assigned; the resident test account is not an Entra tenant user (see [sign-in note](./entra-signin-live-demo-2026-11-18.md)) | az output, this session |
| Reason values present | 16 cases; 4 distinct reason strings plus boolean forms in `resident.adjustment` and `resident.priority_support` (values not retained) | `probe_r2b.json` |
| Reason role sees the reason where entitled | Case detail (200) carries both keys for the reason role | `probe_r2.json` |
| Reason values on other surfaces | Literal hit counts for all 4 distinct strings: 0 in the case CSV, proposals, proposals CSV, AI report, assistants, audit check and RAI metrics | `probe_r2b.json` |
| Export headers | Case CSV columns: Reference, Resident, Address, Town, Postcode, Phone, Stage, Status, Owner, Days in stage, Last contact, Next visit; no reason column | `probe_r2.json` |
| Proposals | Now non-empty (round 1 saw none); the word `reason` appears only as release, denial and ranking vocabulary, with no case reason value | `probe_r2.json`, `probe_r2b.json` |
| Signed-in workbench | `/app` shows the briefing, rules-derived summary and an AI-suggestions choice (observed during the run; the screenshot is not retained because it showed resident names) | Not retained |

## Acceptance criteria

| # | Criterion | Status for the demo | Basis |
| --- | --- | --- | --- |
| 1 | Roles allowed to see a vulnerability reason confirmed (OD-14, OD-19) | Unproven; box stays unticked | Live enforcement shown for the one reason role and no leak to exports. Denial for non-reason and contractor roles cannot be shown live (no second sign-in, no directory privilege). "Confirmed" means a named human approval of the matrix, which the owner excluded for the demo |
| 2 | Allowlists and size limits at every provider boundary | Unproven live | Unchanged from round 1: only unknown-task refusal (400) is reachable; payload content is not exposed by the deployed app; offline spies remain the evidence |
| 3 | Permissions rechecked on outputs, citations, explanations, errors, review records and exports | Partly proven | For the single reason role, the stored proposals now present give zero reason-value hits in outputs, exports and report. No second role comparison, no new model call, so errors and citations for other roles are not shown |
| 4 | Document AI requires derivative or scoped necessity exception | Unproven live | No uploaded document in the demo; upload would change state |

## Adverse and limits

* The first parse of `/api/me` in `probe_r2.json` shows null role fields because
  the fields sit under `user`; `probe_r2b.json` corrects it and both are kept.
* Zero literal hits proves absence of the four exact strings, not of every
  paraphrase.
* Independent review and hosted CI are outstanding; no box is ticked.

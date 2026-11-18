---
title: Entra Roles and Field-Level Visibility Live Demo Evidence, Round 3 (Issue 116)
description: Third live pass on the deployed synthetic demo for the four unticked criteria of issue 116, with a full read-only endpoint sweep for one reason role and a re-run of the offline role, provider-spy and document tests
author: AMA programme
ms.date: 2026-11-18
ms.topic: reference
---

## Scope and authority

Owner decisions of 2026-11-18 apply: synthetic demo, desktop only, live Azure
authorised in resource group `ama` (cap USD 700, no drills, no Key Vault
rotation, no production change). DPO and Legal approval, billing
reconciliation and person-run assistive-technology testing are not needed for
the demo. Sign-in credentials were read from the owner's files at run time and
never printed. No source file, Azure resource, setting or secret was changed or
created, so there was nothing to delete. All live calls were GET requests plus
one refused POST (unknown AI task).

This round extends [round 1](./issue-116-live-demo-evidence-2026-11-18.md) and
[round 2](./issue-116-live-r2-evidence-2026-11-18.md). Target
`ca-cutover-test-demo-api`, Playwright Chromium 1366 by 900, 2026-11-18 about
17:30 UTC. Evidence is under
`.copilot-tracking/evidence/2026-11-18/issue-116-live-r3/`.

## Observations

| Observation | Result | Evidence |
| --- | --- | --- |
| Signed-in identity | Entra, `Retrofit Programme Manager`, app role `ZavaForward.ProgrammeManager`, `view_only` false | `probe_r3.json` |
| Cases visible | 50 (round 2 saw 16) | `probe_r3.json` |
| Endpoint sweep | All 88 GET paths from the repo role inventory (`test_role_endpoint_inventory.py`): 60 return 200, 6 return 403 (handoffs unowned and escalated, cohort and held-out evaluation, aftercare form, an unknown path), 6 return 404, 9 return 503 (law watch and sources, account photo), 7 return 500 (handoffs unaccepted, time status and reports) | `probe_r3.json` |
| Reason values across the sweep | 3 distinct reason strings in case detail (Communication support, Interpreter, Large print): 0 literal hits in any of the 88 responses, including the 2 MB continuity export, the data-protection page, the case CSV and the choice-queue CSV | `probe_r3.json` |
| Unknown AI task | `POST /api/cases/{id}/ai` with an unknown task returns 400 `Unknown request.` before any provider call | `probe_r3.json` |
| Offline tests, re-run | core: `test_ai_provider_payload_spy`, `test_data_protection`, `test_ai_input_bounds`, 52 tests OK. api: `test_role_matrix`, `test_role_endpoint_inventory`, `test_document_controls`, 57 tests OK | `offline-core-tests.txt`, `offline-api-tests.txt` |

## Adverse and corrective evidence

* The first sweep (`probe_r3-first-with-None-false-positives.json`) counted the
  fourth reason value, the word `None`, and reported 379 hits on five
  endpoints. Context extraction (`probe_r3b.json`) showed every hit is the
  ordinary word in unrelated fields ("None known", "None recorded"), not a
  reason value. The sweep was re-run without that value; both files are kept.
* Seven endpoints return 500 for this role (handoffs unaccepted, time status,
  mine, report and their CSVs) and nine return 503. They are separate from
  the visibility criteria and are not investigated here; they stay a
  follow-up for the demo owner.
* Zero literal hits shows absence of the three exact strings, not of
  paraphrases.
* The single available account holds one role. A role comparison, the
  contractor view and a role outside the reason set cannot be signed in live;
  directory privileges are missing (round 2) and the resident test account is
  not an Entra user.

## Acceptance criteria

| # | Criterion | Status for the demo | Basis |
| --- | --- | --- | --- |
| 1 | Roles allowed to see a vulnerability reason confirmed (OD-14, OD-19) | Unproven; box stays unticked | Enforcement for the reason role is shown again (entitled in case detail, absent everywhere else). Denial for other roles rests on the offline matrix (57 tests OK). "Confirmed" is a named human approval of the matrix, which the owner excluded for the demo; OD-14 and OD-19 are open decisions in the BRD |
| 2 | Allowlists and size limits at every provider boundary | Unproven live; offline evidence only | Only the unknown-task refusal is reachable live. The provider-spy and input-bound tests pass offline (52 OK); live payload contents are not exposed |
| 3 | Permissions rechecked on outputs, citations, explanations, errors, review records and exports | Partly proven | 88 outputs and exports for one role carry no reason value; error responses (403, 404, 500, 503) carry no case data. Other roles are not shown live |
| 4 | Document AI requires derivative or scoped necessity exception | Unproven live | The demo has no uploaded document and uploading would change state; `test_document_controls` passes offline |

No acceptance box is ticked. Independent review and hosted CI remain outstanding.

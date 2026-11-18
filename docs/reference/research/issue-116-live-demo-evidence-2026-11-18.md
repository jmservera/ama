---
title: Entra Roles and Field-Level Visibility Live Demo Evidence (Issue 116)
description: Per-criterion record of the four unticked criteria of issue 116 on the deployed synthetic demo, with what was proven, what was not and why
author: AMA programme
ms.date: 2026-11-18
ms.topic: reference
---

## Scope and authority

Owner decisions of 2026-11-18: this is the synthetic demo, desktop only. Live
Azure was authorised (resource group `ama`, cap USD 700, no drills, no Key
Vault rotation, no production change). Azure billing reconciliation, DPO and
Legal approval and person-run assistive-technology testing are not needed for
the demo. No source file changed. No Azure resource, setting or secret was
created or changed, so nothing needs deleting. Credentials were read from the
owner's files at run time and never printed; a literal scan of every retained
evidence file for the employee account name and password found no match.

Target: `ca-cutover-test-demo-api` (Easy Auth with Entra). Browser: Playwright
Chromium, 1366 by 900 viewport, 2026-11-18 about 09:55 to 10:05 UTC. One
employee account was available, with the role `Retrofit Programme Manager`; a
second role could not be signed in, so the live role comparison is limited to
that role. The resident test account is not an Entra tenant user (see the
[sign-in note](./entra-signin-live-demo-2026-11-18.md)).

Evidence files are under `.copilot-tracking/evidence/2026-11-18/issue-116-live/`.

## Observations

| Observation | Result | Evidence |
| --- | --- | --- |
| Signed-in role | `Retrofit Programme Manager`; services `cases`, `assistants` true, `photo`, `law_alerts` false | `probe2.json` |
| Configured reason roles | `ZF_REASON_ROLES` is not among the app's environment variable names, so the code default applies: Resident Liaison Officer, Building Safety Liaison, Retrofit Programme Manager (`projection.DEFAULT_REASON_ROLES`) | `az containerapp show` env names; `src/core/.../projection.py` |
| Case list and detail for a reason role | `/api/cases` 200 with 16 items; the case detail carries `resident.adjustment` and `resident.priority_support`, consistent with a reason role seeing the reason | `probe2.json` |
| Assistant, RAI, audit and export surfaces for that role | `/api/assistants`, `/proposals`, `/rai-metrics`, `/api/audit-check`, `/api/cases.csv` return 200; the case CSV header has no reason column; the proposals list and CSV are empty; the audit check returns counts only | `probe2.json` |
| AI report | `/api/ai/report` 200; its text mentions "reason", "adjustment" and "vulnerab" only as metric and policy vocabulary (keys such as `owned_alerts.reason`), not as case data | `probe2.json` |
| Unknown or missing AI task | `POST /api/cases/{id}/ai` with an unknown or missing task returns 400 `Unknown request.` before any provider call; an unknown case returns 404 | `probe5.json` |
| Document AI hold | Not exercised: no non-generated (uploaded) document exists in the 16 demo cases, and uploading one would change demo state | `probe5.json` (`nongenerated_documents` 0) |
| Offline provider spies and document hold, re-run | `test_ai_provider_payload_spy`, `test_data_protection`, `test_ai_input_bounds` (core): 52 tests OK. `test_document_controls`, `test_assistants` (api): 157 tests OK, 60 skipped | `offline-core-tests.txt`, `offline-api-tests.txt` |

## Adverse and corrective evidence

* The first probe (`probe1.json`) reported zero cases because it read the wrong
  response shape (`items`, not a bare list); it is kept, and `probe2.json`
  replaces it.
* A login callback timed out once at 60 seconds (`probe2-attempt1-login-timeout.err`)
  and passed on retry.
* The first refusal probes used the Playwright request context and received an
  empty HTTP 403 for every POST, with and without the `X-ZF-CSRF` header. The
  same call from inside the signed-in page returned the application's own 400,
  so the 403 is a property of the out-of-page request path (the Easy Auth edge
  answers before the app), not an application result. Those two scripts and
  outputs were deleted before the in-page script `probe5.py` replaced them;
  this paragraph is the only record.
* `workbench.png` shows the public landing page (`/` is an unauthenticated path), not a signed-in screen; the signed-in proof is the JSON.
* The 60 skipped API tests are not counted as passes. Their skip reasons were
  not inspected here.

## Acceptance criteria

| # | Criterion | Status for the demo | Basis |
| --- | --- | --- | --- |
| 1 | Roles allowed to see a vulnerability reason confirmed (OD-14, OD-19) | Partly proven: enforcement shown; confirmation not proven | The deployed service applies the default reason-role set, and the one available role in that set sees `resident.adjustment`. Roles outside the set and the contractor view could not be signed in live; their denial rests on the offline role matrix tests. "Confirmed" means DPO, Legal and control-owner approval of the matrix, which the owner excluded for the demo; the 2026-10-08 owner direction is a design baseline, not ratification. The box stays unticked |
| 2 | Approved task and field allowlists and size limits at every provider boundary | Unproven live | A live call can only show refusals before a provider call, and only the unknown-task refusal was reachable (400). Exact-payload evidence needs the request body sent to the provider, which the deployed app does not expose; the offline spies cover it (52 core tests OK) for the paths they implement. Approved processing manifests, retained legacy families, reactive and proactive scans are not shown as covered |
| 3 | Permissions rechecked on outputs, citations, explanations, errors, review records and exports | Partly observed, unproven | One role was read through case detail, assistants, proposals (empty), the case CSV, the AI report and the audit check without a reason leak outside the reason role's entitlement. No second role was compared, the proposal list is empty so no stored output or citation was inspected, and no AI call was made, so no model output was available to check |
| 4 | Document AI requires the approved derivative or scoped necessity exception; storage and manual reading remain | Unproven live | The demo holds no uploaded document, and upload changes state. The hold logic (`data_protection.document_model_hold`) and its API tests passed offline; no deployed refusal was observed |

## What would close these criteria

* A second and third demo account in non-reason and contractor roles, so a
  live response comparison can be made.
* One owner-approved synthetic uploaded document and a recorded model-hold
  response with and without a derivative.
* One bounded, owner-authorised live assistant call to inspect a stored
  output, its citations and the review record.
* A named human decision on the reason-role matrix, if the programme ever
  moves beyond the demo.

None of these changes the code. The four boxes stay unticked.

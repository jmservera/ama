---
title: Assisted Form Workspace Live Demo Evidence (Issue 96)
description: Per-criterion record of issue 96 on the deployed synthetic demo, covering the one unticked criterion (approved versioned schemas), what was observed and why it cannot be proven
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
created or changed, so nothing needs deleting, and no synthetic record was
written (the probe used GET requests only). Credentials were read from the
owner's files at run time and never printed.

Target: `ca-cutover-test-demo-api`, revision `0000031`, Easy Auth with Entra.
Browser: Playwright Chromium, 1366 by 900 viewport, 2026-11-18 about 13:51
UTC. The one available employee account has the role `Retrofit Programme
Manager`. Evidence files are under
`.copilot-tracking/evidence/2026-11-18/issue-96-live/`.

## Observations

| Observation | Result | Evidence |
| --- | --- | --- |
| Signed-in role | `Retrofit Programme Manager`; 16 demo cases visible | `probe1.json` |
| Registered form schemas | `GET /api/form-schemas` returns 200 with `{"schemas": []}`; the CSV export is empty | `probe1.json`, `form-schemas-response.png` |
| Staged candidates for one case | `form-candidates` returns 200 with no batches | `probe1.json` |
| Working reviews for the same case | `form-review` returns 200 with no drafts and no holds, and the notice "Unapproved working notes only. Not a reviewed application or claim pack; no eligibility, approval, submission, award, payment or cash is established." | `probe1.json` |
| Schema registration path | `forms.register_schema` always records `approval` `Unapproved`, no approval evidence and source policy `Unapproved`; versions are immutable and only the next version can be added. No source path writes `Approved`. | `src/core/src/zava_forward/core/forms.py` lines 355 to 389 |
| Use of approval downstream | `form_validation._approval_gaps` reports a gap unless a human-recorded approval with evidence is bound to the exact schema digest; validation then reports Not evaluated | `src/core/src/zava_forward/core/form_validation.py` |
| Offline tests re-run | `test_form_staging`, `test_form_review`, `test_form_dependencies`, `test_form_export`, `test_form_criteria_5_6` (core): 67 tests OK | `offline-core-tests.txt` |

## Adverse and corrective evidence

* `probe.py` also saved a landing-page screenshot; it was deleted because it
  adds no proof. The signed-in proof is the JSON and `form-schemas-response.png`.
* This note repeats the earlier
  [form schema approval check](./issue-96-live-form-schema-approval-evidence-2026-11-18.md),
  which reached the same result but kept no raw output. The raw probe output
  and test run are retained here.
* The demo holds no schema, so the assisted form workspace and pack assembly
  could not be exercised end to end live. The five ticked criteria rest on
  the earlier offline and review evidence cited in the issue and on the 67
  tests above; they were not re-proven on the deployed demo.
* A throwaway schema was deliberately not registered. The registry is
  append-only with no delete route, so the record could not be cleaned, and it
  could only read `Unapproved`.

## Acceptance criteria

| # | Criterion | Status for the demo | Basis |
| --- | --- | --- | --- |
| 1 | Each assisted form has an approved versioned schema | Unproven, stays unticked | The deployed demo has zero registered schemas. The code can register versioned schemas but never marks one `Approved`; approval of a template and its source policy is a named human decision recorded outside the engineering path. |
| 2 | Candidate values carry raw value, source ID, document hash and locator | Ticked earlier; not re-proven live | No candidate batch exists in the demo; offline `test_form_staging` passes. |
| 3 | Accept, correct or reject per field preserves prior values and reviewer | Ticked earlier; not re-proven live | No draft exists in the demo; offline `test_form_review` passes. |
| 4 | Validation reports field-specific unknown, conflict or fail | Ticked earlier; not re-proven live | Offline tests only (`test_form_criteria_5_6`). |
| 5 | A reviewed export never submits or implies eligibility | Ticked earlier; not re-proven live | The live notice states no eligibility, submission or payment is established; offline `test_form_export` passes. |
| 6 | A source, schema or rule change marks only the dependent proposals and approvals stale | Ticked earlier; not re-proven live | Offline `test_form_dependencies` passes. |

## Not proven

* Criterion 1 needs a named human to approve at least one schema version and
  its source policy, plus a code path or recorded process that stores that
  approval against the digest. Neither exists, so it cannot be proven for the
  demo. Seeding an approved synthetic schema would be a source change and a
  claim of approval the programme has not made.

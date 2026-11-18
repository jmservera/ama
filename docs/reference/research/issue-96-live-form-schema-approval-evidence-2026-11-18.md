---
title: Live form schema approval evidence for issue 96 (demo)
description: Recorded check on 2026-11-18 of the one unticked criterion in issue 96 on the live demo, with per-criterion status
author: AMA RPI agent
ms.date: 2026-11-18
ms.topic: reference
keywords:
  - issue 96
  - form schema
  - approval
estimated_reading_time: 3
---

Refs #96. Scope is the synthetic desktop demo under the owner decisions of 2026-11-18 (resource group `ama`, cap USD 700, no drills, no Key Vault rotation, no production change). Production-only approvals stay deferred to #1905 to #1908. Nothing here is production evidence.

## Method

* Live: Entra sign-in to `ca-cutover-test-demo-api` with the employee test account (credentials read at run time, never printed; the driver asserts that neither value appears in its output), Playwright Chromium at 1366 by 900. `GET /api/form-schemas` and `/api/form-schemas.csv` were read. Driver and output (the screenshot was removed because it could show the account name) are in `.copilot-tracking/evidence/2026-11-18/issue-96-live/`.
* Repository: 67 focused `src/core` tests (`test_form_staging`, `test_form_dependencies`, `test_form_export`, `test_form_review`, `test_form_criteria_5_6`) passed.
* No Azure resource was created, changed or deleted, and no demo data was written.

## Observations

| Observation | Result |
| --- | --- |
| `GET /api/form-schemas` as the signed-in employee | 200, `{"schemas": []}` |
| `GET /api/form-schemas.csv` | 200, empty (no rows) |
| `forms.register_schema` (`src/core/.../forms.py`) | Stores every new version as `approval="Unapproved"`, `approval_evidence=None`, `source_policy_status="Unapproved"`; versions must be consecutive and are immutable |
| Any code path that sets `approval` to `Approved` | None found in `src/*/src`; `form_validation._approval_gaps` only reads it and reports "The registered template schema has no recorded approval." |

## Per-criterion result

| Criterion in #96 | Result for the demo | Evidence and limit |
| --- | --- | --- |
| Each assisted form has an approved versioned schema | Unproven, and cannot be proven for the demo | The demo holds no registered schema at all. Versioning is implemented and tested, but approval needs a recorded named approver and evidence (Finance, Legal or programme owner) and no shipped path records one. Registering a throwaway schema would only yield `Unapproved`, and a synthetic approval would not meet the criterion. Production-only; deferred to #1905 to #1908. |
| Candidate values carry raw value, source ID, document hash and locator | Offline only (already ticked) | `test_form_staging` passes; no live candidates exist because no schema is registered. |
| Accept, correct or reject per field preserves prior values and reviewer | Offline only (already ticked) | `test_form_review` passes; not exercised live. |
| Validation reports field-specific unknown, conflict or fail | Offline only (already ticked) | Rule tests pass; not exercised live. |
| A reviewed export never submits or implies eligibility | Offline only (already ticked) | `test_form_export` passes; no live export is possible without a schema. |
| A source, schema or rule change marks only dependent items stale | Offline only (already ticked) | `test_form_dependencies` passes; not exercised live. |

## What this does not prove

* Any approval of a schema, template or source policy, which is a human act.
* Live behaviour of staging, review, validation, export or stale marking, because the demo has no schema and a live write was out of scope for a docs-only run.

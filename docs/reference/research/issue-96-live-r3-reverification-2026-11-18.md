---
title: Issue 96 live re-verification, run 3 (demo)
description: Third recorded check on 2026-11-18 of the one unticked criterion in issue 96, with retained raw output and a per-criterion table
author: AMA RPI agent
ms.date: 2026-11-18
ms.topic: reference
keywords:
  - issue 96
  - form schema
  - approval
estimated_reading_time: 3
---

Refs #96. Scope is the synthetic desktop demo under the owner decisions of 2026-11-18 (resource group `ama`, cap USD 700, no drills, no Key Vault rotation, no production change). This run repeats the [first](./issue-96-live-demo-evidence-2026-11-18.md) and [second](./issue-96-live-form-schema-approval-evidence-2026-11-18.md) records and keeps the raw output those earlier runs lacked. Nothing here is production evidence.

## Method

* Live: Entra sign-in to `ca-cutover-test-demo-api` as the employee test account (role Retrofit Programme Manager), credentials read at run time and asserted absent from the saved output, Playwright Chromium at 1366 by 900. Two GET requests only. Nothing was written, and no Azure resource was created or changed.
* Repository at `eba446c9e`: a search of `src/*/src` for approval writes, and six focused `src/core` test modules.
* Retained under `.copilot-tracking/evidence/2026-11-18/issue-96-live-r3/`: `probe.py`, `probe.json`, `form-schemas-response.png` (a JSON page only), `approval-search.txt`, `core-tests.txt`.

## Observations

| Observation | Result |
| --- | --- |
| `GET /api/form-schemas` | 200, `{"schemas": []}` |
| `GET /api/form-schemas.csv` | 200, empty body |
| Search for `approval` with `Approved` in `src/*/src` | Three hits, all reads in `form_validation.py` (lines 170, 218, 232) |
| Write route for schemas | `POST /api/form-schemas` calls `forms.register_schema`, which stores each version as `Unapproved` with no approval evidence |
| Focused core tests | 79 passed (`test_form_staging`, `test_form_dependencies`, `test_form_export`, `test_form_review`, `test_form_criteria_5_6`, `test_issue_98_field_validation`) |

A throwaway live registration was not attempted: no delete route exists, so it could not be removed, and it could only produce an `Unapproved` row.

## Per-criterion result

| Criterion in #96 | Result for the demo | Evidence and limit |
| --- | --- | --- |
| Each assisted form has an approved versioned schema | Unproven; cannot be proven for the demo | The demo holds no registered schema. Approval needs a named human (Finance, Legal or programme owner) with recorded evidence, and no shipped path records one. A synthetic approval would not meet the criterion. Production-only; deferred to #1905 to #1908. |
| Candidate values carry raw value, source ID, document hash and locator | Offline only | `test_form_staging` passes; no live candidates exist. |
| Accept, correct or reject per field preserves prior values and reviewer | Offline only | `test_form_review` passes; not exercised live. |
| Validation reports field-specific unknown, conflict or fail | Offline only | `test_issue_98_field_validation` passes; not exercised live. |
| A reviewed export never submits or implies eligibility | Offline only | `test_form_export` passes; no live export without a schema. |
| A source, schema or rule change marks only dependent items stale | Offline only | `test_form_dependencies` and `test_form_criteria_5_6` pass; not exercised live. |

## Limits

* No criterion is ticked. Independent exact-head review and hosted CI are outstanding.
* The live probe shows one moment on one revision; it says nothing about production.
* Approval of a schema, template or source policy is a human act that this record does not perform or imply.

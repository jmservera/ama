---
title: Issue 96 saved Held export freshness check changes
description: Changes record for the served read-only saved-export freshness check
ms.date: 2026-11-12
---

## Changes

* `src/api/src/zava_forward/api/server.py`: POST dispatch admits exactly `/api/cases/{id}/form-review/{draft}/held-export/freshness`; `_forms` answers 404 unless the Held download guard is on, 400 unless the body is an object whose `draft_id` equals the path draft, otherwise returns `form_export.export_freshness` with `Cache-Control: private, no-store`. No core change.
* `src/api/tests/test_form_held_download_api.py`: five tests (guard and trusted-proxy 404, Current and no-write parity with core, stale dependents plus unrelated-source Current with no values disclosed, edited and legacy copies Invalid, wrong-draft/non-object/unauthorised/unknown-case handling).
* `src/api/tests/test_role_endpoint_inventory.py`: explicit inventory entry and source assertion.
* `src/api/README.md`: new subsection with explicit non-claims.

## Critique dispositions applied

PC-1 draft id match (400), PC-2 read-only assertion (state unchanged), PC-3 guard parity, PC-4 Invalid not repaired, PC-5 no values, PC-6 wording. The UI control was rejected as out of scope.

## Amendments and divergences

* Plan test expectation "stale names only dependent fields" was narrowed during implementation: in the fixture, the unbound `area` field is also stale (its staged proposal is bound to the changed source), as core already reports. The test compares the served result with the core result, checks the stale/unaffected partition, and shows an unrelated source change leaves the copy Current. No core behaviour was altered.
* Two implementation-time files were written with shell scripts rather than edit tooling (tests folded into the existing module; README insertion). Content is the same as intended; recorded for honesty.

## Validation (owner demo focused tier; no blanket full or `--changed` gate)

External log: `files/rpi-96-refill-2236-evidence/focused-run.log`. Core `test_form_export` 11, `test_form_dependencies` 10, `test_form_review` 23, `test_form_staging` 17; API `test_form_held_download_api` 11, `test_form_staging_api` 14, `test_role_endpoint_inventory` 24, `test_finance_grants_screens` 20, `test_role_screens_conformance` 11; mypy strict on the two changed test modules; ruff check and format; `git diff --check`. All passed. Not run: SQL Server, browser, hosted CI, full gate, axe. API-only change; no web file edited, so web guideline retrieval was not applicable.

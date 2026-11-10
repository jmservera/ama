---
title: Issue 131 case-local expected-household inventory primitive details
ms.date: 2026-11-10
task_id: 131-household-inventory-1110
---

## P1 Action and strict input (`resident_decisions.py`)

* Add `tenure_inventory_record` to `RESIDENT_ACTIONS` and `INTAKE_ACTIONS`; add `tenure_household_inventories` to `RESIDENT_FIELDS` and `INTAKE_FIELDS`; add derived `tenure_inventory_view` to `INTAKE_FIELDS` only.
* Constants: `INVENTORY_MAX_ROWS = 100` (transport safety, not policy), `INVENTORY_QUALIFICATION` text stating caller supplied, completeness, identity and authority not verified, no release.
* `_res_tenure_inventory_record`: `_intake_fields` exact keys `case_id, expected_version, source, source_version, owner, next_update, households`; existing inventory field must be a list; `_version` on the latest inventory; text bounds via `_intake_text`; owner via `_intake_owner`; `_day` for `next_update`; households `None` records Unknown; otherwise a non-empty list of at most 100 exact-key rows (`household_ref`, `report_version`).
* Row validation: ref a string, non-blank, at most 100, no surrounding whitespace, unique by `casefold`; `report_version` `None` or an exact non-bool positive int pointing to an existing report whose `household_ref` equals the ref and which is the latest report for that ref; digest `_digest(report)` stored server-side.
* Append `dict(version, case_id, source, source_version, owner, next_update, households, status, qualification, recorded_by, at)`; set `tenure_review_required=True`; audit detail carries counts and the version only.

## P2 View and consumers

* `tenure_inventory_view(case)`: pure, never mutates. Returns status (`Missing`, `Unknown`, `Declared`, `Malformed`), inventory version, expected count or `Unknown`, per-ref linkage and binding (`Not linked`, `Current`, `Stale: report changed`, `Stale: newer report for this reference`, `Missing report`) with stored verification, identity state, route and open-trigger count, counts, reasons and the qualification and `release` text. No readiness or approval boolean.
* Reasons are counts-only strings. Any exception while reading a persisted inventory yields `Malformed`.
* `followup_view` adds the view to a managed case only (inventory field present, tenure flag or reports, or malformed reports).
* `_inventory_gate_reasons(case)`: empty unless the inventory field is present; otherwise the view reasons. `resident_gate` returns `reasons + [TENURE_HOLD]` when managed; `_res_scope_record` raises `ValueError` with the same joined text before appending any scope.

## P3 Tests

* Core (`JsonResidentDecisions`, inherited by `SqlResidentDecisions`): revision append and reopen with no read mutation and server digest; strict errors with unchanged case and audit; exact two-household one-missing-link refusal at `resident_gate` and `scope_record`; stale after a new same-ref report, verification, trigger; hold never released with synthetic verified and approved-pack inputs; legacy unmanaged unchanged; malformed persisted field fails closed while hazard and manual routes stay available; deletion retains the flag and removes new data; canaries absent from gate text and from withheld-role details; SQL competing writer and report-version race; committed-unconfirmed outcome.
* API (`test_resident_api.py`): actual POST to `/api/cases/ZF-1/resident` accepts the action, returns strict 400 and 409, `scope_record` refusal before and after full links, and canaries absent for a restricted reader and a contractor.

## P4 Docs

* Core and API README: add a short bounded section on caller-supplied inventory, Unknown, snapshot digest, opt-in scope, no authority or release and residual C1 and C2 acceptance.

## P5 Validation

Targeted Core and API resident test files, `ruff check` and `ruff format --check` on touched Python files, `mypy` on the Core source, `git diff --check`, scoped diff review. No blanket gate.

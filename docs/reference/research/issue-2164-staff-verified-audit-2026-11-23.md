---
title: "Issue 2164 audit of other identity.verified staff paths (2026-11-23)"
description: Audit of every identity.verified caller for the bound-row scope gap closed in assistants.authorize, one gap fixed in sensor review drafts, with a per-criterion table.
ms.date: 2026-11-23
---

Scope: synthetic demo, desktop only. Source reads, a local probe and unit tests; no credentials were used and no Azure resource was created or changed. Refs #2164.

## Findings

* Roster scope fields (`case_ids`, `areas`) are read in two places only: `Assistants.authorize` (fixed for #2164 in 6a03928ccb) and `sensor_review_draft._gate`.
* `identity.bind` runs on every request (`api/server.py`, `_user`) and `identity.matches` skips disabled rows, so a revoked roster row produces an unbound principal on the next request.
* Every other `identity.verified` caller (`bulk_edits`, `forms`, `change_provenance`, `chat_isolation`, `chat_privacy`, `resident_decisions`, `coordinator`, `regulatory_chat`, `regulatory_privacy`, `simulator_admin`) consumes no roster scope, so the scope gap cannot occur there. `change_provenance` already re-resolves the bound row by tenant and object id.
* Gap: `sensor_review_draft._gate` looked up the roster row by the principal's email only. A probe showed a bound principal passed the gate when the row's object id belonged to someone else, and when the principal was `view_only`. Row `case_ids` scope was applied correctly while the object id matched.
* Fix: `_gate` now refuses a tampered or view-only Entra principal and requires the bound row's `oid` to equal the principal's and its `tid` to be empty or equal. Unbound Entra principals still fail closed, as before.

## Evidence

* `cd src/core; python3 -m unittest tests.test_sensor_review_draft`: 68 tests OK (23 skipped, SQL Server variants). Without the source change the new test `test_bound_entra_staff_inherit_the_roster_row` fails 10 subtests (JSON and SQLite: rebound oid, other tenant, missing oid, view-only, tampered binding).
* `src/api` tests `test_sensor_review_draft_api`, `test_sensor_non_authority_boundary` and `src/core` `test_sensor_non_authority`: OK.
* `python3 -m mypy` in `src/core`: 3 errors, all present before the change (missing opentelemetry stubs, unused ignore in `device_provision.py`). `ruff check` and `ruff format --check` pass on the changed files.

## Per-criterion table

| Criterion | Status | Basis |
| --- | --- | --- |
| Decide whether bound Entra staff inherit roster scope | Proven (assistants, sensor drafts) | Decision held in 6a03928ccb; sensor drafts now match |
| Test `view_only` with an eligible role | Proven | Assistants test on main; new sensor draft subtest `view-only` |
| Test scope bypass | Proven | `case scope` and `area scope` subtests; rebound-oid subtest |
| Live demo proof | Unproven | Sensor review drafts are default-off and need retained SQL consent and an approved rule; not served in the demo apps |

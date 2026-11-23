---
title: "Issue 2164 tenant binding of roster rows for bound Entra staff (2026-11-23)"
description: Assistants and sensor draft gates now apply the legacy-tenant rule when a bound Entra principal re-reads its roster row, with a per-criterion table.
ms.date: 2026-11-23
---

Scope: synthetic demo, desktop only. Source reads and local unit tests; no credentials, Azure call or roster edit. Refs #2164.

## Finding

* `identity.matches` binds a principal to a tenant-less roster row only when the store's legacy tenant equals the principal's tenant.
* `Assistants.authorize` and `sensor_review_draft._gate` re-read the bound row but accepted any tenant-less row for any tenant, so a forged or stale bound pointer could inherit a row from another tenant.
* Fix: `identity.row_tenant_ok` applies the same rule in both gates.

## Evidence

* New `test_bound_entra_forged_pointer_tenant_and_area_scope` (`src/api/tests/test_assistants.py`) fails without the fix and passes with it. `src/api` `test_assistants`, `test_entra_authoritative`, `test_auth`, `test_sensor_review_draft_api` and `src/core` `test_sensor_review_draft` pass; ruff is clean; mypy shows only 3 pre-existing errors.

## Per-criterion table

| Criterion | Status | Basis |
| --- | --- | --- |
| Decide whether bound Entra staff inherit roster scope | Proven | decision in 6a03928ccb; tenant binding tightened here |
| Test `view_only` with an eligible role | Proven | `test_unbound_and_view_only_entra_principals` |
| Test scope bypass | Proven | new test and the existing bound scope test |
| Live behaviour with a restricted roster row | Unproven | needs a live roster edit, excluded for the demo |

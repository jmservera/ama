---
title: Plan for issue 80 round 5
description: Form-schema catalogue CSV export
ms.date: 2026-11-05
---

## Phases

* [x] Phase 1: `/api/form-schemas.csv` in `LIST_EXPORTS`, `EXPORT_KINDS` (kind `forms`) and `list_rows` with a seven-field whitelist over `forms.list_schemas`.
* [x] Phase 2: tests in `test_form_staging_api.py` (rows, denial, revocation and reason-view, formula cell, empty, no case data), registry and role inventory.
* [x] Phase 3: API README.

Details: [phase details](../details/2026-11-05-excel-transition-80-r5-schema-catalogue-details.md).

## Critique (one pass, direct)

Verdict: proceed. Reuse `list_schemas` unchanged so authorization, stale-cache and revocation checks stay authoritative; reuse `to_csv`; no new helper beyond the field tuple. Compatible advice applied; nothing conflicts with a confirmed decision.

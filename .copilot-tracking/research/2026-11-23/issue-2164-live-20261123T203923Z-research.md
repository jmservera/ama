---
title: Research for issue 2164 live r11
ms.date: 2026-11-23
---

## Disposition

Research executed (new angle). Planning Readiness: Ready.

## Prior coverage read

* r10 changes and research (tenant binding), staff-verified audit (sensor draft gate), deployed-code proof, roster-scope recheck.
* All earlier workers covered `Assistants.authorize` and `sensor_review_draft._gate`.

## New finding

* `Assistants._authorize_challenge_staff` (assistants.py) is a third reader of roster `case_ids` and `areas`. It looks the row up by the principal's email only, with no Entra checks.
* Unlike `authorize` and `_gate`, it accepts a `view_only` or tampered Entra principal, a row whose `oid` is another person's, and a row of another tenant (or a tenant-less row without a matching legacy tenant), provided the email matches.
* Normal requests are protected by `identity.bind`; the gap matters for a forged or stale bound pointer, the same class closed for the other two gates.

## Criteria status

| Criterion | Evidence |
| --- | --- |
| Decide inheritance | Decided earlier (6a03928ccb) |
| Test view_only with eligible role | `test_unbound_and_view_only_entra_principals` (authorize); challenge path untested |
| Test scope bypass | authorize and sensor gate covered; challenge gate to add |
| Live restricted roster row | Not provable without a live roster edit; challenge route is not served by an Entra-bound demo account |

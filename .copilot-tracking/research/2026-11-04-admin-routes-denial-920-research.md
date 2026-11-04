# Research: admin-only case-data routes (Refs #920)

Disposition: reused (research 2026-11-04 admin-landing-denial-920) plus a Chromium probe. Planning readiness: Ready.

## Already delivered

* PRs #929, #1017, #1061, #1006 (photo, law alerts, regulatory chat status, assistants, admin-only landing; strict mypy).

## Remaining gap (probed)

* An admin-only account (no case access) that opens a case-data route directly or from navigation received 403 and console errors: #/overview (/api/stats), #/visits, #/funding, #/coordinator (/api/facets, /api/coordinator), #/finance. Server returns 403 by design (expected denial, avoidable by not requesting).
* #/import and #/screens do not request case data and stay unchanged.

## Classification

* Expected denial: role has no case access. Plain-language state already exists ("No case work for this account"); reuse it. No authorisation change.

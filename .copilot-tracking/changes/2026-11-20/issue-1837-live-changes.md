---
title: Changes issue 1837 live
ms.date: 2026-11-20
---

Tier FOCUSED: test-only change, no src or workflow edit.

## Per-criterion status

| Criterion | Status | Evidence |
| --- | --- | --- |
| 1 failing-first browser regression, all three forms | Proven on current source (not failing-first: fix already on main) | `test_standalone_route_forms_submit_in_browser` passes; axe check statuses 200,200,200 |
| 2 valid submissions retain account, owner, provenance, records; JSON callers compatible | Proven | same test asserts owner, original account, correction source, challenge record |
| 3 negative tests | Built here: 401, 403 (contractor), malformed, stale version, bad id, bad date, cross-case; no write. Missing-CSRF header unproven (non trusted-proxy test provider) | new test; module 9 tests OK |
| 4 browser journeys with axe, zero unexpected skips | Partial: route-forms check passed, zero violations; `nomination_browser_check` fails at nomination_review (adverse, retained) | /tmp/axe1837 outputs |
| 5 independent exact-head review, hosted CI | Unproven: needs human/hosted run | none |
| 6 full-tier receipt | Not applicable here: no src change; full receipt not run by instruction | none |

## Validation

* `python3 -m unittest tests.test_nomination_api_routes -q` (src/api): 9 tests OK.
* ruff format/check on the test file: clean. mypy: 7 pre-existing errors in core `telemetry_support.py` (missing opentelemetry stub), none in changed file.

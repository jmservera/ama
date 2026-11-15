---
title: 82-c3 changes
ms.date: 2026-11-13
---

* `finance.py`: type-safe `_norm`; `_same` (strings only) for invoice matching; `identity_well_formed`; `_independent` looks up the registry only for `None`/`{}` identity and refuses malformed stored or acting identity with `PermissionError`.
* `grants.py`: `_complete` delegates to `identity_well_formed` (`oid` must be absent, `None` or `str`); `_malformed` gives an explicit "malformed" unknown reason.
* `gates.py`: `_reason`, `_text_items`, `_recorders` helpers; evidence, quality, booking, safety release, eligibility, authority, finance and capacity gates return pass/fail/unknown with a non-empty reason on malformed inputs.
* Tests: `test_gates.py::GateBoundaryTests`, `test_grant_lifecycle_controls.py` (falsey and truthy `oid`/`email`/`code` on all parties, end-to-end `grant_approve` on JSON and SQL), `test_finance_signoffs.py` (sign-off and invoice match).
* Failing-first confirmed: 8 failures and 17 errors in the new gate/grant tests and 22 failures plus 28 errors in finance/grant cases before the fix; all pass after.
* Validation (focused tier): core `test_gates*`, `test_grant*`, `test_finance*` pass; api `test_grant*`, `test_financ*` pass; ruff check and format check, core and api mypy clean. Full-suite run exceeded the time box and is not claimed.
* Deviation: rebased onto origin/main `c13d077d2`, which adds one chore commit over the requested `2489d839e` (an ancestor).

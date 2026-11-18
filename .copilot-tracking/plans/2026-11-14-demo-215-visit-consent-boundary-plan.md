# Plan: #215 visit consent boundary (2026-11-14)

* Add one sentence to the `_unblock` rules answer naming consent/access confirmation and independent safety sign-off, with no assumption of either.
* Add `src/api/tests/test_alert_chat_visit_consent_boundary_215.py`: API tests (rules answer, withheld unsupported drafts, refusals, zero case mutation over every answer path) and deterministic access-pending tests.
* Narrow the sibling `CLAIMS` regex from `consent` to `consented` so the new wording is not a false claim.
* Focused tier only: unittest, ruff check, ruff format --check, mypy.
* Critique (once): small product wording change is required to make the contract true; risk is existing tests pinning text, mitigated by running affected siblings. Applied directly. Refs #215.

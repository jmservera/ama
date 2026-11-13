# Plan: wire eligibility_gate (#82 F1)

* [ ] Add `ELIGIBILITY_OUTCOMES`, `grant_eligibility_verdict` and a Submitted-approval gate in `grants.py`; carry optional eligibility evidence in `pending`.
* [ ] Add tests in `test_grant_lifecycle_controls.py`: pass, fail, explicit unknown, legacy record unaffected.
* [ ] Run test_gates, test_grant, test_finance, test_workflows, ruff, mypy (core, api).

Process note: an early draft of the `grants.py` edit was made before research-open; it was reverted and is re-applied after Plan and Critique.

Details: `.copilot-tracking/details/2026-11-13/82-wire-eligibility-gate-1819-details.md`.

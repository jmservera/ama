# Plan: issue 145 live (2026-11-23)

Details: [details](../details/2026-11-23-issue-145-live-details.md). Tier: focused (test-only, no src, no workflow change).

* [ ] Add test comparing the runbook parameter table to the Bicep defaults and the pilot example
* [ ] Run `python3 -m unittest infra.tests.test_sql_tier`, ruff check and format check
* [ ] Changes record with criterion table; review; commit locally

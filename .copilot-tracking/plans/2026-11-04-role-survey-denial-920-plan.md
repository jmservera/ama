# Plan: role survey browser test (Refs #920)

* Phase 1: extend `src/api/checks/expected_denials_browser_check.py` with a per-role survey (all staff roles and Contractor): no 4xx response and no console error across navigation routes, a case route and #/assistants.
* Phase 2: focused validation (check run in Chromium, unit tests, ruff, mypy as src-ci), review, PR (Refs #920).

Critique: executed once, self-review; compatible. No application code, authorisation, security, infrastructure, SQL or deployment change. Details: [details](../details/2026-11-04-role-survey-denial-920-details.md).

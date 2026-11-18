---
title: Issue 349 live demo sign-in research
---

Task: issue-349-live. Refs #349. Date 2026-11-18. Disposition: executed. Planning Readiness: Ready.

Sources read: issue 349 body, `src/api/checks/employee_identity_check.py`, `employee_live_acceptance.py`, `resident_demo_browser_check.py`, cut-over evidence pack live employee acceptance (2026-11-02), Easy Auth 500 note (2026-11-03). Live evidence gathered with Playwright and read-only Azure CLI; outputs and findings are in [the research note](../../../docs/reference/research/entra-signin-live-demo-2026-11-18.md).

Key findings: Entra sign-in, role-scoped /api/me, logout and anonymous 401 are provable on the demo with the test account; wrong-role inside the employee app is not (one staff account); tenant objects, vault path and roster are unreadable or absent, so criteria 1, 2 and 4 stay unproven. The resident test account is not an Entra user.

Note: evidence collection ran before the plan file was written; the plan records that order honestly.

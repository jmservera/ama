---
title: Plan for issue 73 live run (2026-11-19)
---

1. Add `src/api/tests/test_list_clocks_over_http_76.py`: real server, one hazard with `aware_at` and one safeguarding item; assert list rows and detail carry named-owner clocks for a safeguarding-visible role and none for Contractor.
2. Run it, mypy for `src/api`, ruff format check; record in changes.
3. Write research note with per-criterion table; commit.

Details: [details](../details/2026-11-19-issue-73-live-details.md). Critique: [critique](../critique/2026-11-19-issue-73-live-critique.md). Tier: FOCUSED (test only, no src change).

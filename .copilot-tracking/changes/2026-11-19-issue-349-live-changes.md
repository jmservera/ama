# Changes: issue-349-live
No source change (criterion 1 is tenant administration). Added evidence dir, research note r4, index and log entries. Validation tier FOCUSED: documentation link and diff review; no src code touched so mypy/ruff/tests not applicable.

| # | Criterion | Status |
| --- | --- | --- |
| 1 | Tenant app, roles, credential | Partly proven (Graph denied) |
| 2 | Credential in private vault | Proven for demo |
| 3 | Audience and callback; prior preserved | Partly proven; preservation unproven |
| 4 | Staff roster | Unproven, not applicable to demo |
| 5 | Real-user sign-in, logout, denial | Proven for test account only |
| 6 | Anonymous 401, forged denial, positive request | Proven with qualification |

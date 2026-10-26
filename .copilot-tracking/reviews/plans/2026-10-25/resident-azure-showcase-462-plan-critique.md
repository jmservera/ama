# Plan critique: synthetic resident Azure showcase (issue 462)

Date: 2026-10-25, executed once by an independent `rubber-duck` agent after the plan, phase details and research were written and before any implementation. Not repeated.

Execution: complete. Verdict: **REVISE** (2 high, 2 medium; no acceptance-criterion contradiction found).

| # | Severity | Location | Finding | Disposition |
| --- | --- | --- | --- | --- |
| 1 | High | Plan decision 9; details phases 3 and 4 | Base-table SELECT fallback grants raw JSON to the resident principal and relies on code filtering | Accepted. The database-owned allowlist view is mandatory and the fallback is removed. If approval or creation is impossible, deployment is blocked. Test that the resident principal cannot read `cases` or prohibited paths |
| 2 | High | Plan decision 4; acceptance evidence | In-memory logout revocation is lost on restart or scale to zero, so a pre-logout token revives | Accepted. Every token MAC covers a random per-process boot nonce, so any restart or scale-to-zero invalidates all sessions (re-login required) and cannot revive a logged-out token. Logout also adds in-process revocation for the live process. Restart-after-logout negative test added |
| 3 | Medium | Plan decision 2; cost and stop plan | Secret expiry "plus margin" can pass the authority window | Accepted. Expiry and scheduled cleanup are at or before 2026-10-26T12:00Z; any extension needs a new explicit owner authorisation before an expiry change |
| 4 | Medium | Plan cost and stop plan; details phase 1 step 5 and rollback | Cleanup authority and deletion verification for SQL principal, view and role assignments not planned; SQL objects cannot carry tags | Accepted. Gap G3 includes create and delete/revoke authority for every RBAC assignment, SQL principal and view; deterministic names are recorded; post-delete readback queries verify removal; no reliance on tags for SQL objects |

Original plan text is unchanged; amendments are appended to the plan and details as dated sections.

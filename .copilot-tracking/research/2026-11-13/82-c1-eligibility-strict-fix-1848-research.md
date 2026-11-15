# Research: #82 eligibility gate strict fix (F1, F2, F3)

Disposition: executed. Planning Readiness: Ready. Tier: Focused.

* Rebased a760d847e onto b630279b4 (clean, one commit).
* Source review: review-82-elig-1836 findings F1 (missing key bypasses gate), F2 (self-asserted proposer eligibility), F3 (stale Eligible survives Rejected).
* Code: `grants.py` `_grant_set_pending`, `_grant_approve`, `grant_eligibility_verdict`; roles in `controls.py` (`FINANCE_ROLES`); independence in `finance._independent`.
* Gap: eligibility rides on the proposal by the proposer; legacy key skipped; never cleared.

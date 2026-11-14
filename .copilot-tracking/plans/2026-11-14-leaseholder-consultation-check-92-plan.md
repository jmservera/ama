# Plan: leaseholder consultation check (#92)

* [x] Add `leaseholder_status()` (missing or invalid reads `unknown`, derived from history so it cannot be forged) and status-specific hold reasons.
* [x] Expose `leaseholder_consultation_status`, `letting_renewal_blocked`, `letting_renewal_reason` in `list_packages`; set on create and record; return in gate and audit detail.
* [x] Procurement screen shows status and the blocked letting or renewal reason.
* [x] Focused unit test; run `test_consultation_controls`, ruff, mypy only.
* Critique (single pass): keep the Legal-authority hold rather than letting `complete` unblock, consistent with existing tests and policy. Accepted.

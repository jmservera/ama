# Plan: issue 220 hazard referral ageing, 2026-11-03

* [x] Optional `received_on` on record_digital/record_staff, kept inside `hazard_referral` only.
* [x] Read-only `hazard_referrals_overdue(today, max_days=1)`; unknown age is flagged, not hidden.
* [x] Tests, README update.
* Critique: executed once (self); compatible, no clock/consent/refusal/sanction fields, human owner acts. Verdict: proceed.
* Stacked next: store/API/UI wiring (#130); human acceptance of criterion 5.
* Validation tier: focused (no security, infrastructure, SQL or deployment surface); gate not run.

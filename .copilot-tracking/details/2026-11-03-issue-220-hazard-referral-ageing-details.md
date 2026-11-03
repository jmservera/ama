# Details: issue 220 hazard referral ageing

* `challenges.py`: `received_on` ISO date validated; stored as `hazard_referral.received_on` (None when absent).
* `hazard_referrals_overdue` returns copies with `referral_age_days`; excludes handed-off referrals.
* Stacked on origin/feat/issue-218-rai-control-stack; PR base is that branch.

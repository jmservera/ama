# Review: issue 2206 (2026-11-21)

Executed once. Outcome: conformant for local scope; live counts criterion remains unproven.

* Read-only: run_az rejects argv without list/show/get-access-token; a test covers a delete attempt.
* Secrets: exceptions are reduced to class names; tests assert no leak.
* Residual: the runbook itself is not edited.

Routed follow-ups: (1) run counts from inside the private network (job with SQL access); (2) investigate job-live-receiver failures since 09:00Z.

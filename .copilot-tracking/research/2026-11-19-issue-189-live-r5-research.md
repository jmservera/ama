# Research r5: issue 189 first unmet criterion (2026-11-19)

Task: issue-189-live-r5. Disposition: executed (reuses r1-r4 evidence).

* Issue 189 has one unticked criterion: "Run has an owner, a time limit and a budget alert".
* Existing code: `live_control` (owner, approval, hard expiry, stop), `run_governance` (RunMeter), `run_live_check` (verifier).
* Prior notes prove each part separately; no live run showing owner + expiry halt on the demo hub; alert recipients are noreply.
* Known routed gap from r4 review: verifier selects the budget only by name `budget-<hub>`.
* Plan: fix that gap in code with tests; run a live governed run (throwaway job, deleted after) and record evidence.
* Planning readiness: Ready.

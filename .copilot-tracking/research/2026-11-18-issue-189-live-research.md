# Research: issue 189 live proof of run owner, time limit and budget alert

Date: 2026-11-18. Disposition: executed (extends 2026-11-14 research). Planning Readiness: Ready.

Scope: one unticked criterion, "Run has an owner, a time limit and a budget alert", on the synthetic demo, desktop only, no src changes, no drills, no Key Vault rotation.

Live read-only facts gathered 2026-11-18 (resource group ama):

* Budgets (az consumption budget list): budget-[hub] USD 25 monthly, notifications actual80 (>80 percent) and forecast100 (>100 percent), both enabled; budget-cutover-test and budget-forward-test USD 300 monthly, same two alerts.
* IoT Hub [hub]: Basic B1, 1 unit, Active; tag owner set.
* No job-live-simulator exists in ama (only manual cutover jobs), so no unattended run is possible; the simulator job template is authored but not deployed.

Code-path evidence (read-only, no src change):

* `PYTHONPATH=src:tests python3 -m unittest tests.test_simulator_run_controls_189 tests.test_simulator_run_budget_controls` in `src/core`: Ran 32 tests, OK.
* Deterministic run of `RunGovernance`/`RunMeter` (owner "Juan Manuel Servera", 30 minute limit, GBP 4 alert, GBP 5 cap): accumulated GBP 4.5 emitted one `budget_alert` event naming the owner; a further GBP 1 halted with `RUN_BUDGET_HALT`; a clock past 1800 s halted with `RUN_DEADLINE`; blank and `TBD` owners were refused with `RUN_OWNER_REQUIRED`.
* `infra/live-simulator-job.bicep` binds an owner/expiry/stop `control.json`, `replicaTimeout: 240` and a mandatory approval reference, but is not deployed.

Conclusions:

* Budget alert: proven live. Azure budget `budget-[hub]` (USD 25, alerts at 80 percent actual and 100 percent forecast, enabled, recipient set) covers the hub run cost.
* Owner: proven live by the hub `owner` tag and in code by the refusal of blank owners; the per-run owner lives in the unobserved `control.json`.
* Time limit: proven in code and unit tests; not provable live because no simulator job is deployed and deploying one (device registration, certificates, image push) is a production-affecting owner step outside this evidence-only task. Not needed for the demo.
* A live budget alert firing cannot be proven without spending to the threshold; the cap (USD 700) and "no drills" rule forbid it. Alert configuration is the provable fact.

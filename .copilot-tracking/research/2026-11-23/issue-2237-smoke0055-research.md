# Research: live smoke of API 0000055 and resident 0000027 (issue 2237)

Disposition: executed (existing probes reused as method). Planning Readiness: Ready.

* Revisions read via az: `ca-cutover-test-demo-api--0000055` and `ca-resident-demo--0000027` are Healthy at 100% traffic.
* Prior method: `docs/reference/research/issue-2202-demosmoke-2026-11-22/` (employee sign-in, map) and `issue-2202-finalproof-2026-11-22/probe_resident.py` (resident chart `[data-sensor-chart]` after Sensors tab).
* Issue 2237 criteria: reproduce, cause from logs, fix with regression test, re-prove 200 live. Issue 2257: map recovers/cause. Issue 2244: start-up lock crash-loop.
* No src change planned: tier focused.

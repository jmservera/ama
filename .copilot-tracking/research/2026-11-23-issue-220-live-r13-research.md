# Issue 220 r13 research (2026-11-23)

Refs #220. Synthetic desktop demo; owner decisions of 2026-11-18 apply.

## Scope

Only the fifth criterion is unticked: no retaliation, inferred refusal or delayed hazard response. The r12 run hardened the adverse-key guard in `challenges.py` and did not deploy it. Live revision `ca-cutover-test-demo-api--0000058` (created 2026-11-23T19:20Z) predates the r12 commit (19:33Z).

## Questions

* Does the live API on 0000058 still accept key variants such as `Retaliation_Flag` or `hazard-pause`?
* Is any further guard gap visible offline (nested keys, other separators)?

## Disposition

Research executed. Planning Readiness: Ready.

<!-- markdownlint-disable-file -->
# Critique: #74 buildingView observation plan (issue-74-building-observation-0420)

One independent rubber-duck execution, read-only, before any browser or server. Verdict Revise (6 blocking, 2 non-blocking). Not repeated.

| ID | Severity | Finding | Disposition |
| --- | --- | --- | --- |
| PC-001 | Blocking | checks imported from cwd, checkout not proven | Applied: runner cds to `src/api`; driver records whether the imported harness module is under that checkout |
| PC-002 | Blocking | isolation not enforced | Applied: exact `env -i` runner script with owned HOME/scratch/interpreter and preflight |
| PC-003 | Blocking | network monitor only recorded | Applied: context-wide route guard from before navigation; aborts non-loopback and post-sign-in non-safe methods and records bounded counts (a blocked write would be a visible failure) |
| PC-004 | Blocking | vacuous or duplicate sections | Applied: exactly one visible section per expected h2, tokens recorded only then |
| PC-005 | Blocking | home-only absence scope | Applied: home sentinels first recorded on the home view, then checked across the whole building main; conclusion limited to those sentinels |
| PC-006 | Blocking | cleanup escalation | Applied: runner starts the check in its own session, records the exact PID/PGID, enforces a timeout with TERM then KILL of that exact group only, then verifies it is gone |
| PC-007 | Non-blocking | unbounded error/response text | Applied: counts and integer statuses only |
| PC-008 | Non-blocking | port release race before server start | Not changed: the harness is reused unchanged; residual risk recorded; credentials are synthetic and no real data exists |

No conflict with a confirmed decision.

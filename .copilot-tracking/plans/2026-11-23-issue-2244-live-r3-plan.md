# Plan 2244 live r3 (2026-11-23)

Tier FULL (infra Bicep change affects deployment settings; no src code change planned). Local commit only.

## Phases

* [ ] P1 Raise the API StartUp failureThreshold from 40 to 80 in `infra/modules/containerapps.bicep`.
* [ ] P2 Update the pinned probe in `infra/tests/test_bicep_policy.py` and add a test that the StartUp window exceeds the worst-case retry budget computed from `LOCK_RETRY_*` and the 15 s lock timeout.
* [ ] P3 Run `infra` tests for probes and Bicep policy, `ruff check` and format on changed Python; compile Bicep.
* [ ] P4 Changes record with per-criterion table, review, commit.

## Critique (executed once, final candidate)

Verdict: compatible. Findings applied directly: (1) a 241 s window leaves under 60 s margin to the sum of both stores if each hit the worst case sequentially; accepted because the stores hit contention only while the same writer holds the lock and the test ceiling of 300 s forbids more; recorded as a residual risk. (2) Do not touch the resident-demo probe (separate app, no SQL). (3) Do not claim C4 proven; the live setting stays 121 s until the owner deploys.

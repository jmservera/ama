---
title: Issue 2206 demo preflight proof
description: Live and local evidence for the read-only demo preflight script, with a per-criterion verdict
ms.date: 2026-11-21
ms.topic: reference
---

Evidence for #2206 (Refs #2118). Synthetic demo, desktop only, resource group ama. The script is
[tools/demo_preflight.py](../../../tools/demo_preflight.py); tests are
[tools/test_demo_preflight.py](../../../tools/test_demo_preflight.py) (6 cases with fake az, HTTP
and SQL readers, no network).

## Live run, 2026-11-21T10:54Z (python3 tools/demo_preflight.py)

```text
Demo preflight, resource group ama, 2026-11-21T10:54:34Z

| Check | Result | Detail |
| --- | --- | --- |
| revisions ca-cutover-test-demo-api | PASS | ca-cutover-test-demo-api--0000039 Healthy/Running 100% |
| health ca-cutover-test-demo-api | PASS | GET /healthz 200 |
| revisions ca-resident-demo | PASS | ca-resident-demo--0000015 Healthy/RunningAtMaxScale 100% |
| health ca-resident-demo | PASS | GET /healthz 200 |
| job job-cutover-test-demo-load | UNAVAILABLE | no executions |
| job job-cutover-test-demo-audit | PASS | latest Succeeded at 2026-11-21T02:00:00+00:00 |
| job job-cutover-test-demo-orch | PASS | latest Succeeded at 2026-11-21T10:50:00+00:00 |
| job job-live-simulator | PASS | latest Succeeded at 2026-11-21T10:50:00+00:00 |
| job job-live-receiver | FAIL | latest Failed at 2026-11-21T10:30:00+00:00 |
| cohort and consent counts | UNAVAILABLE | SQL not reachable (ProgrammingError) |

Summary: 7 pass, 1 fail, 2 unavailable.
```

Only `az containerapp revision list`, `az containerapp show`, `az containerapp job execution list`,
`az account get-access-token` and GET /healthz are issued. The token is passed to the SQL driver and
never printed. Plain `--strict` exits 1 here because counts are unavailable and the receiver job fails.

## Criteria

| Criterion | Verdict | Basis |
| --- | --- | --- |
| Checks revisions, job statuses and health without printing secrets | Proven | Live output above; tests assert read-only argv, no token or exception text in output |
| Checks cohort and consent counts | Unproven live | SQL has public network access disabled; connection from this host is refused. The count logic is proven with a fake reader only; the live row reports UNAVAILABLE with the reason |
| Output usable as the runbook preflight record | Proven | Timestamped Markdown table with per-check PASS, FAIL or UNAVAILABLE and a summary line; the runbook is not edited here |

## Findings for the owner

* job-live-receiver: the last four executions (09:00 to 10:30Z) are Failed. The preflight surfaces this; cause not investigated here.
* job-cutover-test-demo-load has no executions (expected for an on-demand job; shown as unavailable).
* Counts need a runner inside the private network (for example a job with SQL access); this host cannot reach SQL.

## Round 2 evidence, 2026-11-21T22:5xZ

Live rerun of the script (revision 0000042 of the API, 0000018 of the resident app):

* Revisions and health PASS for the API. The resident app was ScaledToZero and the first /healthz timed out at 15 s, so the check reported FAIL. A manual curl minutes later returned 200 in 0.1 s, so this was a cold-start false failure and a real script defect. Fixed in `tools/demo_preflight.py`: a timeout is retried once with a 90 s limit and the detail says "cold start, retried"; a second timeout still fails. Covered by `test_health_cold_start_timeout_retries_once`.
* job-live-receiver: the executions list is now Running (22:30Z), Failed (22:00, 21:30, 20:30) and Succeeded (21:00, 20:00). The job runs `zava_forward.api.live_receiver --seconds 1500` every 30 minutes with a 1620 s replica timeout. The failure cause stays unproven: Log Analytics refuses queries from this host (NspValidationFailedError, workspace network perimeter).

### Counts proven live from inside the private network

SQL is unreachable from this host, so a read-only count was run in the API replica with `az containerapp exec` (a pty and a Python REPL fed through stdin; only one SELECT of `sensor_consumer_control.body`, nothing written, no connection string or token printed). The replica uses the app's own managed-identity connection (`zava_forward.core.mssqlstore.connection_string`, driver `mssql_python`). Output:

```text
controls 20 homes 20 {'declined': 10, 'granted': 10}
```

That matches the 20-home cohort with 10 granted and 10 declined consents (the mix set by `tools/demo_consent_mix.py`). The preflight script's own live count row still reports UNAVAILABLE from this host, because the script cannot reach SQL itself; the count logic and the in-network figure are both evidenced, but one unattended script run producing the figure is not.

## Criteria after round 2

| Criterion | Verdict | Basis |
| --- | --- | --- |
| Checks revisions, job statuses and health without printing secrets | Proven | Two live runs; cold-start false failure fixed and tested |
| Checks cohort and consent counts | Partly proven | Counts verified live in-network (20 homes, 10 granted, 10 declined) and logic tested; the script run from outside the network still reports UNAVAILABLE |
| Output usable as the runbook preflight record | Proven | Timestamped Markdown table with summary; not yet pasted into the runbook |

Still open: receiver failure cause (logs blocked) and running the script from a runner inside the network.

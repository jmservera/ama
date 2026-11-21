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

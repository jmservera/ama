Demo preflight, resource group ama, 2026-11-23T19:50:15Z

| Check | Result | Detail |
| --- | --- | --- |
| revisions ca-cutover-test-demo-api | PASS | ca-cutover-test-demo-api--0000058 Healthy/Running 100% |
| health ca-cutover-test-demo-api | PASS | GET /healthz 200 |
| revisions ca-resident-demo | PASS | ca-resident-demo--0000028 Healthy/RunningAtMaxScale 100% |
| health ca-resident-demo | PASS | GET /healthz 200 |
| job job-cutover-test-demo-load | UNAVAILABLE | no executions |
| job job-cutover-test-demo-audit | PASS | latest Succeeded at 2026-11-23T02:00:00+00:00 |
| job job-cutover-test-demo-orch | PASS | latest Succeeded at 2026-11-23T19:45:00+00:00 |
| job job-live-simulator | PASS | latest Succeeded at 2026-11-23T19:45:00+00:00 |
| job job-live-receiver | PASS | latest Running at 2026-11-23T19:30:00+00:00 |
| hardening ca-cutover-test-demo-api | PASS | ZF_CONTAINER_HARDENING enforced |
| hardening ca-resident-demo | PASS | ZF_CONTAINER_HARDENING enforced |
| hardening ca-cutover-test-demo-agents | PASS | ZF_CONTAINER_HARDENING enforced |
| hardening job-live-simulator | PASS | ZF_CONTAINER_HARDENING enforced |
| hardening job-live-receiver | PASS | ZF_CONTAINER_HARDENING enforced |
| cohort and consent counts | UNAVAILABLE | SQL not reachable (ProgrammingError) |

Summary: 13 pass, 0 fail, 2 unavailable.

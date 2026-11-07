# Plan: issue 144 queue adapter (2026-11-04)

Research: [research](../../research/2026-11-04-issue-144-queue-adapter-research.md). Details: [details](../../details/2026-11-04/issue-144-queue-adapter-details.md). Continues [slice 1](issue-144-worker-run-loop-plan.md).

* [x] Slice 2 (this PR): `queue_azure.AzureTaskQueue` (receive, ack, release, poison after 5 deliveries or malformed), https-only endpoint, no redirects, tests.
* [ ] Slice 3: managed-identity token source, API post-back `ResultSink` with fence and release re-validation, `serve` wiring (security-sensitive; complete gate).
* [ ] Slice 4: orchestrator job entrypoint; hosted load run, rollout and restore proof (owner Azure access).

Validation: focused tier. The slice touches queue transport credentials handling (security-adjacent); the complete gate is left to the coordinator.

Critique (single pass): proceed. Applied: bearer token only over https origin, redirects refused, poison copy written before delete, 404 on ack or release treated as an expired lease.

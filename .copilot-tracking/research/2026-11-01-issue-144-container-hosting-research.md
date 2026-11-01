# Research: issue 144 container hosting completeness (2026-11-01)

Research disposition: executed. Planning Readiness: Ready (scoped slice).

## Question

Which #144 acceptance criteria remain unmet on `origin/main` (efebfc6d), and what is the smallest demo-ready slice that proves some of them without Azure access?

## Evidence

* `infra/modules/containerapps.bicep`: API has Liveness/Readiness `/healthz` probes, 0.5 vCPU/1 GiB, `activeRevisionsMode: Single`, http scale rule (50 concurrent requests), min 0 (default) to max 4 replicas. Agents app has a queue scale rule (0 to 5, `queueLength` 5) and no probes (no ingress). Orchestrator, ledger-verify, import and token jobs have timeouts/retry limits.
* `src/agents/src/zava_forward/agents/__main__.py` and `src/orchestrator/src/zava_forward/orchestrator/__main__.py` only print a version. `dispatch.py` states the queue transport and API post-back belong to #144; the API has no worker claim/post-back endpoint and `azure-storage-queue` is not in the agents requirements. Real queue-worker transport is a cross-project feature, not a slice.
* `src/*/Dockerfile` build real, digest-pinned, non-root (UID 10001) images; `src-deploy.yml` builds, scans, SBOMs, publishes run-versioned digests and deploys through `infra/scripts/pipeline.py`. `src/check-container.py` enforces read-only, cap-drop and no-new-privileges in CI only.
* `infra/README.md` (hosted hardening, checked 2026-10-16): Container Apps schema exposes no `readOnlyRootFilesystem`, capability-drop or `securityContext`; hosted hardening stays Partial.
* PRD `NFR-002` scale dimension: separately generated fictional 60,000-home/600,000-event fixture, twenty sessions, five requests/s for thirty minutes, no inference per home, report bounded query behaviour, no production autoscaling or availability claim. Staff thresholds: list/detail 1 s, dashboard 3 s.
* `src/core/tests/test_sqlreads.py` already generates a deterministic 60,000-case fixture (`make_cases`); `test_queue_benchmark.py` measures SQL-store pages only, not the HTTP API. No recorded API load test exists.
* Ledger tests cover tamper and digest checks but no restart/reopen persistence of audit entries.
* `docs/reference/resources/ai-tokenomics.md` and the issue require cost drivers per unit of load with Unknown cost when no price source exists.

## Criteria status on main

| Criterion | Status |
| --- | --- |
| Worker and job images real and deployed via pipeline | Images and pipeline real; worker entrypoints are version-printing placeholders. Unmet |
| Scale rules, probes, limits, rollback defined and tested | Rules exist; no contract test for scale/limits/probes, no startup probe, no rollback definition. Addressable |
| Hardening enforced in deployed app | Platform cannot express it. Blocked, remains Partial |
| Load test against declared fixture, recorded | Not run. Addressable locally (single process, honest scope) |
| Single-replica and restart behaviour with audit persistence | Not tested. Addressable locally |
| Tokenomics: cost drivers per unit of load | Addressable in the load report |

## Conclusion

Deliver: (1) API-level scale load harness plus a recorded 60,000-home run with cost drivers, (2) restart/audit persistence test, (3) startup probe, compiled contract tests for scale, probes, limits and Single-revision mode, and a documented rollback by digest redeploy. Worker transport and hosted hardening stay unmet, so the PR must use `Refs #144`.

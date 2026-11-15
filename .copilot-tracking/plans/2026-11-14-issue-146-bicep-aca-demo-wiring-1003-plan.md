# Plan: Bicep Container Apps demo wiring contract (2026-11-14)

Research: [research](../research/2026-11-14/2026-11-14-issue-146-bicep-aca-demo-wiring-1003-research.md)

* [x] Add infra/tests/test_bicep_containerapp_demo_wiring.py: text-based contract, strict annotations, no Bicep change.
* [x] Cover identity/registry/AZURE_CLIENT_ID per workload, secret hygiene, AI default-off gating, chat demo gating, telemetry, orchestrator/agents API wiring, IoT job identities.
* [x] Validate with unittest (PYTHONDONTWRITEBYTECODE=1), ruff check and ruff format --check.
* [x] Commit locally with Co-authored-by trailer; do not push.

Critique (single pass): compatible finding applied directly; the test must not fail on new workloads silently, so an unknown-workload assertion was added. No significant or divergent issue.
Tier: focused (test-only, no workflow, deployment or Bicep change).

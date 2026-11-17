<!-- markdownlint-disable-file -->
# Plan: deploy current-main resident showcase to Azure (issue 462)

Date: 2026-11-17. Task: resident-showcase-azure-deploy-462. Tier: FULL (coordinator runs the gate).
Research: .copilot-tracking/research/2026-11-17/resident-showcase-azure-deploy-462-research.md
Details: .copilot-tracking/details/2026-11-17/resident-showcase-azure-deploy-462-phase-details.md
Critique: .copilot-tracking/reviews/plans/2026-11-17/resident-showcase-azure-deploy-462-plan-critique.md

## Phases

* [x] P01 Admission record: current resources, accrued spend, remaining cap, finite resource plan, stop conditions.
* [x] P02 Build and push: local build from `src/` with `Dockerfile.resident-demo` at HEAD, push by digest inside a trapped registry window.
* [x] P03 Deploy: `az containerapp update` image-only to the digest; no other setting changes; verify revision Healthy.
* [x] P04 Live verification: real HTTPS browser run with the synthetic test user, correct-case data, negative paths.
* [x] P05 Close: restore ingress and registry state as found or documented, 0 replicas, record evidence, docs, commit.

## Stop conditions

* Headroom unknown or above cap, any unexpected resource, replica minimum above 0, registry state not restored.
* No SQL, secret, role, tenant, SQL S0, employee app or other resource group change.
* No push, PR or merge by this worker.

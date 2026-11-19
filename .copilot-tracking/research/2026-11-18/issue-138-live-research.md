---
title: Issue 138 live CI/CD OIDC research
ms.date: 2026-11-18
---

## Scope

Prove issue #138 criteria against the demo resource group `ama`, read-only. Disposition: executed.
Planning Readiness: Ready.

## Evidence

Full findings and the per-criterion table are in
[docs/reference/research/issue-138-live-cicd-oidc-evidence-2026-11-18.md](../../../docs/reference/research/issue-138-live-cicd-oidc-evidence-2026-11-18.md).

* Workflows active; infra-plan runs all skipped (variable unset); src-deploy never run; no OIDC variables, no release/deploy environments, no runner.
* Entra app listing denied; managed identities have no federated credentials.
* Live what-if of the real template succeeded; smoke checks pass against the demo API; fail-closed environment gate refuses.

## Decisions

* No workflow or source edit (FULL tier would apply); evidence-only documentation change.
* Making the criteria pass requires repository-admin and Entra changes outside the brief.

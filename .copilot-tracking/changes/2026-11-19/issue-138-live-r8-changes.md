---
title: Issue 138 live r8 changes
ms.date: 2026-11-19
---

Only these `.copilot-tracking/` records were added. No source, test, doc or Azure/GitHub change. Tier: FOCUSED;
mypy, ruff and unit tests not applicable (no code touched).

| Criterion | Status | Reason |
| --- | --- | --- |
| OIDC federated credentials per environment | Unproven | 0 federated credentials on 6 identities; no `AZURE_*` variables |
| what-if on infra PRs, result attached | Unproven | 0 runners; no run produced a summary |
| Approval per environment, same templates | Unproven | 0 protection rules on all environments; 0 deploy runs |
| Versioned image built, pushed, referenced | Unproven | 0 `src-deploy.yml` runs |
| Post-deployment checks fail the run | Unproven | Offline tests only; no pipeline run |
| No secret in logs or repository | Unproven | No live log audit possible without a run |

Owner action needed: create protected environments, Entra federation, and a runner.

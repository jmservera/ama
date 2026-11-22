---
title: Issue 138 r11 changes record
ms.date: 2026-11-22
---

Tier: focused (documentation and evidence only; no src, workflow or infra change). Planned checks: `check-repo-secrets.py` and its tests, `infra/tests/test_pipeline*.py`, live smoke, link and diff review. Hosted CI for this head was not observed because nothing is pushed.

## Files

* docs/reference/research/issue-138-live-r11-2026-11-22.md and its evidence folder (new)
* docs/reference/README.md, docs/reference/log.md (index and log entry)

## Per-criterion proven or unproven

| Criterion | Status | Reason |
| --- | --- | --- |
| 1 OIDC federated credentials per environment | Unproven | None exist; needs owner Entra setup |
| 2 what-if on infra PRs, result attached | Unproven | Workflow skipped (variable unset, no runner); no PR run possible without pushing |
| 3 approval per environment, same templates | Unproven | 0 protection rules; `dev`, `test`, `pilot` absent |
| 4 versioned image built, pushed, referenced | Unproven | No release run; needs runner and approval |
| 5 post-deployment checks fail the run | Unproven as a pipeline run; logic proven live | Smoke passes on the live demo API and raises on an unreachable one |
| 6 no secret in logs or repository | Repository proven; logs unproven | 0 findings; no hosted run logs exist |

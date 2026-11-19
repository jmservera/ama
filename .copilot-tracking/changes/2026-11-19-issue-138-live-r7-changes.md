---
title: Issue 138 live r7 changes
ms.date: 2026-11-19
---

Refs #138. Documentation only; no src, workflow or setting change. Tier: focused (docs). Not run:
`rpi-checks.py --all`, mypy, ruff (no Python changes).

## Files

* docs/reference/research/issue-138-live-r7-2026-11-19.md and its evidence folder
* docs/reference/README.md (index), docs/reference/log.md (entry)

## Validation

* Read-only `gh api` and `az` queries recorded in the evidence folder; no resource created.
* Link review and `git diff --check`: see review.

## Per-criterion result

| Criterion | Result |
| --- | --- |
| OIDC federated credentials per environment | Unproven (0 credentials on 6 identities; owner Entra/GitHub work) |
| What-if on infra PRs, result attached | Unproven (100 of 100 runs skipped; 0 runners) |
| Approval per environment, same templates | Unproven (0 protection rules; 0 deploy runs) |
| Versioned image built, pushed, referenced | Unproven (no pipeline run) |
| Post-deployment checks automatic, fail closed | Unproven (no pipeline run; offline tests only) |
| No secret in logs or repository | Unproven (no live run log audit) |

Stop line: every remaining criterion needs an owner action or a pushed run; no code to build.

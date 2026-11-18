---
title: Issue 138 live r4 changes
ms.date: 2026-11-18
---

Refs #138. Documentation only; no src, workflow or setting change. Tier: focused (docs). Not run:
`rpi-checks.py --all` (not required), no mypy/ruff (no Python changes).

## Files

* docs/reference/research/issue-138-live-r4-2026-11-18.md and its evidence folder
* docs/reference/README.md (index), docs/reference/log.md (entry)

## Validation

* `python3 -m unittest discover -s infra/tests -p 'test_pipeline*.py'`: OK
* Live `pipeline.smoke` passes; unreachable host fails with expected HTTP 200
* What-if: Succeeded; temporary parameter file deleted; no resource created
* Link review and `git diff --check`: see review

## Per-criterion result

| Criterion | Result |
| --- | --- |
| OIDC federated credentials per environment | Unproven (0 federated credentials; owner settings and Entra privilege) |
| What-if on infra PRs, result attached | Unproven (PR job never ran; no runner, gate unset) |
| Approval per environment, same templates | Unproven (no reviewers, 0 deploy runs) |
| Versioned image built, pushed, referenced | Unproven (no pipeline run; private registry) |
| Post-deployment checks automatic, fail closed | Partly proven (logic live; not inside a run) |
| No secret in logs or repository | Partly proven (tree and one log clean; no live run audit) |

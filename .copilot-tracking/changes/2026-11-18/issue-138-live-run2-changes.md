---
title: Issue 138 run 2 changes
ms.date: 2026-11-18
---

Documentation and evidence only; no source, workflow, GitHub setting or Azure change. Focused tier.

## Files

* Added docs/reference/research/issue-138-live-cicd-pipeline-run2-evidence-2026-11-18.md
* Updated docs/reference/README.md (index) and docs/reference/log.md (append-only entry)
* Added run2 research, plan, details, critique, changes, review under .copilot-tracking; state file rewritten (first-run versions remain in git history and the first-run research file was restored)

## Per-criterion result

| Criterion | Result | Reason |
| --- | --- | --- |
| OIDC federated credentials per environment | Unproven | No AZURE_* variables, no environments, 0 federated credentials, Entra app registrations unreadable |
| what-if on infra PRs, result attached | Partly proven (mechanism only) | Live what-if Succeeded (99 Create, 15 Modify, 81 Ignore, 14 Unsupported, 0 Delete); PR job never ran, attachment unobserved |
| Approval per environment, same templates and parameters | Unproven | No protected environments; src-deploy.yml has 0 runs |
| Versioned image built, pushed, referenced | Unproven | No pipeline run produced the digest-pinned demo image; ACR private, tags not listable |
| Post-deployment checks fail on unhealthy or unauth success | Partly proven (logic, live target) | smoke() passed live, failed on unreachable host; unit tests OK; in-pipeline execution unobserved |
| No secret in logs or repository | Partly proven | Tree and one CI log clean for tested patterns; not exhaustive |

## Validation

* `python3 -m unittest discover -s infra/tests -p test_pipeline.py`: OK.
* Link check of the new note: passed. mypy, ruff and web checks not applicable (no code or web files changed).
* Temporary what-if parameter file and probe files deleted.

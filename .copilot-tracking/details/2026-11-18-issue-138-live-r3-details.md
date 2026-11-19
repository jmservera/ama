---
title: Issue 138 live audit r3 details
ms.date: 2026-11-18
---

## Phase details

* Phase 1: `gh api` for variables, secrets, runners, environments, workflow runs; `az identity federated-credential list`, `az acr list`, `az containerapp list` in resource group `ama`.
* Phase 2: `pipeline.parameters` with throwaway values, `az deployment group what-if` (applications off, temp file deleted), `pipeline.summarize_plan`, `pipeline.smoke` live and against an unreachable host, `infra/tests` pipeline tests, `git grep` and one CI log scan for value-shaped secrets.
* Phase 3: note `docs/reference/research/issue-138-live-r3-2026-11-18.md` plus folder of outputs; README index and log.
* Phase 4: changes, review, commit with trailers.

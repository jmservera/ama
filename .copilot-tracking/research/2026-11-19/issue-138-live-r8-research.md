---
title: Issue 138 live r8 research
ms.date: 2026-11-19
---

Refs #138. Read-only re-check of GitHub and Azure (no credential read, nothing created). Baseline: r7 note
`docs/reference/research/issue-138-live-r7-2026-11-19.md`. Findings: no `AZURE_*` variable (only
`GH_AW_DEFAULT_MAX_DAILY_AI_CREDITS`); one secret name `COPILOT_GITHUB_TOKEN`; environments `dev-plan`,
`pilot-plan`, `test-plan` have 0 protection rules; 0 runners; 0 `src-deploy.yml` runs; 6 identities in `ama`
with 0 federated credentials. Planning readiness: Ready, stop outcome.

---
title: Issue 138 live audit r3 changes
ms.date: 2026-11-18
---

## Changes

Refs #138. Documentation only; no source, workflow or Azure change. Tier: focused.

Files: `docs/reference/research/issue-138-live-r3-2026-11-18.md`, the `issue-138-live-r3-2026-11-18/` output folder, `docs/reference/README.md` index entry, `docs/reference/log.md` entry, and these tracking artifacts. The session state file replaced the earlier tracked version (history is in git).

## Per-criterion result

| Criterion | Status | Basis |
| --- | --- | --- |
| OIDC federated credentials scoped per environment | Unproven | 0 federated credentials, no `AZURE_*` variables, no matching environments |
| `what-if` on infra PRs, result attached | Unproven | Live what-if Succeeded (99 Create, 15 Modify, 82 Ignore, 14 Unsupported) but `summarize_plan` refuses it; PR job skipped, 0 runners |
| Approval per environment, same templates and parameters | Unproven | 0 protection rules; `src-deploy.yml` 0 runs |
| Versioned image built, pushed, referenced | Unproven | No pipeline run produced the demo images; registry private |
| Post-deployment checks automatic, fail on unhealthy or unauthenticated success | Partly proven | `smoke()` passes live, fails on unreachable host; no deployment run |
| No secret in logs or repository | Partly proven | Five test fixtures only in tree; 0 matches in one CI log; no secrets context |

Production-only or owner items: repository settings, private runner, protected environments, Entra app registrations (CLI lacks directory privilege), demo naming mismatch (`forward` vs `cutover-test`).

## Validation

* `python3 -m unittest discover -s infra/tests -p 'test_pipeline*.py'`: OK.
* Live commands and outputs in `docs/reference/research/issue-138-live-r3-2026-11-18/`.
* Not run: mypy, ruff, `rpi-checks.py` (no executable change); hosted CI is not observed for this local commit.
* Azure: read-only plus what-if; nothing created, nothing to delete; temp parameter file removed.

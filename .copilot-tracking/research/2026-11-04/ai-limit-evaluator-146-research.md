<!-- markdownlint-disable-file -->
---
title: Issue 146 AI-limit evaluator research
description: Prior delivery check and slice choice for monitoring coverage
ms.date: 2026-11-04
---

## Research

* Disposition: executed. Planning Readiness: Ready.
* Prior merged work: #512 (source-only job/IoT candidates, runbooks, workbook) and #674 (coverage register, indicator states, diagnostic sanitiser). Runbook gap matrix in `infra/monitoring-runbooks.md` lists remaining evidence.
* Unmet, needing Azure/owner (not implementable here): installed poison-queue producer and alert, live deployment, KQL execution, named owners, finance cost feed, wiring redaction into platform logs, live thresholds.
* Unmet and locally testable: a deterministic AI-limit breach classifier (tokenomics T1 evidence) and restart-safe event reconciliation (RAI R5), both absent from the core module.
* Slice: add both as pure functions in `src/core/.../monitoring_coverage.py`. No Bicep or infrastructure change, so the focused tier applies.
* Branch note: the requested branch name is checked out in another worktree; work is on `feat/issue-146-r6` from `origin/main`.

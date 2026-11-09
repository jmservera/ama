---
title: Issue 81 demo recovery plan
description: Prospective plan to reconcile main locally and run demo-targeted checks for the parent PR 1240
ms.date: 2026-11-09
task_slug: issue-81-demo-recovery
---

Refs #81. Details: [details](../../details/2026-11-09/issue-81-demo-recovery-details.md). Research: [research](../../research/2026-11-09/issue-81-demo-recovery-research.md).

## Phases

1. Merge fetched `origin/main` `b46a9ad9` into the local recovery branch with an ordinary merge, keeping main's rubric score and cut-over evidence and the parent's append-only checkpoint blocks. No rebase, reset, push or PR change.
2. Run owner-selected demo-targeted tests from an out-of-tree scratch install: core lifecycle, gate, resident decision, quality and hazard selectors; ranking selectors; lint and types for touched core.
3. If the shared heavy lock is free (nonqueued), run the owned loopback SQL Server selector for changed persistence. A reproduction of #1292 is recorded exactly and returned as a blocked handoff; no fix is written here.
4. Record changes, one author Review, the AC-to-evidence matrix and the handoff. Commit a clean candidate.

## Success criteria

* Clean merged HEAD with main as ancestor and no unresolved intent conflict.
* Actual commands, counts, exits and skips recorded; no earlier result inferred.
* Unmet criteria remain unticked; whole #81 stays open (`Refs #81`).

## Critique

Executed once (author, before implementation): the plan avoids duplicating #1292, avoids the complete gate per the owner's demo decision, and keeps SQL on an owned disposable container. Compatible finding applied: record the SQL result as blocked rather than waiving a failing selected test.

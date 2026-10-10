---
title: Branch Lineage Instruction Authoring Evidence
description: Bounded authoring record for the branch workstream and stacked-PR amendment
ms.date: 2026-10-10
ms.topic: reference
---

## Scope and Outcome

* Outcome: Complete.
* Source edit: `.github/copilot-instructions.md`, Branch and Pull Request
  Workflow only.
* Source boundary: frontmatter and all other source sections were left
  unchanged. This log is the approved stage-evidence file, not a source
  instruction artifact.
* Authority: the added prose is advisory guidance, not proof of Git or hosting
  protection.

## Edit-to-Acceptance Mapping

| Acceptance need | Implemented amendment | Evidence |
| --- | --- | --- |
| Workstream continuity | Branch selection now checks status, current branch, known upstream/PR lifecycle, relationship and dependency; a matching active branch or PR is reused by default across research, design, PRD, implementation and review. | Branch decision table |
| Fresh main only when appropriate | Latest `origin/main` is selected only for unrelated work, a merged/completed workstream or explicit owner direction; a message, document type or phase is explicitly insufficient. | Branch decision table |
| Isolated related work | Risky, breaking or independently reviewable related work may use a child branch from the current topic, with worktrees for parallel or isolated copies. | Branch decision table |
| Safe ambiguity handling | Closed-unmerged, detached, unknown and ambiguous dependency cases request the smallest owner clarification; history-changing actions are prohibited as a resolution. | Guard note |
| PR-base correctness | Independent PRs target `main`; deliberate stacked PRs target their parent, declare the dependency, and are re-evaluated after the parent merges. | Pull request note |
| Existing safeguards | Dirty-worktree protection, privacy-safe authorship, checks and owner-controlled merge boundaries remain in place. | Unchanged adjacent bullets |

## Validation

* Reviewed the amended workflow as rendered Markdown: one compact table and
  two supporting notes; no command dump or duplicate rule added.
* Confirmed source scope manually against the approved boundary: only the
  Branch and Pull Request Workflow section was changed.
* Applied catalog criteria: Outcome and structure: explicit success criteria
  and stop rules; Instruction-file architecture: concise always-loaded files
  and living documentation; Safety and enforcement: separate advisory from
  enforced.
* Fidelity: static document review only. No native Git, GitHub, branch
  protection or PR execution was performed; the amendment does not enforce
  its advisory rules.

## Unresolved Issues

* No unresolved authoring issue within the approved source boundary.
* Runtime behavior, Git-host controls and branch-protection enforcement remain
  outside this amendment and require separate approval if protection is needed.

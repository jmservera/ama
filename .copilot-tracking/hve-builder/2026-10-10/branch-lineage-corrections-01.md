---
title: Branch Lineage Static Corrections
description: Coherent correction batch for the original independent static findings
ms.date: 2026-10-10
ms.topic: reference
---

## Scope

The correction batch stays within the original Branch and Pull Request
Workflow source boundary. No capability, artifact architecture, enforcement
setup or acceptance boundary changed.

## Corrections

* BRANCH-001: Explicit safe owner branch/base directions take precedence.
  Only an owner request specifically for a fresh main-based branch selects
  that route. The fresh-base row also explicitly covers main with no matching
  active topic and previously merged work.
* BRANCH-002: Read-only branch selection grants no authority to modify
  existing work/history, reopen/merge PRs, delete branches or write remotely.
  Creating/switching the chosen local branch happens after selection and
  dirty-worktree protection; publishing remains a separate workflow step.

## Closure

Await targeted independent closure of the original BRANCH-001/002 findings.
Behavior simulation and final mechanical validation remain downstream;
neither has run yet.

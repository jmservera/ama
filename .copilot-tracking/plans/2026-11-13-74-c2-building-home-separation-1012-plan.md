---
title: Issue 74 criterion 2 evidence-only plan
description: Bounded plan to run the smallest existing focused fixture check for shared-building versus per-home separation and record evidence without source change
ms.date: 2026-11-13
---

## Objective

Record whether existing focused tests already prove criterion 2 shared-building versus per-home separation, without new tests or source edits.

## Phases

1. Create an isolated venv outside the repository and install the three worktree distributions editable with `--no-deps`; verify the import path resolves to this worktree (the system install points at another checkout, so it must not be used).
2. Run three existing core unittest selectors with `ZF_DATA` pointed at a temporary file: the two-home shared-building test (both stores), the shared-view test, the cost-visibility test.
3. Record commands, exits, limitations; write changes and request independent Review.

## Out of scope

Source or test edits, API/browser/Docker/SQL/cloud, full gate, issue or board writes, ticking criteria, null-funding and own-home controls, new retention criteria.

## Decision rule

If checks pass, cite them as partial proof of the shared-cost/works separation and name the empty dependencies/holds fixture as the residual gap for a later separately assessed admission.

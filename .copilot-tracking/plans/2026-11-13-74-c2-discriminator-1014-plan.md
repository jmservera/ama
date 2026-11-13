---
title: Issue 74 criterion 2 discriminator plan
description: Plan for a single external probe with in-process module origin checks and isolated temporary state
ms.date: 2026-11-13
---

## Steps

1. Write the critique, then only if acceptable create a temp venv (pip --no-deps -e src/core -e src/agents -e src/api), temp ZF_DATA, runner in /tmp.
2. Run the runner once from the worktree test directory helpers; record command, exit, hash, raw output, in-process `__file__` origins asserted under this worktree.
3. Delete only the owned temp runtime; write changes, independent targeted Review, local commit.

## Out of scope

Repository test or source edits, API HTTP, browser, SQL server, Docker, cloud, full gate, ticks, GitHub writes, human-approval claims.

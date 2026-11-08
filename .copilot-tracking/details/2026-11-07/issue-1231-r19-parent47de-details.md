---
title: Issue 1231 r19 phase details
description: Prospective phase details for the r19 parent79 47de325d merge
ms.date: 2026-11-07
---

* Backup: `git branch backup/issue-1231-cfc78-pre-r19-merge cfc78dbffb205743a5154d98440d4d884cec5fbb`.
* Merge: `git merge --no-ff` of 47de325d80eda5665f3e3d3250fedce7a17c85d1 with Refs #1231 and the Copilot trailer.
* Proof: compare `git diff --raw 9b21a6a0 47de325d` with `git diff --raw cfc78dbf HEAD`, both excluding .copilot-tracking; ranking blobs equal start; zero deleted log lines.
* Checks: PYTHONDONTWRITEBYTECODE=1, /tmp/zf79venv, Ruff from the r7 venv, mypy cache in scratch, module `__file__` printed, exit codes captured directly.

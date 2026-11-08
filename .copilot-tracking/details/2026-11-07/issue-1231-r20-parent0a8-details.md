---
title: Issue 1231 r20 phase details
description: Prospective phase details for the r20 parent79 0a8ecd50 merge
ms.date: 2026-11-07
---

* Backup: `git branch backup/issue-1231-120bb-pre-r20-merge 120bbccea44d031df41efb5803fff2b92dce54b4`.
* Merge: `git merge --no-ff` of 0a8ecd50 with Refs #1231 and the Copilot trailer.
* Proof: `git diff --raw 47de325d 0a8ecd50` versus `git diff --raw 120bbcce HEAD`, excluding .copilot-tracking; child ranking blobs equal start; zero deleted log lines. Do not claim all src unchanged (test_assistant_release.py is received).
* Checks: PYTHONDONTWRITEBYTECODE=1, /tmp/zf79venv, Ruff from the r7 venv, mypy cache in scratch, module `__file__` printed; each command writes its own .out/.err/.exit.

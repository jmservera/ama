<!-- markdownlint-disable-file -->
---
title: Issue 349 remote-reconcile phase details
description: Steps and validation
ms.date: 2026-10-25
---

* Step 3.1: verify HEAD d78373a5 and remote 44ba5b77 are unchanged, then git merge --no-ff 44ba5b77 with Conventional message and Copilot trailer.
* Step 3.2: on conflict, test file keep ours, latest.json keep ours (main), anything else stop and report. No -X theirs, no score edits.
* Step 3.3: proof: is-ancestor for 44ba5b77, each of its eight commits, d78373a5 and ea5577b2 of the new HEAD; git diff of preflight files versus both parents.
* Step 3.4: write changes record and session-only PR body file under the session files folder.
* Step 4.1: PYTHONDONTWRITEBYTECODE=1 unittest of the focused file; python3 -m py_compile; ruff/mypy if installed (not installed earlier; install via pip only if needed).
* Step 4.2: independent assessment once; commit with repo-local noreply identity; gate with --lock-timeout 0 to a new external dir, no queueing or polling.

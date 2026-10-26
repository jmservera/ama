<!-- markdownlint-disable-file -->
---
title: Issue 349 ama-restart phase details
description: Phase details for the diagnosis-only continuation
ms.date: 2026-10-24
---

## Phase 3: Implement (evidence only)

* Step 3.1: Confirm git status clean for source paths; no edits to infra/ or src/.
* Step 3.2: Write the changes artifact listing only new dated tracking files.
* Step 3.3: Write the minimal owner/coordinator intervention plan (changes artifact).
Validation: focused test file (35 tests) already green; git diff touches only .copilot-tracking.

## Phase 4: Review and gate

* Step 4.1: Independent reviewer reads research, plan, changes and diff; outcome recorded.
* Step 4.2: Resolve gh identity, set repo-local noreply email, conventional commit with trailer.
* Step 4.3: Rebase onto origin/main only if the gate requires a current base; keep prior log entries.
* Step 4.4: tools/rpi-checks.py --all --base <sha> --out <new external dir>; verify receipt; no push.

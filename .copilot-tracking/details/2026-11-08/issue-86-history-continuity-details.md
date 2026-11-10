---
title: Issue 86 history continuity details
description: Commands and proof checks for the history merge
ms.date: 2026-11-08
---

* Merge: `git merge --no-ff -s ours -m <message> 6ff492adf9d897c81ae666e71696f5a10ed1573d`.
* Proof: `git rev-parse HEAD^{tree}` equals the pre-merge tree plus the record commits only; `git diff --name-only a8efb903 HEAD` lists only `.copilot-tracking`; `git merge-base --is-ancestor X HEAD` echoing explicit exit codes for the five commits; `git diff --check`; `python3 -m json.tool .github/rubric/scores/latest.json`.

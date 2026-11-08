---
title: Issue 86 Main 4bc1e3f3 CI dependency integration details
description: Proof and check commands
ms.date: 2026-11-08
---

* Proof: compare `git ls-tree -r HEAD src` before and after; `git diff --name-only origin/main HEAD` outside tracking must be empty for non-tracking paths.
* Checks: selectors taken from the repository's own tool test files, run from the repo root with `python3 -m unittest`; counts read from the unittest summary lines.
* Scratch under `/home/azureuser/.local/share/ama/gates/g86-main4bc1-ci`.

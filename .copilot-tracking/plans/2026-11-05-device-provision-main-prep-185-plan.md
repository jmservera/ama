---
title: Plan for #185 current-main preparation
ms.date: 2026-11-05
---

* Step 1: commit these research, plan and details records on the child.
* Step 2: ordinary merge of pinned `bb3a3b03cb94eef6c06ae4b12d07cfe7bbdef43f` into the child. No rebase, amend, force or parent change. Stop on an ambiguous conflict.
* Step 3: light checks only, from this worktree: the device identity and provisioning unit selectors, ruff with no cache, mypy with an external cache, and import-path proof.
* Step 4: record changes and a single review, then the state record. No push, PR update, deployment or issue change.
* Critique (single pass, self): the only risk is dependency drift in the shared venv; the check proves the import path, and any missing dependency is recorded rather than worked around. Applied.
* Excluded: FULL gate, heavy runner, browser, SQL, Docker, Azure, providers, real data, credentials.

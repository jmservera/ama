---
title: Issue 86 Main 4bc1e3f3 CI dependency integration plan
description: One normal merge and focused tool checks under the CI-first tier
ms.date: 2026-11-08
---

Tier: CI-first focused checks; no FULL, SQL, browser, image or whole-API sweep, because no application behavior changes.

1. Commit research, plan, details and critique first.
2. Re-fetch; stop on drift.
3. `git merge --no-ff origin/main` (no rebase, reset or force). Stop on any source conflict.
4. Prove `src/` blob and mode identity before and after, tree contents equal Main for incoming paths, `git diff --check`.
5. Run the inherited installer, CI-selection and runner tests by actual selectors, plus ruff and mypy on the changed tools as the repository config defines.
6. Changes and one author Review; commit; freeze.

Stop on drift, conflict or a failing check (report, no silent fix).

## Critique amendments (all accepted)

* F1: verify the allowlist by comparing the merge with its first parent, and compare incoming paths with Main separately; do not require every non-tracking path to equal Main.
* F2: whitespace check is `git diff --check HEAD^1 HEAD`.
* F3: run actionlint on the workflow only if the pinned installer can provide it locally; otherwise record it as not run, and no hosted-download claim is made.
* F4: confirm clean worktree and final tree equal to the tested tree after the last commit.

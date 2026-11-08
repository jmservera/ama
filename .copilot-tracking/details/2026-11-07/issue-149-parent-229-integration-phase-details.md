---
title: Issue 149 parent integration of merged child 229 and current main, phase details
ms.date: 2026-11-07
---

## Phase details

* Merge commands: `git merge --no-edit origin/test/ux-evidence-149`; `git merge origin/main -m "chore: adopt main b284d0d3 into the 149 parent topic" -m "Refs #149." -m "Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>"`.
* Proof: `git merge-base --is-ancestor` for 660716929024, 4d95, 1263 hotfix and b284; `git diff origin/main HEAD --name-only`; `git diff origin/main HEAD -- src/core`.
* Validation roots: /tmp/zf149-integrated-1107 (snapshot, venv, logs) and /tmp/zf149-integrated-browser-1107 (browser scratch, axe copy, logs). Existing /tmp/zf149-* directories are never overwritten.

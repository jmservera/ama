---
title: Issue 81 fresh-main merge details
description: Step details for the prospective normal merge
ms.date: 2026-11-07
task_slug: issue-81-merge-755
status: prospective
plan: ../../plans/2026-11-07/issue-81-merge-755-plan.md
---

1. Verify HEAD equals the pinned start and `git fetch` still yields `7551e50e`; otherwise stop.
2. `git merge --no-ff -m "chore: merge origin/main 7551e50e into issue 81 parent" 7551e50e` with repo-local noreply identity and Copilot trailer.
3. Proof: `git rev-parse HEAD^1 HEAD^2`; `git diff --stat HEAD^1 HEAD` equals the four main files plus main tracking files; `git rev-parse HEAD:<path>` for `appointments.py`, `gates.py`, `procurement.py`, `quality.py`, test file equals pre-merge blobs.
4. Run the four focused modules, ruff, format, mypy as in the plan; record exits and skips verbatim.
5. Write changes and one author Review, commit, report ignored-inclusive status.

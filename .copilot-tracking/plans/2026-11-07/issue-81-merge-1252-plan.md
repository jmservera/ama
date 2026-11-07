---
title: Issue 81 main 1252 merge research, plan and details
description: Prospective research, plan and details for one normal merge of pinned main a1d26534 (PR 1252) into the parent
ms.date: 2026-11-07
task_slug: issue-81-merge-1252
parent_task: issue-81-merge-1253
status: prospective
---

## Research

* Start HEAD `720d9e49cfadf61416903cbfebdd20a3aef6986f`, tree `52201661d167872133c86fc7e1eaa7c4237c6513`, branch `feat/controlled-lifecycle-integration-81`, ignored-inclusive clean, PR #1240 open to `main`. Preservation ref `refs/ama/issue81-pre-a1d-merge` set to the start head; earlier refs unchanged.
* Fetched `origin/main` `a1d265340ba7d6f14b24e028362b2d5f4bb80126` (PR #1252, issue #1251), single parent `39506027` which is already in the parent. Merge base with the parent: `39506027`. The scorer run for `a1d26534` (42381926533) is completed with success and no score descendant exists yet, so `a1d26534` itself is the admitted target. A later score-only descendant would need a fresh amendment.
* Incoming delta `39506027..a1d26534`: `tools/backlog-sync.py`, `tools/test_backlog_sync.py` and original RPI tracking files. No `src/`, schema, workflow or score change. Dry `git merge-tree` is clean (tree `ec7266db150b178d0e42ea687ae003ea1f42eb5e`).
* The parent has not changed those tools files since the merge base.
* CI convention for these tools (`.github/workflows/src-ci.yml` lines 261-267): unittest `test_backlog_sync`, isolated ruff check and format over the five tools files, `mypy --ignore-missing-imports tools/test_backlog_sync.py tools/backlog-sync.py`, plus `mypy --strict` on the rpi-checks files.

## Plan and details

* One normal `--no-ff` merge of exactly `a1d26534`; no rebase, force, rewrite, retarget, push or child touch. Stop on drift, dirty tree or conflict.
* Order: commit these records as PRE, recheck clean and pinned main, merge.
* Proof: parents are PRE and `a1d26534`; `git diff --raw PRE HEAD` equals `git diff --raw 39506027 a1d26534` including modes; `src/` and `.github/` identical to PRE; `git diff --check` clean.
* Light checks in `/mnt/ama-gates/g81-main1252-preparation-1107`: `env -i`, `PYTHONDONTWRITEBYTECODE=1`, external caches, `git archive` snapshot of the merged head, scratch venv with ruff 0.17.1 and mypy 2.4.0 (CI pins mypy 2.4.0). Run the three CI tools unittests, the isolated ruff check and format, and both mypy commands, exits unmasked. Also rerun the four core modules, with non-editable `--no-deps` core and agents installs and import-origin proof, because the parent's core source is unchanged but the head differs; optional context only. No queue benchmark, services, FULL, private data or uv.
* Critique: one independent critique before mutation. Results are local observed only, not acceptance.

## Amendment 1 (critique verdict Approve with two Non-blocking findings; both accepted)

1. Whitespace proof uses `git diff --check PRE HEAD`.
2. Python 3.12 (venv from `python3` 3.12.3). Core modules: `test_quality_procurement test_gates test_hazard_referral test_resident_preview` from `src/core/tests`.

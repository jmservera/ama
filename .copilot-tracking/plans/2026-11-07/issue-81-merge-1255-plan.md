---
title: Issue 81 main 1255 merge research, plan and details
description: Prospective research, plan and details for one normal merge of pinned main c1a16482 (PR 1255) into the parent
ms.date: 2026-11-07
task_slug: issue-81-merge-1255
parent_task: issue-81-merge-1252
status: prospective
---

## Research

* Start HEAD `6cae8cbeef8400392e7d9ab955b97d1799415f22`, tree `5ffea910e77ac1aca65381676b401cdc89f5220e`, branch `feat/controlled-lifecycle-integration-81`, ignored-inclusive clean, PR #1240 open to `main`. Preservation ref `refs/ama/issue81-pre-c1a-merge` set to the start head; earlier refs unchanged.
* Fetched `origin/main` `c1a164829e77efe45f5f002740bd79699b89b334` (PR #1255, merged, the coordinator-declared post-1255 head), single parent `a1d26534` already in the parent. Merge base: `a1d26534`. Dry `git merge-tree` is clean (tree `9d98956c383f5097edb3f7613f3bf7f9bd8a8478`).
* Scorer run 42387247541 for `c1a16482` was in progress at fetch time. Only `c1a16482` itself is admitted now. A later descendant is admitted only after a fresh amendment proving it changes solely `.github/rubric/scores/latest.json` (parsed JSON).
* Incoming delta `a1d26534..c1a16482` outside tracking records: `src/api/tests/test_assistant_release.py` (test only, 76 lines), `tools/rpi-checks.py` (adds `test_assistant_release.MssqlUnleasedRevocation` to `SQL_SELECTORS`), `tools/test_rpi_checks.py` (one assertion). Fourteen added `.copilot-tracking` files for the 107 records. No `src/*/src` production, schema, workflow or score change (verified: zero raw diff under `src/*/src`).
* The parent has not changed those three files since the merge base, so no content conflict is expected. Unlike PR 1252, `src/` is not unchanged: exactly one test file under `src/api/tests` changes.
* Light check convention: tools unittests and isolated ruff and mypy as in `.github/workflows/src-ci.yml` lines 261-267; `test_assistant_release` for the received test; four core modules for parent source context.

## Plan and details

* One normal `--no-ff` merge of exactly `c1a16482`; no rebase, force, rewrite, retarget, push or child touch. Stop on drift, dirty tree or conflict.
* Order: commit these records as PRE, recheck clean and pinned main, merge.
* Proof: parents are PRE and `c1a16482`; `git diff --raw PRE HEAD` equals `git diff --raw a1d26534 c1a16482` including modes and blob ids; `src/*/src`, `.github/` and schema identical to PRE; `git diff --check PRE HEAD` clean; whole prior log prefixes preserved.
* Light checks in `/mnt/ama-gates/g81-main1255-preparation-1107`: `env -i`, `PYTHONDONTWRITEBYTECODE=1`, external caches, full `git archive` snapshot of the merged head (not a subset), scratch venv Python 3.12, ruff 0.17.1, mypy 2.4.0, non-editable `--no-deps` core, agents and api installs with import-origin proof, PyYAML only after a missing-dependency failure. Run unmasked: `test_backlog_sync`, `test_ci_affected`, `test_rpi_checks`, `test_assistant_release` (SQL and Azure tests skip without services), the four core modules `test_quality_procurement test_gates test_hazard_referral test_resident_preview` from `src/core/tests`, the isolated ruff check and format over the five tools files and both mypy commands. Pre-existing formatter diagnostics in excluded test files are reported, not reformatted. No queue benchmark, services, FULL, SQL, private data or uv.
* Future gates must pass `--lock-timeout 0`. Results are local observed only, not acceptance; the old receipts stay historical.
* Critique: one independent critique before mutation, authored by a read-only agent, not human or operating approval.

## Amendment 1 (critique verdict Approve with one Non-blocking finding, accepted)

1. No SQL acceptance claim; the SQL release-denial test needs the later FULL gate with `--lock-timeout 0`.
2. The scorer run 42387247541 was still in progress after the critique and a recheck. The coordinator pinned `c1a16482` as the declared post-1255 head, so exactly that commit is merged now. A later score-only descendant is not merged by this lane; it would need a separate admitted amendment and merge.

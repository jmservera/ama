---
title: Issue 81 score 23b merge research, plan and details
description: Prospective research, plan and details for one normal merge of the score-only main 23b26a7f into the parent
ms.date: 2026-11-07
task_slug: issue-81-merge-score-23b
parent_task: issue-81-merge-1255
status: prospective
---

## Research

* Start HEAD `a0ec0834491a5e2b4a471f44d7cb3257d9bc450b`, tree `c65672b6eebe0c621d53c9a4319b8f570c3e05a8`, branch `feat/controlled-lifecycle-integration-81`, ignored-inclusive clean, PR #1240 open to `main`. Preservation ref `refs/ama/issue81-pre-23b-merge` is set to the start head.
* Fetched `origin/main` `23b26a7f3a4693cd20dcf0447303d97491096cb3`, one `chore(rubric): record score 77/100` commit whose only parent is `c1a16482`, already an ancestor of the parent. Raw delta `c1a16482..23b26a7f` is exactly one entry: `M .github/rubric/scores/latest.json` (100644, `61a5109f1` to `a0cfed75b`). The incoming blob parses as JSON. Dry `git merge-tree` is clean (tree `6152a766d044340c28657ce4c55f81814a680533`).
* Reason: `tools/rpi-checks.py` requires current `origin/main` to be an ancestor of HEAD and `validate_stack` requires it for each parent member, so a normal merge is needed before later child propagation. The coordinator admitted this score-only descendant; it is not human or policy approval.
* Child #86 is recorded at `ed5bddf4faa5071487e1f805d5159a2cd488b4ce` (coordinator-declared) and is not touched.

## Plan and details

* Commit these records as PRE, recheck clean state and pinned main, then one `--no-ff` merge of exactly `23b26a7f`. No rebase, force, push, retarget, child change, or later main merge. Stop on extra main content.
* Proof: parents are PRE and `23b26a7f`; `git diff --raw PRE HEAD` equals `git diff --raw c1a16482 23b26a7f` plus the added records; `src/`, `tools/`, `.github/workflows` and schema trees identical to PRE; incoming score blob and mode exact; JSON parse; `git diff --check PRE HEAD`; prior `.copilot-tracking` files byte-identical.
* No tests, services, FULL or installs. Earlier results (233 core tests with 1 skip, 48 release tests with 1 skip, tools tests and static checks) stay historical for source head `a0ec0834`, whose executable inputs are unchanged by this merge.
* Critique: one independent read-only critique before mutation. It is author-side planning evidence, not independent acceptance.

## Amendment 1 (critique verdict Revise: two Blocking findings, both accepted)

1. The merge adds no records: `git diff --raw PRE HEAD` must equal exactly `git diff --raw c1a16482 23b26a7f` (one entry), not that plus records.
2. PRE's parent must be `a0ec0834` and `git diff --name-status a0ec0834 PRE` must list only the two new records (plan and critique) under `.copilot-tracking/plans/2026-11-07/`. Also prove `git diff --raw a0ec0834 HEAD` equals the score delta plus those two paths, and that every pre-existing `.copilot-tracking` blob is unchanged.

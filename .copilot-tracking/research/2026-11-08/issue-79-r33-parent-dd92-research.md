---
title: Issue 79 r33 research, parent topic input dd92e0d1
ms.date: 2026-11-08
---

* Preflight: local root `341410c366df40b014ffc0e4505a583ce0b0a8d8`/tree `b5390ab50c97c22d6bf132a5cbc3a7a3191839c5`, branch `feat/ranking-publication-runner-79`, `git status --short --ignored` empty. Fetched `origin/main` is `b284d0d3e8ebed24d40bf9eb1e23de1ae9101d01` (unchanged).
* Input: `origin/feat/ranking-publication-runner-79` = `dd92e0d14b8a69fc1825d6fcd1a2f272ed10f605`, tree `b99d822247dd36e6eaebb7b761259f190fcef394`, the squash merge of child PR 1242 (2026-11-08T00:39:41Z, child head `40d51403`). Local 341410c3 is its first parent and merge base, so the input is a direct descendant.
* Delta 341410c3..dd92e0d1: eight source/test/doc files (`server.py`, `store.py`, `ranking_publication.py`, `ranking_publication_runner.py`, `src/core/README.md`, and three ranking test files) plus 146 child `.copilot-tracking` records. The log is unchanged. `git merge-tree` of HEAD and the input is clean.
* Incoming source semantics (read, not assumed): `publish` stages privately, `_confirmed` syncs the archive folder for new/existing/race-loser outcomes and raises `DurabilityUnconfirmedError` carrying `written`, `_remove` is non-throwing, the runner reports `committed_unconfirmed` (exit 2) with the error's `written`. These match this root's existing fixes.
* Evidence status: the incoming tree equals the child tree, which does not validate this integrated parent HEAD or the RPI commits added here. Root341/child40d R35 FULL and independent assessments are historical combined-tip evidence, not a FULL for the integrated parent. Old CI and scorer results do not validate the new head.
* Approval gaps (unchanged, none created here): named policy, legal, approver and human acceptance, deployed scheduling, cross-platform and whole #1231/#79/#73/#135/#440 acceptance; topic integration is not merged-main acceptance. #1258, #1259, unmerged #123 and #81/#86/#107 sibling functionality stay out of scope; the #440 stabilization gate stays due and is not retroactively accepted.
* Tier FULL (SQL/filesystem publication, concurrency, security-sensitive). Admitted gate: one nonqueued `rpi-checks.py --all --jobs 2 --lock-timeout 0 --base b284d0d3` to a new root-filesystem output.

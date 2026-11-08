---
title: Issue 1231 r10 research (ancestor-preserving merge of the named local parent)
ms.date: 2026-11-06
---

## Chronology statement (prospective)

Written 2026-11-06 about 20:40Z (clock read 20:36:10Z at the last evidence command), before any merge, source edit or test run for r10. Original R1 to R8 research, plans, changes, reviews, the r4 passed receipt, the r7 failed receipt and the r9 passed receipt are preserved unchanged. The r9 FULL receipt (sha256 `8f59959f…2f9c`) was genuine for head `29d1669e6` on base `bb3a3b03c` and is historical, not current, because main and the parent have since moved.

## Question

Can the local child head `29d1669e6ddf09a8566861228c6584d30fba8b51` (tree `c3c16145dfc4223112b2dd90c1a147da9f8af092`) take an ancestor-preserving normal local merge of the named local parent `feat/ranking-publication-runner-79` at `d654634fcbe5c82a362e9a3d948d09d0c2993d6d` (tree `7bf7a4af3f494d03c16d3af92fe7e9fa4cc6badb`) without conflict or any substantive source-intent change?

## Evidence (read-only, this session)

* Actual branch is `fix/ranking-archive-concurrent-writer-metadata` (the brief's shorthand `feat/ranking-archive-1231` does not exist as the checked-out topic; the actual branch is preserved and never switched). Ignored-inclusive status is clean.
* Original parent `43080ab42a96fada36b9d0bc523dfa16fe0c3cd5` is an ancestor of the child head. `git merge-base HEAD parent` is `43080ab42`.
* Parent-only commits (4): `030c56b5c` (r13 prospective records), `56eec7369` (main #1236), merge `aeb1adfa4` (main into parent), `d654634fc` (r13 changes, review, state). Child-only commits: 13.
* `git diff 43080ab42 d654634fc -- src` is empty: the parent `src` tree is identical to the original parent.
* `origin/main` and local `feat/case-workbench-integration-73` are both `56eec736906774ef56d8c9a66ed7f3f9c1e520c6`. Main `56eec7369` is not an ancestor of the child head; it is an ancestor of the parent. Main's only change over `bb3a3b03c` is the coordinator agent file `.github/agents/ama-backlog-delivery-coordinator.agent.md` plus tracking.
* `git merge-tree --write-tree HEAD parent` exits 0 with no conflicts, predicted tree `5d21b1d44de448b6c2678afc9ff66a4c8cd69056`. Against the child head that tree differs only by: the coordinator agent file modified, and 231 added `.copilot-tracking` files (parent and main RPI records). `src`, `infra`, `tools` and `.github/workflows` are identical to the child head.
* The reverse diff of the child versus the parent in `src` (8 files) is exactly the child corrections (hard-link stage, truthful metadata, `ArchiveStorageError`, `stage_retained`, conditional wording, wrapped lines), so the merge keeps them.

## Findings and limits

* No conflict and no source-intent decision is needed; this is a normal merge, not a rebase, and no history is rewritten.
* A merge only aligns ancestry. It is not source acceptance, FULL validation, independent review, human approval or publication authority.
* The r9 receipt will not verify the merged head (identity mismatch is expected and will be recorded, not hidden).
* Issue 86 owns the sole native FULL lane, so only lightweight checks are admitted. Missing SQL, browser and image prerequisites are not tested here.
* Topology stays child -> parent79 -> parent73. No retarget to main. Parent79 has no remote yet.

## Planning readiness

Ready. Disposition: executed (read-only evidence only).

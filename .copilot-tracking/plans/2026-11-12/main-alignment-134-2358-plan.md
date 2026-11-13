---
title: Main alignment of the #134 disposition candidate, plan
description: Prospective plan amendment for a local normal merge of current main into the frozen #134 documentation candidate
ms.date: 2026-11-12
---

## Scope

Prospective amendment, written before any merge. It extends [the original #134 plan](ac-dispositions-134-1112-plan.md) and does not edit it, its critique, its review, or [correction 1](ac-dispositions-134-1112-correction1-amendment.md) and [correction 2](ac-dispositions-134-1112-correction2-amendment.md). The original process defect (edits before plan and critique) and both spent corrections stay as recorded. Evidence: [research](../../research/2026-11-12/main-alignment-134-2358-research.md).

## Ordering

1. This plan and an independent fresh-context critique are persisted before the merge. No merge or doc edit happens first.
2. Apply critique findings directly. Do not repeat the critique.
3. `git merge origin/main` (normal local merge of the fetched `774a91e5f`; no rebase, no force). Merge commit with the repository-local noreply identity and the Co-authored-by trailer.
4. Resolve only the two proven genuine docs conflicts, `docs/architecture/cutover-evidence-pack.md` and `docs/reference/README.md`, keeping both sides: main's post-fix-wave section or paragraph first, then the #134 section or paragraph, with a blank line between. Preserve the pack's no-trailing-newline state or add one consistently. Do not touch `log.md` content (auto-merged, append-only), source, tests, tools or workflows.
5. At most one alignment correction, only if validation proves a defect created by the merge, within the existing history (no new pool, no renewal of A4, E1 to E4 or corrections 1 and 2).
6. Independent review of the frozen merge result, then a final result JSON.

## Validation (docs only, no executable gate)

* No conflict markers; `git diff --check`; ASCII check of added lines.
* Section and paragraph count: both the post-fix-wave and the #134 sections are present exactly once in the pack and README, and the #134 section text is byte-identical to `cc7e3c3a9`'s.
* Log: both sides' entries present, no earlier entry rewritten (compare against both parents).
* Anchor and relative link resolution for the two touched index anchors.
* Unchanged historical claims check: six partial, four deferred, #83 OPEN, #134 OPEN, no ticks.
* Tree diff against `origin/main` limited to the #134 docs and tracking files; tree diff against `cc7e3c3a9` limited to main's six commits.

## Out of scope and held

No push, PR, merge into main, tick, issue or board write, cloud, model or deploy, shared cleanup, publication, source change, merge of unmerged PR 1495, or touch of the existing #134 source worktree. This is a candidate for UX parent integration, not a standalone PR, and not an acceptance upgrade: #83 stays OPEN, #134 stays partial and deferred. Blockers: coordinator exact-head review, human approval and hosted CI remain outside this task.

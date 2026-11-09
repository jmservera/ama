---
title: Issue 1292 current-main priority SQL candidate main-preparation changes
ms.date: 2026-11-09
task_id: 1292-current-main-sql-mainprep-1109
---

## Executed (Git and Markdown only; no SQL, source or harness change)

* Planning commit `8565a5204` (research, plan, details, critique Revise F1 to F4 applied, state) before the merge.
* Merge commit `18a879574` of pinned `origin/main` `1a84b3b0054990262a0df0625d95e3f545d2739a` (parents: planning commit, main). Conflicts only in `docs/architecture/cutover-evidence-pack.md` and `docs/reference/README.md` (append conflicts); resolved by keeping both sides unchanged. `docs/reference/log.md` auto-merged.
* Disclosed deviation from the plan: the merge commit placed main's blocks first (as planned). That put the candidate's `###` subsection after main's `##` section, changing its parent heading. Commit `975170c73` moved the candidate blocks before main's blocks in the pack and the index to restore the original hierarchy and the log order; the line multiset of both files is identical before and after (pure move).
* Commit `1eab5a984`: dated current-target binding paragraph in the candidate pack subsection and a new append-only log entry.
* Tree equality at the final head and at main: `src` `86bc00e19a167e517ae2955ad88d6e2f7b4eac26`, `tools` `74ad3cb586dbff7f08ed3ba78301b9596a31ca86`, `infra` `b0969f8b7b8c3b21763c5f332123ef5ea2aac94d`, `.github/workflows` `29eb03ea759ea6717e334d8f0949915d5ba37a90`. The stop condition did not trigger; no campaign was run.

## Validation

* No conflict markers in tracked docs or tracking. No line from either parent was deleted by the merge (checked with `git diff` against both parents).
* Relative links in the touched pack and index resolve; the new anchor resolves. `docs/reference/log.md` has 17 pre-existing unresolved relative links to retired `mvp` and `capstone` paths in historical entries, none in the new entry; left unchanged (append-only).
* `6c05b1e12922205286400a17c73957c9c23bb35e` is an ancestor of the final head.
* Final path counts are taken from the actual Git ranges in the handoff, not from this record.

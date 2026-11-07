---
title: Issue 79 r27 changes, score-only merge of main f0afa8d7
ms.date: 2026-11-07
---

* One normal `--no-ff` merge of `origin/main` `f0afa8d76d7be13ec4278321e09e16e23eaeb37c` into planning head `baebb9e2d461b9115145d0239a370fca8d369e34`; merge commit `47ff4fe3123b533ad32201b6a7d0667db281cbe0`. No conflict, rebase or rewrite. Old root preserved at `preserve/issue-79-pre-scoref0af` (b6fc0d9b) and `preserve/issue-79-r27-planning`.
* Proofs: `git diff --raw` planning head to merge lists only `.github/rubric/scores/latest.json` (`a0cfed75` to `8045670e`, mode 100644); the merge blob equals main's; `python3 -m json.tool` parses it; `git diff --check` clean. Between b6fc0d9b and the planning head only r27 RPI files were added, so src, tools, workflows, tests, log and earlier RPI bytes equal b6.
* Not run: tests, lint, mypy and FULL, because no executable input changed. The old R26 note that no Config test exists is preserved; a Config test exists at `src/api/tests/test_exception_register.py:163`.

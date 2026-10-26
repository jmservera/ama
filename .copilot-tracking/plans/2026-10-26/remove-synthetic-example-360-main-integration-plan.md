# Plan: integrate main into PR 459 (issue 360)

Date: 2026-10-26, written and committed before the merge. Documentation only; no app source change.

1. Commit this plan and the research file.
2. `git merge origin/main`; resolve `latest.json` to main's side and `docs/reference/log.md` keeping all entries from both sides.
3. Check no conflict markers, Markdown links in the touched docs, `git diff --check`, and that the branch's own diff against main is still only its documentation files.
4. One independent bounded review comparing the first parent and main; commit changes and review artifacts; commit locally.
Holds: no push, PR edit, merge, heavy test, build or gate (disk 6.9 GB, 98 percent). A fresh exact-head/current-main full gate and coordinator review remain required before publication.

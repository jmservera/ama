# 215 C3 rebase plan

1. git rebase 50ff1a02a; keep main's entries and the #215 entry in order.
2. Add C3 artifacts and commit; do not push.
3. Run merge-tree, marker grep, ruff, targeted unittests in src/api and src/core.
4. Record exact HEAD in the review artifact.
Critique: executed once, no findings; plan is a mechanical rebase.

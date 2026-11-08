# Issue 1231 r32 details

Step 3: conflicts expected in ranking files; take child blobs (git checkout --ours). Check root-side deletions of old tracking state files: the root diff shows older state JSONs deleted relative to the child because they are child-only; the merge must keep them (child additions are not removed by a merge unless the root deleted them from a shared base). Verify with git diff --name-status against c18f45f2.
Step 5 environment: own venv from earlier gates, PYTHONDONTWRITEBYTECODE=1, check imported __file__ paths, scratch under /mnt/ama-gates/g1231-r32-prep-1107.

# Issue 1840 live2 research (rebase of 2d4538e69)

Task: rebase reviewed old_image_sql_probe candidate 2d4538e69 onto origin/main e91b6fa81; fix python -I worker self-test; prove or explain each acceptance criterion. Demo desktop only; tier FULL only if src changes.
Status: opened 2026-11-18T22:5Z; findings follow.

## Findings

* Candidate 2d4538e69 (parent 1c9ac230b) cherry-picked onto origin/main e91b6fa81. Conflicts: seven same-named 2026-11-18 `issue-1840-live-*` tracking files (main already holds an earlier blocked run) and `docs/reference/README.md`. Resolution keeps both sides: main's files unchanged, candidate's saved as `issue-1840-live-run2-*`; README keeps the #440 paragraph and the 1840 note.
* Before the fix, `SelfTest` failed on the rebased tree: `python -I` ignores PYTHONPATH, the worker could not import `zava_forward` (identify returned `ModuleNotFoundError`; editable installs point at the main checkout), so provision was `unsupported` and the verdict INSUFFICIENT.
* Live Azure cannot prove any criterion: the defect is in an offline fixture judge that no authorised demo resource runs. None used; no throwaway resource.

Planning Readiness: Ready. Disposition: executed.

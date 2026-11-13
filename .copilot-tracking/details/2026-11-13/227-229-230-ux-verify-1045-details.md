# Details: 227-229-230 UX verification (2026-11-13)

## Phase 2

* git show 499e6428a and fc68e7c60 from the read-only worktrees, write the 3 files to identical paths via git checkout of those blobs (git --git-dir read only), verify with cmp.

## Phase 4

* python3.12 -m venv /tmp/venv-227-1045 (fresh); PYTHONDONTWRITEBYTECODE=1 for all runs; pip install -e src/core src/agents src/api; verify concrete submodule origins (for example zava_forward.api.web or core module __file__) are under this worktree; confirm git status stays tracking-only afterwards.
* Limitation to report: the three modules do not directly exercise the #229 and #230 renderers; results are not renderer validation for those screens.
* From src/api: python -m unittest -v tests.test_safety_screens tests.test_procurement_screens tests.test_content_standard with PYTHONPATH=../core/tests:../agents/tests only if the component guide requires it (never mvp). Capture exit code directly.
* No browsers, Docker or network calls beyond pip index.

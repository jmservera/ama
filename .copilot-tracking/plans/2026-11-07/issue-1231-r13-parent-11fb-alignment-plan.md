# Plan: issue 1231 R13 alignment onto rewritten parent 11fb73f45

Date: 2026-11-07. Governing research: .copilot-tracking/research/2026-11-07/issue-1231-r13-parent-11fb-alignment-research.md. Critique: none run; the work is behaviour-preserving with no source decisions, and the author records this rather than claiming a critique.

## Phases

1. Commit these prospective records before any merge.
2. Recompute `git merge-tree --write-tree --merge-base=181a1c1bb HEAD 11fb73f45`; require a clean tree. Create the merge commit with `git commit-tree` (parents HEAD and 11fb73f45) and advance the current branch to it with `git merge --ff-only`.
3. Prove: parents, both ancestors, ranking source and tests identical to f87416add, main-drift files identical to 11fb73f45, diff scope against 11fb73f45 child-only.
4. Run focused checks with PYTHONDONTWRITEBYTECODE=1 and worktree src on PYTHONPATH: core ranking publication and runner tests, api wiring test, Ruff check and format on changed ranking files and src/api, mypy from src/core, git diff --check.
5. Write changes, author Review and state; commit once. Stop with a frozen clean candidate.

## Stop conditions

Any merge-tree conflict, a ranking-source difference from f87416add, or a failing focused test: stop and report; no repair beyond scope.

## Out of scope

FULL gate, SQL, browser, push, PR, retarget, ticks, parent worktree edits.

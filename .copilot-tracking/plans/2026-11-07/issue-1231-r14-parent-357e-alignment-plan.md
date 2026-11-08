# Plan: issue 1231 R14 alignment onto frozen parent 357e842d

Date: 2026-11-07. Research: .copilot-tracking/research/2026-11-07/issue-1231-r14-parent-357e-alignment-research.md. Critique: none run; behaviour-preserving, no source decision.

1. Commit these records before the merge.
2. Require a clean merge-tree with --merge-base=11fb73f45; commit-tree with parents HEAD and 357e842d; ff the branch.
3. Prove ancestry and source drift (only #891 files vs the old child; child-only 8 ranking files vs the parent).
4. Focused checks: core publication and runner tests, API wiring and chat panel tests, Ruff, format, mypy, diff check.
5. Commit changes, author review and state; freeze; then run the admitted FULL tip gate if every admission condition holds, no commits after.

Stop on conflict, drift or failing focused check. Out of scope: push, PR, retarget, parent edits.

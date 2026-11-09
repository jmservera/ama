<!-- markdownlint-disable-file -->
# Plan: post-policy validation of recovered #123 on current main, 2026-11-09

Research: [research](../../research/2026-11-09/postpolicy-validation-123-research.md). Details: [details](../../details/2026-11-09/postpolicy-validation-123-details.md). Critique: [critique](../critiques/2026-11-09/postpolicy-validation-123-plan-critique.md).

## Phases

* [x] Phase 1: reconcile. `git merge --no-ff origin/main` locally into the clean frozen candidate (untracked evidence files do not overlap main). Preserve both parents; no rebase, reset, stash or force.
* [x] Phase 2: verify merge. Confirm candidate's old base, frozen HEAD and old remote head `cfd1bca` are ancestors of the merge; the merge's second parent is `9814cf6b2`; the source/test diff between frozen HEAD and merge is empty; `git diff --check` is clean.
* [x] Phase 3: selected-tier checks from `src/core` using `~/.venvs/zf123-pinned`: `ruff check .`, `ruff format --check .`, `mypy`, and the 146-test selection with `PYTHONPATH=src:tests`; record versions, counts, skips, exits, and that imports resolve to this worktree.
* [x] Phase 4: documentation link/diff review of the merged policy files touched by both sides (`docs/reference/log.md`, `docs/reference/README.md`, `src/README.md` relative links) by a bounded script-free read of the merged diff and a link-target existence check.
* [x] Phase 5: record changes and one review; commit this lane's evidence only; write handoff.

## Stop conditions

A merge conflict, failing selected test or lint/type error: diagnose; change source only for a confirmed regression coupled to this merge, otherwise report the blocker. No push, PR/issue/board action, rebase, reset, force, global or uv install, Azure/model/private data/credential reads, full gate, SQL/API/browser runs (no main path requires them). `fairness_evidence=False` and `activation_allowed=False` stay unchanged. One critique and one review only; no correction-cycle spent unless a regression is confirmed.

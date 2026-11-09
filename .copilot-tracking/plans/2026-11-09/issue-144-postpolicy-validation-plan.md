# Plan: issue 144 post-policy validation (2026-11-09)

Research: `.copilot-tracking/research/2026-11-09-issue-144-postpolicy-validation-research.md`. Details: `.copilot-tracking/details/2026-11-09/issue-144-postpolicy-validation-details.md`. Written before any validation command was run.

## Objective

Produce fresh, genuine local evidence that the frozen candidate `63d7f8c1` still passes the selected checks and still merges with current main `9814cf6b`, without source change.

## Tier and basis

Owner-selected demo-targeted tier under the current focused tier of `.github/copilot-instructions.md`. Basis: one header added to `AzureTaskQueue._call`; no workflow, dependency, image, permission, secret, gate or SQL change; full gate and `rpi-checks --all` are not run by owner direction. A failing selected check blocks and is not waivable.

## Phases

* [ ] Phase 1: re-verify identities (HEAD, tree, clean status, fetched main, ancestry, merge-tree) and the venv editable paths.
* [ ] Phase 2: run the 49-case suite with the README helper `PYTHONPATH`, no skips allowed; report counts and skips from the runner.
* [ ] Phase 3: run the contract tests verbosely (`RequestDateTests`) and show the negative path: stale or missing date gives 403 and `QueueError`; confirm no network access by checking the tests use only the injected transport.
* [ ] Phase 4: `ruff check .`, `ruff format --check .`, `mypy` from `src/agents`.
* [ ] Phase 5: record changes, review and state; commit records only; verify source, tree of `src/` unchanged versus `63d7f8c1`, clean worktree.

## Decisions

* No merge of main into the candidate: the delta is documentation and policy only, `git merge-tree` is clean, and merging would add commits for no source reason. The relation is recorded instead.
* No rebase, push, PR, issue or cloud action.
* No source change unless a selected check fails and the failure is tightly coupled to the Date change.

## Success criteria

* Every command's exit code, counts and skips recorded from real output.
* `git diff 63d7f8c1 HEAD -- src` is empty at the final head.
* Original adverse review and C1 outcomes remain unmodified.

## Critique (one pass, executed before implementation)

Verdict: proceed with amendments, all applied.

* Risk: counting "OK" without the runner count would hide skips. Applied: phase 2 records `Ran N tests` and any `skipped=`; zero skips required, otherwise state them.
* Risk: citing the old approval as the new head's approval. Applied: the final records say independent approval covers only `63d7f8c1`; records-only commits need the reviewer to confirm that `src/` is unchanged.
* Risk: venv reuse with stale editable paths. Applied: phase 1 verifies paths; reinstall only after a missing dependency.
* Risk: wrong claim of live proof. Applied: no Azure claim; `Refs #144` only.
* No conflict with a confirmed owner decision was found; nothing needed a user decision.

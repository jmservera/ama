<!-- markdownlint-disable-file -->
# Details: issue #81 parent re-alignment (2026-11-07)

Plan: [plan](../../plans/2026-11-07/issue-81-realign-r2-plan.md).

## P1 Wait and pin

Poll `gh run view 42361331168 --json status,conclusion` at bounded intervals (at most 600 s per wait). After completion run `git fetch origin main`, record the SHA, `git log HEAD..origin/main`, and `git diff --name-only` against `312fa3dcc`. A score-only commit is expected to touch only `.github/rubric/scores/latest.json` and `docs/` rubric files.

## P2 Backup and prospective commit

* `git update-ref refs/ama/issue81-r2-pre-realign c5edb320ad10d3d73bb985bfb82b2d0bee94381a` (local only); the earlier `refs/ama/issue81-start` (`af891a5cc`) stays.
* Repository-local identity from a fresh `gh api user`; Conventional Commit with the Copilot trailer.

## P3 Rebase

`git rebase origin/main`. On conflict: inspect both sides, keep main's additive `checklist_rows`/`checklists.csv` and the parent's gate changes, never `-X ours/theirs`, never drop a hunk. If intent is unclear, `git rebase --abort`, record evidence, stop.

## P4 Proof

* `git merge-base --is-ancestor origin/main HEAD`; use `git range-diff` between the pre-realign commits and the rebased commits.
* Per-path `git ls-tree` comparison against `refs/ama/issue81-r2-pre-realign` for every path in the earlier 48-path inventory (`/mnt/ama-gates/restart-1106-81-integration/child-inventory-start.txt`, preserved) and the 2026-11-06 records.
* `git diff origin/main HEAD --stat -- src` must show only the three children's source and tests.

## P5 Commands

Run from scratch env; record commands, exits, counts and skip reasons in the changes record. Failures preserved as adverse evidence.

## P6 Checkpoint

Append a dated addendum section (new heading, no edit of earlier sections) to `docs/architecture/cutover-evidence-pack.md` with pinned identities, covered PRs, requirement traceability (PRD FR-008/FR-016/FR-017 versus BRD numbering), exclusions, actual commands and skips, classifications, gaps, owners and resume conditions, recommendation. State that receipt r15 is invalid for the new main. Update `ms.date`.

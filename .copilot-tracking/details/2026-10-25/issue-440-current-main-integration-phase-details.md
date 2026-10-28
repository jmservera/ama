<!-- markdownlint-disable-file -->
# Phase Details: Issue 440 current-main integration

Plan: .copilot-tracking/plans/2026-10-25/issue-440-current-main-integration-plan.md

## P02 Merge details

* Command: git merge --no-ff origin/main with a Conventional Commit message ("chore: merge origin/main into stabilization checkpoint branch", Refs #440, Copilot trailer). Author and committer email 8036360+jmservera@users.noreply.github.com.
* Expected conflicts: docs/reference/README.md and docs/reference/log.md only (from git merge-tree at f1e2d830 vs ea5577b2). Any other conflict stops the merge for review.
* log.md rule: result equals main's file followed by this branch's added lines. Verify by checking that every line of origin/main:docs/reference/log.md is present in order, and every branch-added line is present.
* README.md rule: take main's file, re-apply the branch's one #440 pointer, keep main's ms.date if later.
* Merge abort is allowed before commit if verification fails; nothing is discarded because the tree is clean at 65c8708d.

## P03 Cheap checks

* git diff --check origin/main...HEAD; link check of relative links in the changed docs with a small script; python3 tools/rpi-checks.py --help to confirm there is no cloud flag. No heavy gate and no test suites outside the one final gate unless the correction procedure triggers.

## P04 Evidence edits

* Append-only. The first-checkpoint section keeps its 2026-10-23 text. The new note states that its main pin is historical, that main now includes #360 changes not assessed by it, and does not rewrite the 17383 ms record.

## P05 Gate

* Preconditions: clean tree, HEAD contains origin/main, output path absent, lock free or timeout set to 14400, no other rpi-checks process of this task.
* Launch via bash async with output to an external log next to the out path; record PID. Report PID and log. Verification afterwards with --verify-receipt <out>/receipt.json --base <fresh SHA>.

## Validation Matrix

| Step | Evidence | Pass signal |
| --- | --- | --- |
| Merge | git diff, byte-preservation check | no lost lines, only expected files |
| Cheap | diff --check, links | exit 0 |
| Gate | rpi-checks --all | exit 0, all groups pass, benchmark under 1500 ms |
| Verify | --verify-receipt | exit 0 |

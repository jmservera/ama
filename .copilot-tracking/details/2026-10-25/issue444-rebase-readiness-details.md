# Issue 444 rebase and readiness details

Date: 2026-10-25. Plan: ../../plans/2026-10-25/issue444-rebase-readiness-plan.md.

## Phase 2

* Record the pre-rebase tip in a local backup ref `refs/backup/444-pre-rebase-6878d6ec` (local only, not pushed) so original history stays recoverable; the remote still holds e1bb33ef until the lease push.
* `git fetch origin main`; `git rebase origin/main` (the merge commit 2049b3b2 is linearised; its content is replayed by the rebase). On conflict: log.md keep all main entries then the #444 entries; latest.json take main's (`git checkout --ours` during rebase means main).
* Re-verify the repo-local noreply identity; rebased commits keep the Copilot trailer.
* Commit evidence for this task before the gate. Include artifacts for this phase set (research, plan, details, critique, changes, review, state).

## Phase 4

Venv /tmp/ama444/venv (pip only). Run resident core/api tests, full core and api suites, ruff, mypy, browser check on a free port and temp data. Clean ignored caches (`git clean -fdX`) before the gate.

## Phase 6

`git fetch origin main`; compare to the gate base; `python3 -B tools/rpi-checks.py --all --base <origin/main> --out <new dir> --lock-timeout 14400`; official `--verify-receipt`. Then `git push --force-with-lease=feat/resident-feedback-preview-444:e1bb33efe186d7c454053d7d4c9b591eba529081`. Check the remote for bot advances first; if moved, inspect the delta and refresh the gate.

No web edits planned; if any arise, fetch current web-interface-guidelines first and disclose no screen-reader audit and partial Fluent 2.

## Critique amendments (applied directly)

* C1: Phase 3 is stop-and-report, not source change.
* C2: after the rebase verify log.md has every main entry followed by the complete six-line #444 entry, and that `git diff 6878d6ec HEAD -- src/core/src/zava_forward/core/resident_preview.py src/api/src/zava_forward/api/resident_preview` is empty plus no #444 path is lost.
* C3: the changes artifact records the superseded bot commit e1bb33ef (`chore(rubric): record score 64/100`, rubric/score SUCCESS on the old head), the rationale, and that the rubric workflow re-scores on synchronize.

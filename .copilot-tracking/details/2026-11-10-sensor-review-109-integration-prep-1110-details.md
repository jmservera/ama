---
title: Issue 109 sensor-review stack integration details
ms.date: 2026-11-10
task_id: 109-integration-preparation-1110
---

Plan: [plan](../plans/2026-11-10-sensor-review-109-integration-prep-1110-plan.md). Research: [research](../research/2026-11-10-sensor-review-109-integration-prep-1110-research.md).

## Phase 3 details (future, after Root admission)

### Step 3.1 Identity re-verification

* Inputs: Root-stated merged remote parent head `P`; `git fetch origin`.
* Record: `HEAD`, `origin/main`, `P`, `git merge-base HEAD P`, ancestry of `2b050647bff51eef4c1b34d6434bba7eae3d5f9a` in `P`, tree ids, `git status --short` empty, `git config --local user.email` equals `8036360+jmservera@users.noreply.github.com` (re-resolve with `gh api user` if in doubt).
* Success: all recorded, worktree clean, no unexpected main movement. Failure: stop for Root.

### Step 3.2 Prospective witness

* Strict unique-key validation of the state file in its own successful call, then `implement-start` in a separate call. Refusal stops and is preserved.

### Step 3.3 Ordinary merge

* `git merge-tree --write-tree --name-only HEAD P` first. Exit 0 and no paths expected, given the current prediction (tree `b7d5494fa300ef65a8795da88ffe3c3d7375b4b6` for main plus child head `2b050647b`).
* `git merge --no-ff --no-commit P`. Verify `git diff --name-only --diff-filter=U` is empty.
* Content invariants to assert by hash after staging: `sensor_review_draft.py`, `test_sensor_review_draft.py`, `test_sensor_review_draft_api.py`, `ops.js` equal the blobs in `P`; `device_registry_azure.py` and `test_device_registry_azure.py` equal main; `src/core/pyproject.toml` parses and holds both sides' intent.
* Not allowed: rebase, reset, amend, force, cherry-pick, patch apply, copy of child source into this branch, hand-authored source.

### Step 3.4 Targeted checks

Run the numbered checks from the plan, saving raw output and exit codes outside the worktree. Report each as run, skipped or not run with reason.

* SQL selector `tests.test_sensor_review_draft.MssqlDraftCases` (22 expected, 0 skips), single `flock -n /tmp/ama-rpi-heavy.lock` attempt with actual-holder identification; do not queue, spin or kill; own disposable container only; secrets not written to logs.
* Mypy prerequisite: record the `azure-iot-hub` and `six` import availability before running; a missing dependency is a prerequisite blocker.

### Step 3.5 Changes record and `implement-done`

* Replace the Prospective section of the changes record with actual results, keep the original prospective text as written, and record divergences, conflicts and defects (none expected). Strict validation then marker `implement-done` in separate calls.

## Phase 4 details (future)

* One Review of the staged merge and records (functional correctness of composition, evidence honesty, claim boundaries). Findings route to later work. Marker `review-done`.
* Commit the merge with the Conventional Commit subject `chore(sensor-review): integrate sensor review stack with main (Refs #109 #111)`, Copilot trailer, repository-local noreply identity. Record the literal HEAD, marker `commit-complete`, `verify`.
* No push, PR or GitHub mutation unless Root instructs. A later PR uses `Refs #109 #111` and lists unmet criteria.

## Follow-up details (Root)

* New #440 sensor-integration checkpoint covering the integrated surface: BRD FR-048, PRD FR-050 with AC-066 to AC-068, ADR 0003 decision 6, code, tests and remaining backlog; separate local observed, Azure observed, implemented-unverified, deferred, blocked and unknown. Gate epic closure and dependent expansion on blocking findings only. Requires owner approval for any pivot or deferral.

## Open prerequisites

* PR #1395 merge method and resulting `P` unknown.
* Hosted CI for the exact child head incomplete at preparation time.
* Heavy-lock holder unknown (not probed here; no runtime checks in this invocation).
* Dev-environment parity with main's new `azure-iot-hub` and `six` extras.

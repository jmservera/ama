---
title: Issue 1292 startup diagnostic record qualification details
ms.date: 2026-11-09
task_id: 1292-startup-diagnostic-qual-1109
---

## Steps

* Step 1 Verify read-only: `git status --short --ignored`, `git rev-parse HEAD HEAD^{tree}`, `git merge-base --is-ancestor 8aea86f8b HEAD`, `git diff --stat ef28d4da4 HEAD -- src infra tools .github pyproject.toml`, `git ls-tree -r HEAD` blobs of the seven originals, `sha256sum -c SHA256SUMS` in the raw directory, `sha256sum SHA256SUMS`, a read of observer JSON events and `.meta`, and, as already performed once during research, a permitted remote-tracking `git fetch origin main` (no merge, rebase or push) with `git diff --name-only ef28d4da4 origin/main -- src` for informational drift only. Baseline sha256 of the seven originals, the raw manifest and the external handoff are captured first.
* Step 2 Create `.copilot-tracking/changes/2026-11-09-startup-diagnostic-1292-qual-changes.md` (qualification), `.copilot-tracking/reviews/2026-11-09-startup-diagnostic-1292-qual-review.md` and `.copilot-tracking/rpi-sessions/2026-11-09/startup-diagnostic-1292-qual-state.json`.
* Step 3 Verify originals unchanged with `git diff 59accfa1c HEAD --name-status` (only additions) and by re-hashing the seven working-tree files and the external handoff against the baseline, check ASCII and relative links, then commit with repository-local privacy email and trailer.
* Step 4 Write the session handoff `handoff-1292-record-qualification.md` outside the repo.

## Boundaries

* No edit to the seven original records or the raw directory. No rerun. Mark every recomputed number as read from the retained files.

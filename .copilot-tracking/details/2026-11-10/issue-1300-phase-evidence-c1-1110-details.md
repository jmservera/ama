---
title: Issue 1300 C1 correction details
description: Phase details for C1 helper corrections
ms.date: 2026-11-10
---

## Design

* `contained(repo, path)`: resolve repo, then `repo/.copilot-tracking`, then the target; return true only if the tracking root is under the repo and the target is under the tracking root. `inside_tracking` calls it. Resolution reads symlinks but never file content.
* `log_paths` callers check `contained(repo, log directory)` first. In record a failure is a printed refusal with exit 2 and no log or lock is opened; in verify it is a finding with exit 1 and the log is not read.
* verify artifact re-check: if the recorded path is not contained, add a finding `artifact path escapes tracking; not read` and skip the open and hash.
* Missing launch: in record, predecessors for any event of order greater than 0 are `EVENTS[:order]`, so `research-open` without launch is qualified. verify requires every event in `EVENTS`.
* Early source change: at `implement-start`, take the earliest earlier ok record that has a HEAD. If its HEAD differs from the current HEAD, run `git diff --name-only <earlier> HEAD`. Non-tracking paths produce a qualification naming them. A failed diff, for example a non-ancestor, produces `unable to compare`. Same HEAD adds nothing. Edit and revert activity that Git never shows is not claimed detected.
* Test fixture: `full_run` opens with a launch whose brief lives outside the repo; a parameter lets tests omit it.

## Critique revision 1 (applied)

* Containment also covers the `events.jsonl` and `events.lock` targets, checked before any open, and `dirty_identities` hashes a tracking path only when contained.
* Early-source comparison checks `merge-base --is-ancestor` explicitly; non-ancestor is `unable to compare`. Diff output uses `-z`.

## Not changed

Rename handling, commit-claim logic, stale-review logic and the step 5 procedure (apart from any wording made inaccurate by the launch requirement).

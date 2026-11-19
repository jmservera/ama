---
title: Issue 184 child stories changes
ms.date: 2026-11-19
---

Tier: FOCUSED (documentation only; no src change; rpi-checks --all not run).

Process deviation, recorded honestly: the evidence note, index row and log entry were written before this changes file and the `implement-start` witness call. They are documentation only.

The state file path was already tracked from an earlier run of this issue (commit 954c26300, which expected #185 and #189 to be open); it is overwritten for this task.

## Files

* docs/reference/research/issue-184-child-stories-demo-2026-11-19.md (new)
* docs/reference/README.md (index row)
* docs/reference/log.md (entry)

## Per-criterion table

| Criterion | Proven for the demo | Basis |
| --- | --- | --- |
| All child stories closed or deferred | Proven (backlog state) | Five sub-issues #185 to #189 closed as completed; summary 5 of 5 |
| Simulator never connects to, discovers or represents installed real devices | Not re-run (already ticked) | none added |
| No device key or connection string in source, logs or telemetry | Not re-run (already ticked) | whole-source and log scans remain unproved |

Unmet by this change: the checkbox itself stays unticked for the owner or coordinator; child acceptance criteria were not re-audited.

## Validation

* Relative links in the new note and index row checked by reading the diff.
* `git diff --check` run before commit.

Witness: `implement-start` and `implement-done` were refused (seq 4, 5) because the state file did not yet point to this changes file; they were retried after the state was updated, out of order, and `review-done` carried a missing-predecessor qualification. Logs are unedited.

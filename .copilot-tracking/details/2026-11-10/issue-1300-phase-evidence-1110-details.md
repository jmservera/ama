---
title: Issue 1300 phase witness details
description: Phase details and acceptance mapping
ms.date: 2026-11-10
---

## Helper contract (`tools/rpi_phase_witness.py`, standard library only)

* `record EVENT --repo R --issue N` with optional `--state`, `--brief`, `--session`, `--actor`, `--claim-model`, `--claim-commit`. Events: `launch`, `research-open`, `plan-done`, `implement-start`, `implement-done`, `review-done`, `commit-complete`. No time argument exists; the UTC value is always the invocation clock, and an unknown time option is rejected.
* `verify --repo R --issue N [--json]` re-reads the log and the current tree.
* Log: `R/.copilot-tracking/phase-witness/issue-N/events.jsonl` under an exclusive `flock`, one append write per record with fsync. Each record has seq, prev hash, own hash, UTC, monotonic ns, issue, worktree real path, HEAD, tree, scoped dirty identities, artifact identities (sha256, size, mtime), brief sha256, outcome (`ok` or `refused` with reasons), and a separate `asserted` object (actor, session, model labels) never treated as observed.
* Evidence required for `ok`: artifacts named by the canonical state `artifact_paths` must exist, be non-empty regular files whose real path stays inside `R/.copilot-tracking`; each event also needs the preceding event recorded `ok` (`research-open` < `plan-done` < `implement-start` < `implement-done` < `review-done`). `commit-complete` needs `--claim-commit` equal to actual HEAD, HEAD differing from the `implement-start` HEAD and descending from it, and no dirty source.
* Refused attempts are written as `refused` records and exit 2; they are never removed.
* Dirty scope: source = porcelain paths outside `.copilot-tracking/`; artifacts = inside. `implement-start` with dirty source is recorded and qualified ("edits predate the changes witness").
* `verify` reports: missing or out-of-order events, refused attempts, backward clock qualification (UTC earlier than previous), torn tail line, broken chain, review bound to a source digest that no longer matches (stale), artifacts changed since observed, and always the limits statement. Exit 0 only when no qualification; 1 otherwise.
* A torn final line (interrupted writer) is kept; the next record starts on a new line and chains from the last valid record.
* No environment, remote URL or config capture; Git is run with a fixed argument list.

## Coordinator step 5 adoption

* After writing the unique brief, run `record launch` with the brief path, session name and `--claim-model claude-sonnet-5.5` before the tmux command.
* The brief tells the worker to call `record` at each boundary (research opening before substantive search, and so on) from the coordinator's checked-out helper.
* The verification paragraph runs `verify` and treats its qualifications as observations, never proof of unobserved reasoning; it keeps original and adverse records.

## Acceptance mapping

| AC | Evidence |
|---|---|
| AC1 | Research trace table, ownership table |
| AC2 | Helper, tests, step 5 adoption; host blocker recorded as external |
| AC3 | Focused tests now; genuine native exercise Deferred to coordinator with plan in handoff |
| AC4 | No edits to 152/1298 artifacts; verified by diff |

## Tests

Cases: actual clock versus injected caller time, missing artifact, out-of-order event, commit claim without commit, stale review source, dirty source at start, interrupted torn append, concurrent writers, backward clock qualification, refused retention, path escape via symlink.

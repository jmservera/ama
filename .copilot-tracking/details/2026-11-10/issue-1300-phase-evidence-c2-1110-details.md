---
title: Issue 1300 C2 details
description: Phase details for the external evidence lifecycle
ms.date: 2026-11-10
---

## P1 helper

* `log_paths(repo, issue, evidence_dir=None)`: default unchanged; with a directory, `evidence_dir/issue-N/events.jsonl|events.lock`.
* `evidence_contained(repo, issue, evidence_dir)`: absolute; resolved directory not inside resolved repo; resolved issue directory, log and lock stay under the resolved directory. Checked before any mkdir, read, hash or lock open. Failure: record prints refused exit 2; verify reports a finding and reads nothing.
* Binding: before append, existing records whose `worktree` or `issue` differ from the invocation refuse with exit 2 without writing. Verify adds a finding per mismatching record.
* Verify report gains `final` (head, tree, log sha256) and a finding when the last `commit-complete` head differs from HEAD.
## P2 tests
Extend `WitnessCase` with an optional evidence dir helper; new class `ExternalEvidenceTests`.
## P3 step 5
Add the directory to launch, worker calls, verify, SQL hash record; state that the log is retained, never committed or deleted, and may be archived under the tracking retention policy.

## Critique amendments
O_NOFOLLOW on final components; require `--repo` equal to Git worktree root in external mode; binding check inside the append lock with no write on mismatch; verify hashes the bytes it parses; step 5 uses `verify --json` and records `final.log_sha256`.

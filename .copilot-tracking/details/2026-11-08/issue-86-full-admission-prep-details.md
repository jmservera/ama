---
title: Issue 86 prospective FULL admission preparation details
description: Verification commands, stop conditions and source qualifiers for the future FULL admission
ms.date: 2026-11-08
---

Scope: issue #86 only. The commands below are for a future admitted run; only read-only git and file inspection happened in this continuation.

* Ancestry: `git merge-base --is-ancestor X HEAD; echo $?`, one check per pin, never an OR or `&&` form.
* Main delta: `git diff --raw <child-base> <fresh-main>`, then blob and mode per path; the only executable paths allowed are `src/api/tests/assistant_process_worker.py` and `src/api/tests/test_assistant_release.py` before any merge proceeds.
* Rubric: `git show <main>:.github/rubric/scores/latest.json` must parse as JSON, with mode and blob equal to Main.
* Incoming delta: `git diff --raw $(git merge-base HEAD <fresh-main>) <fresh-main>`, not a direct child-versus-Main diff.
* Source qualifier after the future merge: `git diff --name-only <pre-merge-head> HEAD -- src tools infra .github` lists only the declared Main files plus `.github/rubric/scores/latest.json`, which has its own mode, blob and JSON-parse proof against Main.
* Old tracking: the 47 blobs incoming from `c5edb320` and every prior issue-86 record equal their pre-merge blobs.
* Runner command: plan step E. Path length: the resolved `--out` byte length must be at most 58 and the path must not exist.
* Verifier: plan step G. Return head, tree, base, receipt SHA, selected, executed and skipped groups, tests and skips with reasons, jobs and shard values, image and environment identities, paths and exits.
* Failure handling: a failed or missing prerequisite blocks FULL; no cloud fallback, partial substitute, scanner skip or fake context. Resume only under the maintained `--resume` rules at the same head, base and tool identity.

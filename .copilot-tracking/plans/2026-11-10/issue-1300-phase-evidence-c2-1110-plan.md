---
title: Issue 1300 C2 plan, external runtime evidence lifecycle
description: Plan for one source correction C2
ms.date: 2026-11-10
---

## Phases

* [ ] P1 Helper: add optional `--evidence-dir` (absolute) to `record` and `verify`; log and lock under `{dir}/issue-N/`; fail closed on bad directory, containment escape, and issue or worktree mismatch; verify reports final head, tree and log sha256 and qualifies HEAD moved past `commit-complete`.
* [ ] P2 Tests: add to existing test file a launch-through-commit-complete synthetic regression leaving the temp Git candidate entirely clean (`git status --porcelain` empty), verifying external log hash and final identity; wrong-repo, in-repo evidence dir, symlink-substituted dir, relative dir, and lock-in-external cases. Existing tests unchanged.
* [ ] P3 Step 5: pass `--evidence-dir {evidence-dir}` (coordinator-owned absolute directory outside every worktree) to launch, to the brief for worker calls, and to verify; record log sha256 in session SQL; no deletion. Only tightly coupled wording.
* [ ] P4 HVE: static closure, one fresh behavior campaign (boundary changed), final host validation, focused checks.

## Non-goals

No change to default in-tree behavior, generic dirty checks, budget, D5, approvals, CI, dependencies. Not native fidelity; records are local observations, not attestation.

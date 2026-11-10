---
title: Issue 1300 C2 research, external runtime evidence lifecycle
description: Research record for correction C2 (opened 2026-11-10T04:13:37Z, state file written first)
ms.date: 2026-11-10
---

## Disposition

Executed. Opening state persisted at 2026-11-10T04:13:37Z (`.copilot-tracking/rpi-sessions/2026-11-10/issue-1300-phase-evidence-c2-1110-state.json`) before this research. Input: HEAD 5600fc93, source unchanged since 132df96. C2 of 5 admitted by the coordinator (three remain afterwards).

## Defect (independently confirmed, High)

`log_paths` in `tools/rpi_phase_witness.py` always places `events.jsonl` and `events.lock` under `{worktree}/.copilot-tracking/phase-witness/issue-N/`. `git check-ignore -v --no-index` on that path exits 1 here (no ignore rule), so the mandatory step 5 route leaves untracked runtime files. Committing the log before `commit-complete` makes it dirty again, and a later metadata commit moves HEAD past the claimed identity. Step 6 requires a clean frozen candidate; there is no declared lifecycle.

## Existing patterns

* `docs/reference/method/tracking-retention-policy.md` already uses owned external scratch and an external approved artifact store with hash verification for generated evidence; the repository gate keeps receipts external. Same principle applies: runtime evidence outside the candidate, bound by identity and hash.
* The helper already resolves paths and refuses containment escapes (`inside_tracking`, `log_contained`) and records `worktree`, `issue`, HEAD and tree in every record, so identity binding needs no new schema.
* The coordinator supplies absolute `--repo` and `--state`; an absolute `--evidence-dir` fits the same pattern.

## Findings for design

* Smallest lifecycle: optional absolute `--evidence-dir` on `record` and `verify`, trusted and coordinator-supplied. Log and lock go to `{dir}/issue-N/`. Reject a directory that resolves inside the repo; fail closed if the resolved log, lock or issue directory leaves the resolved evidence directory (symlink substitution) before any open.
* Bind records to issue and worktree: refuse writing to a log whose records name a different worktree or issue; verify reports such records as findings.
* Verify reports the actual final HEAD, tree and log sha256, and qualifies when HEAD differs from the `commit-complete` head.
* Keep the in-tree default unchanged so historical evidence is not relocated; step 5 supplies the external directory. Dirty, untracked and ignored-source checks are not weakened.
* Planning Readiness: Ready. Risk: external records remain locally writable observations, not attestation.

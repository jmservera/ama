---
title: Issue 1300 C2 changes
description: Changes record for C2, written before any source edit (2026-11-10)
ms.date: 2026-11-10
---

Planned edits, none made yet at the time this record was written:

* `tools/rpi_phase_witness.py`: optional `--evidence-dir`, containment, binding, final identity.
* `tools/test_rpi_phase_witness.py`: external lifecycle regression and misuse tests.
* `.github/agents/ama-backlog-delivery-coordinator.agent.md`: step 5 only.
* Then HVE and validation records.

## Implemented (appended after the source edits, 2026-11-10T04:16Z)

* Helper: `--evidence-dir` on record and verify; `log_contained` returns a reason (absolute, outside the worktree, Git worktree root required, resolved log and lock under the directory); `O_NOFOLLOW` opens; binding to worktree and issue checked under the append lock with no write on mismatch; verify hashes the bytes it parses and reports `final` head, tree and log sha256 plus a HEAD-moved finding. Default in-tree behaviour unchanged.
* Tests: five new `ExternalEvidenceTests` (clean launch-to-commit-complete regression, HEAD moved, inside/relative directory, substituted symlink, subdirectory repo, other-worktree binding) and an adoption needle. 30 tests pass.
* Step 5: `--evidence-dir {evidence-dir}` on launch, worker brief and `verify --json`; SQL records final identity and log hash; log never committed, edited or deleted.
* Residual: a local writer racing the trusted evidence directory between check and open is not closed.

## Amendment after static closure (2026-11-10T04:20Z)

Independent static review (Pass, one Medium) found step 5 still said a log path outside the tracking root is a qualification, which contradicts external evidence. Step 5 qualification list now names the artifact path, the log path outside its evidence directory, evidence bound to another worktree or issue, and HEAD moved past commit-complete. Wording only; behaviour tests unchanged. Static review of the final wording was not repeated; the behavior campaign runs on the final blob.

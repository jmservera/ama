# Research: issue 144 PR 1141 hosted conflict (2026-11-09, Refs #144)

Task: `issue-144-hosted-conflict-2026-11-09`. Parent: `issue-144-postpolicy-validation-2026-11-09`. Research disposition: executed (remote state, overlap) and reused (prior approved source evidence). Planning Readiness: Ready.

## Observed remote state (fetched 2026-11-09, fetch only)

* PR 1141 OPEN, base `main`, `baseRefOid` b46a9ad9 (stale), head `feat/slice-144` = 10d7caeed47bd4638dc62b5754db0302466c4aa6, identical to local HEAD. Owner remote head unchanged, so nothing to preserve beyond HEAD.
* `mergeable` and `mergeStateStatus` now report UNKNOWN (the brief recorded CONFLICTING/DIRTY). Hosted mergeability is recomputed by GitHub on demand and is treated here as an unverified server signal, not as evidence either way.
* origin/main is d4d6827fe60be651cd922ab9656688c18c978e1d (PR 1222, merged after the brief was prepared); it contains 76db469b and 9814cf6b. Merge-base with HEAD is still b46a9ad9.

## Overlap diagnosis (observed)

* Main delta since b46a9ad9: 294 files, 13993 insertions, 38 deletions, almost all tracking and documentation. Non-Markdown non-tracking files: `.github/rubric/scores/latest.json`, `src/core/src/zava_forward/core/paired_equity.py`, `src/core/tests/test_paired_equity.py`. No change to `infra/`, `tools/`, workflows, dependency manifests or `src/agents`.
* Branch delta since b46a9ad9 touching a main-changed path: only `docs/reference/log.md`. Both sides append after the same anchor line (10938 in the base): this branch adds the issue 144 entries, main adds roughly 130 lines of later entries.
* `git merge-tree --write-tree HEAD origin/main` exits 0 in both argument orders with tree c71557173e66f1b6171235f5737e66473d8ca3d6 and no conflicted path. In that tree both entries survive: the issue 144 entries (lines 10423, 11059, 11063/11065) and main's entries (through the 2026-11-09 E1 entry).
* Cause of the hosted CONFLICTING/DIRTY report: NOT established. The most likely candidate is both sides appending at the same anchor in `docs/reference/log.md`, which a different merge implementation can treat as a conflict while local `ort` resolves it; this is a hypothesis only. A local clean prediction is not hosted mergeability, so the real merge must be performed and reviewed, and hosted state re-observed only after the coordinator publishes.

## Source evidence reuse

* `git diff 63d7f8c1 HEAD -- src` is empty. The source head 63d7f8c1 carries the approved `x-ms-date` fix (`queue_azure.py:124`, independent-144-c1 approved).
* `src/agents` imports nothing from `paired_equity`; the main core change is outside the queue adapter surface. Residual impact is limited to the shared core package that agents tests import.

## Constraints

Owner demo-targeted tier (no `rpi-checks --all`), no push, PR, issue, board or workflow action, no rebase/reset/force, no AI or credentials, five-cycle limit not consumed (this is a main reconciliation, not a review correction). All 5 acceptance criteria of issue 144 remain unproven live; use `Refs #144`.

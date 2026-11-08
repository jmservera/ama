---
title: Ranking archive ancestor durability 1258 plan
description: Plan for issue 1258, syncing newly created ranking archive ancestor directory entries before publication is confirmed
ms.date: 2026-11-08
---

## Scope and tier

Task `1258-ranking-archive-ancestor-durability`. Worktree `/home/azureuser/source/ama-wt/issue-1258-archive-ancestors`, branch `fix/ranking-archive-ancestor-durability`, declared PR target `main`, base `f548b65f4aa31eb92a2cc9cb801130e422daed7f`. PR will use `Refs #1258`, `Refs #79`, `Refs #1231`; no closing claim until the reviewed evidence proves every criterion.

Tier FULL (issue criterion; persistence-integrity and security-sensitive behavior). Not downgradable for size.

Research: `.copilot-tracking/research/2026-11-08-ranking-archive-ancestor-durability-1258-research.md` (executed, Ready).
Details: `.copilot-tracking/details/2026-11-08-ranking-archive-ancestor-durability-1258-details.md`.

## Current ceiling

Planning only. Phases 1 to 4 below are NOT started; every checkbox is unticked. Implementation waits for coordinator admission and resumes in this same native session.

## Decisions (agent-recommended, within issue wording; revised after critique PC-001 to PC-006)

* D1 Sync newly created ancestors (option B); do not require a preprovisioned archive (option A needs owner approval; not taken).
* D2 Failure after link is `DurabilityUnconfirmedError`; record kept; no rollback.
* D3 Single fail-closed rule, no "missing at start" bookkeeping. On every confirmation (first writer, lost race and already-archived retry alike), after the archive directory sync, sync each ancestor directory of the real archive location, nearest first. Boundary rationale: an entry this process could have created needs write access to its parent, so the chain is the unbroken run of ancestors that are writable (`os.access(W_OK)`), ending after the first ancestor that is a mount point, at the filesystem root, or just before the first non-writable ancestor. Any `open` or `fsync` error inside that chain is `DurabilityUnconfirmedError` (no skipping of `EACCES`; this removes the earlier D4 skip and PC-002 risk). This covers partial creation by a failed earlier run, a concurrent creator whose sync has not happened, and retry after an ancestor-sync failure (PC-001).
* D4 Real path: use `os.path.realpath(archive_dir)` after `makedirs`, so symlinked components sync the directories that actually hold the entries.
* D5 Declared behavior change for owner/reviewer visibility: steady-state publication now issues extra directory syncs for writable ancestors inside the archive's filesystem. Outputs, results, names, modes, dates and error types are unchanged. If the owner prefers a narrower exact-created-set rule, it cannot be made retry-sound without extra state, so it is not planned. This is not a relaxation of any criterion.
* D6 Runner and API: update the path-free runner message to say "archive folder or a parent folder" and its assertion (PC-005); the API 409 text is already generic and stays.

## Phase 1. Red tests first (before any source edit)

Fixture note (PC-003): both existing test classes set `self.dir = tmp/"archive"`, so every existing test is already a first run with one missing component. Tests use `Path(self.tmp.name)` as the existing root, `root/"a"/"b"/"archive"` as the nested case, and a pre-created archive for the steady-state case. Directory syncs are labelled by device and inode against known paths; any unlabelled directory sync (ancestors above the temp root vary by host) is ignored by order assertions through a subsequence check, so tests do not depend on the host layout.

* [ ] 1.1 `PublicationTests`: nested missing ancestors. Expect the labelled subsequence file, unlink-stage, archive, b, a, root, and every directory sync after `link`.
* [ ] 1.2 `PublicationTests`: post-link failure of the sync of `a` only. Expect `DurabilityUnconfirmedError`, errno, `written True`, original `published_on`, record valid, `verify` clean, basename-only message, mode `0o600`.
* [ ] 1.3 Retry (PC-004): seed state independently, not via 1.2: create the nested directories and the record with a normal `publish`, then call `publish` again with the sync of `a` failing; expect `DurabilityUnconfirmedError` (not `already_published`). A separate call with the fault removed returns `written False` and the original date. This fails before the fix.
* [ ] 1.4 Partial creation (PC-001): pre-create `a` and `b` without syncing, publish with an unfaulted run and assert `a` and `root` are synced; a fault on `root` raises unconfirmed.
* [ ] 1.5 Lost race: use the existing `CommitGate`/link-racing pattern so the loser finds the record and the nested directories; assert it syncs the chain before `already_published`.
* [ ] 1.6 Symlink: archive reached through a symlinked parent; assert the real parent is the directory synced.
* [ ] 1.7 Boundary: a non-writable ancestor (mode change on a temp directory, skipped when running as root) ends the chain without error; a writable ancestor whose sync fails raises unconfirmed. Mount-point stop is asserted with a patched `os.path.ismount`; this is a mock boundary, stated as such.
* [ ] 1.8 `test_ranking_publication_runner.py` and `src/api/tests/test_ranking_publication_wiring.py` (PC-004): an ancestor-targeted sync fault yields `committed_unconfirmed` with audit uncertainty and a path-free 409; record preserved; the existing archive-directory fault tests stay.
* [ ] 1.9 Update `test_publish_syncs_file_then_removes_stage_then_syncs_directory` to the labelled-subsequence form (it already creates `archive`), keeping its intent: file, unlink-stage, archive directory, then the parent. Record this as an intentional existing-test change.
* [ ] 1.10 Run only the new tests on unfixed source; keep the failing output as the "fails before the fix" evidence. Scratch under a root external directory, not `/mnt`; no repo-local output.

## Phase 2. Source change (`src/core/src/zava_forward/core/ranking_publication.py`, plus the runner message only)

* [ ] 2.1 Add private `_ancestors(archive_dir)`: realpath, then parents nearest first, applying the D3 boundary.
* [ ] 2.2 In `_confirmed()`, after `_fsync_dir(archive_dir)`, call `_fsync_dir` for each ancestor; any `OSError` (including `open`) becomes `DurabilityUnconfirmedError` as today, so the record and audit path stay unchanged on every outcome.
* [ ] 2.3 Update the exception message to "archive folder or a parent folder", basename-only; update module and `publish()` docstrings (D5 wording).
* [ ] 2.4 Update the runner message (D6) and its tests only. Do not touch `store.py` or `server.py` unless a test proves it necessary; then record why.

## Phase 3. Green and regression

* [ ] 3.1 Rerun the new tests, then `test_ranking_publication*.py` in `src/core` and `test_ranking_publication_wiring.py` / ranking tests in `src/api` using the documented component commands with synthetic temporary data only.
* [ ] 3.2 Confirm existing event-order, retry, concurrent private-stage, audit, 409/503 and original-date tests pass unchanged.
* [ ] 3.3 State in changes evidence that mocked ordering is not real crash or filesystem durability proof.

## Phase 4. Gates and evidence (resume point: FULL)

* [ ] 4.1 Write changes and divergence records; commit implementation plus dated original RPI evidence on the branch.
* [ ] 4.2 Pre-push: after coordinator admission and a fresh fetch, run `python3 tools/rpi-checks.py --all --base <current origin/main> --out <new root external scratch dir>` and `--verify-receipt ... --base <current origin/main>` immediately before push. Receipt stays external. No reuse of any older receipt, no cloud fallback, no skip relabelled green.
* [ ] 4.3 One post-implementation review (`rpi-review`), then independent exact-head assessment. Any corrective commit invalidates the receipt and assessment and the gate is rerun on the new head (PC-006). Human approvals stay open.
* [ ] 4.4 Publish only when the coordinator admits: push, open a PR to `main` with `Refs` links, then hosted checks run and must pass on the same head (they cannot precede the push). #1259 then targets this branch and must consume its frozen source first.

## Risks

* D5 steady-state extra syncs; fail-closed on a writable ancestor whose sync fails (truthful `committed_unconfirmed`, not silent).
* fsync of directories can fail on exotic filesystems; that is already unconfirmed behavior for the archive directory and stays so.
* Mock ordering only; no real crash proof.

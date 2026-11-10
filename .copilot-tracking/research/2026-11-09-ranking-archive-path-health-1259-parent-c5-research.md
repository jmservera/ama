---
title: Issue 1259 frozen parent c5 integration research
description: Prospective research for merging the exact frozen 1258 Blob parent into the 1259 path-health child
ms.date: 2026-11-09
---

## Disposition

Research executed 2026-11-09 (qualified rpi-agent, Sonnet 5.5), before this task's plan, details, critique and any merge or source edit. Planning Readiness: Ready. Disclosure: the preparation record (`...-recovery-*`) ran its validation before its plan files were written; that ordering divergence is preserved there and is not claimed as ordered here. This task's phases are ordered: Research, Plan and Details, one Critique, then Implement and Review.

## Pinned identities

* Child worktree `/home/azureuser/source/ama-demo-wt/issue-1259-recovery`, branch `fix/ranking-archive-path-health`, clean at start, HEAD `9ff90e124bf14a996063e9f949c68f8a48e3415f`. Original fix `683ec2716ca8f0cb75d8156120e6a8a821403885` preserved. `git diff fab9159d9 HEAD -- src` is empty.
* Exact frozen parent commit `52f9b61bb22c5ceaaed0f9bf6a55dab7a7a59cb8`, tree `20901b61eddb68d3740f6976187d17ff5fc0cea2` (branch `fix/ranking-archive-ancestor-durability`, independent Functional C5 approve, 0 findings; coordinator handoff reports Core 137 and API 35 targeted checks). The merge uses this SHA, never the moving branch name. The parent is unmerged and unpublished; its source is not labelled as merged main.
* Fetched `origin/main` `daf45a46ca85b93cfac510ef6f8b2d685dec5136`. The parent's recorded base main `06e3f2f456ab008f8e41f013d9019c2d82ea05b9` is an ancestor of the parent. Main reconciliation of the stack is deferred to the coordinator's parent-current-main integration; shared #1292 is not imported.
* Declared PR target for this child remains the parent topic `fix/ranking-archive-ancestor-durability`, not main. Merge-base of child and parent: `6d793bc3ad3fd8427f745530a633bb1e553ec0ef`.

## Historical review-correction count (established first)

* Issue 1259 evidence: original 2026-11-08 Research, Plan, Details, one Revise critique (PC-001 to PC-007, applied before source), Changes, one author Review (Residual work, not independent); `-cont-` propagation of parent `6d793bc3a` (normal merge, no conflicts, author Review); 2026-11-09 recovery preparation on unchanged source (author Review). Issue comments (2026-11-08T03:22Z and 03:52Z) describe one implementation freeze. No independent assessment of any 1259 head has run, no PR exists, and no commit or record is a correction to an independent finding.
* Established count: zero productive review-correction cycles consumed for 1259. This task is the first, leaving four after it. Default five total; the preparation did not reset or grant cycles; no membership of the already-exhausted additional cohort is inferred. The parent's separate budget (five of five spent) does not transfer.
* Budget holds, so productive source change is permitted within this single scoped cycle.

## Merge dry run (read-only, `git merge-tree --write-tree --no-messages HEAD 52f9b61bb`)

* `src/core/src/zava_forward/core/ranking_publication.py`: two trivial hunks. Imports (the parent adds `contextlib`; the child adds `errno` and `stat`) and the `verify` signature and docstring (child: local-folder path health; parent: `Archive` union and the Blob listing raising OSError).
* `src/core/tests/test_ranking_publication_runner.py`: both sides append new test classes at the same spot; keep both.
* Auto-merged: `ranking_publication_runner.py`. The child's one-line `reason = e.strerror or "reason not available"` in `_verify` merges against the parent's runner where `_verify` is unchanged in text. Effect on Blob errors to be tested: `BlobArchiveError` is an `OSError` raised with a single message argument, so `strerror` is `None`.

## Intent of each side

* Child: a local archive location that is an existing non-folder, a dangling link, a non-folder ancestor or a stat failure raises a path-free OSError and is never healthy-empty; an absent creatable folder is a first run. Runner reason text is fixed path-free.
* Parent (owner decision 2026-11-08T18:44:58Z on #1258: Blob for ranking JSON): `Archive = Path | BlobRankingArchive`. `BlobRankingArchive.names()` pages the List Blobs result and raises `BlobArchiveError(OSError)` with fixed path-free text for a non-200 status, unreachable transport, authorization unavailable, malformed or structurally invalid body (c5 `_parse_listing`) and a listing that does not finish. `verify` lets that error propagate; the runner `_verify` turns any OSError into `unreadable: True`; schedule and publish treat unreadable as unknown/`archive_unreadable` with no PUT. Valid empty `Blobs` and multi-page listings are accepted. Store and API publication use a conditional create (`create`, If-None-Match) and never list. Existing parent tests: `BlobArchiveRunnerTests`, `VerifyTests`, `ConditionalCreateTests`.
* The two intents are compatible and not duplicates: the parent already carries the health semantics for the configured Blob archive. The child's local hunks apply to the `Path` arm only and remain at most fixture support. The real adaptation question is whether any Blob failure shape still lets an unknown archive look healthy-empty, or leaks a path or secret through the runner message.

## Candidate gaps to test failing-first (not yet known to fail)

* Runner reason text for a Blob listing error: the child's fixed fallback replaces `str(e)`, dropping the parent's fixed path-free message for `BlobArchiveError`. Safe but loses diagnostic value; to be decided against tests.
* Blob listing matrix through the runner for schedule, verify and publish: 403, 404 (missing container), 500, transport raise carrying a secret URL, malformed body, endless pagination. Existing tests cover 500 and two malformed bodies only.
* Store/API-level direct conditional publish must still succeed when the listing would be unreadable (no listing dependency).
* Local filesystem: the child's regular-file, dangling-link and absent-directory tests stay valid on the `Path` arm after merge.

## Constraints and exclusions

No rebase, reset, force, push, PR, issue or board change. No mount hardening, Azure activation, paid resource, retention change, private dataset or live Blob run. Mocked REST tests are not Azure acceptance. Production, live filesystem, WORM, deployment and migration criteria of #1259 stay unmet and unticked; literal issue text is not rewritten.

## Policy choices

No material unapproved policy choice identified yet. If the runner reason-text reconciliation needs one, it is recorded in the Changes and Review records and only that scope stops.

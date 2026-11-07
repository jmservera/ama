---
title: Issue 1231 r16 research, local alignment to parent79 87c027a30
description: Prospective research for aligning the child to parent79 87c027a30
ms.date: 2026-11-07
---

Date: 2026-11-07. Phase: Research for a FUTURE implementation. Planning only; no source, test or README edit was made in this turn. Research disposition: executed (read-only git inspection).

## Chronology and honesty notes

* r15 (a4ada1e91) edited source before research/plan were written and ran no critique, despite an explicit instruction. That deviation is recorded in the r15 research file and is preserved. It is not repaired or backfilled here.
* This r16 record is genuinely prospective: it is written and committed before any alignment merge or code change.
* r4, r7 (failed), r9, r11, r13, r14 and g79 receipts remain historical. None covers a4ada1e91 or any later head. r15 is not publication-ready.

## Pinned identities (read-only, verified this turn)

| Item | Value |
| --- | --- |
| Child branch | fix/ranking-archive-concurrent-writer-metadata |
| Child HEAD | a4ada1e91841143239a0aec33024e4b9788b05e5 |
| Child tree | 472f82b23c3d236bad3ca64e110bdf830174f88e |
| New parent79 | 87c027a30ba5a1dd5e4f16b01052e7c32a09138c |
| Parent tree | f391682d93bac1ce9ec256c6d02dfebf9bda4dc4 |
| Old declared parent | 357e842d064296d4764f087f7a39006cc702f4ee (ancestor of the new parent) |
| merge-base(child, new parent) | 357e842d064296d4764f087f7a39006cc702f4ee |
| Main | 0f420dc9514db22081cb48fa733267d9d33a0d24 (unchanged) |
| Dry-run merge tree | a00c8d197777bb8a6fe03b3d3ae074f5e0b19128 (git merge-tree --write-tree, one output line, no conflict; object only, no ref or worktree change) |
| Identity | repo-local 8036360+jmservera@users.noreply.github.com |

## Parent delta 357e842d..87c027a30 (two commits)

* 3e9983a69 docs(rpi): issue 79 r18 plan for the 357 assessment correction.
* 87c027a30 fix(core): policy validation, future archive date and blocked exit.
* Files: src/core/src/zava_forward/core/ranking_publication_runner.py (+52/-6), src/core/tests/test_ranking_publication_runner.py (+65), src/core/README.md (+4), docs/reference/log.md (+4), six issue-79 r18 RPI records.
* Parent does NOT touch ranking_publication.py, store.py, the API wiring test or test_ranking_publication.py.

Parent runner behaviour added:

* `_policy_problem`: registry key must be the same object as the policy version and `policy_hash(policy) == content_hash`; otherwise refusal `policy_invalid` before sign-off.
* `_future`: a latest archived date after the run date is a problem in `verify` and `schedule` (overdue/due become unknown) and refuses non-exercise `publish` as `archive_unverified` with the future text.
* `main`: status `blocked` now also exits `EXIT_REFUSED` (2).

## Child delta over 357e842d (source)

* ranking_publication.py: unique O_EXCL stage with mode 0600, fsync, os.link, owned-stage removal, `stage_retained` on the primary exception.
* ranking_publication_runner.py: `publish_failed` message/next action name the retained stage and return `stage_retained`.
* store.py: `_log_retained_stage` WARNING and path-free 503 sentence.
* Tests: umask 0022/0002 owner-only test, helper retained-name test, runner double-failure test, manager-route double-failure test, concurrent-writer metadata regressions.

## Overlap analysis

* Only ranking_publication_runner.py and test_ranking_publication_runner.py and src/core/README.md are changed on both sides.
* Child runner hunk is confined to the publish_failed refusal (stage_retained); parent hunks are in `_verify` neighbours, `run` verify/schedule/publish branches and `main`. The dry-run merge reports no textual conflict, but textual cleanliness is not semantic proof.
* README: both sides edit the same region neighbourhood; dry-run was clean, content must still be read.
* log.md is touched only by the parent (append-only). The child does not edit it, so no duplicate entry risk; do not edit it in the alignment.
* RPI records: parent r18 files are new paths; child r15/r16 paths are disjoint. Keep all.

## Semantic interaction risks to verify after the merge

1. Privacy: stage and final inode 0600 under umask 0022 and 0002; parent changes must not reintroduce a 0666 open.
2. Double failure: `stage_retained` still reaches runner refusal, Store WARNING and the path-free 503 with the parent's new refusal ordering.
3. Registry hash guard: `policy_invalid` fires before the publish helper, so no stage is created for an untrusted policy.
4. Future date: parent refuses publishing when the latest archived date is after the run date. Child concurrent-writer semantics (a loser returns the winner's later date as already_published, writtenFalse) happen inside the helper after the runner pre-check, so a future-dated winner is returned truthfully to the racing caller. A later sequential run is refused by the parent rule. These are different layers; verify neither masks the other and that no test is weakened.
5. Blocked CLI exit: `schedule` blocked returns 2; check that child tests asserting exits still hold and that `publish_failed` refusal still exits 2.
6. Import origin: tests must import zava_forward from this worktree src (print module `__file__`), not another worktree or an installed copy.

## Constraints and gaps

* Owner-only mode is proven only as the owning user on the local filesystem; no cross-UID claim.
* EPERM/ENOTSUP injection is not a real unsupported mount.
* A post-link directory-sync failure writes no audit entry (accepted residual).
* No heavy work admitted: #86 holds FULL. A new combined-tip FULL gate, independent exact-head assessment and hosted checks remain coordinator-owned before publication.

Planning Readiness: Ready, subject to the coordinator authorising implementation.

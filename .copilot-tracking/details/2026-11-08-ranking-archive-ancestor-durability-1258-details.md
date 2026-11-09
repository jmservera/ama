---
title: Ranking archive ancestor durability 1258 details
description: Phase details for the issue 1258 plan, including test shape, helper contract and gate order
ms.date: 2026-11-08
---

## Phase 1 details

* Fixtures: `self.dir` is `tmp/"archive"` and is not created in `setUp`; nested cases use `Path(self.tmp.name)/"a"/"b"/"archive"` with the temp root existing.
* Labelling: inside the patched `os.fsync`, `os.fstat(fd)` is compared with `os.stat` of the known candidate paths that exist at that moment; unmatched directory fds are `other` and removed before the subsequence assertion (ancestors above the temp root differ per host).
* 1.1 expected labelled subsequence: `file, unlink-stage, archive, b, a, root`, with `os.link` wrapped so all directory syncs are after it.
* 1.2 raises `OSError(errno.EIO)` only for label `a`; assertions: type, errno, `written True`, record valid, `verify` clean, message holds the record basename and not the temp path.
* 1.3 builds state independently (normal publish first), then fails `a` on the second call and heals for the third.
* The pre-fix run must fail 1.1 to 1.3 and 1.8 (no ancestor syncs, no raise); record 1.4 to 1.7 actual outcomes, do not force them.

## Phase 2 details

* `_ancestors`: `p = realpath(archive_dir)`; loop `p = dirname(p)`; stop if `dirname(p) == p` after yielding root; stop before `p` when `not os.access(p, os.W_OK)`; yield `p`; stop after `p` when `os.path.ismount(p)`.
* `_confirmed(outcome, archive_dir)` keeps its signature; the helper is private; `DurabilityUnconfirmedError` is unchanged.
* The loop is fail-closed: an `open` error such as `EACCES` on a writable ancestor is unconfirmed.

## Phase 3 and 4 details

* Core: `cd src/core && PYTHONPATH=tests python3 -m unittest tests.test_ranking_publication tests.test_ranking_publication_runner -q`.
* API: `cd src/api && PYTHONPATH=../core/tests:../agents/tests python3 -m unittest tests.test_ranking_publication_wiring -q`.
* Install `src/<project>` with pip from an out-of-tree export (avoid `build/` and `egg-info` in the checkout, which invalidate the gate); scratch, venv and receipt under a root external directory with `df` checked first.
* Gate order: commit, fetch, `--all --base`, `--verify-receipt`, push only after the coordinator admits and an independent exact-head assessment is arranged.

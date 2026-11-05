---
title: Issue 96 r16 export review-history changes
description: Changes, check evidence and scoped author Review for the history-in-Held-export increment
ms.date: 2026-11-05
---

## Changes

* `form_export.py`: `history` added to `BODY_KEYS` and the body (`report["history"]`, already a detached ordered copy from the visibility-preflighted `_report`). Legacy copies without it are Invalid through the existing path.
* `test_form_export.py`: two tests on JSON and SQLite: exact ordered history after accept, correct, reject plus a sibling, empty history, detached copy, stable repeat export, same-value new event changing the digest and making the older copy Stale; removed, reordered and legacy (digest recomputed over old keys) copies Invalid with the regenerate-Held action.
* `src/core/README.md`: contract and legacy compatibility documented.

## Checks (light only; FULL pending)

* RED against unchanged `HEAD` source (`git archive` copy, import proved): 3 errors in the two new tests, `/tmp/g96-r16-red.log`.
* GREEN: four form suites, 59 tests OK, no skips reported, exit 0, `/tmp/g96-r16-green.log`. Imports resolved from this worktree.
* Ruff check 0, format check 0, mypy 0 (267 files). Caches external.
* Deviation: an accidental `rm -f /dev/null` in one command failed with permission denied and removed nothing. A first RED attempt failed on a bad cp path before running tests.

## Self-review (author, scoped)

* Reuses the existing preflight, hash and Invalid path; no new reads, writes, endpoints or authority. Held, not reviewed, Not submitted and Not assessed are unchanged.
* The history contains reviewer email and free-text reasons; scope is synthetic data only per the owner answer. That is not DPO, Finance or Legal sign-off.
* Not shown: no negative-actor or unavailable-evidence test was added because those paths are unchanged and already covered by existing tests. Pending: coordinator-admitted FULL gate on fresh images and current main, independent exact-head review, published review and real-data approvals. C1, C5, C6 unchecked; `Refs #96`; PR target `feat/finance-integration-93`.

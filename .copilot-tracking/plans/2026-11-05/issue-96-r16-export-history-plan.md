---
title: Issue 96 r16 export review-history plan
description: Prospective plan and details for the history-in-Held-export increment
ms.date: 2026-11-05
---

## Phases

* [x] Phase 1: Research (r16 research file, read back before this plan).
* [x] Phase 2: Plan and details (this file), before any source or test edit.
* [ ] Phase 3: Implementation.
* [ ] Phase 4: Review (author, scoped honestly).

## Details

* `form_export.py`: add `history` to `BODY_KEYS`; body gets `history=deepcopy(report["history"])` (already a detached copy; deep copy again is unnecessary, so reuse it directly). Order preserved. No new reads or writes; errors unchanged.
* Legacy copies without `history` hit the existing KeyError path: Invalid with the regenerate-Held action. No backfill.
* `src/core/README.md`: state that the body now carries the recorded working field-review history (synthetic-data scope for now, reviewer email included), that history is not Finance pack approval, and that copies without it are Invalid and must be regenerated.
* Tests in `test_form_export.py` (JSON and SQLite): exported history equals the working report history exactly after accept, correct, reject; empty history is an explicit empty list; a same-value new event changes the digest and the older saved copy is unchanged; a returned history mutation does not alter the store; removed, reordered or edited history with a stale digest is Invalid; a legacy history-less copy, even with a digest recomputed over the old keys, is Invalid; no audit or case mutation.
* Existing fixtures that recompute digest over `BODY_KEYS` stay valid.

## Validation

Tier FULL, pending, coordinator-admitted later. Now: four form suites, Ruff check/format, mypy, external caches, import provenance.

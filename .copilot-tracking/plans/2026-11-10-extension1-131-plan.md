---
title: Issue 131 E1 missing households key (plan)
ms.date: 2026-11-10
task_id: 131-extension1-1110
---

## Objective

Reject a stored inventory revision that lacks the `households` key as malformed history in both the view and the writer, keeping explicit null as valid Unknown.

## Phases

* [ ] Phase 1: write red regression test (singleton and earlier revision missing the key, JSON and SQLite stores, plus explicit-null control); run it on the unfixed module and keep the log.
* [ ] Phase 2: require `"households" in revision` in `_inventory_history_ok`.
* [ ] Phase 3: ordinary `git merge --no-ff origin/main` after the implement-start marker; confirm the scoped files are unchanged by the merge.
* [ ] Phase 4: green targeted tests, Core and API resident suites, configured Core ruff check, format check and mypy; focused API resident run.
* [ ] Phase 5: complete changes record, single review, commit, witness events.

## Success criteria

* Red before, green after; no legitimate Unknown or stale-digest history rejected.
* mypy, format and ruff stay green; Core and API resident suites unchanged.
* Only `resident_decisions.py` and `test_resident_decisions.py` change in source; README untouched (no behaviour the README does not already state; corrupt history is already documented as malformed).

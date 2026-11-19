---
title: Issue 1258 criteria proof for the demo (2026-11-19)
description: Per-criterion evidence that the ranking archive ancestor durability fix is on main and what the demo cannot prove
ms.date: 2026-11-19
---

Scope: synthetic demo, desktop only. No Azure action was needed or taken, and no source changed.

## Evidence

* `src/core/src/zava_forward/core/ranking_publication.py` `_confirmed` fsyncs the archive folder and every parent before confirming, and reports `DurabilityUnconfirmedError` when a sync fails.
* `python3 -m unittest test_ranking_publication -q` from `src/core` with `PYTHONPATH=src:tests`: 57 tests, OK (2026-11-19).
* Tests cover nested ancestor order (`test_new_nested_ancestors_are_synced_after_link_deepest_first`) and post-link failure (`test_ancestor_sync_failure_after_link_is_unconfirmed_and_keeps_the_record`).

## Criteria

| Criterion | Status | Basis |
| --- | --- | --- |
| 1 to 4 (ticked in issue) | Proven, previously ticked | Tests above pass on this head |
| 5 Original RPI, FULL receipt, independent exact-head review, hosted checks | Not provable for the demo | Needs a FULL receipt, an independent reviewer and hosted CI on a pushed head. This task changes no src code, forbids `rpi-checks.py --all` and does not push. Mocks do not prove real crash durability. |

No unmet code criterion exists, so no implementation was done.

---
title: Issue 1258 live research
ms.date: 2026-11-22
---

Task: issue 1258, ranking archive ancestor durability. Research disposition: executed. Planning Readiness: Ready.

Findings (read-only):

* `src/core/src/zava_forward/core/ranking_publication.py` `_confirmed` syncs the archive folder and every opened parent (`_walk`) after link, on each confirmation including retries; failure raises `DurabilityUnconfirmedError` and keeps the record.
* `src/core/tests/test_ranking_publication.py` lines 320-441 cover nested ancestor sync order, post-link ancestor sync failure, retries and partial ancestors.
* Criteria 1 to 4 are already ticked. Criterion 5 is process: original RPI, current FULL receipt, independent exact-head review, hosted checks.
* No source change is needed, so tier is focused. The owner brief forbids `rpi-checks.py --all`, pushing and PRs.

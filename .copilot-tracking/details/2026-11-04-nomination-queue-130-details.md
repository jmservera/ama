---
title: Issue 130 nomination overdue queue details
ms.date: 2026-11-04
---

## Phase 1

* `src/core/src/zava_forward/core/taskqueues.py`: loop over `case["nomination_records"]` using the existing `deadline` helper with no completion evidence, so a past next update shows as an overdue task owned by the named owner (Unknown if absent). The overdue queue definition text is updated.
* The task is a staff prompt only. It changes no priority, consent, vulnerability, sanction, eligibility or hazard clock. Missing or invalid dates yield no task (never guessed).
* Existing consumers (`progress.py` counts, `exception_feeds.feed_stranded_tasks`) get an ownerless overdue nomination as a stranded task, which is the intended escalation to a human.
* Test: `test_overdue_nomination_next_update_is_a_staff_task_only` in `src/core/tests/test_taskqueues.py`.

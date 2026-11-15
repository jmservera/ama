---
title: Changes 153-c4-async-action-dedup-1953
ms.date: 2026-11-13
---

* `src/api/src/zava_forward/api/web/async-action.js`: `finish` returns messages already holding Owner plus Next action/step unchanged; default wording is now "check the recorded history before repeating anything".
* `src/api/tests/test_loading_feedback.py`: asserts exactly one Owner and one Next label for owned, stepped and plain failures.

Note: the first implement-start witness call was refused for a missing changes artifact; the edits were made in the same step and the call was repeated once this file existed.

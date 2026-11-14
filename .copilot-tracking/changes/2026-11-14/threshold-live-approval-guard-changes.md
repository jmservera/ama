---
title: Issue 146 live threshold approval changes
ms.date: 2026-11-14
---

Refs #146.

* `src/core/src/zava_forward/core/rai_release.py`: `named_human`, live approver gate.
* `src/core/src/zava_forward/core/cohort_eval.py`: `live`/`now` guard; `approve` accepts `Mapping[str, Any]`.
* `src/core/tests/test_rai_threshold_live_approval_guard.py`: 12 tests.
* Validation: ruff check/format, mypy clean; new suite 12 OK; `test_rai*`, `test_cohort_eval`, `test_resident_preview` and agents cohort suites OK. Hosted CI not observed; not pushed.

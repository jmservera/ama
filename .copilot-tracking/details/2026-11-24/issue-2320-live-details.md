# Details: issue 2320

* Files: `src/core/src/zava_forward/core/store.py`, `sqlstore.py`, test `src/api/tests/test_assistant_release.py`.
* Acceptance: the repeat briefing returns the same cached object, issues no `BEGIN IMMEDIATE` on the primary connection and appends no audit entry; the pre-existing recovery after a recorded release still yields an AI result.
* Limits: first GET after a data change still records (three writes); contention from other writers can still 503 that GET.

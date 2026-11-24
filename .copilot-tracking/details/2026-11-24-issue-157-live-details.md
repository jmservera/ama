# Details 2026-11-24: issue 157 live recheck

## Phase 1 tests
* `test_chat_privacy.py`: after `CHAT_RETENTION_DAYS=30`, a thread whose `created_at` is 31 days old is gone after `sweep_retention()`, a second call inside the interval does nothing (returns None), a call after the interval runs again; with no period recorded nothing is deleted.
* `test_chat_privacy.py`: with 50 stored items of which one is expired, `add_memory` succeeds (live count 49).
* Isolation test: `ChatIsolation.current_user` triggers the sweep so an expired thread is not listed afterwards.

## Phase 2 implementation
* `ChatPrivacy.__init__`: `self._swept: float | None = None`; constant `SWEEP_INTERVAL_SECONDS = 3600`.
* `sweep_retention(interval=SWEEP_INTERVAL_SECONDS)`: return None when last run within interval; otherwise record time first (so failures do not retry every request), call `purge_retention`, log failures with `logging.warning` and return None.
* `ChatIsolation.current_user`: call `self.privacy.sweep_retention()` first.
* `add_memory`: count `self._live(owner)` rather than `repo.memories(owner)`.

## Dependencies
None beyond existing modules.

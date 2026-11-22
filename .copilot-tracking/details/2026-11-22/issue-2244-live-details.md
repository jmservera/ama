# Details: issue 2244

* `LOCK_RETRY_ATTEMPTS = 8`, `LOCK_RETRY_BASE = 1.0`, `LOCK_RETRY_CAP = 30.0` (seconds); delay = min(cap, base * 2**n); sleep via module-level `_sleep` for tests.
* `_Conn.startup_retries` attribute (0 default). In `execute`, for BEGIN IMMEDIATE, loop attempts while the error message contains the lock text and attempts remain.
* `MssqlStore._initialize` sets `self.db.startup_retries` after `_open` (wrapping super) and resets it in finally.

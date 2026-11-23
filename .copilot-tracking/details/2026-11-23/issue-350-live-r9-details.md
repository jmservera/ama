# Issue 350 r9 details

Phase 2: in the `except Exception as e` of the `/api/assistants*` GET branch, `if is_write_lock_busy(e): raise`, else log `http-error GET <path> status=503 exc=<class>` and answer the existing 503. Phase 3: the test patches `assistants.registry` to raise a driver-shaped lock error and a RuntimeError carrying a secret string; asserts 503 with `Retry-After: 5` plus `cause=sql-write-lock-busy`, then plain 503 with the class logged and no secret in body or log.

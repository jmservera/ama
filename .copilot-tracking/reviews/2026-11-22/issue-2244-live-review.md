# Review (executed once): issue 2244

Outcome: conformant with routed open work.
Boundary: src/core mssqlstore.py diff and the new test file, against plan and critique dispositions.

* Retry is limited to start-up and to the exact lock-failure text; other errors and the last timeout re-raise (checked in code and tests).
* A partial BEGIN is rolled back before each retry (`_abandon_partial_begin` is called on every failure), so no open transaction leaks.
* Simulated-MSSQL tests in test_sqlstore found a sqlite connection in `_initialize`; fixed with an `isinstance(db, _Conn)` guard; those tests now pass.

Routed open work: read-only schema check before the lock; probe window versus worst-case 3.5 min start; live proof after the next image rollout.

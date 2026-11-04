# Details: slice 1

* app.py: add `BUSY`, `RETRY_AFTER_SECONDS`; `_route` sends them on bulkhead shed only.
* test_resident_demo_api.py: `test_concurrency_cap_returns_503_not_a_hang` asserts status, wording and header.

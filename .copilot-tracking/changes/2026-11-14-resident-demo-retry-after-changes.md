# Changes: resident demo bulkhead retry guidance (#1054)

* src/api/src/zava_forward/api/resident_demo/app.py: Retry-After 2, `retry_after_seconds`, clearer BUSY text.
* src/api/src/zava_forward/api/resident_demo/web/demo.js: banner states the wait from the server hint.
* src/api/tests/test_resident_demo_api.py: asserts new key and text.
* Validation (src/api): mypy rc=0 (266 files), ruff check and format clean, 60 tests OK. Not run: hosted CI, browser harness. Repo-root `ruff format` has pre-existing unrelated failures.

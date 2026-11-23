# Plan: issue 462 fourth pass

* Phase 1: add a regression test asserting the Server header contains no Python version (fails first).
* Phase 2: set `sys_version = ""` on the resident demo Handler.
* Phase 3: run `test_resident_demo_api`, mypy, ruff; write research note r9, index row and log entry; commit locally.

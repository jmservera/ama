# Issue 129 slice 2 changes

* Added src/core/src/zava_forward/core/learning_test_bundles.py and src/core/tests/test_learning_test_bundles.py.
* Updated the protocol, docs/reference/README.md row and docs/reference/log.md.
* Validation run: PYTHONPATH=src:tests unittest for the new module (7 tests OK), ruff check and format check, mypy --cache-dir=/tmp/mypy-530 on the two files. Not run: gate, benchmarks, full suites, hosted CI.

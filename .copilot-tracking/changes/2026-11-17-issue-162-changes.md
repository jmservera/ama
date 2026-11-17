# Issue 162 changes

* src/api/tests/test_chat_isolation.py: added `test_foreign_memory_item_cannot_be_edited_or_deleted` (cross-user memory edit/delete and thread ask/proposals return 404 with spoofed owner fields; owner's memory unchanged).
* No Core or server change. Criterion 6 (OD-46 policy) untouched and unmet.

Validation (src/api, `PYTHONPATH=../core/tests:../agents/tests:tests`):
* `python3 -m unittest test_chat_isolation test_regulatory_chat_api -q`: 44 OK before; `test_chat_isolation`: 33 OK after.
* `ruff format --isolated --line-length 100 --check tests/test_chat_isolation.py`: fails, pre-existing (file was unformatted on main eb51af5c9 before this change); not reformatted to keep the diff surgical.
* mypy: not applicable (test-only, tests not in src-ci mypy scope). Heavy gate and services not run (lock).
* Note: the editable install resolves zava_forward from the main checkout; sources are identical at base.

# Changes

* src/core/tests/test_chat_case_answers.py: typed `detail`.
* src/api/checks/case_journey_browser_check.py: `tab_buttons` helper, three loops use index-based locators.
* tools/__pycache__/*.pyc: removed from the index.

Validation: mypy clean; core test 4 OK; ruff/format/mypy clean on the check; journey check rc=0 with 0 FAIL, 4 runs.

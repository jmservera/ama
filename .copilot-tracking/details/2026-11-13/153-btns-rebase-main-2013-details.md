# Details: 153-btns-rebase-main-2013

* Api tests run with `PYTHONPATH=../core/tests:../agents/tests:tests` from `src/api` (test_case_journey imports a sibling module).
* Tools: ruff, mypy from the venv; install `-e src/core -e src/agents -e "src/api[dev]"`, playwright, mypy, ruff.

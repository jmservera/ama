# Changes: #108 Cycle 1 mypy fix

* src/core/tests/test_ai_consumption_skill_breakdown.py: bare `import test_ai_consumption as base`; `reference` imported from source.
* Validation: mypy, ruff check, ruff format --check, test_ai_consumption*.py (52 tests) all pass. Refs #108.

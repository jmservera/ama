# Research: #108 Cycle 1 mypy duplicate module

mypy_path = [src, tests] with explicit_package_bases: test_ai_consumption_skill_breakdown.py imported `from tests import test_ai_consumption`, so the file was seen as both `test_ai_consumption` (via safety test) and `tests.test_ai_consumption`. Refs #108.

# Changes: evidence only
No source changes. Tests: 124 pass (python3 -m unittest infra.tests.test_setup_entra). mypy setup-entra.py clean (--cache-dir=/tmp/mypy-358). ruff on the two files reports 15 pre-existing findings, untouched.
Mutation: guard forced valid with "or True" -> 7 failures; reverted.
Not run: gate, benchmarks, full suites, live Azure.

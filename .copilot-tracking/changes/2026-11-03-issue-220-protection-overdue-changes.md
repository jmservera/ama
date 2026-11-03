# Changes: issue 220 protection and overdue slice, 2026-11-03

* `src/core/src/zava_forward/core/challenges.py`: PROTECTION, `view()["protection"]`, `overdue()`.
* `src/core/tests/test_challenges.py`: two tests (16 pass).
* `src/core/README.md`: documented both.
* Validation run: test_challenges (16 pass), ruff check and format, mypy (cache /tmp/mypy-220).
* Not run: gate, full suites, benchmarks (coordinator runs gates).

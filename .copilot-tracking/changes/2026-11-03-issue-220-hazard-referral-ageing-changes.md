# Changes: issue 220 hazard referral ageing

* src/core/src/zava_forward/core/challenges.py: `received_on`, `hazard_referrals_overdue`.
* src/core/tests/test_challenges.py: 2 new tests (18 pass).
* src/core/README.md: documented the flag.
* Validation run: test_challenges, ruff check/format, mypy (--cache-dir=/tmp/mypy-220). Not run: gate, benchmarks, full suites.

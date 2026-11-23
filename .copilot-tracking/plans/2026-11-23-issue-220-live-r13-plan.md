# Plan, issue 220 r13

* Replace `_normalise_key` in `src/core/src/zava_forward/core/challenges.py` with NFKC, camelCase split, format-character removal and non-alphanumeric run collapse.
* Add a regression test in `src/core/tests/test_challenge_no_retaliation_220.py`.
* Run 220 core tests, ruff, mypy on the module; write note, log entry, changes, review.

Critique (executed once): risk of false positives on benign keys such as `consent_given` is nil (exact match on the normalised set only); `Consent` alone is already forbidden. Verdict: proceed.

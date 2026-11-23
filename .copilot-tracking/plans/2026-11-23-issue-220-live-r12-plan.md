# Plan, issue 220 r12

Critique (executed once): risk is false positives on legitimate keys; normalisation only maps case and separators, so no existing key changes meaning. Verdict: proceed. Tier FULL not required beyond core mypy/ruff and the 220 core tests; src change is small but touches a safeguard, so run the full core test suite.

1. Add `_normalise_key` in challenges.py; use it in reject_adverse_mapping and assert_no_adverse_challenge_effects.
2. Add a regression test in test_challenge_no_retaliation_220.py.
3. Run core tests, mypy, ruff. Write a research note with per-criterion table.

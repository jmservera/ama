# Plan: #153 AC3

1. RED: add test in test_content_standard.py parsing HELD_CHECK_ERRORS; every entry needs a reason sentence, `Owner:` and `Next action:`, no banned words.
2. GREEN: add `Owner:` to 400 (signed-in reviewer), 404 (application support), 409 (signed-in reviewer), 502 (application support) in role-screens.js. Keep other lines untouched.
3. Validate: targeted unittests, ruff, mypy. Review, commit.

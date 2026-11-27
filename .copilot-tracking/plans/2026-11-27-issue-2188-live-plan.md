# Plan: issue 2188 live (2026-11-27)

1. Harden `validate_retries`: sha256 must be 64-hex and the log must be a key of `files`.
2. Extend `test_validate_retries_rejects_tampered_or_forged_records` with None, short and absent-file cases (fail before, pass after).
3. Run retry tests, ruff, mypy; add research note, index entry and log entry.

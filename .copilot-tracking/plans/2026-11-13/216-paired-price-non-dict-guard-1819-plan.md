# Plan: paired price non-Mapping guard

1. In `cost_per_accepted_check`, treat non-Mapping `price_source`/`usage` as malformed: add `price_source not a mapping` / `usage not a mapping` to missing_inputs; skip nested key checks for it.
2. Replace the TypeError fallback with `_number` validation per rate/usage key: report `price_source.X not numeric` / `usage.X not numeric` (bool, str, non-finite).
3. Tests: non-Mapping (str, list, int, bool True) for each; missing nested keys; non-numeric rates; all return Unknown with named input.
4. Validate: test_paired*, ruff check/format, mypy.

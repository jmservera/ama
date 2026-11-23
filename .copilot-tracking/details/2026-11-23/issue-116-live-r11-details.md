# Details 2026-11-23, issue 116 live r11

* Phase 1: test calls `evidence` with each payload and asserts outcome `input-refused`, meter and `urlopen` untouched.
* Phase 2: compute UTF-8 length through a helper that converts `UnicodeEncodeError` to `InputRefused`.
* Phase 3: `python3 -m unittest` for the three core boundary tests and three api AI tests; ruff check and format on changed files; `python3 -m mypy` in `src/core`.

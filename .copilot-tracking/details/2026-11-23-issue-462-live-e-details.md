# Details: issue 462 fifth pass

Phase 2: in `_body()` change the guard to require `length.isascii() and length.isdigit()`. Test: with a valid CSRF cookie and header, send a raw non-ASCII digit `Content-Length` (latin-1) to `/demo/login`; expect HTTP 401 with the generic denial instead of a dropped connection; a normal login must still work.

Phase 3: `unittest` for `test_resident_demo_api`, `test_resident_demo_check`, `test_resident_demo_script`, `test_resident_preview_api`; `python3 -m mypy` in `src/api`; `ruff check` and `ruff format --isolated --line-length 100 --check` on the two changed files.

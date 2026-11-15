<!-- markdownlint-disable-file -->
# Changes: C1 mypy typing correction

* Modified only `src/api/tests/test_ai_controlled_record_non_mutation.py` (annotations, casts, six narrow ignores). No behaviour change; `src/api/pyproject.toml` and siblings untouched.
* Validation (focused tier, local): `mypy` in `src/api`: Success, no issues in 245 source files (was 74 errors); ruff check and format --check pass; `unittest tests.test_ai_controlled_record_non_mutation`: 9 tests OK.
* Not run: full local gate, hosted CI, independent exact-head re-review.

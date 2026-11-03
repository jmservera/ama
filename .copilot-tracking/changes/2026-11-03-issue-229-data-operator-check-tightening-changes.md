# Changes: issue #229 slice 3

* `src/api/checks/data_operator_browser_check.py`: region-scoped assertions, reopened reason assertion, `ZF_AXE_REQUIRED=1` fail-on-skip.
* `src/api/README.md`: PARTIAL exit-code and RESULT-line note.

## Validation run

* Browser check with pinned axe 4.10.3: RESULT PASS, new assertions pass.
* With ZF_AXE_REQUIRED=1 and no axe file: AssertionError as intended.
* ruff check and mypy (cache /tmp/mypy-229): clean.

## Not run

Gate, full suites, benchmarks, unit suites (no production code changed). `ruff format --check` reports the file was already unformatted before this change; not reformatted to keep the diff small. No assistive-technology or human review.

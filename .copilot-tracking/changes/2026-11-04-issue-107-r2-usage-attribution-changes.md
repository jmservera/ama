<!-- markdownlint-disable-file -->
# Issue 107 R2 usage attribution: changes

* `src/core/src/zava_forward/core/ai_consumption.py`: `capability_usage`, `by_capability` in the report.
* `src/core/tests/test_ai_consumption.py`: 2 tests.
* `src/core/README.md`, `docs/reference/log.md`: documentation.

## Validation (focused tier)

| Command | Result |
| --- | --- |
| `PYTHONPATH=src:tests python3 -m unittest test_ai_consumption test_ai_consumption_demo test_ai_consumption_safety -q` (src/core) | 42 OK |
| `ruff check` on the two changed Python files | clean |
| `mypy --cache-dir=/tmp/mypy-107 ai_consumption.py` | no issues |

Not run: gate, benchmarks, full suites, MSSQL, hosted CI. The installed editable packages point at another worktree, so PYTHONPATH=src was used.

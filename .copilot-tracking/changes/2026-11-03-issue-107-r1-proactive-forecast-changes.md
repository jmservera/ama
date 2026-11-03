<!-- markdownlint-disable-file -->
# Issue 107 R1 proactive forecast: changes

* `src/core/src/zava_forward/core/assistants.py`: `_task_id`, `forecast`.
* `src/api/src/zava_forward/api/server.py`: `GET /api/assistants/forecast`.
* `src/api/tests/test_assistants.py`: 4 tests.
* `src/agents/README.md`, `docs/reference/log.md`: documentation.

## Validation (focused tier)

| Command | Result |
| --- | --- |
| `test_assistants test_assistant_release` (src/api, PYTHONPATH to src dirs) | 163 OK, 57 skipped (MSSQL not enabled) |
| `test_dispatch` (src/agents) | 15 OK |
| `ruff check` on touched files | clean |
| `ruff format --check` | touched files were already unformatted on main; not reformatted to keep the diff small |
| `mypy --cache-dir=/tmp/mypy-107 -m zava_forward.core.assistants` | no errors in assistants.py; 2 existing errors in doc_controls.py and signoffs.py |

Not run: gate, benchmarks, full suites, MSSQL tests, hosted CI. Not security, infrastructure, SQL or deployment tier.

## Acceptance criteria status

Proven earlier: base 1 to 5, RAI 2, 4, 6, 7, 9, Tokenomics 1. Advanced here: Tokenomics 3 (code and tests; no real usage evidence). Unmet: RAI 1, 3, 5, 8; Tokenomics 2; Tokenomics 3 is not claimed complete until reviewed. Hence `Refs #107`.

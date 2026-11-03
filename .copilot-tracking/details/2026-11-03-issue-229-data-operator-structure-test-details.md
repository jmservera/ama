# Details: issue #229 slice 6

* Phase 1: reuse the asset-board test pattern. Walk the rendered trees (populated, empty, reopen, no handoff, no return); assert section class, h2 first, no h1, table captions, th scope col, no onclick or role-switch; scan the data-operator block of role-screens.js for simulator terms.
* Validation: `python3 -m unittest tests.test_data_operator_screen` from src/api; ruff check and format check; mypy --strict with --cache-dir=/tmp/mypy-229.

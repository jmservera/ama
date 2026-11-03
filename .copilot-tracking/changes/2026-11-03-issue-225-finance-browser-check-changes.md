# Changes: issue 225 finance browser check (2026-11-03, r1)

* `src/api/checks/finance_screens_browser_check.py`: new check (3 stories).
* `src/api/README.md`: paragraph for the check.
* `docs/reference/log.md`: appended entry.

No divergences. Two fixes while running: the fixture invoice has no matched commitment, so the expected quantity phrase is "Unknown. No matched commitment."; a grant stage was added so the funding screen renders a table region.

## Validation (focused tier)

Ran: `python -m checks.finance_screens_browser_check` with pinned axe 4.10.3 (SHA-256 verified): COMPLETE, all PASS, zero axe violations on `main` at 1280 px for all three role/screen stories, axe incomplete lists empty; `unittest tests.test_finance_grants_screens` 17 OK; ruff check and format clean; mypy --cache-dir=/tmp/mypy-225 clean.
Packages were used through PYTHONPATH (no editable install) to avoid ignored egg-info files; generated `__pycache__` and caches removed.
Not run: complete gate, full suites, SQL tests, assistive technology, manual screen reader, hosted CI, independent review.

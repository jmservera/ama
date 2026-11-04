# Details: issue 100 r2

* Roots are counted per capability; a request root spanning capabilities counts in each. Accepted proposals use the existing acceptance rule (eligible, not unresolved, accept or edit-accept).
* The screen never shows a per-capability cost, even if a field is supplied, because no capability-level price or bill is recorded. Token totals are shown for proposals with known tokens only, beside the count of such proposals.
* No new API route: `/api/ai/report` already passes the consumption payload through.
* Validation: focused unittest, ruff check and format, mypy --cache-dir=/tmp/mypy-100 for src/core and src/api (tests included).

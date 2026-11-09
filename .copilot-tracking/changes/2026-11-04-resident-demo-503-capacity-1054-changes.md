---
title: Changes, #1054 slice 3
---

* app.py decision comment; two tests added.
* Run: test_resident_demo*.py (57 OK), ruff check/format, mypy --cache-dir=/tmp/mypy-530 (47 pre-existing environment import errors for playwright and similar, none in touched files). Not run: gate, benchmarks, full suites, browser, live burst.

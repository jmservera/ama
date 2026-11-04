---
title: Changes for #74 home case API and screen slice
ms.date: 2026-11-04
---

* Added: `src/api/tests/test_home_case_api.py`.
* Modified: `src/api/src/zava_forward/api/server.py`, `src/api/src/zava_forward/api/web/app.js`, `src/api/README.md`.
* Validation run: `test_home_case_api` and `test_buildings` (6 OK), `tests.test_home_case` in core, ruff, mypy (`--cache-dir=/tmp/mypy-530`), `node --check app.js`.
* Not run: browser check, complete gate, full suites, hosted CI, SQL Server, accessibility audit.
* Acceptance criteria: 1, 3, 4 already ticked (core). Criterion 2 is advanced (API and screen) but stays unmet: no browser, accessibility or independent review evidence, and building holds/works/costs are shown from existing building records only.

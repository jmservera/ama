---
title: Changes for #74 home case browser evidence slice
ms.date: 2026-11-04
---

* Added: `src/api/checks/home_case_browser_check.py`.
* Modified: `src/api/src/zava_forward/api/web/app.js`, `src/api/tests/test_home_case_api.py`, `src/api/README.md`.
* Run: `test_home_case_api` and `test_buildings` (6 OK); browser check with pinned axe 4.10.3, all PASS; ruff check and format; mypy over src, tests and checks (`--cache-dir=/tmp/mypy-74`, 179 files); `node --check app.js`.
* Not run: complete gate, full suites, hosted CI, screen reader or keyboard manual review, benchmarks.
* Acceptance criteria: 1, 3, 4 already ticked. Criterion 2 is advanced with browser, axe and reflow evidence but stays unmet: building record versioning not delivered, no manual accessibility review, no independent review, no hosted evidence.

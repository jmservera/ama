---
title: Changes for #462 resident demo journey slice
ms.date: 2026-11-04
---

* Changed: plain-language sensor statuses, gauge note and slow-start notice (see details).
* Tests: `test_resident_sensors` (9 passed); `test_resident_demo_api`, `test_resident_api`, `test_resident_demo_check` (66 passed, 1 skipped); `ruff check` clean on core and api; `ruff format --check` clean on the two edited Python files; `node --check demo.js` passed.
* mypy with `--cache-dir=/tmp/mypy-530` on `resident_showcase.py`: only two errors, in unrelated untouched files (`doc_controls.py`, `signoffs.py`), caused by the missing optional Azure stubs in this environment. No error in changed code.
* Not run: browser checks (the Playwright check script edits are unexecuted), complete gate, benchmarks, full suites, Docker, SQL parity, live deploy.
* Unmet acceptance criteria on #462: 1, 2, 5, 6, 7 (retrospective process conditions and owner-run live authenticated checks). Criteria 3, 4, 8 were already ticked. Nothing is ticked by this slice.
* Divergences: none. Deploy is needed to show the change on ca-resident-demo; not done, so a later owner-approved ACR push is required.

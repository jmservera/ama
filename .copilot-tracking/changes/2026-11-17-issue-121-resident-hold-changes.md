---
title: Issue 121 resident hold changes
date: 2026-11-17
---

* `src/api/tests/test_resident_aoai.py`: regression test, added before the fix; it failed on main (events reserve, token, transport on both paths). The implement-start witness records the source as already dirty because of this test edit.
* `src/api/src/zava_forward/api/resident_demo/aoai.py`: `dispatch_hold("tenant_identity")` at the start of `_answer` and `_question`; new allowlisted fallback reason `data_protection_hold`.
* `src/core/README.md`, `docs/reference/log.md`: documented.
* Environment note: the default editable install resolves to the main checkout, so tests ran with PYTHONPATH pointing at this worktree's `src/api/src`, `src/core/src` and `src/agents/src`. A first run without it passed the old code and was discarded.
* Validation (focused tier): test_resident_aoai 17 OK; test_resident_assistant_api 10 OK (discover); test_resident_assistant_provider 13 OK; test_resident_api 22 OK (1 skipped); test_resident_aoai_sql 8 skipped (needs SQL); core test_data_protection 18 OK; ruff format --isolated --line-length 100 --check and ruff check clean; mypy src/api clean (29 files).
* Not run: complete gate, full suites, hosted CI, SQL, browser (no UI change).
* No divergences from the plan.

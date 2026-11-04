# Phase details: issue 121 r6

* Phase 1: `data_protection` kind added to `get_kind` and `STAFF_GET`; handler returns `register_report(os.environ)`; GET only (POST yields 404).
* Phase 2: test in `src/api/tests/test_ai_tasks.py` checks 200, `dpo_reviewed` false, no reference echo, POST 404.
* Phase 3: `src/core/README.md` note; `docs/reference/log.md` entry.
* Phase 4: unittest, ruff, mypy.

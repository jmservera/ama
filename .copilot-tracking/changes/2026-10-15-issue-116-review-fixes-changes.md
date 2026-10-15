# Issue 116 review fixes: changes

* mvp/zavaforward_mvp/ai_tasks.py: contact label gated on `reason_ok`.
* mvp/zavaforward_mvp/assistants.py: appointment outcome gated by role need; unknown outcomes held.
* mvp/zavaforward_mvp/projection.py: recursive `hold_notes`, `status_only`, contractor appointment outcome held.
* mvp/tests/test_role_endpoint_inventory.py: canary tests for list, export, search, case views, citations and assistant source.

Validation: `cd mvp && PYTHONPATH=. python3 -m unittest discover -s tests`: 581 tests, OK (84 skipped).

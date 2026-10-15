---
title: Issue 122 service continuity changes
---

* Added `continuity.py`, `tests/test_continuity.py`.
* Modified `ai.py` (gate hook), `ai_tasks.py` (Quarantined status, epoch check, review gate), `assistants.py` (db-level suspension checks, quarantine, views, export), `server.py` (routes), `store.py`, `sqlstore.py` (persist `continuity`), `mvp/README.md`.
* Validation: `cd mvp && PYTHONPATH=. python3 -m unittest discover -s tests` gives 531 tests OK (85 skipped). `tools/rename-zava-tests.py` fails here only on missing `pptx`/`PIL` modules, as it does without these changes.
* No knowledge-base files changed, so `docs/reference` index and log are untouched.

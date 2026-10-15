---
title: Issue 107 release admission changes
description: Changes made for release admission
ms.date: 2026-10-15
---

* Added `mvp/zavaforward_mvp/assistant_release.py`.
* Changed `assistants.py`, `sqlstore.py`, `server.py`, `mvp/README.md`.
* Tests: added `test_assistant_release.py`, `release_support.py`; updated test_assistants, test_continuity, test_mvp, test_ai_tasks, test_role_endpoint_inventory.
* Validation: `cd mvp && PYTHONPATH=. python3 -m unittest discover -s tests` gave 716 tests OK (92 skipped, SQL Server conditional).
* No knowledge base file changed, so no log entry.

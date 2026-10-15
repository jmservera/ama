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

## PR 287 review fixes (2026-10-15)

* Fixed SQL Server CI: dialect-guarded release DDL in `tests/release_support.py`; `_epoch_sql` hook in `sqlstore.py`/`mssqlstore.py`.
* Gate now receives the deployment actually called and compares all bound versions (`ai_registry.legacy_binding`).
* Legacy completion recheck added in `ai.py` (`run`, `look_at`).
* Returned-model wording corrected in `assistants.py` and `mvp/README.md`; open items listed.
* Tests added: deployment binding, version binding, completion recheck. Full suite: 719 tests OK (92 skipped; SQL Server tests run in CI only).

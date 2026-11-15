---
title: Issue 201 epic legacy-path details
ms.date: 2026-11-14
---

* Execution patterns (`PYTHONPATH=mvp`, `cd mvp`, `working-directory: mvp`, `zavaforward_mvp` imports) always fail except doc lines with a prohibition word.
* Path patterns `mvp/` or `prototype/` fail unless in docs or comment lines carrying an archive/retired/moved marker, or a negative `git ls-files mvp/data` guard.
* `cutover_audit.py` and its test are exempt as retirement records.

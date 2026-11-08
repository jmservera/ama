---
title: Issue 79 details, r24 directory-sync audit correction
ms.date: 2026-11-07
---

* Files: `ranking_publication.py` (error class, wrap `_fsync_dir`), `store.py` (`publish_ranking_snapshot`), `server.py` (route handler), tests in `test_ranking_publication.py` and `test_ranking_publication_wiring.py`, `src/core/README.md` note, log entry.
* Checks: unittest selectors from r20, pinned Ruff 0.17.1 and mypy 2.4.0 with scratch caches `/mnt/ama-gates/g79-dirsync-audit-1107`, `PYTHONDONTWRITEBYTECODE=1`. No FULL, SQL or browser.

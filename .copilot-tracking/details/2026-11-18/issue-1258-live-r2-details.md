---
title: Details for issue 1258 (live demo run 2)
ms.date: 2026-11-18
---

* Phase 1: `cd src/core; PYTHONPATH=tests python3 -m unittest test_ranking_publication test_ranking_publication_runner`; `python3 -m mypy`; ruff format (isolated, line length 100) and check on `ranking_publication.py`.
* Phase 2: `strace -f -y -e trace=mkdir,mkdirat,link,linkat,fsync,... python3 publish-first-run.py <tmp>` on ext4; second run with `-e inject=fsync:error=EIO:when=4` (the fourth fsync is ancestor `a`). Temp folders removed after.
* Phase 3: `gh api` check-runs and workflow runs; `az containerapp show` filtered to ranking, archive and blob variables only (no secret values read).
* Phase 4: note `docs/reference/research/issue-1258-live-closure-r2-2026-11-18.md`; evidence folder alongside; README index and log entries.
* Out of scope: credentials, browser proof (no web surface), Azure writes, `rpi-checks.py --all`.

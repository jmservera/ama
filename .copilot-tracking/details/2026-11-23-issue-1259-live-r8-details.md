---
title: Details, issue 1259 live run 8
ms.date: 2026-11-23
---

Phase 1: create `locked/` with mode 0, archive below it, restore mode in cleanup, skip as root. Assert verify and schedule report `problem` with no latest or due, publish refused `archive_unreadable`, and no path in output.
Phase 2: `cd src/core && PYTHONPATH=src:tests python3 -m unittest test_ranking_publication_runner test_ranking_publication -q`; `python3 -m mypy`; `ruff check` and `ruff format --isolated --line-length 100 --check`.
Phase 3: docs/reference/research/2026-11-23-ranking-archive-unusable-1259-live-r8.md, README index row, log entry.

---
title: Issue 83 r1 changes
ms.date: 2026-11-03
---

* Added: handoff ageing, unaccepted-handoff listing, exception feed, three tests and a feed test.
* Docs: `src/core/README.md`, `docs/reference/log.md`.
* Validation run: handoff lifecycle (20 tests) and exception feed (6 tests) unittest; ruff check; mypy on the feed module and its test.
* Not run: gate, full suites, benchmarks, SQL Server replays, API or browser checks, mypy on workflows.py.

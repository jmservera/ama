---
title: Changes, issue 1259 live run 8
ms.date: 2026-11-23
---

Tier: FOCUSED (test-only, no `src/zava_forward` change).

* `src/core/tests/test_ranking_publication_runner.py`: four real-filesystem scenarios added to `UnusableArchivePathTests`.
* `docs/reference/research/2026-11-23-ranking-archive-unusable-1259-live-r10.md`, index row and log entry.

Validation: 110 tests OK; mutation fails 7 scenarios; ruff clean; mypy errors only in unrelated files.

| Criterion | Status |
| --- | --- |
| AC1 to AC3 (ticked) | Proven (unit, real filesystem) |
| AC4 regressions plus failing-first | Proven (tests, mutation, earlier failing-first note); owner ticks |
| AC5 RPI, FULL receipt, exact-head assessment, hosted checks | Unproven: nothing pushed, no hosted CI or independent assessment; no FULL receipt needed without src change |

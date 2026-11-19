---
title: Changes for issue 1258 (live)
ms.date: 2026-11-18
---

Tier: FOCUSED (documentation only; no `src/` change, so FULL is not triggered). Live Azure not used (not applicable).

Files: docs/reference/research/issue-1258-archive-ancestor-durability-2026-11-18.md (new), docs/reference/README.md, docs/reference/log.md.

Validation: `src/core` `PYTHONPATH=tests python3 -m unittest test_ranking_publication test_ranking_publication_runner` 110 OK; same module fails on `cd687abad^` and `python3 -m mypy` clean (both Observed; raw output not retained). Ruff format applies to no changed Python file.

| Criterion | Status |
| --- | --- |
| 1 Ancestor sync before confirm | Proven offline (mock order) |
| 2 Post-link failure committed_unconfirmed | Proven offline |
| 3 Syscall-order regression, fails pre-fix | Proven offline |
| 4 Retry/stage/audit/path-free/date intact | Proven offline |
| 5 FULL receipt, independent review, hosted checks | Unproven: process gates; no real crash proof |

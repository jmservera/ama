---
title: Issue 104 live plan details (2026-11-21)
ms.date: 2026-11-21
---

* Phase 3: from src/agents, `PYTHONPATH=src:tests:../core/src:../core/tests:../api/tests` with a throwaway venv holding opentelemetry-api and sdk 1.45.2, `python -m unittest test_epic104_bounded_ai_invariants test_candidate_comparison test_heldout_freeze`. Venv deleted afterwards.
* Phase 4: research note with a per-criterion table; index row in docs/reference/README.md; entry in docs/reference/log.md.
* Phase 5: a failure that shows a real defect would add a regression test and a fix under the full tier.
